#!/usr/bin/env python3
"""
history.py — View 3D print failure history and detect recurring patterns.

Usage:
  history.py                          # Show all failures
  history.py --last 10               # Show last 10
  history.py --printer "Prusa MK4"   # Filter by printer
  history.py --material "PETG"       # Filter by material
  history.py --failure-type stringing # Filter by failure type
  history.py --patterns              # Show pattern analysis only
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(SKILL_DIR, "assets", "failure-log.json")


# ---------------------------------------------------------------------------
# Log loading
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


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def filter_failures(failures, printer=None, material=None, failure_type=None, last=None):
    """Apply filters to failure list."""
    result = failures

    if printer:
        result = [f for f in result if printer.lower() in f.get("printer", "").lower()]

    if material:
        result = [f for f in result if material.lower() in f.get("material", "").lower()]

    if failure_type:
        norm = failure_type.lower().replace(" ", "_").replace("-", "_")
        result = [f for f in result if norm in f.get("failure_type", "").lower()]

    # Sort by timestamp descending
    result = sorted(result, key=lambda x: x.get("timestamp", ""), reverse=True)

    if last:
        result = result[:last]

    return result


# ---------------------------------------------------------------------------
# Pattern detection
# ---------------------------------------------------------------------------

def detect_patterns(failures):
    """Detect recurring patterns in the failure log."""
    patterns = []
    now = datetime.now()
    thirty_days_ago = now - timedelta(days=30)
    ninety_days_ago = now - timedelta(days=90)

    # Parse timestamps
    def parse_ts(ts_str):
        try:
            return datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            return None

    # Count failure_type × material combinations in last 30 days
    recent = []
    for f in failures:
        ts = parse_ts(f.get("timestamp", ""))
        if ts and ts >= thirty_days_ago:
            recent.append(f)

    # Group by (failure_type, material)
    combo_counts = {}
    for f in recent:
        key = (f.get("failure_type", "unknown"), f.get("material", "unknown"))
        combo_counts[key] = combo_counts.get(key, 0) + 1

    for (ft, mat), count in sorted(combo_counts.items(), key=lambda x: -x[1]):
        if count >= 2:
            patterns.append(
                f"⚠ You've had {count} {ft.replace('_', ' ')} issue(s) with {mat} in the last 30 days."
            )

    # Most problematic printer
    printer_counts = {}
    for f in failures:
        ts = parse_ts(f.get("timestamp", ""))
        if ts and ts >= ninety_days_ago:
            printer = f.get("printer", "unknown")
            printer_counts[printer] = printer_counts.get(printer, 0) + 1

    if printer_counts:
        worst_printer = max(printer_counts, key=printer_counts.get)
        worst_count = printer_counts[worst_printer]
        if worst_count >= 3:
            patterns.append(
                f"🖨 {worst_printer} has had {worst_count} failures in the last 90 days — most of any printer."
            )

    # Most problematic material
    material_counts = {}
    for f in failures:
        ts = parse_ts(f.get("timestamp", ""))
        if ts and ts >= ninety_days_ago:
            mat = f.get("material", "unknown")
            material_counts[mat] = material_counts.get(mat, 0) + 1

    if material_counts:
        worst_mat = max(material_counts, key=material_counts.get)
        worst_mat_count = material_counts[worst_mat]
        if worst_mat_count >= 3:
            patterns.append(
                f"🧵 {worst_mat} has been involved in {worst_mat_count} failures in the last 90 days."
            )

    # Repeated same failure type overall
    all_ft_counts = {}
    for f in failures:
        ft = f.get("failure_type", "unknown")
        all_ft_counts[ft] = all_ft_counts.get(ft, 0) + 1

    top_ft = sorted(all_ft_counts.items(), key=lambda x: -x[1])
    if top_ft and top_ft[0][1] >= 3:
        ft_name, ft_count = top_ft[0]
        patterns.append(
            f"📊 '{ft_name.replace('_', ' ')}' is your most common failure type overall ({ft_count} occurrences)."
        )

    return patterns


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_failure(f, verbose=True):
    """Print a single failure entry."""
    ts = f.get("timestamp", "unknown")
    print(f"\n  [{ts}]")
    print(f"  Printer:  {f.get('printer', 'N/A')}")
    print(f"  Material: {f.get('material', 'N/A')}" +
          (f" ({f['material_brand']})" if f.get("material_brand") else ""))
    print(f"  Type:     {f.get('failure_type', 'N/A').replace('_', ' ')}")
    print(f"  Problem:  {f.get('description', 'N/A')}")

    if verbose:
        if f.get("slicer_settings"):
            settings = f["slicer_settings"]
            settings_str = ", ".join(f"{k}: {v}" for k, v in settings.items())
            print(f"  Settings: {settings_str}")
        if f.get("fixed_by"):
            print(f"  Fixed by: {f['fixed_by']}")
        if f.get("notes"):
            print(f"  Notes:    {f['notes']}")
        print(f"  ID:       {f.get('id', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="View 3D print failure history and detect patterns."
    )
    parser.add_argument("--printer", "-p", help="Filter by printer name (partial match)")
    parser.add_argument("--material", "-m", help="Filter by material (partial match, e.g. 'PETG')")
    parser.add_argument("--failure-type", "-f", help="Filter by failure type (e.g. 'stringing')")
    parser.add_argument("--last", "-n", type=int, help="Show only last N failures")
    parser.add_argument("--patterns", action="store_true", help="Show pattern analysis only")
    parser.add_argument("--no-patterns", action="store_true", help="Skip pattern analysis")
    parser.add_argument("--brief", "-b", action="store_true", help="Brief output (less detail per failure)")

    args = parser.parse_args()

    data = load_log()
    all_failures = data.get("failures", [])

    if not all_failures:
        print("No failures logged yet.")
        print(f"Use log_failure.py to log your first failure.")
        print(f"Log will be saved to: {LOG_FILE}")
        return

    print(f"\n{'=' * 60}")
    print(f"  3D Print Failure History")
    print(f"{'=' * 60}")
    print(f"  Total failures on record: {len(all_failures)}")

    # Pattern analysis (on all failures, before filtering)
    if not args.no_patterns:
        patterns = detect_patterns(all_failures)
        if patterns:
            print(f"\n  Pattern Analysis:")
            for p in patterns:
                print(f"    {p}")

    if args.patterns:
        # Patterns-only mode
        if not patterns:
            print("\n  No significant patterns detected yet.")
        return

    # Apply filters
    filtered = filter_failures(
        all_failures,
        printer=args.printer,
        material=args.material,
        failure_type=args.failure_type,
        last=args.last,
    )

    # Display filter summary
    filters_applied = []
    if args.printer:
        filters_applied.append(f"printer={args.printer}")
    if args.material:
        filters_applied.append(f"material={args.material}")
    if args.failure_type:
        filters_applied.append(f"type={args.failure_type}")
    if args.last:
        filters_applied.append(f"last={args.last}")

    print(f"\n  Showing {len(filtered)} failure(s)" +
          (f" [filters: {', '.join(filters_applied)}]" if filters_applied else ""))
    print(f"{'─' * 60}")

    if not filtered:
        print("  No failures match the given filters.")
        return

    for f in filtered:
        print_failure(f, verbose=not args.brief)

    print(f"\n{'─' * 60}")


if __name__ == "__main__":
    main()
