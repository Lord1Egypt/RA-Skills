# Pagination Optimization for Time-Series

## The Problem with OFFSET

Time-series data is naturally ordered by time. OFFSET-based pagination ignores this and causes problems:

```sql
-- SLOW: OFFSET forces scan of first 10000 rows
SELECT ts, temperature
FROM sensor_data
WHERE device_id = 'D001' AND ts >= '2026-04-01'
ORDER BY ts
LIMIT 20 OFFSET 10000;
```

**Why it's slow:**
1. Database scans and discards first 10000 rows
2. Time-series tables have no index to skip rows
3. Each page request gets slower

## Time-Based Cursor Pagination (Recommended)

Use the last seen timestamp as the cursor:

```sql
-- First page
SELECT ts, temperature
FROM sensor_data
WHERE device_id = 'D001' AND ts >= '2026-04-01'
ORDER BY ts
LIMIT 20;

-- Subsequent pages (use last ts from previous page)
SELECT ts, temperature
FROM sensor_data
WHERE device_id = 'D001'
  AND ts > '2026-04-01 12:30:00'  -- cursor from last row
ORDER BY ts
LIMIT 20;
```

## Cursor Pagination Implementation

### Application Logic

```python
# Pseudocode for paginating through time-series data
def fetch_page(cursor_ts=None, page_size=20):
    query = """
        SELECT ts, temperature, humidity
        FROM sensor_data
        WHERE device_id = 'D001' AND ts >= '2026-04-01'
    """
    if cursor_ts:
        query += f" AND ts > '{cursor_ts}'"
    query += " ORDER BY ts LIMIT %s" % page_size

    rows = execute(query)
    next_cursor = rows[-1].ts if rows else None
    return rows, next_cursor
```

### Page-by-Page Navigation

```
Page 1:  ts='2026-04-01 00:00:00' to '2026-04-01 00:19:59'
         -> cursor = '2026-04-01 00:19:59'

Page 2:  ts > '2026-04-01 00:19:59' -> '2026-04-01 00:39:59'
         -> cursor = '2026-04-01 00:39:59'

Page 3:  ts > '2026-04-01 00:39:59' -> ...
```

## Handling Irregular Timestamps

When timestamps aren't perfectly regular, cursor must be the actual last value:

```sql
-- Page 1
SELECT ts, value FROM metrics
WHERE device_id = 'D001' AND ts >= '2026-04-01'
ORDER BY ts LIMIT 5;
-- Returns: [12:00:01, 12:00:03, 12:00:07, 12:00:12, 12:00:15]

-- Page 2 (cursor = 12:00:15)
SELECT ts, value FROM metrics
WHERE device_id = 'D001' AND ts > '2026-04-01 12:00:15'
ORDER BY ts LIMIT 5;
```

## Bidirectional Pagination

### Forward Cursor

```sql
-- Forward: ts > last_seen
SELECT ts, temperature
FROM sensor_data
WHERE device_id = 'D001' AND ts > :cursor
ORDER BY ts
LIMIT :page_size;
```

### Backward Cursor

```sql
-- Backward: ts < first_seen
SELECT ts, temperature
FROM sensor_data
WHERE device_id = 'D001' AND ts < :cursor
ORDER BY ts DESC
LIMIT :page_size;
-- Results returned in reverse order, client flips if needed
```

## Filtering with Cursor

Always maintain filter conditions across pages:

```sql
-- Initial query with filters
SELECT ts, temperature, humidity
FROM sensor_data
WHERE device_id = 'D001'
  AND location = 'Beijing'        -- filter 1
  AND ts >= '2026-04-01'          -- filter 2
ORDER BY ts
LIMIT 20;
-- Returns last row with ts='2026-04-01 12:30:00'

-- Next page MUST repeat all filters
SELECT ts, temperature, humidity
FROM sensor_data
WHERE device_id = 'D001'
  AND location = 'Beijing'
  AND ts >= '2026-04-01'
  AND ts > '2026-04-01 12:30:00'  -- cursor added
ORDER BY ts
LIMIT 20;
```

## Stable Sort Requirement

Cursor pagination requires stable sort order. Use multiple columns if needed:

```sql
-- Single column sort (simple)
ORDER BY ts

-- Multiple columns (when ts can have duplicates)
ORDER BY ts, primary_key
-- Cursor: WHERE ts > :ts OR (ts = :ts AND id > :last_id)
```

## Comparison Table

| Method | Page N Speed | Memory | Use Case |
|--------|--------------|--------|----------|
| OFFSET | O(N) per page | Low | Random access (rare) |
| Cursor | O(1) per page | Low | Sequential scan |
| Seek | O(1) per page | Medium | Jump to specific |

## When OFFSET Is Acceptable

OFFSET is only acceptable when:
1. N is small (< 100)
2. Pages are accessed rarely (not in loops)
3. Total dataset is bounded

```sql
-- Acceptable use of OFFSET
SELECT * FROM small_lookup_table LIMIT 20 OFFSET 0;
```
