#!/usr/bin/env python3
"""Append Pocketbook ledger events from structured payloads."""

from __future__ import annotations

import argparse
import json
import sys

from ledger_common import (
    LedgerError,
    atomic_ledger_operation,
    build_create_event,
    build_revert_event,
    build_update_event,
    configure_standard_streams,
    entry_response,
    json_dump,
    load_payload,
    materialize_entries,
)


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description="Append events to a Pocketbook ledger.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("create", "update", "revert"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--data-dir", default=None, help="Ledger data root.")
        subparser.add_argument(
            "--payload",
            default="-",
            help="Path to a JSON payload file, or - to read JSON from stdin.",
        )

    args = parser.parse_args()
    try:
        payload = load_payload(args.payload)
        def operation(events, profile):
            if args.command == "create":
                return build_create_event(payload, events, profile)
            if args.command == "update":
                return build_update_event(payload, events, profile)
            return build_revert_event(payload, events)

        result = atomic_ledger_operation(args.data_dir, operation)
        entries = materialize_entries(result["events_after"])
        entry_id = result["entry_id"]
        response = {
            "ok": True,
            "entry": entry_response(entries[entry_id]),
            "reused_existing": bool(result.get("reused_existing", False)),
        }
        if result.get("event") is not None:
            response["event"] = result["event"]
        if args.command == "create":
            response["duplicate_candidates"] = result["duplicate_candidates"]
        print(json_dump(response))
        return 0
    except (LedgerError, json.JSONDecodeError) as exc:
        print(json_dump({"ok": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
