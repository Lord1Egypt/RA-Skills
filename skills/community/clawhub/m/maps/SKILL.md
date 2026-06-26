---
name: Maps
slug: maps
version: 1.0.0
homepage: https://clawic.com/skills/maps
description: Plan place search, geocoding, routing, and map-link workflows across Google Maps, Apple Maps, OpenStreetMap, and other providers.
changelog: Initial release with provider selection rules, normalized map workflows, and safer route and link execution patterns.
metadata: {"clawdbot":{"emoji":"MAP","requires":{"bins":[],"config":["~/maps/"]},"os":["linux","darwin","win32"],"configPaths":["~/maps/"]}}
---

## When to Use

User needs place search, forward geocoding, reverse geocoding, routing, travel-time estimates, static map links, or provider selection for a maps workflow.
Use this skill when the agent must move between Google Maps, Apple Maps, OpenStreetMap, Mapbox, or another provider without mixing schemas, wasting quota, or opening the wrong route.

## Architecture

Memory lives in `~/maps/`. If `~/maps/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/maps/
|-- memory.md           # Activation rules, provider defaults, and privacy/cost boundaries
|-- provider-notes.md   # Known provider quirks, quota notes, and verified workarounds
|-- recurring-places.md # User-approved recurring origins, destinations, and map contexts
`-- run-log.md          # Optional notes on failures, ambiguous matches, and fixes
```

## Quick Reference

Load only the file needed for the current map task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema and status model | `memory-template.md` |
| Provider choice by task and constraint | `provider-matrix.md` |
| Canonical schema and coordinate normalization | `normalization-guide.md` |
| Search, route, and launch workflows | `execution-patterns.md` |
| Cost controls and fallback logic | `cost-controls.md` |
| Common failures and recovery steps | `troubleshooting.md` |

## Requirements

- No credentials required for provider selection, normalization, and map-link planning.
- Live Google Maps, Mapbox, HERE, or other paid API calls need user-approved credentials.
- Apple Maps app launching is macOS-specific, but Apple Maps link generation works anywhere a browser can open `https://maps.apple.com`.
- Confirm before sending sensitive origin, destination, or itinerary data to a live provider.

## Coverage

This skill is designed for mixed map work that usually fails when an agent treats every provider as interchangeable:
- place search and place-detail workflows
- forward and reverse geocoding
- route and matrix calculations
- static map or shareable map-link generation
- provider fallback when quota, privacy, or coverage changes the right choice

## Core Rules

### 1. Separate structured data from launch actions
- Decide first whether the user wants machine-readable output, an interactive map, or both.
- Use APIs for structured records and calculations.
- Use app or browser links only when the user wants to open, preview, or share a map.

### 2. Normalize every provider before comparing results
- Keep coordinates internally as decimal `lat` and `lng`, then serialize per provider.
- Track result type, confidence, place status, provider ID, timezone, and distance units before merging outputs.
- Use `normalization-guide.md` whenever provider schemas disagree.

### 3. Bound ambiguous searches with context and confidence
- Add city, region, postal code, country, or nearby coordinates before calling search or geocode endpoints.
- If top candidates disagree on locality or type, ask a disambiguation question instead of guessing.
- Do not treat the first geocode result as truth when the provider reports approximate or partial matches.

### 4. Route travel distance through a route engine
- Haversine is only for radius filters, rough proximity checks, and clustering.
- For ETA, driving distance, cycling, transit, or waypoint order, use a routing or matrix engine.
- Explicitly set travel mode and units before comparing providers.

### 5. Choose the provider by task, cost, and privacy
- Use `provider-matrix.md` to pick the cheapest provider that still meets the accuracy and policy needs of the task.
- Default to Apple Maps for app-launch workflows, Google for broad place detail coverage, and the OpenStreetMap stack for low-cost open-data fallback.
- Switch providers only when the delta is clear: richer data, safer privacy posture, better coverage, or lower cost.

### 6. Preview high-impact executions
- Show final route mode, origin, destination, and provider before opening routes or sharing links.
- For multiple links, repeated launches, or route changes, require explicit confirmation.
- If a link contains private notes or sensitive addresses, confirm again before execution.

### 7. Degrade gracefully when providers fail
- Fall back from premium APIs to open-data providers when the result quality remains acceptable.
- Cache canonicalized queries and provider IDs so repeated geocodes do not burn quota.
- If no trustworthy fallback exists, stop and explain whether the blocker is quota, precision, coverage, or privacy.

## Common Traps

- Swapping `lat,lng` and `lng,lat` -> routes jump continents or geofences miss targets.
- Truncating coordinates below 5-6 decimals -> rooftop and curbside results drift by tens to hundreds of meters.
- Treating the first geocode result as final -> duplicate street names and chain locations cause silent errors.
- Using straight-line distance for delivery or commute promises -> travel times can be off by 2-5x.
- Mixing launch URLs with API schemas -> a valid Apple Maps link does not imply a complete structured place record.
- Ignoring place status and confidence -> closed businesses and approximate addresses leak into downstream logic.
- Repeating the same paid lookup -> avoidable quota burn and inconsistent results when provider ordering changes.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://maps.googleapis.com | addresses, coordinates, place queries, route parameters | Google geocoding, places, routes, and static maps |
| https://maps.apple.com | search text, coordinates, and route parameters | Apple Maps links and app or browser launch |
| https://nominatim.openstreetmap.org | address text or reverse-geocode coordinates | OpenStreetMap geocoding fallback |
| https://router.project-osrm.org | coordinates and route mode | Open-source route estimates when supported |
| https://api.mapbox.com | queries, coordinates, and route parameters | Alternative geocoding, routing, and static maps |

No other data should be sent externally unless the user approves another provider.

## Security & Privacy

Data that may leave your machine:
- address queries
- coordinates
- route origin and destination
- place-search text
- optional static-map parameters

Data that stays local:
- notes in `~/maps/`
- provider preferences and fallback rules
- user-approved recurring contexts
- failure logs and verified fixes

This skill does NOT:
- store API keys in local notes
- guess precise destinations from vague requests
- treat a launch URL as proof of data accuracy
- modify its own `SKILL.md`

## Trust

This skill can send addresses, coordinates, and route parameters to the map provider selected for the task.
Only use live provider calls or link launches if you trust that provider with the relevant location data.

## Scope

This skill ONLY:
- selects providers and execution modes for map work
- normalizes place, geocode, route, and link workflows
- prepares safe request plans, links, or structured summaries

This skill NEVER:
- invent place data, ETAs, or coverage claims
- scrape undeclared providers behind anti-bot flows
- share map links externally without approval
- persist sensitive location history without telling the user first

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `apple-maps` - Open Apple Maps search and route flows on macOS with local command automation.
- `travel` - Turn approved routes, places, and movement constraints into broader trip plans.
- `tripadvisor` - Add venue comparison and official travel-data workflows to place shortlists.
- `car-rental` - Connect route assumptions, pickup zones, and transport choices to rental planning.

## Feedback

- If useful: `clawhub star maps`
- Stay updated: `clawhub sync`
