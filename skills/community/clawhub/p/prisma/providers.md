# Providers — What Each Database Refuses To Do

Prisma's API is uniform; the databases underneath are not. Code that works on PostgreSQL and fails on MySQL is almost never a Prisma bug — it is a capability gap, and P2026 ("unsupported feature for this provider") is the polite version of it.

## Capability Matrix

| Capability | PostgreSQL | MySQL | SQLite | SQL Server | MongoDB |
|---|---|---|---|---|---|
| Scalar lists (`String[]`) | Yes | No | No | No | Yes |
| Native enum type | Yes | Yes | Stored as text, enforced by the client only | No enum type — plain string column | Yes |
| `mode: 'insensitive'` | Yes | Not needed: collation is case-insensitive by default | No | No | Yes |
| `createMany` `skipDuplicates` | Yes | Yes | Yes | No | No |
| `createManyAndReturn` | Yes | No | Yes | No | No |
| Transactional DDL (a failed migration rolls back) | Yes | No — partial application is normal | Yes | Partly | No migrations at all |
| Interactive transactions | Yes | Yes | Yes (single writer) | Yes | Replica set required (P2031) |
| `$queryRaw` | Yes | Yes | Yes | Yes | No — `$runCommandRaw` |
| JSON filtering | `path` as an array | `path` as a `$.a.b` string | Limited | Limited | Native |
| Prisma Migrate | Yes | Yes | Yes | Yes | No — `db push` only |

## PostgreSQL

- The reference provider: everything in this skill works, and the escape hatches (partial indexes, `DISTINCT ON`, `FOR UPDATE SKIP LOCKED`, full-text, trigram) are all reachable through raw SQL (→ `raw-sql.md`, and `pg` for the server side).
- Foreign key columns are **not** indexed automatically (`SKILL.md` rule 4).
- `?schema=` in the URL selects the search path — the isolation knob for per-tenant schemas and per-worker test databases (→ `testing.md`).
- Case-insensitive comparison via `mode: 'insensitive'` emits a predicate no plain B-tree serves; a functional index is required and is not expressible in the schema (→ `performance.md`).
- `COUNT(*)` in raw SQL returns `BigInt`. Cast to `int` in the query unless you enjoy serialization errors (→ `typescript.md`).

## MySQL and MariaDB

- Default `String` maps to `varchar(191)` — a legacy of index length limits under utf8mb4. Anything longer needs `@db.Text` or `@db.VarChar(n)`, or writes truncate or fail with P2000.
- DDL is not transactional: a migration that fails halfway leaves half of it applied. Recovery is the manual branch of the P3009 procedure (→ `migrations.md`).
- Foreign key columns are auto-indexed, so rule 4 costs you nothing here — and the schema still deserves the explicit `@@index` for portability.
- Case sensitivity is a collation property, not a query property: the same `contains` filter is case-insensitive here and case-sensitive on PostgreSQL. Test the behavior you rely on.
- Index prefix length for long text columns: `@@index([bio(length: 200)])`.

## SQLite

- One writer at a time. Concurrent writes surface as `SQLITE_BUSY`; WAL mode and a busy timeout raise the ceiling but do not remove it.
- No arrays, no native enums, weak type affinity. A schema that passes here can fail on the real provider — which is why SQLite is a poor stand-in for PostgreSQL in tests (→ `testing.md`).
- Legitimately excellent for local-first apps, CLI tools, and embedded use; Turso/libSQL brings the same engine over the network through a driver adapter (→ `deployment.md`).

## SQL Server

- No enum type: enum fields become strings with no database-level constraint. Model a lookup table if the values must be enforced.
- Supports `Snapshot` isolation in addition to the standard levels (→ `transactions.md`).
- `skipDuplicates` and `createManyAndReturn` are both unavailable; bulk work goes through `$transaction([...])` or raw SQL.

## MongoDB

- No migrations. `prisma db push` is the only way to sync, and it mostly creates indexes — the document shape is enforced by the client, not the database, so existing documents can violate the schema and only fail on read.
- Relations are references without foreign keys: no `onDelete`, no database-side integrity. Cascade behavior is emulated by the client, and only for writes going through Prisma.
- Transactions require a replica set; a standalone `mongod` returns P2031. Atlas and most managed deployments are replica sets by default.
- `_id` is mapped explicitly: `id String @id @default(auto()) @map("_id") @db.ObjectId`, and every relation scalar pointing at it needs `@db.ObjectId` too.
- Raw access is `$runCommandRaw` / `findRaw` / `aggregateRaw`, not SQL.

## CockroachDB

- Serializable isolation by default, so write conflicts (P2034) are a normal operating condition rather than an edge case: the retry loop is mandatory, not optional (→ `transactions.md`).
- Sequential integer keys create hotspots on a distributed cluster. Use UUIDs or the provider's own sequence types.

## Hosted PostgreSQL and MySQL Variants

| Platform | What changes |
|---|---|
| PlanetScale | Historically no foreign keys, requiring `relationMode = "prisma"` and manual indexes on every relation scalar; newer clusters support FKs — check yours before choosing. Schema changes go through branches and deploy requests, so `migrate deploy` may not be the delivery mechanism at all |
| Neon | Serverless Postgres that pauses when idle: first request after idling can return P1001/P1002. Pooled and direct URLs are separate endpoints — `directUrl` matters (→ `connections.md`) |
| Supabase | Supavisor in transaction mode: `?pgbouncer=true` on the app URL, direct URL for migrations, and session-scoped features unavailable |
| RDS / Cloud SQL | Standard engines; the constraint is usually `max_connections` on small instance classes and IAM/SSL details in the URL |
| Cloudflare D1 | SQLite semantics over HTTP via a driver adapter; no long-lived connections, so no interactive transactions in the usual sense |

## Writing for Portability

Only worth doing if you genuinely expect to switch engines — the cost is real:

- Avoid scalar lists, native enums and provider-specific `@db.` types; use a lookup table and `@db.Text`/`Decimal` primitives.
- Do case-insensitive matching by storing a normalized column (`emailLower`) rather than relying on `mode` or collation.
- Keep raw SQL behind a repository boundary so the dialect-specific parts sit in one file.
- Run the test suite against both engines in CI. Portability that is not exercised is portability that does not exist.
