---
name: SQL Explainer
description: SQL query performance analyzer. Paste any slow query + EXPLAIN ANALYZE output and get an instant diagnosis: which nodes are bottlenecks, why row estimates are off, which indexes to add (B-tree, GIN, partial, composite), and which query rewrites will help. Works with PostgreSQL, MySQL, and SQLite. Zero external API — pure analysis. Triggers on "slow query", "explain analyze", "optimize sql", "query too slow", "add index", "why is my query slow", "/sql-explainer".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - sql
    - postgresql
    - mysql
    - performance
    - database
    - query-optimization
    - explain-analyze
    - indexing
    - developer-tools
---

# SQL Explainer

Diagnose slow SQL queries in seconds. Paste your EXPLAIN ANALYZE output and get a plain-English breakdown: which nodes are killing performance, why estimates are off, and exactly which indexes or rewrites will fix it.

**Works with PostgreSQL, MySQL, SQLite. No API keys. No config.**

---

## Trigger Phrases

- "slow query", "why is my query slow", "explain this query"
- "explain analyze", "query plan", "execution plan"
- "optimize sql", "add index", "missing index"
- "query taking too long", "database slow"
- "/sql-explainer"

---

## How to Provide Input

Give the agent any combination of:

```
# Option 1: Just paste EXPLAIN ANALYZE output
/sql-explainer
[paste EXPLAIN ANALYZE output here]

# Option 2: Query + EXPLAIN output
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending'

EXPLAIN ANALYZE output:
[paste here]

# Option 3: Just the query (agent will run EXPLAIN ANALYZE if DB is accessible)
/sql-explainer SELECT * FROM orders WHERE user_id = 123

# Option 4: Include table schema for better index suggestions
Table: orders (user_id INT, status VARCHAR, created_at TIMESTAMPTZ, total DECIMAL)
Indexes: PRIMARY KEY (id), INDEX (created_at)
Query: SELECT * FROM orders WHERE user_id = 123 AND status = 'pending'
```

---

## Step 1: Run EXPLAIN ANALYZE

If the user provides a query but no EXPLAIN output, run it:

### PostgreSQL
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';
```

### MySQL
```sql
EXPLAIN FORMAT=JSON
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';

-- Or for runtime stats:
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';
```

### SQLite
```sql
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';
```

---

## Step 2: Parse the Plan Tree

Read the EXPLAIN output as a tree. For each node, extract:

| Field | What to Look For |
|-------|-----------------|
| **Node Type** | Seq Scan = no index used; Index Scan = good; Bitmap Heap Scan = OK for bulk |
| **Cost** | `(cost=startup..total)` — total cost is the bottleneck metric |
| **Rows** | `rows=N` (estimated) vs `actual rows=M` — big gap = stale statistics |
| **Loops** | Nested Loop with `loops=1000` = N+1 problem |
| **Buffers** | `shared read=N` = disk reads; `shared hit=N` = cache; high read = cold cache or missing index |
| **Time** | `actual time=start..end` — where is the wall clock going? |

### Critical Signals to Flag

```
🔴 Seq Scan on large table (> 10K rows estimated)
   → Table is being scanned fully — missing index

🔴 Rows estimated << actual rows (off by 10x+)
   → Stale statistics → run ANALYZE tablename
   → Correlated columns not captured by statistics

🔴 Nested Loop with high loops count (> 100)
   → N+1 query pattern — join condition may be missing index on inner side

🔴 Hash Join with high hash batches (> 1)
   → Spilling to disk — work_mem too low, or query needs refactoring

🟠 Sort with "Sort Method: external merge Disk"
   → Sort spilled to disk → increase work_mem or add covering index

🟠 Filter with high "rows removed by filter" ratio (> 80%)
   → Index exists but predicate not selective enough — consider partial index

🟡 Index Scan with many "heap fetches"
   → Index-Only Scan would be faster — add covering index
