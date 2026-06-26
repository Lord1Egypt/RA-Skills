---
name: japan-seasons
description: Query Japanese seasonal data — cherry blossom forecasts, autumn foliage tracking, and festival search. Use when a user asks about sakura bloom dates, best time to visit Japan, autumn leaves, Japanese festivals, or any Japan travel timing question. Requires a free API key from https://jpseasons.dokos.dev/dashboard.
---

# Japan Seasons API

Query cherry blossom, autumn foliage, and festival data for Japan.

## Setup

Get a free API key at https://jpseasons.dokos.dev/dashboard (100 req/day).

Store the key as an environment variable or pass directly in headers.

## Base URL

```
https://jpseasons.dokos.dev
```

## Authentication

All requests need `X-API-Key` header:

```bash
curl -H "X-API-Key: YOUR_KEY" https://jpseasons.dokos.dev/v1/sakura/forecast?city=tokyo
```

## Endpoints

### Sakura (Cherry Blossom)

```bash
# Current bloom status (which cities have bloomed)
curl -H "X-API-Key: $KEY" "https://jpseasons.dokos.dev/v1/sakura/status"

# Bloom forecast (historical average-based)
curl -H "X-API-Key: $KEY" "https://jpseasons.dokos.dev/v1/sakura/forecast?city=tokyo"

# Historical records (1953-present)
curl -H "X-API-Key: $KEY" "https://jpseasons.dokos.dev/v1/sakura/historical?city=tokyo"

# All 57 observation stations
curl -H "X-API-Key: $KEY" "https://jpseasons.dokos.dev/v1/sakura/locations"

# Travel recommendation
curl -H "X-API-Key: $KEY" "https://jpseasons.dokos.dev/v1/sakura/recommend?city=kyoto&dates=2026-03-25/2026-04-05"
```

### Kouyou (Autumn Foliage)

Same pattern as sakura, under `/v1/kouyou/`:
- `status`, `forecast`, `historical?city=`, `locations`, `recommend?city=&dates=`

### Matsuri (Festivals)

```bash
# Search by region/month/category
curl -H "X-API-Key: $KEY" "https://jpseasons.dokos.dev/v1/matsuri/search?region=kansai&month=7"

# Upcoming festivals (next N days, default 30, max 90)
curl -H "X-API-Key: $KEY" "https://jpseasons.dokos.dev/v1/matsuri/upcoming?days=60"

# Festival detail (ID is kebab-case, e.g. gion-matsuri, aomori-nebuta)
curl -H "X-API-Key: $KEY" "https://jpseasons.dokos.dev/v1/matsuri/gion-matsuri"
```

## Error Handling

- `401` — Missing or invalid API key
- `404` — Unknown city ID or festival ID
- `429` — Rate limit exceeded (100/day free, 10K/day pro)
- `400` — Invalid parameters (bad date format, missing required param)

## Common City IDs

tokyo, osaka, kyoto, yokohama, nagoya, sapporo, fukuoka, sendai, hiroshima, kobe, naha, kagoshima, nagano, kanazawa, matsuyama

## Regions

hokkaido, tohoku, kanto, chubu, kansai, chugoku, shikoku, kyushu, okinawa

## Usage Pattern

1. Use `web_fetch` or `exec` (curl) to call endpoints
2. Parse JSON response
3. Present data to user in natural language

Example — answering "When should I visit Kyoto for cherry blossoms?":

```bash
curl -s -H "X-API-Key: $KEY" "https://jpseasons.dokos.dev/v1/sakura/recommend?city=kyoto&dates=2026-03-25/2026-04-10"
```

Response includes `likelihood`, `confidence`, `best_days`, and `alternatives`.
