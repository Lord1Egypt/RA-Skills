#!/usr/bin/env python3
"""
compare.py - Filter check_prices.py output for significant price changes.

Usage:
  python3 check_prices.py | python3 compare.py [--threshold PERCENT]
  python3 compare.py --threshold 10 < results.json

Options:
  --threshold N   Minimum % change to report (default: 5)

Exits 0 with output when changes found, exits 0 with empty JSON array when none.
Exits 1 on input error.
"""

import json
import sys


def parse_threshold(args):
    threshold = 5.0
    for i, arg in enumerate(args):
        if arg == "--threshold" and i + 1 < len(args):
            try:
                threshold = float(args[i + 1])
            except ValueError:
                print(f"[ERROR] Invalid threshold: {args[i + 1]}", file=sys.stderr)
                sys.exit(1)
    return threshold


def main():
    threshold = parse_threshold(sys.argv[1:])

    raw = sys.stdin.read().strip()
    if not raw:
        print("[ERROR] No input received. Pipe check_prices.py output to this script.", file=sys.stderr)
        sys.exit(1)

    try:
        results = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(results, list):
        print("[ERROR] Expected a JSON array from check_prices.py", file=sys.stderr)
        sys.exit(1)

    significant = []
    for item in results:
        status = item.get("status", "ok")

        # Always surface errors
        if status in ("fetch_error", "no_price"):
            significant.append(item)
            continue

        change_pct = item.get("change_pct")
        if change_pct is None:
            continue

        if abs(change_pct) >= threshold:
            significant.append(item)

    print(json.dumps(significant, indent=2))

    # Summary to stderr
    total = len(results)
    ok = sum(1 for r in results if r.get("status") == "ok")
    errors = total - ok
    changes = sum(1 for r in significant if r.get("status") == "ok")

    print(f"[INFO] Checked {total} products | {ok} OK | {errors} errors | {changes} above {threshold}% threshold", file=sys.stderr)


if __name__ == "__main__":
    main()
