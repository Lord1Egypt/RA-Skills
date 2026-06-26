import argparse
import json

from generate_summary_audio import generate_summary_audio
from meeting_memory import save_meeting_memory
from read_meeting_text import read_text_source


def create_meeting_summary_audio_session(
    location: str,
    summary_text: str,
    output_path: str,
    api_key: str | None = None,
    voice_id: str | None = None,
    memory_path: str | None = None,
) -> str:
    meeting_text = read_text_source(location)
    if meeting_text.startswith("ERROR:"):
        return meeting_text

    saved_memory_path = save_meeting_memory(
        source_location=location,
        meeting_text=meeting_text,
        summary_text=summary_text,
        memory_path=memory_path,
    )

    audio_result = generate_summary_audio(
        summary_text=summary_text,
        output_path=output_path,
        voice_id=voice_id,
        api_key=api_key,
    )
    if audio_result.startswith("ERROR:"):
        return audio_result

    parsed = json.loads(audio_result)
    parsed["summary_text"] = summary_text
    parsed["memory_path"] = saved_memory_path
    return json.dumps(parsed, ensure_ascii=False, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create summary audio and save meeting memory.")
    parser.add_argument("--location", required=True, help="Local file path or URL containing meeting text")
    parser.add_argument("--summary", required=True, help="Summary text produced in the current conversation")
    parser.add_argument("--output-path", required=True, help="Local output path for the summary mp3 file")
    parser.add_argument("--memory-path", help="Optional path for the saved meeting memory JSON")
    parser.add_argument("--voice-id", help="SenseAudio voice identifier")
    parser.add_argument("--api-key", help="SenseAudio API key. Falls back to SENSEAUDIO_API_KEY when omitted.")
    args = parser.parse_args()

    result = create_meeting_summary_audio_session(
        location=args.location,
        summary_text=args.summary,
        output_path=args.output_path,
        api_key=args.api_key,
        voice_id=args.voice_id,
        memory_path=args.memory_path,
    )
    print(result)
    return 0 if not result.startswith("ERROR:") else 1


if __name__ == "__main__":
    raise SystemExit(main())
