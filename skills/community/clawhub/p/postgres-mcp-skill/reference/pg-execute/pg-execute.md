---
name: pg-execute
description: |
  PostgreSQL safe SQL execution tool. Supports read-only mode and access control for safely executing SQL queries and commands.
  Use when users need to execute SQL, query data, update data, insert data, or delete data.
---

## Feature Description

pg-execute provides safe SQL execution capabilities, supporting read-only mode and multi-layer security controls.

## Execution Flow

### 1. Pre-check

Confirm postgres-mcp MCP tools are available (refer to pre-check in root SKILL.md).

### 2. Check Execution Mode

Confirm postgres-mcp running mode:

- **Read-Only Mode (Restricted)** — Only allows SELECT queries
- **Full Mode (Unrestricted)** — Allows all SQL operations

Can determine current mode through configuration or environment variables.

### 3. SQL Classification and Validation

Handle differently based on SQL type:

#### Read Operations (SELECT)

**Characteristics**:
- Does not modify data
- Allowed in both read-only and full mode
- Relatively safe

**Validation**:
- Check if query is valid
- Avoid overly complex queries (prevent resource exhaustion)
- Consider adding LIMIT (if not present)

**Examples**:
```sql
SELECT * FROM orders WHERE user_id = 123;
SELECT COUNT(*) FROM users;
SELECT u.name, o.total_amount
FROM users u
JOIN orders o ON u.id = o.user_id;
```

#### Write Operations (INSERT, UPDATE, DELETE)

**Characteristics**:
- Modifies data
- Only allowed in full mode
- Requires user confirmation

**Validation**:
- Check if in read-only mode (reject execution)
- Check for WHERE conditions (avoid mistakes)
- Show SQL to be executed to user and confirm

**Examples**:
```sql
INSERT INTO orders (user_id, status, total_amount)
VALUES (123, 'pending', 99.99);

UPDATE orders
SET status = 'paid'
WHERE id = 456;

DELETE FROM orders
WHERE id = 789 AND status = 'cancelled';
```

#### DDL Operations (CREATE, ALTER, DROP)

**Characteristics**:
- Modifies database structure
- High risk, requires special caution
- Only allowed in full mode

**Validation**:
- Check if in read-only mode (reject execution)
- Strongly recommend user confirmation
- Warn about potential impact

**Examples**:
```sql
CREATE TABLE new_table (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

ALTER TABLE orders ADD COLUMN notes TEXT;

DROP TABLE old_table;
```

### 4. Execute SQL

After validation, execute SQL:

#### Direct Execution

For simple queries, execute directly:

```sql
SELECT * FROM orders WHERE user_id = 123 LIMIT 10;
```

#### Transaction Execution

For important operations, execute in transaction:

```sql
BEGIN;
UPDATE orders SET status = 'paid' WHERE id = 456;
-- Check results
COMMIT;  -- or ROLLBACK;
```

#### Batch Execution

For multiple SQL statements, execute in batch:

```sql
BEGIN;
INSERT INTO orders (user_id, status) VALUES (123, 'pending');
INSERT INTO order_items (order_id, product_id) VALUES (LASTVAL(), 456);
COMMIT;
```

### 5. Return Results

Format and return execution results:

#### Query Results

```
Query executed successfully
Returned 10 rows in 0.05 seconds

| id  | user_id | status  | total_amount |
|-----|---------|---------|--------------|
| 1   | 123     | pending | 99.99        |
| 2   | 123     | paid    | 149.99       |
...
```

#### Write Operation Results

```
UPDATE executed successfully
Affected 1 row
Execution time: 0.02 seconds
```

#### Error Messages

```
Error executing SQL:
ERROR: column "invalid_column" does not exist
LINE 1: SELECT invalid_column FROM orders
               ^
```

### 6. Security Controls

Multiple security control layers:

#### Read-Only Mode

```bash
# Enable read-only mode
postgres-mcp --read-only "postgresql://..."
```

Only allows SELECT queries, rejects all write operations.

#### SQL Validation

- **Syntax check** — Ensure SQL syntax is correct
- **Dangerous operation detection** — Warn about DROP, TRUNCATE, etc.
- **Injection prevention** — Use parameterized queries to prevent SQL injection

#### User Confirmation

For high-risk operations, must get user confirmation:

```
User: Delete all cancelled orders

Assistant: Will execute the following SQL:
         DELETE FROM orders WHERE status = 'cancelled';
         
         This will delete approximately 1000 rows.
         Confirm execution? (yes/no)
```

#### Transaction Protection

Important operations executed in transactions:

```sql
BEGIN;
-- Execute operations
UPDATE orders SET status = 'paid' WHERE id = 456;
-- Check results
SELECT * FROM orders WHERE id = 456;
-- Confirm correct then commit
COMMIT;
```

## Usage Examples

**Simple query**:
```
User: Query all pending orders
Assistant: SELECT * FROM orders WHERE status = 'pending' LIMIT 100;
```

**Update data**:
```
User: Change order 456 status to paid
Assistant: Will execute:
         UPDATE orders SET status = 'paid' WHERE id = 456;
         Confirm? (yes/no)
         
User: yes
Assistant: [Execute SQL]
         Update successful, affected 1 row
```

**Batch operations**:
```
User: Create new order and add order items
Assistant: Will execute in transaction:
         BEGIN;
         INSERT INTO orders (user_id, status) VALUES (123, 'pending');
         INSERT INTO order_items (order_id, product_id) 
         VALUES (LASTVAL(), 456);
         COMMIT;
         
         Confirm? (yes/no)
```

## Advanced Features

### Parameterized Queries

Use parameterized queries to prevent SQL injection:

```sql
-- Unsafe
SELECT * FROM orders WHERE user_id = $user_input;

-- Safe
PREPARE query AS SELECT * FROM orders WHERE user_id = $1;
EXECUTE query(123);
```

### Query Timeout

Set query timeout to prevent long-running queries:

```sql
SET statement_timeout = '30s';
SELECT * FROM large_table;
```

### Result Set Limit

Limit result set size to prevent memory overflow:

```sql
SELECT * FROM orders LIMIT 1000;
```

## Configuration Options

### Read-Only Mode

```bash
# Enable read-only mode
postgres-mcp --read-only "postgresql://..."
```

### Query Timeout

```bash
# Set query timeout to 30 seconds
postgres-mcp --query-timeout 30 "postgresql://..."
```

### Result Set Limit

```bash
# Return maximum 1000 rows
postgres-mcp --max-rows 1000 "postgresql://..."
```

## Notes

1. **Read-only mode** — Production environments recommend using read-only mode to avoid mistakes
2. **Confirmation mechanism** — Must confirm with user before write operations
3. **Transaction usage** — Execute important operations in transactions, can rollback on error
4. **Permission checks** — Ensure database user has sufficient permissions
5. **Performance impact** — Large data operations may impact database performance, choose appropriate timing
6. **Backup first** — Ensure backups exist before important operations

## Related Commands

```sql
-- View current transaction status
SELECT * FROM pg_stat_activity WHERE pid = pg_backend_pid();

-- View lock information
SELECT * FROM pg_locks;

-- View long-running queries
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > interval '1 minute';

-- Terminate query
SELECT pg_cancel_backend(pid);  -- Gentle termination
SELECT pg_terminate_backend(pid);  -- Force termination
```
