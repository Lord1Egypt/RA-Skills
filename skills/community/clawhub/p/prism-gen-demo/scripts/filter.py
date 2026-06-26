#!/usr/bin/env python3
"""
PRISM-Gen Skill — Filter
Filter molecules by property thresholds.

Usage:
    python3 scripts/filter.py --stage step4a --where "pIC50>7.5" "QED>0.7" "hERG_Prob<0.5"
    python3 scripts/filter.py --stage step5b --where "Broad_Spectrum_Score<-7.0" "Is_Final_Top==True"
    python3 scripts/filter.py --stage step3c --where "gap_ev>3.0" "gap_ev<6.0" --columns smiles,pIC50,gap_ev,R_total
"""

import argparse
import sys
import os
import operator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import resolve_stage, read_csv, print_table, to_float, to_bool


OPERATORS = {
    ">":  operator.gt,
    "<":  operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}


def parse_condition(cond_str):
    """Parse 'column>value' into (column, op_func, value_str)."""
    for op_str in [">=", "<=", "!=", "==", ">", "<"]:
        if op_str in cond_str:
            parts = cond_str.split(op_str, 1)
            if len(parts) == 2:
                return parts[0].strip(), OPERATORS[op_str], parts[1].strip()
    print(f"ERROR: Cannot parse condition '{cond_str}'. Use format: column>value", file=sys.stderr)
    sys.exit(1)


def apply_filter(rows, column, op_func, value_str):
    """Filter rows by a condition."""
    result = []
    for r in rows:
        cell = r.get(column, "")
        # Try numeric comparison first
        num_cell = to_float(cell)
        num_val = to_float(value_str)
        if num_cell is not None and num_val is not None:
            if op_func(num_cell, num_val):
                result.append(r)
        else:
            # String or bool comparison
            if value_str.lower() in ("true", "false"):
                if op_func(to_bool(cell), to_bool(value_str)):
                    result.append(r)
            else:
                if op_func(str(cell), value_str):
                    result.append(r)
    return result


def main():
    parser = argparse.ArgumentParser(description="Filter PRISM-Gen molecules by property thresholds.")
    parser.add_argument("--stage", type=str, required=True, help="Pipeline stage key")
    parser.add_argument("--where", nargs="+", required=True, help="Filter conditions (e.g., 'pIC50>7.5' 'QED>0.7')")
    parser.add_argument("--columns", type=str, default=None, help="Comma-separated columns to display")
    parser.add_argument("--max_rows", type=int, default=50, help="Maximum rows to display")
    parser.add_argument("--count_only", action="store_true", help="Only show count of matching rows")
    args = parser.parse_args()

    filepath, desc = resolve_stage(args.stage)
    headers, rows = read_csv(filepath)

    original_count = len(rows)
    for cond in args.where:
        col, op_func, val = parse_condition(cond)
        if col not in headers:
            print(f"ERROR: Column '{col}' not found. Available: {headers[:20]}...", file=sys.stderr)
            sys.exit(1)
        rows = apply_filter(rows, col, op_func, val)

    print(f"Stage: {args.stage} — {desc}")
    print(f"Filters: {' AND '.join(args.where)}")
    print(f"Result: {len(rows)} / {original_count} molecules passed\n")

    if args.count_only:
        return

    if args.columns:
        selected = [c.strip() for c in args.columns.split(",") if c.strip() in headers]
    else:
        selected = headers[:12] if len(headers) > 12 else headers

    print_table(selected, rows, max_rows=args.max_rows)


if __name__ == "__main__":
    main()
