# transit_land — Transit Land API (GTFS Transit Data)

## What this source has

Transit Land aggregates GTFS (General Transit Feed Specification) and GTFS-Realtime data from 1000+ transit agencies worldwide. Data includes:

- Transit routes (bus, rail, ferry, etc.)
- Stops and stations
- Agencies/operators
- Schedule data (stop pairs with arrival/departure times)
- Route geometries

Use transit_land for: transit route lookup, stop finding, schedule queries, trip planning research, and complementing geo sources with transit-specific data.

## Auth

| | |
|---|---|
| Required | none |
| Account | optional |

Anonymous access available with rate limits. API key available for higher limits.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 1000/hour anonymous; higher with key |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `routes` | Search transit routes | none (optional: `operated_by`, `search`, `bbox`) |
| `stops` | Search transit stops | none (optional: `search`, `bbox`, `served_by`) |
| `operators` | List transit agencies | none (optional: `search`, `country`) |
| `schedule` | Get schedule stop pairs | none (optional: `route_onestop_id`, `date`) |

## Worked examples

```bash
# Search for BART routes
python3 scripts/reach.py query transit_land routes '{"search": "BART", "operated_by": "o-9q9-bart"}'

# Find stops near a location (bbox)
python3 scripts/reach.py query transit_land stops '{"bbox": "-122.5,37.7,-122.3,37.8", "served_by": "o-9q9-bart"}'

# List operators in a country
python3 scripts/reach.py query transit_land operators '{"country": "US"}'

# Get schedule for a route
python3 scripts/reach.py query transit_land schedule '{"route_onestop_id": "r-9q9-10", "date": "2024-01-15"}'
```

## Response shape

Standard REST JSON with pagination:

```json
{
  "routes": [
    {
      "onestop_id": "r-9q9-10",
      "name": "Richmond - Daly City/Millbrae",
      "operated_by": "o-9q9-bart",
      "geometry": { "type": "LineString", "coordinates": [...] },
      "tags": { "route_color": "FF0000" }
    }
  ],
  "meta": {
    "total": 12,
    "per_page": 50,
    "page": 1
  }
}
```

## Pitfalls

- **Onestop IDs are the primary key.** Routes use `r-` prefix, stops use `s-`, operators use `o-`. Use search endpoints to find IDs.
- **Bbox format is `min_lon,min_lat,max_lon,max_lat`.** Not the same as typical map bbox ordering.
- **GTFS data quality varies by agency.** Some agencies have rich data, others are minimal.
- **Schedule data is large.** Use date filters and pagination. Don't request all stop pairs for a large system.
- **Rate limits apply.** Anonymous users get 1000/hour. Cache results for repeated queries.
- **Complements geo sources.** Use Nominatim/Photon for geocoding, Transit Land for transit-specific data.

## Source links

- Transit Land: https://www.transit.land/
- API docs: https://www.transit.land/documentation/rest
- GTFS spec: https://gtfs.org/
- Dataset: https://www.transit.land/documentation/feed-registry
