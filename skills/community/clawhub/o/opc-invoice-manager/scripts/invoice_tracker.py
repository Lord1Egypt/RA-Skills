#!/usr/bin/env python3
"""
Invoice tracking, aging reports, payment reconciliation, and revenue insights.

Walks the invoices/ directory, builds INDEX.json, generates aging reports,
tracks payment status, and produces AR + revenue analytics.

Usage:
    python3 invoice_tracker.py [invoices_dir]
    python3 invoice_tracker.py --index [invoices_dir]
    python3 invoice_tracker.py --aging --human [invoices_dir]
    python3 invoice_tracker.py --overdue --json [invoices_dir]
    python3 invoice_tracker.py --insights [invoices_dir]
    python3 invoice_tracker.py --update-status INV-2026-001 paid [invoices_dir]
    python3 invoice_tracker.py --mark-paid INV-2026-001 [invoices_dir]
    python3 invoice_tracker.py --mark-paid INV-2026-001 --amount 5000 [invoices_dir]
    python3 invoice_tracker.py --action-summary [invoices_dir]
    python3 invoice_tracker.py --auto-detect-overdue [invoices_dir]

Options:
    --index                 Build/update INDEX.json from metadata files
    --aging                 Generate aging report
    --overdue               Show only overdue invoices
    --insights              Generate INSIGHTS.json + INSIGHTS.md
    --update-status ID STS  Update invoice status
    --mark-paid ID          Mark invoice as fully paid
    --amount AMT            Partial payment amount (use with --mark-paid)
    --date DATE             Payment date (default: today)
    --auto-detect-overdue   Scan sent invoices past due_date, update to overdue
    --action-summary        Generate today's action items
    --json                  Output as JSON (default)
    --human                 Output as human-readable table
    --quiet                 Suppress output, exit code 1 if overdue items exist
    --help                  Show this help message

Exit codes:
    0 - No overdue items (or no index found)
    1 - Overdue items exist

Dependencies: Python 3.8+ stdlib only.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path


def parse_date(date_str):
    """Parse an ISO date string. Returns None if unparseable."""
    if not date_str or date_str in ("null", "unknown", "needs_manual_review"):
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def parse_amount(amount_str):
    """Parse an amount string to Decimal. Returns None if unparseable."""
    if not amount_str or amount_str in ("null", "unknown"):
        return None
    try:
        cleaned = amount_str.replace(",", "").replace("$", "").replace("€", "").replace("£", "").strip()
        return Decimal(cleaned)
    except (InvalidOperation, ValueError):
        return None


def find_metadata_files(invoices_dir):
    """Find all metadata.json files in the invoices directory."""
    return sorted(invoices_dir.glob("*/*/metadata.json")) + sorted(invoices_dir.glob("*/metadata.json"))


def build_index(invoices_dir):
    """Build or update the invoice index."""
    index_path = invoices_dir / "INDEX.json"
    metadata_files = find_metadata_files(invoices_dir)
    entries = {}

    for mf in metadata_files:
        try:
            with open(mf, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"ERROR: Could not read {mf}: {e}", file=sys.stderr)
            continue

        invoice_id = metadata.get("invoice_id") or metadata.get("invoice_number")
        if not invoice_id:
            print(f"WARNING: No invoice_id in {mf}, skipping.", file=sys.stderr)
            continue

        entries[invoice_id] = metadata

    sorted_entries = sorted(
        entries.values(),
        key=lambda x: x.get("issue_date") or "0000-00-00",
        reverse=True
    )

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(sorted_entries, f, indent=2, ensure_ascii=False)

    print(f"Index updated. {len(sorted_entries)} invoice(s).", file=sys.stderr)
    return sorted_entries


def load_index(invoices_dir):
    """Load existing INDEX.json."""
    index_path = invoices_dir / "INDEX.json"
    if index_path.exists():
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def find_overdue(entries, today=None):
    """Find overdue invoices."""
    if today is None:
        today = date.today()
    overdue = []
    for entry in entries:
        status = entry.get("status", "")
        if status in ("paid", "void", "draft", "disputed"):
            continue
        due = parse_date(entry.get("due_date"))
        if due and due < today:
            days_overdue = (today - due).days
            overdue.append({
                "invoice_number": entry.get("invoice_number", "?"),
                "client_name": entry.get("client_name", "Unknown"),
                "total_amount": entry.get("total_amount", "?"),
                "outstanding_amount": entry.get("outstanding_amount") or entry.get("total_amount", "?"),
                "currency": entry.get("currency", ""),
                "due_date": entry.get("due_date", ""),
                "days_overdue": days_overdue,
                "collection_stage": entry.get("collection_stage", "current"),
                "reminder_count": entry.get("reminder_count", 0),
                "status": status
            })
    overdue.sort(key=lambda x: x["days_overdue"], reverse=True)
    return overdue


def generate_aging(entries, today=None):
    """Generate aging report data."""
    if today is None:
        today = date.today()

    buckets = {
        "current": [],
        "overdue_1_30": [],
        "overdue_31_60": [],
        "overdue_60_plus": [],
        "due_this_week": [],
        "due_this_month": [],
        "paid_this_month": [],
        "draft": []
    }

    totals = {
        "outstanding": Decimal("0"),
        "overdue": Decimal("0"),
        "paid_this_month": Decimal("0")
    }

    for entry in entries:
        status = entry.get("status", "")
        due = parse_date(entry.get("due_date"))
        amount = parse_amount(entry.get("outstanding_amount") or entry.get("total_amount"))
        paid_date = parse_date(entry.get("paid_date"))

        if status == "draft":
            buckets["draft"].append(entry)
            continue

        if status == "void":
            continue

        if status == "paid":
            if paid_date and paid_date.year == today.year and paid_date.month == today.month:
                buckets["paid_this_month"].append(entry)
                if amount:
                    totals["paid_this_month"] += parse_amount(entry.get("total_amount")) or Decimal("0")
            continue

        if amount:
            totals["outstanding"] += amount

        if not due:
            buckets["current"].append(entry)
            continue

        days_diff = (today - due).days

        if days_diff > 60:
            buckets["overdue_60_plus"].append(entry)
            if amount:
                totals["overdue"] += amount
        elif days_diff > 30:
            buckets["overdue_31_60"].append(entry)
            if amount:
                totals["overdue"] += amount
        elif days_diff > 0:
            buckets["overdue_1_30"].append(entry)
            if amount:
                totals["overdue"] += amount
        elif days_diff >= -7:
            buckets["due_this_week"].append(entry)
        elif days_diff >= -30:
            buckets["due_this_month"].append(entry)
        else:
            buckets["current"].append(entry)

    return {
        "generated_at": today.isoformat(),
        "buckets": buckets,
        "totals": {k: str(v) for k, v in totals.items()},
        "counts": {k: len(v) for k, v in buckets.items()}
    }


def format_aging_human(aging_data):
    """Format aging report as human-readable text."""
    lines = [
        "ACCOUNTS RECEIVABLE AGING REPORT",
        f"Generated: {aging_data['generated_at']}",
        "=" * 80,
        "",
        f"  Outstanding: {aging_data['totals']['outstanding']}",
        f"  Overdue:     {aging_data['totals']['overdue']}",
        f"  Paid (month):{aging_data['totals']['paid_this_month']}",
        ""
    ]

    bucket_labels = [
        ("overdue_60_plus", "OVERDUE 60+ DAYS"),
        ("overdue_31_60", "OVERDUE 31-60 DAYS"),
        ("overdue_1_30", "OVERDUE 1-30 DAYS"),
        ("due_this_week", "DUE THIS WEEK"),
        ("due_this_month", "DUE THIS MONTH"),
        ("draft", "DRAFT"),
    ]

    for key, label in bucket_labels:
        items = aging_data["buckets"].get(key, [])
        if not items:
            continue

        lines.append(f"--- {label} ({len(items)}) ---")
        lines.append(f"{'Invoice':<18} {'Client':<25} {'Amount':>12} {'Due':>12}")
        lines.append("-" * 70)

        for item in items:
            inv = str(item.get("invoice_number", "?"))[:16]
            client = str(item.get("client_name", "?"))[:23]
            amt = str(item.get("outstanding_amount") or item.get("total_amount", "?"))
            due = str(item.get("due_date", ""))
            lines.append(f"{inv:<18} {client:<25} {amt:>12} {due:>12}")
        lines.append("")

    return "\n".join(lines)


def generate_action_summary(entries, today=None):
    """Generate today's action items."""
    if today is None:
        today = date.today()

    actions = {
        "send_now": [],
        "follow_up_today": [],
        "escalate_this_week": [],
        "likely_cash_in_14_days": [],
        "at_risk": []
    }

    for entry in entries:
        status = entry.get("status", "")
        due = parse_date(entry.get("due_date"))
        last_reminder = parse_date(entry.get("last_reminder_date"))
        stage = entry.get("collection_stage", "current")
        summary = {
            "invoice_number": entry.get("invoice_number"),
            "client_name": entry.get("client_name"),
            "total_amount": entry.get("outstanding_amount") or entry.get("total_amount"),
            "currency": entry.get("currency", ""),
            "due_date": entry.get("due_date"),
            "status": status
        }

        if status == "draft":
            actions["send_now"].append(summary)
            continue

        if status in ("paid", "void"):
            continue

        if due:
            days_until = (due - today).days
            days_overdue = -days_until

            # Follow up: overdue and no reminder in last 7 days
            if days_overdue > 0:
                should_remind = True
                if last_reminder:
                    days_since_reminder = (today - last_reminder).days
                    should_remind = days_since_reminder >= 7

                if should_remind and stage in ("current", "reminder", "overdue"):
                    actions["follow_up_today"].append(summary)

                if stage in ("escalation", "final"):
                    actions["escalate_this_week"].append(summary)

                if days_overdue > 30:
                    actions["at_risk"].append(summary)

            # Likely cash in: due in next 14 days, status is sent
            elif 0 <= days_until <= 14 and status == "sent":
                actions["likely_cash_in_14_days"].append(summary)

    return {
        "generated_at": today.isoformat(),
        "actions": actions,
        "counts": {k: len(v) for k, v in actions.items()}
    }


