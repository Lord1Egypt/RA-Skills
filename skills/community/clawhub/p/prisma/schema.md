# Schema Design — Modeling Against What Prisma Can Express

The schema is a diff source, not documentation: everything here is read by `migrate` to compute SQL, and by `generate` to compute types. Design decisions that look cosmetic (a field name, a nullable flag) become DDL.

## Contents

- Relations and referential actions
- Keys and identifiers
- Indexes
- Types that bite
- Enums
- Naming and mapping
- Constructs Prisma cannot express
- Multi-tenancy
- Soft delete
- Schema layout

## Relations and Referential Actions

- Every relation needs a scalar field plus `@relation(fields: [...], references: [...])` on the owning side. The other side gets the array or the optional back-reference. Prisma refuses to generate without both halves.
- **Two relations between the same pair of models must be named** or `prisma validate` fails with an ambiguous-relation error (P1012): `author User @relation("AuthoredPosts", ...)` and `reviewer User @relation("ReviewedPosts", ...)`.
- Self-relations always need a name, including the manager/reports and parent/children shapes.
- Defaults you inherit if you say nothing:

| Relation | `onDelete` default | `onUpdate` default | Consequence |
|---|---|---|---|
| Required (`author User`) | `Restrict` | `Cascade` | Deleting a parent with children fails with P2003 — often the correct behavior, rarely the expected one |
| Optional (`author User?`) | `SetNull` | `Cascade` | Deleting a parent silently orphans children with a NULL FK |

State both actions explicitly on every relation. `Cascade` on delete is a loaded gun worth aiming deliberately: a cascade chain three models deep deletes rows nobody in the code path mentioned. `SetNull` on a required relation is a schema error, not a runtime one.

- **Implicit many-to-many** (`posts Post[]` / `tags Tag[]`) generates a hidden `_PostToTag` table with columns `A` and `B`. It works until you need a column on the relationship — and then there is no in-place upgrade, only a data migration.
- **Explicit many-to-many** is a real model with `@@id([postId, tagId])`. Default to explicit whenever the join could ever carry a timestamp, a role, an order, or a soft-delete flag. Retrofitting is the expensive direction.
- `relationMode = "prisma"` (PlanetScale and any engine without foreign keys) removes the constraints from the database and emulates the actions in extra client queries. Two consequences: writes made outside Prisma break integrity with no error, and every relation scalar needs `@@index` by hand.

## Keys and Identifiers

- `@id @default(cuid())` — collision-resistant, URL-safe, sortable enough for pagination tie-breaks, and it does not leak row counts. `uuid()` is v4 by default: random, and random primary keys fragment the index (`SKILL.md`, Where Experts Disagree). `@default(autoincrement())` is the cheapest key and the loudest leak.
- Compound primary key: `@@id([tenantId, id])`. The client then addresses the row with the generated compound key name: `where: { tenantId_id: { tenantId, id } }`.
- Compound unique: `@@unique([orgId, email])` → `where: { orgId_email: { orgId, email } }`. Rename that generated key with `name:`, and the database constraint with `map:` — two different arguments, and the error messages do not distinguish them for you.
- Database-side generation goes through `@default(dbgenerated("gen_random_uuid()"))`; Prisma then never computes the value, so a `create` returns it only because Prisma reads the row back.

## Indexes

- Prisma migrate indexes `@id` and `@unique` automatically and nothing else. Foreign keys are your job on PostgreSQL (`SKILL.md` rule 4).
- Composite order follows the leftmost-prefix rule: `@@index([tenantId, createdAt])` serves `where: { tenantId }`, `where: { tenantId, createdAt }`, and `orderBy: { createdAt }` scoped to a tenant. It does nothing for a query filtering `createdAt` alone. Reversing the pair makes the common query slower as the tenant gets smaller.
- PostgreSQL index types are expressible: `@@index([data], type: Gin)`, plus `Hash`, `Gist`, `Brin`, `SpGist`. Operator classes take the `ops:` argument.
- MySQL prefix length: `@@index([bio(length: 200)])` — required for indexing long text columns at all.
- Sort direction is expressible (`@@index([createdAt(sort: Desc)])`) and matters for keyset pagination on that column.
- Partial indexes, expression indexes and covering indexes have no schema syntax. Write them in raw SQL inside a migration — then read every subsequently generated migration, because the diff cannot see them and will happily propose a `DROP INDEX`.

## Types That Bite

