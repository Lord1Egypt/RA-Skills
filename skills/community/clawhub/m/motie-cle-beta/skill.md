---
name: motie-cli
description: Discover and explore APIs on the Motie marketplace using the motie CLI. Use this skill whenever you need to find an API or service to accomplish a task — restaurant reservations, web scraping, price monitoring, data extraction, or any other capability. Also use it when the user mentions Motie, the Motie marketplace, or asks what APIs are available. Always search before trying to call an unknown API.
---

# Motie CLI — API Discovery Tool

You have access to the `motie` CLI tool for discovering and calling APIs published on the Motie marketplace. Use it whenever you need an external API to accomplish a task.

## Setup

The CLI requires a Motie API key (starts with `mtk_`). Check if `MOTIE_API_KEY` is set in the environment. If not, tell the user to get one at https://beta.motie.dev under **Profile > API Key > Generate API Key**, then set it:

```bash
export MOTIE_API_KEY=mtk_your_key_here
```

Alternatively, pass `--api-key` to each command.

The CLI is installed via: `npm install -g @saucedocs/motie-cli`

## Workflow

Always follow this sequence:

### Step 1: Search for an API

```bash
motie search "<descriptive query>"
```

Use natural language — the search is semantic (embedding-based), so descriptive queries like "find restaurant availability and reservations" work better than single keywords.

Options: `--category <cat>`, `--tags <tags>` (comma-separated), `--limit <n>` (1-100, default 20)

Response:
```json
{
  "listings": [
    {
      "id": "abc-123",
      "name": "Restaurant Availability API",
      "short_description": "Real-time restaurant search and reservation availability",
      "category": "content_monitoring",
      "tags": ["restaurants", "reservations"],
      "published_at": "2026-04-03T19:42:55.318Z"
    }
  ],
  "total": 1
}
```

### Step 2: Get docs for a listing

Use the `id` from search results to fetch full API documentation:

```bash
motie docs <listing-id>
```

This returns all available routes with their parameters, request/response schemas, and an `example_cli` command you can run directly. Read the response carefully — it tells you exactly how to call the API.

Response (abbreviated):
```json
{
  "listing": { "id": "...", "name": "...", "description": "..." },
  "api": {
    "base_url": "https://example.execute-api.us-east-2.amazonaws.com",
    "routes": [
      {
        "method": "GET",
        "path": "/v1/restaurants/search",
        "description": "Search for restaurants by name or cuisine",
        "parameters": [
          { "name": "query", "required": true, "type": "string" },
          { "name": "location", "required": false, "type": "string | null" }
        ],
        "request_body": null,
        "response_schema": [ { "id": "string", "name": "string" } ],
        "example_cli": "motie call abc-123 /v1/restaurants/search --query <query> [--location <location>]"
      }
    ]
  }
}
```

### Step 3: Call the API

Use `motie call` to invoke any route directly:

```bash
motie call <listing-id> <route-path> --<key> <value> ...
```

Pass all parameters as flags — the CLI automatically places each parameter in the right location (query string, URL path, or request body) based on the route documentation.

Options: `--method <METHOD>` (auto-detected if omitted), `--api-key <key>`, `--base-url <url>`

Examples:
```bash
# GET with query params
motie call abc-123 /v1/restaurants/search --query "italian food" --location NYC

# GET with path param
motie call abc-123 /api/v1/airports/{iata} --iata LAX

# POST with body params (method auto-detected)
motie call abc-123 /api/v1/flight-searches --origin_iata LAX --destination_iata JFK --date 2026-05-01
```

## Error handling

All errors output JSON to stderr with exit code 1:
```json
{"error": "Missing API key. Set MOTIE_API_KEY or pass --api-key."}
```
