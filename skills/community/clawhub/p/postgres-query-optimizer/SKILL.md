---
name: cm-postgres-query-optimizer
description: Analyze slow PostgreSQL queries, interpret EXPLAIN ANALYZE output, identify performance bottlenecks, and recommend indexes, query rewrites, and configuration tuning. Parses query plans to find sequential scans, nested loops on large tables, poor join ordering, and missing indexes. Use when asked to optimize a SQL query, analyze a slow query, read EXPLAIN output, suggest PostgreSQL indexes, tune a query plan, fix a slow database query, or improve query performance. Triggers on "slow query", "query optimization", "EXPLAIN ANALYZE", "PostgreSQL performance", "query plan", "sequential scan", "index suggestion", "postgres tuning", "query optimizer", "database performance", "slow SQL", "pg_stat".
metadata:
  tags: ["postgresql", "sql", "query-optimization", "database", "performance", "indexing", "explain-analyze", "dba", "backend"]
---

# PostgreSQL Query Optimizer

Analyze slow PostgreSQL queries by interpreting EXPLAIN ANALYZE output, identifying performance bottlenecks, recommending indexes, suggesting query rewrites, and providing configuration tuning advice. Acts as an expert DBA reviewing your query plans.

## Usage

Invoke this skill when you have a slow PostgreSQL query and need to understand why it is slow and how to fix it.

**Basic invocation:**
> Optimize this query: SELECT * FROM orders WHERE created_at > '2026-01-01' AND status = 'pending'
> Analyze this EXPLAIN ANALYZE output: [paste output]
> Why is this query slow? [paste query and/or plan]

**With context:**
> Here's my table schema and the slow query, suggest indexes
> I have this query plan, explain what each node means and where the bottleneck is
> This query takes 12 seconds, target is under 200ms — help me get there

The agent analyzes the query, the execution plan (if provided), and the table schema to produce actionable optimization recommendations.

## How It Works

### Step 1: Understand the Query and Context

The agent first reads the SQL query and gathers context:

- **Parse the query**: identify tables, joins, WHERE conditions, GROUP BY, ORDER BY, subqueries, CTEs, window functions
- **Identify table schemas**: ask for or look up `\d table_name` output to understand columns, types, existing indexes, constraints, and foreign keys
- **Check table statistics**: if available, review row counts, data distribution, and bloat

```sql
-- The agent may ask you to run these for additional context:
\d+ table_name                           -- Schema with sizes
SELECT reltuples::bigint FROM pg_class WHERE relname = 'table_name';  -- Row count
SELECT * FROM pg_stats WHERE tablename = 'table_name' AND attname = 'column';  -- Column stats

-- Or check existing indexes:
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'table_name';

-- Check table bloat:
SELECT pg_size_pretty(pg_total_relation_size('table_name')) AS total_size,
       pg_size_pretty(pg_relation_size('table_name')) AS table_size,
       pg_size_pretty(pg_indexes_size('table_name')) AS index_size;
```

### Step 2: Analyze the EXPLAIN ANALYZE Output

If the user provides EXPLAIN ANALYZE output, the agent performs deep analysis on each node. If not provided, the agent will request it or reason about the likely plan.

```sql
-- The agent recommends running:
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) <your query>;

-- For even more detail:
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS, WAL, FORMAT TEXT) <your query>;
```

**Node-by-node analysis:**

The agent reads the execution plan tree and evaluates each node:

| Node Type | What the Agent Checks |
|-----------|----------------------|
| **Seq Scan** | Table size — is it justified or should it use an index? Checks filter selectivity. |
| **Index Scan** | Is it the right index? Could a covering index avoid heap fetches? |
| **Index Only Scan** | Checks visibility map freshness (heap fetches indicate need for VACUUM). |
| **Bitmap Index Scan** | Evaluates if multiple indexes are being combined inefficiently. |
| **Nested Loop** | Acceptable for small outer sets; flags when outer is large (O(n*m) risk). |
| **Hash Join** | Checks work_mem adequacy — are hash batches spilling to disk? |
| **Merge Join** | Verifies pre-sorted inputs; checks if sort is the real bottleneck. |
| **Sort** | Disk sort vs. in-memory? Could an index provide pre-sorted data? |
| **Aggregate** | HashAggregate vs. GroupAggregate efficiency. |
| **Materialize** | Identifies unnecessary re-execution of subplans. |
| **SubPlan** | Correlated subqueries — often the #1 performance killer. |

**Key metrics the agent extracts:**

```
Node: Sort
  Actual Time: 1,247ms (89% of total query time) <-- BOTTLENECK IDENTIFIED
  Rows: 1,200,000
  Sort Method: external merge  <-- DISK SORT (work_mem too low)
  Sort Space Used: 98MB
  Recommendation: Increase work_mem to 128MB or add index on sort columns
```

### Step 3: Identify Performance Bottlenecks

