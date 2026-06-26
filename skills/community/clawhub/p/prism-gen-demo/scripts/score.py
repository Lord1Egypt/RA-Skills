#!/usr/bin/env python3
"""
PRISM-Gen Skill — Score
Compute composite scores, multi-target worst-case analysis, and summary metrics.

Usage:
    python3 scripts/score.py --mode worst_case --stage step5a --top 10
    python3 scripts/score.py --mode composite --stage step4c --weights "pIC50:1.0,QED:0.5,R_ADMET:2.0"
    python3 scripts/score.py --mode stats --stage step5b --columns pIC50,QED,Broad_Spectrum_Score
    python3 scripts/score.py --mode pareto --stage step5b --obj1 pIC50 --obj2 Broad_Spectrum_Score
"""

import argparse
import sys
import os
import math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import resolve_stage, read_csv, print_table, to_float


def worst_case_analysis(rows, top_n):
    """Rank by worst-case (maximum, least negative) docking score across 3 targets."""
    targets = ["E_SARS_CoV_2", "E_SARS_CoV_1", "E_MERS_CoV"]
    scored = []
    for r in rows:
        energies = [to_float(r.get(t)) for t in targets]
        energies = [e for e in energies if e is not None]
        if energies:
            worst = max(energies)  # least negative = weakest binding
            mean_e = sum(energies) / len(energies)
            var_e = sum((e - mean_e) ** 2 for e in energies) / len(energies)
            r["_worst_case"] = f"{worst:.1f}"
            r["_mean_E"] = f"{mean_e:.2f}"
            r["_variance"] = f"{var_e:.3f}"
            r["_sort_key"] = worst
            scored.append(r)

    scored.sort(key=lambda x: x["_sort_key"])
    for i, r in enumerate(scored):
        r["_rank"] = str(i + 1)

    display_cols = ["_rank", "name", "smiles", "E_SARS_CoV_2", "E_SARS_CoV_1",
                    "E_MERS_CoV", "_worst_case", "_mean_E", "_variance"]
    display_cols = [c for c in display_cols if any(r.get(c) for r in scored[:1])]

    print(f"Worst-case broad-spectrum ranking (Score_broad = max E_i)\n")
    print_table(display_cols, scored[:top_n], max_rows=top_n)


def composite_score(rows, headers, weights_str, top_n):
    """Compute a custom weighted composite score."""
    weights = {}
    for item in weights_str.split(","):
        parts = item.strip().split(":")
        if len(parts) == 2:
            weights[parts[0].strip()] = to_float(parts[1].strip(), 1.0)

    for col in weights:
        if col not in headers:
            print(f"WARNING: Column '{col}' not found, skipping.", file=sys.stderr)

    for r in rows:
        score = 0.0
        for col, w in weights.items():
            val = to_float(r.get(col))
            if val is not None:
                score += w * val
        r["_composite"] = f"{score:.4f}"
        r["_sort_val"] = score

    rows.sort(key=lambda x: x.get("_sort_val", 0), reverse=True)
    for i, r in enumerate(rows):
        r["_rank"] = str(i + 1)

    display_cols = ["_rank", "_composite"] + list(weights.keys())
    if "name" in headers:
        display_cols.insert(1, "name")
    if "smiles" in headers:
        display_cols.insert(2, "smiles")

    print(f"Composite score: {weights_str}\n")
    print_table(display_cols, rows[:top_n], max_rows=top_n)


def summary_stats(rows, headers, columns_str):
    """Compute summary statistics for selected columns."""
    cols = [c.strip() for c in columns_str.split(",")]
    print(f"{'Column':25s} {'N':>6s} {'Mean':>10s} {'Std':>10s} {'Min':>10s} {'Med':>10s} {'Max':>10s}")
    print("-" * 85)
    for col in cols:
        if col not in headers:
            print(f"{col:25s}  (not found)")
            continue
        vals = [to_float(r.get(col)) for r in rows]
        vals = [v for v in vals if v is not None]
        if not vals:
            print(f"{col:25s}  (no numeric data)")
            continue
        n = len(vals)
        mean = sum(vals) / n
        std = math.sqrt(sum((v - mean) ** 2 for v in vals) / n) if n > 1 else 0
        vals_sorted = sorted(vals)
        median = vals_sorted[n // 2]
        print(f"{col:25s} {n:6d} {mean:10.4f} {std:10.4f} {vals_sorted[0]:10.4f} {median:10.4f} {vals_sorted[-1]:10.4f}")


def pareto_analysis(rows, headers, obj1, obj2, top_n):
    """Identify Pareto-optimal molecules for two objectives."""
    scored = []
    for r in rows:
        v1 = to_float(r.get(obj1))
        v2 = to_float(r.get(obj2))
        if v1 is not None and v2 is not None:
            r["_obj1"] = v1
            r["_obj2"] = v2
            scored.append(r)

    # Find Pareto front (maximizing both objectives)
    pareto = []
    for r in scored:
        dominated = False
        for s in scored:
            if s["_obj1"] >= r["_obj1"] and s["_obj2"] >= r["_obj2"] and \
               (s["_obj1"] > r["_obj1"] or s["_obj2"] > r["_obj2"]):
                dominated = True
                break
        r["_pareto"] = "Yes" if not dominated else "No"
        if not dominated:
            pareto.append(r)

    pareto.sort(key=lambda x: x["_obj1"], reverse=True)
    for i, r in enumerate(pareto):
        r["_rank"] = str(i + 1)

    display_cols = ["_rank", obj1, obj2, "_pareto"]
    if "name" in headers:
        display_cols.insert(1, "name")
    if "smiles" in headers:
        display_cols.insert(2, "smiles")

    print(f"Pareto front: {obj1} vs {obj2}")
    print(f"Pareto-optimal molecules: {len(pareto)} / {len(scored)}\n")
    print_table(display_cols, pareto[:top_n], max_rows=top_n)


def main():
    parser = argparse.ArgumentParser(description="PRISM-Gen scoring and analysis.")
    parser.add_argument("--mode", type=str, required=True,
                        choices=["worst_case", "composite", "stats", "pareto"],
                        help="Analysis mode")
    parser.add_argument("--stage", type=str, required=True, help="Pipeline stage key")
    parser.add_argument("--top", type=int, default=20, help="Top N results")
    parser.add_argument("--weights", type=str, default="pIC50:1.0,QED:0.5",
                        help="Weights for composite score (col:weight,...)")
    parser.add_argument("--columns", type=str, default="pIC50,QED,MW,LogP",
                        help="Columns for stats mode")
    parser.add_argument("--obj1", type=str, default="pIC50", help="First objective for Pareto")
    parser.add_argument("--obj2", type=str, default="QED", help="Second objective for Pareto")
    args = parser.parse_args()

    filepath, desc = resolve_stage(args.stage)
    headers, rows = read_csv(filepath)

    print(f"Stage: {args.stage} — {desc}\n")

    if args.mode == "worst_case":
        worst_case_analysis(rows, args.top)
    elif args.mode == "composite":
        composite_score(rows, headers, args.weights, args.top)
    elif args.mode == "stats":
        summary_stats(rows, headers, args.columns)
    elif args.mode == "pareto":
        pareto_analysis(rows, headers, args.obj1, args.obj2, args.top)


if __name__ == "__main__":
    main()
