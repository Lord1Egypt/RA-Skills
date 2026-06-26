# MBTA V3 API Reference

## Base URL
`https://api-v3.mbta.com`

## Authentication
- No key required for basic access (lower rate limits)
- Set `MBTA_API_KEY` env var for higher rate limits
- API key goes in query param: `?api_key=YOUR_KEY`
- Free keys available at: https://api-v3.mbta.com/

## Key Endpoints

### Stops — Search & Lookup
```
GET /stops
  filter[name]={name}           — search by name (partial match)
  filter[id]={id}               — get specific stop
  filter[route]={route_id}      — stops on a route
  filter[location_type]=0       — only platforms/stops (not parent stations)
```

**Location Types:**
- `0` — Stop / Platform
- `1` — Station (parent)
- `2` — Entrance / Exit
- `3` — Generic node
- `4` — Boarding area

**Common Stop IDs (parent stations):**
| Stop | ID |
|------|-----|
| South Station | `place-sstat` |
| North Station | `place-north` |
| Back Bay | `place-bbsta` |
| Downtown Crossing | `place-dwnxg` |
| Park Street | `place-pktrm` |
| Harvard | `place-harsq` |
| Kendall/MIT | `place-knncl` |
| Alewife | `place-alfcl` |
| Braintree | `place-brntn` |
| Forest Hills | `place-forhl` |
| Oak Grove | `place-ogmnl` |
| Wonderland | `place-wondl` |
| Bowdoin | `place-bomnl` |
| Airport | `place-aport` |

### Predictions — Next Departures
```
GET /predictions
  filter[stop]={stop_id}        — required: departures from stop
  filter[route]={route_id}      — optional: filter by route
  filter[direction_id]=0|1      — optional: filter direction
  sort=departure_time           — sort by departure (recommended)
  include=route,trip,stop       — include related resources
```

**Prediction Attributes:**
- `departure_time` — ISO 8601 with timezone offset
- `arrival_time` — ISO 8601 with timezone offset
- `direction_id` — 0 or 1
- `status` — "Boarding", "Approaching", etc.
- `stop_sequence` — order in trip

### Alerts — Service Disruptions
```
GET /alerts
  filter[stop]={stop_id}        — alerts affecting a stop
  filter[route]={route_id}      — alerts affecting a route
  filter[activity]=BOARD,EXIT,RIDE — filter by passenger activity
  filter[lifecycle]=NEW,ONGOING,ONGOING_UPCOMING — active alerts only
```

**Alert Severity (0–10):**
- 0–3: Informational
- 4–6: Warning / Caution
- 7–10: Severe disruption

**Common Effects:**
- `DELAY` — Service delayed
- `SUSPENSION` — Service suspended
- `STATION_CLOSURE` — Station closed
- `SHUTTLE` — Shuttle buses replacing train service
- `DETOUR` — Route detour
- `STOP_CLOSURE` — Specific stop closed

### Vehicles — Real-Time Positions
```
GET /vehicles
  filter[route]={route_id}      — vehicles on a route
  filter[label]={label}         — specific vehicle
  include=stop,trip             — include current stop and trip
```

**Vehicle Status:**
- `INCOMING_AT` — Approaching next stop
- `STOPPED_AT` — At a stop
- `IN_TRANSIT_TO` — Moving between stops

**Occupancy Status:**
- `MANY_SEATS_AVAILABLE`
- `FEW_SEATS_AVAILABLE`
- `STANDING_ROOM_ONLY`
- `CRUSHED_STANDING_ROOM_ONLY`
- `FULL`
- `NOT_ACCEPTING_PASSENGERS`

### Routes
```
GET /routes
  filter[type]=0|1|2|3|4        — filter by route type
  filter[stop]={stop_id}        — routes serving a stop
```

**Route Types:**
- `0` — Light Rail (Green Line, Mattapan Trolley)
- `1` — Heavy Rail / Subway (Red, Orange, Blue)
- `2` — Commuter Rail
- `3` — Bus
- `4` — Ferry

**Common Route IDs:**
| Route | ID |
|-------|-----|
| Red Line | `Red` |
| Orange Line | `Orange` |
| Blue Line | `Blue` |
| Green Line B | `Green-B` |
| Green Line C | `Green-C` |
| Green Line D | `Green-D` |
| Green Line E | `Green-E` |
| Commuter Rail (Providence) | `CR-Providence` |
| Commuter Rail (Framingham/Worcester) | `CR-Worcester` |
| Silver Line SL1 | `741` |
| Silver Line SL2 | `742` |

## API Response Format (JSON:API)
All responses follow the JSON:API spec:
```json
{
  "data": [...],         // array of resource objects
  "included": [...],     // sideloaded related resources (when using include=)
  "links": {...}         // pagination links
}
```

Each resource object:
```json
{
  "id": "...",
  "type": "prediction",
  "attributes": { ... },
  "relationships": {
    "route": { "data": { "id": "Red", "type": "routes" } },
    "stop":  { "data": { "id": "place-sstat", "type": "stops" } },
    "trip":  { "data": { "id": "...", "type": "trips" } }
  }
}
```

## Rate Limits
- **Without API key:** 20 requests/minute per IP
- **With API key:** 1000 requests/minute

## Useful Tips
- Use parent station IDs (e.g., `place-sstat`) for predictions — covers all platforms
- `sort=departure_time` puts soonest departures first
- `filter[activity]=BOARD` on alerts shows only alerts relevant to boarding passengers
- The `include=` parameter lets you get route/stop/trip names in one request
