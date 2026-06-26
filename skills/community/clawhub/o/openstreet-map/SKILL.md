---
name: openstreet-map
version: 1.0.0
description: "Use when you need OpenStreetMap geocoding or annotated map generation for a set of places."
---

# OpenStreet Map Skill (for OpenClaw)

This skill provides two capabilities:

1. Query one place's location information.
2. Render an annotated map image for multiple places with numbered markers and a legend.

## Prerequisites

- Python 3.10+
- Internet access (Nominatim + OSM tile endpoints)

Optional environment variable:

- `OPENSTREET_MAP_HOST`: Override only the `openstreetmap.org` host suffix in the default endpoints. Recommended form: `openstreetmap.org`. If `http://` or `https://` is provided, only the host part is used.

When set, the skill uses:

- Geocode endpoint: `https://nominatim.${OPENSTREET_MAP_HOST}/search`
- Tile endpoint: `https://tile.${OPENSTREET_MAP_HOST}/{z}/{x}/{y}.png`

Examples:

- `OPENSTREET_MAP_HOST=openstreetmap.org` -> `https://nominatim.openstreetmap.org/search`
- `OPENSTREET_MAP_HOST=https://openstreetmap.org` -> `https://tile.openstreetmap.org/{z}/{x}/{y}.png`

## Install

```bash
pip install -r requirements.txt
```

## Capability 1: Query location info

```bash
python tools/openstreet_skill.py locate --query "The Bund Shanghai" --limit 1
```

Output is JSON including `display_name`, `lat`, `lon`, and type metadata.

## Capability 2: Render annotated map

Input JSON file format (array):

```json
[
  {"name": "Point A", "lat": 31.2304, "lon": 121.4737},
  {"name": "Point B", "query": "The Bund Shanghai"}
]
```

Render command:

```bash
python tools/openstreet_skill.py render \
  --points-file examples/points.json \
  --output output/annotated_map.png \
  --width 1600 \
  --height 800
```

Render command with base64 JSON input:

```bash
python tools/openstreet_skill.py render \
  --points-base64 "W3sibmFtZSI6IlBvaW50IEEiLCJsYXQiOjMxLjIzMDQsImxvbiI6MTIxLjQ3Mzd9LHsibmFtZSI6IlBvaW50IEIiLCJxdWVyeSI6IlRoZSBCdW5kIFNoYW5naGFpIn1d" \
  --output output/annotated_map.png
```

Optional: render command returning base64-encoded image (no file written):

```bash
python tools/openstreet_skill.py render \
  --points-base64 "..." \
  --base64
```

Optional: render command writing file **and** returning base64:

```bash
python tools/openstreet_skill.py render \
  --points-base64 "..." \
  --output output/annotated_map.png \
  --base64
```

`render` input/output options:

- `--points-file` / `--points-base64`: points source (mutually exclusive, one required).
- `--output`: save image to path. This is the default and recommended output mode.
- `--base64`: include base64-encoded PNG in JSON stdout under `image_base64`. Use only when the caller cannot access output files directly.
- At least one of `--output` or `--base64` must be provided.

> **Recommended**: Default to file output with `--output`.
> Do not use `--base64` unless file delivery is impossible, because base64 image payloads consume a large number of tokens.
>
> ```bash
> python tools/openstreet_skill.py render \
>   --points-file examples/points.json \
>   --output output/annotated_map.png
> ```

Behavior:

- Selects a suitable zoom level to fit all points.
- Downloads OSM tiles and stitches them into one map image.
- Draws numbered markers on each place.
- Appends a three-column legend under the map showing index and place name.
- Saves final image to `--output` path if specified.

JSON output structure:

```json
{
  "zoom": 14,
  "size": { "width": 1200, "height": 880 },
  "places": [
    { "index": 1, "name": "Point A", "lat": 31.2304, "lon": 121.4737 }
  ],
  "output": "output/annotated_map.png"
}
```

- `output`: present only when `--output` is provided.
- `image_base64`: present only when `--base64` is set. PNG image encoded as standard base64. Avoid this in normal flows because it significantly increases token usage.

## Notes for OpenClaw integration

- Expose these two CLI actions as callable tools in OpenClaw:
  - `locate`: maps to `python tools/openstreet_skill.py locate ...`
  - `render`: maps to `python tools/openstreet_skill.py render ...`
- For `render`, default to `--output` file delivery instead of `--base64` to keep responses small.
- Return JSON stdout to the caller and treat non-zero exit code as failure.
- Respect OSM usage policy by not sending high-frequency requests.
