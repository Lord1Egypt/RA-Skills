# Index Analysis for Relational Tables

## This is for RELATIONAL tables only

Time-series tables do NOT support secondary indexes. See `timeseries-optimization.md` for time-series optimization.

## Viewing Indexes

```sql
-- List all indexes on a table
SHOW INDEX FROM orders;

-- View index definition
SHOW CREATE TABLE orders;
```

## Index Usage Analysis

### EXPLAIN Output Markers

| Marker | Meaning |
|--------|---------|
| Index Scan | Using index to find rows |
| Index Only Scan | Using index, no table access needed |
| Seq Scan | Reading entire table |
| Bitmap Heap Scan | Multiple index lookups combined |

### When Index Is Used

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
-- → Index Scan using idx_orders_user on orders
-- → Index Cond: user_id = 123
```

### When Index Is NOT Used

```sql
EXPLAIN SELECT * FROM orders WHERE status = 'pending';
-- → Sequential Scan on orders
-- → Filter: status = 'pending'
-- Index not used because: low selectivity or no index exists
```

## Identifying Unused Indexes

### Check EXPLAIN for Index Usage

```sql
-- For each index, check if EXPLAIN uses it
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
-- If no "Index Scan" in output, index might be unused

-- Check specific index
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
-- Look for: Index Scan using idx_orders_user
```

### Common Unused Index Patterns

```sql
-- Function on indexed column
WHERE LOWER(email) = 'x'  -- index on email not used

-- Implicit type conversion
WHERE user_id = '123'  -- user_id is INT

-- OR conditions
WHERE status = 'a' OR status = 'b'  -- may not use index
```

## Index Recommendations

### High-Selectivity Columns

```sql
-- Unique or near-unique columns
CREATE UNIQUE INDEX idx_users_id ON users(id);

-- High-cardinality foreign keys
CREATE INDEX idx_orders_user ON orders(user_id);
```

### Composite Index Design

```sql
-- Query: WHERE a = 1 AND b = 2
-- Best index: (a, b) in that order

-- Query: WHERE b = 2
-- Best index: (b) alone or (b, a)
```

### Covering Indexes

> **Note**: INCLUDE clause for covering indexes may not be supported by KWDB. Verify before using.

```sql
-- Query: SELECT email, name FROM users WHERE email = 'x'
-- Standard composite index (widely supported):
CREATE INDEX idx_users_email_covering ON users(email, name);
-- INCLUDE syntax (PostgreSQL style, verify KWDB support):
-- CREATE INDEX idx_users_email_covering ON users(email) INCLUDE (name);
```

## Index Maintenance

### Index Bloat

Sequential inserts cause index bloat. Consider:
- Periodic REINDEX (if supported)
- Batch inserts instead of row-by-row

### Partial Indexes

```sql
-- Index only pending orders (if supported)
CREATE INDEX idx_orders_pending ON orders(created_at)
  WHERE status = 'pending';
```

## Removing Unused Indexes

```sql
-- Drop unused index (careful!)
DROP INDEX idx_orders_old_status;

-- First verify with EXPLAIN that it's not used
EXPLAIN SELECT * FROM orders WHERE status = 'old';
```

## Index vs Full Table Scan

### Index Faster When:

- High selectivity (< 5-10% of rows)
- Large table
- Query returns few columns

### Seq Scan Faster When:

- Low selectivity (> 20% of rows)
- Small table
- Query returns most columns
- Index not available

## Quick Reference

| Query Pattern | Recommended Index |
|--------------|------------------|
| `WHERE col = x` | Single column B-tree |
| `WHERE col IN (a,b,c)` | Single column B-tree |
| `WHERE col > x AND col < y` | B-tree range |
| `WHERE col LIKE 'x%'` | B-tree prefix |
| `WHERE col @> ARRAY[...]` | Inverted index |
| `WHERE a = 1 AND b = 2` | Composite (a, b) |
