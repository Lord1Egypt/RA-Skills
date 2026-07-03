# Time-Series Query Optimization

## Core Principle: No Secondary Indexes

Time-series tables in KaiwuDB CANNOT have secondary indexes. Performance comes from:
1. **Partition pruning** - time range filter restricts physical data
2. **Hash index on PRIMARY TAG** - O(1) lookup for exact tag match
3. **Columnar storage** - only read needed columns

## Rule 1: Time Range Filter (Mandatory)

Time-series tables are partitioned by time. Without a time filter, you scan ALL partitions.

```sql
-- WRONG: Full table scan across all time partitions
SELECT * FROM sensor_data WHERE device_id = 'D001';

-- CORRECT: Scans only one day's partition
SELECT * FROM sensor_data
WHERE device_id = 'D001'
  AND ts >= '2026-04-01' AND ts < '2026-04-02';

-- BEST: Use NOW() for recent data
SELECT * FROM sensor_data
WHERE device_id = 'D001'
  AND ts >= NOW() - INTERVAL '1 day';
```

### Partition Interval Guidelines

| Write Rate | Partition Size | Reason |
|------------|---------------|--------|
| > 1M rows/sec | 1h | Many small partitions |
| 100K-1M rows/sec | 6h | Moderate partitions |
| < 100K rows/sec | 1d | Larger partitions OK |

## Rule 2: Primary Tag Exact Match (Mandatory for Hash Index)

PRIMARY TAG columns get automatic hash indexes. Only exact equality uses them.

```sql
-- CORRECT: Exact match uses hash index (O(1))
WHERE device_id = 'D001'

-- WRONG: Function prevents hash index usage (full scan)
WHERE SUBSTRING(device_id, 1, 3) = 'D00'

-- WRONG: LIKE prevents hash index usage (full scan)
WHERE device_id LIKE 'D00%'
WHERE device_id LIKE '%001%'  -- cannot use index at all

-- WRONG: Range scan on tag (cannot use hash index efficiently)
WHERE device_id > 'D001' AND device_id < 'D100'
```

### Multi-Tag Queries

If you have multiple PRIMARY TAGS, include all for best performance:

```sql
-- Assuming PRIMARY TAGS (device_id, location)
-- BEST: All tags specified
WHERE device_id = 'D001' AND location = 'Beijing'

-- ACCEPTABLE: Only first tag (uses first tag's hash)
WHERE device_id = 'D001'
```

## Rule 3: SELECT Only Needed Columns

Columnar storage means reading only the columns you need.

```sql
-- WRONG: Reads all columns (wasteful IO)
SELECT * FROM sensor_data WHERE ts >= '2026-04-01';

-- CORRECT: Reads only needed columns
SELECT ts, temperature, humidity
FROM sensor_data
WHERE ts >= '2026-04-01';
```

### Field vs Tag Columns

| Column Type | SELECT Benefit |
|-------------|----------------|
| TAG (string) | Low - tags usually needed |
| FIELD (numeric) | High - many columns, large data |

## Rule 4: Use TIME_BUCKET for Time Grouping

TIME_BUCKET is a specialized function optimized for time-series aggregation.

```sql
-- SLOW: Manual date truncation
SELECT DATE_TRUNC('hour', ts) AS hour, AVG(temp)
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', ts);

-- FAST: TIME_BUCKET (engine-optimized)
SELECT TIME_BUCKET(ts, '1 hour') AS hour, AVG(temp)
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '7 days'
GROUP BY TIME_BUCKET(ts, '1 hour');
```

### TIME_BUCKET Benefits

1. **Pushdown optimization**: Runs in storage engine, not SQL layer
2. **Pre-sorted data**: Time-bucketed data is pre-sorted on disk
3. **Memory efficiency**: Better memory allocation than manual GROUP BY

### TIME_WINDOW (Alternative to TIME_BUCKET)

TIME_WINDOW is another time-based window function:

```sql
-- TIME_WINDOW: groups data by time interval
SELECT count(ts) AS records, avg(speed) AS avg_speed
FROM vehicles
WHERE ts >= '2025-01-10'
GROUP BY TIME_WINDOW(ts, '10m');
```

Supported interval units: ms, s, m, h, d, w, mon, y

### Other Time Window Functions

KaiwuDB supports specialized window functions for time-series analysis:

**COUNT_WINDOW**: Fixed row count per window
```sql
-- Every 3 rows per window, no overlap
SELECT count(ts), avg(speed) FROM vehicles GROUP BY COUNT_WINDOW(3);

-- With sliding offset (overlapping windows)
SELECT count(ts), avg(speed) FROM vehicles GROUP BY COUNT_WINDOW(3, 2);
```

