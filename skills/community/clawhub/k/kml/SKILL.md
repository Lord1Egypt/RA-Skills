---
name: kml
description: Inspect, validate, summarize, and extract data from KML and KMZ files, including Placemark geometry counts, Folder structure, coordinate ranges, bbox generation, altitude tuples, Google Earth packaging issues, and conversion guidance. Use when the user asks about KML, KMZ, Google Earth placemarks, coordinate extraction, KML cleanup, KMZ debugging, or KML data processing. 中文触发：KML、KMZ、谷歌地球、地标、坐标提取、KML 校验、KMZ 解包、KML 数据处理。
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["python3"]
    install:
      - id: "brew"
        kind: "brew"
        formula: "python"
        bins: ["python3"]
        label: "Install Python 3 (brew)"
---

# KML

Use this skill for practical KML and KMZ inspection, validation, and lightweight data extraction.

This skill is optimized for safe analysis of KML structure and coordinates. For deterministic reprojection, clipping, format conversion, or batch GIS processing on files, hand off to `qgis`.

## What This Skill Does

- Inspect `.kml` and `.kmz` files.
- Summarize document name, placemark count, geometry types, folder count, and bbox.
- Validate coordinate tuples and flag obvious longitude/latitude range problems.
- Extract placemark-level summaries for downstream review or cleanup.
- Explain common KML/KMZ issues such as missing `doc.kml`, malformed XML, empty `Placemark`, or suspicious coordinate order.

## Standard Workflow

1. Confirm whether the input is a `.kml` file or a `.kmz` archive.
2. Parse the XML and detect the main KML document inside KMZ when needed.
3. Count placemarks, geometry types, folders, overlays, and coordinates.
4. Compute bbox from parsed coordinates when possible.
5. Flag likely issues:
   - malformed XML
   - KMZ archive without a readable KML payload
   - coordinate tuples outside lon/lat range
   - empty placemarks without geometry
6. If the user needs reprojection, clipping, or deterministic file conversion, switch to `qgis`.

## Practical Commands

### Summarize a KML or KMZ file

```bash
python3 {baseDir}/scripts/kml_tool.py summary --file ./data/sample.kml
```

### Validate a KML or KMZ file

```bash
python3 {baseDir}/scripts/kml_tool.py validate --file ./data/sample.kmz
```

### List placemark summaries

```bash
python3 {baseDir}/scripts/kml_tool.py placemarks --file ./data/sample.kml
```

## Decision Rules

- Treat KML coordinates as `lon,lat[,alt]` unless the source explicitly says otherwise.
- KML is commonly used with WGS84-style geographic coordinates; if precision matters, confirm the source workflow instead of guessing.
- Do not silently rewrite malformed coordinates; report the exact problem.
- Prefer writing derived outputs to a new path when a later task requires edits or conversion.
- If the user wants GeoJSON, Shapefile, reprojection, clipping, or batch cleanup, route execution to `qgis`.

## What To Return

- Source type: `kml` or `kmz`.
- Document name when present.
- Placemark count and geometry type counts.
- Folder and overlay counts.
- Bounding box when coordinates are present.
- Specific validation errors or suspicious patterns when found.

## When Not To Use

- Reverse geocoding or coordinates-to-address lookup: use `geocode`.
- WGS84-specific CRS reasoning: use `wgs84`.
- Deterministic GIS conversion, reprojection, clipping, or raster/vector processing: use `qgis`.
- Web map rendering logic: use `leaflet`, `mapbox`, or `cesium` as appropriate.

## OpenClaw + ClawHub Notes

- Keep examples generic and portable.
- Do not hardcode private datasets, machine paths, or secrets.
- For clawhub.ai publication, keep examples standards-based and version/changelog updates semver-driven.

## Reference Docs In This Skill

- Read `{baseDir}/references/patterns.md` for KML/KMZ structure notes, common failures, and escalation guidance.
