# Katzilla — source reference for ocas-reach

## API
- Base: `https://api.katzilla.dev`
- Auth: `X-API-Key` header
- Env: `KZ_KEY`

## Commands
| Command | Args | Description |
|---------|------|-------------|
| `agents` | — | List all 27 agents with handles + action counts |
| `query <agent> <action> [params]` | JSON | Execute action on agent |
| `mock <agent> <action> [params]` | JSON | Free mock mode (no upstream hit) |

## Known Agents
| Agent | Handle | Domain |
|-------|--------|--------|
| Hazards | `hazards` | USGS earthquakes, NOAA weather, volcanoes |
| Health | `health` | FDA recalls, CDC diseases |
| Government | `government` | Congress bills, members, White House |
| Economics | `economic` | FRED data (GDP, inflation), SEC filings |
| Crime | `crime` | FBI wanted lists, UCR stats |

## Response format
```json
{
  "meta": {"agent": "...", "action": "...", "cacheStatus": "...", "creditsCharged": 0},
  "data": {...},
  "citation": {"source_name": "...", "license": "..."},
  "quality": {"confidence": "...", "certainty_score": 0-100}
}
