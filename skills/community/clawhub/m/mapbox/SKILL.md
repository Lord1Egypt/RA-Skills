---
name: mapbox
description: Build, debug, and integrate Mapbox apps and APIs, including Mapbox GL JS map setup, styles, sources/layers, markers/popups, geocoding, directions, static images, and token-safe frontend patterns. Use when the user asks for Mapbox code, Mapbox architecture, style expressions, tile/source issues, or Mapbox migration guidance. 中文触发：Mapbox、地图样式、矢量瓦片、地理编码、路径规划、底图集成。
metadata:
  openclaw:
    emoji: "🗺️"
---

# Mapbox

Use this skill for practical Mapbox platform work in web apps and API integrations.

## Workflow

1. Confirm the runtime first: plain HTML, Vite, React, Next.js, or another framework.
2. Confirm which Mapbox surface is involved: GL JS map rendering, styles, tilesets, geocoding, directions, or static images.
3. Start with the smallest working map before adding custom sources, layers, controls, or API calls.
4. Keep access tokens out of source files and examples unless the user explicitly wants a local-only demo.
5. For bugs, isolate whether the failure is in container sizing, token/scopes, style/source IDs, coordinate order, or layer order.

## Implementation Guardrails

- Prefer `mapbox-gl` with explicit imports and explicit CSS loading.
- Always ensure the map container has a real height before debugging rendering.
- Use `lng, lat` order consistently for Mapbox coordinate arrays.
- Add sources before layers, and keep layer IDs stable so updates are easy.
- Prefer GeoJSON for lightweight overlays; move to vector tiles or tilesets for larger datasets.
- In React or other SPA frameworks, remove the map instance during teardown to avoid leaks.
- Treat the access token as configuration. Read it from environment or runtime config instead of hardcoding it.

## Common Failure Checks

- Blank map: verify token, style URL, CSS import, and container height.
- Layer not visible: verify source exists, source-layer matches, zoom bounds, and paint/layout visibility.
- Wrong location: verify coordinate order and CRS assumptions; Mapbox expects WGS84 `lng,lat`.
- Performance issues: reduce marker count, cluster point data, and prefer data-driven layers over many DOM markers.
- API failures: verify token scopes, endpoint type, rate limits, and request parameters.

## Task Boundaries

- Use this skill for Mapbox-specific implementation, debugging, and integration patterns.
- For generic CRS/projection reasoning, use `project` or `wgs84`.
- For deterministic desktop GIS batch processing, use `qgis`.
- For CesiumJS globe rendering, use `cesium`.

## OpenClaw + ClawHub Notes

- Keep examples generic, portable, and token-safe.
- Do not hardcode private datasets, private style URLs, or machine-specific paths.
- For clawhub.ai publication, keep content reproducible and semver-friendly; put detailed examples in references instead of bloating `SKILL.md`.

## Reference Docs In This Skill

- Read `{baseDir}/references/patterns.md` when generating or fixing Mapbox GL JS or API integration code.
