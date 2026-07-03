---
name: kwdb-performance-review
description: |
  Optimize SQL query performance for KaiwuDB time-series and relational engines.
  Covers: EXPLAIN analysis, time-series optimization, pagination, cross-model queries.
  Trigger keywords: optimize query, slow query, explain, execution plan, performance, 性能, 查询优化.
  NOT for: DDL, schema design, deployment, DML writes.
version: 0.2.0
---

Read the required reference files first.

## Tiered Reference Architecture

**Tier 1 (Always Read)**
- `references/key-rules.md` - Core engine differences and anti-patterns
- `references/query-analysis.md` - EXPLAIN output interpretation

**Tier 2 (High-Frequency Optimization)**
- `references/timeseries-optimization.md` - Time-series query patterns
- `references/pagination-optimization.md` - Cursor-based pagination

**Tier 3 (Medium-Frequency)**
- `references/relational-optimization.md` - B-tree indexes, join optimization
- `references/cross-model-optimization.md` - Hybrid query optimization

**Tier 4 (Low-Frequency)**
- `references/schema-tuning.md` - Partition interval, TTL, encoding
- `references/index-analysis.md` - Index review for relational tables
- `references/config-optimization.md` - Storage configuration parameter optimization

## When to Activate

**Should trigger:**
- "optimize this query" / "优化查询"
- "slow query" / "查询很慢" / "慢查询"
- "explain this query" / "执行计划"
- "query performance" / "查询性能"
- "KWDB query slow"
- "全表扫描" / "查询超时"
- "时序数据查询慢" / "传感器数据"
- "TIME_BUCKET" / "时间聚合"
- "索引优化" (relational tables only)
- "config optimization" / "配置优化"
- "parameter tuning" / "参数调优"
- "存储配置" / "参数调整"

**Should NOT trigger:**
- Schema design ("create table", "add index") → kwdb-schema-design
- Deployment/configuration questions
- DML write optimization ("fast INSERT")
- Non-KWDB databases

## Engine Detection

Before optimizing, determine which engine the query targets:

```
TIME SERIES TABLE:
  - Has ts_column, primary_tags in CREATE TABLE
  - Cannot have secondary indexes
  - Query must include time range filter
  - Primary tag filter uses hash index

RELATIONAL TABLE:
  - Standard SQL table
  - Can have B-tree, inverted indexes
  - Standard SQL optimization applies
```

Ask user if unclear.

## Workflow

### Step 1: Parse EXPLAIN Output

Key indicators to look for:

| Pattern | Time-Series | Relational | Action |
|---------|-------------|------------|--------|
| Partition Filter: ts | Good | N/A | Time pruning working |
| Tag Filter: tag_col | Good | N/A | Hash index hit |
| Seq Scan in partition | Normal | Check size | Normal for small |
| Index Scan | N/A | Good | Index being used |
| Distribute: Shuffle | Warning | Varies | Cross-node traffic |

### Step 2: Identify Anti-Patterns

**Time-Series Critical Issues:**
- Missing time range filter -> full partition scan
- Fuzzy match on primary tag (LIKE, SUBSTRING) -> hash index miss
- SELECT * -> unnecessary column IO
- Large OFFSET pagination -> memory pressure
- Manual GROUP BY instead of TIME_BUCKET

**Relational Issues:**
- Seq Scan on large table -> missing index
- Nested loop on large sets -> bad join order
- Missing index on join column

### Step 3: Provide Optimized Query

Always provide:
1. The anti-pattern being fixed
2. The rewritten query
3. Expected improvement in EXPLAIN

### Step 4: Validate

Include `EXPLAIN (ANALYZE)` to verify the optimization works.

### Step 5: Configuration Optimization (Conditional)

Only activate when:
1. User explicitly mentions "config optimization" / "parameter tuning" / "配置优化" / "参数调优", OR
2. SQL optimization steps (1-4) are exhausted and performance issues persist

**Per-Parameter Trigger (review on demand, not full scan):**

