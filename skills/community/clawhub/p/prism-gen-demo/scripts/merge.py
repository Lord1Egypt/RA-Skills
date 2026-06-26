#!/usr/bin/env python3
"""
PRISM-Gen Skill — Merge
Merge/join data across pipeline stages on SMILES keys.

Usage:
    python3 scripts/merge.py --stages step3c,step4a --on smiles --columns pIC50,gap_ev,R_total,Lipinski_Pass,hERG_Prob
    python3 scripts/merge.py --stages step3c,step5a --on smiles --top 36
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import resolve_stage, read_csv, print_table


def main():
    parser = argparse.ArgumentParser(description="Merge PRISM-Gen pipeline stages.")
    parser.add_argument("--stages", type=str, required=True, help="Comma-separated stage keys (e.g., step3c,step4a)")
    parser.add_argument("--on", type=str, default="smiles", help="Join key column (default: smiles)")
    parser.add_argument("--how", type=str, default="inner", choices=["inner", "left"], help="Join type")
    parser.add_argument("--columns", type=str, default=None, help="Columns to include in output")
    parser.add_argument("--top", type=int, default=50, help="Max rows to display")
    args = parser.parse_args()

    stage_keys = [s.strip() for s in args.stages.split(",")]
    if len(stage_keys) < 2:
        print("ERROR: Need at least 2 stages to merge.", file=sys.stderr)
        sys.exit(1)

    # Load all stages
    all_data = {}
    all_headers = []
    for key in stage_keys:
        filepath, desc = resolve_stage(key)
        headers, rows = read_csv(filepath)
        if args.on not in headers:
            print(f"ERROR: Join key '{args.on}' not in stage {key}.", file=sys.stderr)
            sys.exit(1)
        all_data[key] = {r[args.on]: r for r in rows}
        # Collect headers with stage prefix for disambiguation
        for h in headers:
            if h == args.on:
                if h not in all_headers:
                    all_headers.append(h)
            else:
                prefixed = f"{key}.{h}" if h in [hh.split(".")[-1] for hh in all_headers] else h
                if prefixed not in all_headers and h not in all_headers:
                    all_headers.append(h)

    # Merge
    base_key = stage_keys[0]
    base_data = all_data[base_key]

    if args.how == "inner":
        common_keys = set(base_data.keys())
        for key in stage_keys[1:]:
            common_keys &= set(all_data[key].keys())
        merge_keys = common_keys
    else:
        merge_keys = set(base_data.keys())

    merged_rows = []
    for join_val in merge_keys:
        merged = {args.on: join_val}
        for key in stage_keys:
            row = all_data[key].get(join_val, {})
            for col, val in row.items():
                if col != args.on:
                    if col not in merged:
                        merged[col] = val
                    else:
                        merged[f"{key}.{col}"] = val
        merged_rows.append(merged)

    # Determine display columns
    if args.columns:
        selected = [args.on] + [c.strip() for c in args.columns.split(",")]
    else:
        available = list(merged_rows[0].keys()) if merged_rows else []
        selected = available[:15]

    print(f"Merged stages: {', '.join(stage_keys)}")
    print(f"Join key: {args.on} ({args.how}) | Result: {len(merged_rows)} rows\n")
    print_table(selected, merged_rows, max_rows=args.top)


if __name__ == "__main__":
    main()
