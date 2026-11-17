# overpass — OpenStreetMap features via Overpass QL

## What this source has

Overpass is a read-only mirror of the global OpenStreetMap database, queryable with its own DSL — Overpass QL. Every node, way, and relation in OSM is reachable: streets, buildings, POIs, administrative boundaries, transit lines, hiking trails, addresses, opening hours. Updated to within minutes of OSM edits.

OSM identifies elements by a (type, ID) pair: nodes are points, ways are ordered lists of nodes (lines or polygons), relations group elements (e.g., a multi-polygon for a national park). Tags are key-value pairs like `amenity=cafe` or `highway=primary`.

Use Overpass for: "all coffee shops in a bounding box", "every hospital within 5km of a point", "trails tagged `sac_scale=alpine_hiking` in Switzerland". Pair with `nominatim` for free-text → coordinates first, then Overpass for features around those coordinates.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 10,000 query elements per 5 min (per IP); throttled when public instance is busy |

The public Overpass instance (`overpass-api.de`) is shared. Heavy queries can be killed mid-execution. For repeated heavy use, set up your own instance.

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `query` | Run an Overpass QL query (POST body, plain text) | `data` (raw QL string) |

## Worked examples

```bash
# All cafes in a Berlin bounding box
python3 scripts/reach.py query overpass query '{
  "data": "[out:json][timeout:25]; node[\"amenity\"=\"cafe\"](52.50,13.38,52.54,13.42); out body;"
}'

# All hospitals within 2km of a coordinate
python3 scripts/reach.py query overpass query '{
  "data": "[out:json]; (node[\"amenity\"=\"hospital\"](around:2000,40.7128,-74.0060); way[\"amenity\"=\"hospital\"](around:2000,40.7128,-74.0060);); out center;"
}'

# Trails tagged sac_scale=alpine_hiking in a Swiss bbox
python3 scripts/reach.py query overpass query '{
  "data": "[out:json][timeout:60]; way[\"sac_scale\"=\"alpine_hiking\"](46.0,7.5,46.5,8.5); out geom;"
}'
```

## Response shape

```json
{
  "version": 0.6,
  "generator": "Overpass API ...",
  "osm3s": {"timestamp_osm_base": "...", "copyright": "..."},
  "elements": [
    {"type": "node", "id": 12345, "lat": 52.51, "lon": 13.40, "tags": {"amenity": "cafe", "name": "..."}},
    {"type": "way", "id": 67890, "nodes": [...], "tags": {...}},
    {"type": "relation", "id": 11, "members": [...], "tags": {...}}
  ]
}
```

The `out` statement controls what's returned: `out body;` returns tags + minimal geometry, `out center;` adds a centroid for ways/relations, `out geom;` includes full geometry for ways.

## Pitfalls

- **Overpass QL is its own language — NOT SPARQL, NOT SQL.** Statements end in `;`. Filters use `["key"="value"]` syntax. Bounding boxes are `(south,west,north,east)`. Misordering coordinates returns empty.
- **POST as `text/plain`, not URL-encoded.** The connector handles this — the body is the raw QL string. Don't double-wrap in JSON.
- **`[out:json]` at the top is required for JSON output.** Without it you get XML.
- **`[timeout:N]` cap.** The public instance honors timeouts up to ~180 seconds. Long queries die without it.
- **Way/relation geometry is opt-in.** A bare `out body;` on ways gives you node references, not coordinates. Use `out center;` or `out geom;` to get usable spatial data.
- **`(around:radius,lat,lon)` order.** Radius first (in meters), then lat, then lon. Reversing returns empty silently.
- **Recursion operators.** `>;` after a statement adds child nodes of returned ways; `<;` adds parent relations. Forgetting these is the #1 cause of "I got the way IDs but no coordinates".
- **Tag values are case-sensitive.** `amenity=Cafe` won't match `amenity=cafe`.

## Source links

- Overpass QL guide: https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL
- Overpass turbo (interactive): https://overpass-turbo.eu/
- OSM tag reference: https://wiki.openstreetmap.org/wiki/Map_features
