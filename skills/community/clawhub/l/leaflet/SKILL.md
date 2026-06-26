---
name: leaflet
description: Build, debug, and integrate Leaflet web maps, including map setup, tile layers, markers, popups, GeoJSON overlays, bounds fitting, event handling, and plugin-safe patterns for vanilla HTML, Vite, React, and other frontend apps. Use when the user asks for Leaflet code, OpenStreetMap/XYZ tile integration, 2D web map debugging, or Leaflet migration guidance. 中文触发：Leaflet、OSM 地图、瓦片底图、GeoJSON 地图、交互地图、前端地图调试。
homepage: https://leafletjs.com/
metadata:
  openclaw:
    emoji: "🍃"
    homepage: "https://leafletjs.com/"
---

# Leaflet

Use this skill for practical 2D web map work with Leaflet.

Leaflet is best for lightweight interactive maps that need simple setup, raster or XYZ tile layers, GeoJSON overlays, and straightforward custom controls. It is usually the right choice when the user wants a dependable browser map without the heavier rendering model of WebGL-first stacks.

## Workflow

1. Confirm the runtime first:
   - plain HTML
   - Vite
   - React
   - Next.js or another SPA framework
2. Confirm the actual map job:
   - base map only
   - markers and popups
   - GeoJSON overlay
   - choropleth or feature styling
   - draw/edit interaction
   - bug fixing or migration
3. Start from the smallest visible map before adding controls, overlays, clustering, or plugins.
4. Check container size and CSS before debugging data or tile logic.
5. Keep data CRS assumptions explicit; Leaflet usually expects WGS84 longitude/latitude input for GeoJSON-style work.

## Implementation Guardrails

- Ensure the map container has a real height before initializing the map.
- Use `L.map(...)` once per container and clean it up in SPA teardown paths.
- Fit bounds from real data instead of hardcoding zoom/center when the dataset is dynamic.
- Prefer `L.geoJSON(...)` for lightweight vector overlays and feature-level styling.
- Keep tile URLs configurable and attribute them correctly.
- Use clustering or canvas-based rendering when marker counts grow large.
- Treat plugins as optional dependencies; verify maintenance status and compatibility before adopting them.

## Common Failure Checks

- Blank map: verify container height, CSS import, tile URL, and network access.
- Tiles not loading: verify URL template, attribution requirements, CORS behavior, and rate limits.
- Features in the wrong place: verify coordinate order and whether the source data is really WGS84 lon/lat.
- Map rendering oddly after resize or tab switch: call `map.invalidateSize()` after the container becomes visible.
- Memory leaks in React or SPA routes: remove the map instance and detach listeners on teardown.
- Slow interaction with many points: cluster points, simplify GeoJSON, or switch from DOM-heavy markers to canvas-friendly rendering.

## Practical Patterns

### Minimal map

- Create the map only after the container exists.
- Add one tile layer with attribution.
- Set a sane initial center/zoom or fit to bounds from data.

### GeoJSON overlay

- Use `L.geoJSON` with explicit style and `onEachFeature`.
- Keep popup content deterministic and escape or sanitize user-provided text.
- Fit to the resulting layer bounds when the overlay is the main subject.

### Interactive app integration

- Store the map instance outside repeated render loops.
- Update layers incrementally instead of recreating the entire map on every state change.
- Separate base layer setup from data overlay updates.

### Drawing and editing

- Use a maintained drawing plugin only when the user explicitly needs editing.
- Confirm output format, CRS assumptions, and persistence flow before wiring edit tools.

## Task Boundaries

- Use this skill for Leaflet-specific implementation, debugging, and integration patterns.
- For CRS and reprojection decisions, use `project` or `wgs84`.
- For China-specific CGCS2000 reasoning, use `cgcs2000`.
- For file-based GIS conversion or batch reprojection, use `qgis`.
- For Mapbox GL JS or vector-tile style expressions, use `mapbox`.
- For CesiumJS globe rendering, use `cesium`.

## What To Return

- A minimal working Leaflet setup or a targeted fix.
- The likely root cause when debugging a broken map.
- Clear notes on tile source assumptions, coordinate order, and CRS constraints.
- Any required cleanup or lifecycle handling for the framework in use.
- A smaller reproducible example first if the original integration is too noisy.

## OpenClaw + ClawHub Notes

- Keep examples generic, portable, and safe to paste into local projects.
- Do not hardcode private tile servers, private tokens, or machine-specific paths.
- Prefer maintained public dependencies and standards-based examples.
- For clawhub.ai publication, keep examples reproducible and version/changelog updates semver-driven.

## Reference Docs In This Skill

- Read `{baseDir}/references/patterns.md` when generating or fixing Leaflet code for vanilla HTML, Vite, React, or GeoJSON-heavy pages.
