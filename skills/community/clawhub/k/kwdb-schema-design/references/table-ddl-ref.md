---
title: Table DDL Reference
tier: 2
tags: [ddl, create-table, alter-table, drop-table, time-series-table, tags, primary-tags, retention, k_timestamp, relational-table]
---

# Table DDL Reference

Quick reference for KWDB table DDL. Read when creating, altering, or dropping tables.

## CREATE TABLE (Relational)

```sql
CREATE TABLE table_name (
    column_name TYPE [NULL|NOT NULL] [DEFAULT expr] [COMMENT 'text'],
    ...,
    [CONSTRAINT name PRIMARY KEY (col1, col2)]
    [CONSTRAINT name FOREIGN KEY (col) REFERENCES other_table(col)]
    [CONSTRAINT name CHECK (condition)]
    [INDEX idx_name (col1, col2)]
) [PARTITION BY ...];
```

**Common Types**: INT4, INT8, DECIMAL(p,s), VARCHAR(n), BOOL, TIMESTAMPTZ, JSONB, UUID

**Primary Key Options**:
- `INT8 DEFAULT unique_rowid()` - Auto-generated (recommended for single table)
- `UUID DEFAULT gen_random_uuid()` - For distributed systems
- `INT4` or explicit column - When natural key exists

**Key Points**:
- Auto-adds `rowid INT8` hidden PK if no PK defined
- JSONB supports `INVERTED INDEX` for full-text search
- Column-level constraints move to table-level in `SHOW CREATE`

## ALTER TABLE

| Operation | Syntax |
|-----------|--------|
| Add column | `ALTER TABLE t ADD COLUMN col TYPE [DEFAULT val]` |
| Drop column | `ALTER TABLE t DROP COLUMN col` |
| Rename column | `ALTER TABLE t RENAME COLUMN old TO new` |
| Alter column type | `ALTER TABLE t ALTER COLUMN col TYPE new_type` |
| Add constraint | `ALTER TABLE t ADD CONSTRAINT name CHECK (...)` |
| Drop constraint | `ALTER TABLE t DROP CONSTRAINT name` |
| Rename table | `ALTER TABLE t RENAME TO new_name` |
| Set retention (TS) | `ALTER TABLE t SET RETENTIONS = 30d` |

**TS Table Specific**:
- `ADD TAG tag_name TYPE` - Add tag (NOT primary tag)
- `DROP TAG tag_name` - Remove tag
- `RENAME TAG old TO new` - Rename tag

## DROP TABLE

```sql
DROP TABLE table_name;              -- Error if not exists
DROP TABLE IF EXISTS table_name;    -- Silent if not exists
DROP TABLE t1, t2, t3;             -- Multiple tables (relational only)
DROP TABLE t CASCADE;               -- Drop + dependent objects
```

**Time-Series Limitation**: `DROP TABLE t1, t2, t3` is NOT supported for time-series tables. Drop them one at a time: `DROP TABLE t1; DROP TABLE t2;`.

**CASCADE** drops: views referencing this table, foreign key constraints

**FK Dependency Error**:
```sql
-- Error: table referenced by foreign key
DROP TABLE warehouses;
-- ERROR: "warehouses" is referenced by foreign key from table "inventory"

-- Solution: use CASCADE (drops referencing FK constraints, NOT the referencing table)
DROP TABLE warehouses CASCADE;
-- Or drop referencing table first: DROP TABLE inventory; DROP TABLE warehouses;
```

## Time-Series Table Syntax

> **Prerequisite**: Time-series tables MUST be created in a TS database (`CREATE TS DATABASE`). Creating a time-series table in a relational database will fail with `ERROR: can not create timeseries table in relational database`. Use `SHOW DATABASES;` to verify the database type before creating tables.

```sql
CREATE TABLE sensor_data (
    k_timestamp TIMESTAMPTZ(3) NOT NULL,  -- Timestamp (ms precision)
    temperature FLOAT8 NOT NULL,
    humidity FLOAT8 NULL
) TAGS (
    sensor_id INT4 NOT NULL,
    location VARCHAR(50) NULL
) PRIMARY TAGS (sensor_id)
RETENTIONS 180d;
```

**Key Differences from Relational**:
- First column MUST be timestamp
- Tags defined in `TAGS (...)` clause
- Primary tags via `PRIMARY TAGS (tag1, tag2)` - max 4
- Retention via `RETENTIONS 180d` (default: 0s = permanent)

**Tag Types**:
- Supported: INT2, INT4, INT8, FLOAT4, FLOAT8, CHAR, VARCHAR, BOOL
- NOT supported: UUID, DATE, TIMESTAMPTZ, DECIMAL, JSONB, ARRAY
- Workaround: Use VARCHAR for dates (e.g., `'2024-01-15'`), INT for UUIDs

