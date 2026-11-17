---
title: Partitioning Reference
tier: 3
tags: [ddl, partitioning, list, range, hash, hashpoint, time-series-partition, relational-partition, partition-key]
---

# Partitioning Reference

Quick reference for KWDB partitioning. Read when designing partitions.

## Partition Types

| Type | Applies To | Use When |
|------|------------|----------|
| LIST | Relational | Categorical values (region, type) |
| RANGE | Relational | Time ranges, numeric ranges |
| HASH | Relational | Even distribution, no hotspots |
| HASHPOINT | Time-Series | Partition by tag values |

## Syntax Quick Reference

### LIST (Relational)

```sql
PARTITION BY LIST (column) (
  PARTITION name VALUES IN ('a', 'b'),
  PARTITION other VALUES IN (DEFAULT)
)
```

### RANGE (Relational)

```sql
-- NOTE: partition column (sale_date) MUST be first in primary key
CREATE TABLE partitioned_sales (
    id UUID DEFAULT gen_random_uuid(),
    product_name VARCHAR(200) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    sale_date DATE NOT NULL,
    region VARCHAR(50) NOT NULL,
    PRIMARY KEY (sale_date, id)  -- sale_date first!
) PARTITION BY RANGE (sale_date) (
    PARTITION jan2024 VALUES FROM ('2024-01-01') TO ('2024-02-01'),
    PARTITION feb2024 VALUES FROM ('2024-02-01') TO ('2024-03-01'),
    PARTITION future VALUES IN (MAXVALUE)
);
```

**Wrong:**
```sql
-- PK is (id), but partition by sale_date → ERROR
CREATE TABLE sales (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    sale_date DATE NOT NULL
) PARTITION BY RANGE (sale_date) (...)
-- ERROR: declared partition columns (sale_date) do not match
--         first 1 columns in index being partitioned (id)
```

### HASH (Relational)

```sql
PARTITION BY HASH (column) (
  PARTITION p0 VALUES IN (0),
  PARTITION p1 VALUES IN (1)
)
```

### HASHPOINT (Time-Series)

> **已验证**: `VALUES IN` 必须使用方括号 `[]`，不能用圆括号 `()`。圆括号 `VALUES IN (...)` 是 `PARTITION BY HASH`（关系型表）的语法，用于 HASHPOINT 会报语法错误。来源：`kwbase/pkg/sql/parser/sql.y:6176`。

```sql
-- 正确：方括号 []（HASHPOINT 专属）
ALTER TABLE t PARTITION BY HASHPOINT (
  PARTITION p1 VALUES IN [0],
  PARTITION p2 VALUES IN [1],
  PARTITION p3 VALUES IN [2]
);

-- 也支持范围语法（圆括号，用于 FROM/TO）
ALTER TABLE t PARTITION BY HASHPOINT (
  PARTITION p1 VALUES FROM (0) TO (100),
  PARTITION p2 VALUES FROM (100) TO (200)
);

-- 错误：圆括号用于 VALUES IN 会报 syntax error
-- ALTER TABLE t PARTITION BY HASHPOINT (
--   PARTITION p1 VALUES IN (0),  -- ERROR: at or near "(": syntax error
-- );
```

## When to Use

| Choose... | When... |
|-----------|---------|
| LIST | Data has known categories, queries filter by category |
| RANGE | Time-based data, need to drop old partitions easily |
| HASH | Hot spots on sequential IDs, need even distribution |
| HASHPOINT | TS table, want to group by device/sensor type |

## Key Rules

1. **Partition key MUST be first column(s) of primary key** (Relational)
   - If PK is `(id)`, you cannot partition by `sale_date`
   - Must change PK to `(sale_date, id)` to partition by `sale_date`
   - Example error: `ERROR: declared partition columns (sale_date) do not match first 1 columns in index being partitioned (id)`
2. **RANGE boundaries**: lower INCLUSIVE, upper EXCLUSIVE
3. **Use MAXVALUE** for catch-all partitions
4. **Number of partitions**: 4-16 typical (not too many)

## Common Mistakes

1. **HASH on timestamp** → Use RANGE for time data
2. **Too many partitions** → 100+ partitions is excessive
3. **Partition key not in PK prefix** → Error: "declared partition columns do not match first N columns in index being partitioned"
4. **Missing catch-all** → Out-of-range values fail

## TS vs Relational

| Aspect | HASHPOINT | HASH |
|--------|-----------|------|
| Partition Key | Tag values | Any column |
| Only TS tables? | Yes | No (Relational only) |
| Groups | Devices/sensors | N/A |

## Design Checklist

- [ ] Partition type matches access pattern
- [ ] Partition key is first in primary key
- [ ] Number of partitions is reasonable
- [ ] Catch-all partition exists (or explicit ranges cover all values)
