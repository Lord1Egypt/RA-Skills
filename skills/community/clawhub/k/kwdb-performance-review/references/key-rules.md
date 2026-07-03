# KWDB Performance Optimization: Core Rules

## Fundamental: Two Different Engines

KaiwuDB has two completely separate execution engines with different optimization rules:

### Time-Series Engine

- **Index Constraint**: NO manual secondary indexes allowed
- **Built-in Indexes**: Automatic hash index on PRIMARY TAG columns only
- **Data Organization**: Columnar storage + time partitioning
- **Access Pattern**: Time range scan + tag filter (O(1) hash lookup)
- **Query Must-Haves**:
  - Time range filter (enables partition pruning)
  - Exact equality on primary tag (hits hash index)

### Relational Engine

- **Indexes**: Supports B-tree, inverted, composite indexes
- **Data Organization**: Row store (standard SQL)
- **Access Pattern**: B-tree index scans, sequential scans
- **Standard SQL optimization applies**

## Time-Series Golden Rules

### 1. Partition Pruning (Required)

```
GOOD:  WHERE ts >= '2026-04-01' AND ts < '2026-04-02'
BAD:   No time filter -> full table scan across all partitions
```

### 2. Tag Hash Index (Required for O(1))

```
GOOD:  WHERE device_id = 'D001'        -- exact match, hash index hit
BAD:   WHERE device_id LIKE '%001%'    -- fuzzy, full scan
BAD:   WHERE SUBSTRING(device_id,1,3) = 'D00'  -- function, hash miss
```

### 3. Column Selection (Critical for IO)

```
GOOD:  SELECT ts, temperature FROM sensor_data
BAD:   SELECT * FROM sensor_data  -- reads all columns, wastes IO
```

### 4. Deep Pagination (No OFFSET)

```
GOOD:  WHERE ts > '2026-04-01 12:00:00' ORDER BY ts LIMIT 20
BAD:   LIMIT 10000, 20  -- OFFSET 10000 reads 10020 rows
```

### 5. Time Aggregation

```
GOOD:  SELECT TIME_BUCKET(ts, '1h'), AVG(temp) FROM sensor_data GROUP BY 1
BAD:   SELECT DATE_TRUNC('hour', ts), AVG(temp) FROM sensor_data GROUP BY 1
```

## Relational Engine Rules

### 1. Index Usage

```
GOOD:  WHERE email = 'x@y.com'  -- with index on email
BAD:   WHERE status = 'active'  -- without index, full scan
```

### 2. Join Optimization

```
GOOD:  SELECT * FROM small_table s JOIN large_table l ON s.id = l.s_id
BAD:   SELECT * FROM large_table l JOIN small_table s ON s.id = l.s_id
```

### 3. Composite Index Order

```
For:  WHERE a = 1 AND b = 2
GOOD:  INDEX (a, b)  -- leftmost prefix match
BAD:   INDEX (b, a)  -- cannot use index
```

## Cross-Model Query Rules

### Join Order (Critical)

```
GOOD:  FROM relational_table r JOIN timeseries_table t ON r.id = t.id
       WHERE r.filter_col = 'x' AND t.ts >= '...'  -- filter on small table first
BAD:   FROM timeseries_table t JOIN relational_table r ON t.id = r.id
       WHERE r.filter_col = 'x'  -- scans huge time-series first
```

## Decision Tree

```
Is query on TIME SERIES table?
├── YES -> Must have time range filter?
│         ├── YES -> Is primary tag filter exact equality?
│         │         ├── YES -> Is pagination using cursor (not OFFSET)?
│         │         │         ├── YES -> Is SELECT specifying needed columns (not *)?
│         │         │         │         ├── YES -> Query likely optimized
│         │         │         │         └── NO -> Remove unnecessary columns
│         │         │         └── NO -> Use time-based cursor pagination
│         │         └── NO -> Use exact tag equality, avoid functions/LIKE
│         └── NO -> ADD time range filter (required!)
└── NO (RELATIONAL) -> Is query using index?
          ├── YES -> Is EXPLAIN showing index scan (not seq scan)?
          │         └── YES -> Query likely optimized
          └── NO -> Is large table being scanned?
                    ├── YES -> Consider adding index
                    └── NO -> Sequential scan may be acceptable
```
