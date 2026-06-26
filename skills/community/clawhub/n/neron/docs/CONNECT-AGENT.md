# Connect Neron to Your Agent

Give your AI agent read/write access to your knowledge graph via MCP.

---

## Steps

### 1. Get your Bearer token

Open **@NeronBetaBot** in Telegram → send `/token`

Copy the token string.

### 2. Add MCP config

```json
{
  "mcpServers": {
    "neron": {
      "url": "https://mcp.neron.guru/mcp",
      "transport": "sse",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
```

Where this goes:

| Agent | Config location |
|-------|----------------|
| OpenClaw | `~/.openclaw/workspace/config/mcporter.json` |
| Claude Code | `~/.claude/mcp.json` |
| Cursor | Settings → MCP → Add Server |

### 3. Load the skill

Copy `SKILL.md` into your agent's skills directory. This teaches the agent how to use Neron's 12 tools intelligently.

### 4. Verify

Ask your agent:
```
Call Neron get_stats and show me what's in my graph
```

---

## 12 tools your agent gets

| Tool | Purpose |
|------|---------|
| `get_stats` | Entity counts |
| `search` | ILIKE text search across entities |
| `semantic_search` | Vector similarity search (Voyage AI) — finds by meaning, cross-language |
| `search_notes` | Notes by date/keywords |
| `list_entities` | Browse by type + filters |
| `node_context` | Node + neighborhood via graph BFS (depth 1-3) |
| `create_entity` | Create notes, tasks, people, insights, edges |
| `update_entity` | Partial updates |
| `delete_entity` | Delete + cascade edges |
| `bulk_create` | Atomic multi-create |
| `cypher` | Raw Cypher on Apache AGE graph |
| `instructions` | Full API docs — call once per conversation |

Full schemas → [docs/mcp-tools.md](mcp-tools.md)

---

## Agent use cases

**Daily assistant** — agent checks graph each morning, surfaces stale tasks, mood trends, yesterday's notes.

**Meeting prep** — "Pull everything I know about $PERSON" → searches notes, finds edges, builds context.

**Pattern detection** — weekly Cypher queries: "energy peaks on exercise days", "mood drops after substance use".

**RAG on your life** — semantic_search finds conceptually related notes for complex questions about yourself.

**Auto-logging** — agent writes ai_notes when it spots insights. Graph grows passively.

---

## Security

- Tokens are per-user, revocable via `/token` (new token invalidates old)
- Schema-per-user isolation in PostgreSQL — no cross-user access
- All traffic over HTTPS
