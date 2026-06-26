# Leaflet Patterns

Use this reference when the user needs concrete code structure or debugging heuristics.

## Minimal runtime checklist

- The page loads Leaflet JS and CSS.
- The map container exists before initialization.
- The container has explicit height.
- A tile layer is added after `L.map(...)`.
- Attribution is present when required by the tile provider.

## Coordinate and CRS rules

- Leaflet APIs commonly use `[lat, lng]` for `setView`, markers, and many direct method calls.
- GeoJSON coordinate arrays remain `[lng, lat]`.
- Many "wrong location" bugs come from mixing Leaflet method order with GeoJSON order.
- If the source data is not ordinary WGS84-style longitude/latitude, identify the CRS before rendering.

## SPA integration rules

- Create the map once per mounted container.
- Keep the map instance in stable state or a ref, not in repeated render-local variables.
- Remove listeners and destroy the map on teardown.
- When a hidden container becomes visible later, call `invalidateSize()`.

## Tile layer guidance

- Prefer a known XYZ source unless the user already has a provider.
- Keep the tile URL and attribution configurable.
- Do not assume a provider allows unrestricted production traffic.
- Verify retina, subdomain, maxZoom, and bounds options only when needed.

## GeoJSON guidance

- Use `L.geoJSON(data, { style, pointToLayer, onEachFeature })`.
- Keep style functions deterministic and cheap.
- Bind popups from feature properties carefully; avoid raw HTML injection from untrusted data.
- Fit map bounds from the overlay when the map should focus on that dataset.

## Common debugging sequence

1. Prove the map container renders.
2. Prove a basic tile layer loads.
3. Add one marker with known coordinates.
4. Add the real overlay.
5. Add controls and plugins last.

## When to reach for another skill

- `mapbox`: vector tiles, GL-style layers, token-based Mapbox APIs.
- `qgis`: deterministic reprojection and file-based GIS processing.
- `project` or `wgs84`: CRS selection and coordinate-system reasoning.
- `cgcs2000`: China-specific CGCS2000 workflows.
