---
name: notamify
description: Retrieve and analyze NOTAMs (Notices to Airmen) for airports worldwide using the Notamify Python SDK
homepage: https://github.com/skymerse/notamify-mcp
user-invocable: true
metadata: {"openclaw":{"emoji":"✈️","requires":{"env":["NOTAMIFY_TOKEN"],"anyBins":["python3","python"]},"primaryEnv":"NOTAMIFY_TOKEN"}}
---

# Notamify - Aviation NOTAM Intelligence

You help pilots, dispatchers, and aviation professionals retrieve and interpret NOTAMs (Notices to Airmen) for flight planning and situational awareness.

You query the Notamify API by writing and executing short Python scripts using the `notamify-sdk` package. The SDK reads the API token from the `NOTAMIFY_TOKEN` environment variable automatically — never hardcode tokens in scripts.

## Setup

Install the SDK (Python 3.10+):

```bash
pip install notamify-sdk
```

The SDK authenticates automatically via (in priority order):
1. `NOTAMIFY_TOKEN` environment variable
2. Path in `NOTAMIFY_CONFIG_FILE` environment variable
3. Default config at `~/.config/notamify/config.json`

API keys are generated at https://notamify.com/api-manager (requires Notamify Pro plan; 7-day free trial with 50 credits).

```python
from notamify_sdk import NotamifyClient

# Reads NOTAMIFY_TOKEN from environment automatically
client = NotamifyClient()

# Or load from config file
from notamify_sdk import ConfigStore
cfg = ConfigStore().load()
client = NotamifyClient(token=cfg.token)
```

## How to Query NOTAMs

When a user asks about NOTAMs, airport conditions, or flight planning:

1. **Identify the airports** — convert airport names to ICAO codes (e.g., JFK = KJFK, Heathrow = EGLL, Munich = EDDM, Warsaw Chopin = EPWA)
2. **Pick the right query type** — active, nearby, raw, historical, or briefing (see below)
3. **Write and execute a Python script** using `notamify-sdk`
4. **Present results clearly** — organize by severity/impact, highlight closures and hazards, provide flight planning recommendations
5. **Always remind the user** that NOTAM data is for informational purposes only — refer to official sources for operational decisions

## Query Types and Code Patterns

### Active NOTAMs (most common)

Use when the user asks about current or upcoming NOTAMs for specific airports. Returns auto-paginated iterator.

```python
from datetime import datetime, timedelta
from notamify_sdk import NotamifyClient, ActiveNotamsQuery

client = NotamifyClient()
query = ActiveNotamsQuery(
    location=["KJFK", "EGLL"],
    starts_at=datetime.utcnow(),
    ends_at=datetime.utcnow() + timedelta(hours=48),
    per_page=30
)

for notam in client.notams.active(query):
    interp = notam.interpretation
    print(f"[{notam.icao_code}] {notam.notam_number}")
    if interp:
        print(f"  Category: {interp.category}/{interp.subcategory}")
        print(f"  Summary: {interp.excerpt}")
        for elem in interp.affected_elements:
            print(f"  Affected: {elem.type} {elem.identifier} — {elem.effect}")
    else:
        print(f"  Message: {notam.message}")
    print()
```

**ActiveNotamsQuery parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `location` | list[str] | Yes | — | ICAO (4-char) or domestic (3-char) codes. Max 5 |
| `starts_at` | datetime | No | Current UTC | Cannot be >1 day before current UTC |
| `ends_at` | datetime | No | 365 days ahead | Must be later than `starts_at` |
| `excluded_classifications` | list[str] | No | — | Exclude: DOM, FDC, INTL, MIL |
| `notam_ids` | list[str] | No | — | Filter to specific NOTAM IDs |
| `always_include_est` | bool | No | true | Include estimated-time NOTAMs even if expired |
| `qcode` | list[str] | No | — | Filter by Q-codes (e.g., QMRLC, QWULW) |
| `category` | list[str] | No | — | AERODROME, AIRSPACE, NAVIGATION, COMMUNICATION, OPERATIONS, OBSTACLES, ADMINISTRATIVE, WEATHER, SAFETY, OTHER, ALL |
| `subcategory` | list[str] | No | — | Filter by interpretation subcategory |
| `affected_element` | list | No | — | Filter by effect (CLOSED, RESTRICTED, HAZARD, UNSERVICEABLE, WORK_IN_PROGRESS, CAUTION) and/or type (RUNWAY, TAXIWAY, APPROACH, NAVAID, AIRSPACE, APRON, LIGHTING, SERVICE, PROCEDURE, OTHER) |
| `page` | int | No | 1 | Start page |
| `per_page` | int | No | 10 | Results per page (max 30) |

