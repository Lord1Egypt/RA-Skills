# photon — fast OSM-based geocoder (Komoot)

## What this source has

Photon is a geocoder built by Komoot on OSM data, served from `photon.komoot.io`. It's the fast/fuzzy alternative to Nominatim — same OSM source, different indexing (Elasticsearch under the hood) optimized for typo-tolerance and partial input. Forward geocoding only (text → coordinates) plus reverse.

Photon doesn't do structured address breakdown as cleanly as Nominatim. It's optimized for "what does the user mean by `paris`" rather than "give me the postal address of 12.3, 45.6". Each result has an OSM ID, lat/lon, and a properties bag with `name`, `country`, `state`, `city`, `street`, `housenumber`, `postcode`, `osm_value`, `osm_key`, `type` (e.g., `city`, `house`, `street`).

Use Photon for: autocomplete-style lookups, fuzzy/typo-tolerant search, free-text → first-best-coordinate. Pair with `nominatim` when you need authoritative structured addresses; pair with `overpass` for surrounding-features queries.

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
| Rate | no published cap; public instance is best-effort, slower under heavy load |

For sustained heavy traffic, self-host (the project ships a Docker image).

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Forward geocode (free text → coords) | `q` |
| `reverse` | Reverse geocode | `lat`, `lon` |

## Worked examples

```bash
# Fuzzy forward search
python3 scripts/reach.py query photon search '{
  "q": "berln germny",
  "limit": 5
}'

# Bias by location (rank closer results first)
python3 scripts/reach.py query photon search '{
  "q": "main street",
  "lat": 40.7128,
  "lon": -74.0060,
  "limit": 5
}'

# Reverse geocoding
python3 scripts/reach.py query photon reverse '{
  "lat": 48.8566,
  "lon": 2.3522
}'

# Filter by OSM tag layer
python3 scripts/reach.py query photon search '{
  "q": "bakery",
  "lat": 48.86,
  "lon": 2.35,
  "layer": "poi",
  "limit": 10
}'
```

## Response shape

GeoJSON `FeatureCollection`:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [lon, lat]},
      "properties": {
        "osm_id": 240109189, "osm_type": "N", "osm_key": "place", "osm_value": "city",
        "type": "city", "name": "Berlin",
        "country": "Germany", "countrycode": "DE",
        "state": "Berlin", "city": "Berlin",
        "postcode": "10117", "housenumber": null,
        "street": null, "extent": [w, n, e, s]
      }
    }
  ]
}
```

## Pitfalls

- **Coordinates are GeoJSON order: `[lon, lat]`.** Nominatim returns `lat`/`lon` strings; Photon returns a coordinates pair in the geometry. Don't swap when chaining.
- **Fuzzy by design.** "berln germny" works — but it also means typos may anchor unexpectedly. Always check the returned `name` before assuming.
- **`lat`/`lon` bias is not a hard filter.** Passing them rerankes results, but the top hit may still be far away if no closer match exists.
- **`limit` cap.** Default is 15; max practically ~100.
- **`layer` filter** restricts result type: `house`, `street`, `locality`, `district`, `city`, `county`, `state`, `country`, `poi`. Comma-separate for multiple.
- **No structured-address parameter.** Unlike Nominatim, you can't pass `street`/`city`/`country` separately. Concatenate into `q`.
- **`extent`** is `[west, north, east, south]` — note non-standard order (north before east).
- **Public instance has no SLA.** For mission-critical geocoding, self-host or pay for a hosted alternative.

## Source links

- Project page: https://photon.komoot.io/
- Source: https://github.com/komoot/photon
- Self-hosting guide: https://github.com/komoot/photon#installation
