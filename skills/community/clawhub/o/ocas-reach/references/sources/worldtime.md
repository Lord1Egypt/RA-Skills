# worldtime — current time + DST info by IANA timezone or IP

## What this source has

WorldTimeAPI returns the current time, UTC offset, DST status, day of year/week, week number, and the next DST transition for a given IANA timezone or for the caller's IP. ~400 IANA zones supported (the standard tzdata set). It's a lightweight time-only service — no historical times, no calendaring, no holidays.

Use WorldTimeAPI for: "what time is it in Tokyo right now", "is it DST in Sydney today", quick UTC offset lookup. Pair with `nager_holidays` when you also need holidays in a country; pair with `geonames` `timezone` action when you have lat/lon and need the IANA zone first.

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
| Rate | no documented cap; respond ~50ms per call |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `timezone` | Time info for an IANA zone | `area`, `location` |
| `ip` | Time info for caller's IP | none |

## Worked examples

```bash
# Time in Los Angeles
python3 scripts/reach.py query worldtime timezone '{
  "area": "America",
  "location": "Los_Angeles"
}'

# Time in Tokyo
python3 scripts/reach.py query worldtime timezone '{
  "area": "Asia",
  "location": "Tokyo"
}'

# Time at the caller's IP location
python3 scripts/reach.py query worldtime ip '{}'
```

## Response shape

```json
{
  "abbreviation": "PDT",
  "client_ip": "...",
  "datetime": "2026-04-26T13:42:11.123456-07:00",
  "day_of_week": 0,
  "day_of_year": 116,
  "dst": true,
  "dst_from": "2026-03-08T10:00:00+00:00",
  "dst_offset": 3600,
  "dst_until": "2026-11-01T09:00:00+00:00",
  "raw_offset": -28800,
  "timezone": "America/Los_Angeles",
  "unixtime": 1745700131,
  "utc_datetime": "2026-04-26T20:42:11.123456+00:00",
  "utc_offset": "-07:00",
  "week_number": 17
}
```

## Pitfalls

- **Path format is `area/location`** with underscores, exactly as IANA: `America/Los_Angeles`, not `America/Los Angeles` or `America/LosAngeles`.
- **Some zones have a third path segment** (`America/Indiana/Indianapolis`). The current connector path template only takes `area`/`location`; for nested zones you'll need the full path encoded into `location` (e.g. `Indiana/Indianapolis`).
- **`day_of_week` is 0-indexed Sunday-first.** 0=Sunday, 6=Saturday. ISO 8601 expects 1=Monday — convert if you're cross-referencing.
- **`raw_offset` excludes DST**, `dst_offset` is the additional seconds when active, total current offset is `raw_offset + (dst_offset if dst else 0)`.
- **`dst_from` / `dst_until`** is the current DST window. Outside DST these may show the *next* DST window, but check `dst` boolean first.
- **`ip` action.** Returns the time for the *caller's* IP (which on a server is the egress IP, not the user's). Don't use this for end-user timezone — pass an explicit zone.
- **Service occasionally goes down.** No SLA; cache aggressively if a service depends on it.

## Source links

- Docs: http://worldtimeapi.org/
- Source: https://github.com/worldtimeapi/worldtimeapi
- IANA tzdb: https://www.iana.org/time-zones
