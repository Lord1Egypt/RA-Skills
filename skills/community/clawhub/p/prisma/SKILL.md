---
name: Prisma
slug: prisma
version: 1.0.2
description: >-
  Designs Prisma schemas, writes type-safe queries, and fixes migrations, connection pools, and N+1 relation loads in Node and TypeScript. Use when editing schema.prisma, modeling relations, indexes, enums, JSON or Decimal columns, or choosing between db push, migrate dev and migrate deploy; when a migration drifts, fails, or would drop a column on rename, or a database needs baselining; on errors P2002, P2025, P2024, P2034 or P3009; when connections run out on Lambda, Vercel or behind PgBouncer; when queries are slow or include loads too much; on transaction timeouts, deadlocks and optimistic locking; when Decimal or BigInt break JSON.stringify; for $queryRaw and TypedSQL; when porting $use middleware to client extensions; when prisma generate fails in Docker, Alpine or CI; and for seeding and test isolation. Not for database-server tuning or hand-written SQL (pg, sql), or other ORMs.
homepage: https://clawic.com/skills/prisma
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🔺
    requires:
      bins:
      - npx
    os:
    - linux
    - darwin
    - win32
    displayName: Prisma
    configPaths:
    - ~/Clawic/data/prisma/
---

User preferences and memory live in `~/Clawic/data/prisma/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/prisma/` or `~/clawic/prisma/`), move it to `~/Clawic/data/prisma/`.

## When To Use

- Writing or reviewing `schema.prisma`: models, relations, referential actions, indexes, enums, JSON, money and time columns
- Getting a schema change into a database safely: `db push` vs `migrate dev` vs `migrate deploy`, renames, backfills, baselining, drift, failed migrations
- Writing Prisma Client queries: filters, pagination, nested writes, upserts, aggregation, and the raw escape hatch
- Diagnosing runtime failures by error code (P1xxx connectivity, P2xxx query, P3xxx migrate) or by symptom (slow, too many queries, pool exhausted, transaction timeout)
- Deploying Prisma: generate in CI and Docker, engine targets, serverless and edge, poolers, test databases
- Extending the client: soft delete, audit logs, tenant scoping, computed fields — and porting existing `$use` middleware
- Not for tuning the database server itself (`EXPLAIN` plans, vacuum, index internals) or hand-written SQL optimization — see Related Skills

## Quick Reference

| Situation | Play |
|---|---|
| Schema edited, database unchanged | Dev: `npx prisma migrate dev`; prod/CI: `migrate deploy`; throwaway prototype only: `db push` (→ Core Rules 1) |
| "Unknown argument" or a model missing on the client | Client is stale generated code — `npx prisma generate` (→ Core Rules 2) |
| Renaming a field or table with rows in it | Prisma diffs by name: rename = DROP + ADD. `@map` to keep the column, or hand-edit the SQL (→ Core Rules 3) |
| Existing database, no `prisma/migrations` folder | `db pull` to introspect, then baseline the first migration as applied (→ `migrations.md`) |
| "Drift detected" or `migrate dev` wants to reset prod-like data | Someone changed the DB out of band; diff before you accept anything (→ `migrations.md`) |
| P3009 — failed migration blocks every deploy | Fix the SQL by hand, then `migrate resolve --applied` or `--rolled-back` (→ `errors.md`) |
| P2002 unique constraint failed | Genuine duplicate or an upsert race — catch the code, retry once (→ `errors.md`) |
| P2025 record not found on update/delete | Row gone, or an extra `where` filter did not match — this is the optimistic-locking signal (→ `transactions.md`) |
| P2024 timed out fetching a new connection | Pool exhausted: long transactions, too many client instances, or a limit below concurrency (→ `connections.md`) |
| "Too many connections" on Lambda, Vercel or Next.js dev | One client per process behind a `globalThis` singleton, plus an external pooler (→ `connections.md`) |
| Query log shows hundreds of queries per request | Relation loads in a loop, not `include` — measure before rewriting (→ `performance.md`) |
| Relation is `undefined` at runtime | Prisma never loads relations implicitly; `include` or `select` it (→ `queries.md`) |
| List endpoint gets slower as the table grows | `take` missing, offset pagination, or `count()` scanning (→ `performance.md`) |
| Transaction times out at 5s or deadlocks under load | Shrink the body, raise `timeout` deliberately, retry P2034 (→ `transactions.md`) |
| Soft delete, audit trail, tenant scoping, computed fields | Client extensions (`$extends`), not middleware (→ `extensions.md`) |
| `include` result does not narrow in TypeScript | `GetPayload` / `validator` instead of hand-written interfaces (→ `typescript.md`) |
| `Do not know how to serialize a BigInt`, or Decimal arrives as an object | Prisma returns `BigInt` and `Decimal`, not numbers (→ `typescript.md`) |
| Query the schema cannot express (CTE, window, DISTINCT ON, upsert-heavy batch) | `$queryRaw` tagged template, or TypedSQL for typed results (→ `raw-sql.md`) |
| Deploy fails with "Query engine could not be located" | `prisma generate` missing from the build, or wrong `binaryTargets` for the image (→ `deployment.md`) |
| Tests interfere with each other or need a real database | Per-worker database or schema, rollback-per-test, deterministic seed (→ `testing.md`) |
| Works on PostgreSQL, breaks on MySQL, SQLite, or MongoDB | Provider capability gap, not a Prisma bug (→ `providers.md`) |
| Anything else | Turn on query logging and read the SQL Prisma actually sent, then run that SQL by hand: the answer is almost always in the gap between what you expressed and what was emitted (→ `performance.md`) |

