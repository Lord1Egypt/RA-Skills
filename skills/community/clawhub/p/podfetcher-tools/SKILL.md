---
name: podfetcher-tools
description: Search podcasts, browse episodes, and fetch podcast transcripts from Podfetcher using the bundled Node.js CLI, SDK, or MCP server.
version: 0.5.1
metadata:
  openclaw:
    requires:
      env:
        - PODFETCHER_API_KEY
        - PODFETCHER_BASE_URL
        - PODFETCHER_API_KEY_HEADER
      bins:
        - node
    primaryEnv: PODFETCHER_API_KEY
    homepage: https://podfetcher.com
---

# Podfetcher Tools

Podfetcher Tools is a Node.js client bundle for the Podfetcher API. It gives you three ways to work with podcast data from the same package:

- a CLI for quick terminal workflows
- an SDK for custom scripts and apps
- an MCP server so agents can search shows, list episodes, and fetch transcripts

Use it when you want to discover podcasts, inspect episode catalogs, or retrieve transcripts from [podfetcher.com](https://podfetcher.com).

## Requirements

- Node.js 20+
- `PODFETCHER_API_KEY` set to a valid Podfetcher API key

The default API base URL is `https://api.podfetcher.com`. Override it only when targeting a non-production environment.

## Getting Started

1. Create or sign in to your account at [podfetcher.com](https://podfetcher.com).
2. Generate an API key from the Podfetcher dashboard.
3. Export the key before running the CLI or MCP server:

```bash
export PODFETCHER_API_KEY="pk_live_your_key_here"
```

Optional overrides:

- `PODFETCHER_BASE_URL` for non-production environments
- `PODFETCHER_API_KEY_HEADER` if you need a non-default header name

## Entry Points

If the package is installed globally from npm, use these binaries:

- `podfetcher`
- `podfetcher-mcp`

If you are working from a local checkout instead, run commands from this directory or reference these files by absolute path from another workspace:

- CLI: `node src/cli.js`
- MCP server: `node src/mcp.js`
- SDK import: `./src/sdk.js`

## CLI Commands

### Search shows

```bash
podfetcher shows search --q "<query>" [--limit <n>] [--cursor <cursor>] [--json]
```

- `--q` is required
- Returns `items[]` with `showId`, `title`, and `author`
- If present, pass `nextCursor` into `--cursor` for the next page

### List episodes

```bash
podfetcher shows episodes --show-id <showId> [--from <iso>] [--to <iso>] [--since <iso>] [--order-by publishedAt] [--order asc|desc] [--limit <n>] [--cursor <cursor>] [--json]
```

- `--show-id` is required
- Returns `items[]` with `episodeId`, `publishedAt`, `title`, and `transcriptStatus`

### Fetch transcript

```bash
podfetcher transcripts fetch --episode-id <episodeId> [--wait] [--poll-interval-ms <ms>] [--wait-timeout-ms <ms>] [--idempotency-key <key>] [--json]
```

- `--episode-id` is required
- Without `--wait`, the API may return a queued job with `jobId` and `status=PROCESSING`
- With `--wait`, the client polls until the transcript is ready or the timeout expires

## Global CLI Options

- `--api-key <key>` or `PODFETCHER_API_KEY` for Podfetcher authentication
- `--base-url <url>` or `PODFETCHER_BASE_URL` for API endpoint override
- `--api-key-header <header>` or `PODFETCHER_API_KEY_HEADER` for header override
- `--timeout-ms <ms>`
- `--json`

## Typical Workflow

```bash
# 1. Find a show
podfetcher shows search --q "lex fridman" --limit 3 --json

# 2. List recent episodes
podfetcher shows episodes --show-id <showId> --order-by publishedAt --order desc --limit 5 --json

# 3. Fetch the transcript and wait for completion
podfetcher transcripts fetch --episode-id <episodeId> --wait --json
```

## MCP Server

Start the MCP server over stdio:

```bash
podfetcher-mcp
```

Available tools:

- `search_shows`
- `list_episodes`
- `fetch_transcript`

Example config:

```json
{
  "mcpServers": {
    "podfetcher": {
      "command": "node",
      "args": ["/absolute/path/to/podfetcher-tools/src/mcp.js"],
      "env": {
        "PODFETCHER_API_KEY": "pk_live_..."
      }
    }
  }
}
```

## Error Handling

- HTTP errors are formatted as `[HTTP <status>] <code>: <message>`
- Missing API key errors are reported before the request is sent
- Exit code is `1` on error and `0` on success