def format_action_summary_human(summary):
    """Format action summary as human-readable text."""
    lines = [
        "WHAT TO DO TODAY",
        f"Generated: {summary['generated_at']}",
        "=" * 60,
    ]

    sections = [
        ("send_now", "SEND NOW"),
        ("follow_up_today", "FOLLOW UP TODAY"),
        ("escalate_this_week", "ESCALATE THIS WEEK"),
        ("likely_cash_in_14_days", "LIKELY CASH-IN (14 DAYS)"),
        ("at_risk", "AT-RISK RECEIVABLES"),
    ]

    for key, label in sections:
        items = summary["actions"].get(key, [])
        if items:
            lines.append(f"\n{label} ({len(items)}):")
            for item in items:
                lines.append(
                    f"  - {item['invoice_number']} | {item['client_name']} | "
                    f"{item.get('total_amount', '?')} {item.get('currency', '')} | "
                    f"due {item.get('due_date', '?')}"
                )
        else:
            lines.append(f"\n{label}: None")

    return "\n".join(lines)


def auto_detect_overdue(invoices_dir, entries, today=None):
    """Scan sent invoices past due_date and update status to overdue."""
    if today is None:
        today = date.today()

    updated = 0
    for entry in entries:
        if entry.get("status") != "sent":
            continue
        due = parse_date(entry.get("due_date"))
        if due and due < today:
            entry["status"] = "overdue"
            if entry.get("collection_stage") in (None, "current"):
                entry["collection_stage"] = "overdue"
            updated += 1

    if updated > 0:
        # Rewrite INDEX.json
        index_path = invoices_dir / "INDEX.json"
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        print(f"Auto-detected {updated} overdue invoice(s).", file=sys.stderr)

    return updated