Depth on demand, by phase:

- **Model** — `schema.md` relations, referential actions, keys, indexes, types, multi-tenancy · `providers.md` what PostgreSQL, MySQL, SQLite, SQL Server, MongoDB and PlanetScale each refuse to do
- **Change** — `migrations.md` push vs migrate, renames, baselining, drift, zero-downtime sequences · `testing.md` test databases, isolation, seeding, mocking · `deployment.md` generate in CI and Docker, engines, serverless, edge, monorepos
- **Query** — `queries.md` filters, nested writes, upsert, pagination, aggregation · `performance.md` relation loading, indexes, counts, logging, payload size · `transactions.md` batch vs interactive, isolation, retries, optimistic locking · `raw-sql.md` `$queryRaw`, TypedSQL, safe interpolation
- **Extend and type** — `extensions.md` `$extends` for soft delete, audit, RLS, computed fields · `typescript.md` generated types, payload types, JSON, Decimal, BigInt
- **Operate** — `connections.md` pool sizing, PgBouncer, serverless, `directUrl` · `errors.md` every P-code to cause and fix

## Core Rules

1. **One migration command per environment, and never the other one.** `db push` for a throwaway prototype (no history, silently drops columns to converge); `migrate dev` in development only (generates SQL, needs a shadow database, may reset); `migrate deploy` in CI and production (applies existing files, never generates, never resets). Check: grep the deploy pipeline — a `migrate dev` or a `db push` there is an incident waiting for its trigger.
2. **The client is generated code, not a schema reader.** Every schema edit needs `npx prisma generate`, and every install path needs it too (postinstall script plus an explicit step in the build). The signature failure: types compile locally, production throws "Unknown argument" or a model that exists in the schema is missing on the client, because a cached `node_modules` shipped a client generated from an older schema.
3. **Rename with `@map`, never by renaming the field.** Prisma diffs by name, so renaming `fullName` to `name` emits `DROP COLUMN` + `ADD COLUMN`: every row loses that value. Keep the column and rename only in Prisma (`name String @map("fullName")`), or hand-edit the generated migration to `ALTER TABLE ... RENAME COLUMN` before it is applied. Same rule for models (`@@map`).
4. **Index the foreign key yourself on PostgreSQL.** Prisma migrate creates indexes for `@id` and `@unique` only. MySQL auto-indexes FK columns; PostgreSQL does not — so `@@index([authorId])` is your job, and without it a `where: { authorId }` filter or a cascading parent delete scans the child table. Under `relationMode = "prisma"` (PlanetScale and friends) there are no FK constraints at all and the index is mandatory on every relation scalar.
5. **`include` costs one query per relation; loops cost one per row.** Queries = 1 + one per distinct relation at each nesting level: `findMany` with three includes is 4 round trips whether it returns 10 rows or 10,000. The N+1 you actually have comes from a loop or a GraphQL resolver — with one exception: `findUnique`/`findUniqueOrThrow` calls on the same model in the same event-loop tick are batched into a single `WHERE id IN (...)`. Nothing else batches.
6. **`undefined` means "ignore this filter", `null` means "match NULL".** `deleteMany({ where: { tenantId: undefined } })` is a full-table delete, and `findFirst({ where: { email: undefined } })` returns a stranger's row. Rule: never let a possibly-undefined variable reach a `where`. Validate first, or make the skip explicit with `Prisma.skip` under the `strictUndefinedChecks` preview (`prisma >=5.20`), which turns implicit `undefined` into an error.
7. **An interactive transaction holds a pooled connection for its entire body.** Defaults: `timeout` 5000 ms, `maxWait` 2000 ms. No HTTP calls, no queues, no user input inside it. Concurrency ceiling is the pool: with `connection_limit=5`, the sixth concurrent interactive transaction waits and then fails P2028 after `maxWait` (2 s by default) — the app looks "deadlocked" while the database is idle. Ordinary queries queueing for the same pool fail P2024 instead, at `pool_timeout` (10 s).
8. **Size the pool against the database, not against hope.** Prisma's default `connection_limit` is `num_physical_cpus * 2 + 1` per client instance. Budget: `connection_limit ≤ (max_connections − 3 reserved − other consumers) / expected instances`. PostgreSQL ships `max_connections = 100` with 3 reserved, so on a 4-core runtime (9 connections each) eleven instances ask for 99 against the 97 available, and the eleventh gets P1001. Serverless: 1-2 plus an external pooler (`connections.md`).
9. **Retry only the codes that are retryable.** P2034 (write conflict / deadlock) and P2024 (pool timeout) deserve a retry of the whole transaction with jitter, capped at 3 attempts; P2002 deserves exactly one retry when it came from an upsert race, and zero when the duplicate is real. Never retry P2003, P2025 or any P1012 — nothing about a second attempt changes them.

