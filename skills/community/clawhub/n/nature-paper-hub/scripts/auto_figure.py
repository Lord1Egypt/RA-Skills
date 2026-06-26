#!/usr/bin/env python3
"""
auto_figure.py — Nature-style publication figure generator.

Usage:
    python3 auto_figure.py --input data.csv --output figure.pdf [options]
"""

import argparse
import math
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

# ── Dependencies ──────────────────────────────────────────────────────────────
try:
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import seaborn as sns
except ImportError as e:
    sys.exit(f"❌ Missing dependency: {e}\n"
             "Run: pip3 install pandas matplotlib seaborn openpyxl -q --break-system-packages")

# ── Palettes ──────────────────────────────────────────────────────────────────
PALETTES = {
    'nature':     ['#4878CF','#D65F5F','#6ACC65','#EE854A','#956CB4','#82C6E2','#D5BB67','#8C8C8C'],
    'colorblind': ['#0072B2','#E69F00','#009E73','#CC79A7','#56B4E9','#F0E442','#D55E00','#000000'],
    'grayscale':  ['#000000','#404040','#808080','#AAAAAA','#CCCCCC'],
}

# ── Width presets (mm → inches at 300 DPI) ────────────────────────────────────
MM_TO_IN = 1 / 25.4
WIDTH_MM = {'single': 89, 'onehalf': 120, 'double': 183}

# ── Nature rcParams ───────────────────────────────────────────────────────────
NATURE_RC = {
    'font.family':        'Arial',
    'font.size':          8,
    'axes.linewidth':     0.8,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'xtick.major.width':  0.8,
    'ytick.major.width':  0.8,
    'xtick.major.size':   3,
    'ytick.major.size':   3,
    'xtick.direction':    'out',
    'ytick.direction':    'out',
    'figure.dpi':         300,
    'savefig.dpi':        300,
    'savefig.bbox':       'tight',
    'savefig.pad_inches': 0.05,
    'pdf.fonttype':       42,
    'ps.fonttype':        42,
}


# ── Font check ────────────────────────────────────────────────────────────────
def _setup_font(lang: str) -> None:
    """Apply Nature rcParams; fall back to DejaVu Sans if Arial missing."""
    available = {f.name for f in fm.fontManager.ttflist}
    if lang == 'zh':
        # prefer CJK fonts for Chinese labels
        cjk_prefs = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC',
                     'STHeiti', 'Microsoft YaHei', 'SimHei']
        chosen = next((f for f in cjk_prefs if f in available), None)
        if chosen:
            NATURE_RC['font.family'] = chosen
        else:
            warnings.warn("⚠️  No CJK font found — Chinese labels may not render correctly.")
    else:
        if 'Arial' not in available:
            warnings.warn("⚠️  Arial not found — falling back to DejaVu Sans.")
            NATURE_RC['font.family'] = 'DejaVu Sans'
    plt.rcParams.update(NATURE_RC)


# ── Data loading ──────────────────────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == '.csv':
        df = pd.read_csv(p)
    elif suffix in ('.xls', '.xlsx'):
        df = pd.read_excel(p)
    elif suffix == '.json':
        df = pd.read_json(p)
    else:
        sys.exit(f"❌ Unsupported file type: {suffix}  (use .csv, .xlsx, or .json)")
    # NaN handling
    n_nan = df.isna().sum().sum()
    if n_nan:
        warnings.warn(f"⚠️  Dropped {n_nan} NaN value(s) from data.")
        df = df.dropna()
    return df


# ── Column classification ─────────────────────────────────────────────────────
def classify_columns(df: pd.DataFrame):
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
    # also try parsing object cols as datetime
    for col in df.select_dtypes(include='object').columns:
        try:
            pd.to_datetime(df[col])
            datetime_cols.append(col)
        except Exception:
            pass
    categorical_cols = [c for c in df.columns
                        if c not in numeric_cols and c not in datetime_cols]
    return numeric_cols, categorical_cols, datetime_cols


# ── Auto-detect chart type ────────────────────────────────────────────────────
def auto_detect_type(df: pd.DataFrame, numeric_cols, categorical_cols, datetime_cols) -> str:
    n_num = len(numeric_cols)
    n_cat = len(categorical_cols)
    n_dt  = len(datetime_cols)

    if n_dt >= 1 and n_num >= 1:
        return 'line'
    if n_cat == 1 and n_num == 1:
        return 'bar'
    if n_num >= 2:
        # heuristic: square-ish all-numeric frame → heatmap
        if n_cat == 0 and n_dt == 0 and abs(len(df) - n_num) <= max(2, n_num * 0.3):
            return 'heatmap'
        return 'scatter'
    if n_cat >= 1 and n_num >= 2:
        return 'box'
    return 'bar'  # fallback