```

---

## Step 3: Identify Root Cause

After reading the tree, classify the problem:

### Category A: Missing Index

**Symptoms:**
- `Seq Scan` on a large table
- Filter condition in WHERE clause not covered by any index

**Diagnosis:**
```sql
-- Check what indexes exist on the table
\d tablename  -- PostgreSQL
SHOW INDEXES FROM tablename;  -- MySQL
```

**Typical patterns:**
| Query Pattern | Recommended Index |
|--------------|-------------------|
| `WHERE col = value` | `CREATE INDEX ON t(col)` |
| `WHERE col1 = v AND col2 = v` | Composite: `CREATE INDEX ON t(col1, col2)` |
| `WHERE col = v ORDER BY created_at` | `CREATE INDEX ON t(col, created_at)` |
| `WHERE status IN ('a','b') AND user_id = v` | `CREATE INDEX ON t(user_id, status)` |
| `WHERE email LIKE 'prefix%'` | B-tree works; `WHERE email LIKE '%suffix'` needs `pg_trgm` GIN |
| `WHERE body @@ to_tsquery('word')` | GIN: `CREATE INDEX ON t USING gin(to_tsvector('english', body))` |
| `WHERE deleted_at IS NULL` (most rows) | Partial: `CREATE INDEX ON t(user_id) WHERE deleted_at IS NULL` |

---

### Category B: Stale Statistics

**Symptoms:**
- Planner estimates `rows=5` but actual is `rows=50000`
- Plan looks like it should be fast but isn't

**Fix:**
```sql
ANALYZE tablename;  -- PostgreSQL (updates statistics)
ANALYZE TABLE tablename;  -- MySQL
```

For correlated columns:
```sql
-- PostgreSQL 14+ extended statistics
CREATE STATISTICS s1 ON col1, col2 FROM tablename;
ANALYZE tablename;
```

---

### Category C: N+1 / Nested Loop

**Symptoms:**
- `Nested Loop` with `loops=1000+`
- Hash Join or inner query repeated many times
- Code fetches one row, then queries for related data in a loop

**Fix:**
- Add index on the foreign key / join column in the **inner** table
- Rewrite to use a single JOIN instead of a loop:

```sql
-- Before (N+1): fetch users, then query orders for each
SELECT * FROM users WHERE id = $1;
-- × N times:
SELECT * FROM orders WHERE user_id = $1;

-- After: single JOIN
SELECT u.*, o.*
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.id = $1;
```

---

### Category D: Query Rewrite Needed

**Symptoms:**
- `IN (SELECT ...)` subquery producing full scan
- `OR` condition preventing index use
- `SELECT *` fetching unnecessary columns (prevents Index-Only Scan)

**Common rewrites:**

```sql
-- ❌ Slow: correlated subquery
SELECT * FROM orders
WHERE user_id IN (SELECT id FROM users WHERE country = 'US');

-- ✅ Fast: JOIN
SELECT o.* FROM orders o
JOIN users u ON u.id = o.user_id
WHERE u.country = 'US';

-- ❌ Slow: OR prevents index use
SELECT * FROM events WHERE type = 'click' OR type = 'view';

-- ✅ Fast: UNION ALL
SELECT * FROM events WHERE type = 'click'
UNION ALL
SELECT * FROM events WHERE type = 'view';

-- ❌ Slow: function on indexed column
SELECT * FROM orders WHERE DATE(created_at) = '2026-03-18';

-- ✅ Fast: range scan uses index
SELECT * FROM orders
WHERE created_at >= '2026-03-18' AND created_at < '2026-03-19';

-- ❌ Slow: LIKE with leading wildcard
SELECT * FROM products WHERE name LIKE '%widget%';

-- ✅ Fast: full-text search
SELECT * FROM products WHERE name_vector @@ to_tsquery('widget');
-- Requires: CREATE INDEX ON products USING gin(to_tsvector('english', name));
```

---

### Category E: Configuration Limits

**Symptoms:**
- `Sort Method: external merge Disk`
- `Hash Batches: 4` (spilling to disk)
- Large aggregations are slow

**Fixes (PostgreSQL):**
```sql
-- Increase per-query memory (default 4MB is often too low)
SET work_mem = '64MB';  -- session level
-- In postgresql.conf for permanent change:
-- work_mem = 64MB

-- Check current value
SHOW work_mem;
```

---

## Step 4: Output Report

Always produce this report structure:

```markdown
## SQL Explainer Report
Query: [first 60 chars of query...]
Database: PostgreSQL / MySQL / SQLite
Execution Time: [from EXPLAIN ANALYZE, if available]

### Diagnosis

