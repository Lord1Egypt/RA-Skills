#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate an interactive HTML route map from parsed track JSON.
Includes Leaflet map with colored route, markers, and embedded elevation profile.
"""

import sys
import json
import base64
import argparse
import math
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import matplotlib
matplotlib.use("Agg")

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
from io import BytesIO

try:
    import folium
    from folium.plugins import HeatMap
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False


def load_track_data(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_elevation_profile_base64(points: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
    """Generate elevation profile image and return as base64 PNG."""
    dists = [p.get("dist", 0) / 1000 for p in points]
    eles = [p["ele"] for p in points]

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.fill_between(dists, eles, alpha=0.3, color="#3498db")
    ax.plot(dists, eles, color="#2980b9", linewidth=1.5)

    max_idx = int(np.argmax(eles))
    min_idx = int(np.argmin(eles))
    ax.scatter(dists[max_idx], eles[max_idx], c="red", s=50, zorder=5, marker="^")
    ax.scatter(dists[min_idx], eles[min_idx], c="blue", s=50, zorder=5, marker="v")

    ax.set_xlabel("Distance (km)", fontsize=9)
    ax.set_ylabel("Elevation (m)", fontsize=9)
    ax.set_title("Elevation Profile", fontsize=11, fontweight="bold")
    ax.grid(True, alpha=0.3)

    textstr = (f"Gain: +{stats['elevation_gain_m']:.0f}m  Loss: -{stats['elevation_loss_m']:.0f}m  "
               f"Max: {stats['max_elevation_m']:.0f}m  Min: {stats['min_elevation_m']:.0f}m")
    props = dict(boxstyle="round,pad=0.4", facecolor="wheat", alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=8,
            verticalalignment="top", bbox=props)

    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=120, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_base64


def generate_interactive_html(data: Dict[str, Any], output_path: str):
    """Generate interactive HTML map with elevation profile."""
    if not FOLIUM_AVAILABLE:
        print("Error: folium is not installed. Run: pip install folium", file=sys.stderr)
        sys.exit(1)

    points = data["points"]
    stats = data["statistics"]
    source = Path(data["source_file"]).name

    lats = [p["lat"] for p in points]
    lons = [p["lon"] for p in points]
    eles = [p["ele"] for p in points]

    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)

    # Create folium map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14,
                   tiles="OpenStreetMap")

    # Add satellite tile layer option
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite",
        overlay=False,
        control=True,
    ).add_to(m)

    # Add terrain tile layer option
    folium.TileLayer(
        tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attr="OpenTopoMap",
        name="Terrain",
        overlay=False,
        control=True,
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # Build colored polyline segments based on elevation
    min_ele, max_ele = min(eles), max(eles)
    if max_ele == min_ele:
        max_ele = min_ele + 1  # avoid div by zero

    cmap = plt.get_cmap("viridis")

    for i in range(len(points) - 1):
        avg_ele = (eles[i] + eles[i + 1]) / 2
        norm_val = (avg_ele - min_ele) / (max_ele - min_ele)
        rgba = cmap(norm_val)
        hex_color = "#%02x%02x%02x" % (int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255))

        folium.PolyLine(
            locations=[[lats[i], lons[i]], [lats[i+1], lons[i+1]]],
            color=hex_color,
            weight=4,
            opacity=0.85,
        ).add_to(m)

    # Start marker
    folium.Marker(
        location=[lats[0], lons[0]],
        popup=folium.Popup(f"<b>Start</b><br>Lat: {lats[0]:.6f}<br>Lon: {lons[0]:.6f}<br>Elev: {eles[0]:.1f}m", max_width=200),
        tooltip="Start",
        icon=folium.Icon(color="green", icon="play", prefix="fa"),
    ).add_to(m)

    # End marker
    folium.Marker(
        location=[lats[-1], lons[-1]],
        popup=folium.Popup(f"<b>End</b><br>Lat: {lats[-1]:.6f}<br>Lon: {lons[-1]:.6f}<br>Elev: {eles[-1]:.1f}m", max_width=200),
        tooltip="End",
        icon=folium.Icon(color="red", icon="flag-checkered", prefix="fa"),
    ).add_to(m)

    # Fit bounds
    m.fit_bounds([[min(lats), min(lons)], [max(lats), max(lons)]], padding=[30, 30])

    # Generate elevation profile base64 image
    elev_base64 = generate_elevation_profile_base64(points, stats)

    # Inject custom HTML/JS for stats panel and elevation profile
    stats_html = f"""
    <div style="font-family: Arial, sans-serif; padding: 10px; background: #f8f9fa; border-bottom: 1px solid #ddd;">
        <h3 style="margin: 0 0 8px 0; color: #333;">🗺️ {source}</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 15px; font-size: 13px; color: #555;">
            <span><b>Distance:</b> {stats['total_distance_km']:.2f} km</span>
            <span><b>Points:</b> {stats['point_count']}</span>
            <span><b>Elev Gain:</b> +{stats['elevation_gain_m']:.0f} m</span>
            <span><b>Elev Loss:</b> -{stats['elevation_loss_m']:.0f} m</span>
            <span><b>Max Elev:</b> {stats['max_elevation_m']:.0f} m</span>
            <span><b>Min Elev:</b> {stats['min_elevation_m']:.0f} m</span>
            <span><b>Avg Elev:</b> {stats['avg_elevation_m']:.0f} m</span>
        </div>
    </div>
    """

    elev_html = f"""
    <div style="padding: 10px; background: white;">
        <img src="data:image/png;base64,{elev_base64}" style="width: 100%; max-width: 100%; height: auto;" />
    </div>
    """

    # Get the raw HTML
    html = m.get_root().render()

    # Insert stats panel after <body>
    body_idx = html.find("<body>")
    if body_idx != -1:
        insert_pos = body_idx + len("<body>")
        html = html[:insert_pos] + stats_html + html[insert_pos:]

    # Insert elevation profile before </body>
    close_body_idx = html.rfind("</body>")
    if close_body_idx != -1:
        html = html[:close_body_idx] + elev_html + html[close_body_idx:]

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Interactive HTML saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate interactive HTML route map")
    parser.add_argument("input", help="Input JSON file from parse_track.py")
    parser.add_argument("-o", "--output", default="route_map.html", help="Output HTML file path")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    data = load_track_data(args.input)
    generate_interactive_html(data, args.output)


if __name__ == "__main__":
    main()
