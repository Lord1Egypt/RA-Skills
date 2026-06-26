# OVERCLOCK QA Mission

You are testing the OVERCLOCK AI Battle Arena. Use these APIs:

**Base URL:** `https://overclock-903028338458.us-central1.run.app`

## APIs

```
GET  /api/game                    → Game state (agents, crystals)
GET  /api/game/strategy           → Current strategy
POST /api/game/battle             → Execute battle (3/min limit, wait 25s)
POST /api/game/strategy           → Change strategy
POST /api/overclock/purchase      → Buy card pack
GET  /api/logs                    → Error logs
```

## Your Tasks

### 1. Explore (GET all endpoints, document what you see)
### 2. Play (change strategy → battle → repeat 3x, wait 25s between battles)

Strategy body example:
```json
{"battleStance":"aggressive","focusTarget":"lowest_hp","skillUsage":"asap"}
```

Purchase body example:
```json
{"packType":"basic","source":"acp"}
```

### 3. Find Bugs (try invalid packType, check /api/logs)
### 4. Write Report (intro + play log + bugs + improvements)
