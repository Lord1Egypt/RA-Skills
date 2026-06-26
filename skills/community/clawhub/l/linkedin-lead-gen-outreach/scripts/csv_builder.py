#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

FIELDS = [
    "first_name",
    "last_name",
    "full_name",
    "linkedin_url",
    "title",
    "company",
    "location",
    "keyword_match",
    "business_potential_note",
    "personalization_note",
    "score_total",
    "priority",
    "score_reason",
    "message_v1",
    "campaign_name",
    "owner",
    "source",
    "status",
    "next_action",
]


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: csv_builder.py input.json output.csv")
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    try:
        data = json.loads(input_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {input_path}: {exc}")
        return 1

    if not isinstance(data, list):
        print("Input JSON must be a list of lead objects")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in data:
            if not isinstance(row, dict):
                print("Each lead entry must be a JSON object")
                return 1
            clean = {field: row.get(field, "") for field in FIELDS}
            writer.writerow(clean)

    print(f"Wrote {len(data)} rows to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
