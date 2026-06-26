---
name: pg-health
description: |
  PostgreSQL database health check tool. Analyzes index health, connection utilization, buffer cache, vacuum status, sequence limits, replication lag, and other key metrics.
  Use when users ask about database health status, performance monitoring, connection count, cache hit rate, or need optimization recommendations.
---

## Feature Description

pg-health provides comprehensive database health checks to help identify potential performance issues and optimization opportunities.

## Execution Flow

### 1. Pre-check

Confirm postgres-mcp MCP tools are available (refer to pre-check in root SKILL.md).

### 2. Execute Health Check

Call `get_database_health` tool to get database health report.

### 3. Analyze Results

Health checks typically include the following dimensions:

#### Index Health
- **Unused indexes** — Indexes that occupy space but are never used by queries
- **Duplicate indexes** — Indexes with redundant functionality that can be merged
- **Missing indexes** — Tables with frequent full table scans may need indexes
- **Index bloat** — Index size exceeds actual needs, requires REINDEX

#### Connection Status
- **Active connections** — Connections currently executing queries
- **Idle connections** — Idle but not released connections
- **Connection pool utilization** — Connection count as percentage of max_connections
- **Long-running queries** — Slow queries that may block other operations

#### Buffer Cache
- **Cache hit rate** — shared_buffers hit rate (should be > 95%)
- **Cache size** — Whether current cache configuration is reasonable
- **Dirty page ratio** — Number of dirty pages that need to be written to disk

#### Vacuum Status
- **Auto vacuum status** — Whether running normally
- **Dead tuple count** — Expired data that needs cleanup
- **Table bloat** — Table size exceeds actual needs
- **Transaction ID wraparound risk** — Tables approaching wraparound

#### Replication Status (if replication is configured)
- **Replication lag** — Lag time between primary and standby
- **Replication slot status** — Whether replication slots are normal
- **WAL accumulation** — Whether WAL logs are accumulating

#### Sequence Status
- **Sequence usage** — Sequences approaching limits (may cause insert failures)

### 4. Generate Report

Organize health check results into a readable report, including:

1. **Overall score** — Overall assessment of database health
2. **Critical issues** — Issues requiring immediate attention (red warnings)
3. **Optimization recommendations** — Areas that can be improved (yellow tips)
4. **Normal metrics** — Parts running well (green)

### 5. Provide Recommendations

Based on discovered issues, provide specific optimization recommendations:

- **Index issues** → Recommend removing unused indexes, merging duplicate indexes, adding missing indexes
- **Connection issues** → Recommend adjusting connection pool configuration, closing idle connections, optimizing slow queries
- **Cache issues** → Recommend adjusting shared_buffers size
- **Vacuum issues** → Recommend manual VACUUM, adjusting autovacuum parameters
- **Replication issues** → Recommend checking network, optimizing replication configuration
- **Sequence issues** → Recommend changing sequence type from integer to bigint

## Usage Examples

**Basic health check**:
```
User: Check database health status
Assistant: [Call get_database_health]
          [Analyze results and generate report]
```

**Targeted check**:
```
User: Why is the database connection count so high?
Assistant: [Call get_database_health]
          [Focus on analyzing connection status section]
```

**Regular monitoring**:
```
User: Check database health every day at 9 AM
Assistant: [Set up scheduled task to execute health check daily]
```

## Report Format Example

```
📊 Database Health Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Overall Status: Good (85/100)

🔴 Critical Issues:
  • Table users has 3 unused indexes, wasting 2.5GB space
  • Connection count near limit (95/100), may cause new connection failures

🟡 Optimization Recommendations:
  • Cache hit rate 92%, recommend increasing shared_buffers
  • Table orders needs VACUUM, dead tuple ratio 15%

✅ Running Normally:
  • Replication lag < 1s
  • No long-running queries
  • Sequence usage normal
```

## Notes

1. **Permission requirements** — Health checks need access to system views (pg_stat_*), ensure database user has sufficient permissions
2. **Performance impact** — Health checks execute some queries, use cautiously during high load periods
3. **Regular checks** — Recommend executing health checks regularly (daily or weekly) to discover issues early
4. **Combine with monitoring** — Health checks are snapshots, recommend combining with continuous monitoring tools (like Prometheus + Grafana)
