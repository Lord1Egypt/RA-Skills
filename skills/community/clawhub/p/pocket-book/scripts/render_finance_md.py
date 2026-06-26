#!/usr/bin/env python3
"""Render a readable Markdown snapshot from the Pocketbook event ledger."""

from __future__ import annotations

import argparse
import sys

from ledger_common import (
    DEFAULT_TIMEZONE,
    active_entries,
    configure_standard_streams,
    decimal_to_str,
    entry_response,
    filter_entries_by_period,
    load_events,
    markdown_path,
    materialize_entries,
    sorted_entries,
    summarize_entries,
)


def render_markdown(data_dir: str | None, timezone_name: str) -> str:
    entries = active_entries(materialize_entries(load_events(data_dir)))
    ordered = sorted_entries(entries)
    today_entries = filter_entries_by_period(entries, "today", timezone_name)
    month_entries = filter_entries_by_period(entries, "month", timezone_name)
    pending_entries = [entry_response(entry) for entry in ordered if entry_response(entry)["pending_reasons"]]
    today_summary = summarize_entries(today_entries)
    month_summary = summarize_entries(month_entries)

    lines = [
        "# Personal Finance",
        "",
        "## Today",
        f"- Expense: {decimal_to_str(today_summary.expense_total)}",
        f"- Income: {decimal_to_str(today_summary.income_total)}",
        f"- Refund: {decimal_to_str(today_summary.refund_total)}",
        f"- Transfer: {decimal_to_str(today_summary.transfer_total)}",
        f"- Net outflow: {decimal_to_str(today_summary.net_outflow)}",
        "",
        "## Month To Date",
        f"- Expense: {decimal_to_str(month_summary.expense_total)}",
        f"- Income: {decimal_to_str(month_summary.income_total)}",
        f"- Refund: {decimal_to_str(month_summary.refund_total)}",
        f"- Transfer: {decimal_to_str(month_summary.transfer_total)}",
        f"- Net outflow: {decimal_to_str(month_summary.net_outflow)}",
        "",
        "## Pending Completion",
    ]

    if pending_entries:
        for entry in pending_entries[:10]:
            reasons = ", ".join(entry["pending_reasons"])
            lines.append(
                f"- {entry['occurred_at']}: {entry['entry_type']} {entry['amount']} "
                f"{entry['category']} via {entry['payment_method']} [{reasons}]"
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Recent Entries"])
    if ordered:
        for entry in ordered[:20]:
            lines.append(
                f"- {entry['occurred_at']}: {entry['entry_type']} {entry['amount']} "
                f"{entry['category']} via {entry['payment_method']}"
            )
    else:
        lines.append("- No entries")
    return "\n".join(lines) + "\n"


def main() -> int:
    configure_standard_streams()
    parser = argparse.ArgumentParser(description="Render personal_finance.md from a Pocketbook ledger.")
    parser.add_argument("--data-dir", default=None, help="Ledger data root.")
    parser.add_argument("--output", default=None, help="Optional output path.")
    parser.add_argument("--timezone", default=DEFAULT_TIMEZONE)
    args = parser.parse_args()

    content = render_markdown(args.data_dir, args.timezone)
    output_path = args.output or markdown_path(args.data_dir)
    with open(output_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    print(output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
