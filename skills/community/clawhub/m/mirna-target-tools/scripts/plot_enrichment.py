#!/usr/bin/env python3
"""
Publication-style enrichment dot plot.

Input : enrichment TSV produced by annotate_targets.py (g:Profiler output)
Output: PNG (+ optional SVG) dot plot - terms ranked by significance,
        bubble size = genes in term, bubble colour = significance.

Usage:
  python plot_enrichment.py --input merged_enrichment_all.tsv \
      --output enrichment_bubble.png --source GO:BP --top 15

Styling notes
-------------
* clusterProfiler-like dot plot, re-drawn with a clean, journal-friendly look:
  white bubble edges, no top/right spines, thin grey grid, left-aligned title,
  wrapped term labels, size legend and a slim colour bar.
* Colours encode significance on a perceptually ordered blue -> red ramp, so
  the plot stays readable in greyscale (dark = more significant).
* Writes 300 dpi PNG by default; pass --svg to also emit a vector version with
  editable text (useful for Illustrator/Inkscape touch-ups).

Dependencies: pandas, numpy, matplotlib
"""

import argparse
import os
import shutil
import subprocess
import sys
import textwrap

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

# blue -> amber -> red ramp: low significance (light/blue) -> high (dark red)
SIG_CMAP = LinearSegmentedColormap.from_list(
    'significance',
    ['#2C6BA8', '#4E9BD6', '#9FC9E8', '#F2E3B8', '#E9A03B', '#D2603A', '#B02418'])

SKILL_SCRIPTS = os.path.dirname(os.path.abspath(__file__))
R_PLOT_SCRIPT = os.path.join(SKILL_SCRIPTS, 'plot_enrichment.R')
R_PLOT_PKGS = ('ggplot2', 'dplyr', 'stringr', 'scales')

INK = '#222222'
MUTED = '#6b7280'
GRID = '#e9e9e9'


def style_axes(ax):
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color('#c9ccd1')
        ax.spines[side].set_linewidth(0.9)
    ax.tick_params(colors=MUTED, length=3, width=0.9)
    ax.tick_params(axis='y', length=0)
    ax.set_axisbelow(True)
    ax.grid(axis='x', color=GRID, linewidth=0.9)
    ax.grid(axis='y', visible=False)


def bubble_sizes(values):
    """Map gene counts to marker areas (points^2) with a sensible floor."""
    v = np.asarray(values, dtype=float)
    lo, hi = float(v.min()), float(v.max())
    if hi <= lo:
        return np.full_like(v, 90.0)
    return 22.0 + 300.0 * (v - lo) / (hi - lo)


def size_legend_handles(values, color='#b9c2cc'):
    v = np.asarray(values, dtype=float)
    lo, hi = float(v.min()), float(v.max())
    picks = sorted({int(round(x)) for x in (lo, (lo + hi) / 2.0, hi)})
    areas = bubble_sizes(np.array(picks, dtype=float))
    handles = [
        Line2D([], [], marker='o', linestyle='none', color=color,
               markeredgecolor='white', markeredgewidth=0.8,
               markersize=2.0 * np.sqrt(a / np.pi), label=str(p))
        for a, p in zip(areas, picks)
    ]
    return handles


def r_engine_status():
    """Return (ok, message) for the R plotting engine (Rscript + packages)."""
    if shutil.which('Rscript') is None:
        return False, 'Rscript not found on PATH'
    check = ' && '.join('requireNamespace("%s", quietly=TRUE)' % p for p in R_PLOT_PKGS)
    try:
        proc = subprocess.run(['Rscript', '-e', 'cat(%s)' % check],
                              capture_output=True, text=True, timeout=180)
    except Exception as exc:                      # pragma: no cover
        return False, 'Rscript failed: %s' % exc
    if proc.stdout.strip().upper().startswith('TRUE'):
        return True, 'R + ' + '/'.join(R_PLOT_PKGS)
    return False, 'missing R packages: %s' % ', '.join(R_PLOT_PKGS)


