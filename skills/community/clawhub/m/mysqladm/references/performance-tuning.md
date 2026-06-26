# Performance Tuning Reference

Guide for optimizing MySQL query performance, indexing strategies, and database configuration.

## Query Analysis

### EXPLAIN Basics

```sql
-- Basic query execution plan
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- Extended explain with filtered rows
EXPLAIN SELECT * FROM orders WHERE user_id = 123 AND status = 'completed';

-- Format JSON output (MySQL 8.0+)
EXPLAIN FORMAT=JSON SELECT * FROM products WHERE category_id = 5;
```

### Understanding EXPLAIN Output

Key columns to analyze:

- **type**: Access method (ALL = full table scan, index = good, range = acceptable)
- **possible_keys**: Indexes that could be used
- **key**: Index actually used
- **rows**: Estimated rows to examine (lower is better)
- **Extra**: Additional info (Using index = good, Using filesort = bad)

### Slow Query Log

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;  -- Log queries > 2 seconds
SET GLOBAL log_queries_not_using_indexes = 'ON';

-- View slow query settings
SHOW VARIABLES LIKE 'slow_query%';
SHOW VARIABLES LIKE 'long_query_time';

-- Analyze slow queries
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;
```

## Indexing Strategies

### When to Create Indexes

Create indexes on columns used in:

- WHERE clauses
- JOIN conditions
- ORDER BY clauses
- GROUP BY clauses

### Single Column Indexes

```sql
-- Basic index
CREATE INDEX idx_user_email ON users(email);

-- Unique index
CREATE UNIQUE INDEX idx_user_username ON users(username);

-- Partial index (prefix)
CREATE INDEX idx_user_name_prefix ON users(name(10));
```

### Composite Indexes

```sql
-- Multi-column index (order matters!)
CREATE INDEX idx_order_user_status ON orders(user_id, status);

-- Covering index (includes all query columns)
CREATE INDEX idx_order_user_status_date ON orders(user_id, status, created_at);
```

### Index Best Practices

1. **Column order matters**: Put most selective columns first
2. **Avoid over-indexing**: Indexes slow down INSERT/UPDATE/DELETE
3. **Use covering indexes**: Include columns in SELECT to avoid table lookup
4. **Monitor index usage**: Remove unused indexes

### Index Usage Analysis

```sql
-- Check index cardinality
SHOW INDEX FROM table_name;

-- Find low cardinality indexes (not useful)
SELECT
  table_name,
  index_name,
  cardinality,
  ROUND(cardinality / table_rows * 100, 2) AS selectivity_pct
FROM information_schema.statistics s
JOIN information_schema.tables t
  ON s.table_schema = t.table_schema
  AND s.table_name = t.table_name
WHERE s.table_schema = 'your_database'
  AND s.index_name != 'PRIMARY'
  AND t.table_rows > 0
ORDER BY selectivity_pct;
```

## Query Optimization

### SELECT Optimization

```sql
-- Bad: SELECT *
SELECT * FROM users WHERE status = 'active';

-- Good: Select only needed columns
SELECT id, name, email FROM users WHERE status = 'active';

-- Bad: SELECT DISTINCT without need
SELECT DISTINCT user_id FROM orders;

-- Good: Use GROUP BY if needed
SELECT user_id, COUNT(*) FROM orders GROUP BY user_id;
```

### WHERE Clause Optimization

```sql
-- Bad: Function on column (prevents index use)
SELECT * FROM users WHERE YEAR(created_at) = 2026;

-- Good: Range scan on indexed column
SELECT * FROM users WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01';

-- Bad: Leading wildcard (full scan)
SELECT * FROM users WHERE name LIKE '%john%';

-- Good: Trailing wildcard (uses index)
SELECT * FROM users WHERE name LIKE 'john%';
```

### JOIN Optimization

```sql
-- Ensure join columns are indexed
CREATE INDEX idx_order_user_id ON orders(user_id);
CREATE INDEX idx_user_id ON users(id);

-- Use appropriate join types
-- INNER JOIN: Only matching rows
-- LEFT JOIN: All from left, matching from right
-- RIGHT JOIN: All from right, matching from left

