---
title: Output Templates
description: Response format templates for all schema design operations (CREATE TABLE, ALTER TABLE, INDEX, VIEW, DROP, REVIEW)
tags: [template, response-format, time-series, relational, alter, index, view, drop, review]
---

# Output Template

Use this template for schema design responses.

## Template

```markdown
## Intent
[Brief description of what this schema is for]

## Workload Type
[relational / time-series / mixed]

## Assumptions
- [Assumption 1]
- [Assumption 2]

## Design
| Table | Type | Primary Key | Purpose |
|-------|------|-------------|---------|
| table_name | [relational/ts] | [pk description] | [purpose] |

### Column Details
| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| col1 | TYPE | NOT NULL / NULL | value | [notes] |

### Indexes
| Index | Columns | Type | Purpose |
|-------|---------|------|---------|
| idx_name | (col1, col2) | btree | [purpose] |

## DDL
```sql
-- Table creation DDL
CREATE TABLE ...;
```

## Validation
```sql
-- Verify table created
SHOW CREATE TABLE table_name;

-- Verify columns
SHOW COLUMNS FROM table_name;
```
```

## Example: Time-Series

```markdown
## Intent
Store temperature sensor readings from IoT devices

## Workload Type
time-series

## Assumptions
- Retention: 180 days (default assumption)
- Timestamp precision: millisecond (3)
- Primary tag: sensor_id

## Design
| Table | Type | Primary Tag | Purpose |
|-------|------|-------------|---------|
| sensor_readings | time-series | sensor_id | Temperature readings |

### Column Details
| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| k_timestamp | TIMESTAMPTZ | NOT NULL | Timestamp (ms precision) |
| temperature | FLOAT4 | NOT NULL | Temperature value |
| humidity | FLOAT4 | NULL | Humidity value |

### Tags
| Tag | Type | Primary | Notes |
|-----|------|---------|-------|
| sensor_id | INT4 | YES | Device identifier |
| location | VARCHAR(50) | NO | Installation location |

## DDL
```sql
CREATE TABLE sensor_readings (
    k_timestamp TIMESTAMPTZ(3) NOT NULL,
    temperature FLOAT4 NOT NULL,
    humidity FLOAT4 NULL
) TAGS (
    sensor_id INT4 NOT NULL,
    location VARCHAR(50) NULL
) PRIMARY TAGS (sensor_id)
RETENTIONS 180d;
```

## Validation
```sql
SHOW CREATE TABLE sensor_readings;
SHOW COLUMNS FROM sensor_readings;
SHOW TAGS FROM sensor_readings;
```
```

## Example: Relational

```markdown
## Intent
Track customer orders in e-commerce system

## Workload Type
relational

## Assumptions
- Auto-generated primary keys
- Soft delete via status field
- No partitioning initially

## Design
| Table | Purpose |
|-------|---------|
| customers | Customer information |
| orders | Order header |
| order_items | Order line items |

### customers
| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| id | UUID | NOT NULL | PK, auto-generated |
| email | VARCHAR(254) | NOT NULL | Unique |
| name | VARCHAR(100) | NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL | |

### orders
| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| id | UUID | NOT NULL | PK |
| customer_id | UUID | NOT NULL | FK → customers |
| status | VARCHAR(20) | NOT NULL | |
| total_amount | DECIMAL(12,2) | NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL | |

## DDL
```sql
CREATE TABLE customers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(254) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    customer_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE INDEX idx_orders_customer ON orders (customer_id);
```

## Validation
```sql
SHOW CREATE TABLE customers;
SHOW CREATE TABLE orders;
SHOW CONSTRAINTS FROM orders;
```
```

---

## ALTER TABLE Templates

### Add Column

```markdown
## Intent
Add [column description] to existing table

## Target Table
[table_name]

## Modification
| Action | Column | Type | Default | Notes |
|--------|--------|------|---------|-------|
| ADD | column_name | TYPE | [DEFAULT val] | [NULL/NOT NULL] |

## DDL
```sql
ALTER TABLE table_name ADD COLUMN column_name TYPE [DEFAULT default_val];
```

## Validation
```sql
SHOW COLUMNS FROM table_name;
```
```

### Alter Column Type

```markdown
## Intent
Modify column type in existing table

## Target Table
[table_name]

## Modification
| Action | Column | Old Type | New Type |
|--------|--------|----------|----------|
| ALTER TYPE | column_name | VARCHAR(50) | VARCHAR(100) |

## DDL
```sql
ALTER TABLE table_name ALTER COLUMN column_name TYPE new_type;
```

## Validation
```sql
SHOW COLUMNS FROM table_name;
```
```

### Add Constraint

