# Offline MCP Setup

This skill uses a local stdio MCP server backed by the bundled catalog snapshot.

Start it with:

```bash
node skills/pp-lounge-map-offline/scripts/run-offline-mcp.mjs
```

Print a ready-to-paste config snippet with:

```bash
node skills/pp-lounge-map-offline/scripts/print-offline-mcp-config.mjs
```

Local tools:

- `search_lounges`
- `get_lounge`
- `get_catalog_meta`

Local resources:

- `pp-lounge://meta`
- `pp-lounge://filters`
- `pp-lounge://lounge/{id}`

Local prompts:

- `airport-lounge-brief`
- `compare-airport-lounges`

The offline server uses only the bundled snapshot and does not fetch data at runtime.
