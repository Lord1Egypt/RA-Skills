#!/usr/bin/env python3
"""
PRISM-Gen Skill — Plot
Generate visualizations for pipeline data.

Usage:
    python3 scripts/plot.py --mode histogram --stage step4a --column pIC50 --output hist_pIC50.png
    python3 scripts/plot.py --mode scatter --stage step5b --x pIC50 --y Broad_Spectrum_Score --output scatter.png
    python3 scripts/plot.py --mode heatmap --stage step5a --output heatmap.png
    python3 scripts/plot.py --mode funnel --output funnel.png
    python3 scripts/plot.py --mode pareto --stage step5b --x pIC50 --y QED --output pareto.png
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import resolve_stage, read_csv, to_float, get_data_dir, STAGE_FILES

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def check_matplotlib():
    if not HAS_MPL:
        print("ERROR: matplotlib is required for plotting. Install with: pip install matplotlib", file=sys.stderr)
        sys.exit(1)


def plot_histogram(stage, column, output, bins=30):
    check_matplotlib()
    filepath, desc = resolve_stage(stage)
    _, rows = read_csv(filepath)
    vals = [to_float(r.get(column)) for r in rows]
    vals = [v for v in vals if v is not None]
    if not vals:
        print(f"ERROR: No numeric data in column '{column}'.", file=sys.stderr)
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(vals, bins=bins, color="#4C72B0", edgecolor="white", alpha=0.85)
    ax.set_xlabel(column, fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title(f"{column} Distribution — {stage} (N={len(vals)})", fontsize=13)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    print(f"Saved: {output}")


def plot_scatter(stage, x_col, y_col, output, color_col=None):
    check_matplotlib()
    filepath, desc = resolve_stage(stage)
    headers, rows = read_csv(filepath)
    xs, ys, cs, labels = [], [], [], []
    for r in rows:
        xv = to_float(r.get(x_col))
        yv = to_float(r.get(y_col))
        if xv is not None and yv is not None:
            xs.append(xv)
            ys.append(yv)
            cs.append(to_float(r.get(color_col, ""), 0.5) if color_col else 0.5)
            labels.append(r.get("name", ""))

    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(xs, ys, c=cs if color_col else "#4C72B0",
                         cmap="viridis" if color_col else None,
                         alpha=0.7, edgecolors="white", linewidth=0.5, s=50)
    if color_col:
        plt.colorbar(scatter, label=color_col)

    # Label top points
    if labels:
        for i in range(min(5, len(labels))):
            if labels[i]:
                ax.annotate(labels[i], (xs[i], ys[i]), fontsize=7, alpha=0.7)

    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)
    ax.set_title(f"{x_col} vs {y_col} — {stage}", fontsize=13)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    print(f"Saved: {output}")


def plot_heatmap(stage, output):
    check_matplotlib()
    filepath, desc = resolve_stage(stage)
    _, rows = read_csv(filepath)
    targets = ["E_SARS_CoV_2", "E_SARS_CoV_1", "E_MERS_CoV"]
    names = []
    matrix = []
    for r in rows:
        name = r.get("name", r.get("smiles", "?")[:20])
        energies = [to_float(r.get(t)) for t in targets]
        if all(e is not None for e in energies):
            names.append(name)
            matrix.append(energies)

    if not matrix:
        print("ERROR: No complete docking data found.", file=sys.stderr)
        return

    fig, ax = plt.subplots(figsize=(8, max(4, len(names) * 0.35)))
    im = ax.imshow(matrix, cmap="RdYlGn_r", aspect="auto")
    ax.set_xticks(range(len(targets)))
    ax.set_xticklabels(["SARS-CoV-2\n(6W63)", "SARS-CoV-1\n(3V3M)", "MERS-CoV\n(4YLU)"], fontsize=10)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)

    # Annotate cells
    for i in range(len(matrix)):
        for j in range(len(targets)):
            ax.text(j, i, f"{matrix[i][j]:.1f}", ha="center", va="center", fontsize=8)

    plt.colorbar(im, label="Docking Energy (kcal/mol)", shrink=0.8)
    ax.set_title("Multi-Target Docking Score Heatmap", fontsize=13)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    print(f"Saved: {output}")


def plot_funnel(output):
    check_matplotlib()
    data_dir = get_data_dir()
    stages = [
        ("Generated", "step3a_optimized_molecules.csv"),
        ("xTB screened", "step3c_dft_refined.csv"),
        ("ADMET filtered", "step4a_admet_final.csv"),
        ("DFT validated", "step4b_top_molecules_pyscf.csv"),
        ("Docking (broad)", "step5a_broadspectrum_docking.csv"),
        ("Final candidates", "step5b_final_candidates.csv"),
    ]
    counts = []
    labels = []
    for label, fname in stages:
        path = os.path.join(data_dir, fname)
        if os.path.isfile(path):
            _, rows = read_csv(path)
            # For step4a, count Active_Set=True if available
            if "admet" in fname:
                active = [r for r in rows if r.get("Active_Set", "").lower() == "true"]
                counts.append(len(active) if active else len(rows))
            else:
                counts.append(len(rows))
            labels.append(label)

    if not counts:
        print("ERROR: No stage files found.", file=sys.stderr)
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.Blues([(i + 2) / (len(counts) + 2) for i in range(len(counts))])
    bars = ax.barh(range(len(counts)), counts, color=colors, edgecolor="white", height=0.6)
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(labels, fontsize=11)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Molecules", fontsize=12)
    ax.set_title("PRISM-Gen Pipeline Attrition Funnel", fontsize=13)

    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + max(counts) * 0.02, bar.get_y() + bar.get_height() / 2,
                str(count), va="center", fontsize=11, fontweight="bold")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    print(f"Saved: {output}")


def plot_pareto(stage, x_col, y_col, output):
    check_matplotlib()
    filepath, _ = resolve_stage(stage)
    headers, rows = read_csv(filepath)
    points = []
    for r in rows:
        xv = to_float(r.get(x_col))
        yv = to_float(r.get(y_col))
        if xv is not None and yv is not None:
            points.append((xv, yv, r.get("name", "")))

    # Find Pareto front (maximizing both)
    pareto = []
    for p in points:
        dominated = any(q[0] >= p[0] and q[1] >= p[1] and (q[0] > p[0] or q[1] > p[1]) for q in points)
        pareto.append(not dominated)

    fig, ax = plt.subplots(figsize=(8, 6))
    non_pareto = [(p[0], p[1]) for p, is_p in zip(points, pareto) if not is_p]
    pareto_pts = [(p[0], p[1], p[2]) for p, is_p in zip(points, pareto) if is_p]

    if non_pareto:
        ax.scatter([p[0] for p in non_pareto], [p[1] for p in non_pareto],
                   c="#CCCCCC", alpha=0.5, s=30, label="Dominated")
    if pareto_pts:
        ax.scatter([p[0] for p in pareto_pts], [p[1] for p in pareto_pts],
                   c="#E74C3C", s=60, edgecolors="white", linewidth=0.5, label="Pareto front", zorder=5)
        for p in pareto_pts[:8]:
            if p[2]:
                ax.annotate(p[2], (p[0], p[1]), fontsize=7, alpha=0.8)

    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)
    ax.set_title(f"Pareto Front: {x_col} vs {y_col}", fontsize=13)
    ax.legend(fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    print(f"Saved: {output}")


def main():
    parser = argparse.ArgumentParser(description="PRISM-Gen visualization.")
    parser.add_argument("--mode", type=str, required=True,
                        choices=["histogram", "scatter", "heatmap", "funnel", "pareto"],
                        help="Plot type")
    parser.add_argument("--stage", type=str, default="step5b", help="Pipeline stage")
    parser.add_argument("--column", type=str, default="pIC50", help="Column for histogram")
    parser.add_argument("--x", type=str, default="pIC50", help="X-axis column")
    parser.add_argument("--y", type=str, default="QED", help="Y-axis column")
    parser.add_argument("--color", type=str, default=None, help="Color-by column for scatter")
    parser.add_argument("--output", type=str, default="plot.png", help="Output file path")
    parser.add_argument("--bins", type=int, default=30, help="Number of bins for histogram")
    args = parser.parse_args()

    if args.mode == "histogram":
        plot_histogram(args.stage, args.column, args.output, args.bins)
    elif args.mode == "scatter":
        plot_scatter(args.stage, args.x, args.y, args.output, args.color)
    elif args.mode == "heatmap":
        plot_heatmap(args.stage, args.output)
    elif args.mode == "funnel":
        plot_funnel(args.output)
    elif args.mode == "pareto":
        plot_pareto(args.stage, args.x, args.y, args.output)


if __name__ == "__main__":
    main()