def update_invoice_status(invoices_dir, entries, invoice_number, new_status):
    """Update an invoice's status in INDEX.json."""
    valid_statuses = {"draft", "sent", "paid", "partial", "overdue", "void", "disputed"}
    if new_status not in valid_statuses:
        print(f"ERROR: Invalid status '{new_status}'. Must be one of: {', '.join(sorted(valid_statuses))}", file=sys.stderr)
        sys.exit(1)

    found = False
    for entry in entries:
        if entry.get("invoice_number") == invoice_number:
            entry["status"] = new_status
            entry["updated_at"] = date.today().isoformat()
            if new_status == "paid" and not entry.get("paid_date"):
                entry["paid_date"] = date.today().isoformat()
            found = True
            break

    if not found:
        print(f"ERROR: Invoice '{invoice_number}' not found.", file=sys.stderr)
        sys.exit(1)

    index_path = invoices_dir / "INDEX.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"Updated {invoice_number} → {new_status}", file=sys.stderr)


def mark_paid(invoices_dir, entries, invoice_number, amount=None, pay_date=None):
    """Mark an invoice as paid (full or partial)."""
    if pay_date is None:
        pay_date = date.today().isoformat()

    found = False
    for entry in entries:
        if entry.get("invoice_number") == invoice_number:
            found = True
            total = parse_amount(entry.get("total_amount"))

            if amount is not None:
                pay_amount = parse_amount(str(amount))
                if pay_amount is None:
                    print(f"ERROR: Invalid payment amount: {amount}", file=sys.stderr)
                    sys.exit(1)

                # Record partial payment
                if "partial_payments" not in entry:
                    entry["partial_payments"] = []
                entry["partial_payments"].append({
                    "amount": str(pay_amount),
                    "date": pay_date,
                    "reference": None,
                    "notes": None
                })

                # Calculate outstanding
                total_paid = sum(
                    parse_amount(p["amount"]) or Decimal("0")
                    for p in entry["partial_payments"]
                )
                if total and total_paid >= total:
                    entry["status"] = "paid"
                    entry["paid_date"] = pay_date
                    entry["outstanding_amount"] = "0"
                else:
                    entry["status"] = "partial"
                    if total:
                        entry["outstanding_amount"] = str(total - total_paid)
            else:
                entry["status"] = "paid"
                entry["paid_date"] = pay_date
                entry["outstanding_amount"] = "0"

            entry["updated_at"] = date.today().isoformat()
            entry["collection_stage"] = None
            break

    if not found:
        print(f"ERROR: Invoice '{invoice_number}' not found.", file=sys.stderr)
        sys.exit(1)

    index_path = invoices_dir / "INDEX.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    status = "paid" if amount is None else f"partial ({amount})"
    print(f"Marked {invoice_number} as {status}", file=sys.stderr)


