# Example Queries for kwdb-performance-review

## Example 1: Time-Series Query Without Time Filter

**Original Query:**
```sql
SELECT * FROM device_sensor WHERE device_id = 'D001';
```

**Anti-Pattern:** Missing time range filter causes full partition scan

**Optimized Query:**
```sql
SELECT ts, temperature, humidity
FROM device_sensor
WHERE device_id = 'D001'
  AND ts >= '2026-04-01' AND ts < '2026-04-02';
```

**Expected Improvement:**
- EXPLAIN shows Partition Filter on ts column
- Tag Filter on device_id using hash index
- Only reads needed columns instead of all columns

---

## Example 2: Deep Pagination with OFFSET

**Original Query:**
```sql
SELECT ts, temperature
FROM sensor_data
WHERE device_id = 'D001'
ORDER BY ts
LIMIT 20 OFFSET 10000;
```

**Anti-Pattern:** OFFSET scans and discards first 10000 rows

**Optimized Query:**
```sql
-- Page 1
SELECT ts, temperature
FROM sensor_data
WHERE device_id = 'D001' AND ts >= '2026-04-01'
ORDER BY ts
LIMIT 20;
-- Returns cursor: ts = '2026-04-01 12:30:00'

-- Page 2 (use last ts as cursor)
SELECT ts, temperature
FROM sensor_data
WHERE device_id = 'D001'
  AND ts > '2026-04-01 12:30:00'
ORDER BY ts
LIMIT 20;
```

**Expected Improvement:** O(1) per page instead of O(N)

---

## Example 3: Fuzzy Tag Match

**Original Query:**
```sql
SELECT * FROM device_sensor
WHERE device_id LIKE 'D00%'
  AND ts >= '2026-04-01';
```

**Anti-Pattern:** LIKE prevents hash index usage on primary tag

**Optimized Query:**
```sql
-- Option 1: List devices explicitly (uses hash index)
SELECT * FROM device_sensor
WHERE device_id IN ('D001', 'D002', 'D003')
  AND ts >= '2026-04-01';

-- Option 2: Add a separate prefix tag column (requires schema change)
-- Requires ALTER TABLE to add device_type as tag - delegate to kwdb-schema-design:
SELECT * FROM device_sensor
WHERE device_type = 'D00'
  AND ts >= '2026-04-01';
```

**Expected Improvement:** Exact equality uses hash index

**Note:**
- Time-series tables do NOT support secondary indexes
- Schema changes (ALTER TABLE) belong to `kwdb-schema-design` skill

---

## Example 4: Missing SELECT Columns

**Original Query:**
```sql
SELECT * FROM sensor_data
WHERE ts >= '2026-04-01' AND ts < '2026-04-02';
```

**Anti-Pattern:** SELECT * reads all columns (columnar storage penalty)

**Optimized Query:**
```sql
SELECT ts, temperature, humidity
FROM sensor_data
WHERE ts >= '2026-04-01' AND ts < '2026-04-02';
```

**Expected Improvement:** 50-70% reduction in IO

---

## Example 5: Aggregation Without TIME_BUCKET

**Original Query:**
```sql
SELECT DATE_TRUNC('hour', ts) AS hour, AVG(temperature)
FROM sensor_data
WHERE device_id = 'D001'
  AND ts >= NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', ts)
ORDER BY hour;
```

**Anti-Pattern:** Manual date truncation bypasses time-series optimizations

**Optimized Query:**
```sql
SELECT TIME_BUCKET(ts, '1 hour') AS hour, AVG(temperature)
FROM sensor_data
WHERE device_id = 'D001'
  AND ts >= NOW() - INTERVAL '7 days'
GROUP BY TIME_BUCKET(ts, '1 hour')
ORDER BY hour;
```

**Expected Improvement:** TIME_BUCKET is pushdown-optimized

---

## Example 6: Cross-Model Join Order

**Table Types:**
- `sensor_data` - TIME SERIES table (large, partitioned by time)
- `devices` - RELATIONAL table (small, device metadata)

**Original Query:**
```sql
SELECT s.ts, s.temp, d.name
FROM sensor_data s           -- TIME SERIES (large, as driver - BAD)
JOIN devices d ON s.device_id = d.id
WHERE d.group_id = 'G001';
```

**Anti-Pattern:** Time-series as driver causes full scan

**Optimized Query:**
```sql
SELECT s.ts, s.temp, d.name
FROM devices d               -- RELATIONAL (small, as driver - GOOD)
JOIN sensor_data s ON d.id = s.device_id  -- TIME SERIES
WHERE d.group_id = 'G001'
  AND s.ts >= '2026-04-01';  -- Time filter required
```

**Expected Improvement:** Small relational table drives query

---

## Example 7: Relational Table Missing Index

**Original Query:**
```sql
SELECT * FROM orders
WHERE customer_email = 'test@example.com';
```

**Analysis:** Sequential scan on large table

**Recommendation:**
```sql
CREATE INDEX idx_orders_customer_email ON orders(customer_email);
```

**Expected Improvement:** Index scan instead of sequential scan

---

## Example 8: Function on Time Column

**Original Query:**
```sql
SELECT * FROM sensor_data
WHERE DATE_TRUNC('day', ts) = '2026-04-01';
```

**Anti-Pattern:** Function prevents partition pruning

**Optimized Query:**
```sql
SELECT * FROM sensor_data
WHERE ts >= '2026-04-01' AND ts < '2026-04-02';
```

**Expected Improvement:** Partition pruning works correctly
