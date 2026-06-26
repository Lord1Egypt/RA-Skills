---
name: hk-route
description: Smart public transport routing for Hong Kong with real-time bus ETAs. Queries Google Maps for transit alternatives, enriches bus legs with live arrival times, and ranks routes by effective total time.
triggers:
  - /hkroute
  - How do I get to
  - How to get from
  - transit route in Hong Kong
  - bus from
  - best way to get to
  - public transport Hong Kong
  - HK route
  - getting to .* from
metadata:
  { "openclaw": { "requires": { "env": ["GOOGLE_MAPS_API_KEY"], "bins": ["node"] }, "primaryEnv": "GOOGLE_MAPS_API_KEY", "homepage": "https://clawhub.ai/7ito/hkroute" } }
---

# HK Route — Hong Kong Transit Routing with Real-Time ETAs

## What this skill does

Finds the best public transport route in Hong Kong by combining Google Maps directions with real-time bus ETAs. Routes are ranked by **effective total time** (real-time wait + travel duration), not just schedule data.

## Required environment

| Requirement | Details |
|---|---|
| `GOOGLE_MAPS_API_KEY` | Google Maps API key with Directions API enabled |
| `node` >= 18 | Runtime for the bundled script |

## External endpoints

This skill makes network requests to:

| Endpoint | Purpose | Credentials |
|---|---|---|
| `maps.googleapis.com` (Google Directions API) | Transit route planning | `GOOGLE_MAPS_API_KEY` |
| HK government & operator APIs via [hk-bus-eta](https://github.com/hkbus/hk-bus-eta) (DATA.GOV.HK, KMB, CTB, etc.) | Real-time bus arrival times | None (public APIs) |

No other network calls are made. The ETA database is cached locally at `~/.cache/hk-route/etaDb.json` (refreshed every 24h).

## Source code

The bundled `scripts/hk-route.cjs` is built from readable TypeScript source at [github.com/7ito/hkroute](https://github.com/7ito/hkroute). Build command: `esbuild src/index.ts --bundle --platform=node --format=cjs`.

## How to invoke

```bash
node /path/to/skill/scripts/hk-route.cjs \
  --origin "<origin>" \
  --destination "<destination>"
```

> The `scripts/hk-route.cjs` bundle is self-contained — no `npm install` needed. Just `node` >= 18.

### Optional flags

- `--departure-time "<ISO 8601 datetime>"` — plan a future trip (e.g., `--departure-time "2026-03-26T08:00:00+08:00"`)

### Input formats

- **Coordinates**: `"22.2822,114.1875"` (lat,lng — no space after comma)
- **Place name**: `"Causeway Bay"`, `"Hong Kong Airport"`, `"Stanley Market"`
- Both origin and destination accept either format.

## Conversational flows

### One-shot (user provides both locations)

User: "How do I get from Causeway Bay to Stanley?"
→ Run the CLI with `--origin "Causeway Bay" --destination "Stanley"`, format the output.

### Multi-turn (e.g., WhatsApp via OpenClaw)

1. User sends `/hkroute`
2. Ask: "Where are you now? Send a location pin or type your location."
3. User sends a coordinate pin (e.g., `22.2822,114.1875`) or text (e.g., "Tin Hau MTR")
4. Ask: "Where do you want to go?"
5. User sends destination as text or coordinates.
6. Run the CLI, format the output.

If the user provides invalid input at any step, ask them to try again with a valid location.

### Implicit activation

Activate this skill when the user asks about getting somewhere in Hong Kong by public transport, even without using `/hkroute`. Look for intent like "how do I get to...", "best way to...", "bus from...", etc., in a Hong Kong context.

## Output format

The CLI outputs JSON to stdout. Format it for the user as follows:

### WhatsApp / messaging format template

```
🚌 **Routes from {origin} to {destination}**

⭐ **Route 1 (Recommended)** — {effective_total_min} min
{for each leg:}
  🚶 Walk {duration_seconds/60} min — {instructions}
  🚌 Bus {route_number} from {departure_stop} — **Next bus: {etas[0] formatted as relative time}** (then {etas[1]})
     {num_stops} stops → {arrival_stop}
  🚇 MTR {route_number} from {departure_stop}
     {num_stops} stops → {arrival_stop}
  ⛴️ Ferry ...
  🚊 Light Rail / Tram ...

📍 Route 2 — {effective_total_min} min
{same leg format}

📍 Route 3 — {effective_total_min} min
{same leg format}
```

### Formatting rules

- **Recommended route**: Mark with ⭐ and "(Recommended)"
- **Actionable leg**: The leg with `actionable: true` is the one that determines when the user needs to leave. Call it out prominently: **"Next bus in X min — leave now!"** or **"Next bus in X min — you have time."**
- **ETAs**: Format as relative time ("in 3 min", "in 12 min"). Show up to 2 ETAs per bus leg.
- **Walking legs**: Always show with duration. Use 🚶 emoji.
- **Transport emojis**: 🚌 bus, 🚇 MTR/subway, ⛴️ ferry, 🚊 light rail/tram, 🚶 walk
- **Bold**: Use bold for ETAs, route numbers, and the recommended route label.
- **Unavailable ETAs**: If `eta_source` is `"unavailable"`, show "ETA unavailable (scheduled: {departure_time})" instead of a real-time ETA.
- **Schedule-only**: If `eta_source` is `"schedule"`, show the scheduled departure time without a real-time label.

### Error handling

If the CLI returns `error: true`:
- `NO_TRANSIT_ROUTES`: Tell the user no transit routes were found. Suggest trying a different departure time or considering a taxi.
- `GOOGLE_API_ERROR`: Tell the user there was an issue fetching routes. Suggest trying again.
- `INVALID_INPUT`: Tell the user what was wrong with their input.
