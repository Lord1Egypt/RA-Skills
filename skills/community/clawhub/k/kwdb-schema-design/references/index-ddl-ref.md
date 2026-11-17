---
title: Index DDL Reference
tier: 2
tags: [ddl, create-index, drop-index, composite-index, covering-index, storing, tag-index, time-series-index, fk-index, btree, gin]
---

# Index DDL Reference

Quick reference for KWDB index operations. Read when adding or modifying indexes.

## CREATE INDEX

```sql
-- Single column
CREATE INDEX idx_name ON table_name (column);

-- Composite (multi-column)
CREATE INDEX idx_name ON table_name (col1, col2);

-- Unique
CREATE UNIQUE INDEX idx_name ON table_name (column);

-- Covering (with STORING columns)
CREATE INDEX idx_name ON table_name (col1) STORING (col2, col3);

-- Function-based
CREATE INDEX idx_name ON table_name (abs(column));

-- Inverted (JSONB)
CREATE INDEX idx_name ON table_name USING GIN (jsonb_column);
-- or
CREATE INVERTED INDEX idx_name ON table_name (jsonb_column);
```

## DROP INDEX

```sql
DROP INDEX table_name@index_name;           -- Error if not exists
DROP INDEX IF EXISTS table_name@index_name; -- Silent if not exists
DROP INDEX table_name@index_name CASCADE;   -- Drop dependent objects
```

## ALTER INDEX

```sql
-- Rename
ALTER INDEX table_name@old_idx RENAME TO new_idx;

-- Split at row (for performance)
ALTER INDEX table_name@idx_name SPLIT AT SELECT col FROM table_name;
```

## SHOW INDEX

```sql
SHOW INDEX FROM table_name;
```

Output columns: table_name, index_name, non_unique, seq_in_index, column_name, direction, storing, implicit

## When to Add Index

**Add index when column appears in**:
- WHERE clause
- JOIN condition
- ORDER BY
- GROUP BY

**Do NOT add index when**:
- Column has low selectivity (boolean, status codes with few values)
- Table is small (< 1000 rows)
- Query returns > 10% of table

## Index Types

| Type | Syntax | Use When |
|------|--------|----------|
| B-tree (default) | `USING BTREE` | Equality, range queries |
| Composite | `(col1, col2)` | Multi-column filters |
| Covering | `STORING (col)` | SELECT columns not in WHERE |
| Unique | `UNIQUE INDEX` | Enforce uniqueness |
| Function | `(abs(col))` | Computed column access |
| Inverted | `USING GIN` | JSONB full-text search |

## Time-Series Tag Index

```sql
-- Tag index for TS table queries filtering by tag
CREATE INDEX ON ts_table (tag_column);
```

**TS Tag Index Rules**:
- Only on tags (max 4 primary tags)
- Supported tag types: INT2, INT4, INT8, FLOAT4, FLOAT8, CHAR, NCHAR, BOOL
- NOT supported: VARCHAR, NVARCHAR (ERROR: "creating index on tag with type varchar/varbytes is not supported in timeseries table")
- No index on: TIMESTAMP, GEOMETRY, FLOAT primary tags
- **Always check existing indexes first** (`SHOW INDEX FROM table_name`) — UNIQUE constraints and FK auto-indexes may already cover the column

## Composite Index Column Order

```
(col1, col2) -- Use when:
- Query filters by col1 AND col2
- Query filters by col1 only

(col2, col1) -- Wrong order for above queries
```

**Rule**: Put high-selectivity column first.

## Covering Index Example

```sql
-- Query: SELECT name, price FROM products WHERE category = 'electronics'
-- Instead of scanning table, index covers all columns:

CREATE INDEX idx_products_category ON products (category) STORING (name, price);
```

## Validation

```sql
-- Verify index exists
SHOW INDEX FROM table_name;

-- Verify index is used (check query plan)
EXPLAIN SELECT * FROM table_name WHERE col = 'value';
```

## Common Mistakes

### Error vs Correct Examples

**Incorrect (index on low-cardinality):**
```sql
CREATE INDEX idx_users_active ON users (is_active);  -- Boolean: only 2 values
CREATE INDEX idx_orders_status ON orders (status);    -- 3-5 statuses: low selectivity
```

**Correct:**
```sql
-- No index on boolean/status columns (low cardinality)
-- Only index if combined with high-cardinality column:
CREATE INDEX idx_orders_customer_status ON orders (customer_id, status);
```

**Incorrect (wrong composite order):**
```sql
-- Query: SELECT * FROM orders WHERE customer_id = 'x' AND created_at > '2025-01-01'
CREATE INDEX idx_orders ON orders (created_at, customer_id);  -- Wrong order
```

**Correct:**
```sql
-- Put equality filter first, range filter second
CREATE INDEX idx_orders ON orders (customer_id, created_at);
```

**Incorrect (FK without index):**
```sql
CREATE TABLE order_items (
    order_id UUID NOT NULL REFERENCES orders(id),  -- FK column not indexed
    product_id UUID NOT NULL REFERENCES products(id) -- FK column not indexed
);
```

**Correct:**
```sql
-- KWDB 会为 FK 列自动创建索引（命名: <table>_auto_index_<fk_name>）
-- 因此无需手动为 FK 列再建索引，否则会重复
CREATE TABLE order_items (
    order_id UUID NOT NULL REFERENCES orders(id),
    product_id UUID NOT NULL REFERENCES products(id)
);
-- 用 SHOW INDEX FROM order_items; 确认自动索引已存在
-- 仅当自动索引不满足查询模式时（如需要复合索引），才手动添加
```

### Mistake Summary

| Wrong | Right | Impact |
|-------|-------|--------|
| Index on boolean/low-cardinality | Skip or combine with selective column | 索引无用，浪费写入 |
| `INDEX ON ts (k_timestamp)` | Not needed | TS 表 timestamp 自动索引 |
| `INDEX ON ts (GEOMETRY)` | Not supported | TS 表不支持 |
| `INDEX ON ts (varchar_tag)` | Not supported | VARCHAR/NVARCHAR tag 不支持索引，改用 CHAR 或用 INT 编码 |
| `(created_at, customer_id)` for `WHERE customer_id = ?` | `(customer_id, created_at)` | 复合索引列顺序错误，索引不被使用 |
| Index every column | Only WHERE/JOIN/ORDER BY columns | 过多索引降低写入性能 |
| Random index name `idx1` | `idx_tablename_column` | 命名不清难以维护 |
| Forget FK index | Always check `SHOW INDEX` first | KWDB 为 FK 列自动创建 `<table>_auto_index_<fk_name>` |
| Create index on UNIQUE column | Check `SHOW INDEX` first | UNIQUE 约束已自动创建索引，重复建索引无意义 |
| Duplicate FK index | Check `SHOW INDEX` before creating | FK 自动索引已存在，手动再建产生冗余索引 |

## Design Checklist

- [ ] Query patterns analyzed
- [ ] Index column selectivity evaluated
- [ ] Composite index column order correct
- [ ] Covering index for SELECT optimization
- [ ] FK columns indexed
- [ ] Index name follows convention
