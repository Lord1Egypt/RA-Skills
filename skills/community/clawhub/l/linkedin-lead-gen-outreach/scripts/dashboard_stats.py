#!/usr/bin/env python3
import csv
import json
import sys
from collections import Counter
from pathlib import Path

READY_STATUSES = {"approved", "ready_for_outreach", "contacted", "replied"}


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: dashboard_stats.py input.csv output.json")
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    priority_counter = Counter((row.get("priority") or "").strip().lower() for row in rows)
    title_counter = Counter((row.get("title") or "Unknown").strip() or "Unknown" for row in rows)
    location_counter = Counter((row.get("location") or "Unknown").strip() or "Unknown" for row in rows)
    status_counter = Counter((row.get("status") or "").strip().lower() for row in rows)

    with_signal = 0
    ready_for_outreach = 0
    for row in rows:
        if (row.get("personalization_note") or "").strip():
            with_signal += 1
        if (row.get("status") or "").strip().lower() in READY_STATUSES:
            ready_for_outreach += 1

    total = len(rows)
    stats = {
        "total_leads": total,
        "priority": {
            "high": priority_counter.get("high", 0),
            "medium": priority_counter.get("medium", 0),
            "low": priority_counter.get("low", 0),
        },
        "top_titles": title_counter.most_common(10),
        "top_locations": location_counter.most_common(10),
        "status": dict(status_counter),
        "personalization_coverage_pct": round((with_signal / total) * 100, 2) if total else 0.0,
        "ready_for_outreach": ready_for_outreach,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote dashboard stats to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
