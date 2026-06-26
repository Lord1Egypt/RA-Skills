#!/usr/bin/env python3
"""
report.py — Generate a markdown spending report from categorized transactions.

Reads the output of categorize.py and produces a clean Obsidian-compatible
markdown report with budget vs. actual comparison, top merchants, and
month-over-month trends.

Usage:
    python3 report.py categorized.json [--budget budget.json] [--output report.md]
"""

import json
import os
import sys
import argparse
from datetime import datetime
from collections import defaultdict


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_budget(path: str) -> dict:
    """Load budget config JSON. Returns empty dict if not provided."""
    if not path:
        return {}
    if not os.path.isfile(path):
        sys.stderr.write(f"WARNING: Budget file not found: {path}. Running without budget.\n")
        return {}
    with open(path) as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as e:
            sys.stderr.write(f"WARNING: Invalid budget JSON: {e}. Running without budget.\n")
            return {}
    return config.get("monthly_budgets", {})


def fmt_currency(amount: float) -> str:
    """Format a float as a currency string."""
    return f"${amount:,.2f}"


def fmt_pct(value: float, total: float) -> str:
    """Format a percentage of total."""
    if total == 0:
        return "0%"
    return f"{value / total * 100:.1f}%"


def month_label(year_month: str) -> str:
    """Convert YYYY-MM to 'Month YYYY'."""
    try:
        dt = datetime.strptime(year_month, "%Y-%m")
        return dt.strftime("%B %Y")
    except ValueError:
        return year_month


def bar_chart(actual: float, budget: float, width: int = 20) -> str:
    """Generate a simple text progress bar."""
    if budget <= 0:
        return ""
    ratio = min(actual / budget, 1.5)
    filled = int(ratio * width)
    bar = "█" * min(filled, width) + ("▓" * max(0, filled - width))
    empty = "░" * max(0, width - filled)
    return f"[{bar}{empty}]"


# ── Data processing ───────────────────────────────────────────────────────────

def group_by_month(transactions: list) -> dict:
    """Group transactions by YYYY-MM."""
    months = defaultdict(list)
    for tx in transactions:
        date = tx.get("date", "")
        if len(date) >= 7:
            month_key = date[:7]  # YYYY-MM
        else:
            month_key = "unknown"
        months[month_key].append(tx)
    return dict(sorted(months.items()))


def compute_month_stats(transactions: list) -> dict:
    """Compute spending stats for a list of transactions (single month)."""
    by_category = defaultdict(float)
    by_merchant = defaultdict(float)
    total_spent = 0.0
    total_income = 0.0

    for tx in transactions:
        amount = tx.get("amount", 0.0)
        tx_type = tx.get("type", "debit")
        category = tx.get("category", "Other")
        desc = tx.get("description", "Unknown")

        if tx_type == "credit" or category == "Income":
            total_income += amount
        else:
            total_spent += amount
            by_category[category] += amount
            by_merchant[desc] += amount

    # Sort merchants by spend descending
    top_merchants = sorted(by_merchant.items(), key=lambda x: x[1], reverse=True)

    return {
        "total_spent": round(total_spent, 2),
        "total_income": round(total_income, 2),
        "by_category": {k: round(v, 2) for k, v in sorted(by_category.items())},
        "top_merchants": [(desc, round(amt, 2)) for desc, amt in top_merchants[:10]],
        "transaction_count": len(transactions),
    }


# ── Report generation ─────────────────────────────────────────────────────────

