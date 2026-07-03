# Cross-Model Query Optimization

KaiwuDB supports querying both time-series and relational tables in a single SQL statement. This requires careful optimization.

## Query Planning

When a query involves both table types, KWDB:
1. Determines which engine handles each table
2. Plans data movement between engines
3. Optimizes join order

## Key Principle: Drive from Small Table

### Wrong: Time-Series as Driver

```sql
-- SLOW: Scans large time-series table first
SELECT s.ts, s.temp, d.name
FROM sensor_data s              -- Large time-series (millions of rows)
JOIN devices d ON s.device_id = d.id  -- Small relational (hundreds)
WHERE d.group_id = 'G001';      -- Filter on small table

-- EXPLAIN shows:
-- Nested Loop / Hash Join
--   -> Partition Filter: None  -- Full time-series scan!
--   -> Sequential Scan: devices
--       Filter: group_id = 'G001'
```

### Correct: Relational as Driver

```sql
-- FAST: Filters small table first, pushes to time-series
SELECT s.ts, s.temp, d.name
FROM devices d                  -- Small relational (hundreds)
JOIN sensor_data s ON d.id = s.device_id
WHERE d.group_id = 'G001'       -- Filter on small table
  AND s.ts >= '2026-04-01';    -- Time filter on time-series
```

## Time Filter Placement

Always add time filter for time-series table in JOIN:

```sql
-- GOOD: Time filter present
SELECT s.ts, s.temp, d.name
FROM devices d
JOIN sensor_data s ON d.id = s.device_id
WHERE d.group_id = 'G001'
  AND s.ts >= '2026-04-01' AND s.ts < '2026-04-02';

-- BAD: No time filter, full time-series scan
SELECT s.ts, s.temp, d.name
FROM devices d
JOIN sensor_data s ON d.id = s.device_id
WHERE d.group_id = 'G001';
```

## Multiple Time-Series Tables

Joining multiple time-series tables is complex:

```sql
-- COMPLEX: Multiple time-series without time sync
SELECT s1.ts, s1.temp, s2.humidity
FROM sensor_temp s1
JOIN sensor_humidity s2 ON s1.device_id = s2.device_id
WHERE s1.device_id = 'D001';

-- BETTER: Add time synchronization
SELECT s1.ts, s1.temp, s2.humidity
FROM sensor_temp s1
JOIN sensor_humidity s2
  ON s1.device_id = s2.device_id
  AND s1.ts = s2.ts  -- Time alignment
WHERE s1.device_id = 'D001'
  AND s1.ts >= '2026-04-01';

-- BEST: Use UNION/JOIN with TIME_BUCKET alignment
SELECT
  TIME_BUCKET(s1.ts, '1h') AS ts,
  s1.device_id,
  s1.temp,
  s2.humidity
FROM sensor_temp s1
JOIN sensor_humidity s2
  ON s1.device_id = s2.device_id
  AND TIME_BUCKET(s1.ts, '1h') = TIME_BUCKET(s2.ts, '1h')
WHERE s1.ts >= '2026-04-01'
GROUP BY 1, 2, s1.temp, s2.humidity;
```

## Aggregation with Cross-Model

### Time-Series First

```sql
-- Aggregate time-series first, then join
SELECT d.name, avg_temp
FROM devices d
JOIN (
  SELECT device_id, AVG(temp) AS avg_temp
  FROM sensor_data
  WHERE ts >= '2026-04-01'
  GROUP BY device_id
) s ON d.id = s.device_id
WHERE d.group_id = 'G001';
```

### Denormalization Option

Consider storing device name in time-series table to avoid JOIN:

```sql
-- Denormalized: no JOIN needed
SELECT ts, temp, device_name
FROM sensor_data_denorm
WHERE ts >= '2026-04-01';

-- vs Normalized: requires JOIN
SELECT s.ts, s.temp, d.name
FROM sensor_data s
JOIN devices d ON s.device_id = d.id
WHERE s.ts >= '2026-04-01';
```

## Distribution Awareness

In distributed KWDB, cross-node data movement is expensive:

```sql
-- Check EXPLAIN for Distribution type
EXPLAIN SELECT ...
-- Local: data on same node (good)
-- Shuffle: data needs redistribution (expensive)
```

### Co-located JOIN

```sql
-- If devices is distributed by id, and sensor_data has device_id,
-- co-located JOIN avoids shuffle
```

## Summary Table

| Pattern | Recommendation |
|---------|----------------|
| Time-series as driver | Avoid - full scan |
| Relational as driver | Best - pushes filter down |
| Missing time filter | Always add |
| Multiple TS tables | Complex - consider pre-aggregation |
| Cross-node shuffle | Expensive - check distribution |
| FULL JOIN with subquery | Avoid - use INNER/LEFT instead |

## Transaction and Consistency

Cross-model queries have specific consistency characteristics:

> **Warning**: KaiwuDB does not guarantee cross-model query consistency between time-series and relational engines.

```sql
-- CROSS-MODEL CONSIDERATIONS:
-- 1. Time-series writes may not be immediately visible in relational queries
-- 2. FULL JOIN results may be inconsistent across engines
-- 3. For critical consistency needs, query each engine separately
```

### FULL JOIN Limitation

Avoid using FULL JOIN with subqueries in cross-model queries:

```sql
-- BAD: FULL JOIN with subquery
SELECT * FROM ts_table t FULL JOIN (
  SELECT * FROM rel_table WHERE status = 'active'
) r ON t.id = r.id;

-- BETTER: Use INNER JOIN or LEFT JOIN without subqueries
SELECT * FROM ts_table t
INNER JOIN rel_table r ON t.id = r.id
WHERE r.status = 'active';
```

## UNION and Set Operations

Cross-model queries support UNION, INTERSECT, EXCEPT:

```sql
-- UNION ALL (faster - no deduplication)
SELECT device_id, ts FROM ts_table
UNION ALL
SELECT id AS device_id, created_at AS ts FROM rel_table;

-- UNION (with deduplication)
SELECT device_id, ts FROM ts_table
UNION
SELECT id AS device_id, created_at AS ts FROM rel_table;
```
