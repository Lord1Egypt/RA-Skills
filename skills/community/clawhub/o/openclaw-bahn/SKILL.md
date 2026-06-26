---
name: bahn
description: A comprehensive suite of commands for tracking Deutsche Bahn trains
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    install:
      - kind: node
        package: db-vendo-client
      - kind: node
        package: devalue
      - kind: node
        package: fast-xml-parser
    emoji: "🚆"
    homepage: https://github.com/ableitung/openclaw-bahn
    os:
      - macos
      - linux
---

# Bahn

A comprehensive suite of commands for Deutsche Bahn trains - live departures, delay tracking, Baustellen/disruption alerts, journey planning, connection parsing, historical delay stats, and delay predictions. No API keys needed.

## Flags

| Flag | What it does | When to use |
|------|-------------|-------------|
| `--predict` | Runs the exponential delay model (transferProb, zugbindungProb) | User asks about probability of catching a transfer or Zugbindung being lifted |
| `--stats` | Fetches historical bahn.expert aggregate data per train | User asks about historical delay patterns for a specific train |

## Examples
```bash
# Search for a train station
node scripts/bahn.mjs --search "Wuppertal" [--json]

# Find latest departures from a given station
node scripts/bahn.mjs --departures "Wuppertal Hbf" [--results N] [--json]

# Default: Parse and show live data
echo '<raw Navigator share text>' | node scripts/bahn.mjs --parse [--json]

# With prediction model (transferProb, zugbindungProb)
echo '<text>' | node scripts/bahn.mjs --parse --predict [--json]

# With historical stats from bahn.expert
node scripts/bahn.mjs --parse connections/active.json --stats [--json]

# Both
node scripts/bahn.mjs --parse connections/active.json --predict --stats [--json]

# Find a given journey in timetable
node scripts/bahn.mjs --journey "From" "To" [--date YYYY-MM-DD] [--time HH:MM] [--results N] [--days N] [--json]

# Get current delays
node scripts/bahn.mjs --live --current-leg N [--delay M] connections/active.json [--json]

# Find a specific train by number and category (example: ICE 933)
node scripts/bahn.mjs --category CAT --train NUM [--date YYYY-MM-DD] [--json]
```

## File Layout

```
scripts/
├── bahn.mjs                    ← thin CLI dispatcher (~60 lines)
├── lib/
│   ├── commands/             ← one module per mode
│   │   ├── search.mjs        ← --search: station lookup
│   │   ├── departures.mjs    ← --departures: live departure board
│   │   ├── parse.mjs         ← --parse: connection parsing + enrichment
│   │   ├── journey.mjs       ← --journey: route search
│   │   ├── live.mjs          ← --live: real-time transfer check
│   │   └── track.mjs         ← --track: train tracking
│   ├── helpers.mjs           ← shared helpers (envelope, transfers, assessment)
│   ├── data.mjs              ← source router (IRIS/Vendo/bahn.expert)
│   ├── predict.mjs           ← probability model (opt-in via --predict)
│   ├── stats.mjs             ← delay profiles + historical stats (opt-in via --stats)
│   ├── parse.mjs             ← connection text parser
│   ├── format.mjs            ← output formatter
│   ├── messageLookup.mjs     ← IRIS delay code lookup
│   └── sources/
│       ├── bahn-expert.mjs   ← bahn.expert tRPC source
│       ├── iris.mjs          ← IRIS XML source
│       └── vendo.mjs         ← db-vendo-client source
```

## JSON Envelope

All modes support `--json`:

```json
{
  "mode": "string",
  "timestamp": "ISO8601",
  "connection": { "date", "from", "to", "legs", "transfers" },
  "journeyOptions": { "from", "to", "date", "options" },
  "departures": { "station", "entries" },
  "stations": { "query", "results" },
  "liveStatus": { "currentLeg", "nextTransfer", "zugbindungStatus", "recommendation", "remainingTransfers" },
  "trackStatus": { "train", "from", "to", "stops", "maxDelay", "zugbindungStatus" },
  "assessment": null,
  "errors": [],
  "warnings": []
}
```

The `assessment` field is only populated when `--predict` is used. Without it, `assessment` is `null`.

## Prediction Model (predict.mjs) — opt-in only

Exponential delay distributions per train category. Only loaded when `--predict` is passed.

| Category | Mean delay | Cancel rate |
|----------|-----------|-------------|
| ICE | 5.0min | 5.5% |
| IC/EC | 4.0min | 4.0% |
| RE | 2.5min | 2.0% |
| RB | 2.0min | 1.5% |
| S | 1.5min | 1.0% |
| Bus | 3.0min | 2.0% |

P(Zugbindung triggered) per leg = exp(-20/mean).
Overall P(Zugbindung) = 1 - ∏(1 - P(leg_i ≥ 20min)).

## Coverage

Long-distance (ICE/IC/EC), regional (RE/RB), S-Bahn, buses, and international trains to neighboring countries.


Report issues and legal information here: https://github.com/ableitung/openclaw-bahn