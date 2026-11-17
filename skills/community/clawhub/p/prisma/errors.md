# Errors — Every Code to a Cause and a Fix

Codes are stable across versions; message text is not. Match on `code`, never on the message string.

## Contents

- Catching and narrowing
- HTTP mapping
- P1xxx — connection and startup
- P2xxx — query
- P3xxx — migrate
- Errors with no code
- Logging errors usefully

## Catching and Narrowing

```ts
import { Prisma } from '@prisma/client'

try {
  await prisma.user.create({ data })
} catch (e) {
  if (e instanceof Prisma.PrismaClientKnownRequestError) {
    if (e.code === 'P2002') return conflict(e.meta?.target)   // string[] of field names
    if (e.code === 'P2025') return notFound()
  }
  if (e instanceof Prisma.PrismaClientValidationError) return badRequest()  // no code — a shape error
  throw e
}
```

| Class | Has `code` | Means |
|---|---|---|
| `PrismaClientKnownRequestError` | Yes | The engine understood and refused: everything in the tables below |
| `PrismaClientValidationError` | No | The arguments do not match the schema — a bug in your call, caught before SQL |
| `PrismaClientInitializationError` | Sometimes (`errorCode`) | Startup: bad URL, missing env var, engine binary not found (→ `deployment.md`) |
| `PrismaClientUnknownRequestError` | No | The database returned something unmapped — read `message`, then check the database log |
| `PrismaClientRustPanicError` | No | Engine crash: the client is unusable, restart the process, and it is worth reporting |

