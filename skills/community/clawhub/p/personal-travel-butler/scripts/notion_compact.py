#!/usr/bin/env python3
"""Compact simple Notion sync records so they stay in _records.jsonl only."""

from __future__ import annotations

import argparse
import json

from notion_common import load_records, notion_dir, normalize_record, notion_record_from_page, resolve_db, save_records, should_be_detailed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=None, help="Path to travel-db.")
    parser.add_argument("--id", default=None, help="Only compact one local record ID.")
    parser.add_argument("--from-page-json", default=None, help="Read a Notion page JSON file and print or add a compact record.")
    parser.add_argument("--apply", action="store_true", help="Write compacted records. Without this flag, only print a dry-run plan.")
    args = parser.parse_args()

    sync_dir = notion_dir(resolve_db(args.db))
    records = load_records(sync_dir)

    if args.from_page_json:
        with open(args.from_page_json, "r", encoding="utf-8") as handle:
            page = json.load(handle)
        record = notion_record_from_page(page)
        record["record_weight"] = "detailed" if should_be_detailed(record) else "light"
        if not args.apply:
            print(json.dumps(record, ensure_ascii=False, sort_keys=True))
            print("Dry-run only. Re-run with --apply to append/update _records.jsonl.")
            return 0
        by_id = {row["id"]: row for row in records}
        by_id[record["id"]] = normalize_record(record)
        save_records(sync_dir, list(by_id.values()))
        print(f"Compacted Notion page into {record['id']}.")
        return 0

    changed = 0
    for record in records:
        if args.id and record["id"] != args.id:
            continue
        if record.get("detail_file"):
            continue
        target_weight = "detailed" if should_be_detailed(record) else "light"
        if record.get("record_weight") != target_weight:
            print(f"{record['id']}: {record.get('record_weight')} -> {target_weight}")
            changed += 1
            if args.apply:
                record["record_weight"] = target_weight

    if args.apply:
        save_records(sync_dir, records)
        print(f"Compacted {changed} record(s).")
    else:
        print(f"Dry-run only. {changed} record(s) would change.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
