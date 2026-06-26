# meteoswiss-ogd skill

## Purpose

Teaches AI agents to access MeteoSwiss Open Government Data directly via HTTP, without requiring an MCP server. Covers current weather, forecasts, pollen data, and station discovery.

## Tier

**Publishable/reusable** — platform-independent, no OS-specific dependencies. Works with any agent that can make HTTP requests (curl, WebFetch, fetch).

## Provenance

Data source documentation and URLs extracted from the [`meteoswiss-mcp`](../../../meteoswiss-mcp/) server codebase:

- STAC API client: `packages/meteoswiss-mcp/src/data/ogd-stac-client.ts`
- Current weather: `packages/meteoswiss-mcp/src/data/ogd-current-weather.ts`
- Forecast data: `packages/meteoswiss-mcp/src/data/ogd-local-forecast.ts`
- Pollen data: `packages/meteoswiss-mcp/src/data/ogd-pollen-data.ts`
- Shared schemas: `packages/meteoswiss-mcp/src/schemas/ogd-shared.ts`
- Weather icons: `packages/meteoswiss-mcp/src/support/weather-icons.ts`

Official documentation: [opendatadocs.meteoswiss.ch](https://opendatadocs.meteoswiss.ch/)

## Testing

```bash
# Validate skill format
pnpm test

# Verify data URLs are live
curl -sf 'https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv' | head -1
curl -sf 'https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-smn' | jq .id
curl -sf 'https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-local-forecasting/items?limit=1' | jq '.features[0].id'
```

## Known Gaps

- No radar/satellite image data (not available as structured OGD)
- Climate normals tool pending MeteoSwiss publishing `ch.meteoschweiz.ogd-climate-normals`
- Weather icon code descriptions cover codes 1-35 (day) and 101-142 (night) — additional codes may exist
- Forecast point_id examples are limited; agents should look up point_id from metadata
