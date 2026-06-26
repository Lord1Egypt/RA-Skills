# Schema Analysis Reference

Guide for analyzing MySQL database schemas, table structures, and relationships.

## Table Information Queries

### Basic Table Info

```sql
-- Show all tables in database
SHOW TABLES;

-- Show table structure
DESCRIBE table_name;
-- or
SHOW COLUMNS FROM table_name;

-- Show table creation statement
SHOW CREATE TABLE table_name;

-- Show table engine and row format
SHOW TABLE STATUS WHERE Name = 'table_name';
```

### Table Size Analysis

```sql
-- Table sizes in MB
SELECT
  table_schema,
  table_name,
  ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb,
  ROUND(data_length / 1024 / 1024, 2) AS data_mb,
  ROUND(index_length / 1024 / 1024, 2) AS index_mb,
  table_rows
FROM information_schema.tables
WHERE table_schema = 'your_database'
ORDER BY size_mb DESC;
```

### Row Count by Table

```sql
-- Row counts for all tables
SELECT
  table_name,
  table_rows
FROM information_schema.tables
WHERE table_schema = 'your_database'
ORDER BY table_rows DESC;
```

## Index Analysis

### Show Indexes

```sql
-- All indexes on a table
SHOW INDEX FROM table_name;

-- Index information from information_schema
SELECT
  table_name,
  index_name,
  column_name,
  seq_in_index,
  cardinality,
  index_type
FROM information_schema.statistics
WHERE table_schema = 'your_database'
  AND table_name = 'your_table'
ORDER BY index_name, seq_in_index;
```

### Duplicate Indexes

```sql
-- Find potentially duplicate indexes
SELECT
  a.table_schema,
  a.table_name,
  a.index_name,
  GROUP_CONCAT(a.column_name ORDER BY a.seq_in_index) AS columns
FROM information_schema.statistics a
WHERE a.table_schema = 'your_database'
GROUP BY a.table_schema, a.table_name, a.index_name
HAVING COUNT(*) > 1;
```

### Unused Indexes

```sql
-- Check for unused indexes (requires performance_schema)
SELECT
  object_schema,
  object_name,
  index_name
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NOT NULL
  AND count_star = 0
  AND object_schema = 'your_database'
ORDER BY object_schema, object_name;
```

## Column Analysis

### Column Types and Sizes

```sql
-- Column information
SELECT
  column_name,
  data_type,
  character_maximum_length,
  is_nullable,
  column_default,
  column_key
FROM information_schema.columns
WHERE table_schema = 'your_database'
  AND table_name = 'your_table'
ORDER BY ordinal_position;
```

### Text Column Analysis

```sql
-- Find long text columns
SELECT
  table_name,
  column_name,
  data_type,
  character_maximum_length
FROM information_schema.columns
WHERE table_schema = 'your_database'
  AND data_type IN ('text', 'varchar', 'char')
  AND character_maximum_length > 1000
ORDER BY character_maximum_length DESC;
```

## Foreign Key Analysis

### Show Foreign Keys

```sql
-- Foreign key relationships
SELECT
  table_name,
  constraint_name,
  referenced_table_name,
  referenced_column_name
FROM information_schema.key_column_usage
WHERE table_schema = 'your_database'
  AND referenced_table_name IS NOT NULL
ORDER BY table_name, constraint_name;
```

### Foreign Key Tree

```sql
-- Build foreign key dependency tree
WITH RECURSIVE fk_tree AS (
  SELECT
    table_name AS parent_table,
    referenced_table_name AS child_table,
    1 AS level
  FROM information_schema.key_column_usage
  WHERE table_schema = 'your_database'
    AND referenced_table_name IS NOT NULL

  UNION ALL

  SELECT
    t.parent_table,
    k.referenced_table_name,
    t.level + 1
  FROM fk_tree t
  JOIN information_schema.key_column_usage k
    ON t.child_table = k.table_name
  WHERE k.table_schema = 'your_database'
    AND k.referenced_table_name IS NOT NULL
)
SELECT * FROM fk_tree ORDER BY level, parent_table;
```

## Data Quality Checks

### Null Value Analysis

```sql
-- Null value percentages by column
SELECT
  table_name,
  column_name,
  data_type,
  COUNT(*) AS total_rows,
  SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) AS null_count,
  ROUND(100.0 * SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS null_percentage
FROM your_table
GROUP BY table_name, column_name, data_type;
```

### Duplicate Detection

```sql
-- Find duplicate rows based on specific columns
SELECT
  column1,
  column2,
  COUNT(*) as duplicate_count
FROM your_table
GROUP BY column1, column2
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
```

### Data Distribution

```sql
-- Column value distribution
SELECT
  column_name,
  COUNT(*) as count,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM your_table), 2) as percentage
FROM your_table
GROUP BY column_name
ORDER BY count DESC
LIMIT 20;
```

## Schema Comparison

### Compare Two Tables

```sql
-- Column differences between tables
SELECT
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_schema = 'your_database'
  AND table_name = 'table1'

EXCEPT

SELECT
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_schema = 'your_database'
  AND table_name = 'table2';
```

## Partitioning Info

```sql
-- Check partitioned tables
SELECT
  table_name,
  partition_method,
  partition_expression,
  partition_description
FROM information_schema.partitions
WHERE table_schema = 'your_database'
  AND partition_name IS NOT NULL
GROUP BY table_name, partition_method, partition_expression, partition_description;
```

## Storage Engine Analysis

```sql
-- Storage engines by table
SELECT
  engine,
  COUNT(*) as table_count,
  ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as total_mb
FROM information_schema.tables
WHERE table_schema = 'your_database'
GROUP BY engine
ORDER BY total_mb DESC;
```