| Column | Write it as | Why |
|---|---|---|
| Money | `Decimal @db.Decimal(12,2)` | `Float` is a double: 0.1 + 0.2 ≠ 0.3, and rounding drift shows up in reconciliation, not in tests. Reads come back as `Prisma.Decimal`, never a number (→ `typescript.md`) |
| Instant in time | `DateTime @db.Timestamptz(3)` on PostgreSQL | Plain `DateTime` maps to `timestamp(3)` without a zone; two servers in different zones then write incomparable values |
| Calendar date | `DateTime @db.Date` | Otherwise a birthday shifts by a day across a timezone boundary |
| Big counters, external IDs | `BigInt` | Reads come back as JS `BigInt`, which `JSON.stringify` throws on (→ `typescript.md`) |
| Semi-structured payload | `Json` | Typed as `JsonValue`; filtering syntax differs per provider (→ `providers.md`) |
| Binary | `Bytes` | `Buffer` on `prisma <6`, `Uint8Array` from `prisma >=6` — a silent break for code doing `.toString("base64")` |
| Free text | `String @db.Text` | The default `String` maps to `varchar(191)` on MySQL: silent truncation risk at 191 characters |

- Nullability is a modeling decision with two visible effects: the FK default action (table above) and the query surface (`null` matches, `undefined` skips — `SKILL.md` rule 6). Prefer NOT NULL with a real default over an optional field that "usually has a value".
- `@updatedAt` is set by Prisma Client on updates, not by the database. Raw SQL updates, database triggers and cascade writes leave it stale, and updating a child never touches the parent's timestamp — if the parent's freshness matters, write it explicitly in the same transaction.

## Enums

- Supported on PostgreSQL, MySQL, MongoDB and CockroachDB; not on SQLite or SQL Server, where the field becomes a plain string with no database-level check (→ `providers.md`).
- Adding a value is safe. Removing or reordering is not: existing rows holding the removed value fail to read, and PostgreSQL cannot drop an enum value at all without recreating the type. Treat enums as append-only.
- Switch to a lookup table with a foreign key as soon as the value set is edited by humans, needs a label or a sort order, or changes more than once a quarter.

## Naming and Mapping

- Convention that survives both worlds: PascalCase singular models, camelCase fields in Prisma; snake_case in the database via `@map`/`@@map`. Set it up on day one — retrofitting `@map` across a live schema is the rename problem (`SKILL.md` rule 3) applied to every column at once.
- `@@map("users")` renames the table without touching data; `@map("full_name")` does the same for a column. This is also the escape hatch for reserved words and for a database you do not own.
- Constraint and index names live in `map:`. Databases enforce global or per-table uniqueness on those names, and the generated defaults collide in schemas with many similar tables.

## Constructs Prisma Cannot Express

- Tables without a primary key, and columns with types Prisma has no mapping for, come back from introspection as `@@ignore` / `Unsupported("...")`. Ignored models are absent from the client entirely; `Unsupported` fields exist in the schema for migration purposes but cannot be read or written.
- Triggers, functions, materialized views, partitions, row-level security policies and CHECK constraints are all invisible to the schema. They belong in hand-written SQL inside migrations, and they survive only if you never let a generated migration drop them.
- Database views have a preview generator (`views`); until it is enabled they are best modeled as an ignored model plus `$queryRaw` (→ `raw-sql.md`).

## Multi-Tenancy

Three shapes, in ascending isolation and cost:

1. **Tenant column** — `tenantId` on every table, `@@index([tenantId, ...])` on every access path, scoping enforced in a client extension (→ `extensions.md`). Cheapest, and one missing `where` is a cross-tenant leak.
2. **Schema per tenant** — one schema, N schemas. With PostgreSQL this means a datasource URL carrying `?schema=` per client instance, and one connection pool per tenant unless you pool centrally; the `multiSchema` preview feature covers static multi-schema layouts, not tenant-per-schema fan-out.
3. **Database per tenant** — full isolation, one `PrismaClient` per tenant, and the connection budget (`SKILL.md`) multiplied by tenant count. Viable for tens of tenants, not thousands.

Whichever you pick, the scoping rule belongs in one place. Scattered `where: { tenantId }` clauses are audited by hope.

## Soft Delete

- Model it as `deletedAt DateTime?`, not `deleted Boolean` — the timestamp answers "when" and still filters as `{ deletedAt: null }`.
- Uniqueness breaks under soft delete: a `@unique` email blocks re-registration after deletion. Fix with a compound unique against a non-null discriminator, or a partial unique index in raw SQL (`WHERE deleted_at IS NULL`).
- Filtering cannot be fully automated: extensions and middleware do not reach relation loads inside `include` (→ `extensions.md`). Either accept explicit filters at every call site, or move the filtering into database views and read through them.

## Schema Layout

- One file is fine until it is not; the multi-file layout (`prismaSchemaFolder`, a `prisma/schema/` directory) splits by domain without changing semantics. Generators and datasource stay in one file.
- Set the generator `output` path explicitly. The historical default writes into `node_modules`, which monorepos, bundlers and Docker layer caches all resolve differently — an explicit output directory removes an entire class of "works on my machine" (→ `deployment.md`).
- `prisma format` normalizes and `prisma validate` catches ambiguous relations, missing back-references and invalid attributes before a migration is generated. Both are fast enough to be pre-commit hooks.
