#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

VALID_STATUS = {"to_review", "approved", "ready_for_outreach", "contacted", "replied", "disqualified"}
VALID_PRIORITY = {"high", "medium", "low"}


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: sheets_prep.py input.csv output.csv")
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    required = ["priority", "status", "next_action"]
    for field in required:
        if field not in fieldnames:
            fieldnames.append(field)

    for row in rows:
        priority = (row.get("priority") or "medium").strip().lower()
        status = (row.get("status") or "to_review").strip().lower()
        row["priority"] = priority if priority in VALID_PRIORITY else "medium"
        row["status"] = status if status in VALID_STATUS else "to_review"
        row["next_action"] = (row.get("next_action") or "review").strip() or "review"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Normalized {len(rows)} rows into {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
