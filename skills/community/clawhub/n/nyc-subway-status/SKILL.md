---
name: nyc-subway
description: Check real-time NYC subway arrivals, track trains, and find stations. Use when user asks about subway times, train status, MTA arrivals, or NYC transit.
---

# NYC Subway Status

Real-time NYC subway arrival times. No API key required.

## Setup

Before making any API calls, fetch the full API reference:

```
GET https://nyc-subway-status.com/llms.txt
```

This returns a plain-text guide with all endpoints, slug formats, response schemas, and tips. Read it once per session to understand the API surface.

**Base URL:** `https://nyc-subway-status.com`

## Core Workflow

**Always search first — never guess station or route slugs.**

1. Search: `GET /api/search?q={query}` to find station slugs and route slugs
2. Use the returned slugs to call the appropriate endpoint

## Use Cases

### 1. Next train at a station

User asks: "when is the next Q at 72nd st"

```
GET /api/search?q=72+st+q
```

The response includes an `arrivals_url` when both station and route match. Use it:

```
GET /api/stops/72-st-n-q-r/lines/q
```

Present the `minutes_away` values from `arrivals.uptown` and `arrivals.downtown`. Example output:

> **Q at 72 St (N/Q/R)**
> Uptown: 3 min, 8 min, 15 min
> Downtown: 1 min, 6 min, 12 min

### 2. All arrivals at a station

User asks: "what trains are coming to Union Square"

```
GET /api/search?q=union+square
GET /api/stops/14-st-union-sq
```

Use the `by_route` field to group arrivals by line. Show each route with its next few trains in both directions.

### 3. Is a line running?

User asks: "is the G train running"

```
GET /api/lines/g
```

Returns next arrival at every station on the route. If most stations have `next_uptown` or `next_downtown` values, the line is running. If many are `null`, service may be disrupted. Summarize the overall status.

### 4. Track a specific train

User asks for details on a specific trip (usually after seeing a trip_id from an arrivals response):

```
GET /api/trips/{tripId}?route={routeSlug}
```

Returns every stop on the trip with `status` ("passed" or "upcoming") and `minutes_away`. Show the train's current position and upcoming stops.

### 5. Find a station

User asks: "find subway stations near Times Square"

```
GET /api/search?q=times+square
```

List matching stations with their routes. Offer to check arrivals at any of them.

### 6. Compare routes at a station

User asks: "should I take the N or Q at 72nd"

```
GET /api/stops/72-st-n-q-r
```

Use the `by_route` field to compare the next arrivals for each route in the user's direction. Recommend the sooner train.

## Response Format

All responses follow this envelope:

```json
{
  "ok": true,
  "data": { ... },
  "_meta": { "timestamp": "...", "endpoint": "...", "realtime": true }
}
```

Errors return `"ok": false` with an `error` object containing `code` and `message`.

## Key Details

- **Directions:** "uptown" = northbound, "downtown" = southbound
- **minutes_away** is pre-computed server-side — no client math needed
- **Arrival times** include both Unix timestamps and ISO 8601 strings
- **Route slugs** are lowercase: `a`, `q`, `7`, `si`, `gs`
- **Station slugs** are hyphenated lowercase: `14-st-union-sq`, `times-sq-42-st`

## MCP Server (Alternative)

For agents that support Model Context Protocol, connect directly:

```json
{
  "mcpServers": {
    "nyc-subway": { "url": "https://nyc-subway-status.com/mcp" }
  }
}
```

Tools: `search_subway`, `get_arrivals`, `get_station_arrivals`, `list_stations`, `list_routes`, `get_trip`