### Nearby NOTAMs

Use when the user provides coordinates or asks about NOTAMs near a geographic point (e.g., along a flight route). Returns auto-paginated iterator.

```python
from notamify_sdk import NotamifyClient, NearbyNotamsQuery

client = NotamifyClient()
query = NearbyNotamsQuery(lat=51.4775, lon=-0.4614, radius_nm=15.0)

for notam in client.notams.nearby(query):
    print(f"{notam.notam_number}: {notam.interpretation.excerpt if notam.interpretation else notam.message}")
```

**NearbyNotamsQuery additional parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lat` | float | Yes | — | Latitude in decimal degrees (-90 to 90) |
| `lon` | float | Yes | — | Longitude in decimal degrees (-180 to 180) |
| `radius_nm` | float | No | 1 | Search radius in nautical miles (0.1–25) |

Also accepts `starts_at`, `ends_at`, `excluded_classifications`, `qcode`, `category`, `subcategory`, `affected_element`, `always_include_est`, `page`, `per_page`.

### Historical/Archive NOTAMs

Use when the user asks about NOTAMs that were active on a past date (incident investigation, compliance audits). Returns auto-paginated iterator.

```python
from datetime import date
from notamify_sdk import NotamifyClient, HistoricalNotamsQuery

client = NotamifyClient()
query = HistoricalNotamsQuery(
    location=["EDDM", "EGLL"],
    valid_at=date(2025, 9, 20)
)

for notam in client.notams.historical(query):
    print(f"{notam.notam_number} [{notam.icao_code}]: {notam.interpretation.excerpt if notam.interpretation else notam.message}")
```

**HistoricalNotamsQuery parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `valid_at` | date | Yes | — | Date to check (YYYY-MM-DD). Cannot be in the future |
| `location` | list[str] | No | — | ICAO/domestic codes. Max 5 |
| `notam_ids` | list[str] | No | — | Filter to specific NOTAM IDs |
| `category` | list[str] | No | — | Filter by interpretation category |
| `subcategory` | list[str] | No | — | Filter by subcategory |
| `affected_element` | list | No | — | Filter by effect and/or type |
| `always_include_est` | bool | No | true | Include estimated-time NOTAMs |
| `page` | int | No | 1 | Start page |
| `per_page` | int | No | 10 | Results per page (max 30) |

If none of the requested locations exist in the archive, the API returns 404 without charging credits.

### Flight Briefing (async)

Use when the user asks for a structured flight briefing between origin and destination airports. This is an async job — you submit a request and poll for completion.

```python
import time
from datetime import datetime, timedelta
from notamify_sdk import NotamifyClient, GenerateFlightBriefingRequest, LocationWithType

client = NotamifyClient()

job = client.create_briefing(GenerateFlightBriefingRequest(
    locations=[
        LocationWithType(
            location="EPWA",
            type="origin",
            starts_at=datetime.utcnow() + timedelta(hours=3),
            ends_at=datetime.utcnow() + timedelta(hours=3)
        ),
        LocationWithType(
            location="EGLL",
            type="destination",
            starts_at=datetime.utcnow() + timedelta(hours=6),
            ends_at=datetime.utcnow() + timedelta(hours=8)
        ),
    ],
    aircraft_type="B738",
    origin_runway="RWY11",
    destination_runway="RWY27L",
))

print(f"Briefing job submitted: {job.uuid}")

while True:
    status = client.get_briefing_status(job.uuid)
    if status.status == "completed":
        briefing = status.response
        break
    elif status.status == "failed":
        raise RuntimeError("Briefing generation failed")
    time.sleep(2)
