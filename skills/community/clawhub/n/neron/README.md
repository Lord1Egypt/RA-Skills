# Neron

Personal knowledge graph. Voice notes in, structured intelligence out.

```
voice/text → transcription → extraction → graph → patterns → push
```

## What it is

A Telegram bot (@NeronBetaBot) that turns your stream of consciousness into a queryable knowledge graph. Every note you send gets automatically decomposed into: mood, activities, body state, people, tasks, reflections — all linked in Apache AGE (graph layer on PostgreSQL).

Then you (or your AI agent) can query the graph to find patterns, track mood over time, correlate activities with energy, manage tasks, and build self-knowledge from raw data.

## Architecture

```
Telegram Bot ←→ PostgreSQL 16 + Apache AGE
                    ↕
              MCP Server (SSE)
                    ↕
           Your AI Agent / Claude / OpenClaw
```

- **Bot** — records notes, runs extractions, sends push coaching, handles /ai queries
- **MCP Server** — 11 tools for external agent access (read/write/search/cypher)
- **Graph** — schema-per-user multitenancy, Voyage AI embeddings, full observability (LGTM/Grafana)

## For Users

→ [User Guide](docs/USER-GUIDE.md) — how to use the bot, commands, cool features
→ [Connect to Claude](docs/CONNECT-CLAUDE.md) — add Neron as a Claude connector

## For Agents

→ [SKILL.md](SKILL.md) — teach your agent how to use Neron's MCP tools intelligently
→ [Connect Agent](docs/CONNECT-AGENT.md) — Bearer token setup for OpenClaw/Cursor/Claude Code

## MCP Tools (12)

| Tool | Purpose |
|------|---------|
| `get_stats` | Entity counts |
| `search` | ILIKE text search |
| `semantic_search` | Vector similarity search (Voyage AI embeddings) |
| `search_notes` | Notes by date/keywords |
| `list_entities` | Browse by type + filters |
| `node_context` | Node + neighborhood (BFS, depth 1-3) |
| `create_entity` | Create any entity |
| `update_entity` | Partial update |
| `delete_entity` | Delete + cascade edges |
| `bulk_create` | Atomic multi-create |
| `cypher` | Raw Cypher queries |
| `instructions` | Full API documentation |

## Connect

**Claude users** — `/password` in @NeronBetaBot → add custom connector in Claude → [guide](docs/CONNECT-CLAUDE.md)

**Agent users** — `/token` in @NeronBetaBot → add to MCP config:
```json
{
  "mcpServers": {
    "neron": {
      "url": "https://mcp.neron.guru/mcp",
      "transport": "sse",
      "headers": { "Authorization": "Bearer <token from /token>" }
    }
  }
}
```

## Stack

PostgreSQL 16 · Apache AGE · Node.js · Whisper · Voyage AI · Hetzner · Grafana/LGTM
