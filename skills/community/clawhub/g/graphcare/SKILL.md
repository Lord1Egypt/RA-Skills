---
name: graphcare
description: "Structural database health scanner. Audits schema topology for orphaned tables, missing indexes, nullable FKs, circular dependencies — without ever reading row data. Supports PostgreSQL, MySQL, SQLite."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
      env: []
    emoji: "\U0001F6E1"
    homepage: https://github.com/mind-protocol/graphcare
---

# GraphCare — Structural Database Health Scanner

The first structural antivirus for AI databases. Scans your schema topology for hidden problems — **without ever touching your data**.

## Why

AI agents evolve schemas at speed. But nobody audits the structure. Over time:

- Foreign keys lose their indexes (JOINs slow to a crawl)
- Tables drift into isolation (orphaned, unreachable data)
- Primary keys go missing (replication breaks, ORMs fail)
- Nullable FKs create silent referential gaps
- Circular dependencies make inserts impossible
- Redundant indexes waste disk and slow writes

GraphCare catches all of this in one scan.

## Zero-Trust by Design

GraphCare only queries metadata (`information_schema`, `PRAGMA`, `pg_indexes`). It is **structurally impossible** for it to read, leak, or mutate your row data.

- **READ-ONLY**: Zero writes, zero mutations
- **NO ROW DATA**: Only schema metadata is accessed
- **STATELESS**: Memory purged after every scan

## Setup

GraphCare is an MCP server. Add it to your MCP client config:

```json
{
  "mcpServers": {
    "graphcare": {
      "command": "node",
      "args": ["/path/to/graphcare/index.js"]
    }
  }
}
```

Or run via Docker:

```bash
docker build -t graphcare .
docker run -i graphcare
```

Or install from npm:

```bash
npm install -g graphcare-mcp
graphcare-mcp
```

## Tools

### `audit_db_structure`

Full structural scan. Pass a connection string, get a complete health report.

**Parameters:**
- `connection_string` (required) — Database URI: `postgresql://`, `mysql://`, `sqlite:///path/to/db`, or just `file.db`

**Returns:** JSON report with:
- `db_type` — Database engine detected
- `tables[]` — All tables found
- `findings[]` — Each structural issue with type, severity, table, and message
- `metrics{}` — Counts per finding type + computed `health_score` (0-100)

**Example:**

```
Use graphcare to audit my database at postgresql://localhost:5432/myapp
```

The agent calls `audit_db_structure` with the connection string and receives a structured JSON report.

### `explain_finding`

Plain-language explanation of any finding type. Includes severity, impact, and recommended fix.

**Parameters:**
- `finding_type` (required) — One of: `orphaned_table`, `missing_fk_index`, `duplicate_index`, `nullable_fk`, `no_primary_key`, `circular_dependency`
- `context` (optional) — Table or column name for specific advice

## What GraphCare Detects

| Finding | Severity | Impact |
|---------|----------|--------|
| Orphaned Tables | Warning | Structurally isolated dead weight |
| Missing FK Indexes | Critical | #1 cause of slow JOINs and DELETEs |
| No Primary Key | Critical | Breaks replication and ORMs |
| Nullable Foreign Keys | Warning | Hidden referential integrity gaps |
| Circular Dependencies | Warning | Makes clean inserts impossible |
| Duplicate Indexes | Info | Wasted disk, slower writes |

## Supported Databases

- **PostgreSQL** — Full 6-finding detection via `information_schema` + `pg_indexes`
- **MySQL** — Full detection via `information_schema`
- **SQLite** — Full detection via `sqlite_master` + `PRAGMA`

## Security

This tool runs read-only queries against database metadata catalogs only. It never executes `SELECT` on user tables, never writes, and holds no state between invocations. Connection strings are received via MCP JSON-RPC over stdin — never exposed in process listings.

---

*Built by [Mind Protocol](https://mindprotocol.ai).*
