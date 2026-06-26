#!/usr/bin/env python3
"""Google-quality health visualization theme and helpers for PHA.

This module provides:
1. A Material Design 3 theme (apply_google_theme)
2. Helper functions for common chart patterns
3. The agent generates custom charts dynamically via fitbit_analyze.py

Design principles (Google Fit / Material Design 3):
- Clean, minimal, generous whitespace
- Material Design 3 color palette with semantic meaning
- Smooth gradients, rounded corners, subtle shadows
- Big stat numbers (hero metrics) — the first thing you see
- Smart annotations that tell a story
- Mobile-optimized 16:9 aspect ratio
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
from pathlib import Path

CHARTS_DIR = Path(__file__).parent.parent / "data" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Material Design 3 Color System ──────────────────────────────────────

COLORS = {
    # Primary
    "blue": "#1A73E8",
    "blue_dark": "#1557B0",
    "blue_light": "#4FC3F7",
    "blue_50": "#E8F0FE",
    "blue_100": "#D2E3FC",
    "blue_200": "#AECBFA",

    # Secondary
    "green": "#34A853",
    "green_dark": "#1E8E3E",
    "green_light": "#81C995",
    "green_50": "#E6F4EA",

    # Tertiary
    "yellow": "#FBBC04",
    "yellow_dark": "#F29900",
    "yellow_50": "#FEF7E0",

    # Error
    "red": "#EA4335",
    "red_dark": "#C5221F",
    "red_light": "#EE675C",
    "red_50": "#FCE8E6",

    # Extended
    "purple": "#A142F4",
    "purple_light": "#C58AF9",
    "purple_50": "#F3E8FD",
    "teal": "#12B5CB",
    "teal_50": "#E4F7FB",
    "orange": "#FA903E",
    "orange_50": "#FEF0E1",
    "indigo": "#3F51B5",
    "pink": "#E91E63",

    # Surfaces
    "white": "#FFFFFF",
    "bg": "#FAFAFA",
    "card": "#FFFFFF",
    "text": "#202124",
    "text_secondary": "#5F6368",
    "text_hint": "#80868B",
    "divider": "#DADCE0",
    "divider_light": "#F1F3F4",

    # Sleep stage palette
    "sleep_deep": "#1A237E",
    "sleep_rem": "#5C6BC0",
    "sleep_light": "#90CAF9",
    "sleep_awake": "#FFD54F",
}

# Semantic color sequences for different health metrics
METRIC_COLORS = {
    "steps": {"primary": COLORS["blue"], "fill": COLORS["blue_50"], "accent": COLORS["green"]},
    "heart_rate": {"primary": COLORS["red"], "fill": COLORS["red_50"], "accent": COLORS["red_light"]},
    "sleep": {"primary": COLORS["indigo"], "fill": COLORS["purple_50"], "accent": COLORS["purple"]},
    "calories": {"primary": COLORS["orange"], "fill": COLORS["orange_50"], "accent": COLORS["yellow"]},
    "hrv": {"primary": COLORS["teal"], "fill": COLORS["teal_50"], "accent": COLORS["green"]},
    "spo2": {"primary": COLORS["purple"], "fill": COLORS["purple_50"], "accent": COLORS["blue"]},
    "activity": {"primary": COLORS["green"], "fill": COLORS["green_50"], "accent": COLORS["blue"]},
}

MULTI_SERIES = [
    COLORS["blue"], COLORS["green"], COLORS["orange"],
    COLORS["red"], COLORS["purple"], COLORS["teal"], COLORS["pink"],
]


def apply_google_theme():
    """Apply Google Material Design 3 matplotlib theme."""
    plt.rcParams.update({
        "figure.facecolor": COLORS["bg"],
        "figure.edgecolor": "none",
        "figure.figsize": (12, 6.75),
        "figure.dpi": 150,
        "figure.titlesize": 22,
        "figure.titleweight": "bold",

        "axes.facecolor": COLORS["white"],
        "axes.edgecolor": COLORS["divider"],
        "axes.linewidth": 0.5,
        "axes.titlesize": 17,
        "axes.titleweight": "medium",
        "axes.titlepad": 18,
        "axes.labelsize": 11,
        "axes.labelcolor": COLORS["text_secondary"],
        "axes.labelpad": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.prop_cycle": plt.cycler("color", MULTI_SERIES),

        "grid.color": COLORS["divider_light"],
        "grid.linewidth": 0.6,
        "grid.alpha": 0.8,

        "xtick.color": COLORS["text_hint"],
        "ytick.color": COLORS["text_hint"],
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "xtick.major.pad": 10,
        "ytick.major.pad": 8,

        "lines.linewidth": 2.5,
        "lines.antialiased": True,
        "lines.markersize": 6,

        "legend.frameon": False,
        "legend.fontsize": 10,
        "legend.labelcolor": COLORS["text_secondary"],

        "font.family": ["Helvetica Neue", "Arial", "sans-serif"],
        "font.size": 11,
        "text.color": COLORS["text"],

        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.4,
        "savefig.facecolor": COLORS["bg"],
        "savefig.dpi": 150,
    })


# ── Helper Functions ─────────────────────────────────────────────────────

def hero_stat(ax, value, label, color=COLORS["blue"], x=0.02, y=0.93):
    """Add a large hero stat number (Google Fit style)."""
    ax.text(x, y, str(value), transform=ax.transAxes,
            fontsize=36, fontweight="bold", color=color,
            va="top", ha="left", zorder=10)
    ax.text(x, y - 0.14, label, transform=ax.transAxes,
            fontsize=11, color=COLORS["text_secondary"],
            va="top", ha="left", zorder=10)


def gradient_fill(ax, x, y, color=COLORS["blue"], alpha=0.12):
    """Smooth gradient fill under a line."""
    ax.fill_between(x, 0, y, alpha=alpha, color=color, linewidth=0, zorder=1)


def reference_band(ax, ymin, ymax, label=None, color=COLORS["green"], alpha=0.06):
    """Add a horizontal reference band (e.g., normal range)."""
    ax.axhspan(ymin, ymax, alpha=alpha, color=color, zorder=0)
    ax.axhline(ymin, color=color, linewidth=0.6, linestyle=":", alpha=0.3)
    ax.axhline(ymax, color=color, linewidth=0.6, linestyle=":", alpha=0.3)
    if label:
        ax.text(0.98, (ymin + ymax) / 2, label, transform=ax.get_yaxis_transform(),
                fontsize=8, color=COLORS["text_hint"], ha="right", va="center", alpha=0.7)


def goal_line(ax, y, label=None, color=COLORS["yellow_dark"], style=":"):
    """Add a goal/target horizontal line."""
    ax.axhline(y=y, color=color, linewidth=1.5, linestyle=style, alpha=0.6, zorder=2)
    if label:
        ax.text(1.01, y, label, transform=ax.get_yaxis_transform(),
                fontsize=9, color=color, va="center", ha="left")


def trend_arrow(ax, start_val, end_val, x=0.98, y=0.93, size=14):
    """Add a trend indicator arrow with percentage change."""
    if start_val == 0:
        return
    pct = (end_val - start_val) / start_val * 100
    if abs(pct) < 1:
        arrow, color = "→", COLORS["text_hint"]
    elif pct > 0:
        arrow, color = "↑", COLORS["green"]
    else:
        arrow, color = "↓", COLORS["red"]
    ax.text(x, y, f"{arrow} {abs(pct):.0f}%", transform=ax.transAxes,
            fontsize=size, fontweight="bold", color=color, ha="right", va="top")


def smart_date_axis(ax, days):
    """Apply smart date formatting based on range."""
    if days <= 7:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%b %d"))
        ax.xaxis.set_major_locator(mdates.DayLocator())
    elif days <= 31:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    elif days <= 90:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), ha="center")


def bar_with_highlights(ax, dates, values, threshold=None, color=COLORS["blue"],
                        highlight_color=COLORS["green"], alpha=0.85):
    """Bar chart where bars above threshold get highlighted."""
    if threshold:
        colors = [highlight_color if v >= threshold else color for v in values]
    else:
        colors = color
    ax.bar(dates, values, width=0.7, color=colors, alpha=alpha, edgecolor="none", zorder=3)


def smooth_line(ax, dates, values, color=COLORS["blue"], fill=True, markers=True):
    """Smooth line with optional fill and markers."""
    marker = "o" if markers and len(dates) <= 31 else None
    ms = 4 if len(dates) <= 14 else 3
    ax.plot(dates, values, color=color, linewidth=2.5, marker=marker,
            markersize=ms, markerfacecolor="white", markeredgecolor=color,
            markeredgewidth=1.5, zorder=4)
    if fill:
        gradient_fill(ax, dates, values, color=color)


def rolling_avg_line(ax, dates, values, window=7, color=COLORS["red"], label="7-day avg"):
    """Add a rolling average overlay."""
    import pandas as pd
    rolling = pd.Series(values).rolling(window, min_periods=1).mean()
    ax.plot(dates, rolling, color=color, linewidth=2, linestyle="--",
            alpha=0.7, label=label, zorder=5)


def card_background(ax):
    """Add a subtle card-like background to an axes."""
    ax.set_facecolor(COLORS["white"])
    for spine in ax.spines.values():
        spine.set_edgecolor(COLORS["divider"])
        spine.set_linewidth(0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(fig, name, close=True):
    """Save chart to the charts directory."""
    path = str(CHARTS_DIR / f"{name}.png")
    fig.savefig(path)
    if close:
        plt.close(fig)
    print(f"Chart saved: {path}")
    return path


def number_format(x, pos=None):
    """Format numbers with commas."""
    return f"{x:,.0f}"


# Expose as ticker formatter
NUMBER_FMT = ticker.FuncFormatter(number_format)
