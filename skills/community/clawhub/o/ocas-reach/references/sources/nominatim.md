# nominatim — OSM-backed geocoding (free-text → coordinates and reverse)

## What this source has

Nominatim is the OpenStreetMap project's geocoder. Forward geocoding turns free text ("221b Baker Street, London") into coordinates + administrative hierarchy; reverse geocoding turns a coordinate into a structured address. Coverage is global wherever OSM has data, which is most of the inhabited world; quality varies regionally — Western Europe and North America are dense; rural areas in some countries are sparse.

Each result has a `place_id` (Nominatim internal, NOT stable across rebuilds), an `osm_type`/`osm_id` pair (the canonical OSM key — stable), a `display_name`, and an `address` object with admin-level breakdown (`country`, `state`, `city`, `road`, `house_number`, `postcode`).

Use Nominatim for: address lookup, "where is X" → lat/lon, structured admin breakdown of a coordinate. Pair with `photon` when you need fuzzy / typo-tolerant search; pair with `overpass` once you have coordinates and want surrounding features.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

The public instance enforces a strict usage policy: max 1 request per second, real `User-Agent` mandatory, no bulk geocoding (use a self-hosted instance for that). Reach sends a compliant `User-Agent` automatically.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 1 request per second absolute (per IP); 50,000-result hard cap on any single search |

Hammering the public instance gets your IP blocked at the load balancer.

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Forward geocode (free text → coords) | `q` (or structured: `street`, `city`, `country`, ...) |
| `reverse` | Reverse geocode (coords → address) | `lat`, `lon` |
| `lookup` | Bulk fetch by OSM IDs | `osm_ids` (comma-separated `N123,W456,R789`) |

## Worked examples

```bash
# Forward geocode an address
python3 scripts/reach.py query nominatim search '{
  "q": "221B Baker Street, London",
  "limit": 1,
  "addressdetails": 1
}'

# Reverse geocode coordinates
python3 scripts/reach.py query nominatim reverse '{
  "lat": 40.7484,
  "lon": -73.9857,
  "zoom": 18,
  "addressdetails": 1
}'

# Structured search
python3 scripts/reach.py query nominatim search '{
  "street": "1600 Pennsylvania Ave",
  "city": "Washington",
  "country": "USA",
  "limit": 1
}'

# Lookup multiple OSM elements
python3 scripts/reach.py query nominatim lookup '{
  "osm_ids": "N240109189,W34633854,R195384"
}'
```

## Response shape

- `search`: list of `[{place_id, licence, osm_type, osm_id, lat, lon, class, type, place_rank, importance, addresstype, name, display_name, boundingbox: [s, n, w, e], address: {house_number, road, city, state, postcode, country, country_code, ...}}, ...]`. `lat`/`lon` are strings — convert to float.
- `reverse`: a single object with the same fields. If the coord is over open water you get `{error: "Unable to geocode"}`.
- `lookup`: same array shape as `search`.

## Pitfalls

- **1 req/sec is enforced by the load balancer**, not just etiquette. Burst over and you'll get 429s, then a temporary block.
- **`User-Agent` rule.** Anonymous or generic UAs (browser fingerprints) get blocked. Reach injects a compliant one.
- **No bulk geocoding on the public instance.** Hundreds of consecutive queries earn a block. Self-host for batch work.
- **`lat`/`lon` are strings in responses.** Cast before math.
- **`boundingbox` is `[south, north, west, east]`** — note the order, opposite of GeoJSON convention.
- **`osm_type` codes.** `node`/`way`/`relation` in responses; abbreviated `N`/`W`/`R` in `lookup` `osm_ids` parameter. Don't mix.
- **`addressdetails: 1`** is required to get the `address` object — without it you only get `display_name`.
- **`zoom` on reverse** controls admin-level granularity: 18 = building, 14 = neighborhood, 10 = city, 5 = country. Default is 18.
- **House-number ambiguity.** Many OSM entries have ranges or are missing — search may return the road without the number.

## Source links

- API docs: https://nominatim.org/release-docs/latest/api/Overview/
- Usage policy: https://operations.osmfoundation.org/policies/nominatim/
- Source / self-host: https://github.com/osm-search/Nominatim
