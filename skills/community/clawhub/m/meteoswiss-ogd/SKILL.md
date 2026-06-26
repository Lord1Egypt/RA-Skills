---
name: meteoswiss-ogd
description: >-
  Use when the user asks about Swiss weather, MeteoSwiss data, or Swiss weather
  forecasts and no MCP server is available. Covers current weather, forecasts,
  pollen, and station discovery via direct HTTP. No API key required.
globs: []
license: CC0-1.0
metadata:
  author: eins78
  repo: https://github.com/eins78/meteoswiss-llm-tools
  version: 1.0.0-rc.1
compatibility: claude-code, cursor
---

# MeteoSwiss Open Data

Access Swiss weather data from MeteoSwiss Open Government Data. Free, no API key. All data from `data.geo.admin.ch`. CSVs use **semicolon** (`;`) delimiters. Metadata CSVs are Latin1 — pipe through `iconv -f latin1 -t utf-8`.

## Quick Reference

| Data | URL / Method | Updates |
|------|-------------|---------|
| Current weather | `https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv` | 10 min |
| Station metadata | STAC `ch.meteoschweiz.ogd-smn` → asset `ogd-smn_meta_stations.csv` (Latin1) | Daily |
| Forecast metadata | STAC `ch.meteoschweiz.ogd-local-forecasting` → asset containing `meta_point.csv` (Latin1) | Daily |
| Forecast data | STAC items in `ch.meteoschweiz.ogd-local-forecasting` → parameter CSVs | Hourly |
| Pollen data | `https://data.geo.admin.ch/ch.meteoschweiz.ogd-pollen/{abbr}/ogd-pollen_{abbr}_d_now.csv` (Latin1) | Daily |

STAC API base: `https://data.geo.admin.ch/api/stac/v1`

## 1. Get Current Weather

```bash
# Get weather for Zurich (station SMA) — key columns: tre200s0 (temp °C),
# ure200s0 (humidity %), rre150z0 (precip mm), fu3010z0 (wind km/h)
curl -s 'https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv' \
  | awk -F';' 'NR==1 || $1=="SMA"'
```

Full parameter list in `${CLAUDE_SKILL_DIR}/REFERENCE.md`. Missing values appear as empty fields or `-`. Timestamps are `YYYYMMDDHHmm` in UTC.

## 2. Find Stations

```bash
# Search weather stations by name (Latin1 encoded)
curl -s 'https://data.geo.admin.ch/ch.meteoschweiz.ogd-smn/ogd-smn_meta_stations.csv' \
  | iconv -f latin1 -t utf-8 \
  | awk -F';' 'NR==1 || tolower($0) ~ /zurich/'
```

Columns: `station_abbr`, `station_name`, `station_canton`, `station_height_masl`, `station_coordinates_wgs84_lat`, `station_coordinates_wgs84_lon`.

```bash
# Search forecast locations (~6000 points: stations, postal codes, mountains)
# NOTE: Asset key has a known typo "forcasting" — always get URL from STAC
META_URL=$(curl -s 'https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-local-forecasting' \
  | jq -r '[.assets | to_entries[] | select(.key | contains("meta_point")) | .value.href] | first')
curl -s "$META_URL" | iconv -f latin1 -t utf-8 \
  | awk -F';' 'NR==1 || $3 ~ /8001/'  # search by postal code
```

Point columns: `point_id`, `point_type_id` (1=station, 2=postal_code, 3=mountain), `postal_code`, `station_abbr`, `point_name`.

## 3. Get Forecasts

Two steps: get the latest STAC item, then download parameter CSVs.

```bash
# Step 1: Get latest forecast item
ITEM=$(curl -s 'https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-local-forecasting/items?limit=10' \
  | jq -r '[.features[].id] | sort | reverse | .[0]')

# Step 2: Get a parameter CSV (e.g., daily max temperature for Zurich station, point_id=48)
ASSET_URL=$(curl -s "https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-local-forecasting/items/$ITEM" \
  | jq -r '[.assets | to_entries[] | select(.key | contains("tre200dx"))] | sort_by(.key) | last | .value.href')
curl -s "$ASSET_URL" | awk -F';' 'NR==1 || $1=="48"'
```

**Station forecasts** (point_type_id=1) have daily params: `tre200dx` (max temp), `tre200dn` (min temp), `rka150d0` (precip), `jp2000d0` (weather icon). **Postal codes/mountains** (type 2,3) have hourly params: `tre200h0`, `rre150h0`, `jww003i0` — aggregate to daily by grouping on first 8 timestamp chars. Common point_ids: Zurich=48, Bern=29, Geneva=53.

## 4. Get Pollen Data

```bash
# Stations: BAS, BER, BUC, DAV, GEN, LAU, LOG, LUG, LUZ, MUN, NEU, VIS, ZUE
# Use lowercase in URLs
curl -s 'https://data.geo.admin.ch/ch.meteoschweiz.ogd-pollen/zue/ogd-pollen_zue_d_now.csv' \
  | iconv -f latin1 -t utf-8 \
  | awk -F';' 'NR==1{print} {last=$0} END{print last}'
```

Columns: `station_abbr`, `Date`, then pollen types (`BIR`=birch, `GRA`=grass, etc.) in particles/m³.

## Error Handling

- **Station not found**: Check metadata CSV (Section 2) for valid abbreviations
- **Empty data**: Station may be offline — try a nearby station
- **403/404 on pollen**: Verify abbreviation is lowercase and is a pollen station (~13 total)
- **Garbled text**: You're reading Latin1 as UTF-8 — add `iconv -f latin1 -t utf-8`

## Bundled Scripts

Token-efficient CLI tools that output structured key=value pairs. Use these instead of raw curl when available — they handle encoding, error checking, and output parsing.

```bash
${CLAUDE_SKILL_DIR}/scripts/current-weather.sh SMA          # current weather for Zurich
${CLAUDE_SKILL_DIR}/scripts/search-stations.sh zurich        # find weather stations
${CLAUDE_SKILL_DIR}/scripts/search-forecast-points.sh 8001   # find forecast point_id by postal code
${CLAUDE_SKILL_DIR}/scripts/forecast.sh 48                   # forecast for Zurich (point_id=48)
${CLAUDE_SKILL_DIR}/scripts/pollen.sh ZUE                    # pollen data for Zurich
```

All scripts accept `--help` for usage details. Requires: `curl`, `awk`, `iconv`. Forecast also needs `jq`.

## MCP Server Alternative

For complex queries (fuzzy search, geocoding, structured JSON), use the MCP server: `claude mcp add meteoswiss https://meteoswiss-mcp.ars.is/mcp`

## Full Reference

See `${CLAUDE_SKILL_DIR}/REFERENCE.md` for all parameters, weather icon codes, and STAC collections.