**SESSION_WINDOW**: Groups data by time gap threshold
```sql
-- New window when gap exceeds 5 minutes
SELECT count(ts), avg(speed) FROM vehicles
GROUP BY SESSION_WINDOW(ts, '5m');
```

**STATE_WINDOW**: Groups data by state changes
```sql
-- New window when lane_no changes
SELECT count(ts), avg(speed) FROM vehicles
GROUP BY STATE_WINDOW(lane_no);
```

**EVENT_WINDOW**: Groups data by start/end conditions
```sql
-- Window opens when speed < 40, closes when lane_no = 2
SELECT count(ts), avg(speed) FROM vehicles
GROUP BY EVENT_WINDOW(speed < 40, lane_no = 2);
```

> Note: Window functions require GROUP BY and support only single-table queries.

## Rule 5: Avoid Functions on Time Column

```sql
-- SLOW: Function on time column
WHERE DATE_TRUNC('day', ts) = '2026-04-01'

-- FAST: Direct comparison
WHERE ts >= '2026-04-01' AND ts < '2026-04-02'
```

## Rule 6: Correlated Subqueries

For queries with correlated subqueries, push conditions down:

```sql
-- SLOW: Correlated subquery scans for each row
SELECT * FROM main_table m
WHERE ts >= '2026-04-01'
  AND temp > (SELECT AVG(temp) FROM sensor_data WHERE device_id = m.device_id);

-- FAST: Use JOIN with aggregation
SELECT m.*, avg_temp
FROM main_table m
JOIN (
  SELECT device_id, AVG(temp) AS avg_temp
  FROM sensor_data
  WHERE ts >= '2026-04-01'
  GROUP BY device_id
) s ON m.device_id = s.device_id
WHERE m.ts >= '2026-04-01';
```

## Schema-Level Optimizations

> **Note**: Schema changes (CREATE TABLE, ALTER TABLE) belong to `kwdb-schema-design` skill.
> This section provides query-side context only.

### Partition Interval Adjustment

Check current setting:
```sql
SHOW CREATE TABLE sensor_data;
```

For higher write rates, consider smaller partitions (1h or 6h instead of 1d). Delegate schema changes to `kwdb-schema-design`.

### TTL for Data Lifecycle

TTL automatically removes old data to control table size. Delegate TTL changes to `kwdb-schema-design`.

### DICT ENCODING for High-Cardinality Strings

Dictionary encoding compresses high-cardinality string tags. Configure at table creation time (delegate to `kwdb-schema-design`).

## Key Points

- **Primary Tag**: Must set for exact query (WHERE device_id = 'xxx'), O(1) complexity
- **Partition Granularity**:
  - High frequency (>1M/sec): 1h or 6h
  - Medium frequency: 1d
  - Avoid too small (many small files) or too large (slow scan)

## Time Arithmetic and Intervals

KaiwuDB supports time arithmetic with intervals:

```sql
-- Time arithmetic in WHERE
SELECT * FROM sensor_data WHERE ts > now() - INTERVAL '1 hour';

-- Time arithmetic in SELECT
SELECT ts + INTERVAL '1h' AS adjusted_ts FROM sensor_data;

-- Supported interval units: ns, us, ms, s, m, h, d, w, mon, y
```

> Note: Compound interval format (e.g., '1d1h') is not supported.

## Historical Data Queries

Use AS OF SYSTEM TIME to query historical data:

```sql
-- Query data as of 1 hour ago
SELECT * FROM sensor_data AS OF SYSTEM TIME '-1 hour'
WHERE device_id = 'D001' AND ts >= '2026-04-01';

-- Query data as of specific timestamp
SELECT * FROM sensor_data AS OF SYSTEM TIME '2026-04-01 12:00:00'
WHERE device_id = 'D001';
```

> Note: Returns historical data that may be outdated.

## Cluster-Level Query Tuning

KaiwuDB supports cluster parameters for query tuning:

```sql
-- Set parallel query degree
SET CLUSTER SETTING ts.parallel_degree = 4;

-- Limit max rows returned (safety limit)
SET CLUSTER SETTING sql.auto_limit.quantity = 10000;

-- Order by write timestamp when no ORDER BY specified
SET CLUSTER SETTING ts.ordered_table.enabled = true;
```

These are session or cluster-level settings. For performance, the primary optimization is still proper query patterns (time filter, tag equality).