The agent ranks bottlenecks by impact:

**1. Sequential Scans on Large Tables**

```
PROBLEM: Seq Scan on orders (rows=2,400,000)
  Filter: (status = 'pending' AND created_at > '2026-01-01')
  Rows Removed by Filter: 2,350,000
  Selectivity: 2.1% — an index would be beneficial

SOLUTION: CREATE INDEX idx_orders_status_created
  ON orders (status, created_at)
  WHERE status = 'pending';  -- Partial index if status='pending' is the common query
```

**2. Nested Loops with Large Outer Sets**

```
PROBLEM: Nested Loop (outer rows=50,000, inner rows=200 per loop)
  Total inner executions: 50,000 * index scan = 10,000,000 row lookups

SOLUTION: Consider rewriting as a Hash Join:
  - Ensure inner table has sufficient statistics (ANALYZE)
  - Check join_collapse_limit if many tables
  - Explicit JOIN hints via CTE restructuring
```

**3. Disk Sorts and Spills**

```
PROBLEM: Sort Method: external merge  Disk: 245MB
  work_mem is 4MB, sort needs 245MB

SOLUTION:
  - SET work_mem = '256MB' (for this session/query)
  - Or add index: CREATE INDEX idx_orders_created ON orders (created_at DESC)
  - Use LIMIT + subquery pattern if only top-N results needed
```

**4. Correlated Subqueries**

```
PROBLEM: SubPlan executing once per outer row
  SELECT *, (SELECT max(amount) FROM payments p WHERE p.order_id = o.id)
  FROM orders o;
  -- SubPlan executes 500,000 times

SOLUTION: Rewrite as JOIN:
  SELECT o.*, p.max_amount
  FROM orders o
  LEFT JOIN (SELECT order_id, max(amount) AS max_amount
             FROM payments GROUP BY order_id) p
  ON p.order_id = o.id;
```

**5. Poor Statistics and Cardinality Misestimates**

```
PROBLEM: Estimated rows=100, Actual rows=450,000
  Planner chose Nested Loop based on bad estimate

SOLUTION:
  - ANALYZE table_name;  -- Refresh statistics
  - ALTER TABLE table_name ALTER COLUMN col SET STATISTICS 1000;
  - Check for correlated columns: CREATE STATISTICS
```

### Step 4: Recommend Indexes

The agent recommends indexes based on the query patterns:

**Index recommendation logic:**

1. **Equality conditions first** in composite indexes (`WHERE status = 'active'`)
2. **Range conditions second** (`WHERE created_at > '2026-01-01'`)
3. **ORDER BY columns** as trailing index columns when possible
4. **INCLUDE columns** for covering indexes to avoid heap fetches
5. **Partial indexes** when queries always filter on a specific value
6. **Expression indexes** for function calls in WHERE clauses

```sql
-- Composite index for common query pattern
CREATE INDEX idx_orders_status_created_at
  ON orders (status, created_at DESC);

-- Covering index to enable Index Only Scan
CREATE INDEX idx_orders_covering
  ON orders (status, created_at DESC)
  INCLUDE (total_amount, customer_id);

-- Partial index for hot path
CREATE INDEX idx_orders_pending
  ON orders (created_at DESC)
  WHERE status = 'pending';

-- Expression index for computed filters
CREATE INDEX idx_users_lower_email
  ON users (lower(email));

-- GIN index for JSONB queries
CREATE INDEX idx_events_metadata
  ON events USING gin (metadata jsonb_path_ops);

-- BRIN index for append-only time-series tables
CREATE INDEX idx_logs_created
  ON application_logs USING brin (created_at);
```

**Index cost-benefit analysis:**

The agent estimates:
- Write overhead: each index adds ~10-15% write latency
- Storage cost: approximate index size based on column types and row count
- Read improvement: expected speedup from Seq Scan to Index Scan
- Whether the index will actually be used (based on selectivity and planner behavior)

### Step 5: Suggest Query Rewrites

The agent suggests structural improvements:

**Common rewrites:**

| Pattern | Problem | Rewrite |
|---------|---------|---------|
| `SELECT *` | Fetches unnecessary columns | Select only needed columns |
| `WHERE col IN (SELECT ...)` | Correlated subquery | `JOIN` or `EXISTS` |
| `DISTINCT` on large sets | Full sort/hash required | `GROUP BY` or redesign |
| `OFFSET 10000 LIMIT 20` | Scans 10,020 rows | Keyset pagination |
| `OR` across columns | Prevents index use | `UNION ALL` |
| `NOT IN (SELECT ...)` | Poor NULL handling, slow | `NOT EXISTS` |
| `COUNT(*)` on large table | Full scan | Approximate count or caching |
| `ORDER BY random()` | Full sort | `TABLESAMPLE` |
| Function in `WHERE` | Prevents index use | Expression index or precompute |

