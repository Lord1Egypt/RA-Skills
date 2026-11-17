#!/usr/bin/env python3
"""One stable command surface for the personal travel butler scripts."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from find_duplicates import find_duplicates, print_matches  # noqa: E402
from notion_common import load_local_env, notion_dir, read_jsonl, resolve_db  # noqa: E402


def run(command: list[str], check: bool = False) -> int:
    print("+ " + " ".join(str(part) for part in command), flush=True)
    result = subprocess.run(command)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.returncode


def py(script: str, *args: str) -> list[str]:
    return [sys.executable, str(SCRIPT_DIR / script), *args]


def db_arg(db: Path) -> list[str]:
    return ["--db", str(db)]


def command_doctor(args: argparse.Namespace) -> int:
    db = resolve_db(args.db)
    if args.fix_local:
        rc = run(py("build_records_from_places.py", *db_arg(db), "--apply"))
        if rc != 0:
            return rc

    print(f"Database: {db}")
    rc_validate = run(py("validate_db.py", str(db)))
    rc_notion = run(py("notion_check.py", *db_arg(db), "--dry-run"))

    sync_dir = notion_dir(db)
    records = read_jsonl(sync_dir / "_records.jsonl")
    ledger = read_jsonl(sync_dir / "_ledger.jsonl")
    logs = read_jsonl(sync_dir / "_sync_log.jsonl")
    print("")
    print("Local summary:")
    print(f"- compact records: {len(records)}")
    print(f"- ledger rows: {len(ledger)}")
    print(f"- sync log rows: {len(logs)}")
    for filename in ("cities.md", "tags.md", "sources.md"):
        path = db / "indexes" / filename
        print(f"- index {filename}: {'OK' if path.exists() else 'missing'}")

    load_local_env()
    if args.live_schema:
        rc_schema = run(py("notion_schema.py", "check", *db_arg(db)))
    else:
        rc_schema = 0
        print("- live schema: skipped by default; run `butler.py schema --db travel-db check` when Notion network access is available")

    print("")
    if rc_validate == 0 and rc_notion == 0 and rc_schema == 0:
        print("Next step: run `python3 personal-travel-butler/scripts/butler.py sync --db travel-db` for a strict dry-run.")
        return 0
    print("Next step: fix the failed check above, or run `doctor --fix-local` for derived local files.")
    return 1


def command_refresh(args: argparse.Namespace) -> int:
    db = resolve_db(args.db)
    command = py("build_records_from_places.py", *db_arg(db))
    if args.apply:
        command.append("--apply")
    return run(command)


def sync_command(db: Path, args: argparse.Namespace, apply: bool = False) -> list[str]:
    command = py("notion_sync.py", "push", *db_arg(db))
    if not args.no_strict:
        command.append("--strict")
    if args.filter_city:
        command.extend(["--filter-city", args.filter_city])
    for tag in args.filter_tag:
        command.extend(["--filter-tag", tag])
    if args.limit is not None:
        command.extend(["--limit", str(args.limit)])
    if apply:
        command.append("--apply")
    return command


def command_sync(args: argparse.Namespace) -> int:
    db = resolve_db(args.db)
    if not args.apply:
        return run(sync_command(db, args, apply=False))

    for command in (
        py("build_records_from_places.py", *db_arg(db), "--apply"),
        py("validate_db.py", str(db)),
        sync_command(db, args, apply=False),
        sync_command(db, args, apply=True),
    ):
        rc = run(command)
        if rc != 0:
            return rc
    return 0


def command_schema(args: argparse.Namespace) -> int:
    db = resolve_db(args.db)
    command = py("notion_schema.py", args.action, *db_arg(db))
    if args.apply:
        command.append("--apply")
    return run(command)


def command_add_place(args: argparse.Namespace) -> int:
    db = resolve_db(args.db)
    matches = find_duplicates(db, args.name, args.city, args.tag, [], threshold=args.duplicate_threshold)
    if matches and not args.force_new:
        print_matches(matches)
        print("Stop: likely duplicate found. Use `butler.py update-place` or pass --force-new only when the user explicitly wants a new entry.")
        return 2

    command = py("create_entry.py", *db_arg(db), "--type", "place", "--name", args.name, "--city", args.city)
    for tag in args.tag:
        command.extend(["--tag", tag])
    for evidence in args.evidence:
        command.extend(["--evidence", evidence])
    if args.coords:
        command.extend(["--coords", args.coords])
    if args.dry_run:
        command.append("--dry-run")
        return run(command)

    rc = run(command)
    if rc != 0:
        return rc
    for followup in (
        py("build_records_from_places.py", *db_arg(db), "--apply"),
        py("validate_db.py", str(db)),
    ):
        rc = run(followup)
        if rc != 0:
            return rc
    return 0


def command_update_place(args: argparse.Namespace) -> int:
    db = resolve_db(args.db)
    command = py("update_place.py", *db_arg(db))
    for option in ("id", "name", "city", "address", "province", "phone", "website"):
        value = getattr(args, option)
        if value is not None:
            command.extend([f"--{option.replace('_', '-')}", value])
    for option in ("tag", "source", "evidence", "note"):
        for value in getattr(args, option):
            command.extend([f"--{option}", value])
    if args.dry_run:
        command.append("--dry-run")
        return run(command)

    rc = run(command)
    if rc != 0:
        return rc
    for followup in (
        py("build_records_from_places.py", *db_arg(db), "--apply"),
        py("validate_db.py", str(db)),
    ):
        rc = run(followup)
        if rc != 0:
            return rc
    return 0


def command_duplicates(args: argparse.Namespace) -> int:
    matches = find_duplicates(resolve_db(args.db), args.name, args.city, args.tag, args.source, args.threshold)
    print_matches(matches, args.json)
    return 2 if matches else 0


def command_ingest_text(args: argparse.Namespace) -> int:
    db = resolve_db(args.db)
    command = py("ingest_text.py", *db_arg(db))
    for option in ("text", "file", "title", "name", "city", "coords"):
        value = getattr(args, option)
        if value is not None:
            command.extend([f"--{option}", value])
    for option in ("tag", "evidence"):
        for value in getattr(args, option):
            command.extend([f"--{option}", value])
    if args.force_new:
        command.append("--force-new")
    if args.apply:
        command.append("--apply")
    if args.dry_run:
        command.append("--dry-run")
    return run(command)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor")
    doctor.add_argument("--db", default=None)
    doctor.add_argument("--fix-local", action="store_true")
    doctor.add_argument("--live-schema", action="store_true")
    doctor.set_defaults(func=command_doctor)

    refresh = subparsers.add_parser("refresh")
    refresh.add_argument("--db", default=None)
    refresh.add_argument("--apply", action="store_true")
    refresh.set_defaults(func=command_refresh)

    sync = subparsers.add_parser("sync")
    sync.add_argument("--db", default=None)
    sync.add_argument("--apply", action="store_true")
    sync.add_argument("--no-strict", action="store_true")
    sync.add_argument("--filter-city", default=None)
    sync.add_argument("--filter-tag", action="append", default=[])
    sync.add_argument("--limit", type=int, default=None)
    sync.set_defaults(func=command_sync)

    schema = subparsers.add_parser("schema")
    schema.add_argument("--db", default=None)
    schema.add_argument("action", choices=("check", "migrate"))
    schema.add_argument("--apply", action="store_true")
    schema.set_defaults(func=command_schema)

    add_place = subparsers.add_parser("add-place")
    add_place.add_argument("--db", default=None)
    add_place.add_argument("--name", required=True)
    add_place.add_argument("--city", required=True)
    add_place.add_argument("--tag", action="append", default=[])
    add_place.add_argument("--evidence", action="append", default=[])
    add_place.add_argument("--coords", default=None)
    add_place.add_argument("--force-new", action="store_true")
    add_place.add_argument("--duplicate-threshold", type=int, default=70)
    add_place.add_argument("--dry-run", action="store_true")
    add_place.set_defaults(func=command_add_place)

    update_place = subparsers.add_parser("update-place")
    update_place.add_argument("--db", default=None)
    update_place.add_argument("--id", default=None)
    update_place.add_argument("--name", default=None)
    update_place.add_argument("--city", default=None)
    update_place.add_argument("--tag", action="append", default=[])
    update_place.add_argument("--source", action="append", default=[])
    update_place.add_argument("--evidence", action="append", default=[])
    update_place.add_argument("--note", action="append", default=[])
    update_place.add_argument("--address", default=None)
    update_place.add_argument("--province", default=None)
    update_place.add_argument("--phone", default=None)
    update_place.add_argument("--website", default=None)
    update_place.add_argument("--dry-run", action="store_true")
    update_place.set_defaults(func=command_update_place)

    duplicates = subparsers.add_parser("duplicates")
    duplicates.add_argument("--db", default=None)
    duplicates.add_argument("--name", required=True)
    duplicates.add_argument("--city", default=None)
    duplicates.add_argument("--tag", action="append", default=[])
    duplicates.add_argument("--source", action="append", default=[])
    duplicates.add_argument("--threshold", type=int, default=70)
    duplicates.add_argument("--json", action="store_true")
    duplicates.set_defaults(func=command_duplicates)

    ingest = subparsers.add_parser("ingest-text")
    ingest.add_argument("--db", default=None)
    ingest.add_argument("--text", default=None)
    ingest.add_argument("--file", default=None)
    ingest.add_argument("--title", default=None)
    ingest.add_argument("--name", default=None)
    ingest.add_argument("--city", default=None)
    ingest.add_argument("--tag", action="append", default=[])
    ingest.add_argument("--evidence", action="append", default=[])
    ingest.add_argument("--coords", default=None)
    ingest.add_argument("--force-new", action="store_true")
    ingest.add_argument("--apply", action="store_true")
    ingest.add_argument("--dry-run", action="store_true")
    ingest.set_defaults(func=command_ingest_text)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
