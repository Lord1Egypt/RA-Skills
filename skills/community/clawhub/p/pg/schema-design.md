# Schema Design — Types, Keys, Constraints

Type defaults (TIMESTAMPTZ, NUMERIC money, TEXT, IDENTITY) are Core Rules 6 in SKILL.md. This file is everything downstream of those defaults.

## Keys

- `GENERATED ALWAYS AS IDENTITY` (PostgreSQL >=10) over `SERIAL`: identity is standard SQL, owns its sequence properly, and cannot be overwritten by accident (`OVERRIDING SYSTEM VALUE` is required, which is exactly the audit trail you want).
- UUID: `gen_random_uuid()` is in core since PostgreSQL >=13 — the `uuid-ossp` extension is no longer needed. v4 is random and fragments every index it appears in; v7 is time-ordered and behaves like a bigint for locality. PostgreSQL >=18 has `uuidv7()` built in; below that, generate v7 in the application or from a small plpgsql function.
- Natural keys (email, slug) as the primary key propagate every rename into every child table. Keep a surrogate key and put a unique constraint on the natural one.
- Composite primary keys are correct for join tables (`(user_id, role_id)`) and correct for partitioned tables (the partition key must be part of every unique constraint). Elsewhere they complicate every ORM and FK.
- Sequences are not transactional: a rolled-back insert consumes the number. Gaps are normal and are not a bug; if the business needs gapless numbering, that is a separate counter table with its own locking, not a sequence.
- `int` overflows at 2.1 billion. On a table doing a million inserts a day, `int` is a five-year fuse; `bigint` costs 4 extra bytes. Migrating a live `int → bigint` primary key is a multi-day expand/contract exercise (procedure in the migrations guide).

## Constraints Are Cheaper Than Application Checks

- `NOT NULL` is the highest-value constraint in the database: it removes a branch from every consumer and lets the planner discard NULL handling.
- `CHECK` for invariants that are true forever (`amount >= 0`, `starts_at < ends_at`). Add on big tables as `NOT VALID` then `VALIDATE` (SKILL.md Safe DDL).
- Foreign keys: `ON DELETE RESTRICT` is the safe default; `CASCADE` on a table with millions of children is a locking event, not a convenience. FK columns need their own index (SKILL.md Core Rules 2) — the parent-side check takes `FOR KEY SHARE` row locks on the parent, which is the origin of most FK deadlocks.
- Deferrable constraints (`DEFERRABLE INITIALLY IMMEDIATE`, then `SET CONSTRAINTS ... DEFERRED`) let a transaction pass through a temporarily inconsistent state — the only clean way to swap two unique values.
- Exclusion constraints solve "no two bookings overlap in the same room" declaratively:
  ```sql
  CREATE EXTENSION btree_gist;
  ALTER TABLE bookings ADD CONSTRAINT no_overlap
    EXCLUDE USING gist (room_id WITH =, during WITH &&);
  ```
  Application-side overlap checks lose the race under concurrency; this one cannot.

## Uniqueness, NULLs, and Soft Deletes

- A unique constraint treats NULLs as distinct, so `UNIQUE (email)` allows unlimited NULL emails. `UNIQUE NULLS NOT DISTINCT` (PostgreSQL >=15) closes it.
- Soft delete plus uniqueness: `CREATE UNIQUE INDEX ON users (email) WHERE deleted_at IS NULL` — a plain unique constraint blocks recreating a deleted record forever.
- Case-insensitive uniqueness: `CREATE UNIQUE INDEX ON users (lower(email))`, or a `citext` column. The expression index is more portable and its behaviour is visible in the DDL; `citext` is convenient but its comparisons follow the database collation, which changes across OS upgrades.
- Soft delete costs every future query a `WHERE deleted_at IS NULL` that someone will forget. The alternative worth considering: move rows to a `<table>_archive` table in the same transaction. Choose per table, not per codebase.

## Time, Ranges, and Intervals

- `TIMESTAMPTZ` stores a UTC instant; the session `TimeZone` only affects rendering. When the *original* wall-clock zone matters (a recurring calendar event in Madrid), store the zone name in a second column — the instant alone cannot survive a DST rule change.
- `DATE` for birthdays and business dates: they are not instants and must not shift with a zone.
- `INTERVAL` for durations; do not store seconds in an integer and rebuild the unit in five different places.
- Range types (`tstzrange`, `daterange`, `int4range`) replace `start`/`end` column pairs and unlock `&&` overlap, `@>` containment, and exclusion constraints. Bounds are explicit: `'[)'` (default) is half-open and the only bound style that composes without off-by-one bugs.
- Multiranges (PostgreSQL >=14) represent "available except these gaps" in one value.

## Text, Enums, Arrays

- Enum: fast and compact, but values cannot be removed or reordered, and `ADD VALUE` could not run inside a transaction block before PostgreSQL 12. Use it for a truly closed set (`'left' | 'right'`); use a lookup table with an FK the moment product owns the list.
- Arrays are correct for a small, ordered, always-read-together list (tags on a post). They are wrong as a substitute for a join table: no FK, no per-element constraints, and rewriting one element rewrites the whole row. Index containment with GIN.
- `TEXT` has no length limit but a row-level one: values above ~2 kB are compressed and moved to TOAST transparently. A B-tree index entry, however, is capped at about a third of an 8 kB page — index `md5(long_text)` or a prefix, not the column (SKILL.md Error Codes, 54000).
- Collation determines sort order and `LIKE` behaviour. `COLLATE "C"` is byte order: faster, stable across OS upgrades, and the right choice for identifiers, codes, and slugs. Human-facing sorting wants ICU (`"en-US-x-icu"`), which is versioned and survives glibc changes.

## Normalization, Denormalization, Materialization

- Start normalized. A join between two indexed tables is a nested loop over a handful of pages, not a table scan.
- Counter caches (`posts.comment_count`) are the most common denormalization and the most common source of drift. If you keep one, maintain it in the same transaction with a trigger, never in application code across two connections.
- Materialized views are the honest form of denormalization: one refresh point, and `REFRESH MATERIALIZED VIEW CONCURRENTLY` keeps readers online (it requires a unique index on the view and is slower than the blocking form).
- Generated columns: `GENERATED ALWAYS AS (...) STORED` computes on write and is indexable — the right home for a `tsvector`, a normalized email, or a computed total. PostgreSQL >=18 also offers virtual (computed on read); virtual columns cannot be indexed.

## Schemas and Layout

- One database, several schemas beats several databases when the data is related: cross-schema queries are ordinary, cross-database queries need FDW.
- Since PostgreSQL 15 the `public` schema is no longer writable by every user — grants that "always worked" fail after an upgrade. Create per-domain schemas and grant explicitly rather than relying on `public`.
- Multi-tenancy: shared tables with a `tenant_id` column scale to thousands of tenants and one migration; schema-per-tenant multiplies every DDL by the tenant count and pushes the catalog into the tens of thousands of tables. Choose schema-per-tenant only when isolation is a contractual requirement.
- Keep the `tenant_id` first in composite indexes on tenant tables — it is the equality column in every query (SKILL.md Core Rules 3).