**Data Column Types (TS 表)**:
- Supported: INT2, INT4, INT8, FLOAT4, FLOAT8, CHAR, VARCHAR, BOOL, TIMESTAMP, TIMESTAMPTZ
- NOT supported: DECIMAL, NUMERIC, JSONB, UUID, ARRAY, GEOMETRY, BYTES
- **Why**: TS 存储引擎面向数值型测量值优化，不支持精确小数和复杂类型
- **Workaround**: 价格等需要精确计算的字段改用 FLOAT8（约 15 位有效数字），或存入关系型表用 DECIMAL
- **Error**: `ERROR: column xxx: unsupported column type decimal in timeseries table`

**TS 表不支持 CHECK 约束**:
- **Error**: `ERROR: check constraint is not supported in timeseries table`
- **Workaround**: 在应用层校验，或仅用 CHAR(1)/BOOL 等类型隐式约束取值范围

**Timestamp Precision** (first column):
- `TIMESTAMPTZ(3)` — millisecond (default, suitable for most IoT scenarios)
- `TIMESTAMPTZ(6)` — microsecond (high-frequency trading, industrial control)
- `TIMESTAMPTZ(9)` — nanosecond (scientific instruments, ultra-low-latency)

## Validation

```sql
SHOW CREATE TABLE table_name;  -- Verify DDL
SHOW COLUMNS FROM table_name;  -- Verify columns
SHOW TAGS FROM table_name;     -- TS: verify tags
SHOW RETENTIONS ON TABLE t;    -- TS: verify retention
```

## When to Use

| Use Case | Table Type |
|----------|------------|
| Business entities (users, orders, products) | Relational |
| Sensor/metrics with timestamp | Time-Series |
| Mixed: entity metadata + measurements | Mixed (2 tables + JOIN) |
| Audit logs, activity history | Time-Series |
| Config/policy/master data | Relational |

## Common Mistakes

### Relational Table Mistakes

| Wrong | Right | Why |
|-------|-------|-----|
| `CREATE TABLE t (name VARCHAR)` | `CREATE TABLE t (name VARCHAR(100))` | VARCHAR 必须指定长度 |
| `price FLOAT` | `price DECIMAL(12,2)` | FLOAT 有精度损失 |
| `id VARCHAR(36)` | `id UUID DEFAULT gen_random_uuid()` | UUID 类型索引性能更好 |
| No PK defined | `id INT8 DEFAULT unique_rowid() PRIMARY KEY` | 无 PK 会隐藏 rowid |

### Time-Series Table Mistakes

| Wrong | Right | Why |
|-------|-------|-----|
| `CREATE TABLE t (id INT, ts TIMESTAMPTZ, ...)` | First column = timestamp | TS 表第一列必须是 timestamp |
| `RETENTIONS 30` | `RETENTIONS 30d` | 必须指定时间单位 |
| `PRIMARY TAGS (location)` where location is FLOAT | Only INT/CHAR/VARCHAR tags | 主标签不支持 FLOAT |
| `TAGS (ts TIMESTAMPTZ, ...)` | Tags only: INT/FLOAT/CHAR/VARCHAR | Tags 不支持 TIMESTAMPTZ |
| No RETENTIONS on high-volume table | `RETENTIONS 180d` | 无 retention 数据无限增长 |
| `price DECIMAL(18,4)` in TS table | `price FLOAT8` | TS 表不支持 DECIMAL 数据列 |
| `CHECK (status IN (...))` in TS table | Remove CHECK, validate in app | TS 表不支持 CHECK 约束 |
| `id INT4 DEFAULT unique_rowid()` | `id INT8 DEFAULT unique_rowid()` | unique_rowid() 返回 INT8，与 INT4 类型不匹配 |

### Error vs Correct Examples

**Incorrect (relational):**
```sql
CREATE TABLE orders (
    id VARCHAR(50),
    amount FLOAT,
    status INT
);
```

**Correct (relational):**
```sql
CREATE TABLE orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Incorrect (time-series):**
```sql
CREATE TABLE sensor (
    sensor_id INT NOT NULL,
    ts TIMESTAMPTZ NOT NULL,
    temperature FLOAT
);
```

**Correct (time-series):**
```sql
CREATE TABLE sensor (
    ts TIMESTAMPTZ(3) NOT NULL,
    temperature FLOAT4 NOT NULL
) TAGS (
    sensor_id INT4 NOT NULL
) PRIMARY TAGS (sensor_id)
RETENTIONS 180d;
```

## Design Checklist

- [ ] Workload type classified (relational/ts/mixed)
- [ ] Column types appropriate for data semantics
- [ ] Primary key strategy decided
- [ ] NOT NULL for required fields
- [ ] Retention stated (time-series)
- [ ] Validation steps included
