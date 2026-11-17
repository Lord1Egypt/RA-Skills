<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Data Architecture → database-rules.md

## Purpose

This mapping rule transforms the **Data Architecture & Schema** document (AP artifact) into a steering file that governs all database access, schema design, migrations, caching, and data lifecycle decisions.

**Output:** `rules/database-rules.md`

---

## MANDATORY: Stage Sub-Role — Security Architect

During THIS activity, ALSO adopt the mindset of a **Security Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think about data integrity holistically — schema conventions, query patterns, caching, and lifecycle are all surfaces for data corruption
- Enforce tenant scoping EVERYWHERE it matters — queries, cache keys, indexes, search filters — not just in one section
- Write ORM-first rules — the data access layer is the gatekeeper for scoping, soft-delete, and audit timestamps
- Treat migration discipline as production safety — bad migrations cause outages; write rules accordingly
- Cross-reference domain-context.md for table/column naming — database entities must match the ubiquitous language

### Anti-Patterns for This Activity
- Do NOT generate generic database advice — every rule must trace to the specific AP's technology and data model choices
- Do NOT separate caching rules from tenant isolation — a cache key without tenant_id is a security vulnerability
- Do NOT allow soft-delete to be an afterthought — it must be enforced at ORM level from day one

### Quality Check
A good output from this activity sounds like:
- "DB-QUERY-03: EVERY query MUST include `WHERE tenant_id = ?` — enforced by repository base class. Source: Data Architecture §Multi-Tenant Scoping."
- "DB-MIG-06: Destructive operations (drop column, drop table) require two-phase approach: deprecate in release N, remove in release N+1."

---

## Source (AP Artifact)

**Document:** Data Architecture (typically `07_Data_Architecture.md` or `design/data-architecture.md`)

**Sections to extract:**

| Section | Contains | What to Extract |
|---------|----------|----------------|
| Data Model Strategy | DDD aggregates, ERD, hybrid approach | Modeling approach rules |
| Schema Management | Migrations, versioning, tools | Migration rules |
| Multi-Tenant Data Scoping | How tenant_id is enforced | Tenant isolation rules |
| Core Domain Entities | Entity relationships, cardinality | Entity design rules |
| Structured Data (RDBMS) | Table conventions, indexes | Schema rules |
| Unstructured Data | Documents, attachments, storage | Blob/document rules |
| Cached Data | What, where, TTL strategy | Caching rules |
| Search Indexes | What's indexed, sync strategy | Search rules |
| Data Lifecycle | Retention, archival, backup | Lifecycle rules |
| Soft Delete Strategy | How deletions are handled | Delete pattern rules |

**Additional sources:**
- Technology Stack (database technology, ORM)
- Multi-Tenancy Architecture (if exists — isolation model details)
- Related ADRs (data modeling decisions)

**If Event Sourcing/CQRS extension active:**
- Event store design, projections, read models, snapshots

---

## Target: database-rules.md

### Role

Governs how developers interact with the database layer. Covers schema conventions, query patterns, migration discipline, caching strategy, and data integrity rules. This file prevents: incorrect schema patterns, missing tenant scoping, cache inconsistencies, and data lifecycle violations.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Data Architecture | date: {generation-date} -->

# Database Rules

## Data Layer Identity

**Primary database:** {from AP — e.g., PostgreSQL 16}
**ORM / Data access:** {from AP — e.g., Prisma / TypeORM / Drizzle / raw SQL}
**Modeling approach:** {from AP — e.g., DDD Aggregates / Traditional ERD / Hybrid}
**Migration tool:** {from AP — e.g., Prisma Migrate / Flyway / Liquibase / custom}
**Multi-tenant scoping:** {from AP — e.g., row-level (tenant_id column) / schema-per-tenant / N/A}

---

## Schema Conventions

<!-- begin: AP-sourced -->

### Table Naming

| Rule | Standard |
|------|----------|
| DB-SCHEMA-01 | Table names: {from AP — e.g., plural snake_case: `incidents`, `service_requests`, `change_records`} |
| DB-SCHEMA-02 | Join tables: `{table_a}_{table_b}` alphabetically: `role_permissions` not `permission_roles` |
| DB-SCHEMA-03 | Tables MUST match domain entity names from domain-context.md — no synonyms |

### Column Naming

