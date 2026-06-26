# Relational Query Reference

Standard SQL patterns for KWDB relational tables.

## Basic SELECT

```sql
SELECT column1, column2 FROM table_name WHERE condition;
SELECT * FROM table_name;  -- all columns
```

## Filtering

```sql
WHERE column = value
WHERE column > value
WHERE column LIKE '%pattern%'
WHERE column IN (val1, val2, val3)
WHERE column IS NULL
WHERE column IS NOT NULL
```

## Aggregation

```sql
SELECT count(*) FROM table_name;
SELECT sum(column) FROM table_name;
SELECT avg(column) FROM table_name;
SELECT min(column), max(column) FROM table_name;
```

## GROUP BY

```sql
SELECT department, count(*) as cnt
FROM employees
GROUP BY department
HAVING count(*) > 5;
```

## ORDER BY

```sql
ORDER BY column ASC        -- ascending (default)
ORDER BY column DESC       -- descending
ORDER BY col1 ASC, col2 DESC
```

## Common Aggregate Functions

- `count(*)` - count all rows
- `count(column)` - count non-null values
- `sum(column)` - sum of values
- `avg(column)` - average of values
- `min(column)` - minimum value
- `max(column)` - maximum value

## Natural Language Mapping

| NL Pattern | SQL Pattern |
|------------|-------------|
| 查询所有数据 | `SELECT * FROM table` |
| 按条件过滤 | `WHERE column = value` |
| 按列分组统计 | `GROUP BY column` |
| 分组后筛选 | `HAVING count(*) > N` |
| 结果排序 | `ORDER BY column DESC` |
| 统计总数 | `count(*)` |
| 计算平均值 | `avg(column)` |

## KWDB Relational Specifics

KWDB's relational engine follows CockroachDB's SQL dialect. Key points:


### Supported Relational Features

- Standard SELECT/GROUP BY/HAVING/ORDER BY
- JOINs (INNER, LEFT, RIGHT — see cross-model.md for full join details)
- Subqueries (in FROM, WHERE, SELECT)
- Common table expressions (WITH clause)
- Window functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, NTILE)
- IMPORT for bulk data loading (DDL-level, not query-level)
- Change Data Feed (CDC) for tracking changes