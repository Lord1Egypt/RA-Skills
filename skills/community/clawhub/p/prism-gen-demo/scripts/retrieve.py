#!/usr/bin/env python3
"""
PRISM-Gen Skill — Retrieve
Retrieve and display data from any pipeline stage CSV.

Usage:
    python3 scripts/retrieve.py --stage step5b --columns name,smiles,pIC50,Broad_Spectrum_Score --max_rows 10
    python3 scripts/retrieve.py --stage step3c --smiles "NC(=O)Cc1ccc..."
    python3 scripts/retrieve.py --list_stages
    python3 scripts/retrieve.py --stage step4a --columns ALL
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import resolve_stage, read_csv, print_table, STAGE_FILES, STAGE_DESCRIPTIONS


def main():
    parser = argparse.ArgumentParser(description="Retrieve data from PRISM-Gen pipeline stages.")
    parser.add_argument("--stage", type=str, help="Pipeline stage key (e.g., step3a, step5b)")
    parser.add_argument("--columns", type=str, default=None, help="Comma-separated column names, or ALL")
    parser.add_argument("--smiles", type=str, default=None, help="Filter by exact SMILES match")
    parser.add_argument("--name", type=str, default=None, help="Filter by molecule name (e.g., mol_16)")
    parser.add_argument("--max_rows", type=int, default=20, help="Maximum rows to display")
    parser.add_argument("--list_stages", action="store_true", help="List all available pipeline stages")
    parser.add_argument("--list_columns", action="store_true", help="List columns for the given stage")
    args = parser.parse_args()

    if args.list_stages:
        print("Available pipeline stages:\n")
        for key in sorted(STAGE_FILES.keys()):
            print(f"  {key:15s}  {STAGE_DESCRIPTIONS[key]}")
        return

    if not args.stage:
        parser.print_help()
        return

    filepath, desc = resolve_stage(args.stage)
    headers, rows = read_csv(filepath)

    if args.list_columns:
        print(f"Stage: {args.stage} — {desc}")
        print(f"File: {os.path.basename(filepath)}")
        print(f"Rows: {len(rows)}, Columns: {len(headers)}\n")
        for i, h in enumerate(headers):
            print(f"  [{i:2d}] {h}")
        return

    # Filter by SMILES
    if args.smiles:
        rows = [r for r in rows if r.get("smiles", "") == args.smiles]

    # Filter by name
    if args.name:
        rows = [r for r in rows if r.get("name", "") == args.name]

    # Select columns
    if args.columns and args.columns.upper() != "ALL":
        selected = [c.strip() for c in args.columns.split(",")]
        missing = [c for c in selected if c not in headers]
        if missing:
            print(f"WARNING: Columns not found: {missing}", file=sys.stderr)
        selected = [c for c in selected if c in headers]
    else:
        # Default: show a sensible subset if too many columns
        if len(headers) > 12 and args.columns is None:
            priority = ["name", "smiles", "pIC50", "QED", "MW", "LogP", "Reward",
                        "R_total", "R_global", "Broad_Spectrum_Score",
                        "E_SARS_CoV_2", "E_SARS_CoV_1", "E_MERS_CoV",
                        "gap_ev", "hERG_Prob", "Lipinski_Pass", "Active_Set",
                        "Is_Final_Top", "Filter_Status", "Selection_Mode"]
            selected = [c for c in priority if c in headers]
            if not selected:
                selected = headers[:12]
        else:
            selected = headers

    print(f"Stage: {args.stage} — {desc}")
    print(f"Rows: {len(rows)} | Showing columns: {len(selected)}\n")
    print_table(selected, rows, max_rows=args.max_rows)


if __name__ == "__main__":
    main()
