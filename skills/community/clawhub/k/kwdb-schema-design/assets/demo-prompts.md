---
title: Test Prompts
description: 32 example prompts for testing kwdb-schema-design skill across all DDL categories
tags: [testing, prompts, time-series, relational, mixed, index, alter, view, review]
---

# Demo Prompts

Example prompts for testing kwdb-schema-design skill.

## Schema Design (CREATE TABLE)

### Time-Series Examples

#### 1. Basic Sensor Data
```
Design a KWDB schema for temperature sensors that report every minute.
```

#### 2. IoT with Multiple Metrics
```
I need to store data from IoT devices that send temperature, humidity, and pressure readings.
```

#### 3. With Retention Requirements
```
Create a schema for storing machine sensor data for 90 days only.
```

#### 4. Complex Sensor Setup
```
Design KWDB tables for a fleet of electric vehicle chargers. Each charger reports voltage, current, power, and status every 30 seconds. Data should be kept for 1 year.
```

### Relational Examples

#### 5. E-commerce Entities
```
Write KWDB DDL for customers, products, orders, and order_items tables.
```

#### 6. User Management
```
Design a schema for a user management system with roles and permissions.
```

#### 7. Inventory System
```
Create schema for product inventory with categories and warehouse locations.
```

#### 8. With Foreign Keys
```
Design a KWDB schema for a blog system with users, posts, comments, and tags.
```

### Mixed Workload Examples

#### 9. Sensor + Device Info
```
I have temperature sensors. Each sensor has metadata (location, model, install_date) and sends readings every minute.
```

#### 10. User Activity Tracking
```
Track user logins and actions over time. I need to store user info and their activity history.
```

### Disambiguation Examples

#### 11. Ambiguous Request
```
How should I model product pricing history?
```

#### 12. Unclear Workload
```
I want to store application logs with different severity levels.
```

### Edge Case Examples

#### 13. Minimal Info
```
Design a KWDB table for storing sensor data.
```

#### 14. With Constraints
```
Create a schema for orders where total_amount must be positive and status can only be 'pending', 'shipped', or 'delivered'.
```

#### 15. JSON Data
```
Design a schema for storing user preferences as JSON.
```

#### 16. Partitioning Request
```
Create a partitioned table for monthly sales data.
```

## Index Operations

#### 17. Add Index to Relational Table
```
Add indexes to the orders table for frequently queried columns: customer_id, status, and created_at.
```

#### 18. Composite Index
```
Create an index on orders table for queries that filter by customer_id and status together.
```

#### 19. Tag Index on Time-Series
```
Add a tag index to sensor_readings table for queries that filter by sensor_type.
```

#### 20. Covering Index
```
Create an index on products table that includes columns for common SELECT queries (category, price).
```

## ALTER TABLE Operations

#### 21. Add Column
```
Add a phone column to the customers table.
```

#### 22. Add Column with Default
```
Add a status column to orders with default value 'pending'.
```

#### 23. Modify Column
```
Alter the users table to change the name column from VARCHAR(50) to VARCHAR(100).
```

#### 24. Rename Column
```
Rename the 'created' column to 'created_at' in the orders table.
```

#### 25. Add Check Constraint
```
Add a constraint to products table to ensure price is greater than 0.
```

#### 26. Set Retention on Time-Series
```
Alter the sensor_data table to set retention to 30 days.
```

## DROP Operations

#### 27. Drop Table
```
Drop the old_logs table from the database.
```

#### 28. Drop Index
```
Drop the idx_customer_status index from the orders table.
```

## View Operations

#### 29. Create View
```
Create a view for active orders that shows order details with customer name.
```

#### 30. Create Materialized View
```
Create a materialized view for monthly sales summary.
```

## Schema Review

#### 31. Review Existing Schema
```
Review this schema and suggest improvements:
CREATE TABLE users (id INT, name VARCHAR(100), email VARCHAR(254));
CREATE TABLE orders (id INT, user_id INT, amount DECIMAL(10,2));
```

#### 32. Add Missing Constraints
```
The orders table needs proper primary key and foreign key constraints. Design the ALTER statements.
```

## Test Scenarios

| # | Type | Complexity | Expected Output |
|---|------|-----------|-----------------|
| 1 | Time-series | Simple | Single TS table |
| 2 | Time-series | Medium | TS table with multiple metrics |
| 3 | Time-series | With retention | TS table + RETENTIONS clause |
| 4 | Time-series | Complex | Multi-metric TS table + tags |
| 5 | Relational | Medium | 4-table schema with FK |
| 6 | Relational | Medium | Users + roles schema |
| 7 | Relational | Simple | Single entity table |
| 8 | Relational | Complex | Multi-table with constraints |
| 9 | Mixed | Medium | Single TS table with metadata as TAGS (not separate relational table) |
| 10 | Mixed | Medium | User activity tracking |
| 11 | Disambiguation | - | Ask clarifying questions |
| 12 | Disambiguation | - | Ask about time-series vs logs |
| 13 | Edge case | Minimal | Assumptions stated |
| 14 | Constraint | Medium | CHECK constraints |
| 15 | JSON | Simple | JSONB column |
| 16 | Partitioning | Medium | RANGE partitioned table, partition column MUST be PK prefix |
| 17 | Index | Simple | ALTER TABLE ADD INDEX |
| 18 | Index | Medium | Composite index |
| 19 | Index (TS) | Simple | Tag index on time-series (INT/CHAR/BOOL only, NOT VARCHAR) |
| 20 | Index | Medium | Covering index |
| 21 | ALTER | Simple | ADD COLUMN |
| 22 | ALTER | Simple | ADD COLUMN with DEFAULT |
| 23 | ALTER | Simple | ALTER COLUMN TYPE |
| 24 | ALTER | Simple | RENAME COLUMN |
| 25 | ALTER | Medium | ADD CHECK constraint |
| 26 | ALTER (TS) | Simple | SET RETENTIONS |
| 27 | DROP | Simple | DROP TABLE (CASCADE if FK dependency exists) |
| 28 | DROP | Simple | DROP INDEX |
| 28.5 | DROP (TS) | Medium | Drop multiple TS tables - must drop one at a time (NOT `DROP TABLE t1, t2`) |
| 29 | View | Simple | CREATE VIEW |
| 30 | Materialized View | Medium | CREATE MATERIALIZED VIEW |
| 31 | Review | Medium | Schema critique |
| 32 | Schema Extension | Medium | ALTER + constraints |
