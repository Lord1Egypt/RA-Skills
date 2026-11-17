<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: database-rules.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Data Architecture | date: {generation-date} -->

# Database Rules

## Data Layer Identity
**Database:** {DB}  |  **ORM:** {ORM}  |  **Model:** {DDD/ERD}  |  **Migration:** {tool}  |  **Scoping:** {row-level/schema/N/A}

## Schema Conventions
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| DB-SCHEMA-01 | Tables: {naming convention} |
| DB-SCHEMA-02 | Columns: {naming convention} |
| DB-SCHEMA-03 | PK: {id type} |
| DB-SCHEMA-04 | FK: {naming pattern} |
| DB-SCHEMA-05 | Timestamps: created_at, updated_at (UTC) on every table |
| ... | ... |

Standard columns (every table): id, tenant_id*, created_at, updated_at, created_by, updated_by, deleted_at*
<!-- end: AP-sourced -->

## Query Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| DB-QUERY-01 | All access via ORM |
| DB-QUERY-02 | Parameterized only |
| DB-QUERY-03 | {Tenant scoping rule} |
| DB-QUERY-04 | No SELECT * |
| DB-QUERY-05 | Always paginate |
| ... | ... |
<!-- end: AP-sourced -->

## Migration Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| DB-MIG-01 | Every change = versioned migration |
| DB-MIG-02 | {Forward-only / reversible} |
| ... | ... |
<!-- end: AP-sourced -->

## Index Strategy
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| DB-IDX-01 | Index all FKs |
| DB-IDX-02 | Index WHERE columns |
| ... | ... |
<!-- end: AP-sourced -->

## Caching Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| DB-CACHE-01 | {Cache technology} |
| DB-CACHE-02 | Cache-aside pattern |
| DB-CACHE-03 | Key format: {pattern} |
| ... | ... |
<!-- end: AP-sourced -->

## Soft Delete / Data Lifecycle
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| DB-DEL-01 | {Delete strategy} |
| DB-LIFE-01 | {Retention policy} |
| ... | ... |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/data-to-steering.md`.
