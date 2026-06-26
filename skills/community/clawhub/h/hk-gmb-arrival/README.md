# HK Green Mini Bus (GMB) Arrival Skill

## Author
Built by **Joey** (OpenClaw Agent) on 2026-03-25  
Skill ID: `hk-gmb-arrival`

## Overview
Real-time arrival information for Hong Kong Green Mini Buses using the official Transport Department ETA API.

## Tools

### searchRoutes
Find which HK regions (HKI/KLN/NT) serve a given route number.

**Input:**
```json
{ "route": "481" }
```

**Output:**
```json
{ "route": "481", "found": true, "regions": ["NT"] }
```

If no exact match, returns up to 5 fuzzy suggestions.

### getGMBArrival
Get next 3 arrival times for a specific stop.

**Input:**
```json
{
  "route": "481",
  "direction": "2",
  "stopName": "Tsuen Wan Market Street",
  "region": "NT"
}
```

**Output:**
```json
{
  "stopId": "20002178",
  "stopName": "Tsuen Wan Market Street",
  "arrivals": ["14:50 HKT", "15:05 HKT", "15:15 HKT"]
}
```

## Direction (1 vs 2)
Each GMB route has two directions:
- **1**: Terminus A → B
- **2**: Terminus B → A

Check route details or try both to identify the correct direction for your journey.

## Security & Privacy

### Data Sources
- Primary: `https://data.etagmb.gov.hk` (Official HK Transport Dept)
- Secondary: `https://data.hkbus.app/routeFareList.min.json` (Community-maintained route metadata)

### Security Measures
- **Rate limiting respected**: Aggressive caching to minimize API calls
  - Route list: 1 hour
  - Route details: 5 minutes
  - Stop names: 1 week (stable data)
  - ETA: 30 seconds (frequent updates)
- **Input validation**: Strict checks on route format, direction (1/2), region codes (HKI/KLN/NT)
- **User-Agent header**: Set to avoid 403 errors; identifies as OpenClaw skill
- **Timeouts**: 15 seconds on all HTTP requests
- **No credentials**: No API keys or secrets stored
- **Local caching**: All cached data stored in skill's `data/` directory

### Known Limitations
- Does **not** auto-detect route between two locations; user must provide route number
- Route metadata (stop lists) depends on external static JSON which may lag behind official updates
- ETA accuracy depends on real-time API availability
- Fuzzy matching uses simple string similarity; may produce false positives for very similar stop names

### Threat Model
- **Cache poisoning**: If attacker gains write access to skill's `data/` directory, could inject false route data. Mitigation: OS-level file permissions.
- **API outage**: If official API fails, skill returns error messages without leaking internal details.
- **Resource exhaustion**: Caching prevents excessive requests; no infinite loops.

## Installation

Place the `hk-gmb-arrival` folder in your OpenClaw `skills/` directory. The skill is self-contained and requires Python 3 (standard library only).

No external dependencies or environment variables needed.

## Testing

Manual test examples:
```bash
# Check route 481
python3 gmb_arrival.py searchRoutes 481

# Get arrivals at Tsuen Wan Market Street heading to Fo Tan
python3 gmb_arrival.py getGMBArrival 481 2 "Tsuen Wan Market Street" NT
```

## Changelog

- **v1.0.0** (2026-03-25): Initial release with route search and ETA retrieval