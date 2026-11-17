#!/usr/bin/env python3
"""Promote a light or standard Notion sync record to a detailed Markdown file."""

from __future__ import annotations

import argparse

from notion_common import detail_filename, load_records, notion_dir, render_detail_markdown, resolve_db, save_records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id", help="Record ID to promote.")
    parser.add_argument("--db", default=None, help="Path to travel-db.")
    parser.add_argument("--apply", action="store_true", help="Create the detail file and update _records.jsonl.")
    args = parser.parse_args()

    sync_dir = notion_dir(resolve_db(args.db))
    records = load_records(sync_dir)
    target = next((record for record in records if record["id"] == args.id), None)
    if not target:
        print(f"Record not found: {args.id}")
        return 1

    filename = target.get("detail_file") or detail_filename(target)
    target_path = sync_dir / filename
    print(f"Promote {target['id']} -> {filename}")

    if not args.apply:
        print("Dry-run only. Re-run with --apply to create the detailed Markdown file.")
        return 0

    if target_path.exists() and not target.get("detail_file"):
        print(f"Refusing to overwrite existing file: {target_path}")
        return 1

    target["record_weight"] = "detailed"
    target["detail_file"] = filename
    if not target_path.exists():
        target_path.write_text(render_detail_markdown(target), encoding="utf-8")
    save_records(sync_dir, records)
    print(f"Created detailed record: {target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