# ── Panel layout helper ────────────────────────────────────────────────────────
def panel_layout(n: int):
    if n <= 3:
        return 1, n
    if n == 4:
        return 2, 2
    return math.ceil(n / 3), 3


# ── Figure width/height ───────────────────────────────────────────────────────
def figure_size(width_key: str, n_rows: int, n_cols: int):
    w_mm = WIDTH_MM.get(width_key, 183)
    w_in = w_mm * MM_TO_IN
    h_in = w_in * (n_rows / n_cols) * 0.75
    h_in = max(h_in, 1.5)  # minimum height
    return w_in, h_in, w_mm


# ── Panel label helper ────────────────────────────────────────────────────────
def add_panel_label(ax, index: int):
    label = chr(ord('a') + index)
    ax.text(-0.15, 1.05, label, transform=ax.transAxes,
            fontsize=8, fontweight='bold', va='top', ha='right')


# ── Guard group column ────────────────────────────────────────────────────────
def guard_group_col(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    if group_col and group_col in df.columns:
        cats = df[group_col].nunique()
        if cats > 10:
            warnings.warn(f"⚠️  Group column '{group_col}' has {cats} categories — "
                          "using only top 10.")
            top10 = df[group_col].value_counts().nlargest(10).index
            df = df[df[group_col].isin(top10)].copy()
    return df


# ── Plot functions ────────────────────────────────────────────────────────────

def _set_labels(ax, xlabel, ylabel):
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)


def plot_line(ax, df, x_col, y_col, group_col, palette, xlabel, ylabel, title):
    colors = palette
    if group_col and group_col in df.columns:
        for i, (grp, sub) in enumerate(df.groupby(group_col)):
            ax.plot(sub[x_col], sub[y_col], label=str(grp),
                    color=colors[i % len(colors)], linewidth=1)
        ax.legend(title=title or group_col, frameon=False, fontsize=7)
    else:
        ax.plot(df[x_col], df[y_col], color=colors[0], linewidth=1,
                label=title or y_col)
        if title:
            ax.legend(frameon=False, fontsize=7)
    _set_labels(ax, xlabel or x_col, ylabel or y_col)


def plot_bar(ax, df, x_col, y_col, group_col, palette, xlabel, ylabel, title):
    colors = palette
    if group_col and group_col in df.columns:
        pivot = df.groupby([x_col, group_col])[y_col].mean().unstack(group_col)
        pivot.plot(kind='bar', ax=ax, color=colors[:len(pivot.columns)],
                   edgecolor='none', width=0.7)
        ax.legend(title=title or group_col, frameon=False, fontsize=7,
                  bbox_to_anchor=(1, 1), loc='upper left')
    else:
        grp = df.groupby(x_col)[y_col].mean()
        ax.bar(range(len(grp)), grp.values,
               color=colors[:len(grp)], edgecolor='none', width=0.7)
        ax.set_xticks(range(len(grp)))
        ax.set_xticklabels(grp.index, rotation=45, ha='right')
    _set_labels(ax, xlabel or x_col, ylabel or y_col)


def plot_scatter(ax, df, x_col, y_col, group_col, palette, xlabel, ylabel, title):
    colors = palette
    if group_col and group_col in df.columns:
        for i, (grp, sub) in enumerate(df.groupby(group_col)):
            ax.scatter(sub[x_col], sub[y_col], label=str(grp),
                       color=colors[i % len(colors)], s=12, alpha=0.8, linewidths=0)
        ax.legend(title=title or group_col, frameon=False, fontsize=7)
    else:
        ax.scatter(df[x_col], df[y_col], color=colors[0], s=12, alpha=0.8, linewidths=0)
    _set_labels(ax, xlabel or x_col, ylabel or y_col)


def plot_heatmap(ax, df, palette, xlabel, ylabel, title):
    import numpy as np
    numeric_df = df.select_dtypes(include='number')
    sns.heatmap(numeric_df, ax=ax, cmap='viridis', linewidths=0,
                cbar_kws={'shrink': 0.8, 'pad': 0.02})
    _set_labels(ax, xlabel or '', ylabel or '')
    if title:
        ax.set_title(title, fontsize=8)


