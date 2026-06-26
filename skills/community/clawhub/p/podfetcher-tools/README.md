# podfetcher-tools

Node.js CLI, SDK, and MCP server for searching podcasts, listing episodes, and fetching transcripts from Podfetcher.

## Features
- Shared SDK for API auth, requests, and error handling
- CLI for show search, episode lookup, and transcript fetch
- MCP server exposing the same operations as tools

## Requirements
- Node.js 20+
- A valid Podfetcher API key (`X-API-Key`)

## Getting Started

Create or sign in to your account at [podfetcher.com](https://podfetcher.com), then generate an API key from the Podfetcher dashboard.

Export the key before using the CLI or MCP server:

```bash
export PODFETCHER_API_KEY="pk_live_your_key_here"
```

Install globally from npm to use the `podfetcher` and `podfetcher-mcp` commands anywhere:

```bash
npm install -g podfetcher-tools
```

Then verify:

```bash
podfetcher --help
```

## Configuration
Environment variables:

- `PODFETCHER_BASE_URL` (default `https://api.podfetcher.com`)
- `PODFETCHER_API_KEY` (required, format: `pk_live_...`)
- `PODFETCHER_API_KEY_HEADER` (default `X-API-Key`)

CLI flags can override env values:
- `--base-url`
- `--api-key`
- `--api-key-header`
- `--timeout-ms`

## CLI Usage

### Search shows
```bash
podfetcher shows search --q "ai" --limit 5
```

### List episodes for a show
```bash
podfetcher shows episodes --show-id pi_1001 --order-by publishedAt --order desc --limit 10
```

### Fetch transcript for an episode
```bash
podfetcher transcripts fetch --episode-id ep_pi_1001_004
```

### Fetch transcript and wait until READY
```bash
podfetcher transcripts fetch \
  --episode-id ep_pi_1001_002 \
  --wait \
  --poll-interval-ms 1000 \
  --wait-timeout-ms 60000
```

### Machine-readable JSON output
```bash
podfetcher shows search --q "ai" --json
```

## MCP Usage
Run the MCP server over stdio:

```bash
podfetcher-mcp
```

Available tools:
- `search_shows`
- `list_episodes`
- `fetch_transcript`

Example MCP server config snippet:

```json
{
  "mcpServers": {
    "podfetcher": {
      "command": "node",
      "args": ["/absolute/path/to/clients/podfetcher-tools/src/mcp.js"],
      "env": {
        "PODFETCHER_API_KEY": "pk_live_..."
      }
    }
  }
}
```
