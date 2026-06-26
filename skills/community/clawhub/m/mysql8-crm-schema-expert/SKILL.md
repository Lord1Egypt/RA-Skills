---
name: mysql8-design-crm
version: "1.0.0"
description: >
  MySQL 8 database schema design for CRM systems. Use this skill whenever the user needs to design,
  review, optimize, or generate database schemas for Customer Relationship Management systems.
  Triggers on: CRM database design, CRM schema, customer database, contact management database,
  sales pipeline database, lead tracking schema, opportunity management tables, CRM entity relationships,
  CRM data model, accounts/contacts/deals schema, activity tracking database, CRM audit trail,
  CRM custom fields, EAV pattern for CRM, CRM soft deletes, polymorphic relationships in CRM,
  sales funnel database, customer lifecycle database, CRM normalization, CRM indexing strategy,
  MySQL CRM tables, or any database design work involving customer relationship management concepts.
  Also trigger when the user mentions designing tables for contacts, accounts, opportunities, leads,
  deals, pipelines, activities, notes, tasks, campaigns, or any combination of these CRM entities.
---

# MySQL 8 CRM Database Design Skill

A comprehensive guide for designing production-quality MySQL 8 database schemas for CRM (Customer Relationship Management) systems. This skill covers everything from core entity design to advanced patterns like EAV custom fields, polymorphic activities, audit trails, and multi-tenant architectures.

## How to Use This Skill

This skill is organized into a main guide (this file) and detailed reference documents. Read the relevant reference file before generating any SQL or making design decisions.

### Reference Files

Read these from `references/` as needed:

| File | When to Read |
|------|-------------|
| `core-entities.md` | Designing the foundational CRM tables (accounts, contacts, leads, opportunities, etc.) |
| `relationships-and-normalization.md` | Establishing foreign keys, junction tables, and achieving proper normal forms |
| `indexing-and-performance.md` | Creating indexes, query optimization, partitioning, and performance tuning |
| `custom-fields-and-flexibility.md` | Implementing EAV patterns, JSON columns, or hybrid approaches for user-defined fields |
| `audit-and-soft-deletes.md` | Change tracking, audit trails, soft delete patterns, and compliance logging |
| `activities-and-timeline.md` | Polymorphic activity feeds, notes, tasks, emails, calls, and event tracking |
| `security-and-multitenancy.md` | Row-level security, role-based access, tenant isolation, and data privacy |
| `migrations-and-seeding.md` | Schema versioning, migration scripts, and realistic test data generation |
| `reference-schemas.md` | Complete example schemas you can use as starting points |

## Core Design Principles

When designing a CRM database on MySQL 8, always follow these principles:

1. **Relational integrity first.** Define FOREIGN KEY constraints at the database level. Never rely on application code alone to maintain referential integrity.

2. **Normalize to 3NF, then denormalize deliberately.** Start at Third Normal Form. Only denormalize when you have measured performance evidence, and document the reason.

3. **Consistent naming conventions.** Use `snake_case` for all identifiers. Table names are plural (`contacts`, `accounts`). Foreign keys follow the pattern `{singular_referenced_table}_id` (e.g., `account_id`). Timestamps are `created_at`, `updated_at`, `deleted_at`.

4. **Every table gets an audit baseline.** At minimum: `id` (BIGINT UNSIGNED AUTO_INCREMENT), `created_at`, `updated_at`. Most CRM tables also need `created_by` and `updated_by`.

5. **Soft deletes over hard deletes.** CRM data has legal, compliance, and historical reporting value. Use `deleted_at` (TIMESTAMP NULL) rather than DELETE statements.

6. **Use BIGINT UNSIGNED for primary keys.** INT runs out at ~2.1 billion. CRM tables like activities and audit logs grow fast. BIGINT UNSIGNED gives you headroom through 18.4 quintillion.

7. **UTF8MB4 everywhere.** Always `CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`. Customer names, notes, and communications contain international characters and emoji.