def plot_box(ax, df, x_col, y_col, group_col, palette, xlabel, ylabel, title, kind='box'):
    colors = palette
    kwargs = dict(
        data=df, x=x_col, y=y_col,
        hue=group_col if group_col and group_col in df.columns else None,
        ax=ax, palette=colors[:df[x_col].nunique()] if x_col else None,
    )
    if kind == 'violin':
        sns.violinplot(**kwargs, linewidth=0.8, inner='box', cut=0)
    else:
        sns.boxplot(**kwargs, linewidth=0.8, flierprops=dict(marker='o', markersize=2))
    _set_labels(ax, xlabel or x_col, ylabel or y_col)
    if group_col and group_col in df.columns:
        ax.legend(title=title or group_col, frameon=False, fontsize=7)
    elif title:
        ax.set_title(title, fontsize=8)


# ── Multi-panel rendering ─────────────────────────────────────────────────────

def render_panels(df, panel_cols, x_col, group_col, chart_type,
                  palette, xlabel, ylabel, title, width_key, lang):
    n = len(panel_cols)
    n_rows, n_cols = panel_layout(n)
    w_in, h_in, w_mm = figure_size(width_key, n_rows, n_cols)
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(w_in, h_in),
                             squeeze=False)
    axes_flat = [axes[r][c] for r in range(n_rows) for c in range(n_cols)]

    for i, ycol in enumerate(panel_cols):
        ax = axes_flat[i]
        _draw_single(ax, df, x_col, ycol, group_col, chart_type,
                     palette, xlabel, ylabel or ycol, title)
        add_panel_label(ax, i)

    # hide unused axes
    for j in range(n, len(axes_flat)):
        axes_flat[j].set_visible(False)

    fig.tight_layout()
    return fig, n_rows, n_cols, w_mm, h_in