`e.meta` carries the useful part: `target` (the constraint's fields for P2002), `field_name` (P2003), `cause` (P2025), `modelName`. Log `code` + `meta`, not the whole error object — messages can contain parameter values.

## HTTP Mapping

| Code | Status | Body |
|---|---|---|
| P2002 | 409 | Which field collided, from `meta.target` |
| P2025 | 404 (or 409 for optimistic locking) | Never echo the internal cause text |
| P2003 | 409 on delete, 400 on create | The relation is the user's problem only on create |
| P2000, P2006, P2007, P2020, P2033 | 400 | Value invalid or out of range |
| `PrismaClientValidationError` | 500 | It is your bug, not the caller's — unless the caller supplied a filter shape |
| P2024, P1001, P1002, P1017 | 503 | Infrastructure; retryable at the edge |

## P1xxx — Connection and Startup

| Code | Meaning | First move |
|---|---|---|
| P1000 | Authentication failed | Credentials or a rotated password; URL-encode special characters in the password |
| P1001 | Can't reach database server | Host, port, firewall, SSL — or a serverless database that paused while idle (→ `connections.md`) |
| P1002 | Reached but timed out | Raise `connect_timeout`; a cold managed instance can exceed the 5s default |
| P1003 | Database does not exist | Wrong database name in the URL, or it was never created |
| P1008 | Operations timed out | `socket_timeout` or a genuinely long statement |
| P1010 | User denied access | Grants; commonly the app user lacking DDL rights for a migration |
| P1011 | TLS connection error | `sslmode` mismatch or a certificate the host does not trust |
| P1012 | Schema validation error | The schema itself: ambiguous relations, missing back-reference, or an env var absent at generate time |
| P1013 | Invalid connection string | Usually an unescaped `@`, `#` or `/` in the password |
| P1017 | Server closed the connection | Pooler/database idle timeout, a failover, or an OOM kill on the database side |

## P2xxx — Query

| Code | Meaning | First move |
|---|---|---|
| P2000 | Value too long for the column | Column length (`varchar(191)` on MySQL by default) vs actual input (→ `schema.md`) |
| P2002 | Unique constraint failed | `meta.target` names the fields. Real duplicate → 409. Upsert or `connectOrCreate` race → retry once |
| P2003 | Foreign key constraint failed | On create: the parent does not exist. On delete: a `Restrict` action, usually inherited by default |
| P2004 | A database constraint failed | A CHECK or trigger Prisma does not model — read the database error in `meta` |
| P2005 / P2023 | Stored value invalid for the field type | Schema drifted from the data: an enum value or column type changed out of band |
| P2010 | Raw query failed | The SQL is wrong or the parameters are; `meta.message` carries the engine's text (→ `raw-sql.md`) |
| P2011 | Null constraint violation | A required column got `undefined`, which is not the same as a default |
| P2012 / P2013 | Missing required value / argument | Client call shape; usually an optional TypeScript field feeding a required column |
| P2014 | Change would violate a required relation | Deleting or disconnecting a parent whose child requires it — change the action or delete the child first |
| P2015 / P2018 | Related record(s) not found | A `connect` to a row that does not exist, inside a nested write |
| P2017 | Records not connected | An `update` on a nested relation that is not linked to this parent |
| P2020 | Value out of range | Integer overflow: `Int` maxes at 2,147,483,647 — the column wants `BigInt` |
| P2021 / P2022 | Table / column does not exist | The migration never ran here, or the client was generated from a newer schema (`SKILL.md` rules 1-2) |
| P2024 | Timed out fetching a connection from the pool | Pool exhausted (→ `connections.md`, triage list) |
| P2025 | Depends on records that were not found | Row gone, or an extra `where` filter did not match — the optimistic-lock signal (→ `transactions.md`) |
| P2026 | Feature unsupported by this provider | A capability gap, not a bug (→ `providers.md`) |
| P2028 | Transaction API error | Transaction used after it ended, or `maxWait` exceeded |
| P2030 | No full-text index found | The `search` operator needs a database index Prisma cannot create for you |
| P2031 | MongoDB needs a replica set | Transactions on a standalone deployment |
| P2033 | Number out of 64-bit integer range | Pass a JS `BigInt`, not a `number` |
| P2034 | Write conflict or deadlock | Retry the whole transaction with jitter, cap 3 (`SKILL.md` rule 9) |

## P3xxx — Migrate

| Code | Meaning | First move |
|---|---|---|
| P3005 | Database schema is not empty | Baseline it (→ `migrations.md`) |
| P3006 | Migration fails on the shadow database | History is not replayable from zero — usually an applied migration was edited afterwards |
| P3009 | Failed migration found; deploys blocked | `migrate status`, decide applied vs rolled back, then `migrate resolve` |
| P3014 / P3020 | Shadow database could not be created | Missing CREATE DATABASE rights; set `shadowDatabaseUrl` to a second empty database |
| P3018 | A migration failed to apply | Read the SQL error inside the message; recovery is the P3009 procedure |
| P3019 | Datasource provider does not match the lock file | Someone switched providers; a provider change means a new migration history |
| P3008 | Migration already recorded as applied | Usually a double `migrate resolve` — check `_prisma_migrations` before doing more |
| P3001 | Destructive changes detected | The diff wants to drop something; nearly always an unintended rename (`SKILL.md` rule 3) |

P4001/P4002 come from introspection: an empty or inconsistent database behind `db pull`.
P5xxx are Accelerate/Data Proxy transport errors (rate limits, request size, timeouts) rather than database errors — read them as HTTP problems.

## Errors With No Code

| Message | Cause | Fix |
|---|---|---|
| "Query engine could not be located" / "PrismaClientInitializationError: could not locate the Query Engine" | The generated client is missing or built for another platform | `prisma generate` in the build; correct `binaryTargets` for the image (→ `deployment.md`) |
| "Cannot read properties of undefined (reading 'findMany')" | The model does not exist on this client: stale generation, or importing from the wrong output path | Regenerate; check the generator `output` and what the bundler resolved |
| "Unknown argument `x`" | Client generated from an older schema | Regenerate; in CI check that `postinstall` actually ran |
| "prepared statement \"s0\" already exists" | Transaction-mode pooler without `?pgbouncer=true` | Add the flag (→ `connections.md`) |
| "Do not know how to serialize a BigInt" | `BigInt` (including PostgreSQL `COUNT(*)`) reached `JSON.stringify` | Cast in SQL or add a serializer (→ `typescript.md`) |
| "Environment variable not found: DATABASE_URL" | `.env` not loaded in this context — CLI, edge runtime, and app load env differently | Load explicitly; do not assume the CLI's `.env` handling exists at runtime |
| "Error validating datasource: the URL must start with the protocol" | The env var is empty at generate time, not wrong | Check where the variable is set for the *build*, not for the run |
| Silent no-op: query never executes | A missing `await` — Prisma queries are lazy promises | Enable `no-floating-promises` (`SKILL.md` Traps) |

## Logging Errors Usefully

- Log `code`, `meta`, model and operation. The message can embed parameter values, which means PII in your log aggregator.
- Count P2002 and P2034 as metrics rather than alerts: they are expected under concurrency, and their *rate* is the signal.
- Alert on P2024 and P1017 immediately — those are capacity and connectivity, and they precede an outage rather than describing one.
