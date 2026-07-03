# Schema-Level Performance Tuning

> **Note**: Schema changes (CREATE TABLE, ALTER TABLE) belong to `kwdb-schema-design` skill.
> This document provides query-side context only. For DDL changes, delegate to kwdb-schema-design.

## Time-Series Table Properties

Time-series tables have specific WITH options that affect performance:

### ts_partition_interval

Controls how time data is physically partitioned.

```sql
-- View current setting
SHOW CREATE TABLE sensor_data;
```

**Guidelines:**

| Write Rate | Partition Interval | Reason |
|------------|-------------------|--------|
| > 1M rows/sec | 15min or 1h | Prevents oversized files |
| 100K-1M rows/sec | 1h or 6h | Balance management overhead |
| < 100K rows/sec | 6h or 1d | Reduce partition count |

**Trade-offs:**
- Too small: Many small files, metadata overhead
- Too large: Longer scan times per partition

> **Schema change**: Adjusting partition interval requires ALTER TABLE. Delegate to `kwdb-schema-design`.

### ttl_duration

Automatically removes old data to control table size. Delegate TTL changes to `kwdb-schema-design`.

**Benefits:**
- Automatic data cleanup
- Prevents table bloat
- Reduces backup size

### DICT_ENCODING

Compresses high-cardinality string columns. Configure at table creation time.

**Best for:**
- High-cardinality strings (error codes, message IDs)
- Strings with limited unique values
- Repeated string values

**Not for:**
- Low-cardinality (yes/no, status)
- Unique identifiers (UUIDs)

> **Schema change**: DICT_ENCODING must be set at table creation. Delegate table creation to `kwdb-schema-design`.

## Primary Tag Selection

Tags define query dimensions. Choose wisely at creation.

**Good Tag Selection:**
- Query dimension: filter by device and location
- Primary tag enables exact match queries (O(1) hash index)
- Max 4 primary tags per table

**Bad Tag Selection:**
- Timestamp as tag: wrong, ts is already partitioned
- High-cardinality value as tag (e.g., error_message with millions of unique values)
- Tag you'll never filter on

## Relational Table Partitioning

For relational tables, KWDB supports LIST, RANGE, and HASH partitioning.

> **Schema change**: Partitioning strategy is set at table creation. Delegate to `kwdb-schema-design`.

### LIST Partitioning Example
- Suitable for: categorical data (regions, categories)
- Example: Partition by region (Asia, EMEA, Americas)

### RANGE Partitioning Example
- Suitable for: time-series data with date columns
- Example: Partition by quarter or year

### HASH Partitioning Example
- Suitable for: evenly distributed data
- Example: Partition by user_id modulo

## Index Strategy for Relational Tables

Indexes are for RELATIONAL tables only. Time-series tables do NOT support secondary indexes.

### Single Column Index
```sql
CREATE INDEX idx_orders_user ON orders(user_id);
```

### Composite Index
Column order matters! For `WHERE user_id = 123 AND status = 'pending'`, use `INDEX (user_id, status)`.

> **Schema change**: Creating indexes on relational tables. Delegate to `kwdb-schema-design`.

## Schema Review Checklist

```sql
-- Time-Series Tables
SHOW CREATE TABLE sensor_data;

-- Check:
-- 1. ts_partition_interval appropriate for data volume?
-- 2. ttl_duration set for data lifecycle?
-- 3. DICT_ENCODING used for high-cardinality strings?
-- 4. PRIMARY TAGS match common query filters?
```

## When to Modify Schema

**Consider schema changes when:**
- Query patterns change significantly
- Write rate increases 10x+
- Data retention requirements change
- New query dimensions emerge

**Avoid schema changes when:**
- Just for one ad-hoc query
- Temporary analysis need
- Can solve with query rewrite

> **Action**: For any schema changes (CREATE TABLE, ALTER TABLE, CREATE INDEX), delegate to `kwdb-schema-design` skill.
