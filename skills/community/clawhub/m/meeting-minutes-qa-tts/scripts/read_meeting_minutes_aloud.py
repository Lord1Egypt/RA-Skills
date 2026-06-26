import argparse

from generate_meeting_audio import generate_meeting_audio, read_text_source


def read_meeting_minutes_aloud(
    location: str,
    output_path: str | None = None,
    mode: str = "full_text",
    voice_id: str | None = None,
    api_key: str | None = None,
) -> str:
    input_text = read_text_source(location)
    if input_text.startswith("ERROR:"):
        return input_text

    return generate_meeting_audio(
        input_text=input_text,
        output_path=output_path,
        mode=mode,
        voice_id=voice_id,
        api_key=api_key,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Read meeting minutes and generate audio.")
    parser.add_argument("--location", required=True, help="Local file path or URL containing meeting text")
    parser.add_argument(
        "--mode",
        default="full_text",
        choices=["action_items", "decisions", "full_text", "summary"],
        help="Text selection mode",
    )
    parser.add_argument("--output-path", help="Local output path for the mp3 file")
    parser.add_argument("--voice-id", help="SenseAudio voice identifier")
    parser.add_argument("--api-key", help="SenseAudio API key. Falls back to SENSEAUDIO_API_KEY when omitted.")
    args = parser.parse_args()

    result = read_meeting_minutes_aloud(
        location=args.location,
        output_path=args.output_path,
        mode=args.mode,
        voice_id=args.voice_id,
        api_key=args.api_key,
    )
    print(result)
    return 0 if not result.startswith("ERROR:") else 1


if __name__ == "__main__":
    raise SystemExit(main())
