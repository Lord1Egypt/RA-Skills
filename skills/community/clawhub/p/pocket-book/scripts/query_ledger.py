#!/usr/bin/env python3
"""Query Pocketbook ledger state and summaries."""

from __future__ import annotations

import argparse
import sys

from ledger_common import (
    DEFAULT_TIMEZONE,
    LedgerError,
    active_entries,
    configure_standard_streams,
    decimal_to_str,
    entry_response,
    filter_entries_by_period,
    group_amounts,
    json_dump,
    load_events,
    materialize_entries,
    sorted_entries,
    summarize_entries,
)


def summary_command(args: argparse.Namespace) -> dict:
    entries = active_entries(materialize_entries(load_events(args.data_dir)))
    filtered = filter_entries_by_period(entries, args.period, args.timezone, args.date)
    summary = summarize_entries(filtered)
    return {
        "ok": True,
        "period": args.period,
        "timezone": args.timezone,
        "entry_count": summary.entry_count,
        "totals": {
            "expense": decimal_to_str(summary.expense_total),
            "income": decimal_to_str(summary.income_total),
            "refund": decimal_to_str(summary.refund_total),
            "transfer": decimal_to_str(summary.transfer_total),
            "net_outflow": decimal_to_str(summary.net_outflow),
        },
        "by_category": group_amounts(filtered, "category")[: args.limit],
        "by_payment_method": group_amounts(filtered, "payment_method")[: args.limit],
        "recent_entries": [entry_response(entry) for entry in sorted_entries(filtered)[: args.limit]],
    }


def recent_command(args: argparse.Namespace) -> dict:
    entries = active_entries(materialize_entries(load_events(args.data_dir)))
    return {
        "ok": True,
        "entries": [entry_response(entry) for entry in sorted_entries(entries)[: args.limit]],
    }


def pending_command(args: argparse.Namespace) -> dict:
    entries = active_entries(materialize_entries(load_events(args.data_dir)))
    pending = [entry for entry in sorted_entries(entries) if entry_response(entry)["pending_reasons"]]
    return {
        "ok": True,
        "entries": [entry_response(entry) for entry in pending[: args.limit]],
    }


def entry_command(args: argparse.Namespace) -> dict:
    entries = materialize_entries(load_events(args.data_dir))
    entry = entries.get(args.entry_id)
    if not entry:
        raise LedgerError(f"Entry not found: {args.entry_id}")
    return {"ok": True, "entry": entry_response(entry)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query a Pocketbook ledger.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    summary = subparsers.add_parser("summary")
    summary.add_argument("--data-dir", default=None, help="Ledger data root.")
    summary.add_argument("--period", choices=["today", "week", "month", "all", "date"], default="today")
    summary.add_argument("--date", default=None, help="YYYY-MM-DD, required when --period date.")
    summary.add_argument("--timezone", default=DEFAULT_TIMEZONE)
    summary.add_argument("--limit", type=int, default=5)

    recent = subparsers.add_parser("recent")
    recent.add_argument("--data-dir", default=None, help="Ledger data root.")
    recent.add_argument("--limit", type=int, default=5)

    pending = subparsers.add_parser("pending")
    pending.add_argument("--data-dir", default=None, help="Ledger data root.")
    pending.add_argument("--limit", type=int, default=10)

    entry = subparsers.add_parser("entry")
    entry.add_argument("--data-dir", default=None, help="Ledger data root.")
    entry.add_argument("--entry-id", required=True)

    return parser


def main() -> int:
    configure_standard_streams()
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "summary":
            result = summary_command(args)
        elif args.command == "recent":
            result = recent_command(args)
        elif args.command == "pending":
            result = pending_command(args)
        else:
            result = entry_command(args)
        print(json_dump(result))
        return 0
    except LedgerError as exc:
        print(json_dump({"ok": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
