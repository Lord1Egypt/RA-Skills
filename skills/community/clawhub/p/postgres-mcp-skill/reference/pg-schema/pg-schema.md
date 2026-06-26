---
name: pg-schema
description: |
  PostgreSQL database schema query and intelligent SQL generation tool. Understands database structure and generates SQL queries that conform to the schema.
  Use when users ask about table structure, field information, table relationships, need to generate SQL, or query what tables exist in the database.
---

## Feature Description

pg-schema provides intelligent querying and understanding of database schemas, helping generate accurate SQL statements.

## Execution Flow

### 1. Pre-check

Confirm postgres-mcp MCP tools are available (refer to pre-check in root SKILL.md).

### 2. Schema Query

Query different levels of schema information based on user needs.

#### Query All Tables

```sql
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename;
```

#### Query Table Structure

```sql
SELECT
  column_name,
  data_type,
  character_maximum_length,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_name = 'orders'
ORDER BY ordinal_position;
```

#### Query Primary and Foreign Keys

```sql
-- Primary keys
SELECT a.attname
FROM pg_index i
JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
WHERE i.indrelid = 'orders'::regclass AND i.indisprimary;

-- Foreign keys
SELECT
  tc.constraint_name,
  tc.table_name,
  kcu.column_name,
  ccu.table_name AS foreign_table_name,
  ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = 'orders';
```

#### Query Indexes

```sql
SELECT
  indexname,
  indexdef
FROM pg_indexes
WHERE tablename = 'orders';
```

#### Query Table Size

```sql
SELECT
  pg_size_pretty(pg_total_relation_size('orders')) AS total_size,
  pg_size_pretty(pg_relation_size('orders')) AS table_size,
  pg_size_pretty(pg_total_relation_size('orders') - pg_relation_size('orders')) AS indexes_size;
```

### 3. Understand Schema

Based on schema information, build understanding of database structure:

#### Table Relationships
- **One-to-many** — Foreign key relationships
- **Many-to-many** — Through junction tables
- **One-to-one** — Unique foreign keys

#### Data Types
- **Numeric types** — integer, bigint, numeric, real, etc.
- **String types** — varchar, text, char, etc.
- **Date/time types** — timestamp, date, time, interval, etc.
- **Boolean type** — boolean
- **JSON types** — json, jsonb
- **Array types** — integer[], text[], etc.

#### Constraints
- **NOT NULL** — Field cannot be null
- **UNIQUE** — Field value must be unique
- **CHECK** — Custom validation rules
- **DEFAULT** — Default values

### 4. Generate SQL

Based on user intent and schema information, generate accurate SQL statements.

#### Simple Query

```
User: Query all pending orders
Assistant: [Check orders table structure]
         [Confirm status field exists]
         SELECT * FROM orders WHERE status = 'pending';
```

#### Join Query

```
User: Query user names and their order amounts
Assistant: [Check users and orders table relationships]
         [Confirm foreign key relationship]
         SELECT u.name, o.total_amount
         FROM users u
         JOIN orders o ON u.id = o.user_id;
```

#### Aggregate Query

```
User: Count orders per user
Assistant: SELECT user_id, COUNT(*) as order_count
         FROM orders
         GROUP BY user_id;
```

#### Complex Query

```
User: Query users who placed orders in the last 30 days and their total order amounts
Assistant: SELECT
           u.id,
           u.name,
           COUNT(o.id) as order_count,
           SUM(o.total_amount) as total_amount
         FROM users u
         JOIN orders o ON u.id = o.user_id
         WHERE o.created_at > NOW() - INTERVAL '30 days'
         GROUP BY u.id, u.name
         ORDER BY total_amount DESC;
```

### 5. Validate SQL

Before executing generated SQL, validate:

1. **Table existence** — Confirm all referenced tables exist
2. **Field existence** — Confirm all referenced fields exist
3. **Data type matching** — Confirm comparison operations match data types
4. **Syntax correctness** — Confirm SQL syntax is correct

### 6. Optimize SQL

Optimize generated SQL:

- **Avoid SELECT *** — Only query needed fields
- **Use appropriate indexes** — Ensure WHERE conditions can use indexes
- **Limit result set** — Add LIMIT for large result sets
- **Use EXPLAIN** — Check execution plan to ensure performance

## Usage Examples

**Query table structure**:
```
User: What fields does the orders table have?
Assistant: [Query orders table structure]
         orders table has the following fields:
         - id (bigint, primary key)
         - user_id (bigint, foreign key to users)
         - status (varchar)
         - total_amount (numeric)
         - created_at (timestamp)
```

**Generate query SQL**:
```
User: Query all orders for user 123
Assistant: [Check schema]
         SELECT * FROM orders WHERE user_id = 123;
```

**Generate complex SQL**:
```
User: I want to see each user's order count and total amount, sorted by amount
Assistant: [Analyze schema and relationships]
         SELECT
           u.id,
           u.name,
           COUNT(o.id) as order_count,
           SUM(o.total_amount) as total_amount
         FROM users u
         LEFT JOIN orders o ON u.id = o.user_id
         GROUP BY u.id, u.name
         ORDER BY total_amount DESC NULLS LAST;
```

## Advanced Features

### Schema Caching

Cache frequently queried schema information to avoid repeated queries:

```
# First query: Get from database
User: What fields does orders have?
Assistant: [Query database] [Cache results]

# Subsequent queries: Use cache
User: Generate a query for orders
Assistant: [Use cached schema] [Generate SQL]
```

### Intelligent Field Matching

Fuzzy match user input to actual field names:

```
User: Query orders by creation time
Assistant: [Match "creation time" to created_at field]
         SELECT * FROM orders WHERE created_at > ?;
```

### Relationship Inference

Automatically infer table relationships:

```
User: Query user names and order amounts
Assistant: [Infer users.id = orders.user_id relationship]
         [Generate JOIN query]
```

## Notes

1. **Schema caching** — Schema information can be cached to avoid repeated queries
2. **Permission checks** — Ensure user has permission to access relevant tables and fields
3. **Large databases** — For databases with many tables, query on-demand rather than loading all schemas at once
4. **Schema changes** — Note that schemas may change, refresh cache periodically
5. **Naming conventions** — Follow database naming conventions (like snake_case)

## Related Queries

```sql
-- Query all views
SELECT schemaname, viewname
FROM pg_views
WHERE schemaname NOT IN ('pg_catalog', 'information_schema');

-- Query all functions
SELECT proname, prosrc
FROM pg_proc
WHERE pronamespace = 'public'::regnamespace;

-- Query all triggers
SELECT tgname, tgrelid::regclass, tgtype
FROM pg_trigger
WHERE tgisinternal = false;

-- Query table comments
SELECT
  c.relname AS table_name,
  d.description
FROM pg_class c
LEFT JOIN pg_description d ON c.oid = d.objoid
WHERE c.relkind = 'r' AND c.relnamespace = 'public'::regnamespace;
```