| Parameter | Config Group | Trigger Condition |
|-----------|-------------|-------------------|
| ts.compress.stage | Compression Group | User wants compression optimization or smaller disk space usage |
| ts.compress.algorithm | Compression Group | User wants compression optimization or smaller disk space usage |
| ts.compress.level | Compression Group | User wants compression optimization or smaller disk space usage |
| ts.rows_per_block.min_limit | Rows Per Block Group | User reports excessive small blocks from flushing, long write visibility delay, or high per-device data volume with low compression ratio |
| ts.rows_per_block.max_limit | Rows Per Block Group | User reports excessive small blocks from flushing, long write visibility delay, or high per-device data volume with low compression ratio |
| ts.compress.last_segment.enabled | Independent | User wants compression optimization or smaller disk space usage, or needs to optimize write performance |
| ts.block.lru_cache.max_limit | Independent | User wants to optimize overall query performance, or memory usage is too high |
| ts.last_cache_size.max_limit | Independent | User wants to optimize last-related SQL query performance, or memory usage is too high |
| ts.mem_segment_size.max_limit | Independent | Write performance optimization (after ts.compress.last_segment.enabled reviewed), or memory usage is too high (after ts.block.lru_cache.max_limit and ts.last_cache_size.max_limit reviewed) |
| ts.reserved_last_segment.max_limit | Independent | Frequent compaction triggers or disk space is tight |
| ts.compact.max_limit | Independent | User reports compaction backlog with significant CPU idle, or CPU usage is too high |
| ts.auto_vacuum.enabled | Independent | User wants to clean up data |
| ts.block_filter.sampling_ratio | Independent | User reports poor query performance with range conditions or null checks, suspects inefficient filter pushdown |

**Decision Tree:**

1. Compression optimization / disk space reduction → Compression Group
   - Performance priority, disk sufficient → snappy/lz4, level=any, stage=1; extreme: stage=0
   - Disk space priority, CPU sufficient → zstd, level=high, stage=3
   - CPU usage too high → lz4, level=any, stage=1; if still high → stage=0
2. Excessive small blocks / write visibility delay / low compression ratio → Rows Per Block Group
   - High-throughput write → increase max (8192-16384)
   - Memory constrained → decrease max (2048)
   - Point queries → decrease max
   - Sequential scan → increase max
   - Low-latency small batch → increase min (1024+)
3. Write performance → ts.compress.last_segment.enabled (SSD: false, HDD: true)
4. Query performance / high memory → ts.block.lru_cache.max_limit
5. Last query performance / high memory → ts.last_cache_size.max_limit
6. Write performance (after #3) / high memory (after #4,#5) → ts.mem_segment_size.max_limit
7. Frequent compaction / disk tight → ts.reserved_last_segment.max_limit
8. Compaction backlog / high CPU → ts.compact.max_limit
9. Data cleanup → ts.auto_vacuum.enabled
10. Poor filter pushdown → ts.block_filter.sampling_ratio

**Pre-conditions (confirm relevant resources before suggesting):**
- Memory-related params: confirm available free memory with user
- Disk-related params: confirm available disk space with user
- CPU-related params: confirm CPU availability with user

Read `references/config-optimization.md` for detailed parameter guidance.
See `assets/example-configs.md` for configuration tuning examples.

**Config query approach:**
- Use MCP tool if available: `mcp__kwdb__read-query("SHOW CLUSTER SETTING ts.xxx")`
- Otherwise, ask user to run: `SHOW CLUSTER SETTING ts.xxx;`
- NEVER use `SHOW CLUSTER SETTINGS`

**Important:**
- NEVER execute `SET CLUSTER SETTING` automatically
- Only provide SQL statements for user to review and execute

## NOT for

- **DDL operations**: Creating/dropping tables, indexes (→ kwdb-schema-design)
- **Deployment/Config**: Memory settings, installation, replication
- **Write optimization**: Bulk INSERT, import performance
- **Data migration**: Moving data between databases
- **Hardware sizing**: Server specs, disk I/O recommendations
- **Application tuning**: Connection pooling, caching (beyond SQL)

## Guardrails

1. **Never suggest CREATE INDEX on time-series tables** - they don't support secondary indexes
2. **Time-series queries MUST have time range filters** - warn if missing
3. **Never recommend OFFSET for deep pagination** - use time-based cursor
4. **Always specify SELECT columns** for time-series - no SELECT *
5. **Verify table type before index recommendations**
6. **Explain WHY the optimization works** - not just what to change
7. **Validate with EXPLAIN** before finishing
8. **Confirm memory and disk before config changes** - never suggest cache/memory size increases without confirmed free resources
9. **Never auto-execute SET CLUSTER SETTING** - only provide SQL for user to review
10. **Never use SHOW CLUSTER SETTINGS** - always query specific settings individually
11. **Resource overload reduce warning** - when recommending reduced values for memory/CPU-impact parameters, always include the risk warning about potential performance degradation

## Output Format

```markdown
## Intent
[Brief description of the optimization goal]

## Engine Type
[time-series / relational / mixed]

## Anti-Pattern Detected
[What was causing the slowness]

## Original Query
```sql
[query before optimization]
```

## Optimized Query
```sql
[rewritten query]
```

## Expected Improvement
[What should change in EXPLAIN]

## Validation
```sql
EXPLAIN (ANALYZE) [optimized query];
```
```

For configuration optimization output format, see `assets/config-output-template.md`.