**Example rewrite — pagination:**

```sql
-- SLOW: Offset-based pagination
SELECT * FROM events ORDER BY id LIMIT 20 OFFSET 500000;
-- Scans and discards 500,000 rows

-- FAST: Keyset pagination
SELECT * FROM events WHERE id > 500000 ORDER BY id LIMIT 20;
-- Index seek directly to the right position
```

### Step 6: Configuration Tuning

The agent checks whether PostgreSQL configuration contributes to the problem:

```sql
-- Key settings the agent evaluates:
SHOW work_mem;              -- Sort/hash memory (default 4MB is often too low)
SHOW shared_buffers;        -- Should be ~25% of RAM
SHOW effective_cache_size;  -- Should be ~50-75% of RAM
SHOW random_page_cost;      -- 1.1 for SSD, 4.0 for HDD
SHOW effective_io_concurrency; -- 200 for SSD, 2 for HDD
SHOW max_parallel_workers_per_gather; -- Parallel query workers
SHOW jit;                   -- JIT compilation (can hurt short queries)
```

**Common configuration recommendations:**

```
FINDING: work_mem = 4MB, but your query sorts 245MB of data
  RECOMMENDATION: SET work_mem = '256MB' for this session
  NOTE: Don't set globally too high — multiply by max_connections

FINDING: random_page_cost = 4.0, but you're on SSD
  RECOMMENDATION: SET random_page_cost = 1.1
  IMPACT: Planner will prefer index scans over sequential scans

FINDING: effective_cache_size = 4GB, but server has 32GB RAM
  RECOMMENDATION: SET effective_cache_size = '24GB'
  IMPACT: Planner will trust that data is likely cached
```

### Step 7: Produce the Optimization Report

The agent delivers a structured report:

```
# Query Optimization Report

## Query
SELECT o.id, o.total, c.name
FROM orders o JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending' AND o.created_at > '2026-01-01'
ORDER BY o.created_at DESC LIMIT 50;

## Current Performance
  Execution time: 3,847ms
  Planning time: 2.1ms
  Rows returned: 50
  Rows scanned: 2,400,000 (48,000x more than returned)

## Bottlenecks (ranked by impact)
  1. Sequential scan on orders (2.4M rows) — 78% of query time
  2. Sort on created_at — spills to disk due to low work_mem
  3. No issue with join (customers table is small, hash join is fine)

## Recommendations
  1. CREATE INDEX idx_orders_pending_created
     ON orders (created_at DESC)
     WHERE status = 'pending';
     Expected improvement: 3,847ms -> ~15ms

  2. SET work_mem = '64MB' (for sort operations)
     Expected improvement: eliminates disk sort

## Expected Result After Optimization
  Index Scan on idx_orders_pending_created -> ~5ms
  Nested Loop with customers -> ~10ms
  No sort needed (index provides order)
  Total: ~15ms (256x improvement)
```

## Output

The agent produces:

- **Query analysis**: parsed breakdown of the query structure
- **Plan interpretation**: plain-English explanation of each EXPLAIN node
- **Bottleneck ranking**: ordered list of performance issues by impact
- **Index recommendations**: specific CREATE INDEX statements with rationale
- **Query rewrites**: alternative SQL that achieves the same result faster
- **Configuration suggestions**: PostgreSQL settings that affect this query
- **Expected improvement**: estimated execution time after optimizations
- **Warnings**: potential risks of recommended changes (write overhead, index bloat, plan regression)

## Common Scenarios

### "My query is slow but I don't know why"
Provide the query and table schema. The agent will explain the likely plan and recommend running EXPLAIN ANALYZE.

### "I have an EXPLAIN ANALYZE output, what does it mean?"
Paste the full output. The agent explains every node, identifies the bottleneck, and suggests fixes.

### "Which indexes should I create for my application?"
Provide the most common queries (or let the agent examine `pg_stat_statements`). The agent recommends a minimal set of indexes that covers the critical paths.

### "My query was fast, now it's slow"
The agent checks for: statistics staleness, table bloat, plan regression after ANALYZE, new data volume crossing planner thresholds, index corruption. Recommends `ANALYZE`, `REINDEX`, or plan pinning.

### "I need to optimize a migration query that touches millions of rows"
The agent recommends batching strategies, temp table patterns, and locking considerations.

## Tips for Best Results

- Always provide `EXPLAIN (ANALYZE, BUFFERS)` output when possible — without it the agent reasons from the query alone
- Include table schemas (`\d+ table_name`) so the agent knows about existing indexes
- Mention the PostgreSQL version — optimizer capabilities vary significantly (e.g., parallel queries, JIT, incremental sort)
- Share the table row counts so the agent can assess selectivity
- If the query runs in an ORM (Django, Rails, SQLAlchemy), share the generated SQL, not the ORM code
- For ongoing optimization, export `pg_stat_statements` output for workload-level analysis
