---
name: gpx-kml-visualizer
description: This skill should be used when the user wants to visualize GPS track routes from KML or GPX files. Trigger when the user mentions drawing, plotting, converting, or generating route maps, track visualizations, elevation profiles, or GIS maps from .kml, .gpx, or similar GPS track files. Also trigger for requests involving trail maps, running/cycling/hiking route charts, or generating JPG/HTML route planning diagrams from recorded GPS tracks.
---

# GPX / KML Route Visualizer

## Overview

Convert GPS track files (KML/GPX) into professional route visualization outputs:
- **Static JPG**: High-resolution image with route map + elevation profile + statistics panel
- **Interactive HTML**: Browser-based Leaflet map with zoom, layer switching, and embedded elevation chart

## Workflow

### Step 1: Parse Track File

Run the parsing script to extract coordinates and compute statistics:

```bash
python scripts/parse_track.py <input.kml|input.gpx> -o track_data.json
```

This produces a JSON file containing:
- Parsed track points (`lat`, `lon`, `ele`, cumulative `dist`)
- Route statistics (total distance, elevation gain/loss, max/min/average elevation)

### Step 2: Generate Visualization

Choose output format based on user request:

#### Option A: Static JPG Image

Generate a printable/static route map image:

```bash
python scripts/plot_static.py track_data.json -o route_map.jpg --dpi 150
```

Output layout:
- Top panel: Route trajectory with elevation-based color gradient, start/end markers, elevation colorbar
- Bottom panel: Distance vs. elevation profile with gain/loss annotations
- Footer: Key statistics text strip

#### Option B: Interactive HTML Map

Generate a browser-based interactive map:

```bash
python scripts/plot_interactive.py track_data.json -o route_map.html
```

Features:
- Leaflet map centered on route with OSM, Satellite, and Terrain tile layers
- Route colored by elevation (viridis gradient)
- Clickable start/end markers with coordinates and elevation
- Auto-fit bounds to show entire route
- Embedded elevation profile image below the map
- Statistics header panel

## Combined One-Liner Workflow

For quick generation, chain the scripts:

```bash
# Static JPG
python scripts/parse_track.py input.gpx -o track_data.json && python scripts/plot_static.py track_data.json -o route_map.jpg

# Interactive HTML
python scripts/parse_track.py input.gpx -o track_data.json && python scripts/plot_interactive.py track_data.json -o route_map.html
```

## Dependencies

Required Python packages:

```bash
pip install matplotlib numpy folium Pillow
```

- `matplotlib`: Static plotting and image generation
- `numpy`: Numerical operations for statistics
- `folium`: Interactive Leaflet HTML map generation
- `Pillow`: Image handling (usually installed with matplotlib)

All scripts use only the Python standard library plus the above packages.

## Script Reference

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `scripts/parse_track.py` | Parse KML/GPX, compute stats | `.kml` or `.gpx` | `track_data.json` |
| `scripts/plot_static.py` | Generate static JPG | `track_data.json` | `.jpg` image |
| `scripts/plot_interactive.py` | Generate interactive HTML | `track_data.json` | `.html` page |

## File Format Support

- **KML**: Parses `<coordinates>` elements inside `<LineString>` (handles both KML 2.1 and 2.2 namespaces)
- **GPX**: Parses `<trkpt>` elements with `lat`/`lon` attributes and `<ele>` child elements (GPX 1.1)

For detailed format specifications, see `references/formats.md`.

## Notes

- Static JPG DPI can be increased (`--dpi 300`) for print-quality output
- Interactive HTML is fully self-contained (no external dependencies after generation) except for map tile CDN requests
- The parser handles both namespaced and non-namespaced XML automatically
- Large track files (>100k points) may take several seconds to process
