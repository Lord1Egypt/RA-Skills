#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: meeting_summary.py input.txt output.json")
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    lines = [line.strip() for line in input_path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    summary = {
        "summary": " ".join(lines[:3])[:500],
        "key_points": lines[:5],
        "open_questions": [line for line in lines if "?" in line][:5],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote meeting summary to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