def generate_insights(invoices_dir, entries):
    """Generate AR + revenue insights."""
    if len(entries) < 2:
        print("Not enough invoices for insights (minimum 2).", file=sys.stderr)
        return

    today = date.today()
    insights = []

    # Filter out void
    active = [e for e in entries if e.get("status") != "void"]

    # Revenue view: invoiced and paid this month
    this_month = today.strftime("%Y-%m")
    invoiced_month = [e for e in active if (e.get("issue_date") or "").startswith(this_month)]
    paid_month = [e for e in active if e.get("status") == "paid" and (e.get("paid_date") or "").startswith(this_month)]

    invoiced_total = sum(parse_amount(e.get("total_amount")) or Decimal("0") for e in invoiced_month)
    paid_total = sum(parse_amount(e.get("total_amount")) or Decimal("0") for e in paid_month)

    insights.append({
        "category": "monthly_revenue",
        "insight": f"This month: invoiced {invoiced_total}, collected {paid_total}",
        "confidence": "high",
        "based_on": f"{len(invoiced_month)} invoices issued, {len(paid_month)} paid this month",
        "missing_data_notes": None
    })

    # AR view: outstanding and overdue
    outstanding = [e for e in active if e.get("status") in ("sent", "partial", "overdue")]
    outstanding_total = sum(parse_amount(e.get("outstanding_amount") or e.get("total_amount")) or Decimal("0") for e in outstanding)
    overdue_items = find_overdue(active, today)
    overdue_total = sum(parse_amount(o.get("outstanding_amount")) or Decimal("0") for o in overdue_items)

    insights.append({
        "category": "receivables",
        "insight": f"Outstanding AR: {outstanding_total} ({len(outstanding)} invoices), Overdue: {overdue_total} ({len(overdue_items)} invoices)",
        "confidence": "high",
        "based_on": f"Based on {len(active)} active invoices",
        "missing_data_notes": None
    })

    # DSO (Days Sales Outstanding)
    paid_with_dates = [
        e for e in active
        if e.get("status") == "paid" and e.get("issue_date") and e.get("paid_date")
    ]
    if paid_with_dates:
        dso_values = []
        for e in paid_with_dates:
            issued = parse_date(e.get("issue_date"))
            paid = parse_date(e.get("paid_date"))
            if issued and paid:
                dso_values.append((paid - issued).days)
        if dso_values:
            avg_dso = sum(dso_values) / len(dso_values)
            insights.append({
                "category": "dso",
                "insight": f"Average Days Sales Outstanding: {avg_dso:.0f} days",
                "confidence": "high" if len(dso_values) >= 5 else "medium",
                "based_on": f"Based on {len(dso_values)} paid invoices",
                "missing_data_notes": None
            })

    # Client concentration
    client_amounts = defaultdict(lambda: Decimal("0"))
    for e in outstanding:
        client = e.get("client_name", "Unknown")
        amt = parse_amount(e.get("outstanding_amount") or e.get("total_amount")) or Decimal("0")
        client_amounts[client] += amt

    if client_amounts and outstanding_total > 0:
        top_client = max(client_amounts, key=client_amounts.get)
        top_pct = (client_amounts[top_client] / outstanding_total) * 100

        insight = {
            "category": "client_concentration",
            "insight": f"Top outstanding: {top_client} ({top_pct:.0f}% of AR)",
            "confidence": "medium",
            "based_on": "Based on outstanding invoice amounts, not revenue",
            "missing_data_notes": None
        }
        if top_pct > 50:
            insight["detail"] = f"WARNING: {top_client} represents {top_pct:.0f}% of outstanding receivables. High concentration risk."
        insights.append(insight)

    # Collection rate
    all_non_draft = [e for e in active if e.get("status") != "draft"]
    if all_non_draft:
        paid_count = sum(1 for e in all_non_draft if e.get("status") == "paid")
        rate = (paid_count / len(all_non_draft)) * 100
        insights.append({
            "category": "collection_rate",
            "insight": f"Collection rate: {rate:.0f}% ({paid_count} of {len(all_non_draft)} invoices paid)",
            "confidence": "high" if len(all_non_draft) >= 5 else "medium",
            "based_on": f"Based on {len(all_non_draft)} non-draft invoices",
            "missing_data_notes": None
        })

    # Write output files
    insights_data = {
        "generated_at": today.isoformat(),
        "total_invoices": len(active),
        "insights": insights
    }

    insights_json_path = invoices_dir / "INSIGHTS.json"
    with open(insights_json_path, "w", encoding="utf-8") as f:
        json.dump(insights_data, f, indent=2, ensure_ascii=False)

    # Write INSIGHTS.md
    lines = [
        "# Invoice & AR Insights",
        "",
        f"> Generated on {today.isoformat()} from {len(active)} invoice(s).",
        "> Based on invoice data, not accounting records. This is not tax advice.",
        "",
    ]
    for ins in insights:
        lines.append(f"## {ins['category'].replace('_', ' ').title()}")
        lines.append("")
        lines.append(f"**{ins['insight']}**")
        lines.append(f"*Confidence: {ins['confidence']}* — {ins['based_on']}")
        lines.append("")
        if ins.get("detail"):
            lines.append(ins["detail"])
            lines.append("")
        if ins.get("missing_data_notes"):
            lines.append(f"> Note: {ins['missing_data_notes']}")
            lines.append("")
        lines.append("---")
        lines.append("")

    insights_md_path = invoices_dir / "INSIGHTS.md"
    with open(insights_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated {len(insights)} insight(s) → INSIGHTS.json + INSIGHTS.md", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Invoice tracking, aging reports, and revenue insights.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python3 invoice_tracker.py --index\n"
               "  python3 invoice_tracker.py --aging --human\n"
               "  python3 invoice_tracker.py --overdue --json\n"
               "  python3 invoice_tracker.py --mark-paid INV-2026-001\n"
               "  python3 invoice_tracker.py --mark-paid INV-2026-001 --amount 5000\n"
               "  python3 invoice_tracker.py --action-summary --human\n"
    )
    parser.add_argument("invoices_dir", nargs="?", default="./invoices",
                        help="Path to invoices directory (default: ./invoices)")
    parser.add_argument("--index", action="store_true", help="Build/update INDEX.json")
    parser.add_argument("--aging", action="store_true", help="Generate aging report")
    parser.add_argument("--overdue", action="store_true", help="Show overdue invoices only")
    parser.add_argument("--insights", action="store_true", help="Generate INSIGHTS.json + INSIGHTS.md")
    parser.add_argument("--update-status", nargs=2, metavar=("ID", "STATUS"),
                        help="Update invoice status")
    parser.add_argument("--mark-paid", type=str, metavar="ID", help="Mark invoice as paid")
    parser.add_argument("--amount", type=str, default=None, help="Partial payment amount")
    parser.add_argument("--date", type=str, default=None, help="Payment date (YYYY-MM-DD)")
    parser.add_argument("--auto-detect-overdue", action="store_true",
                        help="Auto-detect and update overdue invoices")
    parser.add_argument("--action-summary", action="store_true", help="Generate action summary")
    parser.add_argument("--json", action="store_true", default=True, help="Output as JSON (default)")
    parser.add_argument("--human", action="store_true", help="Output as human-readable")
    parser.add_argument("--quiet", action="store_true", help="Exit code only")

    args = parser.parse_args()
    invoices_dir = Path(args.invoices_dir)

    if not invoices_dir.exists() and not args.index:
        if not args.quiet:
            if args.human:
                print("No invoices directory found.")
            else:
                print(json.dumps({"status": "no_directory", "invoices": [], "urgent": False}))
        sys.exit(0)

    if args.index:
        invoices_dir.mkdir(parents=True, exist_ok=True)
        entries = build_index(invoices_dir)
    else:
        entries = load_index(invoices_dir)

    if args.auto_detect_overdue:
        auto_detect_overdue(invoices_dir, entries)

    if args.update_status:
        inv_id, new_status = args.update_status
        update_invoice_status(invoices_dir, entries, inv_id, new_status)
        return

    if args.mark_paid:
        mark_paid(invoices_dir, entries, args.mark_paid, args.amount, args.date)
        return

    if args.action_summary:
        summary = generate_action_summary(entries)
        if args.quiet:
            urgent = summary["counts"]["follow_up_today"] + summary["counts"]["escalate_this_week"]
            sys.exit(1 if urgent > 0 else 0)
        if args.human:
            print(format_action_summary_human(summary))
        else:
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        return

    if args.aging:
        aging = generate_aging(entries)
        if args.quiet:
            overdue_count = aging["counts"]["overdue_1_30"] + aging["counts"]["overdue_31_60"] + aging["counts"]["overdue_60_plus"]
            sys.exit(1 if overdue_count > 0 else 0)
        if args.human:
            print(format_aging_human(aging))
        else:
            print(json.dumps(aging, indent=2, ensure_ascii=False, default=str))
        return

    if args.overdue:
        overdue = find_overdue(entries)
        if args.quiet:
            sys.exit(1 if overdue else 0)
        if args.human:
            if not overdue:
                print("No overdue invoices.")
            else:
                print(f"OVERDUE INVOICES ({len(overdue)})")
                print("=" * 70)
                for o in overdue:
                    print(f"  {o['invoice_number']} | {o['client_name']} | "
                          f"{o['outstanding_amount']} {o['currency']} | "
                          f"due {o['due_date']} | {o['days_overdue']} days overdue")
        else:
            output = {
                "generated_at": date.today().isoformat(),
                "overdue_count": len(overdue),
                "urgent": len(overdue) > 0,
                "overdue": overdue
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
        sys.exit(1 if overdue else 0)

    if args.insights:
        generate_insights(invoices_dir, entries)
        return

    # Default: show summary
    overdue = find_overdue(entries)
    if args.quiet:
        sys.exit(1 if overdue else 0)
    print(json.dumps({
        "total_invoices": len(entries),
        "overdue_count": len(overdue),
        "urgent": len(overdue) > 0
    }, indent=2))


if __name__ == "__main__":
    main()
