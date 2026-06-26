---
name: planefilter
description: >
  Aviation flight lookup — query aircraft type, equipment changes, and
  confidence scoring for any flight number. Use when: looking up flight
  aircraft, checking equipment change, querying flight data, asking what plane
  a flight uses. Triggers on: flight lookup, aircraft type, what plane, 查機型,
  航班查詢, equipment change, plane filter, flight number, CI101, 飛機型號.
homepage: https://github.com/ImL1s/planefilter-openclaw-skill
metadata:
  openclaw:
    emoji: "✈️"
    primaryEnv: RAPIDAPI_KEY
    requires:
      bins: [node]
      env: [RAPIDAPI_KEY]
    install:
      - id: "node-brew"
        kind: "brew"
        formula: "node"
        bins: ["node"]
        label: "Install Node.js (brew)"
---

# PlaneFilter — Flight Aircraft Type Lookup

Look up aircraft type, equipment changes, and confidence scoring for any flight
by querying multiple aviation data sources (OpenSky, AeroDataBox, AirLabs) and
merging results with weighted confidence scoring.

## Prerequisites

### Required
- **Node.js** (v18+)
- **RAPIDAPI_KEY** — Subscribe to [AeroDataBox on RapidAPI](https://rapidapi.com/aedbx-aedbx/api/aerodatabox) (free Basic plan: 150 req/month)

### Optional (more data sources)
- **AIRLABS_KEY** — Get from [AirLabs](https://airlabs.co/signup) (free: 150 req/month)

## Commands

### 1. Search Flight

```bash
node {baseDir}/scripts/search_flight.js --flight=CI101 [--date=2026-03-22]
```

**Required env:** `RAPIDAPI_KEY`
**Optional env:** `AIRLABS_KEY` (adds another data source for higher confidence)

### 2. Health Check

```bash
node {baseDir}/scripts/health_check.js
```

Verifies all API keys are set and reachable. Shows which data sources are available.

## Output Format

`search_flight.js` outputs JSON to stdout:

```json
{
  "flightNumber": "CI101",
  "date": "2026-03-22",
  "airline": "China Airlines",
  "origin": "NRT",
  "destination": "TPE",
  "aircraftType": "A333",
  "registration": "B-18311",
  "confidence": 0.6,
  "equipmentChange": null,
  "typeDistribution": { "A333": 1 },
  "sources": ["aerodatabox"]
}
```

## Output Interpretation

When presenting results to the user, follow these rules:

| Field | How to Interpret |
|-------|-----------------|
| `confidence` ≥ 0.8 | High confidence — present the aircraft type directly |
| `confidence` 0.5–0.8 | Medium — mention "likely" or "most probable" |
| `confidence` < 0.5 | Low — warn that data is uncertain, show `typeDistribution` |
| `equipmentChange` not null | ⚠️ **Important** — Highlight this! The actual aircraft differs from the scheduled one. Show `from`, `to`, and `changeType` (upgrade/downgrade/lateral) |
| `typeDistribution` | Shows agreement across sources. Multiple entries = sources disagree |
| `sources` empty | No data found — suggest trying a different date |

**Note on aircraft type codes:** The script automatically normalizes model names (e.g. "Airbus A330-300" → "A333") and filters invalid typecodes. In rare cases, an unrecognized model name may pass through as-is.

## How It Works

1. **Parallel query** — Hits OpenSky (free, no key) + AeroDataBox (RapidAPI) + AirLabs (optional) simultaneously
2. **Confidence scoring** — Weighted votes from each source (AeroDataBox 0.9, OpenSky 0.7, AirLabs 0.6)
3. **Equipment change detection** — If scheduled aircraft ≠ actual aircraft, classifies as Upgrade/Downgrade/Lateral

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `RAPIDAPI_KEY not set` | Missing env var | `export RAPIDAPI_KEY=your_key` or set in `~/.openclaw/openclaw.json` |
| `403 from AeroDataBox` | Invalid or expired key | Check your RapidAPI subscription |
| `No flight data found` | Flight not in any database | Try with a different date or a major airline flight |