8. **InnoDB only.** All tables use InnoDB for transaction support, row-level locking, foreign key enforcement, and crash recovery.

9. **Timestamps use DATETIME(3) or TIMESTAMP.** For CRM, prefer `DATETIME(3)` for event times (timezone-independent, millisecond precision). Use `TIMESTAMP` for `created_at`/`updated_at` with `DEFAULT CURRENT_TIMESTAMP` and `ON UPDATE CURRENT_TIMESTAMP`.

10. **Design for integration.** CRM systems connect to email, marketing, billing, and support tools. Include `external_id` or `external_source` columns on entities that sync with third-party systems.

## Standard Table Template

Every CRM table should follow this baseline structure:

```sql
CREATE TABLE `table_name` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    -- entity-specific columns here --

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    `created_by` BIGINT UNSIGNED NULL DEFAULT NULL,
    `updated_by` BIGINT UNSIGNED NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_table_name_deleted_at` (`deleted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Workflow for Designing a CRM Schema

Follow this sequence when the user asks you to design a CRM database:

1. **Clarify scope.** Determine which CRM modules are needed: contacts/accounts, sales pipeline, marketing/campaigns, support/tickets, or all of the above.

2. **Read the relevant reference files.** Always start with `core-entities.md`. Add others based on the modules identified.

3. **Design entities first, relationships second.** List the tables and their columns, then define the foreign keys and junction tables.

4. **Apply indexing strategy.** Read `indexing-and-performance.md` and add indexes for every foreign key, every column used in WHERE/JOIN/ORDER BY, and composite indexes for common query patterns.

5. **Add flexibility layer.** If the user needs custom fields, read `custom-fields-and-flexibility.md` and choose between EAV, JSON columns, or a hybrid approach.

6. **Add audit and compliance.** Read `audit-and-soft-deletes.md` and implement the appropriate level of change tracking.

7. **Generate migration scripts.** Read `migrations-and-seeding.md` and output versioned, idempotent migration SQL.

8. **Review and validate.** Walk through the schema checking for: missing indexes on FKs, missing NOT NULL constraints, missing default values, orphan risk, and query patterns that would cause full table scans.

## MySQL 8 Features to Leverage

These MySQL 8 specific features are particularly valuable for CRM schemas:

- **JSON columns** for semi-structured data (custom fields, metadata, integration payloads). See `custom-fields-and-flexibility.md`.
- **Generated columns** (VIRTUAL or STORED) to extract and index JSON values.
- **Functional indexes** (8.0.13+) to index expressions without explicit generated columns.
- **Multi-valued indexes** (8.0.17+) to index JSON arrays efficiently.
- **Common Table Expressions (CTEs)** for recursive queries on hierarchical data (org charts, account hierarchies, nested categories).
- **Window functions** for pipeline analytics (running totals, rank, lead/lag).
- **CHECK constraints** for data validation at the database level.
- **DEFAULT expressions** for computed defaults.
- **Invisible indexes** for safe testing of index removal.
- **Descending indexes** for optimizing ORDER BY ... DESC queries.

## Quick Decision Guide

| Situation | Action |
|-----------|--------|
| User needs a full CRM from scratch | Read `core-entities.md` + `reference-schemas.md`, design all modules |
| User needs just contacts + accounts | Read `core-entities.md`, design the contact/account module only |
| User asks about custom fields | Read `custom-fields-and-flexibility.md` |
| User has performance concerns | Read `indexing-and-performance.md` |
| User needs GDPR/compliance support | Read `audit-and-soft-deletes.md` + `security-and-multitenancy.md` |
| User is building multi-tenant SaaS CRM | Read `security-and-multitenancy.md` |
| User wants to track all user activity | Read `activities-and-timeline.md` |
| User needs migration scripts | Read `migrations-and-seeding.md` |
| User wants a ready-to-use schema | Read `reference-schemas.md` |
