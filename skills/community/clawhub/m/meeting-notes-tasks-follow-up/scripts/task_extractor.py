#!/usr/bin/env python3
import csv
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: task_extractor.py input.txt output.csv")
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    lines = [line.strip() for line in input_path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    tasks = []
    for line in lines:
        lower = line.lower()
        if any(token in lower for token in ["todo", "action", "next step", "follow up", "need to", "will "]):
            tasks.append({
                "task": line,
                "owner": "unassigned",
                "status": "todo",
                "note": "extracted from meeting notes",
            })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["task", "owner", "status", "note"])
        writer.writeheader()
        writer.writerows(tasks)

    print(f"Extracted {len(tasks)} tasks to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
