# geonames — populated places, elevation, timezones, country info

## What this source has

GeoNames is a global gazetteer: ~12M place names (cities, towns, villages, mountains, lakes, parks, admin divisions) with lat/lon, elevation, timezone, population (where known), feature class/code, and admin hierarchy (country → ADM1 → ADM2 → ADM3 → ADM4). Coverage is global but quality varies — Western countries are exhaustive; some developing countries have only major settlements.

Plus: SRTM3 elevation queries (90m global elevation grid), timezone-by-coord, country-info with ISO codes / capital / population / area / borders, and find-nearby-place lookups.

Use GeoNames for: "city ID for X", elevation at a coord, timezone for a coord, country fact lookups when you need GeoNames-specific identifiers. Pair with `nominatim`/`photon` for free-text geocoding (GeoNames search is exact-match leaning); pair with `worldtime` for current-time queries (GeoNames `timezone` returns offset, not current time).

## Auth

| | |
|---|---|
| Required | yes |
| Env var | `GEONAMES_USERNAME` |
| Account URL | https://www.geonames.org/login |
| Plan tier | free |

GeoNames uses a **username**, not a key — pass the username as `username` query param. Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`.

**Important post-signup step:** after registering, you must explicitly *enable web services* on the account page (Settings → "Free Web Services" → click to enable). Without this step, every query returns an authentication error. Email confirmation is also required before login.

## Limits

| | |
|---|---|
| Daily | 20,000 |
| Monthly | — |
| Rate | 1,000 req/hour per username |

Hitting the daily cap returns a JSON error rather than HTTP 429. Cap can be raised by donating, or by deploying your own server.

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Search places by name / feature | `q` (or `name`, `name_equals`) |
| `country_info` | Country-level metadata | none (use `country` to filter) |
| `timezone` | Timezone for a coord | `lat`, `lng` |
| `elevation` | SRTM3 elevation for a coord | `lat`, `lng` |
| `nearby` | Nearest place name to a coord | `lat`, `lng` |

## Worked examples

```bash
# Search "Paris" globally
python3 scripts/reach.py query geonames search '{
  "q": "Paris",
  "maxRows": 10,
  "featureClass": "P"
}'

# Country info for Japan
python3 scripts/reach.py query geonames country_info '{"country": "JP"}'

# Timezone at a coord
python3 scripts/reach.py query geonames timezone '{
  "lat": 48.8566,
  "lng": 2.3522
}'

# Elevation at a coord
python3 scripts/reach.py query geonames elevation '{
  "lat": 27.9881,
  "lng": 86.9250
}'

# Nearest populated place
python3 scripts/reach.py query geonames nearby '{
  "lat": 40.0,
  "lng": -75.0
}'
```

## Response shape

- `search`: `{totalResultsCount, geonames: [{geonameId, name, asciiName, alternateNames, latitude, longitude, fcl: "P", fclName: "city, village,...", fcode: "PPL", countryCode, countryName, adminCode1, adminName1, population, timezone: {gmtOffset, dstOffset, timeZoneId}, elevation}, ...]}`.
- `country_info`: `{geonames: [{countryCode, countryName, isoNumeric, isoAlpha3, fipsCode, capital, areaInSqKm, population, continent, currencyCode, languages, geonameId, north, south, east, west}]}`.
- `timezone`: `{countryCode, countryName, lat, lng, timezoneId, gmtOffset, rawOffset, dstOffset, time, sunrise, sunset}`.
- `elevation` (SRTM3): integer meters as the body, e.g., `8848`. Returns `-32768` for "no data" (commonly over open ocean).
- `nearby`: `{geonames: [{name, countryName, lat, lng, distance, ...}]}`.

## Pitfalls

- **Username, not API key.** Pass `username=<agent-handle>` (or whatever the registered username is); ignoring this returns auth errors.
- **Account must enable web services explicitly.** Confirmed email + clicking "Free Web Services" on the account page is required. Until then, every call fails with `the account is not yet activated`.
- **Daily cap returns JSON error**, not 429. Look for `status: {message: "the daily limit ..."}` in the response.
- **Feature class/code matters.** `featureClass: "P"` = populated places (cities, villages); `A` = administrative divisions; `H` = hydrographic features; `L` = parks/areas; `S` = spots/buildings; `T` = mountains/hills; `V` = forest, woods. Without filtering, results include all feature types.
- **`maxRows` default is 100, max is 1000.** Cap your asks.
- **Elevation `-32768`** means SRTM3 has no data — usually open ocean or polar. Fall back to other DEM endpoints (`gtopo30JSON`) for that case.
- **`name_equals` vs `q`.** `name_equals` is exact match; `q` does fuzzy searching across alternate names. Big result-quality difference.
- **Timezones as IDs.** Returned `timezoneId` is IANA (e.g., `America/New_York`); offsets are in hours (not seconds, unlike WorldTimeAPI).
- **`country_info`** without `country` returns ALL countries. Useful for one-shot country-table caching.

## Source links

- Web services overview: https://www.geonames.org/export/web-services.html
- Forum / activation help: https://forum.geonames.org/
- Free credits / commercial: https://www.geonames.org/commercial-webservices.html
