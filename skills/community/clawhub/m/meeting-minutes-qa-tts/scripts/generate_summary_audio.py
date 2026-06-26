import argparse

from generate_meeting_audio import generate_meeting_audio


def generate_summary_audio(
    summary_text: str,
    output_path: str | None = None,
    voice_id: str | None = None,
    api_key: str | None = None,
) -> str:
    return generate_meeting_audio(
        input_text=summary_text,
        output_path=output_path,
        mode="full_text",
        voice_id=voice_id,
        api_key=api_key,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate TTS audio directly from in-memory summary text.")
    parser.add_argument("--text", required=True, help="Summary text to convert to speech")
    parser.add_argument("--output-path", help="Local output path for the mp3 file")
    parser.add_argument("--voice-id", help="SenseAudio voice identifier")
    parser.add_argument("--api-key", help="SenseAudio API key. Falls back to SENSEAUDIO_API_KEY when omitted.")
    args = parser.parse_args()

    result = generate_summary_audio(
        summary_text=args.text,
        output_path=args.output_path,
        voice_id=args.voice_id,
        api_key=args.api_key,
    )
    print(result)
    return 0 if not result.startswith("ERROR:") else 1


if __name__ == "__main__":
    raise SystemExit(main())