```markdown
## Intent
Add [constraint type] constraint to table

## Target Table
[table_name]

## Constraint Details
| Type | Name | Definition |
|------|------|------------|
| CHECK | constraint_name | condition |

## DDL
```sql
ALTER TABLE table_name ADD CONSTRAINT constraint_name CHECK (condition);
```

## Validation
```sql
SHOW CONSTRAINTS FROM table_name;
```
```

### Set Retention (Time-Series)

```markdown
## Intent
Set retention policy on time-series table

## Target Table
[table_name]

## Modification
| Action | Parameter | Value |
|--------|-----------|-------|
| SET RETENTIONS | keep_duration | 30d |

## DDL
```sql
ALTER TABLE table_name SET RETENTIONS = 30d;
```

## Validation
```sql
SHOW RETENTIONS ON TABLE table_name;
```
```

---

## INDEX Templates

### Create Index

```markdown
## Intent
Create index for [query pattern description]

## Target Table
[table_name]

## Index Design
| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| idx_name | (col1, col2) | btree | [optimize filter/join/sort] |

## DDL
```sql
CREATE INDEX idx_name ON table_name (col1, col2);
```

## Validation
```sql
SHOW INDEX FROM table_name;
```
```

### Composite Index

```markdown
## Intent
Create composite index for [query pattern]

## Target Table
[table_name]

## Index Design
| Index Name | Columns | Order | Purpose |
|------------|---------|-------|---------|
| idx_name | (col1, col2) | col1 first | Filter by col1, then col2 |

## DDL
```sql
CREATE INDEX idx_name ON table_name (col1, col2);
```

## Query Pattern
```sql
SELECT * FROM table_name WHERE col1 = 'value' AND col2 > 100;
```

## Validation
```sql
SHOW INDEX FROM table_name;
EXPLAIN SELECT * FROM table_name WHERE col1 = 'value' AND col2 > 100;
```
```

### Covering Index

```markdown
## Intent
Create covering index to avoid table lookup

## Target Table
[table_name]

## Query
```sql
SELECT name, price FROM products WHERE category = 'electronics';
```

## Index Design
| Index Name | Key Columns | Stored Columns | Purpose |
|------------|-------------|----------------|---------|
| idx_products_category | (category) | (name, price) | Cover SELECT |

## DDL
```sql
CREATE INDEX idx_products_category ON products (category) STORING (name, price);
```

## Validation
```sql
SHOW INDEX FROM products;
EXPLAIN SELECT name, price FROM products WHERE category = 'electronics';
```
```

---

## VIEW Templates

### Create View

```markdown
## Intent
Create view to simplify [use case]

## View Definition
| View Name | Columns | Base Table |
|----------|---------|------------|
| view_name | col1, col2 | table_name |

## SQL
```sql
CREATE VIEW view_name AS
SELECT col1, col2
FROM table_name
WHERE condition;
```

## Validation
```sql
SHOW CREATE VIEW view_name;
SELECT * FROM view_name LIMIT 1;
```
```

### Create Materialized View

```markdown
## Intent
Pre-compute [aggregation] for faster reporting

## Materialized View Definition
| Name | Query | Refresh |
|------|-------|---------|
| mv_name | SELECT ... GROUP BY ... | MANUAL |

## DDL
```sql
CREATE MATERIALIZED VIEW mv_name AS
SELECT col1, COUNT(*) as cnt, SUM(amount) as total
FROM table_name
GROUP BY col1;
```

## Validation
```sql
SHOW CREATE MATERIALIZED VIEW mv_name;
SELECT * FROM mv_name LIMIT 1;
```
```

---

## DROP Templates

### Drop Table

```markdown
## Intent
Drop [table_name] from database

## Impact
- All data will be deleted
- Indexes will be removed
- Dependent views will be affected

## DDL
```sql
DROP TABLE table_name;           -- Error if not exists
DROP TABLE IF EXISTS table_name;  -- Silent if not exists
DROP TABLE table_name CASCADE;    -- Drop + dependent objects
```

## Validation
```sql
SHOW TABLES;  -- Verify table is gone
```
```

### Drop Index

```markdown
## Intent
Drop index [index_name] from table

## Target Table
[table_name]

## DDL
```sql
DROP INDEX table_name@index_name;
DROP INDEX IF EXISTS table_name@index_name;
```

## Validation
```sql
SHOW INDEX FROM table_name;  -- Verify index is gone
```
```

---

## Schema Review Template

```markdown
## Review Request
[User's schema or description]

## Analysis

### Issues Found
| # | Severity | Description | Recommendation |
|---|----------|-------------|----------------|
| 1 | [High/Medium/Low] | [Issue] | [Fix] |

### Suggestions
- [Improvement 1]
- [Improvement 2]

## Corrected DDL
```sql
-- Original issues fixed
CREATE TABLE ...;
```

## Validation
```sql
-- Verify corrected schema
SHOW CREATE TABLE table_name;
```
```
