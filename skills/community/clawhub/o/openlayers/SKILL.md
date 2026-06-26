---
name: openlayers
description: Build, debug, and integrate OpenLayers web maps, including map/view setup, XYZ and OSM base layers, vector sources, GeoJSON overlays, Web Mercator and WGS84 handling, feature styling, click/pointer interaction, layer ordering, fit-to-extent flows, and frontend integration for vanilla HTML, Vite, React, and similar apps. Use when the user asks for OpenLayers code, `ol` usage, OpenLayers debugging, web GIS map implementation, or migration guidance from Leaflet/Mapbox. 中文触发：OpenLayers、ol 地图、前端 GIS、GeoJSON 地图、矢量图层、Web Mercator、地图交互、OpenLayers 调试。
metadata:
  openclaw:
    emoji: "🧭"
    homepage: "https://openlayers.org/"
    requires:
      bins: ["python3"]
    install:
      - id: "brew"
        kind: "brew"
        formula: "python"
        bins: ["python3"]
        label: "Install Python 3 (brew)"
---

# OpenLayers

Use this skill for practical OpenLayers web map work in browser apps.

OpenLayers is the right choice when the user needs a stronger GIS-style 2D web map stack than Leaflet, especially for projection-aware workflows, tiled and vector layers, custom styling, feature interaction, and more explicit control over map/view/source/layer composition.

## Workflow

1. Confirm the runtime first:
   - plain HTML
   - Vite
   - React
   - Next.js or another SPA framework
2. Confirm the actual map job:
   - base map only
   - markers or selected features
   - GeoJSON overlay
   - WMS or WMTS layer
   - draw or modify interaction
   - bug fixing or migration
3. Start from the smallest visible map before adding custom sources, interactions, or large datasets.
4. Check container size, CSS, and projection assumptions before debugging layer logic.
5. Keep coordinate transforms explicit; OpenLayers often needs `fromLonLat(...)` or explicit `dataProjection` and `featureProjection`.

## Implementation Guardrails

- Ensure the map container has a real height before initializing `Map`.
- Keep `View` projection, incoming data projection, and display projection explicit.
- Use `fromLonLat([lng, lat])` for geographic coordinates shown on the default Web Mercator map.
- For GeoJSON, set both `dataProjection` and `featureProjection` when the source CRS is known.
- Prefer stable layer and source instances instead of recreating the whole map on every state update.
- Clean up the map target in SPA teardown paths.
- Fit bounds from actual features or source extents when the dataset is dynamic.
- Style features deterministically; do not bury business logic inside a style function unless the user needs data-driven styling.

## Common Failure Checks

- Blank map: verify container height, CSS import, map target, and layer source URL.
- Features in the wrong place: verify whether lon/lat was used without `fromLonLat(...)`, or whether GeoJSON projections were omitted.
- Click picking not working: verify layer visibility, z-index ordering, and `forEachFeatureAtPixel(...)` usage.
- Map looks offset after layout changes: call `map.updateSize()` after the container becomes visible or resizes.
- Performance issues with many features: simplify data, cluster points, reduce style churn, or move expensive logic out of pointer handlers.
- WMS or WMTS not rendering: verify service URL, layer names, matrix set, CRS, and cross-origin behavior.

## Practical Patterns

### Minimal map

- Create one `Map`, one `View`, and one base `TileLayer`.
- Use `OSM` or `XYZ` only after confirming the tile URL and attribution requirements.
- Set center using `fromLonLat(...)` when starting from geographic coordinates.

### GeoJSON overlay

- Use `VectorSource` with a `GeoJSON` format object.
- Set `dataProjection` and `featureProjection` explicitly when precision matters.
- Fit the view to `vectorSource.getExtent()` after features load.

### Interactive picking

- Use `map.on("singleclick", ...)` for primary feature selection.
- Use `forEachFeatureAtPixel(...)` to identify the top visible feature.
- Keep popup or side-panel rendering outside the OpenLayers style layer when possible.

### SPA integration

- Create the map once after the container mounts.
- Reuse `Source` and `Layer` objects across updates.
- On teardown, call `map.setTarget(undefined)` to release DOM bindings.

### Draw and edit

- Add `Draw`, `Modify`, or `Select` only when the user explicitly needs editing.
- Confirm output format and projection before persisting edited geometries.

## Task Boundaries

- Use this skill for OpenLayers-specific implementation, debugging, and migration patterns.
- For CRS and reprojection reasoning, use `project`, `wgs84`, or `cgcs2000` as appropriate.
- For file-based GIS conversion or batch reprojection, use `qgis`.
- For lightweight non-GIS-heavy web maps, `leaflet` may be simpler.
- For Mapbox GL style expressions or hosted Mapbox platform APIs, use `mapbox`.
- For globe and 3D scene rendering, use `cesium`.

## What To Return

- A minimal working OpenLayers setup or a targeted fix.
- The likely root cause when debugging projection, sizing, or layer visibility issues.
- Clear notes on coordinate order, projection assumptions, and view fitting.
- Framework-specific lifecycle handling when relevant.
- A smaller reproducible example first if the original integration is noisy.

## Practical Commands

### Generate a minimal OpenLayers page

```bash
python3 {baseDir}/scripts/openlayers_scaffold.py minimal --out ./openlayers-demo.html
```

### Generate a GeoJSON-ready OpenLayers page

```bash
python3 {baseDir}/scripts/openlayers_scaffold.py geojson --out ./openlayers-geojson.html --geojson ./data/sample.geojson
```

## OpenClaw + ClawHub Notes

- Keep examples generic, portable, and safe to paste into local projects.
- Do not hardcode private tile services, private tokens, or machine-specific paths.
- Prefer standards-based examples and explicit projection handling over hidden magic.
- For clawhub.ai publication, keep examples reproducible and version/changelog updates semver-driven.

## Reference Docs In This Skill

- Read `{baseDir}/references/patterns.md` when generating or fixing OpenLayers code.
- Read `{baseDir}/references/layer-recipes.md` when the task involves XYZ, OSM, GeoJSON, WMS, WMTS, or feature interaction patterns.
