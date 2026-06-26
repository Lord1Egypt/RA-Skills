# GraphCare: Structural Database Health Scanner

Your database has hidden structural problems that silently degrade performance and break integrity. GraphCare is the only MCP tool on ClawHub that scans your schema topology — without ever reading a single row of your data.

## The Problem

AI agents create tables, add columns, and evolve schemas at speed. But they don't audit structure. Over time:
- Foreign keys lose their indexes (JOINs slow to a crawl)
- Tables drift into isolation (orphaned, unreachable data)
- Primary keys go missing (replication breaks, ORMs fail)
- Nullable FKs create silent referential gaps
- Circular dependencies make inserts impossible without disabling constraints
- Redundant indexes waste disk and slow writes

GraphCare catches all of this in one scan.

## Zero-Trust by Design

GraphCare only queries your database's metadata (`information_schema`, `PRAGMA`, `pg_indexes`). It is **structurally impossible** for GraphCare to read, leak, or mutate your row data.

- **READ-ONLY**: Zero writes, zero mutations
- **NO ROW DATA**: Only schema metadata is accessed
- **STATELESS**: Memory purged after every scan

## What GraphCare Detects

| Finding | Severity | What It Means |
|---------|----------|---------------|
| **Orphaned Tables** | Warning | Tables with no FK relationships — structurally isolated dead weight |
| **Missing FK Indexes** | Critical | FK columns without indexes — the #1 cause of slow JOINs and DELETEs |
| **No Primary Key** | Critical | Tables that can't guarantee row uniqueness — breaks replication and ORMs |
| **Nullable Foreign Keys** | Warning | Optional relationships that hide referential integrity gaps |
| **Circular Dependencies** | Warning | FK cycles that make clean inserts impossible |
| **Duplicate Indexes** | Info | Redundant indexes wasting disk space and slowing writes |

## Two Tools

### `audit_db_structure(connection_string)`

Full structural scan. Returns a JSON report with all findings, per-table breakdown, and a computed **health score** (0-100).

### `explain_finding(finding_type, context?)`

Plain-language explanation of any finding type. Severity, impact, and recommended fix — ready for your agent to act on.

## Supported Databases

- **PostgreSQL** — Full detection suite (6 finding types)
- **MySQL** — Full detection suite (6 finding types)
- **SQLite** — Full detection suite (6 finding types)

## How It Works

```
1. Your agent calls audit_db_structure("postgresql://...")
2. GraphCare reads only metadata (information_schema, pg_indexes, PRAGMA)
3. Returns structured JSON: findings[], metrics{}, health_score
4. Server purges all state — zero persistence
```

## Pricing

- **Single Audit**: $50 per scan
- **Continuous Protection (Pro)**: $130/month for automated recurring scans

---

*Built by Mind Protocol.*