def generate_report(months_data: dict, budget: dict, source_file: str) -> str:
    """Generate the full markdown report."""
    now = datetime.now()
    month_keys = sorted(months_data.keys())
    is_multi_month = len(month_keys) > 1

    lines = []

    # ── Frontmatter ──
    all_categories = set()
    for stats in months_data.values():
        all_categories.update(stats["by_category"].keys())
    tags = ["finance", "budget", "spending"]

    lines.append("---")
    lines.append(f"date: {now.strftime('%Y-%m-%d')}")
    lines.append(f"generated: {now.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"type: budget-report")
    lines.append(f"source: {os.path.basename(source_file)}")
    lines.append(f"months: {', '.join(month_keys)}")
    lines.append(f"tags: [{', '.join(tags)}]")
    lines.append("---")
    lines.append("")

    lines.append(f"# 💰 Spending Report")
    if is_multi_month:
        lines.append(f"**Period:** {month_label(month_keys[0])} – {month_label(month_keys[-1])}")
    else:
        lines.append(f"**Period:** {month_label(month_keys[0])}")
    lines.append(f"*Generated {now.strftime('%B %d, %Y at %I:%M %p')}*")
    lines.append("")

    # ── Per-month sections ──
    for month_key in month_keys:
        stats = months_data[month_key]
        label = month_label(month_key)

        if is_multi_month:
            lines.append(f"---")
            lines.append("")
            lines.append(f"## 📅 {label}")
            lines.append("")

        # Summary box
        lines.append("### Summary")
        lines.append("")
        lines.append(f"| | Amount |")
        lines.append(f"|---|---|")
        lines.append(f"| 💸 Total Spent | **{fmt_currency(stats['total_spent'])}** |")
        lines.append(f"| 💵 Income / Credits | {fmt_currency(stats['total_income'])} |")
        net = stats["total_income"] - stats["total_spent"]
        net_label = "✅ Net Surplus" if net >= 0 else "❌ Net Deficit"
        lines.append(f"| {net_label} | {fmt_currency(abs(net))} |")
        lines.append(f"| 🧾 Transactions | {stats['transaction_count']} |")
        lines.append("")

        # Budget vs Actual
        lines.append("### Spending by Category")
        lines.append("")

        if budget:
            lines.append("| Category | Spent | Budget | Remaining | % Used | |")
            lines.append("|---|---:|---:|---:|---:|---|")
        else:
            lines.append("| Category | Spent | % of Total |")
            lines.append("|---|---:|---:|")

        for category, spent in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
            if budget:
                monthly_budget = budget.get(category, 0)
                if monthly_budget > 0:
                    remaining = monthly_budget - spent
                    pct = spent / monthly_budget * 100
                    pct_str = f"{pct:.0f}%"
                    remaining_str = fmt_currency(remaining) if remaining >= 0 else f"**-{fmt_currency(abs(remaining))}**"
                    alert = "⚠️" if spent > monthly_budget else ("🔶" if pct >= 80 else "✅")
                    bar = bar_chart(spent, monthly_budget)
                    lines.append(f"| {category} | {fmt_currency(spent)} | {fmt_currency(monthly_budget)} | {remaining_str} | {pct_str} | {alert} {bar} |")
                else:
                    lines.append(f"| {category} | {fmt_currency(spent)} | — | — | — | — |")
            else:
                pct = fmt_pct(spent, stats["total_spent"])
                lines.append(f"| {category} | {fmt_currency(spent)} | {pct} |")

        lines.append("")

        # Budget alerts
        if budget:
            overages = []
            warnings = []
            for category, monthly_budget in budget.items():
                spent = stats["by_category"].get(category, 0)
                if spent > monthly_budget:
                    overages.append((category, spent, monthly_budget, spent - monthly_budget))
                elif monthly_budget > 0 and spent / monthly_budget >= 0.8:
                    warnings.append((category, spent, monthly_budget))

            if overages or warnings:
                lines.append("### ⚠️ Budget Alerts")
                lines.append("")
                for cat, spent, bud, over in overages:
                    lines.append(f"- **{cat}**: Over budget by **{fmt_currency(over)}** ({fmt_currency(spent)} / {fmt_currency(bud)})")
                for cat, spent, bud in warnings:
                    lines.append(f"- **{cat}**: {fmt_currency(spent)} spent of {fmt_currency(bud)} budget ({spent/bud*100:.0f}% used)")
                lines.append("")

        # Top merchants
        if stats["top_merchants"]:
            lines.append("### Top Merchants")
            lines.append("")
            lines.append("| # | Merchant | Spent |")
            lines.append("|---|---|---:|")
            for i, (merchant, amount) in enumerate(stats["top_merchants"], 1):
                # Truncate long merchant names
                name = merchant[:50] + "…" if len(merchant) > 50 else merchant
                lines.append(f"| {i} | {name} | {fmt_currency(amount)} |")
            lines.append("")

    # ── Month-over-month trend ──
    if is_multi_month:
        lines.append("---")
        lines.append("")
        lines.append("## 📈 Month-over-Month Trend")
        lines.append("")

        # Trend table
        all_cats = sorted(set(
            cat
            for stats in months_data.values()
            for cat in stats["by_category"]
        ))

        # Header
        header = "| Category | " + " | ".join(month_label(m) for m in month_keys) + " | Trend |"
        separator = "|---|" + "---:|" * len(month_keys) + "---|"
        lines.append(header)
        lines.append(separator)

        for cat in all_cats:
            amounts = [months_data[m]["by_category"].get(cat, 0) for m in month_keys]
            row = f"| {cat} | " + " | ".join(fmt_currency(a) for a in amounts) + " | "
            # Simple trend: compare last two months
            if len(amounts) >= 2 and amounts[-2] > 0:
                delta = amounts[-1] - amounts[-2]
                pct_change = delta / amounts[-2] * 100
                if abs(pct_change) < 5:
                    trend = "→"
                elif delta > 0:
                    trend = f"↑ +{pct_change:.0f}%"
                else:
                    trend = f"↓ {pct_change:.0f}%"
            else:
                trend = "—"
            row += f"{trend} |"
            lines.append(row)

        lines.append("")

        # Monthly totals summary
        lines.append("### Monthly Totals")
        lines.append("")
        lines.append("| Month | Spent | Income | Net |")
        lines.append("|---|---:|---:|---:|")
        for month_key in month_keys:
            stats = months_data[month_key]
            net = stats["total_income"] - stats["total_spent"]
            net_str = f"+{fmt_currency(net)}" if net >= 0 else f"-{fmt_currency(abs(net))}"
            lines.append(
                f"| {month_label(month_key)} | {fmt_currency(stats['total_spent'])} | "
                f"{fmt_currency(stats['total_income'])} | {net_str} |"
            )
        lines.append("")

    # ── Footer ──
    lines.append("---")
    lines.append(f"*Report generated by local-budget skill · Source: `{os.path.basename(source_file)}`*")
    lines.append("")

    return "\n".join(lines)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate markdown spending report")
    parser.add_argument("input", help="Path to categorized JSON (from categorize.py)")
    parser.add_argument("--budget", default=None, help="Path to budget config JSON (optional)")
    parser.add_argument("--output", default=None, help="Output markdown file path (default: stdout)")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        sys.stderr.write(f"ERROR: File not found: {args.input}\n")
        sys.exit(1)

    with open(args.input) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            sys.stderr.write(f"ERROR: Invalid JSON in {args.input}: {e}\n")
            sys.exit(1)

    # Handle both raw transaction arrays and categorize.py output format
    if isinstance(data, list):
        transactions = data
    elif isinstance(data, dict) and "transactions" in data:
        transactions = data["transactions"]
    else:
        sys.stderr.write("ERROR: Expected a JSON array or categorize.py output format\n")
        sys.exit(1)

    if not transactions:
        sys.stderr.write("ERROR: No transactions found in input\n")
        sys.exit(1)

    budget = load_budget(args.budget)
    months_grouped = group_by_month(transactions)
    months_data = {m: compute_month_stats(txs) for m, txs in months_grouped.items()}

    report = generate_report(months_data, budget, args.input)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w") as f:
            f.write(report)
        sys.stderr.write(f"INFO: Report written to {args.output}\n")
    else:
        print(report)


if __name__ == "__main__":
    main()
