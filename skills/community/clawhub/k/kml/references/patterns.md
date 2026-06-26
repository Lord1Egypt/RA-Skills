# KML And KMZ Notes

Use this reference when the task needs more detail than the main skill body.

## Core Facts

- KML coordinates are ordered as `longitude,latitude[,altitude]`.
- KMZ is a zip archive that usually contains `doc.kml`, but real-world archives may store the main KML under another `.kml` path.
- `Placemark` often contains one of `Point`, `LineString`, `Polygon`, `MultiGeometry`, or `gx:Track`.
- `GroundOverlay` and `NetworkLink` are valid KML constructs but are not general vector features.

## Common Failure Patterns

- XML parses but no KML namespace is present.
- KMZ opens but contains no `.kml` file.
- `Placemark` exists with no geometry.
- `coordinates` text contains malformed tuples or commas/spaces in the wrong places.
- Longitudes or latitudes fall outside normal geographic ranges.
- The file is visually wrong because the intended CRS or source export workflow was misunderstood.

## Escalation Guidance

- If the user wants actual conversion or geometry repair on files, switch to `qgis`.
- If the user asks whether coordinates are valid WGS84, use `wgs84` for the CRS reasoning and keep `kml` focused on the container and payload.
- If the user only needs a quick structure summary, do not load this reference.

