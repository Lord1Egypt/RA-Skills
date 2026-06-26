import argparse
import json

from generate_summary_audio import generate_summary_audio
from meeting_memory import load_meeting_memory


def answer_meeting_question_audio(
    answer_text: str,
    output_path: str | None = None,
    voice_id: str | None = None,
    api_key: str | None = None,
) -> str:
    return generate_summary_audio(
        summary_text=answer_text,
        output_path=output_path,
        voice_id=voice_id,
        api_key=api_key,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate audio from a meeting Q&A answer.")
    parser.add_argument("--answer", required=True, help="Final answer text to convert to speech")
    parser.add_argument("--memory-path", help="Optional path to the saved meeting memory JSON")
    parser.add_argument("--output-path", help="Local output path for the mp3 file")
    parser.add_argument("--voice-id", help="SenseAudio voice identifier")
    parser.add_argument("--api-key", help="SenseAudio API key. Falls back to SENSEAUDIO_API_KEY when omitted.")
    args = parser.parse_args()

    if args.memory_path:
        try:
            memory = load_meeting_memory(args.memory_path)
        except FileNotFoundError as exc:
            print(f"ERROR: {exc}")
            return 1
    else:
        memory = None

    result = answer_meeting_question_audio(
        answer_text=args.answer,
        output_path=args.output_path,
        voice_id=args.voice_id,
        api_key=args.api_key,
    )
    if result.startswith("ERROR:"):
        print(result)
        return 1

    parsed = json.loads(result)
    if memory:
        parsed["memory_source_location"] = memory.get("source_location")
        parsed["memory_saved_at"] = memory.get("saved_at")
    print(json.dumps(parsed, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
