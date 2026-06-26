#!/usr/bin/env python3
"""
Scan contracts/INDEX.json and report approaching deadlines.

Reads the contract index and checks for upcoming expirations, renewals,
payment deadlines, and cancellation notice windows.

Usage:
    python3 deadline_checker.py [contracts_dir]
    python3 deadline_checker.py --days 7 --json
    python3 deadline_checker.py --days 30 --types renewal,expiration
    python3 deadline_checker.py --quiet

Options:
    --days N                Look-ahead window in days (default: 30)
    --types TYPE[,TYPE]     Filter by event type: renewal, expiration, payment,
                            cancellation_notice, next_action (default: all)
    --json                  Output as structured JSON (default)
    --human                 Output as human-readable table
    --quiet                 Suppress non-urgent output. Exit code 0 if no urgent
                            items, exit code 1 if anything overdue or within 7 days.
    --help                  Show this help message

Exit codes:
    0 - No urgent items (or no index found)
    1 - Urgent items found (overdue or within 7 days)

Dependencies: Python 3.8+ stdlib only (no pip install required).
"""

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


def parse_date(date_str):
    """Parse an ISO date string. Returns None if unparseable."""
    if not date_str or date_str in ("null", "unknown", "needs_manual_review"):
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def extract_deadlines(entry, today):
    """Extract all deadline events from a contract metadata entry."""
    deadlines = []
    contract_id = entry.get("contract_id", "unknown")
    counterparty = entry.get("counterparty_name", "Unknown")

    # Skip terminated/expired contracts (unless checking for action items)
    signed_status = entry.get("signed_status", "")
    if signed_status in ("terminated", "expired"):
        return deadlines

    # 1. Contract expiration
    term_end = parse_date(entry.get("term_end"))
    if term_end:
        days_remaining = (term_end - today).days
        deadlines.append({
            "contract_id": contract_id,
            "counterparty": counterparty,
            "event_type": "expiration",
            "date": term_end.isoformat(),
            "days_remaining": days_remaining,
            "description": f"Contract expires",
            "action_required": "Review and decide on renewal or termination",
            "who_must_act": "you",
            "consequence_if_missed": entry.get("auto_renewal") and "Contract auto-renews" or "Contract lapses"
        })

    # 2. Renewal notice deadline
    renewal_notice = parse_date(entry.get("renewal_notice_deadline"))
    if renewal_notice:
        days_remaining = (renewal_notice - today).days
        deadlines.append({
            "contract_id": contract_id,
            "counterparty": counterparty,
            "event_type": "cancellation_notice",
            "date": renewal_notice.isoformat(),
            "days_remaining": days_remaining,
            "description": "Last day to give cancellation/non-renewal notice",
            "action_required": "Decide whether to renew and send notice if cancelling",
            "who_must_act": "you",
            "consequence_if_missed": "Contract auto-renews for another term"
        })

    # 3. Computed cancellation window (if auto-renew + term_end + cancellation_notice_days)
    if (entry.get("auto_renewal") and term_end
            and not renewal_notice
            and isinstance(entry.get("cancellation_notice_days"), int)):
        notice_days = entry["cancellation_notice_days"]
        computed_deadline = term_end - timedelta(days=notice_days)
        days_remaining = (computed_deadline - today).days
        deadlines.append({
            "contract_id": contract_id,
            "counterparty": counterparty,
            "event_type": "cancellation_notice",
            "date": computed_deadline.isoformat(),
            "days_remaining": days_remaining,
            "description": f"Computed cancellation notice deadline ({notice_days} days before expiry)",
            "action_required": "Send non-renewal notice before this date to prevent auto-renewal",
            "who_must_act": "you",
            "consequence_if_missed": "Contract auto-renews for another term"
        })

    # 4. Next action due date
    next_action_date = parse_date(entry.get("next_action_due_date"))
    next_action = entry.get("next_action")
    if next_action_date and next_action:
        days_remaining = (next_action_date - today).days
        deadlines.append({
            "contract_id": contract_id,
            "counterparty": counterparty,
            "event_type": "next_action",
            "date": next_action_date.isoformat(),
            "days_remaining": days_remaining,
            "description": f"Action due: {next_action}",
            "action_required": next_action,
            "who_must_act": "you",
            "consequence_if_missed": "Depends on action type"
        })

    # 5. Normalized dates (if available)
    normalized = entry.get("normalized_dates", {})
    if normalized:
        for key, label in [("next_renewal", "renewal"),
                           ("next_payment", "payment")]:
            d = parse_date(normalized.get(key))
            if d:
                days_remaining = (d - today).days
                deadlines.append({
                    "contract_id": contract_id,
                    "counterparty": counterparty,
                    "event_type": label,
                    "date": d.isoformat(),
                    "days_remaining": days_remaining,
                    "description": f"Upcoming {label}",
                    "action_required": f"Prepare for {label}",
                    "who_must_act": "you",
                    "consequence_if_missed": f"Missed {label} deadline"
                })

    return deadlines