def _draw_single(ax, df, x_col, y_col, group_col, chart_type,
                 palette, xlabel, ylabel, title):
    if chart_type == 'line':
        plot_line(ax, df, x_col, y_col, group_col, palette, xlabel, ylabel, title)
    elif chart_type == 'bar':
        plot_bar(ax, df, x_col, y_col, group_col, palette, xlabel, ylabel, title)
    elif chart_type == 'scatter':
        plot_scatter(ax, df, x_col, y_col, group_col, palette, xlabel, ylabel, title)
    elif chart_type == 'heatmap':
        plot_heatmap(ax, df, palette, xlabel, ylabel, title)
    elif chart_type == 'box':
        plot_box(ax, df, x_col, y_col, group_col, palette, xlabel, ylabel, title, kind='box')
    elif chart_type == 'violin':
        plot_box(ax, df, x_col, y_col, group_col, palette, xlabel, ylabel, title, kind='violin')
    else:
        plot_bar(ax, df, x_col, y_col, group_col, palette, xlabel, ylabel, title)


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_args(argv=None):
    p = argparse.ArgumentParser(description='Generate Nature-style publication figures.')
    p.add_argument('--input',     required=True,  help='Input data file (.csv, .xlsx, .json)')
    p.add_argument('--output',    default=None,   help='Output PDF path (default: ~/Downloads/auto_figure_YYYYMMDD.pdf)')
    p.add_argument('--type',      default='auto',
                   choices=['auto','line','bar','scatter','heatmap','box','violin'],
                   help='Chart type (default: auto)')
    p.add_argument('--title',     default='',     help='Figure title (appears in legend)')
    p.add_argument('--xlabel',    default='',     help='X-axis label')
    p.add_argument('--ylabel',    default='',     help='Y-axis label')
    p.add_argument('--group-col', default=None,   dest='group_col', help='Grouping/hue column')
    p.add_argument('--x-col',     default=None,   dest='x_col',     help='X column name')
    p.add_argument('--y-col',     default=None,   dest='y_col',     help='Y column name')
    p.add_argument('--width',     default='double',
                   choices=['single','onehalf','double'],
                   help='Column width preset (default: double)')
    p.add_argument('--panels',    default=None,
                   help='Comma-separated y-columns for multi-panel layout')
    p.add_argument('--palette',   default='nature',
                   choices=['nature','colorblind','grayscale'],
                   help='Color palette (default: nature)')
    p.add_argument('--lang',      default='en', choices=['en','zh'],
                   help='Language for font handling (default: en)')
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    # Font setup
    _setup_font(args.lang)

    # Output path
    if args.output is None:
        date_str = datetime.now().strftime('%Y%m%d')
        args.output = str(Path.home() / 'Downloads' / f'auto_figure_{date_str}.pdf')

    out_path = Path(args.output)
    out_pdf  = out_path.with_suffix('.pdf')
    out_png  = out_path.with_suffix('.png')
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    palette  = PALETTES[args.palette]

    # Load data
    df = load_data(args.input)

    # Guard group column
    if args.group_col:
        df = guard_group_col(df, args.group_col)

    # Classify columns
    numeric_cols, categorical_cols, datetime_cols = classify_columns(df)

    # Detect chart type
    chart_type = args.type
    detected   = False
    if chart_type == 'auto':
        chart_type = auto_detect_type(df, numeric_cols, categorical_cols, datetime_cols)
        detected   = True

    # Resolve x/y columns
    x_col = args.x_col
    y_col = args.y_col

    if x_col is None:
        if datetime_cols:
            x_col = datetime_cols[0]
        elif categorical_cols:
            x_col = categorical_cols[0]
        elif numeric_cols:
            x_col = numeric_cols[0]

    if y_col is None:
        candidates = [c for c in numeric_cols if c != x_col]
        y_col = candidates[0] if candidates else (numeric_cols[0] if numeric_cols else df.columns[-1])

    # ── Multi-panel mode ──────────────────────────────────────────────────────
    panel_cols = None
    if args.panels:
        panel_cols = [c.strip() for c in args.panels.split(',') if c.strip() in df.columns]
        missing = [c.strip() for c in args.panels.split(',') if c.strip() not in df.columns]
        if missing:
            warnings.warn(f"⚠️  Panel columns not found in data: {missing}")

    if panel_cols and len(panel_cols) > 1:
        fig, n_rows, n_cols_layout, w_mm, h_in = render_panels(
            df, panel_cols, x_col, args.group_col, chart_type,
            palette, args.xlabel, args.ylabel, args.title, args.width, args.lang
        )
        n_panels = len(panel_cols)
        panel_labels = ', '.join(chr(ord('a') + i) for i in range(n_panels))
        h_mm = round(h_in / MM_TO_IN)
    else:
        # Single panel
        n_panels = 1
        panel_labels = 'a'
        n_rows, n_cols_layout = 1, 1
        w_mm = WIDTH_MM.get(args.width, 183)
        w_in, h_in, _ = figure_size(args.width, 1, 1)
        h_mm = round(h_in / MM_TO_IN)

        fig, ax = plt.subplots(1, 1, figsize=(w_in, h_in))

        if chart_type == 'heatmap':
            plot_heatmap(ax, df, palette, args.xlabel, args.ylabel, args.title)
        else:
            _draw_single(ax, df, x_col, y_col, args.group_col, chart_type,
                         palette, args.xlabel, args.ylabel, args.title)

        fig.tight_layout()

    # Save
    fig.savefig(out_pdf)
    fig.savefig(out_png)
    plt.close(fig)

    # Summary
    type_str = f"{chart_type} (auto-detected)" if detected else chart_type
    print("✅ Figure generated:")
    print(f"   Type:   {type_str}")
    print(f"   Panels: {n_panels} ({panel_labels})" if n_panels > 1 else f"   Panels: 1 (a)")
    print(f"   Size:   {w_mm}mm × {h_mm}mm ({args.width} column)")
    print(f"   Files:  {out_pdf}, {out_png}")

    return str(out_pdf)


# ── Self-test ─────────────────────────────────────────────────────────────────

def _self_test():
    import tempfile, csv, os

    # Write a small inline CSV
    rows = [
        ['group', 'value', 'score'],
        ['A',      10,      0.5],
        ['B',      20,      0.8],
        ['C',      15,      0.6],
        ['A',      12,      0.55],
        ['B',      18,      0.75],
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv.writer(f).writerows(rows)
        tmp_csv = f.name

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        tmp_pdf = f.name

    try:
        argv = ['--input', tmp_csv, '--output', tmp_pdf]
        result = main(argv)
        assert result and Path(result).exists(), "PDF not created"
        png = Path(result).with_suffix('.png')
        assert png.exists(), "PNG not created"
        print("✅ auto_figure test passed")
    finally:
        for p in [tmp_csv, tmp_pdf,
                  str(Path(tmp_pdf).with_suffix('.pdf')),
                  str(Path(tmp_pdf).with_suffix('.png'))]:
            try:
                os.unlink(p)
            except FileNotFoundError:
                pass


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        _self_test()
    else:
        main()
