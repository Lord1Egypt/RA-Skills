---
title: Constraint Reference
tier: 2
tags: [ddl, primary-key, unique, check, foreign-key, cascade, restrict, constraint-naming, fk-index]
---

# Constraint Reference

Quick reference for KWDB constraints. Read when designing table constraints.

## Constraint Types

| Type | Purpose | Syntax | Relational | TS Table |
|------|---------|--------|:----------:|:--------:|
| PRIMARY KEY | Uniquely identify rows | `PRIMARY KEY (col1, col2)` | ✅ | ✅ (timestamp + primary tags) |
| UNIQUE | No duplicate values | `UNIQUE (col)` or column-level | ✅ | ❌ |
| CHECK | Value validation expression | `CHECK (condition)` | ✅ | ❌ |
| FOREIGN KEY | Refer integrity | `FOREIGN KEY (col) REFERENCES other(pk)` | ✅ | ❌ |

**Time-Series 表约束限制**:
- TS 表仅支持 PRIMARY KEY（timestamp + primary tags 自动构成）
- TS 表不支持 CHECK、UNIQUE、FOREIGN KEY
- **Error**: `ERROR: check constraint is not supported in timeseries table`
- **Workaround**: 在应用层做数据校验，或用 CHAR(1)/BOOL 等类型隐式限制取值范围

## Primary Key

### Relational Tables

```sql
-- Single column PK
CREATE TABLE t (id INT PRIMARY KEY, ...);

-- Composite PK
CREATE TABLE t (user_id INT, order_id INT, ..., PRIMARY KEY (user_id, order_id));

-- Auto-generated (recommended for single-table)
CREATE TABLE t (id INT8 DEFAULT unique_rowid() PRIMARY KEY, ...);

-- UUID
CREATE TABLE t (id UUID DEFAULT gen_random_uuid() PRIMARY KEY, ...);
```

### Time-Series Tables

- PK is always: timestamp column + primary tags
- First column = timestamp
- Primary tags = device identifier (max 4)

## UNIQUE Constraint

```sql
-- Column level
CREATE TABLE users (email VARCHAR(254) UNIQUE, ...);

-- Table level
CREATE TABLE t (email VARCHAR(254), phone VARCHAR(20), UNIQUE (email, phone));

-- Named constraint
CREATE TABLE t (..., CONSTRAINT uq_email UNIQUE (email));
```

**Note**: UNIQUE creates an index automatically.

## CHECK Constraint

```sql
-- Simple check
CREATE TABLE orders (
    status VARCHAR(20) CHECK (status IN ('pending', 'shipped', 'delivered')),
    amount DECIMAL(12,2) CHECK (amount > 0)
);

-- Named check
CREATE TABLE t (
    age INT4 CHECK (age >= 0 AND age < 150),
    CONSTRAINT chk_age_range CHECK (age >= 0 AND age < 150)
);

-- Complex expressions
CREATE TABLE products (
    price DECIMAL(10,2) CHECK (price >= 0),
    discount DECIMAL(10,2) CHECK (discount >= 0 AND discount <= price)
);
```

## Foreign Key

```sql
-- Basic FK
CREATE TABLE orders (
    customer_id UUID REFERENCES customers(id),
    ...
);

-- With ON DELETE/UPDATE actions
CREATE TABLE order_items (
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    ...
);

-- Named FK
CREATE TABLE t (
    ..., CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

**Rules**:
1. Referenced column must be PRIMARY KEY or UNIQUE
2. FK column MUST be indexed — **KWDB auto-creates an index** (named `<table>_auto_index_<constraint_name>`), so do NOT manually create a duplicate index on FK columns
3. ON DELETE: CASCADE, SET NULL, RESTRICT, NO ACTION
4. ON UPDATE: CASCADE, SET NULL, RESTRICT, NO ACTION

## ALTER TABLE with Constraints

```sql
-- Add constraint
ALTER TABLE t ADD CONSTRAINT chk_amount CHECK (amount > 0);

-- Drop constraint
ALTER TABLE t DROP CONSTRAINT chk_amount;

-- Add FK
ALTER TABLE t ADD CONSTRAINT fk_ref FOREIGN KEY (col) REFERENCES other(pk);

-- Drop FK
ALTER TABLE t DROP CONSTRAINT fk_ref;
```

## Validation

```sql
SHOW CONSTRAINTS FROM table_name;
SHOW CREATE TABLE table_name;
```

## Constraint Best Practices

### Error vs Correct Examples

**Incorrect (no constraints):**
```sql
CREATE TABLE orders (
    id INT,
    customer_id INT,
    status VARCHAR(20),
    amount FLOAT,
    email VARCHAR(254)
);
-- No PK, no FK, no CHECK, FLOAT for money, email not unique
```

**Correct (with constraints):**
```sql
CREATE TABLE orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    customer_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled')),
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);
CREATE INDEX idx_orders_customer ON orders (customer_id);
```

**Incorrect (circular FK):**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    default_order UUID REFERENCES orders(id)  -- Circular: orders references users
);
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id)
);
```

**Correct (no circular dependency):**
```sql
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY
);
CREATE TABLE orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id)
);
-- Move default_order to application logic, not FK
```

### Do vs Don't

| Do | Don't |
|----|-------|
| Use CHECK for valid value ranges | CHECK on same column as UNIQUE |
| Use FK for refer integrity | Circular FK references |
| Index FK columns | Forget to index FK columns |
| Name constraints meaningfully | Rely on auto-generated names |
| `NOT NULL` for required fields | Allow NULL when data is required |
| `DECIMAL` for money in constraints | `CHECK (amount > 0)` with FLOAT |

## Common Patterns

### Status Field
```sql
status VARCHAR(20) NOT NULL DEFAULT 'pending'
CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled'))
```

### Positive Amount
```sql
amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0)
```

### Email Format (basic)
```sql
email VARCHAR(254) NOT NULL UNIQUE
```

### Phone Number
```sql
phone VARCHAR(20) CHECK (phone ~ '^[0-9\-\+\(\)]+$')
```

### Date Range
```sql
start_date DATE NOT NULL,
end_date DATE CHECK (end_date >= start_date)
```

## Design Checklist

- [ ] Required fields are NOT NULL
- [ ] Unique columns have UNIQUE constraint
- [ ] Value ranges validated with CHECK
- [ ] Foreign key relationships identified
- [ ] FK columns indexed
- [ ] Constraint names are meaningful
- [ ] CASCADE/RESTRICT behavior decided
