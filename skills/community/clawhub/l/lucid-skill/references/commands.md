# CLI Command Reference

Complete reference for all `lucid-skill` CLI commands.

## Table of Contents

- [overview](#overview)
- [connect](#connect)
- [tables](#tables)
- [describe](#describe)
- [profile](#profile)
- [init-semantic](#init-semantic)
- [update-semantic](#update-semantic)
- [search](#search)
- [join-paths](#join-paths)
- [domains](#domains)
- [query](#query)
- [serve](#serve)

---

## overview

Show all connected data sources, tables, and semantic status.

```bash
lucid-skill overview
```

**Start here** on every session. Previous connections auto-restore, so this shows current state immediately.

---

## connect

Connect a data source. Supported types: `csv`, `excel`, `mysql`, `postgres`.

### CSV

```bash
lucid-skill connect csv <path>
```

### Excel

```bash
lucid-skill connect excel <path> [--sheets Sheet1,Sheet2]
```

| Parameter | Description |
|-----------|-------------|
| `--sheets` | Comma-separated sheet names to import. Omit to import all sheets. |

### MySQL

```bash
lucid-skill connect mysql --host <host> --database <db> --username <user> --password <pass> [--port 3306]
```

### PostgreSQL

```bash
lucid-skill connect postgres --host <host> --database <db> --username <user> --password <pass> [--port 5432] [--schema <schema>]
```

| Parameter | Description |
|-----------|-------------|
| `--host` | Database hostname |
| `--port` | Database port (MySQL default: 3306, PostgreSQL default: 5432) |
| `--database` | Database name |
| `--username` | Database user |
| `--password` | Database password (never persisted to disk) |
| `--schema` | PostgreSQL schema (default: `public`) |

---

## tables

List all connected tables with row counts.

```bash
lucid-skill tables [--source-id <id>]
```

| Parameter | Description |
|-----------|-------------|
| `--source-id` | Filter tables by a specific source ID (optional) |

---

## describe

Show column details, sample data, and semantic annotations for a table.

```bash
lucid-skill describe <table>
```

---

## profile

Deep statistical profiling of a table: null rate, distinct count, min/max, quartiles, top values.

```bash
lucid-skill profile <table>
```

---

## init-semantic

Export current table schemas for semantic inference. Use this output to analyze columns and prepare semantic definitions.

```bash
lucid-skill init-semantic [--source-id <id>]
```

| Parameter | Description |
|-----------|-------------|
| `--source-id` | Export schemas for a specific source only (optional) |

Output: JSON with all table schemas. Feed into LLM analysis → `update-semantic`.

---

## update-semantic

Save inferred semantic definitions. Accepts JSON from file or stdin.

```bash
lucid-skill update-semantic <file>
lucid-skill update-semantic -          # Read from stdin
echo '{"tables":[...]}' | lucid-skill update-semantic -
```

For full JSON format specification, see [json-schema.md](json-schema.md).

---

## search

Natural language search across all connected tables. Returns relevant tables, JOIN hints, and suggested metric SQL.

```bash
lucid-skill search "<query>" [--top-k 5]
```

| Parameter | Description |
|-----------|-------------|
| `--top-k` | Number of results to return (default: 5) |

Example:

```bash
lucid-skill search "月度销售额趋势"
lucid-skill search "客户留存" --top-k 10
```

Response includes: `relevantTables`, `suggestedJoins`, `suggestedMetricSqls`.

---

## join-paths

Discover JOIN paths between two tables. Returns the SQL JOIN conditions.

```bash
lucid-skill join-paths <table_a> <table_b>
```

---

## domains

Show auto-discovered business domains based on semantic annotations.

```bash
lucid-skill domains [--datasource <name>]
```

| Parameter | Description |
|-----------|-------------|
| `--datasource` | Filter domains by datasource name (optional) |

---

## query

Execute read-only SQL. Only SELECT statements allowed.

```bash
lucid-skill query "<sql>"
lucid-skill query "<sql>" --format json
lucid-skill query "<sql>" --format csv
```

| Parameter | Description |
|-----------|-------------|
| `--format` | Output format: `markdown` (default), `json`, `csv` |

Default output is markdown table for readability.

---

## serve

Start MCP Server (stdio JSON-RPC) for integration with Claude Desktop, Cursor, etc.

```bash
lucid-skill serve
```
