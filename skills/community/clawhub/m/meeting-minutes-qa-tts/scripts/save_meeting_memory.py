import argparse
import json

from meeting_memory import save_meeting_memory
from read_meeting_text import read_text_source


def main() -> int:
    parser = argparse.ArgumentParser(description="Save meeting text and summary into local memory.")
    parser.add_argument("--location", required=True, help="Local file path or URL containing meeting text")
    parser.add_argument("--summary", required=True, help="Short summary text for the meeting")
    parser.add_argument("--memory-path", help="Optional path for the saved meeting memory JSON")
    args = parser.parse_args()

    meeting_text = read_text_source(args.location)
    if meeting_text.startswith("ERROR:"):
        print(meeting_text)
        return 1

    saved_path = save_meeting_memory(
        source_location=args.location,
        meeting_text=meeting_text,
        summary_text=args.summary,
        memory_path=args.memory_path,
    )
    print(json.dumps({"status": "ok", "memory_path": saved_path}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
