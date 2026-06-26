---
name: idfm-journey
description: Query Île-de-France Mobilités (IDFM) PRIM/Navitia for Paris + suburbs public transport (Île-de-France) — place resolution, journey planning, and disruptions/incident checks. Use when asked to find routes in Île-de-France (e.g., "itinéraire de X à Y"), resolve station/stop ids, or check RER/metro line disruptions, and you have an IDFM PRIM API key.
version: 0.1.6
author: anthonymq
triggers:
  - "Itinéraire de {origine} à {destination}"
  - "Route from {origin} to {destination} in Paris / Île-de-France"
  - "Check RER/metro disruptions" 
  - "Incidents on line {line}"
---

# IDFM Journey (PRIM/Navitia)

Use the bundled script to call PRIM/Navitia endpoints without extra dependencies.

## Metadata

- **Author:** anthonymq
- **Version:** 0.1.6

## Trigger phrases (examples)

- "Itinéraire de {origine} à {destination}"
- "Route from {origin} to {destination} in Paris / Île-de-France"
- "Check RER/metro disruptions" / "incidents on line {line}"

## Prereqs

- Set `IDFM_PRIM_API_KEY` in the environment before running.

### Generating an API Key

To obtain an IDFM PRIM API key:
1. Visit [https://prim.iledefrance-mobilites.fr/](https://prim.iledefrance-mobilites.fr/)
2. Create an account or log in
3. Navigate to "Espace développeur" or the developer portal
4. Subscribe to the "Navitia" API
5. Your API key will be generated and displayed in your dashboard
6. Export it in your environment: `export IDFM_PRIM_API_KEY="your-key-here"`

## Quick commands

Run from anywhere (path is inside the skill folder):

- Resolve places (best match + list):
  - `python3 scripts/idfm.py places "Ivry-sur-Seine" --count 5`

- Journeys (free-text from/to; resolves place ids first):
  - `python3 scripts/idfm.py journeys --from "Ivry-sur-Seine" --to "Boulainvilliers" --count 3`

- Incidents / disruptions (by line id or filter):
  - `python3 scripts/idfm.py incidents --line-id line:IDFM:C01727`
  - `python3 scripts/idfm.py incidents --filter 'disruption.status=active'`

Add `--json` to print raw API output.

## Notes

- If place resolution is ambiguous, increase `--count` and choose the right `stop_area` id.
- For API details and examples, read: `references/idfm-prim.md`.
