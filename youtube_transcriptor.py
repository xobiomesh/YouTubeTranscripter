from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re

def list_transcripts(youtube_url):
    # Extract the video ID from the URL
    video_id = re.search(r'(?<=v=)[^&#]+', youtube_url)
    video_id = video_id.group() if video_id else None

    if video_id is not None:
        try:
            # Get the available transcripts for the video
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            print("Available languages:")
            available_languages = []

            # Display available languages and their types
            for transcript in transcript_list:
                if transcript.is_generated:
                    print(f"{transcript.language} ({transcript.language_code}) - Auto-generated")
                else:
                    print(f"{transcript.language} ({transcript.language_code}) - Manually created")
                available_languages.append(transcript.language_code)

            return available_languages, transcript_list
        except TranscriptsDisabled:
            print("Transcripts are disabled for this video.")
        except NoTranscriptFound:
            print("No transcripts found for this video.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Invalid YouTube URL")

    return None, None

def get_transcript(transcript_list, language_code):
    try:
        # Fetch the transcript in the chosen language
        transcript = transcript_list.find_transcript([language_code]).fetch()
        return transcript
    except Exception as e:
        print(f"An error occurred while fetching the transcript: {e}")
        return None

def clean_text(text):
    # Remove extra whitespace and unwanted symbols but keep accent characters
    cleaned_text = re.sub(r'[^\w\sÀ-ÿ]+', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def main():
    input_url = input("Enter the YouTube URL: ")
    print(f"Fetching transcript info for URL: {input_url}")

    # Get the list of available transcripts
    available_languages, transcript_list = list_transcripts(input_url)
    
    if available_languages:
        language_code = input("Enter the language code you want to use: ")
        if language_code in available_languages:
            print(f"Fetching transcript in {language_code}...")

            # Get the transcript in the chosen language
            transcript = get_transcript(transcript_list, language_code)
            if transcript:
                print(f"Transcript in {language_code}:")
                transcript_text = ""
                for entry in transcript:
                    cleaned_text = clean_text(entry['text'])
                    print(cleaned_text)
                    transcript_text += cleaned_text + "\n"
                
                save_to_file = input("Do you want to save the transcript to a text file? (yes/no): ").lower()
                if save_to_file == 'yes':
                    file_name = input("Enter the filename (with .txt extension): ")
                    try:
                        with open(file_name, 'w', encoding='utf-8') as file:
                            file.write(transcript_text)
                        print(f"Transcript saved to {file_name}")
                    except Exception as e:
                        print(f"An error occurred while saving the file: {e}")
        else:
            print(f"Invalid language code: {language_code}")
    else:
        print("No available transcripts found.")

if __name__ == "__main__":
    main()
