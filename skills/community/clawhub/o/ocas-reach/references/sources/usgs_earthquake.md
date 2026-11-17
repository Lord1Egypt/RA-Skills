# usgs_earthquake — global earthquake catalog (FDSN spec)

## What this source has

The USGS Earthquake Hazards Program serves the authoritative US-monitored earthquake catalog plus contributed data from regional networks worldwide. Every detected event from 1900 onward (older for major events), with magnitude, location (lat/lon/depth), origin time, magnitude type (Mw, ML, mb), phase data, and product attachments (ShakeMap, DYFI "Did You Feel It?", focal mechanisms).

The API implements the FDSN (International Federation of Digital Seismograph Networks) `event` web service spec — the same interface IRIS, EMSC, and other seismic networks expose. Each event has an event ID like `us6000m1y3` (network code + sequence).

Use USGS Earthquake for: recent earthquake counts/locations, "biggest quake near X this year", historical seismicity. Pair with `noaa_nws` for related tsunami warnings; pair with `nasa` EONET for an integrated natural-disaster feed.

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
| Rate | no documented cap; large queries (`limit > 20000`) are paged or rejected |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `query` | Search events (default `format=geojson`) | none (but pass at least one filter) |
| `count` | Count matching events without fetching | none |
| `version` | Web-service version | none |

## Worked examples

```bash
# Magnitude 5+ earthquakes worldwide in the last 30 days
python3 scripts/reach.py query usgs_earthquake query '{
  "starttime": "2026-03-26",
  "endtime": "2026-04-26",
  "minmagnitude": 5,
  "orderby": "magnitude"
}'

# Quakes within 200km of San Francisco, last year
python3 scripts/reach.py query usgs_earthquake query '{
  "latitude": 37.7749,
  "longitude": -122.4194,
  "maxradiuskm": 200,
  "starttime": "2025-04-26",
  "minmagnitude": 2.5
}'

# Just count: how many M3+ in California this month?
python3 scripts/reach.py query usgs_earthquake count '{
  "starttime": "2026-04-01",
  "endtime": "2026-04-26",
  "minmagnitude": 3,
  "minlatitude": 32.5,
  "maxlatitude": 42,
  "minlongitude": -124.5,
  "maxlongitude": -114
}'
```

## Response shape

`query` (with `format=geojson`, the default): GeoJSON `FeatureCollection`:

```json
{
  "type": "FeatureCollection",
  "metadata": {"generated": <ms>, "url": "...", "title": "...", "count": 42},
  "features": [
    {
      "type": "Feature",
      "properties": {
        "mag": 5.2, "place": "12 km NE of ...", "time": <ms>, "updated": <ms>,
        "tz": null, "url": "...", "detail": "...",
        "felt": 17, "cdi": 4.3, "mmi": null, "alert": null,
        "status": "reviewed", "tsunami": 0, "sig": 416,
        "net": "us", "code": "6000m1y3", "ids": ",us6000m1y3,...",
        "type": "earthquake", "magType": "mww", "title": "M 5.2 - ..."
      },
      "geometry": {"type": "Point", "coordinates": [<lon>, <lat>, <depth_km>]},
      "id": "us6000m1y3"
    }
  ]
}
```

`count`: `{count: <int>, maxAllowed: 20000}`.

## Pitfalls

- **`time` is milliseconds since epoch**, not seconds. Off by 1000 if you forget.
- **Coordinates are `[lon, lat, depth]`** — GeoJSON order, with depth in km as the third element. Don't swap.
- **`starttime`/`endtime` accept ISO-8601** but treat both as UTC. Adding `Z` is fine; passing local-time strings without offset is silently UTC.
- **`maxradiuskm` requires `latitude` AND `longitude`.** Passing only one returns 400.
- **`limit` defaults to 20,000 and caps there.** For larger pulls, page by `starttime`/`endtime` windows.
- **`magnitude` filter uses `minmagnitude`/`maxmagnitude`**, not `mag` (the field name in responses). The asymmetry trips up everyone.
- **`magType` varies.** `mww` (moment magnitude), `mb` (body wave), `ml` (local), `md` (duration). For "the magnitude" use `mag` directly — USGS picks the preferred type per event.
- **`alert` field is PAGER alert level** (green/yellow/orange/red), not whether you'll be notified. Most events have `alert: null`.
- **Status `automatic` vs `reviewed`.** Auto-located events get revised; for stable historical analysis filter `status=reviewed`.

## Source links

- FDSN event service docs: https://earthquake.usgs.gov/fdsnws/event/1/
- Catalog overview: https://earthquake.usgs.gov/data/comcat/
- Magnitude type reference: https://www.usgs.gov/programs/earthquake-hazards/magnitude-types
