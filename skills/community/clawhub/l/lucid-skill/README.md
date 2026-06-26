# lucid-skill

**AI-native data analysis skill.** Connect Excel, CSV, MySQL, PostgreSQL — understand business semantics, query with SQL.

No API key required. No LLM inside — the AI agent is the brain; lucid-skill is the hands.

---

## Features

- **Multi-source**: Excel (.xlsx/.xls), CSV, MySQL, PostgreSQL — all unified into SQL
- **Semantic Layer**: Define business meanings for tables and columns; persist as YAML, Git-friendly
- **JOIN Discovery**: Automatically find join paths between tables (direct + indirect)
- **Domain Clustering**: Auto-group tables into business domains
- **Embedding Search**: Optional multilingual vector search for table discovery
- **Read-only Safety**: Only SELECT allowed — mutating SQL is blocked at the engine level

---

## Install

```bash
pip install lucid-skill

# Or with uv (recommended for OpenClaw)
uv tool install lucid-skill

# Optional: database drivers
pip install "lucid-skill[db]"       # MySQL + PostgreSQL

# Optional: embedding search
pip install "lucid-skill[embedding]" # sentence-transformers
```

---

## Quick Start

```bash
# Connect a data source
lucid-skill connect csv /path/to/sales.csv

# Explore schema and semantics
lucid-skill init-semantic

# Search tables by business meaning
lucid-skill search "销售额 客户"

# Query with SQL
lucid-skill query "SELECT product, SUM(amount) FROM sales GROUP BY product ORDER BY 2 DESC LIMIT 10"
```

---

## Architecture

```
Agent ──→ lucid-skill CLI ──→ Connectors (Excel/CSV/MySQL/PG)
                │                      │
                ├── Catalog (DuckDB)   └── DuckDB (in-memory query engine)
                └── Semantic Store (YAML)
```

- **No LLM inside** — lucid-skill provides data access; the AI agent handles reasoning
- **DuckDB unified** — catalog storage + query engine, single dependency, no compilation needed
- **Semantic persistence** — YAML definitions survive restarts, shareable via Git

---

## Supported Data Sources

| Type | Format | Notes |
|------|--------|-------|
| Excel | `.xlsx`, `.xls` | Multiple sheets supported |
| CSV | `.csv` | Auto-detects encoding and delimiter |
| MySQL | 5.7+ / 8.0+ | Reads foreign keys and column comments (`pip install lucid-skill[db]`) |
| PostgreSQL | 12+ | Reads foreign keys and column comments (`pip install lucid-skill[db]`) |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LUCID_DATA_DIR` | `~/.lucid-skill/` | Data directory (catalog, semantic store, models) |
| `LUCID_EMBEDDING_ENABLED` | `false` | Enable vector search (~460 MB model download on first use) |

---

## Security

- **Read-only**: Only `SELECT` / `WITH` statements are allowed; all mutating SQL is blocked
- **No credentials stored**: Database passwords are never written to disk
- **Local only**: All data stays on your machine

---

## MCP Server Mode

lucid-skill also works as an MCP Server for platforms that support it:

```bash
lucid-skill serve
```

---

## Development

```bash
git clone https://github.com/WiseriaAI/lucid-skill
cd lucid-skill
pip install -e ".[dev]"
pytest
```

## License

MIT