| Rule | Standard |
|------|----------|
| DB-SCHEMA-04 | Column names: {from AP — e.g., snake_case: `created_at`, `tenant_id`, `assigned_to`} |
| DB-SCHEMA-05 | Primary key: {from AP — e.g., `id` (UUID v4) on every table} |
| DB-SCHEMA-06 | Foreign keys: `{referenced_table_singular}_id`: `user_id`, `incident_id` |
| DB-SCHEMA-07 | Timestamps: EVERY table MUST have `created_at` and `updated_at` (UTC, auto-managed) |
| DB-SCHEMA-08 | Boolean columns: prefix with `is_` or `has_`: `is_active`, `has_attachment` |
| DB-SCHEMA-09 | Enum columns: {from AP — e.g., store as string/text, not integer — readability over performance} |
| DB-SCHEMA-10 | JSON columns: use ONLY when schema is genuinely dynamic — NEVER for structured data that could be normalized |

### Standard Columns (Every Table)

| Column | Type | Purpose |
|--------|------|---------|
| `id` | {from AP — UUID/ULID/bigint} | Primary key |
| `tenant_id` | UUID | Tenant scoping (if multi-tenant) |
| `created_at` | timestamp(tz) | Creation time (UTC) |
| `updated_at` | timestamp(tz) | Last modification (UTC) |
| `created_by` | UUID (FK → users) | Audit: who created |
| `updated_by` | UUID (FK → users) | Audit: who last modified |
| `deleted_at` | timestamp(tz) nullable | Soft delete marker (if applicable) |

<!-- end: AP-sourced -->

---

## Query Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| DB-QUERY-01 | ALL database access MUST go through the ORM/data access layer — no direct SQL in controllers or services |
| DB-QUERY-02 | Parameterized queries ONLY — NEVER concatenate user input into queries (SQL injection prevention) |
| DB-QUERY-03 | {Tenant scoping rule from AP — e.g., EVERY query MUST include `WHERE tenant_id = ?` — enforced by repository base class} |
| DB-QUERY-04 | SELECT only needed columns — no `SELECT *` in production code |
| DB-QUERY-05 | Always paginate list queries — no unbounded result sets (max: {from AP — e.g., 1000 rows}) |
| DB-QUERY-06 | N+1 queries: MUST use eager loading / joins for known relationships — never query in a loop |
| DB-QUERY-07 | Transactions: use for multi-table writes that must be atomic — {scope from AP — e.g., within one aggregate boundary} |
| DB-QUERY-08 | Read replicas: {from AP — e.g., use for reporting queries / read-heavy endpoints / N/A} |
| DB-QUERY-09 | Connection pooling: {from AP — e.g., configured at infrastructure level, max {n} connections per service instance} |

<!-- end: AP-sourced -->

---

## Migration Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| DB-MIG-01 | Every schema change MUST be a versioned migration — no manual DDL in production |
| DB-MIG-02 | Migrations are forward-only: {from AP — e.g., no rollback migrations / rollback supported but tested} |
| DB-MIG-03 | Migration naming: {from AP — e.g., `{timestamp}_{description}.sql` or auto-generated by ORM} |
| DB-MIG-04 | Migration review: every migration MUST be reviewed before merge — check for data loss, locks, performance |
| DB-MIG-05 | Zero-downtime migrations: {from AP — e.g., required / not required (maintenance window available)} |
| DB-MIG-06 | Destructive operations (drop column, drop table): {from AP — e.g., two-phase: deprecate → remove in next release} |
| DB-MIG-07 | Seed data: separate from schema migrations — use seed files for reference data |
| DB-MIG-08 | Migration testing: run against a copy of production schema size before applying |

<!-- end: AP-sourced -->

---

## Index Strategy

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| DB-IDX-01 | Index all foreign key columns |
| DB-IDX-02 | Index all columns used in WHERE clauses of common queries |
| DB-IDX-03 | Index all columns used in ORDER BY for paginated lists |
| DB-IDX-04 | Composite indexes: most selective column first |
| DB-IDX-05 | {Tenant-specific from AP — e.g., Include `tenant_id` as first column in composite indexes (partition-friendly)} |
| DB-IDX-06 | NEVER create indexes speculatively — add when query performance requires it (measure first) |
| DB-IDX-07 | Unique constraints: enforce at DB level (not just application) for business uniqueness rules |

<!-- end: AP-sourced -->

---

## Caching Rules

<!-- begin: AP-sourced -->

{Include if AP defines a caching strategy — otherwise minimal section}

| Rule | Standard |
|------|----------|
| DB-CACHE-01 | Cache technology: {from AP — e.g., Redis} |
| DB-CACHE-02 | Cache-aside pattern: application reads cache first, falls back to DB, writes to cache on miss |
| DB-CACHE-03 | Cache key format: {from AP — e.g., `{tenant_id}:{entity}:{id}` or `{tenant_id}:{entity}:list:{hash}`} |
| DB-CACHE-04 | TTL defaults: {from AP — e.g., entity: 5 min, list: 1 min, config: 30 min} |
| DB-CACHE-05 | Cache invalidation: invalidate on write — {strategy from AP — e.g., delete key on update/delete} |
| DB-CACHE-06 | NEVER cache sensitive data (tokens, passwords, PII) unless explicitly encrypted |
| DB-CACHE-07 | Cache keys MUST include tenant_id — NEVER serve cached data across tenants |
| DB-CACHE-08 | Cache failure is non-fatal — degrade to DB read, never error to user |

