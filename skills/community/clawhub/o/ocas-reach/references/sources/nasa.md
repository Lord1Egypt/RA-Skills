# nasa — single-key umbrella over many NASA APIs

## What this source has

A single NASA API key unlocks half a dozen distinct datasets:

- **APOD** — Astronomy Picture of the Day (image + scientist-written explanation, daily back to 1995)
- **NEO** — Near-Earth Object database (asteroids: orbit, miss distance, hazard flag, close-approach dates)
- **EPIC** — full-disk Earth imagery from DSCOVR satellite (natural-color photos roughly hourly)
- **EONET** — open natural-event tracker (wildfires, storms, volcanoes, icebergs — categorized)
- **Mars Rover Photos** — Curiosity / Opportunity / Spirit / Perseverance image archives by sol or Earth date
- **Earth Imagery** — Landsat overlays at lat/lon

Use NASA for: imagery (especially for daily briefings — APOD), space hazards, real-time disaster events (EONET is excellent), Mars-related curiosity. EONET in particular is the cleanest open-access "active disasters" feed I know of.

## Auth

| | |
|---|---|
| Required | yes |
| Env var | `NASA_KEY` |
| Account URL | https://api.nasa.gov/ |
| Plan tier | free |

Reach is authorized to register at api.nasa.gov using `<agent-email>`. The signup form is one page (name, email, "what are you using this for"). Key issued instantly. The placeholder `DEMO_KEY` works but is shared and rate-limited to 30/hour — register and use a real key.

## Limits

| | |
|---|---|
| Daily | 1,000 |
| Monthly | — |
| Rate | 1,000 / hour (per registered key) |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `apod` | Astronomy Picture of the Day | optional `date` (YYYY-MM-DD) or `start_date`+`end_date` |
| `neo_feed` | Near-Earth Objects in date window | `start_date`, `end_date` |
| `neo_lookup` | Lookup by NEO id | `id` |
| `epic` | DSCOVR Earth imagery | none for "latest"; or `date` |
| `eonet` | Active natural events | optional `category`, `status`, `days` |
| `mars_rover` | Photos | `rover` (`curiosity`, `perseverance`, etc.); + `sol` or `earth_date` |

## Worked examples

```bash
# Today's Astronomy Picture of the Day
python3 scripts/reach.py query nasa apod '{}'

# NEOs passing close to Earth this week
python3 scripts/reach.py query nasa neo_feed '{
  "start_date": "2026-04-26",
  "end_date":   "2026-05-03"
}'

# Currently active wildfires per EONET
python3 scripts/reach.py query nasa eonet '{"category": "wildfires", "status": "open"}'

# Curiosity sol 1000 photos
python3 scripts/reach.py query nasa mars_rover '{"rover": "curiosity", "sol": 1000}'
```

## Response shape

Each sub-API has its own shape; major fields:

- `apod`: `{date, title, explanation, url, hdurl, media_type, copyright?}`
- `neo_feed`: `{element_count, near_earth_objects: {"YYYY-MM-DD": [{id, name, absolute_magnitude_h, is_potentially_hazardous_asteroid, close_approach_data: [{close_approach_date, miss_distance, relative_velocity}]}, ...]}}`
- `eonet`: `{title, description, link, events: [{id, title, description, categories, sources, geometries: [{date, type, coordinates}]}, ...]}` — geometries are in time-ordered sequence per event.
- `epic`: list of `{identifier, caption, image, date, centroid_coordinates, dscovr_j2000_position, ...}`. Image URL must be constructed from date + identifier.
- `mars_rover`: `{photos: [{id, sol, camera, img_src, earth_date, rover}, ...]}`

## Pitfalls

- **`DEMO_KEY` rate-limits aggressively.** 30 req/hour, 50 req/day. Always register and use a real key.
- **EPIC image URL construction.** The `image` field is a stem; the full URL is `https://epic.gsfc.nasa.gov/archive/natural/<YYYY/MM/DD>/png/<image>.png`. Date components come from `date` field.
- **Mars rover `sol` vs `earth_date`.** Pass one or the other, never both. `sol` counts Martian days since landing; `earth_date` is calendar.
- **EONET timestamps are ISO strings, often timezone-naive.** Treat as UTC.
- **NEO close-approach distance comes in many units** — `astronomical`, `lunar`, `kilometers`, `miles`. Pick one consistently.
- **Date params accept either YYYY-MM-DD or null** in some endpoints (defaults to "today"). Empty string is NOT accepted; omit the param entirely if you want default.

## Source links

- Index of NASA APIs: https://api.nasa.gov/
- EONET: https://eonet.gsfc.nasa.gov/docs/v3
- NEO: https://api.nasa.gov/neo/?api_key=DEMO_KEY
- Mars rover: https://mars-photos.herokuapp.com/