## Error Codes

Codes are stable across versions; message text is not. Match on `e.code` after narrowing with `e instanceof Prisma.PrismaClientKnownRequestError`. Full catalog with causes and fixes: `errors.md`.

| Code | Meaning | First move |
|---|---|---|
| P1001 | Can't reach database server | Host/port/SSL or network, not Prisma — test the same URL with a plain client |
| P1017 | Server has closed the connection | Idle timeout or a pooler killing sessions mid-flight (→ `connections.md`) |
| P2002 | Unique constraint failed | Read `meta.target` for the field, then decide: duplicate data or upsert race (rule 9) |
| P2003 | Foreign key constraint failed | Parent missing, or delete order wrong — check the referential action, not the query |
| P2025 | Record to update/delete not found | Row gone, or your extra `where` filter did not match (the optimistic-lock signal) |
| P2024 | Timed out fetching a new connection from the pool | Pool exhausted; default pool timeout is 10s (→ `connections.md`) |
| P2028 | Transaction API error | Usually a transaction used after commit, or `maxWait` exceeded |
| P2034 | Write conflict or deadlock | Expected under contention: retry the whole transaction (rule 9) |
| P3009 | Failed migration found in the history | Deploys stay blocked until `migrate resolve` records the decision |
| P3005 | Database schema is not empty | You need a baseline migration, not a first migration (→ `migrations.md`) |

## Relation Loading

- Nothing is loaded implicitly. A relation you did not `include` or `select` is `undefined` at runtime and absent from the type — which is why the type error and the runtime bug appear together.
- `include` returns the full scalar set of the relation; `select` inside `include` prunes it. On wide rows the difference is bytes over the wire per row, and it is the cheapest optimization in the list.
- `select` and `include` are mutually exclusive at the same level. Nest them instead: `include: { posts: { select: { id: true, title: true } } }`.
- Filtered relations (`include: { posts: { where: { published: true }, take: 5 } }`) push the filter into the relation query — do this instead of loading everything and filtering in JavaScript.
- Relation counts belong to the same round trip: `select: { _count: { select: { posts: true } } }`. A `posts.length` after loading every post is the same answer with the whole table in memory.
- Relation load strategy is selectable where supported (`relationLoadStrategy: "join" | "query"`, `prisma >=5.7` with the `relationJoins` preview on PostgreSQL and MySQL): `join` is one round trip with JSON aggregation, `query` is one query per relation with a smaller, simpler payload. Measure both on a real dataset — deep nesting favors `join` on a distant database, wide relations favor `query`. Details and current status: `performance.md`.

## Connection Budget

Formula, applied before touching any other performance knob:

```
total connections = client instances × connection_limit
must satisfy: total ≤ max_connections − reserved − other consumers
```