<!-- end: AP-sourced -->

---

## Search Rules

<!-- begin: AP-sourced -->

{Include if AP defines a search engine — otherwise omit section}

| Rule | Standard |
|------|----------|
| DB-SEARCH-01 | Search engine: {from AP — e.g., Elasticsearch 8.x} |
| DB-SEARCH-02 | Sync strategy: {from AP — e.g., async event-driven (DB write → event → index update)} |
| DB-SEARCH-03 | Search is eventually consistent — NEVER read from search index for authoritative data |
| DB-SEARCH-04 | Index schema: {from AP — e.g., one index per entity type, tenant-scoped via filter} |
| DB-SEARCH-05 | Reindex capability: MUST be able to rebuild any index from DB source without downtime |
| DB-SEARCH-06 | Search results: return IDs only → load full entities from primary DB (authoritative source) |

<!-- end: AP-sourced -->

---

## Soft Delete Rules

<!-- begin: AP-sourced -->

{Include if AP specifies soft delete — otherwise "hard delete with audit log" section}

| Rule | Standard |
|------|----------|
| DB-DEL-01 | Delete strategy: {from AP — e.g., soft delete (set `deleted_at` timestamp)} |
| DB-DEL-02 | ALL queries MUST filter `WHERE deleted_at IS NULL` by default (enforced by {mechanism from AP — e.g., ORM global filter}) |
| DB-DEL-03 | Hard delete: {from AP — e.g., only after retention period expires (scheduled job)} |
| DB-DEL-04 | Cascading: when parent soft-deleted, {from AP — e.g., children also soft-deleted / children remain accessible} |
| DB-DEL-05 | Restore capability: {from AP — e.g., clear `deleted_at` within retention period} |
| DB-DEL-06 | Unique constraints: {from AP — e.g., exclude soft-deleted records from uniqueness checks (partial index)} |

<!-- end: AP-sourced -->

---

## Data Lifecycle

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| DB-LIFE-01 | Retention policy: {from AP — e.g., operational data: indefinite / audit logs: 2 years / temp data: 30 days} |
| DB-LIFE-02 | Archival: {from AP — e.g., move records older than {period} to archive table / cold storage} |
| DB-LIFE-03 | Backup strategy: {from AP — e.g., daily full + hourly incremental, retained for 30 days} |
| DB-LIFE-04 | Point-in-time recovery: {from AP — e.g., WAL-based, up to last 7 days} |
| DB-LIFE-05 | Data deletion (GDPR/compliance): {from AP — e.g., tenant data fully purgeable within 30 days of request} |

<!-- end: AP-sourced -->

---

## Aggregate Boundaries (If DDD)

<!-- begin: AP-sourced -->

{Include if AP uses DDD aggregates OR DDD Tactical extension was active}

| Rule | Standard |
|------|----------|
| DB-AGG-01 | One transaction = one aggregate — NEVER modify multiple aggregates in a single transaction |
| DB-AGG-02 | Aggregate root is the only entry point — child entities accessed ONLY through root |
| DB-AGG-03 | References between aggregates: by ID only — NEVER direct object reference |
| DB-AGG-04 | Aggregate size: keep small — if an aggregate loads >50 rows regularly, reconsider boundaries |
| DB-AGG-05 | Eventual consistency between aggregates: use domain events, not distributed transactions |

<!-- end: AP-sourced -->

---

## Event Sourcing Rules (If Extension Active)

<!-- begin: AP-sourced -->

{Include ONLY if Event Sourcing/CQRS extension was active in AI-ADLC}

| Rule | Standard |
|------|----------|
| DB-ES-01 | Event store: append-only — NEVER modify or delete events |
| DB-ES-02 | Event schema: {from AP — e.g., id, stream_id, event_type, version, payload (JSON), timestamp, metadata} |
| DB-ES-03 | Read models: derived from events via projections — NOT from direct event store queries |
| DB-ES-04 | Projection rebuild: MUST be possible to rebuild any read model from event stream |
| DB-ES-05 | Snapshots: create at every {n from AP — e.g., 100} events per stream for performance |
| DB-ES-06 | Event versioning: {from AP — e.g., upcasting strategy for schema evolution} |
| DB-ES-07 | CQRS separation: write side (commands → events) and read side (projections) use separate models |

