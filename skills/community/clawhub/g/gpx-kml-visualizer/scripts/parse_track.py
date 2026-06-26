#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse KML/GPX track files and extract coordinate points with statistics.
Outputs JSON data for downstream plotting scripts.
"""

import sys
import json
import math
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two coordinates in meters."""
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def parse_kml(file_path: str) -> List[Dict[str, Any]]:
    """Parse KML file and return list of track points."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Handle namespace
    ns = {"kml": "http://earth.google.com/kml/2.1"}
    if root.tag.startswith("{"):
        ns = {"kml": root.tag.split("}")[0].strip("{")}

    points = []
    ns_uri = ns.get("kml", "")
    # Find all LineString coordinates (with namespace if present)
    tag = "{" + ns_uri + "}coordinates" if ns_uri else "coordinates"
    for coordinates_elem in root.iter(tag):
        if coordinates_elem.text:
            coords_text = coordinates_elem.text.strip()
            for coord in coords_text.split():
                parts = coord.split(",")
                if len(parts) >= 2:
                    lon = float(parts[0])
                    lat = float(parts[1])
                    ele = float(parts[2]) if len(parts) >= 3 else 0.0
                    points.append({"lat": lat, "lon": lon, "ele": ele})

    # Fallback: try without namespace if nothing found
    if not points and ns_uri:
        for elem in root.iter("coordinates"):
            if elem.text:
                coords_text = elem.text.strip()
                for coord in coords_text.split():
                    parts = coord.split(",")
                    if len(parts) >= 2:
                        lon = float(parts[0])
                        lat = float(parts[1])
                        ele = float(parts[2]) if len(parts) >= 3 else 0.0
                        points.append({"lat": lat, "lon": lon, "ele": ele})

    return points


def parse_gpx(file_path: str) -> List[Dict[str, Any]]:
    """Parse GPX file and return list of track points."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Determine namespace
    ns = {}
    if root.tag.startswith("{"):
        ns_uri = root.tag.split("}")[0].strip("{")
        ns = {"gpx": ns_uri}

    points = []
    ns_uri = ns.get("gpx", "")
    # Try with namespace first
    if ns_uri:
        tag = "{" + ns_uri + "}trkpt"
        for trkpt in root.iter(tag):
            lat = float(trkpt.get("lat", 0))
            lon = float(trkpt.get("lon", 0))
            ele_elem = trkpt.find("{" + ns_uri + "}ele")
            if ele_elem is None:
                ele_elem = trkpt.find("ele")
            ele = float(ele_elem.text) if ele_elem is not None and ele_elem.text else 0.0
            points.append({"lat": lat, "lon": lon, "ele": ele})

    # Fallback: iterate without namespace
    if not points:
        for trkpt in root.iter("trkpt"):
            lat = float(trkpt.get("lat", 0))
            lon = float(trkpt.get("lon", 0))
            ele_elem = trkpt.find("ele")
            ele = float(ele_elem.text) if ele_elem is not None and ele_elem.text else 0.0
            points.append({"lat": lat, "lon": lon, "ele": ele})

    return points


def compute_statistics(points: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute track statistics from parsed points."""
    if not points:
        return {}

    total_distance = 0.0
    elevation_gain = 0.0
    elevation_loss = 0.0
    max_ele = points[0]["ele"]
    min_ele = points[0]["ele"]
    total_ele = 0.0

    for i in range(1, len(points)):
        p1 = points[i - 1]
        p2 = points[i]
        dist = haversine(p1["lat"], p1["lon"], p2["lat"], p2["lon"])
        total_distance += dist

        # Elevation change
        d_ele = p2["ele"] - p1["ele"]
        if d_ele > 0:
            elevation_gain += d_ele
        else:
            elevation_loss += abs(d_ele)

        max_ele = max(max_ele, p2["ele"])
        min_ele = min(min_ele, p2["ele"])
        total_ele += p2["ele"]

    avg_ele = total_ele / len(points)

    # Add cumulative distance to each point
    cumulative = 0.0
    points[0]["dist"] = 0.0
    for i in range(1, len(points)):
        p1 = points[i - 1]
        p2 = points[i]
        cumulative += haversine(p1["lat"], p1["lon"], p2["lat"], p2["lon"])
        points[i]["dist"] = cumulative

    return {
        "point_count": len(points),
        "total_distance_m": round(total_distance, 2),
        "total_distance_km": round(total_distance / 1000, 2),
        "elevation_gain_m": round(elevation_gain, 2),
        "elevation_loss_m": round(elevation_loss, 2),
        "max_elevation_m": round(max_ele, 2),
        "min_elevation_m": round(min_ele, 2),
        "avg_elevation_m": round(avg_ele, 2),
    }


def main():
    parser = argparse.ArgumentParser(description="Parse KML/GPX track files")
    parser.add_argument("input", help="Input KML or GPX file path")
    parser.add_argument("-o", "--output", default="track_data.json", help="Output JSON file path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    suffix = input_path.suffix.lower()
    if suffix == ".kml":
        points = parse_kml(str(input_path))
    elif suffix == ".gpx":
        points = parse_gpx(str(input_path))
    else:
        print(f"Error: Unsupported file format: {suffix}", file=sys.stderr)
        sys.exit(1)

    if not points:
        print("Error: No track points found in file.", file=sys.stderr)
        sys.exit(1)

    stats = compute_statistics(points)
    result = {
        "source_file": str(input_path),
        "format": suffix.lstrip("."),
        "statistics": stats,
        "points": points,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Parsed {len(points)} points. Saved to {args.output}")
    print(f"Distance: {stats['total_distance_km']:.2f} km | "
          f"Gain: {stats['elevation_gain_m']:.0f} m | Loss: {stats['elevation_loss_m']:.0f} m")


if __name__ == "__main__":
    main()
