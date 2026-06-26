# TLE (Satellite Tracking)

Fetch Two-Line Element sets for satellites. TLEs are the standard format for describing satellite orbits -- used by tracking software, ground stations, and orbital mechanics calculations.

## Available tools

**get_tle** -- Fetch TLE data for a specific satellite by its NORAD catalog ID. Returns the satellite name, epoch date, and both TLE lines.

**search_satellites** -- Search by name or keyword. "ISS", "Starlink", "GPS", "Hubble" all work. Returns matching satellites with NORAD IDs and TLE data.

**list_recent** -- The most recently launched or updated satellites, sorted by epoch date.

## Example: get the ISS TLE

The ISS has NORAD catalog number 25544:

```bash
curl -X POST https://gateway.pipeworx.io/tle/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_tle","arguments":{"norad_id":25544}}}'
```

## Common NORAD IDs

- ISS: 25544
- Hubble Space Telescope: 20580
- NOAA-19: 33591
- Terra (EOS): 25994

```json
{
  "mcpServers": {
    "tle": {
      "url": "https://gateway.pipeworx.io/tle/mcp"
    }
  }
}
```
