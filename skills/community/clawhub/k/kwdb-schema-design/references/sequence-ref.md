---
title: Sequence Reference
tier: 3
tags: [ddl, sequence, auto-increment, unique-rowid, uuid, gen_random_uuid, nextval, setval, serial, bigserial]
---

# Sequence Reference

Quick reference for KWDB sequences. Read when user asks about auto-increment or sequence.

## When to Use Sequence

| Use Case | Recommended Approach |
|----------|---------------------|
| Simple auto-increment ID | `INT8 DEFAULT unique_rowid()` |
| Distributed unique ID | `UUID DEFAULT gen_random_uuid()` |
| Explicit sequence control | `CREATE SEQUENCE` |
| PostgreSQL-compatible serial | Use explicit PK with default |

## CREATE SEQUENCE

```sql
CREATE SEQUENCE sequence_name;

-- With options
CREATE SEQUENCE sequence_name
    START WITH 1000
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 999999999;
```

## Use with Table

```sql
CREATE TABLE t (
    id INT8 DEFAULT nextval('sequence_name') PRIMARY KEY,
    name VARCHAR(100)
);
```

## Sequence Operations

```sql
-- Get next value
SELECT nextval('sequence_name');

-- Set current value
SELECT setval('sequence_name', 100);

-- Drop sequence
DROP SEQUENCE sequence_name;
```

## Auto-Generated ID Methods

### unique_rowid() (Recommended for single-node)

```sql
CREATE TABLE t (id INT8 DEFAULT unique_rowid() PRIMARY KEY);
```

Generates: timestamp + node ID + counter

### gen_random_uuid()

```sql
CREATE TABLE t (id UUID DEFAULT gen_random_uuid() PRIMARY KEY);
```

128-bit random UUID (very low collision risk)

### Serial Pseudo-Type

```sql
CREATE TABLE t (id SERIAL PRIMARY KEY);  -- Maps to INT4 with sequence
CREATE TABLE t (id BIGSERIAL PRIMARY KEY); -- Maps to INT8 with sequence
```

## Validation

```sql
SHOW CREATE TABLE t;  -- Shows default expression
```

## When to Use What

| Method | Use When |
|--------|----------|
| `unique_rowid()` | Single table, auto-increment, no coordination needed |
| `gen_random_uuid()` | Distributed systems, global uniqueness needed |
| `CREATE SEQUENCE` | Need explicit sequence control, multiple tables |
| `SERIAL/BIGSERIAL` | PostgreSQL compatibility, simple cases |

## Common Mistakes

| Wrong | Right |
|-------|-------|
| VARCHAR for IDs | INT/UUID |
| No PK defined | Always define PK |
| Using MAX(id)+1 | Use sequences or auto-generated |

## Design Checklist

- [ ] ID generation strategy chosen
- [ ] Single-table: unique_rowid() or UUID
- [ ] Distributed: UUID
- [ ] PK is appropriate type for use case
