# KMB Bus Arrival

Retrieve real-time KMB bus arrival information using the official KMB Open Data API (`data.etabus.gov.hk`).

## Installation

```bash
# Place kmb_bus.py and SKILL.md in your skills directory
# Requires: Python 3.8+, internet access to data.etabus.gov.hk
# Dependencies: certifi (pip install certifi)
```

## Usage

```bash
# Get arrivals for route E31 at Panda Hotel
python3 kmb_bus.py getArrival E31 "Panda Hotel"

# Get arrivals for route 265M at Chung On Street
python3 kmb_bus.py getArrival 265M "Chung On Street"

# Get arrivals for route 265M at 荃灣眾安街 (Chinese)
python3 kmb_bus.py getArrival 265M "荃灣眾安街"
```

### Parameters

| Parameter   | Type   | Description                                                                 |
| ----------- | ------ | --------------------------------------------------------------------------- |
| `route`     | string | KMB route number (e.g., `E31`, `265M`, `269M`) — alphanumeric, max 16 chars |
| `stop_name` | string | Stop name in English or Chinese (partial match supported) — max 50 chars    |

## Output Format

```
*E31 (to TSUEN WAN (DISCOVERY PARK))*

Stop: *PANDA HOTEL (TW281)*

Next arrivals:
- 20:46 HKT
- 21:11 HKT

(Current Time: 20:30 HKT)
```

If a stop serves both directions, both are shown:

```
*265M (to LAI YIU BUS TERMINUS (KW991) / TIN HENG ESTATE BUS TERMINUS (TN972))*

Stop: *CHUNG ON STREET TSUEN WAN (TW388)*

Next arrivals (to LAI YIU BUS TERMINUS (KW991)):
- 21:27 HKT
- 21:45 HKT
- 22:04 HKT
Next arrivals (to TIN HENG ESTATE BUS TERMINUS (TN972)):
- 21:29 HKT
- 21:43 HKT
- 21:55 HKT

(Current Time: 21:24 HKT)
```

## Features

- **Auto-direction**: Tries both inbound and outbound; reports whichever has the stop. If both directions serve the stop, both are shown.
- **Alternate stop ID fallback**: If the given stop name matches multiple stops on the route, uses up to 2 matches.
- **Fresh API calls**: No caching — all requests hit the live KMB API.
- **Plain text output**: Human-readable with Traditional Chinese stop names.
- **Human-readable errors**: Clear error messages for invalid routes/stops.
- **Strict input validation**: Route and stop name validated against allowlist patterns and length limits.
- **No shell interpolation**: Arguments passed as argv array, not shell command string.
- **Rate limiting**: Max 10 requests/minute per process.
- **API call budget**: Max 100 API calls per invocation.

## Security

This skill has been hardened per ClawHub security audit (v1.2.2):

- Removed obsolete tool declarations that didn't match implementation
- Strict input schemas with patterns and maxLength for all parameters
- Arguments passed via argv array (no shell interpolation)
- Local rate limiting (10 req/min) and API call budget (100 calls/invocation)
- Explicit SSL certificate verification with certifi CA bundle
- Unified error messages without internal API structure disclosure
- Removed redundant `/route-stop` full fetch (optimization)

## API

- **Base**: `https://data.etabus.gov.hk/v1/transport/kmb/`
- **Endpoints used**:
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

## License

MIT-0
