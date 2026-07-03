# EXPLAIN Output Analysis

## Reading KWDB EXPLAIN

### Basic EXPLAIN Structure

```
KaiwuDB Time-Series EXPLAIN:
├── Output: [columns]
├── Limit
│   └── Filter: [conditions]
│       └── Partition Filter: ts [range]    <- time pruning indicator
│           └── Tag Filter: device_id = 'D001'  <- hash index indicator
│               └── Table Scan: sensor_data
│                   └── Distribution: Local    <- or Shuffle (cross-node)
```

### Key Indicators

| Indicator | Good | Bad | Meaning |
|-----------|------|-----|---------|
| Partition Filter | Present | Missing | Time pruning working |
| Tag Filter | Present | N/A | Hash index hit |
| Table Scan | Local | Shuffle | Cross-node traffic |
| Rows | Low | High | Filter selectivity |

## Time-Series EXPLAIN Examples

### Optimized Query

```sql
EXPLAIN
SELECT ts, temperature
FROM device_sensor
WHERE device_id = 'D001'
  AND ts >= '2026-04-01' AND ts < '2026-04-02';

-- Expected Output:
Limit
  Output: ts, temperature
  Filter: (device_id = 'D001') AND (ts >= '2026-04-01') AND (ts < '2026-04-02')
  Partition Filter: ts [2026-04-01, 2026-04-02)     <- Time pruning!
  Tag Filter: device_id = 'D001'                     <- Hash index!
  Table Scan: device_sensor
    Distribution: Local
    Index: primary_tag_hash                          <- Hash index used
```

### Missing Time Filter (Bad)

```sql
EXPLAIN
SELECT * FROM device_sensor
WHERE device_id = 'D001';

-- Expected Output:
Limit
  Output: *
  Filter: (device_id = 'D001')
  Partition Filter: None                             <- No time filter!
  Tag Filter: device_id = 'D001'
  Table Scan: device_sensor
    Distribution: Shuffle                           <- Cross-node scan!
    Estimated Rows: 10000000                        <- Full scan
```

### Fuzzy Tag Match (Bad)

```sql
EXPLAIN
SELECT * FROM device_sensor
WHERE device_id LIKE '%001%'
  AND ts >= '2026-04-01';

-- Expected Output:
Limit
  Output: *
  Filter: (device_id ~~ '%001%')                    <- Function/LIKE!
  Partition Filter: ts [2026-04-01, ...)
  Tag Filter: device_id ~~ '%001%'                 <- Cannot use hash!
  Table Scan: device_sensor
    Distribution: Local
    Estimated Rows: 500000                          <- No index usage
```

## Relational EXPLAIN Examples

### Index Scan (Good)

```sql
EXPLAIN
SELECT * FROM users
WHERE email = 'test@example.com';

-- Expected Output:
Limit
  Output: id, email, name, created_at
  Filter: email = 'test@example.com'
  Index Scan: users_email_idx                       <- Using index
  Index Columns: email
  Estimated Rows: 1
```

### Sequential Scan (May Need Index)

```sql
EXPLAIN
SELECT * FROM orders
WHERE status = 'pending'
  AND created_at >= '2026-04-01';

-- Expected Output:
Limit
  Output: id, user_id, status, total, created_at
  Filter: (status = 'pending') AND (created_at >= '2026-04-01')
  Sequential Scan: orders                           <- Sequential scan
  Estimated Rows: 50000
```

### Hash Join (Good for Large Sets)

```sql
EXPLAIN
SELECT o.*, u.name
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'completed';

-- Expected Output:
Hash Join
  Output: o.*, u.name
  Hash Cond: o.user_id = u.id
  -> Sequential Scan: orders
      Filter: status = 'completed'
  -> Sequential Scan: users
      Filter: true
  Distribution: Local
```

### Nested Loop (Bad for Large Sets)

```sql
EXPLAIN
SELECT * FROM large_table t1, other_table t2
WHERE t1.id = t2.ref_id;

-- Expected Output:
Nested Loop
  Output: t1.*, t2.*
  -> Sequential Scan: other_table
  -> Index Scan: large_table_pkey  <- Index on id
      Index Cond: id = ref_id
```

## Cross-Model EXPLAIN

### Optimized Join Order

```sql
EXPLAIN
SELECT s.ts, s.temp, d.name
FROM devices d                    -- Small relational table first
JOIN sensor_data s ON d.id = s.device_id
WHERE d.group_id = 'G001'
  AND s.ts >= '2026-04-01';

-- Expected Output:
Hash Join
  Output: s.ts, s.temp, d.name
  Hash Cond: s.device_id = d.id
  -> Partition Filter: ts [2026-04-01, ...)
      Tag Filter: None
      Table Scan: sensor_data
  -> Sequential Scan: devices       -- Small table first
      Filter: group_id = 'G001'    -- High selectivity
  Distribution: Shuffle
```

### Bad Join Order (Time-Series as Driver)

```sql
EXPLAIN
SELECT s.ts, s.temp, d.name
FROM sensor_data s                 -- Large time-series first (BAD!)
JOIN devices d ON s.device_id = d.id
WHERE d.group_id = 'G001';

-- Expected Output:
Nested Loop
  Output: s.ts, s.temp, d.name
  -> Hash Join
      Output: s.device_id
      Hash Cond: s.device_id = d.id
      -> Partition Filter: None    -- No time filter!
          Tag Filter: None
          Table Scan: sensor_data  -- Full time-series scan!
          Distribution: Shuffle    -- Cross-node!
      -> Sequential Scan: devices
          Filter: group_id = 'G001'
```