NOTE: Full event sourcing rules are in `rules/event-sourcing.md` (conditional file).

<!-- end: AP-sourced -->

---

## Anti-Patterns (NEVER DO)

1. **NEVER** bypass the ORM for "quick" raw queries — consistency and scoping depend on the data layer
2. **NEVER** store computed/derived data that can be calculated from source — exception: read performance (document the reason)
3. **NEVER** use the database as a message queue (polling tables for state changes)
4. **NEVER** create circular foreign key relationships
5. **NEVER** store large binary data in the primary database — use object storage with DB reference
6. **NEVER** query across tenants without explicit platform-admin authorization
7. **NEVER** apply migrations without reviewing for locking behavior on large tables
8. **NEVER** trust application-only uniqueness — enforce at DB level with constraints
```

---

## Transformation Rules

| AP Content | Transformation | Output |
|-----------|---------------|--------|
| Data model strategy (DDD/ERD) | Set Data Layer Identity + determine if aggregate rules apply | Header + conditional DB-AGG section |
| Table/column naming conventions | Convert to DB-SCHEMA-NN rules | Schema Conventions |
| Multi-tenant scoping method | Convert to DB-QUERY-03 + DB-CACHE-07 + DB-IDX-05 | Embedded across sections |
| Migration approach + tooling | Convert to DB-MIG-NN rules | Migration Rules |
| Caching strategy (what, TTL, invalidation) | Convert to DB-CACHE-NN rules | Caching Rules |
| Search engine + sync strategy | Convert to DB-SEARCH-NN rules | Search Rules |
| Soft delete pattern | Convert to DB-DEL-NN rules | Soft Delete Rules |
| Retention/archival policy | Convert to DB-LIFE-NN rules | Data Lifecycle |
| DDD aggregate boundaries | Convert to DB-AGG-NN rules | Aggregate Boundaries |
| Event sourcing design | Convert to DB-ES-NN rules | Event Sourcing (conditional) |

### Numbering Convention

| Prefix | Domain |
|--------|--------|
| DB-SCHEMA-NN | Schema design |
| DB-QUERY-NN | Query patterns |
| DB-MIG-NN | Migrations |
| DB-IDX-NN | Indexing |
| DB-CACHE-NN | Caching |
| DB-SEARCH-NN | Search |
| DB-DEL-NN | Deletion patterns |
| DB-LIFE-NN | Data lifecycle |
| DB-AGG-NN | Aggregate rules (DDD) |
| DB-ES-NN | Event sourcing (extension) |

---

## Key Rules for This Mapping

1. **Tenant scoping is embedded EVERYWHERE** — queries, cache keys, indexes, search filters. Not isolated to one section.
2. **Technology-specific conventions** — if AP says Prisma, rules reference Prisma patterns. If TypeORM, different patterns.
3. **ORM is the gatekeeper** — all access through ORM enforces scoping, soft-delete filters, and audit timestamps.
4. **Standard columns are non-negotiable** — every table gets id, timestamps, audit fields. No exceptions.
5. **Cache rules include tenant isolation** — cross-tenant cache poisoning is a security vulnerability.
6. **Migration discipline is strict** — no manual DDL, no unreviewed migrations, no destructive changes without two-phase approach.
7. **Cross-reference domain-context.md** — table names MUST match domain entity names from ubiquitous language.

---

## Depth Adaptation

| Depth | database-rules.md |
|-------|-------------------|
| **Minimal** | Schema conventions + query rules + migration basics (~20 rules) |
| **Standard** | Full structure as defined above — all sections (~40-50 rules) |
| **Comprehensive** | Full structure + index optimization guide + query performance patterns + data modeling examples per entity + partition strategy (if large scale) |

---

## Reconciliation Behavior

| Change | Impact | Action |
|--------|--------|--------|
| Database technology changed | Entire file affected (conventions differ per DB) | Regenerate; flag HIGH IMPACT |
| ORM changed | Query rules, migration rules affected | Update relevant sections |
| Caching strategy added/changed | DB-CACHE section update | Add/update caching rules |
| Search engine added/removed | DB-SEARCH section add/remove | Add or flag for removal |
| Tenant isolation model changed | Scoping rules across all sections | Update; flag HIGH IMPACT — review all sections |
| New entity added | No direct change (schema follows conventions) | No update needed (rules are generic) |
| Soft delete → hard delete decision | DB-DEL section rewrite | Rewrite section; flag for team awareness |
| Event sourcing extension activated | DB-ES section added | Add section; cross-reference event-sourcing.md |
