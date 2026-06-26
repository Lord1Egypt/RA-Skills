# OpenLayers Patterns

Use this reference when the task needs more detail than the main skill body.

## Runtime Checklist

- Confirm whether the app is plain HTML, Vite, React, or another SPA.
- Confirm the installed OpenLayers package or CDN strategy.
- Confirm whether the displayed map view is default Web Mercator (`EPSG:3857`) or another projection.

## Projection Rules

- OpenLayers view coordinates are often in the view projection, not raw lon/lat.
- For display on the default web map, transform geographic coordinates with `fromLonLat([lng, lat])`.
- For GeoJSON reads, pass `dataProjection` for the source data and `featureProjection` for the map view when they differ.
- Do not assume every incoming dataset is WGS84 without checking context.

## Debugging Sequence

1. Verify the container has size.
2. Verify the map target exists before map initialization.
3. Verify the base layer loads.
4. Verify the view center and zoom are sane.
5. Verify overlay feature extent and projection handling.
6. Verify interactions and event handlers only after the map is visibly correct.

## Migration Notes

- From Leaflet to OpenLayers:
  - expect more explicit projection handling
  - prefer `Map`, `View`, `Layer`, `Source` composition over plugin-heavy shortcuts
  - replace implicit `lat,lng` habits with explicit `lng,lat` plus transform utilities
- From Mapbox GL to OpenLayers:
  - think in OpenLayers layers and sources rather than style-spec layers
  - hosted vector-tile styling workflows may need a different rendering setup
  - feature interaction is often implemented directly against map events and vector layers

