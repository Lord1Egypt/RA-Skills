---
name: kmb-bus-arrival
description: Retrieve real-time KMB bus arrival information. getArrival returns plain text.
version: 1.2.2
author: Steven Ho
repository: https://github.com/StevenHo1394/kmb-bus-arrival
tools:
  - name: getArrival
    description: Get the next bus arrival times for a specific route and stop name. Returns plain text.
    command: python3 kmb_bus.py getArrival {route} {stop_name}
    inputSchema:
      type: object
      required: [route, stop_name]
      properties:
        route:
          type: string
          pattern: '^[A-Za-z0-9]{1,16}$'
          maxLength: 16
        stop_name:
          type: string
          pattern: '^[\w\s\u4e00-\u9fff\(\)（）\-]{1,50}$'
          maxLength: 50
    output:
      format: text
---

# KMB Bus Arrival

Retrieve real-time KMB bus arrival information using the official KMB Open Data API (`data.etabus.gov.hk`).

## Installation

```bash
# Place kmb_bus.py and SKILL.md in your skills directory
# Requires: Python 3.8+, internet access to data.etabus.gov.hk
# Dependencies: certifi (pip install certifi)
```

## Usage

### Hermes CLI / OpenClaw

```bash
# Get arrivals for route E31 at Panda Hotel
python3 kmb_bus.py getArrival E31 "Panda Hotel"

# Get arrivals for route 265M at Chung On Street
python3 kmb_bus.py getArrival 265M "Chung On Street"
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `route` | string | KMB route number (e.g., `E31`, `265M`, `269M`) |
| `stop_name` | string | Stop name in English or Chinese (partial match supported) |

## Output Format

```
*E31 (to TSUEN WAN (DISCOVERY PARK))*

Stop: *PANDA HOTEL (TW281)*

Next arrivals:
- 20:46 HKT
- 21:11 HKT

(Current Time: 20:30 HKT)
```

### Features

- **Auto-direction**: Tries both inbound and outbound; reports whichever has the stop. If both directions serve the stop, both are shown.
- **Alternate stop ID fallback**: If the given stop name matches multiple stops on the route, uses up to 2 matches.
- **Fresh API calls**: No caching — all requests hit the live KMB API.
- **Plain text output**: Human-readable with Traditional Chinese stop names.
- **Human-readable errors**: Clear error messages for invalid routes/stops.

## Implementation Details

- **Script**: `kmb_bus.py` — single command `getArrival <route> <stop_name>`
- **API**: `https://data.etabus.gov.hk/v1/transport/kmb/`
  - `/route-stop/{route}/{bound}/1` — stop sequence with UUID IDs
  - `/stop/{stop_id}` — stop name lookup
  - `/eta/{stop_uuid}/{route}/1` — real-time ETA (Format B, UUID-based)
- **Timezone**: All times in HKT (UTC+8)
- **Retries**: 2 retries with exponential backoff, 3s total timeout per call

## Version History

### v1.2.2 (2026-09-13)
- Security fixes per ClawHub audit
- API call budget raised to 100, timeouts increased to 3s
- Fixed datetime.utcnow() deprecation
- Added README.md, flattened directory structure

### v1.2.1 (2026-08-22)
- Full removal of caching — all API calls are fresh
- Plain-text errors for getArrival
- Auto-direction and alternate stop ID fallback retained
- Single command: `getArrival <route> <stop_name>`
- Removed legacy commands: `getRouteDirection`, `getRouteInfo`, `getBusStopID`, `getNextArrivals`

## Related Skills

- `hk-gmb-arrival` — Green minibus (GMB) real-time arrival (different operator)
- `hong-kong-info` — General HK info services including franchised bus real-time occupancy

## References

- `references/clawhub-security-audit-2026-09-13.md` — ClawHub A.I.G security audit findings and remediation (T09 command injection, E1 external transmission, SDI-4 capability mismatch)
