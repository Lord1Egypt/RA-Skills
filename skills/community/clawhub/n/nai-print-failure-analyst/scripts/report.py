#!/usr/bin/env python3
"""
report.py — Generate a markdown failure pattern report.

Usage:
  report.py                       # Print report to stdout
  report.py --output report.md    # Save to file
  report.py --days 90             # Limit analysis to last N days (default: all time)
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(SKILL_DIR, "assets", "failure-log.json")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_log():
    if not os.path.exists(LOG_FILE):
        return {"failures": []}
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading log file: {e}", file=sys.stderr)
        sys.exit(1)


def parse_ts(ts_str):
    try:
        return datetime.fromisoformat(ts_str)
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze(failures, days=None):
    """Run analysis on the failure log."""
    now = datetime.now()
    cutoff = now - timedelta(days=days) if days else None

    # Apply time filter
    if cutoff:
        failures = [f for f in failures if (parse_ts(f.get("timestamp", "")) or datetime.min) >= cutoff]

    if not failures:
        return None

    # Sort chronologically
    failures_sorted = sorted(failures, key=lambda x: x.get("timestamp", ""))

    # Failure type counts
    ft_counter = Counter(f.get("failure_type", "unknown") for f in failures)

    # Printer failure counts
    printer_counter = Counter(f.get("printer", "unknown") for f in failures)

    # Material failure counts
    material_counter = Counter(f.get("material", "unknown") for f in failures)

    # Printer × material combos
    combo_counter = Counter(
        (f.get("printer", "unknown"), f.get("material", "unknown"))
        for f in failures
    )

    # Failure type × material combos
    ft_material_counter = Counter(
        (f.get("failure_type", "unknown"), f.get("material", "unknown"))
        for f in failures
    )

    # Monthly trend (group by YYYY-MM)
    monthly = defaultdict(int)
    for f in failures:
        ts = parse_ts(f.get("timestamp", ""))
        if ts:
            key = ts.strftime("%Y-%m")
            monthly[key] += 1

    # Unresolved (no fixed_by)
    unresolved = [f for f in failures if not f.get("fixed_by")]

    # Resolution rate
    resolved = len(failures) - len(unresolved)
    resolution_rate = (resolved / len(failures) * 100) if failures else 0

    return {
        "total": len(failures),
        "failures_sorted": failures_sorted,
        "ft_counter": ft_counter,
        "printer_counter": printer_counter,
        "material_counter": material_counter,
        "combo_counter": combo_counter,
        "ft_material_counter": ft_material_counter,
        "monthly": dict(sorted(monthly.items())),
        "unresolved": unresolved,
        "resolved": resolved,
        "resolution_rate": resolution_rate,
        "first_failure": failures_sorted[0].get("timestamp", "unknown"),
        "last_failure": failures_sorted[-1].get("timestamp", "unknown"),
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(data, days=None):
    """Generate a markdown report from analysis data."""
    now = datetime.now()
    lines = []

    title_suffix = f" (Last {days} Days)" if days else " (All Time)"
    lines.append(f"# 3D Print Failure Report{title_suffix}")
    lines.append(f"*Generated: {now.strftime('%Y-%m-%d %H:%M')}*")
    lines.append("")

    if data is None:
        lines.append("No failures found in the selected time range.")
        return "\n".join(lines)

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total Failures | {data['total']} |")
    lines.append(f"| Resolved | {data['resolved']} ({data['resolution_rate']:.0f}%) |")
    lines.append(f"| Unresolved | {len(data['unresolved'])} |")
    lines.append(f"| First Recorded | {data['first_failure'][:10]} |")
    lines.append(f"| Last Recorded | {data['last_failure'][:10]} |")
    lines.append("")

    # Most common failure types
    lines.append("## Most Common Failure Types")
    lines.append("")
    lines.append("| Rank | Failure Type | Count | % of Total |")
    lines.append("|------|--------------|-------|------------|")
    for i, (ft, count) in enumerate(data["ft_counter"].most_common(10), 1):
        pct = count / data["total"] * 100
        ft_display = ft.replace("_", " ").title()
        lines.append(f"| {i} | {ft_display} | {count} | {pct:.0f}% |")
    lines.append("")

    # Worst printer / material combos
    lines.append("## Printer Failure Counts")
    lines.append("")
    lines.append("| Printer | Failures |")
    lines.append("|---------|----------|")
    for printer, count in data["printer_counter"].most_common():
        lines.append(f"| {printer} | {count} |")
    lines.append("")

    lines.append("## Material Failure Counts")
    lines.append("")
    lines.append("| Material | Failures |")
    lines.append("|----------|----------|")
    for mat, count in data["material_counter"].most_common():
        lines.append(f"| {mat} | {count} |")
    lines.append("")

    lines.append("## Worst Printer × Material Combinations")
    lines.append("")
    lines.append("| Printer | Material | Failures |")
    lines.append("|---------|----------|----------|")
    for (printer, mat), count in data["combo_counter"].most_common(10):
        lines.append(f"| {printer} | {mat} | {count} |")
    lines.append("")

    # Recurring issues (same failure type + material, 2+ times)
    recurring = [(k, v) for k, v in data["ft_material_counter"].most_common() if v >= 2]
    if recurring:
        lines.append("## Recurring Issues")
        lines.append("")
        lines.append("Issues that have occurred 2+ times with the same material:")
        lines.append("")
        for (ft, mat), count in recurring:
            ft_display = ft.replace("_", " ").title()
            lines.append(f"- **{ft_display}** with **{mat}**: {count} occurrences")
        lines.append("")

    # Monthly trend
    if data["monthly"]:
        lines.append("## Failure Trend by Month")
        lines.append("")
        lines.append("| Month | Failures | Bar |")
        lines.append("|-------|----------|-----|")
        max_month_count = max(data["monthly"].values()) if data["monthly"] else 1
        for month, count in sorted(data["monthly"].items()):
            bar_len = int(count / max_month_count * 20)
            bar = "█" * bar_len
            lines.append(f"| {month} | {count} | {bar} |")
        lines.append("")

    # Unresolved failures
    if data["unresolved"]:
        lines.append("## Unresolved Failures")
        lines.append("")
        lines.append("These failures have no recorded fix yet:")
        lines.append("")
        for f in data["unresolved"]:
            ts = f.get("timestamp", "unknown")[:10]
            ft = f.get("failure_type", "unknown").replace("_", " ").title()
            printer = f.get("printer", "unknown")
            mat = f.get("material", "unknown")
            desc = f.get("description", "")[:80]
            lines.append(f"- **{ts}** | {printer} | {mat} | {ft}: {desc}")
        lines.append("")

    # Recommendations
    lines.append("## Top Recommendations")
    lines.append("")
    if data["ft_counter"]:
        top_ft, top_count = data["ft_counter"].most_common(1)[0]
        top_ft_display = top_ft.replace("_", " ").title()
        lines.append(f"1. **Focus on {top_ft_display}** — your most common failure ({top_count}x). "
                     f"Review `references/slicer-fixes.md` → {top_ft_display} for specific fixes.")

    if data["resolution_rate"] < 70:
        lines.append(f"2. **Low resolution rate ({data['resolution_rate']:.0f}%)** — "
                     f"try logging what fixes worked using `log_failure.py --fixed-by`.")

    if recurring:
        top_recurring_ft, top_recurring_mat = recurring[0][0]
        tr_display = top_recurring_ft.replace("_", " ").title()
        lines.append(f"3. **Recurring {tr_display} with {top_recurring_mat}** — "
                     f"consider a material change or dedicated calibration session.")

    lines.append("")
    lines.append("---")
    lines.append(f"*Report generated by print-failure-analyst. Log: `{LOG_FILE}`*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate a 3D print failure pattern report."
    )
    parser.add_argument(
        "--output", "-o",
        help="Save report to this file (default: print to stdout)"
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        help="Limit analysis to last N days (default: all time)"
    )

    args = parser.parse_args()

    data_raw = load_log()
    all_failures = data_raw.get("failures", [])

    if not all_failures:
        print("No failures logged yet. Use log_failure.py to start logging.")
        sys.exit(0)

    analysis = analyze(all_failures, days=args.days)
    report = generate_report(analysis, days=args.days)

    if args.output:
        try:
            with open(args.output, "w") as f:
                f.write(report)
            print(f"Report saved to: {args.output}")
        except IOError as e:
            print(f"Error writing report: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(report)


if __name__ == "__main__":
    main()
