#!/usr/bin/env python3
"""
PRISM-Gen Skill — Summary
Generate a full pipeline summary report.

Usage:
    python3 scripts/summary.py
    python3 scripts/summary.py --detailed
"""

import argparse
import sys
import os
import math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import get_data_dir, read_csv, to_float, to_bool, STAGE_FILES, STAGE_DESCRIPTIONS


def stats_line(vals):
    if not vals:
        return "N/A"
    n = len(vals)
    mean = sum(vals) / n
    std = math.sqrt(sum((v - mean) ** 2 for v in vals) / n) if n > 1 else 0
    return f"{mean:.3f} +/- {std:.3f} (N={n})"


def main():
    parser = argparse.ArgumentParser(description="PRISM-Gen pipeline summary.")
    parser.add_argument("--detailed", action="store_true", help="Include detailed per-stage statistics")
    args = parser.parse_args()

    data_dir = get_data_dir()
    print("=" * 70)
    print("  PRISM-Gen Pipeline Summary Report")
    print("=" * 70)

    # --- Attrition ---
    print("\n--- Pipeline Attrition ---\n")
    attrition = [
        ("Step 3a: Generation + Optimization", "step3a_optimized_molecules.csv", None),
        ("Step 3b: xTB Electronic Screening", "step3b_dft_results.csv", "status"),
        ("Step 3c: GEM Re-Ranking", "step3c_dft_refined.csv", None),
        ("Step 4a: ADMET Filtering", "step4a_admet_final.csv", "Active_Set"),
        ("Step 4b: DFT Validation (B3LYP)", "step4b_top_molecules_pyscf.csv", None),
        ("Step 5a: Broad-Spectrum Docking", "step5a_broadspectrum_docking.csv", None),
        ("Step 5b: Final Candidates", "step5b_final_candidates.csv", "Is_Final_Top"),
    ]

    for label, fname, filter_col in attrition:
        path = os.path.join(data_dir, fname)
        if not os.path.isfile(path):
            print(f"  {label:45s}  (file not found)")
            continue
        _, rows = read_csv(path)
        total = len(rows)
        if filter_col:
            if filter_col == "status":
                passed = sum(1 for r in rows if "success" in r.get(filter_col, "").lower())
            else:
                passed = sum(1 for r in rows if to_bool(r.get(filter_col, "")))
            print(f"  {label:45s}  {passed:4d} / {total} passed")
        else:
            print(f"  {label:45s}  {total:4d} molecules")

    # --- Final candidates overview ---
    path_5b = os.path.join(data_dir, "step5b_final_candidates.csv")
    if os.path.isfile(path_5b):
        _, rows_5b = read_csv(path_5b)
        final = [r for r in rows_5b if to_bool(r.get("Is_Final_Top", ""))]

        print(f"\n--- Final Candidates (N={len(final)}) ---\n")

        pic50_vals = [to_float(r.get("pIC50")) for r in final]
        pic50_vals = [v for v in pic50_vals if v is not None]
        print(f"  pIC50:              {stats_line(pic50_vals)}")

        qed_vals = [to_float(r.get("QED")) for r in final]
        qed_vals = [v for v in qed_vals if v is not None]
        print(f"  QED:                {stats_line(qed_vals)}")

        broad_vals = [to_float(r.get("Broad_Spectrum_Score")) for r in final]
        broad_vals = [v for v in broad_vals if v is not None]
        print(f"  Broad_Spectrum:     {stats_line(broad_vals)}")

        rglobal_vals = [to_float(r.get("R_global")) for r in final]
        rglobal_vals = [v for v in rglobal_vals if v is not None]
        print(f"  R_global:           {stats_line(rglobal_vals)}")

        gap_vals = [to_float(r.get("PySCF_Gap_eV")) for r in final]
        gap_vals = [v for v in gap_vals if v is not None]
        if gap_vals:
            print(f"  PySCF_Gap_eV:       {stats_line(gap_vals)}")

        # Lipinski pass rate
        lip = sum(1 for r in final if to_bool(r.get("Lipinski_Pass", "")))
        print(f"  Lipinski Pass:      {lip}/{len(final)} ({100*lip/len(final) if final else 0:.0f}%)")

        # hERG risk
        herg = sum(1 for r in final if to_bool(r.get("hERG_Risk", "")))
        print(f"  hERG High Risk:     {herg}/{len(final)} ({100*herg/len(final) if final else 0:.0f}%)")

    # --- Top 5 by broad-spectrum score ---
    path_5a = os.path.join(data_dir, "step5a_broadspectrum_docking.csv")
    if os.path.isfile(path_5a):
        _, rows_5a = read_csv(path_5a)
        for r in rows_5a:
            r["_sort"] = to_float(r.get("Broad_Spectrum_Score"), 0)
        rows_5a.sort(key=lambda x: x["_sort"])

        print(f"\n--- Top 5 by Worst-Case Broad-Spectrum Score ---\n")
        print(f"  {'Rank':<6s} {'Name':<12s} {'E(6W63)':>10s} {'E(3V3M)':>10s} {'E(4YLU)':>10s} {'Score_broad':>12s}")
        print("  " + "-" * 62)
        for i, r in enumerate(rows_5a[:5]):
            name = r.get("name", "?")
            e1 = r.get("E_SARS_CoV_2", "")
            e2 = r.get("E_SARS_CoV_1", "")
            e3 = r.get("E_MERS_CoV", "")
            sc = r.get("Broad_Spectrum_Score", "")
            print(f"  {i+1:<6d} {name:<12s} {e1:>10s} {e2:>10s} {e3:>10s} {sc:>12s}")

    if args.detailed:
        print(f"\n--- Detailed Per-Stage Statistics ---\n")
        for key in sorted(STAGE_FILES.keys()):
            path = os.path.join(data_dir, STAGE_FILES[key])
            if not os.path.isfile(path):
                continue
            headers, rows = read_csv(path)
            print(f"\n  {key} ({STAGE_DESCRIPTIONS[key]})")
            print(f"    Rows: {len(rows)}, Columns: {len(headers)}")
            # Show stats for key numeric columns
            for col in ["pIC50", "QED", "Reward", "R_total", "R_global", "gap_ev",
                         "Broad_Spectrum_Score", "PySCF_Gap_eV"]:
                if col in headers:
                    vals = [to_float(r.get(col)) for r in rows]
                    vals = [v for v in vals if v is not None]
                    if vals:
                        print(f"    {col:25s} {stats_line(vals)}")

    print("\n" + "=" * 70)
    print("  Report complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
