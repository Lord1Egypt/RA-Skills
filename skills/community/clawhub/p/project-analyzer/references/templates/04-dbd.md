# {{PROJECT_NAME}} - Database Design Document (DBD)

## Document Info

| Item | Content |
|------|---------|
| Project Name | {{PROJECT_NAME}} |
| Version | {{VERSION}} |
| Date | {{DATE}} |

---

## 1. Database Overview

### 1.1 Database Information

| Attribute | Value |
|----------|-------|
| Database Type | {{DB_TYPE}} |
| Schema | {{SCHEMA}} |
| Character Set | {{CHARSET}} |
| Table Count | {{TABLE_COUNT}} |

### 1.2 Design Principles

| Principle | Description |
|----------|-------------|
| Normalization | Follow 3NF |
| Naming Convention | lowercase_underscore |
| Index Design | Index for frequent queries |
| Soft Delete | Use delete_time field |

---

## 2. ER Diagram

```
{{ER_DIAGRAM}}
```

---

## 3. Table Structures

{{TABLE_STRUCTURES}}

---

## 4. Index Design

### 4.1 Index Summary

| Table | Index Name | Type | Columns | Description |
|-------|-----------|------|---------|-------------|
{{INDEX_SUMMARY}}

---

## 5. Data Dictionary

{{DATA_DICTIONARY}}

---

## 6. Migration History

### 6.1 Migration Files

| File | Date | Description |
|------|------|-------------|
{{MIGRATION_HISTORY}}

---

## 7. SQL Coding Standards

### 7.1 Naming Conventions

| Object | Convention | Example |
|--------|-----------|---------|
| Table | lowercase_underscore | doc_library_info |
| Column | lowercase_underscore | lib_code |
| Index | idx/uni prefix | uk_lib_code |

### 7.2 Examples

```sql
-- Recommended
SELECT lib_code, lib_name, tenant_id
FROM {{SCHEMA}}.doc_library_info
WHERE tenant_id = 'T001'
  AND status = 1
  AND delete_time IS NULL;
```

---

*Version: {{VERSION}}*
*Last Updated: {{DATE}}*
