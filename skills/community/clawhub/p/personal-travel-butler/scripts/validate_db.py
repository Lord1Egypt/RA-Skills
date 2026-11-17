#!/usr/bin/env python3
"""Validate the personal travel Markdown database."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from travel_model import ENTRY_DIRS, VALID_STATUS, VALID_TYPES, city_validation_errors, parse_frontmatter_file, validate_coordinates

REQUIRED_FIELDS = (
    "id",
    "type",
    "status",
    "name",
    "city",
    "coordinates",
    "tags",
    "source",
    "evidence",
    "priority",
    "last_verified",
    "created_at",
    "updated_at",
)
NOTION_SYNC_FILES = (
    "_README.md",
    "_config.example.json",
    "_schema.md",
    "_records.jsonl",
    "_index.md",
    "_ledger.jsonl",
    "_conflicts.md",
    "_sync_log.jsonl",
)
NOTION_RECORD_FIELDS = (
    "id",
    "type",
    "status",
    "record_weight",
    "name",
    "city",
    "tags",
    "priority",
    "summary",
    "notes",
    "detail_file",
    "source",
    "evidence",
    "updated_at",
)
NOTION_WEIGHTS = {"light", "standard", "detailed"}


def markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    links = re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)
    wiki_links = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text)
    return links + wiki_links


def validate_file(path: Path, db: Path) -> tuple[dict[str, Any], list[str]]:
    data, _, errors = parse_frontmatter_file(path)
    rel = path.relative_to(db)

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{rel}: missing required field `{field}`")

    entry_type = data.get("type")
    if entry_type is not None and entry_type not in VALID_TYPES:
        errors.append(f"{rel}: invalid type `{entry_type}`")

    status = data.get("status")
    if status is not None and status not in VALID_STATUS:
        errors.append(f"{rel}: invalid status `{status}`")

    priority = data.get("priority")
    if priority is not None and (not isinstance(priority, int) or not 1 <= priority <= 5):
        errors.append(f"{rel}: priority must be an integer from 1 to 5")

    errors.extend(city_validation_errors(data.get("city"), str(rel)))
    errors.extend(validate_coordinates(data.get("coordinates"), str(rel)))

    for list_field in ("tags", "source", "evidence"):
        if list_field in data and not isinstance(data[list_field], list):
            errors.append(f"{rel}: `{list_field}` must be a list")

    for link in markdown_links(path):
        if "://" in link or link.startswith("#") or link.startswith("mailto:"):
            continue
        link_target = link.split("#", 1)[0]
        if not link_target:
            continue
        resolved = (path.parent / link_target).resolve()
        if not resolved.exists():
            errors.append(f"{rel}: broken link `{link}`")

    return data, errors


def validate_directories(db: Path) -> list[str]:
    errors: list[str] = []
    for folder in tuple(ENTRY_DIRS) + ("assets", "_inbox", "indexes", "notion-sync"):
        if not (db / folder).is_dir():
            errors.append(f"missing directory `{folder}`")
    return errors


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.exists():
        return rows, [f"missing file `{path.name}`"]
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name} line {line_number}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"{path.name} line {line_number}: expected a JSON object")
            continue
        rows.append(row)
    return rows, errors


def validate_notion_sync(db: Path) -> tuple[int, list[str]]:
    sync_dir = db / "notion-sync"
    errors: list[str] = []
    if not sync_dir.exists():
        return 0, ["missing directory `notion-sync`"]
    if not sync_dir.is_dir():
        return 0, ["`notion-sync` is not a directory"]

    for child in sync_dir.iterdir():
        if child.is_dir():
            errors.append(f"notion-sync must be flat; found subdirectory `{child.name}`")
    for filename in NOTION_SYNC_FILES:
        if not (sync_dir / filename).exists():
            errors.append(f"notion-sync missing `{filename}`")

    records, record_errors = read_jsonl(sync_dir / "_records.jsonl")
    errors.extend(f"notion-sync/{error}" for error in record_errors)
    ledger, ledger_errors = read_jsonl(sync_dir / "_ledger.jsonl")
    errors.extend(f"notion-sync/{error}" for error in ledger_errors)

    seen: set[str] = set()
    for index, record in enumerate(records, start=1):
        for field in NOTION_RECORD_FIELDS:
            if field not in record:
                errors.append(f"notion-sync/_records.jsonl line {index}: missing `{field}`")
        record_id = record.get("id")
        if not record_id:
            errors.append(f"notion-sync/_records.jsonl line {index}: empty id")
        elif record_id in seen:
            errors.append(f"notion-sync/_records.jsonl line {index}: duplicate id `{record_id}`")
        seen.add(str(record_id))

        if record.get("type") not in VALID_TYPES:
            errors.append(f"notion-sync/_records.jsonl line {index}: invalid type `{record.get('type')}`")
        if record.get("status") not in VALID_STATUS:
            errors.append(f"notion-sync/_records.jsonl line {index}: invalid status `{record.get('status')}`")
        if record.get("record_weight") not in NOTION_WEIGHTS:
            errors.append(f"notion-sync/_records.jsonl line {index}: invalid record_weight `{record.get('record_weight')}`")
        errors.extend(city_validation_errors(record.get("city"), f"notion-sync/_records.jsonl line {index}"))
        if not isinstance(record.get("tags", []), list):
            errors.append(f"notion-sync/_records.jsonl line {index}: `tags` must be a list")
        if not isinstance(record.get("source", []), list):
            errors.append(f"notion-sync/_records.jsonl line {index}: `source` must be a list")
        if not isinstance(record.get("evidence", []), list):
            errors.append(f"notion-sync/_records.jsonl line {index}: `evidence` must be a list")

        detail_file = record.get("detail_file")
        if record.get("record_weight") == "detailed" and not detail_file:
            errors.append(f"notion-sync/_records.jsonl line {index}: detailed record missing detail_file")
        if detail_file:
            detail_file = str(detail_file)
            if "/" in detail_file or "\\" in detail_file:
                errors.append(f"notion-sync/_records.jsonl line {index}: detail_file must not include folders")
            elif not (sync_dir / detail_file).exists():
                errors.append(f"notion-sync/_records.jsonl line {index}: missing detail file `{detail_file}`")

    ledger_ids: set[str] = set()
    for index, row in enumerate(ledger, start=1):
        ledger_id = row.get("id")
        if not ledger_id:
            errors.append(f"notion-sync/_ledger.jsonl line {index}: missing id")
        elif ledger_id in ledger_ids:
            errors.append(f"notion-sync/_ledger.jsonl line {index}: duplicate ledger id `{ledger_id}`")
        ledger_ids.add(str(ledger_id))

    return len(records), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("db", nargs="?", default="../travel-db", help="Path to the travel-db directory.")
    args = parser.parse_args()

    db = Path(args.db).expanduser().resolve()
    errors = validate_directories(db)
    ids: dict[str, Path] = {}
    entries = 0

    for dirname in ENTRY_DIRS:
        for path in sorted((db / dirname).glob("*.md")):
            entries += 1
            data, file_errors = validate_file(path, db)
            errors.extend(file_errors)
            entry_id = data.get("id")
            if entry_id:
                if entry_id in ids:
                    errors.append(f"{path.relative_to(db)}: duplicate id `{entry_id}` also in {ids[entry_id].relative_to(db)}")
                ids[entry_id] = path

    notion_entries, notion_errors = validate_notion_sync(db)
    errors.extend(notion_errors)

    if errors:
        print(f"travel-db validation failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"travel-db validation passed: {entries} entries, {len(ids)} unique ids, {notion_entries} Notion compact record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
