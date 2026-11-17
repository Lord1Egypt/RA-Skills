#!/usr/bin/env python3
"""Check the local Notion sync workspace and optional live Notion schema."""

from __future__ import annotations

import argparse
from pathlib import Path

from notion_common import (
    FIXED_NOTION_FILES,
    OPTIONAL_NOTION_PROPERTIES,
    check_notion_properties,
    load_ledger,
    load_records,
    notion_dir,
    notion_env,
    notion_request,
    read_jsonl,
    resolve_db,
    validate_records,
)


def check_local(sync_dir: Path) -> list[str]:
    errors: list[str] = []
    if not sync_dir.is_dir():
        return [f"missing Notion sync folder: {sync_dir}"]
    for filename in FIXED_NOTION_FILES:
        if not (sync_dir / filename).exists():
            errors.append(f"missing `{filename}`")
    for child in sync_dir.iterdir():
        if child.is_dir():
            errors.append(f"notion-sync must be flat; remove subdirectory `{child.name}`")

    records = load_records(sync_dir)
    errors.extend(validate_records(records, sync_dir))
    read_jsonl(sync_dir / "_ledger.jsonl")
    load_ledger(sync_dir)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=None, help="Path to travel-db.")
    parser.add_argument("--dry-run", action="store_true", help="Only check local files; do not call Notion.")
    args = parser.parse_args()

    db = resolve_db(args.db)
    sync_dir = notion_dir(db)
    errors = check_local(sync_dir)
    if errors:
        print("Local Notion sync check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    records = load_records(sync_dir)
    print(f"Local Notion sync workspace OK: {len(records)} compact record(s).")
    if args.dry_run:
        return 0

    token, data_source_id, version = notion_env()
    if not token or not data_source_id:
        print("Set NOTION_TOKEN and NOTION_TRAVEL_DATA_SOURCE_ID to check live Notion schema.")
        return 1

    data_source = notion_request("GET", f"/data_sources/{data_source_id}", token, version)
    properties = data_source.get("properties", {})
    live_errors = check_notion_properties(properties)
    if live_errors:
        print("Notion schema check failed:")
        for error in live_errors:
            print(f"- {error}")
        return 1
    print(f"Live Notion schema OK using Notion-Version {version}.")
    missing_optional = [name for name in OPTIONAL_NOTION_PROPERTIES if name not in properties]
    if missing_optional:
        print("Optional columns not found; sync will skip them:")
        for name in missing_optional:
            print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
