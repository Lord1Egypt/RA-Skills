# Offline MCP Setup

This skill uses a local stdio MCP server backed by the bundled airport-lounge catalog snapshot.

Start it with:

```bash
node skills/lounge-guru-map/scripts/run-offline-mcp.mjs
```

Print a ready-to-paste config snippet with:

```bash
node skills/lounge-guru-map/scripts/print-offline-mcp-config.mjs
```

Local tools:

- `search_lounges`
- `get_lounge`
- `get_catalog_meta`

Local resources:

- `lounge-guru://meta`
- `lounge-guru://filters`
- `lounge-guru://lounge/{id}`

Local prompts:

- `airport-lounge-brief`
- `compare-airport-lounges`

The offline server uses only the bundled snapshot and does not fetch data at runtime. Answer for any lounge covered by the bundled data; do not imply coverage is limited to one membership program unless the record itself says so.
