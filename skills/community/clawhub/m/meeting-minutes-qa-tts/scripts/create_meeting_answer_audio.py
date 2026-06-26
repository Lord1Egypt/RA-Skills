import argparse
import json

from answer_meeting_question_audio import answer_meeting_question_audio
from meeting_memory import default_memory_path, load_meeting_memory


def create_meeting_answer_audio(
    answer_text: str,
    output_path: str,
    api_key: str | None = None,
    voice_id: str | None = None,
    memory_path: str | None = None,
) -> str:
    memory: dict = {}
    resolved_memory_path = memory_path or str(default_memory_path())
    if memory_path:
        memory = load_meeting_memory(memory_path)
    else:
        try:
            memory = load_meeting_memory()
        except FileNotFoundError:
            memory = {}

    audio_result = answer_meeting_question_audio(
        answer_text=answer_text,
        output_path=output_path,
        voice_id=voice_id,
        api_key=api_key,
    )
    if audio_result.startswith("ERROR:"):
        return audio_result

    parsed = json.loads(audio_result)
    parsed["text_answer"] = answer_text
    parsed["memory_path"] = resolved_memory_path
    parsed["memory_source_location"] = memory.get("source_location")
    parsed["memory_loaded"] = bool(memory)
    return json.dumps(parsed, ensure_ascii=False, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create answer audio for a meeting question.")
    parser.add_argument("--answer", required=True, help="Answer text produced in the current conversation")
    parser.add_argument("--output-path", required=True, help="Local output path for the answer mp3 file")
    parser.add_argument("--memory-path", help="Optional path to the saved meeting memory JSON")
    parser.add_argument("--voice-id", help="SenseAudio voice identifier")
    parser.add_argument("--api-key", help="SenseAudio API key. Falls back to SENSEAUDIO_API_KEY when omitted.")
    args = parser.parse_args()

    try:
        result = create_meeting_answer_audio(
            answer_text=args.answer,
            output_path=args.output_path,
            api_key=args.api_key,
            voice_id=args.voice_id,
            memory_path=args.memory_path,
        )
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(result)
    return 0 if not result.startswith("ERROR:") else 1


if __name__ == "__main__":
    raise SystemExit(main())
