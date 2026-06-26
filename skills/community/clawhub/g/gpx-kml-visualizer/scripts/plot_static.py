#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a static JPG route visualization from parsed track JSON.
Produces a composite image with route map + elevation profile + statistics.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend

# Configure CJK font support (Windows common fonts)
import matplotlib.font_manager as fm
_cjk_fonts = ["Microsoft YaHei", "SimHei", "SimSun", "WenQuanYi Micro Hei", "Noto Sans CJK SC"]
_cjk_font = None
for fn in _cjk_fonts:
    try:
        fp = fm.findfont(fm.FontProperties(family=fn), fallback_to_default=False)
        if fp and "DejaVu" not in fp:
            _cjk_font = fn
            break
    except Exception:
        continue
if _cjk_font:
    matplotlib.rcParams["font.family"] = [_cjk_font, "sans-serif"]
    matplotlib.rcParams["axes.unicode_minus"] = False

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np


def load_track_data(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_distance(km: float) -> str:
    if km < 1:
        return f"{km * 1000:.0f} m"
    return f"{km:.2f} km"


def plot_route_map(ax, points: List[Dict[str, Any]], title: str = ""):
    """Plot route trajectory on given axes."""
    lats = [p["lat"] for p in points]
    lons = [p["lon"] for p in points]

    # Plot route with gradient color based on elevation
    eles = [p["ele"] for p in points]
    min_ele, max_ele = min(eles), max(eles)
    norm = plt.Normalize(min_ele, max_ele)
    cmap = plt.get_cmap("viridis")

    # Draw line segments with color gradient
    for i in range(len(points) - 1):
        avg_ele = (eles[i] + eles[i + 1]) / 2
        color = cmap(norm(avg_ele))
        ax.plot([lons[i], lons[i + 1]], [lats[i], lats[i + 1]],
                color=color, linewidth=2.5, solid_capstyle="round")

    # Start and end markers
    ax.scatter(lons[0], lats[0], c="green", s=120, zorder=5, edgecolors="white", linewidths=1.5, marker="o", label="Start")
    ax.scatter(lons[-1], lats[-1], c="red", s=120, zorder=5, edgecolors="white", linewidths=1.5, marker="X", label="End")

    # Equal aspect ratio (approximate for lat/lon)
    lat_mid = (max(lats) + min(lats)) / 2
    aspect = 1 / math.cos(math.radians(lat_mid)) if lat_mid != 0 else 1
    ax.set_aspect(aspect)

    ax.set_xlabel("Longitude", fontsize=10)
    ax.set_ylabel("Latitude", fontsize=10)
    ax.set_title(title or "Route Map", fontsize=12, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)

    # Add colorbar for elevation
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Elevation (m)", fontsize=9)


def plot_elevation_profile(ax, points: List[Dict[str, Any]], stats: Dict[str, Any]):
    """Plot elevation profile on given axes."""
    dists = [p.get("dist", 0) / 1000 for p in points]  # km
    eles = [p["ele"] for p in points]

    # Fill area under curve
    ax.fill_between(dists, eles, alpha=0.3, color="#3498db")
    ax.plot(dists, eles, color="#2980b9", linewidth=1.5)

    # Mark max and min elevation
    max_idx = int(np.argmax(eles))
    min_idx = int(np.argmin(eles))
    ax.scatter(dists[max_idx], eles[max_idx], c="red", s=60, zorder=5, marker="^", edgecolors="white", linewidths=1)
    ax.scatter(dists[min_idx], eles[min_idx], c="blue", s=60, zorder=5, marker="v", edgecolors="white", linewidths=1)

    ax.set_xlabel("Distance (km)", fontsize=10)
    ax.set_ylabel("Elevation (m)", fontsize=10)
    ax.set_title("Elevation Profile", fontsize=12, fontweight="bold")
    ax.grid(True, alpha=0.3)

    # Add annotation boxes for key stats on the plot
    textstr = (f"Max: {stats['max_elevation_m']:.0f}m\n"
               f"Min: {stats['min_elevation_m']:.0f}m\n"
               f"Gain: +{stats['elevation_gain_m']:.0f}m\n"
               f"Loss: -{stats['elevation_loss_m']:.0f}m")
    props = dict(boxstyle="round,pad=0.5", facecolor="wheat", alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment="top", bbox=props)


def add_stats_panel(fig, stats: Dict[str, Any], source_name: str):
    """Add a statistics text panel at the bottom of the figure."""
    stats_text = (
        f"File: {source_name}  |  "
        f"Distance: {format_distance(stats['total_distance_km'])}  |  "
        f"Points: {stats['point_count']}  |  "
        f"Elevation Gain: {stats['elevation_gain_m']:.0f} m  |  "
        f"Elevation Loss: {stats['elevation_loss_m']:.0f} m  |  "
        f"Max Elevation: {stats['max_elevation_m']:.0f} m  |  "
        f"Min Elevation: {stats['min_elevation_m']:.0f} m  |  "
        f"Avg Elevation: {stats['avg_elevation_m']:.0f} m"
    )
    fig.text(0.5, 0.01, stats_text, ha="center", fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#f0f0f0", alpha=0.9))


def generate_static_image(data: Dict[str, Any], output_path: str, dpi: int = 150):
    """Generate the complete static visualization image."""
    points = data["points"]
    stats = data["statistics"]
    source = Path(data["source_file"]).name

    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 1, height_ratios=[3, 2], hspace=0.25, bottom=0.08, top=0.93)

    # Top: Route map
    ax_map = fig.add_subplot(gs[0])
    plot_route_map(ax_map, points, title=f"Route: {source}")

    # Bottom: Elevation profile
    ax_elev = fig.add_subplot(gs[1])
    plot_elevation_profile(ax_elev, points, stats)

    # Bottom stats panel
    add_stats_panel(fig, stats, source)

    plt.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Static image saved to: {output_path} ({dpi} DPI)")


def main():
    parser = argparse.ArgumentParser(description="Generate static JPG route visualization")
    parser.add_argument("input", help="Input JSON file from parse_track.py")
    parser.add_argument("-o", "--output", default="route_map.jpg", help="Output JPG file path")
    parser.add_argument("--dpi", type=int, default=150, help="Output image DPI (default: 150)")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    data = load_track_data(args.input)
    generate_static_image(data, args.output, dpi=args.dpi)


if __name__ == "__main__":
    import math
    main()
