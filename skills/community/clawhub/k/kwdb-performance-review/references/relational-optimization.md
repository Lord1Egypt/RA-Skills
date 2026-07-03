# Relational Query Optimization

Unlike time-series tables, relational tables in KWDB support standard SQL indexes.

## Index Types

### B-tree Index (Default)

Best for: equality, range, prefix matching

```sql
-- Single column
CREATE INDEX idx_users_email ON users(email);

-- Composite (leftmost prefix)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- Can use for: WHERE user_id = ? AND status = ?
-- Can use for: WHERE user_id = ?
-- Cannot use: WHERE status = ?
```

### Inverted Index

Best for: array containment, JSONB

> Note: INVERTED INDEX syntax varies by database. Verify KWDB supports `CREATE INVERTED INDEX` before using.

```sql
-- Syntax may vary - verify with KWDB documentation
-- Example for array containment:
CREATE INVERTED INDEX idx_tags ON products USING INVERTED(tags);
-- For: WHERE tags @> ARRAY['electronics', 'sale']
```

## When to Create an Index

### Good Candidates

```sql
-- High selectivity (few rows match)
CREATE INDEX ON orders(order_id);  -- PK, unique

-- Foreign key columns (JOIN performance)
CREATE INDEX ON orders(user_id);  -- FK from users

-- Frequently filtered columns
CREATE INDEX ON products(category_id);
```

### Poor Candidates

```sql
-- Low selectivity (most rows match)
CREATE INDEX ON orders(status);  -- 95% are 'pending'?

-- Never filtered on
CREATE INDEX ON users(phone);  -- rarely used in WHERE
```

## EXPLAIN Analysis for Relational

### Sequential Scan (Check Table Size)

```sql
EXPLAIN SELECT * FROM large_table WHERE status = 'x';

-- Sequential scan OK if:
-- - Table is small (< 1000 rows)
-- - Selectivity is high (> 10% of rows)
-- - No index available

-- Sequential scan BAD if:
-- - Table is large
-- - Selectivity is low (< 1%)
```

### Index Scan vs Index Only Scan

```sql
-- Index Scan (reads index + table)
EXPLAIN SELECT * FROM users WHERE email = 'x';
-- -> Index Scan using idx_email on users

-- Index Only Scan (reads index only, faster)
EXPLAIN SELECT email FROM users WHERE email = 'x';
-- -> Index Only Scan using idx_email on users
```

## JOIN Optimization

### Hash Join (Good for Large Sets)

```sql
EXPLAIN
SELECT o.id, u.name
FROM orders o
JOIN users u ON o.user_id = u.id;
-- Optimizer chooses hash join for large tables
```

### Merge Join (Good for Sorted Data)

```sql
-- Merge join when both sides are sorted by join key
-- Benefits: O(n+m) instead of O(n*m)
```

### Nested Loop (Bad for Large Sets)

```sql
-- Nested loop can be OK with small inner table
EXPLAIN
SELECT * FROM large_table l, small_table s
WHERE l.id = s.ref_id;
-- If small_table has index on ref_id, nested loop is efficient
```

## Common Anti-Patterns

### 1. Missing Index on Foreign Key

```sql
-- SLOW: FK without index
SELECT o.*, u.name
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.region = 'Beijing';

-- FAST: Index on FK
CREATE INDEX ON orders(user_id);
```

### 2. Function on Indexed Column

```sql
-- SLOW: Cannot use index
WHERE LOWER(email) = 'test@example.com'

-- FAST: Index usable
WHERE email = LOWER('Test@Example.com')

-- Alternative: Functional index (if supported)
CREATE INDEX ON users (LOWER(email));
```

### 3. Implicit Type Conversion

```sql
-- SLOW: Type conversion prevents index
WHERE user_id = '123'  -- user_id is INT

-- FAST: Same type
WHERE user_id = 123
```

### 4. OR Conditions

```sql
-- SLOW: OR can prevent index usage
WHERE status = 'active' OR status = 'pending'

-- FAST: UNION or IN
WHERE status IN ('active', 'pending')
```

### 5. LIKE Patterns

```sql
-- FAST: Prefix match can use index
WHERE name LIKE 'John%'

-- SLOW: Wildcard at start cannot use index
WHERE name LIKE '%ohn%'
```

## Query Rewriting Tips

### Subquery to JOIN

```sql
-- Slower: Correlated subquery
SELECT * FROM orders o
WHERE amount > (SELECT AVG(amount) FROM orders);

-- Faster: JOIN with derived table
SELECT o.*, avg_amount
FROM orders o
JOIN (SELECT AVG(amount) AS avg_amount FROM orders) a
WHERE o.amount > a.avg_amount;
```

### DISTINCT to GROUP BY

```sql
-- Equivalent, but GROUP BY can use index
SELECT DISTINCT user_id FROM orders;
SELECT user_id FROM orders GROUP BY user_id;
```

## Statistics and Cost Estimation

KWDB maintains statistics for query planning:

```sql
-- Update statistics (helps optimizer)
ANALYZE table_name;

-- View statistics
SHOW STATISTICS FOR table_name;
```

Poor statistics -> bad query plan -> slow execution.