-- Limit result set early
SELECT u.name, COUNT(o.id) as order_count
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id
HAVING order_count > 10
LIMIT 100;
```

### Subquery Optimization

```sql
-- Bad: Correlated subquery (slow)
SELECT * FROM users u
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.user_id = u.id
  AND o.status = 'completed'
);

-- Good: JOIN (faster)
SELECT DISTINCT u.*
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';
```

## Data Type Optimization

### Choose Appropriate Types

```sql
-- Bad: Over-sized types
CREATE TABLE events (
  id INT UNSIGNED,
  user_id BIGINT,
  status VARCHAR(255),
  created_at DATETIME
);

-- Good: Right-sized types
CREATE TABLE events (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNSIGNED,
  status ENUM('pending', 'completed', 'failed'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Numeric Types

- Use TINYINT for 0-255
- Use SMALLINT for 0-65535
- Use INT for up to 2 billion
- Use BIGINT only when necessary
- Use UNSIGNED for non-negative numbers

### String Types

- Use CHAR for fixed-length strings
- Use VARCHAR for variable-length strings
- Use TEXT for long strings (>255 chars)
- Use ENUM for fixed set of values

## Table Optimization

### Table Maintenance

```sql
-- Analyze table for query optimization
ANALYZE TABLE table_name;

-- Optimize table (reclaims space, rebuilds indexes)
OPTIMIZE TABLE table_name;

-- Check table for errors
CHECK TABLE table_name;

-- Repair table (use with caution!)
REPAIR TABLE table_name;
```

### Partitioning

```sql
-- Range partitioning by date
CREATE TABLE events (
  id INT AUTO_INCREMENT,
  event_date DATE,
  data TEXT,
  PRIMARY KEY (id, event_date)
)
PARTITION BY RANGE (YEAR(event_date)) (
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p2025 VALUES LESS THAN (2026),
  PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

## Configuration Tuning

### Key Configuration Parameters

```sql
-- Buffer pool size (most important!)
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
-- Should be 70-80% of available RAM for dedicated DB server

-- Query cache (disabled by default in MySQL 8.0)
SHOW VARIABLES LIKE 'query_cache%';

-- Connection limits
SHOW VARIABLES LIKE 'max_connections';

-- Thread cache
SHOW VARIABLES LIKE 'thread_cache_size';

-- Table cache
SHOW VARIABLES LIKE 'table_open_cache';
```

### InnoDB Configuration

```sql
-- InnoDB buffer pool
SET GLOBAL innodb_buffer_pool_size = 4294967296;  -- 4GB

-- InnoDB log file size
SET GLOBAL innodb_log_file_size = 268435456;  -- 256MB

-- InnoDB flush method
SET GLOBAL innodb_flush_method = 'O_DIRECT';

-- InnoDB I/O capacity
SET GLOBAL innodb_io_capacity = 2000;
```

## Monitoring

### Performance Schema

```sql
-- Enable performance schema
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE '%statement/%';

-- View slow statements
SELECT * FROM performance_schema.events_statements_summary_by_digest
ORDER BY AVG_TIMER_WAIT DESC LIMIT 10;

-- View table I/O
SELECT * FROM performance_schema.table_io_waits_summary_by_table
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10;
```

### Process List

```sql
-- Show running queries
SHOW PROCESSLIST;

-- Show full queries
SHOW FULL PROCESSLIST;

-- Kill long-running query
KILL <process_id>;
```

## Common Performance Issues

### Full Table Scans

```sql
-- Find queries doing full table scans
SELECT * FROM sys.statements_with_full_table_scans
ORDER BY rows_examined DESC LIMIT 10;
```

### Temporary Tables

```sql
-- Find queries creating temporary tables
SELECT * FROM sys.statements_with_temp_tables
ORDER BY memory_tmp_tables_created DESC LIMIT 10;
```

### Filesort Operations

```sql
-- Find queries using filesort
SELECT * FROM sys.statements_with_sorting
ORDER BY sort_merge_passes DESC LIMIT 10;
```
