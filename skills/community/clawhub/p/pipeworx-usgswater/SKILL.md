# USGS Water

Real-time streamflow and gage height data from the USGS National Water Information System. Monitor rivers, creeks, and streams across the United States.

## Tools

**get_current** -- Current instantaneous readings for a USGS monitoring site. Returns discharge (cubic feet per second) and gage height (feet) with timestamps and data quality flags.

**search_sites** -- Find active stream-gage sites in a US state that have real-time data. Returns site ID, name, coordinates, HUC code, and drainage area.

**get_daily** -- Historical daily mean streamflow values for a site between two dates.

## Example: Potomac River at Little Falls

Site 01646500 monitors the Potomac River near Washington, DC:

```bash
curl -X POST https://gateway.pipeworx.io/usgswater/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_current","arguments":{"site_id":"01646500"}}}'
```

## Finding site IDs

Use `search_sites` with a two-letter state abbreviation. For example, `"VA"` returns all active stream gages in Virginia with their site IDs and coordinates.

```json
{
  "mcpServers": {
    "usgswater": {
      "url": "https://gateway.pipeworx.io/usgswater/mcp"
    }
  }
}
```
