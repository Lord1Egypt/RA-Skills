# Normalization Guide - Maps

Normalize provider output before merging, ranking, or caching it.

## Canonical Coordinate Model

Keep coordinates internally as:

```text
lat: decimal degrees
lng: decimal degrees
precision: rooftop | range_interpolated | approximate | centroid | unknown
```

Preserve at least 6 decimal places when the provider offers them.

## Canonical Place Record

Use this minimum record shape:

```text
provider
provider_id
label
formatted_address
lat
lng
confidence
precision
status
types[]
timezone
source_url
```

## Provider Serialization Differences

| Provider or format | Coordinate order | Notes |
|--------------------|------------------|-------|
| Google Maps APIs | `lat,lng` | Human-readable order in most docs and URLs |
| Apple Maps links | `lat,lng` or text query plus optional `ll` | Best for opening or sharing, not for rich place IDs |
| GeoJSON | `[lng, lat]` | Common source of inverted points |
| Mapbox APIs | `[lng, lat]` in many payloads | Do not reuse Google serialization blindly |
| OSRM | `lng,lat` in path segments | Keep conversion explicit at request boundaries |

## Confidence Rules

- `rooftop` or exact parcel match -> safe for navigation and delivery-style precision
- `range_interpolated` -> good for address vicinity, not for exact entrance claims
- `approximate` or locality-level -> safe for area search only
- mixed-provider disagreement -> ask a clarification question or show top candidates

## Route Normalization

For every route or matrix result, normalize:
- provider
- travel mode
- distance meters
- duration seconds
- traffic included yes or no
- tolls or restrictions stated yes or no
- waypoint order returned yes or no

Never compare route outputs until units and traffic assumptions match.
