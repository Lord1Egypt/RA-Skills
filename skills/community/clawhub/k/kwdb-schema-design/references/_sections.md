---
title: Section Definitions
tier: 1
tags: [sections, categories, tier-definitions, organization]
---

# Section Definitions

This file defines the tier categories for KWDB schema design references.

Files are automatically assigned to tiers based on their content and expected read frequency.

---

## Tier 1: Core (Always Read)

**Read Frequency:** Always
**Content:** Decision framework, scope, examples, contribution guidelines

| File | Description |
|------|-------------|
| key-rules.md | Decision tree, core rules (workload classification, types, PK, index) |
| disambiguation.md | Clarifying questions to ask before DDL |
| _scope.md | Skill boundaries: IN scope vs OUT of scope |
| _examples.md | Complete dialogue examples for all workload types |
| _contributing.md | How to add or update reference files |
| _sections.md | This file: tier definitions |

---

## Tier 2: High-Frequency DDL

**Read Frequency:** When designing tables, indexes, constraints, or choosing types
**Content:** DDL syntax and best practices for most common operations

| File | Description | Key Topics |
|------|-------------|------------|
| table-ddl-ref.md | CREATE/ALTER/DROP TABLE | Relational tables, time-series tables, TAGS, RETENTIONS |
| index-ddl-ref.md | CREATE/DROP INDEX | Composite, covering, tag index, column order |
| constraint-ref.md | Constraints | PK, FK, UNIQUE, CHECK, CASCADE |
| type-ref.md | Data types | INT4/8, DECIMAL, FLOAT, VARCHAR, JSONB, UUID, TIMESTAMPTZ |

---

## Tier 3: Medium-Frequency DDL

**Read Frequency:** When explicitly needed
**Content:** Less common DDL operations

| File | Description | Key Topics |
|------|-------------|------------|
| view-ref.md | Views | VIEW, MATERIALIZED VIEW, REFRESH |
| sequence-ref.md | Sequences | unique_rowid(), gen_random_uuid(), SERIAL |
| partitioning-ref.md | Partitioning | LIST, RANGE, HASH, HASHPOINT |
| retention-ref.md | Retention | RETENTIONS syntax, time units, storage estimation |

---

## Tier 4: Low-Frequency DDL

**Read Frequency:** Only when explicitly requested
**Content:** Rarely used operations

| File | Description | Key Topics |
|------|-------------|------------|
| trigger-ref.md | Triggers | BEFORE/AFTER, row-level, audit logging |
| procedure-ref.md | Procedures | Functions, stored procedures, plpgsql |
| database-ref.md | Database ops | CREATE DATABASE, SCHEMA, multi-tenant |
| privilege-ref.md | Privileges | Users, roles, GRANT, REVOKE |

---

## Tier Assignment Rules

When adding a new reference file, assign tier based on:

| Tier | Criteria |
|------|----------|
| 1 | Must-read for every request (rules, scope, examples) |
| 2 | Needed for most schema design tasks (tables, indexes, types) |
| 3 | Needed for specific features (views, partitioning, retention) |
| 4 | Only when user explicitly asks (triggers, procedures, DBA tasks) |

---

## Reference Architecture

```
User Request
    │
    ├─ Tier 1 (Always Read)
    │   ├─ key-rules.md → Classify workload type
    │   ├─ disambiguation.md → Ask clarifying questions
    │   └─ _scope.md → Verify request is IN scope
    │
    ├─ Tier 2 (Based on classification)
    │   ├─ table-ddl-ref.md → Generate TABLE DDL
    │   ├─ type-ref.md → Choose column types
    │   ├─ constraint-ref.md → Add constraints
    │   └─ index-ddl-ref.md → Design indexes
    │
    ├─ Tier 3 (If features requested)
    │   ├─ view-ref.md → If user asks about views
    │   ├─ sequence-ref.md → If user asks about IDs
    │   ├─ partitioning-ref.md → If user asks about partitions
    │   └─ retention-ref.md → If time-series with retention
    │
    └─ Tier 4 (Only if explicitly asked)
        ├─ trigger-ref.md → If user mentions triggers
        ├─ procedure-ref.md → If user asks about procedures
        ├─ database-ref.md → If user asks about DB creation
        └─ privilege-ref.md → If user asks about permissions
```
