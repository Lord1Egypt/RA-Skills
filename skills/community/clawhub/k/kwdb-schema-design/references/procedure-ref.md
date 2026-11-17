---
title: Stored Procedure and Function Reference
tier: 4
tags: [ddl, procedure, function, plpgsql, stored-procedure, call, select-func, transaction-control]
---

# Procedure Reference

Quick reference for KWDB stored procedures and functions. **Low-frequency DDL** - only read when user explicitly asks.

## Overview

Procedures and functions encapsulate business logic in the database.

**Key Differences**:
| Feature | Function | Procedure |
|---------|----------|-----------|
| Return value | Required | Optional |
| Call方式 | SELECT func() | CALL proc() |
| Transaction control | Cannot commit/rollback | Can control transactions |

## CREATE FUNCTION

```sql
CREATE FUNCTION function_name(param1 TYPE, param2 TYPE)
RETURNS return_type AS $$
BEGIN
    -- logic
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

## CREATE PROCEDURE

```sql
CREATE PROCEDURE procedure_name(param1 TYPE)
AS $$
BEGIN
    -- logic
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
$$ LANGUAGE plpgsql;
```

## When to Use

| Use Case | Consider Instead |
|----------|------------------|
| Computed column value | Application logic |
| Complex calculations | Application logic |
| Transactional batch | Application with explicit transaction |

## Note

- KWDB focus is on distributed SQL, not heavy stored procedure usage
- Most business logic should live in application layer for maintainability

## Validation

```sql
SHOW FUNCTIONS FROM database_name;
SHOW PROCEDURES FROM database_name;
```
