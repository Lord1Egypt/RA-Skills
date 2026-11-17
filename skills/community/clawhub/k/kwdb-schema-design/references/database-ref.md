---
title: Database and Schema Operations Reference
tier: 4
tags: [ddl, database, schema, multi-tenant, create-database, drop-database, public-schema, isolation]
---

# Database Reference

Quick reference for KWDB database and schema operations. **Low-frequency DDL** - only read when user explicitly asks about database-level operations.

## DATABASE Operations

### CREATE DATABASE (Relational)

```sql
CREATE DATABASE db_name;
CREATE DATABASE IF NOT EXISTS db_name;
```

Creates a **relational** database. Only relational tables can be created in it.

### CREATE TS DATABASE (Time-Series)

```sql
CREATE TS DATABASE IF NOT EXISTS db_name;
```

Creates a **time-series** database. **Time-series tables (with TAGS/PRIMARY TAGS) can ONLY be created in a TS database.** Attempting to create a time-series table in a relational database will result in: `ERROR: can not create timeseries table in relational database`.

**Key Rules**:
- Time-series tables → must use TS database
- Relational tables → must use relational database
- A database's type (relational/TS) is determined at creation time and cannot be changed
- Time-series tables only support `database.table` (always use public schema)

### DROP DATABASE

```sql
DROP DATABASE db_name;
DROP DATABASE IF EXISTS db_name;
```

### USE/SET DATABASE

```sql
SET database = db_name;  -- or
USE db_name;
```

## SCHEMA Operations

### CREATE SCHEMA

```sql
CREATE SCHEMA schema_name;
```

### DROP SCHEMA

```sql
DROP SCHEMA schema_name;
DROP SCHEMA schema_name CASCADE;  -- Drop all objects
```

## SHOW Commands

```sql
SHOW DATABASES;
SHOW SCHEMAS FROM database_name;
SHOW TABLES FROM database_name.schema_name;
```

## When to Use

| Task | Approach |
|------|----------|
| Multi-tenant data isolation | Separate databases or schemas |
| Development/Testing | Separate schemas in same DB |
| Production deployment | Separate databases |

## Note

- Relational tables support schema prefix: `database.schema.table`
- Time-series tables only support `database.table` (always use public schema)
- **CRITICAL**: Time-series tables require a TS database; relational tables require a relational database. Check database type before creating tables with `SHOW DATABASES;`.

## Validation

```sql
SHOW CREATE DATABASE db_name;
SELECT * FROM information_schema.schemata;
```