| Severity | Node | Problem | Impact |
|----------|------|---------|--------|
| 🔴 Critical | Seq Scan on orders (50K rows) | No index on (user_id, status) | 2.1s → <5ms |
| 🟠 High | Stale statistics | Planner estimated 3 rows, got 48K | Wrong plan chosen |
| 🟡 Medium | SELECT * | 42 columns fetched, 3 used | Prevents Index-Only Scan |

---

### Root Cause

[1-2 sentence plain-English explanation of why the query is slow]

---

### Fix Plan (Prioritized)

**Fix 1 — Add composite index (estimated: 2.1s → <5ms)**
```sql
CREATE INDEX CONCURRENTLY idx_orders_user_status
ON orders(user_id, status)
WHERE deleted_at IS NULL;  -- partial index if most rows are soft-deleted
```
Why: Eliminates Seq Scan. CONCURRENTLY means no table lock in production.

**Fix 2 — Update statistics**
```sql
ANALYZE orders;
```
Why: Planner estimated 3 rows, got 48K. Wrong estimate → wrong plan.

**Fix 3 — Select only needed columns**
```sql
-- Before:
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';

-- After (enables Index-Only Scan):
SELECT id, total, created_at FROM orders WHERE user_id = 123 AND status = 'pending';
```

---

### Expected After Fix

| Metric | Before | After |
|--------|--------|-------|
| Execution time | 2.1s | <5ms |
| Node type | Seq Scan | Index Only Scan |
| Rows scanned | 50,000 | 3 |
| Disk reads | 412 | 1 |

---

### Quick Copy-Paste Fix

```sql
-- Run these in order:
CREATE INDEX CONCURRENTLY idx_orders_user_status ON orders(user_id, status) WHERE deleted_at IS NULL;
ANALYZE orders;
```
```

---

## Quick Mode

If user just wants fast feedback:

```
Quick Check: [query first 40 chars...]

🔴 Missing index on orders(user_id, status) — Seq Scan detected
🟠 Stale stats — run ANALYZE orders
🟡 SELECT * fetching 42 cols

Fix: CREATE INDEX ON orders(user_id, status);
Full analysis: /sql-explainer --full [paste EXPLAIN ANALYZE]
```

---

## Index Type Reference

| Use Case | Index Type | Syntax |
|----------|------------|--------|
| Equality, range, ORDER BY | B-tree (default) | `CREATE INDEX ON t(col)` |
| JSON, arrays, full-text | GIN | `CREATE INDEX ON t USING gin(col)` |
| Geometric, PostGIS | GiST | `CREATE INDEX ON t USING gist(col)` |
| Exclude overlapping ranges | BRIN | `CREATE INDEX ON t USING brin(col)` (huge tables only) |
| Many repeated values (few distinct) | — | Don't index; use partial index instead |
| Only index subset of rows | Partial | `CREATE INDEX ON t(col) WHERE condition` |
| Avoid heap fetch entirely | Covering | `CREATE INDEX ON t(a) INCLUDE (b, c)` |

---

## What EXPLAIN ANALYZE Nodes Mean

| Node | Meaning | Red Flag? |
|------|---------|-----------|
| `Seq Scan` | Full table scan | ✅ On tables > 10K rows |
| `Index Scan` | Used an index, then fetched heap rows | Usually fine |
| `Index Only Scan` | Used index, no heap fetch needed | Best case |
| `Bitmap Index Scan` + `Bitmap Heap Scan` | Multiple index ranges merged | OK for bulk |
| `Nested Loop` | For each outer row, scan inner | ✅ if `loops` >> 10 |
| `Hash Join` | Build hash table of smaller side | ✅ if `Hash Batches > 1` |
| `Merge Join` | Both sides pre-sorted | Fine if Sort cost is low |
| `Sort` | Explicit sort step | ✅ if `external merge Disk` |
| `Aggregate` | GROUP BY / COUNT etc. | Fine usually |
| `Limit` | Stops early | Watch `startup cost` |

---

## Why This Doesn't Exist Elsewhere

Most database GUIs (pgAdmin, TablePlus, DBeaver) show you the EXPLAIN output as a tree or graph — they visualize it. But they don't tell you **what to do about it**.

This skill reads the plan like a senior DBA would: identifies the specific bottleneck, explains why it's happening (stale stats, missing index, wrong join type), and gives you the exact SQL to fix it — optimized for your specific query pattern, not a generic "add an index" suggestion.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
