---
title: View Reference
tier: 3
tags: [ddl, view, materialized-view, refresh, create-view, drop-view, query-simplification]
---

# View Reference

Quick reference for KWDB views. Read when user asks about views or materialized views.

## View vs Materialized View

| Feature | View | Materialized View |
|---------|------|-------------------|
| Data storage | No (query result) | Yes (cached) |
| Query performance | Slower (executes each time) | Faster (pre-computed) |
| Data freshness | Always current | Stale until refreshed |
| DML support | Yes (through view) | No (read-only) |

## Time-Series Table Limitation

**TS 表不支持 VIEW 和 MATERIALIZED VIEW**:
- 不能在 TS 表上创建 VIEW 或 MATERIALIZED VIEW
- 不能在 TS 数据库中创建任何 VIEW
- **Error**: `ERROR: create view is not supported in timeseries table` / `ERROR: create view is not supported in timeseries databases`
- **Workaround**:
  1. 直接用 SQL 查询（支持跨库 JOIN，如 `FROM hft_ts.public.tick_data t JOIN hft_meta.public.securities s ON ...`）
  2. 在关系型库中创建聚合结果表，由应用层或定时任务写入预计算结果

## VIEW

### CREATE VIEW

```sql
CREATE VIEW view_name AS
SELECT column1, column2
FROM table_name
WHERE condition;
```

### DROP VIEW

```sql
DROP VIEW view_name;
DROP VIEW IF EXISTS view_name;
```

## MATERIALIZED VIEW

### CREATE

```sql
CREATE MATERIALIZED VIEW mv_name AS
SELECT col1, SUM(col2) as total
FROM table_name
GROUP BY col1;
```

### REFRESH

```sql
REFRESH MATERIALIZED VIEW mv_name;  -- Full refresh
```

### DROP

```sql
DROP MATERIALIZED VIEW mv_name;
```

## Common Use Cases

| Use Case | Solution |
|----------|----------|
| Simplify complex queries | VIEW |
| Pre-aggregate for reporting | MATERIALIZED VIEW |
| Hide sensitive columns | VIEW |
| Cache expensive aggregations | MATERIALIZED VIEW |

## Index on Materialized View

```sql
CREATE MATERIALIZED VIEW order_summary AS
SELECT customer_id, COUNT(*) as order_count, SUM(total) as total_amount
FROM orders
GROUP BY customer_id;

CREATE INDEX ON order_summary (customer_id);
```

## When to Use

- **VIEW**: When data should always reflect base table state
- **MATERIALIZED VIEW**: When query is expensive and data can be slightly stale

## Validation

```sql
SHOW TABLES;              -- Shows both views and tables
SHOW CREATE VIEW v_name;
SHOW CREATE MATERIALIZED VIEW mv_name;
```

## Design Checklist

- [ ] View or materialized view appropriate for use case
- [ ] View name descriptive
- [ ] Materialized view refresh strategy defined
- [ ] Indexes added to materialized view if needed
