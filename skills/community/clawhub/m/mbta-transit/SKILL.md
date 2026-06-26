# MBTA Transit Skill

Query real-time MBTA (Massachusetts Bay Transportation Authority) transit data: next departures, service alerts, and live vehicle positions for subway, bus, commuter rail, and ferry.

## What This Skill Does

- **Next departures** — Get upcoming departures from any MBTA stop, with route, destination, and predicted time
- **Service alerts** — Check active disruptions, delays, or closures for a stop or route
- **Vehicle positions** — See where trains/buses are right now on a given route
- **Stop search** — Find stop IDs by name
- **Route listing** — Browse all MBTA routes by type

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MBTA_API_KEY` | Optional | Higher rate limits (1000 req/min vs 20). Free at https://api-v3.mbta.com/ |

## Script: `scripts/mbta.py`

### Commands

#### `stops <search_term>` — Find stops by name
```bash
python3 scripts/mbta.py stops "South Station"
python3 scripts/mbta.py stops "Harvard"
python3 scripts/mbta.py stops "Kenmore"
```
Returns: Stop IDs, names, platform info, city.

#### `departures <stop_id_or_name> [limit]` — Next departures
```bash
python3 scripts/mbta.py departures place-sstat 10
python3 scripts/mbta.py departures "Back Bay" 5
python3 scripts/mbta.py departures place-north
```
Returns: Departure times, route names, destinations.

#### `alerts [--stop <id>] [--route <id>]` — Active service alerts
```bash
python3 scripts/mbta.py alerts --route Red
python3 scripts/mbta.py alerts --stop place-sstat
python3 scripts/mbta.py alerts --route Orange --stop place-dwnxg
python3 scripts/mbta.py alerts   # all active alerts
```
Returns: Alert header, effect type, severity, description, last updated.

#### `vehicles <route_id>` — Live vehicle positions
```bash
python3 scripts/mbta.py vehicles Red
python3 scripts/mbta.py vehicles Orange
python3 scripts/mbta.py vehicles "Green-D"
python3 scripts/mbta.py vehicles 1   # Route 1 bus
```
Returns: Vehicle label, current stop/status, heading, occupancy, last update time.

#### `routes [--type <0-4>]` — List routes
```bash
python3 scripts/mbta.py routes
python3 scripts/mbta.py routes --type 1   # Subway/Heavy Rail
python3 scripts/mbta.py routes --type 2   # Commuter Rail
python3 scripts/mbta.py routes --type 3   # Bus
```
Route types: 0=Light Rail, 1=Heavy Rail, 2=Commuter Rail, 3=Bus, 4=Ferry

## Natural Language Requests This Handles

- "When's the next Red Line train from South Station?"
  → `departures place-sstat 5` (filter mentally to Red Line)

- "Are there any delays on the Orange Line?"
  → `alerts --route Orange`

- "What's the next commuter rail departure from Back Bay?"
  → `departures place-bbsta 10`

- "Where are the Green Line D trains right now?"
  → `vehicles Green-D`

- "Find the stop ID for Kenmore Station"
  → `stops Kenmore`

- "Any service alerts near Downtown Crossing?"
  → `alerts --stop place-dwnxg`

- "How crowded is the Blue Line?"
  → `vehicles Blue` (shows occupancy when available)

## Common Stop IDs (Quick Reference)

| Station | Stop ID |
|---------|---------|
| South Station | `place-sstat` |
| North Station | `place-north` |
| Back Bay | `place-bbsta` |
| Downtown Crossing | `place-dwnxg` |
| Park Street | `place-pktrm` |
| Harvard | `place-harsq` |
| Kendall/MIT | `place-knncl` |
| Alewife | `place-alfcl` |
| Airport | `place-aport` |
| Kenmore | `place-kencl` |
| Copley | `place-coecl` |
| Boylston | `place-boyls` |

## Common Route IDs

| Route | ID |
|-------|-----|
| Red Line | `Red` |
| Orange Line | `Orange` |
| Blue Line | `Blue` |
| Green-B/C/D/E | `Green-B`, `Green-C`, `Green-D`, `Green-E` |
| Silver Line 1 | `741` |
| Silver Line 2 | `742` |

## Tips for the AI Agent

1. **Always use stop IDs over names** when you have them — more reliable
2. **Search for stop IDs first** if you only have a station name: `stops "Name"`
3. **Parent station IDs** (e.g., `place-sstat`) cover all platforms — use these for departures
4. **Predictions may be empty** at night or when service isn't running
5. **Alerts with no filter** returns ALL system alerts — often noisy; filter by route or stop when possible
6. **Vehicle tracking** isn't available for all routes (some buses don't report positions)
7. For **commuter rail departures**, stop IDs are usually the station name like `Back Bay`

## References

See `references/API.md` for full MBTA V3 API documentation, including all filter parameters, response formats, and complete lists of stop/route IDs.
