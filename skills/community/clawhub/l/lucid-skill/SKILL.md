---
name: lucid-skill
description: "AI-native data analysis via natural language. Connect Excel, CSV, MySQL, PostgreSQL data sources and query with SQL. Use when: (1) user asks to query, analyze, or explore data ('查询数据', '数据分析', '帮我看下数据'), (2) user provides Excel/CSV files or database credentials for analysis, (3) user asks business questions about connected data ('哪个产品销量最高', 'how do orders and customers relate?'), (4) user wants to discover table relationships, JOINs, or business domains, (5) user wants semantic search across tables. NOT for: data modification (INSERT/UPDATE/DELETE/DROP are blocked — read-only queries only), ETL pipelines, or data ingestion beyond connecting sources."
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["lucid-skill"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "lucid-skill",
              "bins": ["lucid-skill"],
              "label": "Install lucid-skill (uv)",
            },
          ],
      },
  }
---

# lucid-skill

Connect data → infer semantics → query with natural language → get answers.

All output is JSON unless noted. No API key needed.

## Quick Start

```bash
lucid-skill connect csv /path/to/sales.csv     # Connect data
lucid-skill overview                            # Check connected sources
lucid-skill search "月度销售额趋势"              # Find relevant tables + suggested SQL
lucid-skill query "SELECT month, SUM(amount) FROM sales GROUP BY month"  # Execute
```

## Core Commands

| Command | Purpose |
|---------|---------|
| `overview` | Show all connected sources, tables, semantic status |
| `connect csv/excel/mysql/postgres` | Connect a data source |
| `tables` | List all tables with row counts |
| `describe <table>` | Column details + sample data + semantics |
| `profile <table>` | Deep stats: null rate, distinct, min/max, quartiles |
| `init-semantic` | Export schemas for semantic inference |
| `update-semantic <file\|->` | Save semantic definitions (JSON from file or stdin) |
| `search <query> [--top-k N]` | Natural language → relevant tables + JOIN hints + metric SQL |
| `join-paths <a> <b>` | Discover JOIN paths between two tables |
| `domains` | Auto-discovered business domains |
| `query <sql> [--format json\|md\|csv]` | Execute read-only SQL |
| `serve` | Start MCP Server (stdio JSON-RPC) |

For full command reference with all parameters: read [references/commands.md](references/commands.md)

## Smart Query Pattern (Recommended)

When a user asks a data question:

1. `lucid-skill search "关键词"` — find relevant tables, suggestedJoins, suggestedMetricSqls
2. If multi-table: `lucid-skill join-paths table_a table_b` — get JOIN SQL
3. Compose SQL from the returned context
4. `lucid-skill query "SELECT ..."` — execute and present results

## Semantic Layer Setup

First-time setup to enable intelligent search:

```bash
lucid-skill init-semantic                               # Export schemas
# Analyze output → infer business meanings for each column
echo '{"tables":[...]}' | lucid-skill update-semantic -  # Save semantics
```

For JSON schema details: read [references/json-schema.md](references/json-schema.md)

## Key Tips

- **Auto-restore**: Previous connections survive restarts. Always `overview` first to check existing state.
- **Read-only**: Only SELECT allowed. INSERT/UPDATE/DELETE/DROP are blocked.
- **Semantic files**: Stored in `~/.lucid-skill/semantic_store/` (YAML, human-readable).
- **Data directory**: `~/.lucid-skill/` (override with `LUCID_DATA_DIR` env var).
- **Embedding**: Set `LUCID_EMBEDDING_ENABLED=true` for better multilingual search (downloads ~460 MB model on first use).
- **No credentials stored**: Database passwords are never written to disk.
- **MCP mode**: `lucid-skill serve` starts stdio JSON-RPC server for MCP integrations.

## Detailed References

- [references/commands.md](references/commands.md) — Full CLI command reference with all parameters
- [references/json-schema.md](references/json-schema.md) — `update-semantic` JSON format specification
- [references/workflow.md](references/workflow.md) — Multi-step workflow guides (first-time setup, returning sessions, multi-source)
