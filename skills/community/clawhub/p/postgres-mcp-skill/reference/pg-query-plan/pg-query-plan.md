---
name: pg-query-plan
description: |
  PostgreSQL query execution plan analysis tool. Analyzes query performance through EXPLAIN, identifies bottlenecks, and simulates hypothetical index impact.
  Use when users ask why queries are slow, how to optimize queries, want to see execution plans, or analyze query performance.
---

## Feature Description

pg-query-plan helps understand query execution process, identify performance bottlenecks, and provide optimization recommendations.

## Execution Flow

### 1. Pre-check

Confirm postgres-mcp MCP tools are available (refer to pre-check in root SKILL.md).

### 2. Get Query

User provides SQL query that needs analysis.

### 3. Execute EXPLAIN

Use `analyze_query_plan` or similar MCP tool to get query execution plan.

Multiple EXPLAIN options available:

#### EXPLAIN (Basic)
```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
```
- Shows query plan but doesn't actually execute
- Cost estimates based on statistics

#### EXPLAIN ANALYZE (Recommended)
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```
- Actually executes query and collects real data
- Shows actual execution time and row counts
- **Note**: Will actually execute query, be careful with write operations

#### EXPLAIN (ANALYZE, BUFFERS)
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 123;
```
- Additionally shows buffer usage
- Helps identify I/O bottlenecks

#### EXPLAIN (ANALYZE, VERBOSE)
```sql
EXPLAIN (ANALYZE, VERBOSE) SELECT * FROM orders WHERE user_id = 123;
```
- Shows more detailed information
- Includes output columns, filter conditions, etc.

### 4. Analyze Execution Plan

Interpret execution plan and identify performance issues:

#### Common Node Types

**Scan Nodes**:
- **Seq Scan (Sequential Scan)** — Full table scan, slow on large tables
- **Index Scan** — Uses index, usually fast
- **Index Only Scan** — Only reads index, doesn't access table, fastest
- **Bitmap Index Scan** — Bitmap index scan, suitable for returning multiple rows

**Join Nodes**:
- **Nested Loop** — Nested loop, fast for small table joins
- **Hash Join** — Hash join, fast for large table joins
- **Merge Join** — Merge join, fast for sorted data

**Aggregate Nodes**:
- **Aggregate** — Aggregate operations (SUM, COUNT, etc.)
- **GroupAggregate** — Group aggregation
- **HashAggregate** — Hash aggregation

**Sort Nodes**:
- **Sort** — In-memory sort
- **Sort (external merge)** — Disk sort, very slow

#### Key Metrics

**Cost**:
- `cost=0.00..100.00` — Startup cost..total cost
- Cost is relative value, used to compare different plans

**Rows**:
- `rows=1000` — Estimated rows returned
- If significantly different from actual, statistics are outdated

**Actual Time**:
- `actual time=0.123..45.678` — Actual execution time (milliseconds)
- Only shown in EXPLAIN ANALYZE

**Buffers**:
- `Buffers: shared hit=100 read=50` — Cache hits and disk reads
- High `hit` means good cache, high `read` means I/O bottleneck

### 5. Identify Performance Bottlenecks

Identify issues based on execution plan:

#### Full Table Scan
```
Seq Scan on orders  (cost=0.00..10000.00 rows=100000)
  Filter: (user_id = 123)
```
**Issue**: Full table scan on large table
**Recommendation**: Create index on user_id

#### Sort Spilling to Disk
```
Sort  (cost=5000.00..5500.00 rows=100000)
  Sort Method: external merge  Disk: 12345kB
```
**Issue**: Insufficient memory, sort uses disk
**Recommendation**: Increase work_mem or optimize query to reduce sort data

#### Nested Loop Join on Large Tables
```
Nested Loop  (cost=0.00..1000000.00 rows=1000000)
  -> Seq Scan on orders
  -> Index Scan on users
```
**Issue**: Nested loop inefficient on large tables
**Recommendation**: Consider Hash Join or add indexes

