---
name: pg-index-tuning
description: |
  PostgreSQL index optimization tool. Uses industrial-grade algorithms to explore thousands of possible index combinations to find the best indexing solution for workloads.
  Use when users mention slow queries, index optimization, performance tuning, queries too slow, or need to add indexes.
---

## Feature Description

pg-index-tuning uses advanced index optimization algorithms to analyze query workloads and recommend optimal indexing solutions.

## Execution Flow

### 1. Pre-check

Confirm postgres-mcp MCP tools are available (refer to pre-check in root SKILL.md).

### 2. Collect Workload

Two ways to collect queries that need optimization:

#### Method 1: User provides specific queries

User directly provides SQL queries that need optimization.

```
User: This query is too slow, help me optimize it
     SELECT * FROM orders WHERE user_id = 123 AND status = 'pending'
```

#### Method 2: Analyze slow query logs

If database has slow query logging enabled, can get slowest queries from `pg_stat_statements` view.

```sql
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### 3. Call Index Optimization Tool

Use `suggest_indexes` or similar MCP tool to analyze queries and recommend indexes.

Input parameters:
- **Query list** — SQL queries that need optimization
- **Workload weights** — Execution frequency of each query (optional)
- **Constraints** — Maximum number of indexes, maximum index size, etc. (optional)

### 4. Analyze Recommendations

Index optimization tool will return:

#### Recommended Indexes
- **Index definition** — CREATE INDEX statement
- **Expected benefit** — Query performance improvement percentage
- **Index size** — Estimated disk space usage
- **Affected queries** — Which queries will use this index

#### Before/After Comparison
- **Current performance** — Query execution time before optimization
- **Optimized performance** — Expected execution time after adding index
- **Performance improvement** — Improvement percentage

#### Cost Analysis
- **Space cost** — Total size of all recommended indexes
- **Maintenance cost** — Impact of indexes on write operations
- **Benefit** — Overall query performance improvement

### 5. Generate Optimization Plan

Organize recommendations into a clear optimization plan:

```
🎯 Index Optimization Plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Current Issues:
  • Query A: Average 2.5s, full table scan on orders table
  • Query B: Average 1.8s, full table scan on users table

💡 Recommended Indexes:

1. CREATE INDEX idx_orders_user_status
   ON orders(user_id, status);

   Benefit: Query A speeds up 95% (2.5s → 0.12s)
   Cost: ~150MB disk space

2. CREATE INDEX idx_users_email
   ON users(email);

   Benefit: Query B speeds up 90% (1.8s → 0.18s)
   Cost: ~80MB disk space

📈 Overall Effect:
  • Query performance improvement: 92%
  • Disk space usage: 230MB
  • Write operation impact: ~5% performance decrease
```

### 6. Execution Confirmation

Before actually creating indexes, ask user for confirmation:

1. **Show complete CREATE INDEX statements**
2. **Explain expected benefits and costs**
3. **Remind that index creation may take considerable time** (large tables)
4. **Recommend executing during off-peak hours** (production environment)

After user confirmation, can:
- Execute CREATE INDEX directly (if have permissions)
- Generate SQL script for user to execute manually
- Use `CONCURRENTLY` option to avoid table locking (PostgreSQL 11+)

### 7. Verify Results

After index creation, verify optimization results:

1. **Re-execute queries** — Compare execution time before and after optimization
2. **Check index usage** — Confirm queries actually use new indexes
3. **Monitor performance** — Observe for a period to ensure no side effects

## Advanced Features

### Hypothetical Indexes

Simulate index impact on query plans without actually creating indexes:

```sql
-- Create hypothetical index
SELECT * FROM hypopg_create_index('CREATE INDEX ON orders(user_id)');

-- View query plan
EXPLAIN SELECT * FROM orders WHERE user_id = 123;

-- Clean up hypothetical indexes
SELECT hypopg_reset();
```

### Multi-Query Optimization

Optimize multiple queries simultaneously to find optimal index combination:

```
User: Optimize these queries
     Query 1: SELECT * FROM orders WHERE user_id = ?
     Query 2: SELECT * FROM orders WHERE status = ?
     Query 3: SELECT * FROM orders WHERE user_id = ? AND status = ?
Assistant: [Analyze queries]
     Found that creating a composite index (user_id, status)
     can optimize all three queries simultaneously
```

### Index Maintenance Recommendations

Besides adding new indexes, can also:

- **Remove unused indexes** — Free up space, reduce write operation overhead
- **Rebuild bloated indexes** — REINDEX to restore performance
- **Merge duplicate indexes** — Remove functionally redundant indexes

## Usage Examples

**Single query optimization**:
```
User: This query is too slow
     SELECT * FROM orders WHERE user_id = 123 AND created_at > '2024-01-01'
     
Assistant: [Analyze query]
     Recommend creating index:
     CREATE INDEX idx_orders_user_created 
     ON orders(user_id, created_at);
     
     Expected 90% speedup, create it?
```

**Workload optimization**:
```
User: Analyze slow queries from the past week and provide optimization recommendations

Assistant: [Get slow queries from pg_stat_statements]
     [Call index optimization tool]
     [Generate comprehensive optimization plan]
```

## Notes

1. **Indexes are not a silver bullet** — Too many indexes affect write performance, need to balance
2. **Composite index order** — Index column order matters, follow "high selectivity columns first" principle
3. **Partial indexes** — For queries with obvious filter conditions, consider partial indexes to save space
4. **Expression indexes** — For function calls (like LOWER(email)), consider expression indexes
5. **CONCURRENTLY** — Use CONCURRENTLY when creating indexes in production to avoid table locking
6. **Monitor results** — Continuously monitor after index creation to ensure expected results

## Related Tools

- **pg_stat_statements** — Query statistics extension
- **hypopg** — Hypothetical index extension
- **pg_qualstats** — Query condition statistics
- **PoWA** — PostgreSQL Workload Analyzer
