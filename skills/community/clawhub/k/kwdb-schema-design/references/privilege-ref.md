---
title: User, Role, and Privilege Reference
tier: 4
tags: [ddl, user, role, privilege, grant, revoke, permissions, admin, sysadmin, security]
---

# Privilege Reference

Quick reference for KWDB user, role, and privilege management. **Low-frequency DDL** - only read when user explicitly asks about permissions.

## USER Operations

### CREATE USER

```sql
CREATE USER user_name WITH PASSWORD 'password';
```

### DROP USER

```sql
DROP USER user_name;
```

## ROLE Operations

### CREATE ROLE

```sql
CREATE ROLE role_name;
```

### GRANT Role

```sql
GRANT role_name TO user_name;
```

## PRIVILEGE Operations

### GRANT

```sql
-- Table privileges
GRANT SELECT, INSERT ON table_name TO user_name;
GRANT ALL ON table_name TO user_name;

-- Database privileges
GRANT CREATE ON DATABASE db_name TO user_name;

-- Role membership
GRANT role_name TO user_name;
```

### REVOKE

```sql
REVOKE SELECT ON table_name FROM user_name;
REVOKE role_name FROM user_name;
```

## Privilege Types

| Privilege | Applicable To |
|-----------|---------------|
| SELECT | Tables, Views |
| INSERT | Tables |
| UPDATE | Tables |
| DELETE | Tables |
| CREATE | Databases, Schemas, Tables |
| DROP | Databases, Schemas, Tables |
| REFERENCES | Tables |
| ALL | All applicable |

## Built-in Roles

| Role | Description |
|------|-------------|
| admin | Non-three权分立: full privileges |
| sysadmin | Three权分立: full privileges |

## When to Design Privileges

- Multi-user environments
- Application service accounts
- Read-only reporting users

## Note

- Privilege design is typically done by DBA, not application developers
- Schema design should focus on table structure, not security

## Validation

```sql
SHOW GRANTS FOR user_name;
SHOW ROLES FOR user_name;
```
