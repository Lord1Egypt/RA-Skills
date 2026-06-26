---
name: mssql-toolkit
description: Query and explore Microsoft SQL Server databases using sqlcmd. Schema inspection, ad-hoc T-SQL queries, data analysis. Works with any MSSQL/SQL Server instance.
metadata: {"openclaw":{"emoji":"🗄️","requires":{"env":["MSSQL_HOST","MSSQL_USER","MSSQL_PASSWORD","MSSQL_DB"]},"os":["linux","darwin","win32"]}}
---

# MSSQL Toolkit

Query and explore Microsoft SQL Server databases using `sqlcmd`.

## Setup

### Environment Variables

Set these in your OpenClaw `.env` file:

```
MSSQL_HOST=your-server,port    # e.g., 10.0.0.1,1433
MSSQL_USER=your_username
MSSQL_PASSWORD=your_password
MSSQL_DB=your_database
```

### sqlcmd Path

If `sqlcmd` is in your PATH, use it directly. If installed at a non-standard location, set:

```
MSSQL_SQLCMD=/opt/mssql-tools18/bin/sqlcmd
```

If `MSSQL_SQLCMD` is not set, default to `sqlcmd`.

## Connection Command

```bash
${MSSQL_SQLCMD:-sqlcmd} -S $MSSQL_HOST -U $MSSQL_USER -P $MSSQL_PASSWORD -d $MSSQL_DB -C -W -Q "YOUR_QUERY"
```

## Required Flags

- `-C` trust server certificate (always required for modern MSSQL)
- `-Q` run query and exit
- `-W` remove trailing whitespace

## Useful Flags

- `-s ","` comma column separator (CSV-like output)
- `-w 999` wide output (prevent line wrapping)
- `-h -1` hide column headers (for scripting)

## Schema Inspection

### List all schemas

```bash
${MSSQL_SQLCMD:-sqlcmd} -S $MSSQL_HOST -U $MSSQL_USER -P $MSSQL_PASSWORD -d $MSSQL_DB -C -W -Q "SELECT DISTINCT TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_SCHEMA"
```

### List all tables (with schema)

```bash
${MSSQL_SQLCMD:-sqlcmd} -S $MSSQL_HOST -U $MSSQL_USER -P $MSSQL_PASSWORD -d $MSSQL_DB -C -W -Q "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_SCHEMA, TABLE_NAME"
```

### Search tables by keyword

```bash
${MSSQL_SQLCMD:-sqlcmd} -S $MSSQL_HOST -U $MSSQL_USER -P $MSSQL_PASSWORD -d $MSSQL_DB -C -W -Q "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME LIKE '%KEYWORD%' ORDER BY TABLE_SCHEMA, TABLE_NAME"
```

### Describe table columns

```bash
${MSSQL_SQLCMD:-sqlcmd} -S $MSSQL_HOST -U $MSSQL_USER -P $MSSQL_PASSWORD -d $MSSQL_DB -C -W -Q "SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='SCHEMA' AND TABLE_NAME='TABLE' ORDER BY ORDINAL_POSITION"
```

### Row count

```bash
${MSSQL_SQLCMD:-sqlcmd} -S $MSSQL_HOST -U $MSSQL_USER -P $MSSQL_PASSWORD -d $MSSQL_DB -C -W -Q "SELECT COUNT(*) AS row_count FROM schema_name.table_name"
```

### Sample rows

```bash
${MSSQL_SQLCMD:-sqlcmd} -S $MSSQL_HOST -U $MSSQL_USER -P $MSSQL_PASSWORD -d $MSSQL_DB -C -W -Q "SELECT TOP 5 * FROM schema_name.table_name"
```

### List indexes

```bash
${MSSQL_SQLCMD:-sqlcmd} -S $MSSQL_HOST -U $MSSQL_USER -P $MSSQL_PASSWORD -d $MSSQL_DB -C -W -Q "SELECT i.name AS index_name, i.type_desc, STRING_AGG(c.name, ', ') AS columns FROM sys.indexes i JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id WHERE i.object_id = OBJECT_ID('schema_name.table_name') GROUP BY i.name, i.type_desc"
```

## Query Patterns

### Aggregation

```sql
SELECT department, COUNT(*) AS cnt, SUM(amount) AS total
FROM schema_name.table_name
GROUP BY department
HAVING SUM(amount) > 1000
ORDER BY total DESC;
```

### CTE (Common Table Expression)

```sql
WITH monthly AS (
    SELECT
        YEAR(created_at) AS yr,
        MONTH(created_at) AS mo,
        SUM(amount) AS total
    FROM schema_name.table_name
    GROUP BY YEAR(created_at), MONTH(created_at)
)
SELECT * FROM monthly ORDER BY yr, mo;
```

### Window Functions

```sql
SELECT *,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
    SUM(salary) OVER (PARTITION BY department) AS dept_total
FROM schema_name.table_name;
```

### Date Filtering

```sql
-- Today
WHERE CAST(date_column AS DATE) = CAST(GETDATE() AS DATE)

-- This month
WHERE YEAR(date_column) = YEAR(GETDATE()) AND MONTH(date_column) = MONTH(GETDATE())

-- Last 7 days
WHERE date_column >= DATEADD(DAY, -7, GETDATE())

-- Date range
WHERE date_column BETWEEN '2026-01-01' AND '2026-01-31'
```

### PIVOT

```sql
SELECT *
FROM (
    SELECT category, region, revenue
    FROM schema_name.table_name
) AS src
PIVOT (
    SUM(revenue) FOR region IN ([North], [South], [East], [West])
) AS pvt;
```

## Safety Rules

1. **READ-ONLY by default** — only run SELECT unless the user explicitly asks to modify data
2. **Always use TOP or OFFSET-FETCH** — never run unbounded SELECT * on large tables
3. **Never expose credentials** — never print, echo, or cat any env var values or connection strings
4. **Never run DROP, DELETE, TRUNCATE, or ALTER** without explicit user confirmation
5. **Use transactions** for any write operations: BEGIN TRAN ... COMMIT / ROLLBACK
6. **Always include ORDER BY** with TOP to ensure deterministic results
7. **Always qualify table names with schema** — use `schema_name.table_name`, not just `table_name`
