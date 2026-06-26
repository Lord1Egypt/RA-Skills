---
name: millimetric-mcp-setup
description: Connect AI agents (Claude Code, Claude Desktop, Cursor, MCP Inspector, OpenClaw) to the Millimetric MCP server so they can natively call track_event, query_events, get_stats, top_sources, and compare_projects. Use when the user wants their AI to read or write Millimetric analytics directly.
metadata: { "openclaw": { "requires": { "env": ["MILLIMETRIC_KEY"], "bins": ["curl"] }, "primaryEnv": "MILLIMETRIC_KEY", "emoji": "🧠", "homepage": "https://api.millimetric.ai/mcp" } }
---

# Millimetric MCP Setup

Wire any MCP client to Millimetric's `/mcp` (single-project) or `/mcp/account` (multi-project) endpoint. Transport is **JSON-RPC 2.0 over HTTP** — no SSE needed.

## When to Use

- "Let Claude / my agent read my Millimetric data"
- Connecting Claude Code, Claude Desktop, Cursor, or MCP Inspector
- Multi-project / agency setup (`ak_live_…`)
- Verifying an MCP connection or listing available tools

## When NOT to Use

- One-shot CLI queries → `millimetric-query`
- Sending events from a server → `millimetric-track`

## Endpoints

| Endpoint | Auth | Scope | Plan |
|----------|------|-------|------|
| `POST https://api.millimetric.ai/mcp` | `sk_live_…` or `rk_live_…` | One project | Pro+ |
| `POST https://api.millimetric.ai/mcp/account` | `ak_live_…` | All projects on the account | Business |

`pk_live_…` keys are **rejected** with `403 key_kind_not_allowed`. They ship in browser JS and must never grant analytics access.

| Key you give the agent | Tools it gets |
|------------------------|---------------|
| `rk_live_…` | `query_events`, `get_stats`, `top_sources`, `funnel`, resources |
| `sk_live_…` | the read tools above **plus** `track_event` |
| `ak_live_…` | every read tool with optional `project_id`/`project_slug`/`project_ids`, plus `list_projects` and `compare_projects` |

Default to `rk_*`. Only hand the agent `sk_*` if it must emit events.

## Quick start

### Claude Code / Claude Desktop

Edit `~/.claude/config.json` (or use the UI):

```json
{
  "mcpServers": {
    "millimetric": {
      "url": "https://api.millimetric.ai/mcp",
      "transport": "http",
      "headers": {
        "Authorization": "Bearer rk_live_…"
      }
    }
  }
}
```

Restart Claude. Then:

> "Use millimetric.top_sources to show me the Facebook social-vs-paid split for the last 7 days."

### Cursor

`~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "millimetric": {
      "url": "https://api.millimetric.ai/mcp",
      "transport": "http",
      "headers": { "Authorization": "Bearer rk_live_…" }
    }
  }
}
```

### MCP Inspector (interactive testing)

```bash
npx @modelcontextprotocol/inspector
# URL:  https://api.millimetric.ai/mcp   (or http://localhost:8787/mcp for local dev)
# Header: Authorization: Bearer rk_live_…
```

### Account MCP (multi-project)

```json
{
  "mcpServers": {
    "millimetric-account": {
      "url": "https://api.millimetric.ai/mcp/account",
      "transport": "http",
      "headers": { "Authorization": "Bearer ak_live_…" }
    }
  }
}
```

## Verify the connection from the CLI

```bash
# List available tools
curl -s -X POST https://api.millimetric.ai/mcp \
  -H "Authorization: Bearer $MILLIMETRIC_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | jq

# Call top_sources directly
curl -s -X POST https://api.millimetric.ai/mcp \
  -H "Authorization: Bearer $MILLIMETRIC_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0","id":2,"method":"tools/call",
    "params":{
      "name":"top_sources",
      "arguments":{
        "from":"2026-05-01T00:00:00Z",
        "to":"2026-06-01T00:00:00Z",
        "breakdown":"source_medium",
        "limit":20
      }
    }
  }' | jq
```

## Tools cheat sheet

### Single-project (`/mcp`)

| Tool | Scope | Purpose |
|------|-------|---------|
| `track_event` | ingest (`sk_*`) | Emit a single event. |
| `query_events` | read | Filter raw events by date, event name, source, user. |
| `get_stats` | read | Aggregations with `metric`, `group_by`, `interval`. |
| `top_sources` | read | Top sources/mediums with FB social-vs-paid split. |
| `funnel` | read | Step conversion analysis. |

Resources: `events://recent`, `schema://events`.

### Account (`/mcp/account`)

Every read tool accepts optional `project_id` / `project_slug` / `project_ids`. Omit them to span every project the key can see — rows include a `project_id` column when the query is multi-project.

| Tool | Purpose |
|------|---------|
| `list_projects` | Every project the key can read. |
| `query_events` | Multi-project event queries. |
| `get_stats` | Group by `project_id` to compare apps. |
| `top_sources` | Top channels across one or all projects. |
| `compare_projects` | Rank projects by `count` or `uniques`. |

Resources: `projects://all`, `schema://events` (across all accessible projects).

## Tool result shape

MCP tool results come back as `content[]` with stringified JSON:

```json
{
  "jsonrpc": "2.0", "id": 1,
  "result": {
    "content": [
      { "type": "text", "text": "[{\"source\":\"facebook\",\"medium\":\"paid\",\"events\":6,...}]" }
    ]
  }
}
```

Agents `JSON.parse` the `text` to get rows.

## Errors

| Code | Meaning | Fix |
|------|---------|-----|
| -32600 | invalid_request | Body isn't valid JSON-RPC. |
| -32601 | method_not_found | Unknown method. |
| -32602 | unknown_tool / unknown_resource | Misspelled tool/resource name. |
| -32000 | tool_failed / insufficient_scope | Use a higher-scope key (e.g. `sk_*` for `track_event`). |
| -32002 | plan_limit | Account-MCP requires Business; `/mcp` requires Pro+. |
| -32004 | unknown_project_id / unknown_project_slug | Account-MCP only — project doesn't exist or key can't see it. |
| -32005 | no_projects_visible | Account-MCP key has zero accessible projects. |
| HTTP 403 | `key_kind_not_allowed` | You used `pk_*`. Use `rk_*` / `sk_*` (or `ak_*` on `/mcp/account`). |
| HTTP 403 | `account_key_required` | `/mcp/account` only takes `ak_*`. |

## Local dev

When running the Worker locally:

```bash
pnpm dev:api   # http://localhost:8787
```

Point your MCP client at `http://localhost:8787/mcp` with the same Bearer header.

## See also

- Single-shot ingest → `millimetric-track`
- Single-shot reads → `millimetric-query`