```

**GenerateFlightBriefingRequest parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `locations` | list[LocationWithType] | Yes | Origin and destination airports with time windows |
| `aircraft_type` | str | Yes | ICAO aircraft type code (e.g., "B738", "A320") |
| `origin_runway` | str | Yes | Departure runway (e.g., "RWY11") |
| `destination_runway` | str | Yes | Arrival runway (e.g., "RWY27L") |

**LocationWithType fields:** `location` (ICAO code), `type` ("origin" or "destination"), `starts_at`, `ends_at`.

## NOTAM Response Object

All query endpoints return NOTAM objects with these fields:

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `notam_number` | str | No | Official NOTAM number |
| `icao_code` | str | Yes | ICAO airport code |
| `message` | str | No | Human-readable text |
| `icao_message` | str | Yes | ICAO-formatted text |
| `valid_from` | datetime | No | Validity start |
| `valid_to` | datetime | No | Validity end |
| `interpretation` | object | Yes | AI interpretation |

**Interpretation fields:**

| Field | Type | Description |
|-------|------|-------------|
| `description` | str | Detailed interpretation |
| `excerpt` | str | Brief summary |
| `category` | str | AERODROME, AIRSPACE, NAVIGATION, COMMUNICATION, OPERATIONS, OBSTACLES, ADMINISTRATIVE, WEATHER, SAFETY, OTHER |
| `subcategory` | str | Further classification |
| `affected_elements` | list | Elements with `type`, `identifier`, `effect`, `details` |
| `map_elements` | list | Spatial data with `element_type`, `coordinates`, `geojson`, vertical limits |
| `schedules` | list | Recurrence info with `rrule`, `duration_hrs`, `is_sunrise_sunset` |
| `schedule_description` | str | Human-readable schedule |

## Error Handling

The SDK raises typed exceptions:

```python
from notamify_sdk import APIError

try:
    for notam in client.notams.active(query):
        print(notam.notam_number)
except APIError as e:
    print(f"HTTP {e.status}: {e.message}")
```

| Exception | Condition |
|-----------|-----------|
| `APIError` | Non-2xx HTTP response or connection failure (`e.status`, `e.message`, `e.payload`) |
| `pydantic.ValidationError` | Invalid query parameters (e.g., `per_page > 30`) |

## Example Interactions

**"What are the current NOTAMs for JFK?"**
Query active NOTAMs for `["KJFK"]` with default 24h window.

**"I'm flying to Munich tomorrow. What should I know?"**
Query active NOTAMs for `["EDDM"]` with `ends_at` set to 48h ahead. Focus the summary on affected runways, taxiways, and approach procedures.

**"Show me NOTAMs for the London airports this weekend"**
Query active NOTAMs for `["EGLL", "EGLC", "EGSS", "EGGW", "EGKK"]` with explicit start/end dates.

**"What runways are closed at O'Hare and LAX?"**
Query active NOTAMs for `["KORD", "KLAX"]` with short time window. Filter output to RUNWAY type with CLOSED effect.

**"Any NOTAMs near 50.1N 22.0E within 15 nautical miles?"**
Use nearby query with `lat=50.1`, `lon=22.0`, `radius_nm=15`.

**"What NOTAMs were active at Frankfurt on September 20, 2025?"**
Use historical query with `location=["EDDF"]`, `valid_at=date(2025, 9, 20)`.

**"Generate a flight briefing from Warsaw to London, B738"**
Use `create_briefing` with origin EPWA and destination EGLL, poll for result.

## Limitations

- **Max 5 ICAO codes** per request
- **Start date** cannot be earlier than 1 day before current UTC (active/nearby)
- **End date** must be later than start date
- **Archive date** cannot be in the future
- **Nearby radius** 0.1–25 nautical miles
- **Pagination** max 30 items per page (SDK auto-paginates)
- All times are **UTC**

## Common ICAO Codes

| Airport | ICAO | City |
|---------|------|------|
| John F. Kennedy | KJFK | New York |
| Los Angeles Intl | KLAX | Los Angeles |
| O'Hare Intl | KORD | Chicago |
| Heathrow | EGLL | London |
| Frankfurt | EDDF | Frankfurt |
| Munich | EDDM | Munich |
| Charles de Gaulle | LFPG | Paris |
| Schiphol | EHAM | Amsterdam |
| Warsaw Chopin | EPWA | Warsaw |
| Dubai Intl | OMDB | Dubai |
| Changi | WSSS | Singapore |
| Haneda | RJTT | Tokyo |

## Links

- **API Docs:** https://skymerse.gitbook.io/notamify-api
- **SDK Docs:** https://skymerse.gitbook.io/notamify-api/sdk/python
- **API Manager:** https://notamify.com/api-manager
- **Source:** https://github.com/skymerse/notamify-mcp
- **PyPI:** `pip install notamify-sdk`