def run_r_plot(args):
    """Draw with the ggplot2 script. Returns a process return code."""
    if not os.path.exists(R_PLOT_SCRIPT):
        print('R plotting script not found: %s' % R_PLOT_SCRIPT)
        return 1
    cmd = ['Rscript', R_PLOT_SCRIPT,
           '--input', args.input, '--output', args.output,
           '--top', str(args.top), '--dpi', str(args.dpi),
           '--wrap', str(args.wrap), '--sort', args.sort]
    if args.source:
        cmd += ['--source', args.source]
    if args.title:
        cmd += ['--title', args.title]
    if getattr(args, 'color_by', 'p_value'):
        cmd += ['--color-by', args.color_by]
    if args.svg:
        cmd += ['--svg']
    if args.figsize:
        try:
            w, h = [x.strip() for x in args.figsize.split(',')]
            cmd += ['--width', w, '--height', h]
        except ValueError:
            pass
    print('Plotting with R (ggplot2) ...')
    return subprocess.call(cmd)


def main():
    ap = argparse.ArgumentParser(
        description='Publication-style enrichment dot plot')
    ap.add_argument('--input', required=True, help='Enrichment TSV from annotate_targets.py')
    ap.add_argument('--output', required=True, help='Output image (PNG; .svg if --svg)')
    ap.add_argument('--source', default=None,
                    help='Restrict to one source (GO:BP/GO:CC/GO:MF/KEGG); default: all')
    ap.add_argument('--top', type=int, default=15, help='Top N terms by p-value (default 15)')
    ap.add_argument('--figsize', default=None,
                    help='Figure size "width,height" in inches (default: adaptive)')
    ap.add_argument('--title', default=None, help='Custom plot title')
    ap.add_argument('--wrap', type=int, default=46, help='Wrap term labels at N chars (default 46)')
    ap.add_argument('--color-by', default='p_value',
                    help="Column for bubble colour (default p_value; e.g. padj if present)")
    ap.add_argument('--sort', default='p', choices=['p', 'size'],
                    help='Rank terms by significance (p) or by gene count (size)')
    ap.add_argument('--dpi', type=int, default=300, help='Raster DPI (default 300)')
    ap.add_argument('--svg', action='store_true', help='Also write a vector SVG next to --output')
    ap.add_argument('--engine', default='auto', choices=['auto', 'r', 'python'],
                    help='Plotting engine: auto (R when available, else Python), '
                         'r (ggplot2, default choice), python (matplotlib fallback)')
    args = ap.parse_args()

    if not os.path.exists(args.input):
        print("Error: input file '%s' not found!" % args.input)
        sys.exit(1)

    # ---- default: draw with R (ggplot2) -----------------------------------
    if args.engine in ('auto', 'r'):
        ok, why = r_engine_status()
        if ok:
            rc = run_r_plot(args)
            if rc == 0:
                return
            print('Warning: R plotting failed (exit %d).' % rc)
        else:
            print('R plotting engine unavailable: %s' % why)
        if args.engine == 'r':
            print('Install it with: bash %s/install_r_deps.sh'
                  % os.path.dirname(os.path.abspath(__file__)))
            sys.exit(1)
        print('Falling back to the Python (matplotlib) engine.')
        print('To use the R engine: bash %s/install_r_deps.sh'
              % os.path.dirname(os.path.abspath(__file__)))

    df = pd.read_csv(args.input, sep='\t')
    if 'name' not in df.columns or 'p_value' not in df.columns:
        print("Error: input must have 'name' and 'p_value' columns.")
        print("Found columns: %s" % list(df.columns))
        sys.exit(1)

    source = args.source
    if source:
        if 'source' not in df.columns:
            print("Error: --source requested but input has no 'source' column.")
            sys.exit(1)
        df = df[df['source'] == source]
        if len(df) == 0:
            print("No terms for source '%s'." % source)
            sys.exit(1)
    multi_source = 'source' in df.columns and df['source'].nunique() > 1

    size_col = next((c for c in ('intersection_size', 'query_size', 'term_size')
                     if c in df.columns), None)
    if size_col is None:
        df['_size'] = 1
        size_col = '_size'

    color_col = args.color_by if args.color_by in df.columns else 'p_value'
    df = df.sort_values('p_value' if args.sort == 'p' else size_col,
                        ascending=args.sort == 'p').head(args.top).copy()
    df['neg_log10_p'] = df['p_value'].apply(
        lambda x: -np.log10(x) if x > 0 else np.nan)
    df = df.sort_values('neg_log10_p', ascending=True).reset_index(drop=True)

    def label(row):
        text = textwrap.fill(str(row['name']), args.wrap)
        if multi_source:
            text += '  (%s)' % str(row.get('source', '')).replace('GO:', '')
        return text

    labels = [label(r) for _, r in df.iterrows()]
    n = len(df)
    y = np.arange(n)

    if args.figsize:
        w, h = [float(x) for x in args.figsize.split(',')]
    else:
        longest = max((len(line) for lab in labels for line in lab.split('\n')), default=30)
        w = min(16.0, max(7.5, 0.085 * longest + 5.6))
        h = max(2.6, 0.46 * n + 1.9)

    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif'],
        'axes.unicode_minus': False,
        'svg.fonttype': 'none',
    })

    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor('white')

    sizes = bubble_sizes(df[size_col].to_numpy())
    sig = df['neg_log10_p'].to_numpy()
    sc = ax.scatter(sig, y, s=sizes, c=sig, cmap=SIG_CMAP,
                    edgecolors='white', linewidths=0.9, zorder=3)

    p05 = -np.log10(0.05)
    if np.nanmin(sig) <= p05 <= np.nanmax(sig):
        ax.axvline(p05, color='#c9ccd1', linestyle=(0, (4, 4)),
                   linewidth=0.9, zorder=1)
        ax.annotate('p = 0.05', xy=(p05, n - 0.35), xytext=(3, 0),
                    textcoords='offset points', fontsize=7.5, color=MUTED,
                    va='top', ha='left')

    pad = (np.nanmax(sig) - min(0.0, np.nanmin(sig))) * 0.06 + 0.12
    ax.set_xlim(min(0.0, np.nanmin(sig)) - 0.05, np.nanmax(sig) + pad)
    ax.set_ylim(-0.8, n - 0.2)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.5, color=INK, linespacing=1.25)
    ax.set_xlabel('-log10(p-value)', fontsize=10.5, color=INK, labelpad=7)

    title = args.title or ('Enrichment analysis' + (' - %s' % source if source else ''))
    ax.set_title(title, loc='left', fontsize=13, color=INK, pad=16)

    style_axes(ax)

    cbar = fig.colorbar(sc, ax=ax, pad=0.02, fraction=0.030, aspect=30)
    cbar.set_label('-log10(p)', fontsize=9.5, color=INK)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(colors=MUTED, length=2, labelsize=8.5)

    handles = size_legend_handles(df[size_col].to_numpy())
    leg = ax.legend(handles, [h.get_label() for h in handles],
                    title='Genes in term', frameon=False, loc='lower right',
                    fontsize=8.5, title_fontsize=8.5, labelspacing=1.15,
                    handletextpad=1.5, borderpad=1.0, borderaxespad=1.0)
    leg._legend_box.align = 'left'
    for txt in leg.get_texts():
        txt.set_color(MUTED)
    leg.get_title().set_color(MUTED)

    fig.tight_layout()
    fig.savefig(args.output, dpi=args.dpi, bbox_inches='tight', facecolor='white')
    if args.svg:
        svg_path = os.path.splitext(args.output)[0] + '.svg'
        fig.savefig(svg_path, bbox_inches='tight', facecolor='white')
        print("Vector version written to %s" % svg_path)
    plt.close(fig)

    print("Dot plot written to %s (%d terms, %s x %s in)"
          % (args.output, n, round(w, 1), round(h, 1)))
    print("Done!")


if __name__ == '__main__':
    main()