- Client instances are processes, not requests: one Node server = 1; a clustered server = 1 per worker; serverless = 1 per warm sandbox, and the count is set by your traffic, not by you.
- `connection_limit` is a URL parameter: `?connection_limit=10&pool_timeout=20`. Raising it does not create database capacity — it decides who queues where.
- Serverless without a pooler is the classic outage: every cold start opens its own pool and nothing gives them back. Use PgBouncer, a provider pooler, or Prisma Accelerate, and keep `connection_limit` at 1-2 (→ `connections.md`).
- Transaction-mode poolers require `?pgbouncer=true` (Prisma stops using named prepared statements) and a separate `directUrl` for migrations, which need a real session.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/prisma/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| provider | postgresql \| mysql \| sqlite \| sqlserver \| mongodb \| cockroachdb | postgresql | Selects every provider-gated answer: FK indexing, `mode: "insensitive"`, arrays, enums, JSON path syntax, `skipDuplicates` (→ `providers.md`) |
| prisma_major | number (5-6) | 6 | Which version-gated features are offered (`createManyAndReturn`, TypedSQL, `omit`, `Prisma.skip`) when the installed version is unknown |
| pooler | none \| pgbouncer \| supavisor \| provider-pooler \| accelerate | none | Whether URLs carry `pgbouncer=true`, whether `directUrl` is required, and the recommended `connection_limit` |
| deploy_target | node-server \| serverless \| edge \| docker | node-server | Drives the client-instantiation pattern, `binaryTargets`, `$disconnect` advice and generate placement (→ `deployment.md`) |
| migration_workflow | migrate \| push \| sql-first | migrate | Which command sequence is emitted for a schema change, and whether hand-written SQL files are the source of truth |
| id_style | cuid \| uuid \| uuidv7 \| autoincrement | cuid | The `@id` default in every generated model and example |
| naming_convention | camel-with-map \| db-native | camel-with-map | Whether generated models carry `@map`/`@@map` to snake_case database names or match the database verbatim |
| default_take | number (1-1000) | 50 | The pagination cap added to any `findMany` emitted without one (→ `performance.md`) |
| destructive_confirm | bool | true | `migrate reset`, `db push --accept-data-loss`, and `deleteMany`/`updateMany` without a `where` are emitted for review instead of run |

Preference areas — customizable dimensions; a stated preference is recorded in `config.yaml` and applied from then on:

- **Tooling** — package manager and runner, `prisma-client-js` vs the newer generator, validation library paired with Prisma (Zod, Valibot), seeding tool
- **Thresholds** — default page size, transaction `timeout` and `maxWait`, retry attempts and backoff, the query duration worth flagging in a review
- **Conventions** — model and field naming, singular vs plural tables, soft-delete field name, timestamp columns, enum vs lookup table, schema file layout (single file vs folder)
- **Platform** — provider and version, hosting target, region distance to the database (which decides how much round-trip count matters), monorepo layout and client output path
- **Risk posture** — whether migrations are applied directly or handed back as SQL for review, whether raw SQL is allowed at all, how strict the ban on `deleteMany` without `where` is
- **Output format** — schema plus explanation vs schema only, whether emitted queries carry the equivalent SQL in a comment, how much of the migration plan to narrate
- **Work order** — schema-first vs introspection-first, whether tests and seed data are updated in the same change as the migration
- **Integrations** — pooler and database host (Neon, Supabase, PlanetScale, RDS, Turso), Accelerate or a self-managed cache, observability stack for query logs
- **Restrictions** — tables Prisma must not manage (`@@ignore`), compliance rules that forbid raw SQL or require audit logging, columns that must never be selected by default
- **Cadence** — how often to re-run introspection against production, when to prune old migrations, review cycle for unused indexes

## Output Gates

Before emitting a schema, a migration, or a query:

- Every relation scalar indexed (`@@index`) unless the provider already indexes it, and every `relationMode = "prisma"` relation indexed without exception?
- Every rename expressed as `@map`/`@@map`, or the generated SQL hand-edited to a real `RENAME`?
- The destructive step (drop column, drop table) split into a later migration, after the code that stopped using it shipped?
- `onDelete`/`onUpdate` stated explicitly on every relation instead of inherited by default?
- Money as `Decimal @db.Decimal(12,2)`, timestamps as `DateTime @db.Timestamptz(3)` where the provider has it, never `Float` for money?
- Does every `findMany` have a `take`, and every `where` a value that cannot be `undefined`?
- Does the emitted command match the environment (`migrate deploy` in CI, never `migrate dev` or `db push`)?
- Is `prisma generate` guaranteed to run in this deployment path?

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `db push` on a database with real data | Converges by dropping whatever does not match, and leaves no history to deploy elsewhere | `migrate dev` locally, `migrate deploy` everywhere else (rule 1) |
| Building `where` from a request object | Any absent key becomes `undefined`, which Prisma reads as "no filter" | Validate into an explicit shape; `Prisma.skip` for deliberate skips (rule 6) |
| `new PrismaClient()` per request or per module | Each instance opens its own pool; the database hits its limit while the app looks idle | One instance per process, `globalThis` singleton in dev (→ `connections.md`) |
| `await` forgotten on a query | Prisma queries are lazy promises: nothing runs, no error, the value is a Promise | Lint with `no-floating-promises` — this is the one bug the type checker will not show you as a failure |
| `$transaction` wrapped around a single nested write | Nested writes are already one transaction; the wrapper only adds a held connection | Use the nested write alone (→ `transactions.md`) |
| Retrying an interactive transaction from inside itself | The transaction client is dead after the failure — P2028 on the retry | Retry the whole `$transaction` call from outside (rule 9) |
| Soft delete implemented in middleware or a `query` extension | Relation loads inside `include` do not pass through it: deleted children keep appearing | Explicit filters, or a database view — the honest limits are in `extensions.md` |
| `createMany` when you need the rows back | Returns a count only, and skips nested creates entirely | `createManyAndReturn` (`prisma >=5.14`, not on MySQL) or a transaction of creates |
| `count()` on a large table for a UI badge | It is a full scan every render, and it is on the request path | Cached count, approximate count, or `_count` scoped to a relation (→ `performance.md`) |
| String concatenation into `$queryRawUnsafe` | SQL injection with the word "unsafe" already in the call | Tagged `$queryRaw` with `Prisma.sql`/`Prisma.join` (→ `raw-sql.md`) |
| Raw SQL used for writes that other code reads through Prisma | Raw bypasses `@updatedAt`, `@default`, extensions and middleware; rows come back with stale metadata | Keep writes in the client, or set the columns yourself in the SQL |
| `@unique` on a nullable column as a "one per user" rule | SQL treats NULLs as distinct: unlimited NULL rows pass the constraint | Make it NOT NULL, or add a partial/filtered unique index in raw SQL |
| Enum values removed or reordered in a live schema | Rows holding the removed value break reads, and some engines cannot drop a value at all | Add-only enums, or a lookup table once the set churns (→ `schema.md`) |

## Where Experts Disagree

- **`cuid` vs `uuid` vs `bigint` primary keys.** Random v4 UUIDs fragment the B-tree and widen every secondary index; sequential integers leak volume and complicate multi-writer merges. Boundary: externally visible IDs → `cuid`/UUIDv7 (time-ordered, still opaque); internal high-write tables → `autoincrement()` bigint. Switch on measured index bloat, not on aesthetics.
- **Schema-first vs introspection-first.** Prisma's default is schema-first, and it is right when the application owns the database. When the database is shared with other systems, DBAs, or hand-written SQL, `db pull` plus baselined migrations avoids fighting for ownership — the boundary is who is allowed to change the schema, not which is more modern.
- **How much raw SQL is acceptable.** One camp keeps everything in the client for type safety and extension coverage; the other drops to `$queryRaw` at the first CTE or window function. Workable line: raw for read-only analytics and DDL-adjacent work, client for anything that writes rows other code reads back — because raw writes bypass `@updatedAt`, defaults, and every extension.
- **Prisma Migrate vs a plain SQL migration tool.** Migrate is excellent at diffing and terrible at expressing operations SQL has and Prisma does not (concurrent indexes, partitioning, triggers). Teams past a certain size run Prisma for the schema and hand-written SQL for the change; that is a legitimate configuration (`migration_workflow: sql-first`), not a defeat.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/prisma (install if the user confirms):
- `pg` — the PostgreSQL server underneath: plans, vacuum, locks, replication
- `sql` — hand-written SQL, cross-engine portability, index and query design
- `typescript` — type-system depth beyond Prisma's generated types
- `nodejs` — process lifecycle, memory, and shutdown around the client
- `nextjs` — where the client lives in App Router, server actions, and build-time generation

## Feedback

- If useful, star it: https://clawic.com/skills/prisma
- Latest version: https://clawic.com/skills/prisma

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/prisma.
