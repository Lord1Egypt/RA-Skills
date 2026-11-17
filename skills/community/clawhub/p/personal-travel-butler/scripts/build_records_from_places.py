#!/usr/bin/env python3
"""Build compact Notion sync records from Markdown travel entries."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from notion_common import load_records, normalize_record, notion_dir, resolve_db, save_records  # noqa: E402
from travel_model import markdown_records, save_generated_indexes  # noqa: E402


SYNC_PRESERVE_FIELDS = ("notion_page_id", "last_synced_at")


def merge_markdown_records(db: Path, records: list[dict]) -> tuple[list[dict], dict[str, int]]:
    stats = {"added": 0, "updated": 0, "unchanged": 0}
    by_id = {record["id"]: normalize_record(record) for record in records}

    for markdown_record in markdown_records(db):
        record_id = markdown_record["id"]
        existing = by_id.get(record_id)
        if existing:
            merged = dict(markdown_record)
            for field in SYNC_PRESERVE_FIELDS:
                if existing.get(field):
                    merged[field] = existing[field]
            if existing.get("record_weight") == "detailed":
                merged["record_weight"] = "detailed"
                merged["detail_file"] = existing.get("detail_file")
            merged = normalize_record(merged)
            if merged == existing:
                stats["unchanged"] += 1
            else:
                stats["updated"] += 1
            by_id[record_id] = merged
        else:
            by_id[record_id] = normalize_record(markdown_record)
            stats["added"] += 1

    return list(by_id.values()), stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=None, help="Path to travel-db.")
    parser.add_argument("--apply", action="store_true", help="Write _records.jsonl, _index.md, and generated indexes.")
    args = parser.parse_args()

    db = resolve_db(args.db)
    sync_dir = notion_dir(db)
    records = load_records(sync_dir)
    merged, stats = merge_markdown_records(db, records)

    print(
        "Markdown mirror plan: "
        f"{stats['added']} add, {stats['updated']} update, {stats['unchanged']} unchanged "
        f"({len(merged)} total compact record(s))."
    )
    if not args.apply:
        print("Dry-run only. Re-run with --apply to update local sync files.")
        return 0

    save_records(sync_dir, merged)
    save_generated_indexes(db)
    print(f"Updated {sync_dir / '_records.jsonl'}, regenerated _index.md, and refreshed generated indexes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
