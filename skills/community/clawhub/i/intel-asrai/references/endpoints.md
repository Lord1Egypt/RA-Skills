# Intel x402 Endpoints

## Base URL
`https://intel.asrai.me`

## MCP Server URLs

| Transport | URL |
|---|---|
| HTTP Streamable | `https://intel-mcp.asrai.me/mcp?key=0x<your_private_key>` |
| SSE (legacy) | `https://intel-mcp.asrai.me/sse?key=0x<your_private_key>` |
| Key via env | `https://intel-mcp.asrai.me/mcp` (set `INTEL_PRIVATE_KEY` in env) |

## Payment
x402 automatic — $0.005 USDC per request on Base mainnet.
Wallet must hold USDC on Base mainnet. Payments are signed by the user's own wallet.

## Endpoint

### Search
`POST /search`

**Request body:**
```json
{
  "query":   "your search query",
  "mode":    "balanced",
  "sources": ["web"]
}
```

**Parameters:**
- `query` (required) — the search question or topic
- `mode` (optional) — `speed` | `balanced` | `quality` (default: `balanced`)
- `sources` (optional) — array of `web`, `academic`, `discussions` (default: `["web"]`)

**Mode guide:**
- `speed` — fastest, best for current events and simple questions
- `balanced` — default, good for most queries
- `quality` — deepest results, best for research

**Sources guide:**
- `web` — general web results (default)
- `academic` — research papers and academic sources
- `discussions` — forums, Reddit, community sentiment

**Response:**
```json
{
  "message": "synthesized answer text",
  "sources": [
    { "title": "Source Title", "url": "https://..." }
  ]
}
```

## Health check
`GET /health` — returns `{ "status": "ok" }`
