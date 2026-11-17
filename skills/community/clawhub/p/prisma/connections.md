# Connections — Pools, Poolers, and Why the Database Says "Too Many"

One `PrismaClient` instance owns one connection pool. Every connection problem is a counting problem: how many instances exist, how many connections each is allowed, and how long each one is held.

## Contents

- The instance model
- Sizing
- Connection URL parameters worth knowing
- P2024 triage
- Poolers
- Timeouts and failure codes
- Shutdown and health

## The Instance Model

- One instance per **process**, created once at module load, reused for the life of the process. Not per request, not per module, not per service class.
- Node.js in cluster mode: one per worker. Serverless: one per warm sandbox, and the platform decides how many sandboxes exist.
- Next.js and any dev server with hot reload re-evaluate modules on every edit, creating a new client each time until the database refuses connections. The standard guard:

```ts
const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient }
export const prisma = globalForPrisma.prisma ?? new PrismaClient()
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

- Do not call `$connect()` at startup as a rule: the client connects lazily on the first query. Call it explicitly only when you want a fail-fast health check at boot.
- Do not call `$disconnect()` per request. Call it at process exit, in one-off scripts, and after test suites — nowhere else.

## Sizing

```
total connections = client instances × connection_limit
must satisfy: total ≤ max_connections − reserved − other consumers
```

Prisma's default `connection_limit` is `num_physical_cpus * 2 + 1` per instance. PostgreSQL's default `max_connections` is 100 with 3 reserved for superusers, so four 4-core application instances at the default (9 each = 36) coexist fine, while thirty serverless sandboxes at the default do not.

| Deployment | `connection_limit` | Reasoning |
|---|---|---|
| Single long-lived server | Default, or measured concurrency + headroom | The pool is the queue; deeper is not faster |
| Clustered server, N workers | `(budget / N)`, minimum 2 | Workers are independent pools |
| Serverless behind a pooler | 1-2 | Sandbox count is unbounded; the pooler owns the real connections |
| Serverless with no pooler | Not viable past trivial traffic | Every cold start opens a pool nothing hands back |
| Background worker doing bulk work | 2-5 | Fewer, longer statements — depth buys nothing |

Set it in the URL: `postgresql://user:pass@host:5432/db?connection_limit=10&pool_timeout=20`.

## Connection URL Parameters Worth Knowing

| Parameter | Default | Effect |
|---|---|---|
| `connection_limit` | `num_physical_cpus * 2 + 1` | Pool size for this client instance |
| `pool_timeout` | 10 (seconds) | How long a query waits for a free connection before P2024; `0` disables the wait |
| `connect_timeout` | 5 (seconds) | How long the initial TCP/handshake may take before P1001 |
| `socket_timeout` | none | Kills a query stuck on a silent socket; worth setting behind a NAT or load balancer |
| `schema` | `public` | PostgreSQL search path — also the per-tenant and per-test-worker isolation knob |
| `pgbouncer=true` | off | Disables named prepared statements for transaction-mode poolers |
| `sslmode` | provider-dependent | Managed providers usually require `require`; a certificate error at connect time is this |

## P2024 Triage

"Timed out fetching a new connection from the connection pool" means demand exceeded `connection_limit` for longer than `pool_timeout`. It is a symptom with four common causes, in the order to check them:

1. **A long-held connection.** Interactive transactions with network calls inside, or a transaction whose body waits on anything (→ `transactions.md`). One 3-second transaction on a pool of 5 caps throughput at under 2 operations/second.
2. **Too many client instances.** Grep for `new PrismaClient` — anything above one per process is the bug.
3. **The limit is genuinely below concurrency.** Raise `connection_limit` only after confirming the database has the headroom (`total` formula above).
4. **The database is slow, not the pool.** Every query holding a connection twice as long halves effective pool capacity. Check statement duration before adding connections.

Diagnose from the database side, not the app: connection counts per state (`active`, `idle`, `idle in transaction`) tell you whether connections are working or leaked. A pile of `idle in transaction` is an application bug — a transaction opened and never committed.

## Poolers

**Transaction-mode poolers** (PgBouncer, Supabase Supavisor, provider poolers) hand a server connection to a client only for the duration of a transaction. That multiplies your usable concurrency and removes session semantics:

- Add `?pgbouncer=true` so Prisma stops using named prepared statements. Without it, expect intermittent "prepared statement s0 already exists" errors under load.
- Migrations need a real session. Point `directUrl` at the database directly and keep `url` on the pooler:

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")        // pooled, used by the client
  directUrl = env("DIRECT_URL")          // direct, used by migrate and introspect
}
```

- Session-scoped features stop working: session advisory locks, `LISTEN`/`NOTIFY`, `SET` that must persist, temporary tables. Interactive transactions still work — they are a transaction, which is exactly the pooler's unit.
- `connection_limit` on the client should now be small (1-2 per instance): the pooler is the real pool.

**Prisma Accelerate** is a hosted pooler plus a query cache reached over HTTP, which also makes the client usable from edge runtimes. It is a managed dependency in the request path — evaluate it as one.

**Driver adapters** replace Prisma's own connection handling with a JavaScript driver (`pg`, Neon, PlanetScale, libSQL, D1). That is how Prisma runs on edge runtimes with no TCP, and it means pool behavior becomes the driver's, not Prisma's (→ `deployment.md`).

## Timeouts and Failure Codes

| Code | Meaning | Usual cause |
|---|---|---|
| P1001 | Can't reach database server | Host, port, firewall, SSL, or a paused serverless database |
| P1002 | Server reached but timed out | `connect_timeout` too low for a cold managed instance |
| P1017 | Server has closed the connection | Pooler or database idle timeout below the pool's own recycling; also a failover |
| P2024 | Timed out fetching a connection from the pool | Above |
| P2028 | Transaction API error | `maxWait` exceeded waiting for a connection to start a transaction |

Managed databases that sleep when idle (serverless Postgres tiers) produce P1001/P1002 on the first request after idling. Retry once with backoff at the edge of the app rather than treating it as an outage.

## Shutdown and Health

```ts
process.on('SIGTERM', async () => {
  server.close()            // stop accepting new work first
  await prisma.$disconnect() // then release the pool
  process.exit(0)
})
```

- Disconnecting before draining in-flight requests turns a clean deploy into a burst of P1017 for users mid-request.
- A health check is `SELECT 1` through `$queryRaw`, not a `findFirst` on a real table — you are testing the connection, not the schema.
- Long-lived workers should be restarted on repeated P1001 rather than retrying forever: a pool whose credentials rotated will never recover on its own.