#### Inaccurate Statistics
```
Hash Join  (cost=100.00..200.00 rows=100)
  (actual time=1000.00..2000.00 rows=100000)
```
**Issue**: Estimated 100 rows, actual 100000 rows
**Recommendation**: Run ANALYZE to update statistics

#### Low Cache Hit Rate
```
Buffers: shared hit=10 read=1000
```
**Issue**: Lots of disk reads
**Recommendation**: Increase shared_buffers or optimize query

### 6. Generate Analysis Report

Organize execution plan analysis into a readable report:

```
🔍 Query Execution Plan Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Query:
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending'

⏱️ Execution Time: 2.5 seconds

🔴 Performance Bottlenecks:

1. Full table scan on orders table
   • Scanned 1,000,000 rows, only returned 100 rows
   • Cost: 10000.00
   • Recommendation: Create index on (user_id, status)

2. Low cache hit rate
   • Cache hits: 10 blocks
   • Disk reads: 1000 blocks
   • Recommendation: Increase shared_buffers or optimize query

💡 Optimization Recommendations:

CREATE INDEX idx_orders_user_status
ON orders(user_id, status);

Expected result: Query time from 2.5s to 0.1s (96% speedup)
```

### 7. Simulate Hypothetical Indexes

Predict index effects without actually creating them:

```sql
-- Create hypothetical index
SELECT * FROM hypopg_create_index(
  'CREATE INDEX ON orders(user_id, status)'
);

-- View execution plan using hypothetical index
EXPLAIN SELECT * FROM orders
WHERE user_id = 123 AND status = 'pending';

-- Clean up hypothetical indexes
SELECT hypopg_reset();
```

### 8. Provide Optimization Recommendations

Based on analysis results, provide specific optimization recommendations:

**Index Optimization**:
- Add missing indexes
- Use covering indexes (Index Only Scan)
- Consider partial or expression indexes

**Query Rewriting**:
- Avoid SELECT *, only query needed columns
- Use EXISTS instead of IN (subquery)
- Break complex queries into multiple simple queries

**Configuration Tuning**:
- Increase work_mem (sorting, hashing)
- Increase shared_buffers (caching)
- Adjust random_page_cost (SSD)

**Statistics**:
- Run ANALYZE to update statistics
- Increase statistics target (ALTER TABLE ... ALTER COLUMN ... SET STATISTICS)

## Usage Examples

**Basic analysis**:
```
User: Why is this query so slow?
     SELECT * FROM orders WHERE user_id = 123

Assistant: [Execute EXPLAIN ANALYZE]
     [Analyze execution plan]
     Found issue: Full table scan on orders table
     Recommendation: Create index CREATE INDEX ON orders(user_id)
```

**Compare before/after optimization**:
```
User: How much performance improvement after creating the index?

Assistant: [Compare execution plans before and after optimization]
     Before optimization: Seq Scan, 2.5s
     After optimization: Index Scan, 0.1s
     Speedup: 96%
```

**Complex query analysis**:
```
User: This JOIN query is slow, help me check

Assistant: [Analyze multi-table join execution plan]
     [Identify join order, join method]
     [Provide optimization recommendations]
```

## Visualization Tools

Recommend using visualization tools for more intuitive execution plan viewing:

- **explain.depesz.com** — Online execution plan visualization
- **explain.dalibo.com** — Another online tool
- **pgAdmin** — Graphical execution plan
- **DataGrip** — IDE built-in execution plan visualization

## Notes

1. **EXPLAIN ANALYZE actually executes** — Be careful with write operations (UPDATE, DELETE)
2. **Use transaction rollback** — When analyzing write operations use BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;
3. **Statistics must be accurate** — Run ANALYZE regularly to keep statistics current
4. **Production environment caution** — EXPLAIN ANALYZE consumes resources, avoid during peak hours
5. **Cache effects** — First execution and subsequent executions may differ (cache warming)

## Related Commands

```sql
-- Update statistics
ANALYZE orders;

-- View table statistics
SELECT * FROM pg_stats WHERE tablename = 'orders';

-- View index usage
SELECT * FROM pg_stat_user_indexes WHERE relname = 'orders';

-- Reset query statistics
SELECT pg_stat_reset();
```
