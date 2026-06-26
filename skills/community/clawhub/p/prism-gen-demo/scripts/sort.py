#!/usr/bin/env python3
"""
PRISM-Gen Skill — Sort
Sort and rank molecules by any column.

Usage:
    python3 scripts/sort.py --stage step5b --by Broad_Spectrum_Score --ascending --top 10
    python3 scripts/sort.py --stage step4c --by R_global --top 20
    python3 scripts/sort.py --stage step3c --by R_total --columns smiles,pIC50,R_total,gap_ev
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import resolve_stage, read_csv, print_table, to_float


def main():
    parser = argparse.ArgumentParser(description="Sort and rank PRISM-Gen molecules.")
    parser.add_argument("--stage", type=str, required=True, help="Pipeline stage key")
    parser.add_argument("--by", type=str, required=True, help="Column to sort by")
    parser.add_argument("--ascending", action="store_true", help="Sort ascending (default: descending)")
    parser.add_argument("--top", type=int, default=20, help="Show top N results")
    parser.add_argument("--columns", type=str, default=None, help="Comma-separated columns to display")
    args = parser.parse_args()

    filepath, desc = resolve_stage(args.stage)
    headers, rows = read_csv(filepath)

    if args.by not in headers:
        print(f"ERROR: Column '{args.by}' not found.", file=sys.stderr)
        print(f"Available: {', '.join(headers[:30])}", file=sys.stderr)
        sys.exit(1)

    # Sort with numeric awareness
    def sort_key(row):
        val = to_float(row.get(args.by, ""))
        if val is None:
            return float("inf") if not args.ascending else float("-inf")
        return val

    rows.sort(key=sort_key, reverse=not args.ascending)

    # Add rank column
    for i, r in enumerate(rows):
        r["_rank"] = str(i + 1)

    display_rows = rows[:args.top]

    if args.columns:
        selected = ["_rank"] + [c.strip() for c in args.columns.split(",") if c.strip() in headers]
    else:
        selected = ["_rank", args.by]
        priority = ["name", "smiles", "pIC50", "QED", "Reward", "R_global",
                     "Broad_Spectrum_Score", "gap_ev", "hERG_Prob"]
        for c in priority:
            if c in headers and c != args.by and len(selected) < 10:
                selected.append(c)

    order_str = "ascending" if args.ascending else "descending"
    print(f"Stage: {args.stage} — {desc}")
    print(f"Sorted by: {args.by} ({order_str}) | Top {args.top}\n")
    print_table(selected, display_rows, max_rows=args.top)


if __name__ == "__main__":
    main()
