# Layer Recipes

Use this reference for concrete layer wiring patterns.

## OSM Base Layer

- Use `TileLayer` with `OSM` for the quickest public demo.
- Keep attribution visible.

## XYZ Tiles

- Use `TileLayer` with `XYZ`.
- Verify URL template, attribution, max zoom, retina behavior, and cross-origin needs.

## GeoJSON Overlay

- Use `VectorSource` plus `GeoJSON`.
- Explicitly set `dataProjection` and `featureProjection` when the source CRS is known.
- Fit to `vectorSource.getExtent()` after load.

## WMS

- Use `TileWMS` or `ImageWMS` depending on the use case.
- Confirm service URL, params, layer names, styles, transparent mode, and server CRS support.

## WMTS

- Build or derive the correct tile grid and matrix set.
- Matrix set mismatch is a common failure source.

## Interaction Patterns

- Picking: `map.forEachFeatureAtPixel(...)`
- Hover feedback: `pointermove` with throttled highlight updates
- Editing: `Draw`, `Modify`, `Snap`, and `Select` only when the output workflow is clear

