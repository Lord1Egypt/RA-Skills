#!/usr/bin/env python3
"""Safely ingest raw travel text into inbox, optionally creating a place."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from find_duplicates import find_duplicates, print_matches  # noqa: E402
from notion_common import resolve_db  # noqa: E402
from travel_model import slugify, today_iso  # noqa: E402


def read_raw_text(args: argparse.Namespace) -> str:
    if args.file:
        return Path(args.file).expanduser().read_text(encoding="utf-8")
    if args.text:
        return args.text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise ValueError("Provide --text, --file, or stdin content.")


def inbox_path(db: Path, title: str | None) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    name = slugify(title or "travel-capture")
    return db / "_inbox" / f"{stamp}-{name}.md"


def render_inbox_note(raw_text: str, title: str | None) -> str:
    title = title or "Travel Capture"
    return f"""---
id: inbox-{datetime.now().strftime("%Y%m%d%H%M%S")}
type: inbox
status: inbox
name: "{title}"
city: null
coordinates: null
tags: [inbox]
source: []
evidence: []
priority: 3
last_verified: null
created_at: {today_iso()}
updated_at: {today_iso()}
---

# {title}

## Raw Text

{raw_text.strip()}
"""


def run_checked(command: list[str]) -> int:
    result = subprocess.run(command)
    return result.returncode


def create_place_from_args(db: Path, args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "create_entry.py"),
        "--db",
        str(db),
        "--type",
        "place",
        "--name",
        args.name,
        "--city",
        args.city,
    ]
    for tag in args.tag:
        command.extend(["--tag", tag])
    for evidence in args.evidence:
        command.extend(["--evidence", evidence])
    if args.coords:
        command.extend(["--coords", args.coords])
    if args.dry_run:
        command.append("--dry-run")
    return run_checked(command)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=None)
    parser.add_argument("--text", default=None)
    parser.add_argument("--file", default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--name", default=None, help="Optional place name to create after inbox capture.")
    parser.add_argument("--city", default=None)
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--coords", default=None)
    parser.add_argument("--force-new", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Write inbox and optional place. Without this flag, preview only.")
    args = parser.parse_args()

    try:
        raw_text = read_raw_text(args)
    except ValueError as exc:
        print(exc)
        return 1

    db = resolve_db(args.db)
    target = inbox_path(db, args.title or args.name)
    note = render_inbox_note(raw_text, args.title or args.name)
    print(f"Inbox target: {target}")

    if args.name and args.city:
        matches = find_duplicates(db, args.name, args.city, args.tag, [], threshold=70)
        if matches and not args.force_new:
            print_matches(matches)
            print("Stop: likely duplicate found. Use update-place or pass --force-new if the user explicitly wants a new entry.")
            return 2
    elif args.name or args.city:
        print("Place creation requires both --name and --city. Inbox capture can still proceed.")

    if args.dry_run or not args.apply:
        print(note)
        if args.name and args.city:
            return create_place_from_args(db, argparse.Namespace(**{**vars(args), "dry_run": True}))
        print("Dry-run only. Re-run with --apply to write.")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(note, encoding="utf-8")
    print(f"Wrote {target}")

    if args.name and args.city:
        rc = create_place_from_args(db, argparse.Namespace(**{**vars(args), "dry_run": False}))
        if rc != 0:
            return rc
        rc = run_checked([sys.executable, str(SCRIPT_DIR / "build_records_from_places.py"), "--db", str(db), "--apply"])
        if rc != 0:
            return rc
    return run_checked([sys.executable, str(SCRIPT_DIR / "validate_db.py"), str(db)])


if __name__ == "__main__":
    raise SystemExit(main())
