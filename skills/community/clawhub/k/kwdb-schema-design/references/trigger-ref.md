---
title: Trigger Reference
tier: 4
tags: [ddl, trigger, plpgsql, audit-logging, before-trigger, after-trigger, row-level, statement-level]
---

# Trigger Reference

Quick reference for KWDB triggers. **Low-frequency DDL** - only read when user explicitly asks.

## Overview

Triggers execute automatically on INSERT/UPDATE/DELETE events.

**Common Use Cases**:
- Audit logging (track changes)
- Enforce complex business rules
- Maintain derived data

## CREATE TRIGGER

```sql
-- Row-level trigger
CREATE TRIGGER trigger_name
    BEFORE INSERT OR UPDATE ON table_name
    FOR EACH ROW
    EXECUTE FUNCTION function_name(args);

-- Statement-level
CREATE TRIGGER trigger_name
    AFTER DELETE ON table_name
    FOR EACH STATEMENT
    EXECUTE FUNCTION function_name(args);
```

## DROP TRIGGER

```sql
DROP TRIGGER trigger_name ON table_name;
```

## Trigger Functions

```sql
CREATE FUNCTION audit_func()
RETURNS trigger AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, action, new_data)
        VALUES (TG_TABLE_NAME, 'INSERT', row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, action, old_data, new_data)
        VALUES (TG_TABLE_NAME, 'UPDATE', row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, action, old_data)
        VALUES (TG_TABLE_NAME, 'DELETE', row_to_json(OLD));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

## When to Use

| Use Case | Consider Instead |
|----------|------------------|
| Audit logging | Separate application logic, or use changelog table |
| Complex validation | CHECK constraint (simpler) |
| Auto-updates | DEFAULT values, trigger is overkill |

## Limitation

- KWDB triggers are **not commonly used** for performance reasons
- Consider application-level enforcement for high-throughput scenarios

## Validation

```sql
SHOW TRIGGERS FROM table_name;
```