def bucket_deadlines(deadlines):
    """Sort deadlines into urgency buckets."""
    buckets = {
        "overdue": [],
        "next_7_days": [],
        "next_30_days": [],
        "next_60_days": [],
        "next_90_days": [],
        "beyond_90_days": []
    }

    for d in deadlines:
        days = d["days_remaining"]
        if days < 0:
            buckets["overdue"].append(d)
        elif days <= 7:
            buckets["next_7_days"].append(d)
        elif days <= 30:
            buckets["next_30_days"].append(d)
        elif days <= 60:
            buckets["next_60_days"].append(d)
        elif days <= 90:
            buckets["next_90_days"].append(d)
        else:
            buckets["beyond_90_days"].append(d)

    # Sort each bucket by days remaining
    for key in buckets:
        buckets[key].sort(key=lambda x: x["days_remaining"])

    return buckets


def format_human(buckets, days_filter):
    """Format deadlines as a human-readable table."""
    lines = []
    lines.append("CONTRACT DEADLINE REPORT")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append(f"Look-ahead: {days_filter} days")
    lines.append("=" * 80)

    bucket_labels = [
        ("overdue", "OVERDUE"),
        ("next_7_days", "NEXT 7 DAYS"),
        ("next_30_days", "NEXT 30 DAYS"),
        ("next_60_days", "NEXT 60 DAYS"),
        ("next_90_days", "NEXT 90 DAYS"),
        ("beyond_90_days", "BEYOND 90 DAYS"),
    ]

    # Only show buckets within the filter window
    for key, label in bucket_labels:
        items = buckets.get(key, [])
        if not items:
            continue

        # Filter out items beyond the requested window
        if key == "beyond_90_days" and days_filter <= 90:
            items = [i for i in items if i["days_remaining"] <= days_filter]
        if key == "next_90_days" and days_filter < 60:
            continue
        if key == "next_60_days" and days_filter < 30:
            continue

        if not items:
            continue

        lines.append("")
        lines.append(f"--- {label} ---")
        lines.append(f"{'Contract':<30} {'Event':<20} {'Date':<12} {'Days':>5}  Action")
        lines.append("-" * 80)

        for item in items:
            cid = item["contract_id"][:28]
            event = item["event_type"][:18]
            d = item["date"]
            days = item["days_remaining"]
            action = item["action_required"][:30]
            days_str = f"{days:>5}" if days >= 0 else f"{days:>5}"
            lines.append(f"{cid:<30} {event:<20} {d:<12} {days_str}  {action}")

    total = sum(len(v) for v in buckets.values())
    urgent = len(buckets.get("overdue", [])) + len(buckets.get("next_7_days", []))
    lines.append("")
    lines.append(f"Total: {total} deadline(s), {urgent} urgent")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Scan contracts/INDEX.json for approaching deadlines.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python3 deadline_checker.py --days 7 --json\n"
               "  python3 deadline_checker.py --days 30 --human\n"
               "  python3 deadline_checker.py --quiet\n"
    )
    parser.add_argument("contracts_dir", nargs="?", default="./contracts",
                        help="Path to contracts directory (default: ./contracts)")
    parser.add_argument("--days", type=int, default=30,
                        help="Look-ahead window in days (default: 30)")
    parser.add_argument("--types", type=str, default=None,
                        help="Comma-separated event types to include (default: all)")
    parser.add_argument("--json", action="store_true", default=True,
                        help="Output as JSON (default)")
    parser.add_argument("--human", action="store_true",
                        help="Output as human-readable table")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress output, use exit code only (1 = urgent items exist)")

    args = parser.parse_args()
    contracts_dir = Path(args.contracts_dir)
    index_path = contracts_dir / "INDEX.json"

    # If no index exists, exit cleanly
    if not index_path.exists():
        if not args.quiet:
            if args.human:
                print("No INDEX.json found. Run index_builder.py first.")
            else:
                print(json.dumps({"status": "no_index", "deadlines": [], "urgent": False}))
        sys.exit(0)

    # Load index
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            entries = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"ERROR: Could not read INDEX.json: {e}", file=sys.stderr)
        sys.exit(1)

    today = date.today()

    # Extract all deadlines
    all_deadlines = []
    for entry in entries:
        all_deadlines.extend(extract_deadlines(entry, today))

    # Filter by types if specified
    if args.types:
        allowed_types = set(args.types.split(","))
        all_deadlines = [d for d in all_deadlines if d["event_type"] in allowed_types]

    # Filter by days window
    all_deadlines = [d for d in all_deadlines if d["days_remaining"] <= args.days]

    # Bucket the deadlines
    buckets = bucket_deadlines(all_deadlines)

    # Determine urgency
    urgent_count = len(buckets["overdue"]) + len(buckets["next_7_days"])
    has_urgent = urgent_count > 0

    if args.quiet:
        sys.exit(1 if has_urgent else 0)

    if args.human:
        print(format_human(buckets, args.days))
    else:
        output = {
            "generated_at": today.isoformat(),
            "look_ahead_days": args.days,
            "total_deadlines": len(all_deadlines),
            "urgent_count": urgent_count,
            "urgent": has_urgent,
            "buckets": buckets
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))

    sys.exit(1 if has_urgent else 0)


if __name__ == "__main__":
    main()
