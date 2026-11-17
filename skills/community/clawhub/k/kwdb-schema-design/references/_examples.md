---
title: Complete Dialogue Examples
tier: 1
tags: [examples, dialogue, workflow, disambiguation]
---

# Examples

Complete examples showing the full workflow: user request → clarification → DDL → validation.

---

## Example 1: Time-Series (Explicit)

**User:**
```
Design a KWDB schema for temperature sensors that report every minute.
```

**Agent Response:**
```
## Intent
Store temperature readings from sensors

## Workload Type
time-series

## Clarifying Questions
- What's the retention period? (default: 180 days)
- Timestamp precision needed? (default: millisecond)
- Device identifier: sensor_id (INT) or UUID?

## Assumptions
- Retention: 180 days (default)
- Timestamp precision: 3 (millisecond)
- Primary tag: sensor_id

## Design
| Table | Type | Primary Tag | Purpose |
|-------|------|-------------|---------|
| sensor_readings | time-series | sensor_id | Temperature data |

### Columns
| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| k_timestamp | TIMESTAMPTZ(3) | NOT NULL | Timestamp |
| temperature | FLOAT4 | NOT NULL | Temperature °C |

### Tags
| Tag | Type | Primary | Notes |
|-----|------|---------|-------|
| sensor_id | INT4 | YES | Device ID |

## DDL
```sql
CREATE TABLE sensor_readings (
    k_timestamp TIMESTAMPTZ(3) NOT NULL,
    temperature FLOAT4 NOT NULL
) TAGS (
    sensor_id INT4 NOT NULL
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

---

## Example 2: Time-Series (Minimal Info - Assume)

**User:**
```
Create a schema for storing machine sensor data.
```

**Agent Response:**
```
## Intent
Store machine sensor readings

## Workload Type
time-series (assumed based on "sensor data")

## Assumptions
- Workload: time-series (user said "sensor data")
- Retention: 180 days (default assumption, state explicitly)
- Timestamp precision: 3 (millisecond)
- Primary tag: machine_id (INT4, assume single device per table)

**Please confirm:** Do you need different retention period? Is there one machine or multiple?

## Design
| Table | Type | Primary Tag | Purpose |
|-------|------|-------------|---------|
| machine_data | time-series | machine_id | Machine sensor readings |

### Columns
| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| k_timestamp | TIMESTAMPTZ(3) | NOT NULL | Timestamp |
| value | FLOAT8 | NOT NULL | Sensor value |

### Tags
| Tag | Type | Primary | Notes |
|-----|------|---------|-------|
| machine_id | INT4 | YES | Machine identifier |

## DDL
```sql
CREATE TABLE machine_data (
    k_timestamp TIMESTAMPTZ(3) NOT NULL,
    value FLOAT8 NOT NULL
) TAGS (
    machine_id INT4 NOT NULL
) PRIMARY TAGS (machine_id)
RETENTIONS 180d;
```

## Validation
```sql
SHOW CREATE TABLE machine_data;
```
```

---

## Example 3: Relational (Explicit)

**User:**
```
Write KWDB DDL for customers, products, orders, and order_items tables.
```

**Agent Response:**
```
## Intent
E-commerce order management system

## Workload Type
relational

## Design
### customers
| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| id | UUID | NOT NULL | PK, auto-generated |
| email | VARCHAR(254) | NOT NULL | Unique |
| name | VARCHAR(100) | NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL | Default NOW() |

### products
| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| id | UUID | NOT NULL | PK |
| name | VARCHAR(200) | NOT NULL | |
| price | DECIMAL(10,2) | NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL | |

### orders
| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| id | UUID | NOT NULL | PK |
| customer_id | UUID | NOT NULL | FK → customers |
| status | VARCHAR(20) | NOT NULL | pending/shipped/delivered |
| total_amount | DECIMAL(12,2) | NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL | |

### order_items
| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| id | UUID | NOT NULL | PK |
| order_id | UUID | NOT NULL | FK → orders |
| product_id | UUID | NOT NULL | FK → products |
| quantity | INT4 | NOT NULL | |
| price | DECIMAL(10,2) | NOT NULL | |

## DDL
```sql
CREATE TABLE customers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(254) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE products (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    customer_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    order_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INT4 NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products(id)
);

-- KWDB 为 FK 自动创建索引，无需手动再建
-- 用 SHOW INDEX FROM order_items; 可看到 auto_index 索引
-- 仅当需要复合索引（如 (order_id, product_id)）时才手动添加
```

## Validation
```sql
SHOW CREATE TABLE customers;
SHOW CREATE TABLE products;
SHOW CREATE TABLE orders;
SHOW CREATE TABLE order_items;
SHOW CONSTRAINTS FROM orders;
```
```

---

## Example 4: Ambiguous - Ask Disambiguation

**User:**
```
How should I store product pricing history?
```

**Agent Response:**
```
Before I design the schema, I need to clarify:

**Q1: Is this time-series or relational?**
- Time-series: You track price changes over time as a continuous stream
- Relational: You store snapshots of prices for different products

**Q2: What's the data model?**
- Time-series: (timestamp, product_id, price)
- Relational: (product_id, price, effective_date, end_date)

**Q3: How long do you need to retain?**
- For analytics: Keep historical data (time-series)
- Current only: Just update the price field (relational)

**Q4: How often does price change?**
- Frequent updates → Relational (UPDATE)
- Every record is new → Time-series (INSERT)

---

Please clarify which model fits your use case, or describe your data.
```

---

## Example 5: Alter Table Operations

**User:**
```
Add a phone column to the customers table.
```

**Agent Response:**
```
## Intent
Add phone column to existing table

## Target Table
customers

## Modification
| Action | Column | Type | Nullable | Default |
|--------|--------|------|----------|---------|
| ADD | phone | VARCHAR(20) | NULL | - |

## DDL
```sql
ALTER TABLE customers ADD COLUMN phone VARCHAR(20);
```

## Validation
```sql
SHOW COLUMNS FROM customers;
```

## Follow-up Considerations
- Add CHECK constraint if format matters: `CHECK (phone ~ '^[0-9\-\+\(\)]+$')`
- Index if phone is used for lookups: `CREATE INDEX idx_customers_phone ON customers (phone);`
```

---

## Example 6: Index Creation

**User:**
```
Create an index on orders table for queries that filter by customer_id and status together.
```

**Agent Response:**
```
## Intent
Create composite index for customer+status queries

## Target Table
orders

## Query Pattern
```sql
SELECT * FROM orders WHERE customer_id = 'xxx' AND status = 'pending';
-- or
SELECT * FROM orders WHERE customer_id = 'xxx';
```

## Index Design
| Index Name | Columns | Order | Purpose |
|------------|---------|-------|---------|
| idx_orders_customer_status | (customer_id, status) | customer_id first | Filter by customer, then status |

## Reasoning
- **customer_id first**: Most selective, used in both single and multi-column queries
- **status second**: Additional filter after customer_id

## DDL
```sql
CREATE INDEX idx_orders_customer_status ON orders (customer_id, status);
```

## Validation
```sql
SHOW INDEX FROM orders;
EXPLAIN SELECT * FROM orders WHERE customer_id = 'xxx' AND status = 'pending';
```

## Note
If queries always filter by both columns in AND condition, this composite index is optimal.
If queries sometimes filter by status alone, consider adding a separate index on (status).
```

---

## Example 7: Mixed Workload

**User:**
```
I have temperature sensors. Each sensor has metadata (location, model, install_date) and sends readings every minute.
```

**Agent Response:**
```
## Intent
IoT sensor system with entity metadata + time-series readings

## Workload Type
mixed (entity + time-series)

## Design
Two tables with JOIN for combined queries:

### sensor_entities (Relational)
Store sensor metadata - updated occasionally, queried for device info.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| id | INT4 | NOT NULL | PK, matches sensor_id in TS table |
| name | VARCHAR(100) | NOT NULL | Sensor name |
| location | VARCHAR(100) | NULL | Installation location |
| model | VARCHAR(50) | NULL | Device model |
| install_date | DATE | NULL | Installation date |

### sensor_readings (Time-Series)
Store readings - high-volume INSERT, time-range queries.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| k_timestamp | TIMESTAMPTZ(3) | NOT NULL | Timestamp |
| temperature | FLOAT4 | NOT NULL | Temperature reading |

**Tags:**
| Tag | Type | Primary | Notes |
|-----|------|---------|-------|
| sensor_id | INT4 | YES | Links to sensor_entities.id |

## DDL
```sql
-- Entity table (relational)
CREATE TABLE sensor_entities (
    id INT4 PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NULL,
    model VARCHAR(50) NULL,
    install_date DATE NULL
);

-- Time-series table
CREATE TABLE sensor_readings (
    k_timestamp TIMESTAMPTZ(3) NOT NULL,
    temperature FLOAT4 NOT NULL
) TAGS (
    sensor_id INT4 NOT NULL
) PRIMARY TAGS (sensor_id)
RETENTIONS 180d;

-- Index for joining
CREATE INDEX idx_sensor_readings_sensor ON sensor_readings (sensor_id);
```

## Validation
```sql
SHOW CREATE TABLE sensor_entities;
SHOW CREATE TABLE sensor_readings;
SHOW TAGS FROM sensor_readings;
```

## Usage
```sql
-- Get readings with sensor info
SELECT r.*, e.name, e.location
FROM sensor_readings r
JOIN sensor_entities e ON r.sensor_id = e.id
WHERE r.k_timestamp >= NOW() - INTERVAL '1 day';
```
```

---

## Key Patterns

1. **Always classify workload type first** - relational / time-series / mixed
2. **Ask clarifying questions** when request is ambiguous
3. **State assumptions** when information is incomplete
4. **Include validation steps** with every DDL
5. **Add indexes for FK columns** (explicit or confirm auto-created)
6. **Use appropriate types** - DECIMAL for money, FLOAT for measurements
