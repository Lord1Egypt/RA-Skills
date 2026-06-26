#!/usr/bin/env python3
"""Resolve recent Pocketbook entries and apply update or revert events."""

from __future__ import annotations

import argparse
import sys

from ledger_common import (
    LedgerError,
    active_entries,
    atomic_ledger_operation,
    build_revert_event,
    build_update_event,
    configure_standard_streams,
    entry_response,
    json_dump,
    load_events,
    load_payload,
    materialize_entries,
    sorted_entries,
)


def recent_response(data_dir: str | None, limit: int) -> dict:
    entries = active_entries(materialize_entries(load_events(data_dir)))
    return {
        "ok": True,
        "entries": [entry_response(entry) for entry in sorted_entries(entries)[:limit]],
    }


def update_last_command(args: argparse.Namespace) -> dict:
    payload = load_payload(args.payload)
    def operation(events, profile):
        entries = active_entries(materialize_entries(events))
        ordered = sorted_entries(entries)
        if args.offset < 0 or args.offset >= len(ordered):
            raise LedgerError(f"Recent entry offset {args.offset} is out of range.")
        entry_id = ordered[args.offset]["entry_id"]
        return build_update_event(payload, events, profile, entry_id_override=entry_id)

    result = atomic_ledger_operation(args.data_dir, operation)
    entries = materialize_entries(result["events_after"])
    entry_id = result["entry_id"]
    return {"ok": True, "event": result["event"], "entry": entry_response(entries[entry_id])}


def revert_last_command(args: argparse.Namespace) -> dict:
    payload = load_payload(args.payload)
    def operation(events, profile):
        entries = active_entries(materialize_entries(events))
        ordered = sorted_entries(entries)
        if args.offset < 0 or args.offset >= len(ordered):
            raise LedgerError(f"Recent entry offset {args.offset} is out of range.")
        entry_id = ordered[args.offset]["entry_id"]
        return build_revert_event(payload, events, entry_id_override=entry_id)

    result = atomic_ledger_operation(args.data_dir, operation)
    entries = materialize_entries(result["events_after"])
    entry_id = result["entry_id"]
    return {"ok": True, "event": result["event"], "entry": entry_response(entries[entry_id])}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Edit recent entries in a Pocketbook ledger.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    recent = subparsers.add_parser("recent")
    recent.add_argument("--data-dir", default=None, help="Ledger data root.")
    recent.add_argument("--limit", type=int, default=5)

    update_last = subparsers.add_parser("update-last")
    update_last.add_argument("--data-dir", default=None, help="Ledger data root.")
    update_last.add_argument("--payload", default="-", help="JSON payload path or - for stdin.")
    update_last.add_argument("--offset", type=int, default=0, help="0 means the latest active entry.")

    revert_last = subparsers.add_parser("revert-last")
    revert_last.add_argument("--data-dir", default=None, help="Ledger data root.")
    revert_last.add_argument("--payload", default="-", help="JSON payload path or - for stdin.")
    revert_last.add_argument("--offset", type=int, default=0, help="0 means the latest active entry.")

    return parser


def main() -> int:
    configure_standard_streams()
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "recent":
            result = recent_response(args.data_dir, args.limit)
        elif args.command == "update-last":
            result = update_last_command(args)
        else:
            result = revert_last_command(args)
        print(json_dump(result))
        return 0
    except LedgerError as exc:
        print(json_dump({"ok": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
