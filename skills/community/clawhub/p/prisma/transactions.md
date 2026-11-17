# Transactions — Atomicity Without Holding the Pool Hostage

Four ways to be atomic in Prisma, in ascending cost. Pick the cheapest one that expresses the requirement, because each step up holds a connection longer.

| Mechanism | Atomic | Holds a connection for | Use when |
|---|---|---|---|
| Nested write (`create` with nested `create`/`connect`) | Yes | One statement | The whole change is one object graph |
| `$transaction([q1, q2, q3])` | Yes, all-or-nothing | One round trip's worth | Independent statements whose inputs are already known |
| `$transaction(async (tx) => {...})` | Yes | The entire callback | A later write depends on an earlier read |
| Raw `BEGIN`/`COMMIT` via `$executeRaw` | Only by luck | Unbounded | Never — the statements can land on different pooled connections |

## Contents

- Batch transactions
- Interactive transactions
- Isolation levels
- Retrying
- Optimistic locking
- Pessimistic locking
- Deciding between them

## Batch Transactions

`$transaction([...])` sends an array of already-built queries: sequential inside one transaction, rolled back entirely if any fails, and it returns results positionally.

- It cannot branch. Nothing inside can read a result and decide what to do next — that requirement is what interactive transactions are for.
- It is also the cheap way to pipeline independent reads: three counts in one array is one transaction and one round trip's latency instead of three.

## Interactive Transactions

```ts
await prisma.$transaction(async (tx) => {
  const from = await tx.account.update({
    where: { id: fromId, balance: { gte: amount } },
    data: { balance: { decrement: amount } },
  })
  await tx.account.update({ where: { id: toId }, data: { balance: { increment: amount } } })
  return from
}, { timeout: 10_000, maxWait: 5_000, isolationLevel: 'Serializable' })
```

Rules that are not optional:

1. **Use `tx`, never the outer client, inside the callback.** A call to `prisma.*` inside the block runs on a different connection, outside the transaction: it cannot see uncommitted rows, and if it needs a lock the transaction holds, both wait until the pool times out. This is the single most common "Prisma deadlock" that is not a database deadlock.
2. **No network calls, no queues, no user input, no `sleep`.** The connection is held for the whole body; a 2-second payment API call inside a transaction is a 2-second connection lease multiplied by concurrency.
3. **Defaults: `timeout` 5000 ms, `maxWait` 2000 ms.** `maxWait` is how long the call waits for a free connection before P2028; `timeout` is how long the body may run before rollback. Raise them deliberately and locally, never globally to silence a symptom.
4. **Keep the read-write pair adjacent.** Everything between the read and the write is lock duration for every concurrent writer touching those rows.
5. Concurrency ceiling is the pool: `connection_limit` simultaneous interactive transactions, then P2028 after `maxWait` (2 s by default) — not P2024, which is what an ordinary query gets after waiting out `pool_timeout` (`SKILL.md` rules 7-8, `connections.md`).

The callback receives a `Prisma.TransactionClient`, which deliberately lacks `$transaction`, `$connect`, `$disconnect` and `$extends` — there are no nested transactions. Compose by threading the client through your service functions:

```ts
type Db = Prisma.TransactionClient | PrismaClient
async function debit(db: Db, id: string, amount: number) { /* ... */ }
```

## Isolation Levels

`isolationLevel` accepts `ReadUncommitted`, `ReadCommitted`, `RepeatableRead`, `Serializable` (and `Snapshot` on SQL Server), subject to the provider. PostgreSQL and SQL Server default to `ReadCommitted`; MySQL/InnoDB defaults to `RepeatableRead`.

- `ReadCommitted` allows a value read at the start of the transaction to change before the write — the read-modify-write anomaly. Atomic operators (`{ increment: 1 }`) sidestep it entirely for counters.
- `Serializable` makes the anomaly impossible and makes P2034 likely: the database aborts one of two conflicting transactions instead of producing a wrong answer. **Serializable without a retry loop is worse than ReadCommitted**, because the failure moves from silent to visible with nobody handling it.
- MongoDB transactions require a replica set; a standalone deployment refuses them (→ `providers.md`).

## Retrying

Retry the whole `$transaction` call from outside. The transaction client is dead once the transaction fails, so retrying inside the callback yields P2028.

```ts
async function withRetry<T>(fn: () => Promise<T>, attempts = 3): Promise<T> {
  for (let i = 0; ; i++) {
    try {
      return await fn()
    } catch (e) {
      const retryable =
        e instanceof Prisma.PrismaClientKnownRequestError &&
        (e.code === 'P2034' || e.code === 'P2024')
      if (!retryable || i >= attempts - 1) throw e
      await new Promise((r) => setTimeout(r, 2 ** i * 50 + Math.random() * 50))
    }
  }
}
```

- Exponential backoff with jitter: without jitter, every conflicting client retries at the same instant and reproduces the conflict.
- Cap attempts at 3. A conflict that survives three retries is a design problem — usually two code paths taking the same rows in opposite orders.
- Retried transactions must be idempotent from the outside: they will run more than once. An email sent inside a retried transaction is sent twice.

## Optimistic Locking

Cheaper than a transaction for the "last writer wins is unacceptable" case, and it needs no locks at all:

```ts
const updated = await prisma.document.update({
  where: { id, version: currentVersion },      // non-unique filter alongside the unique key
  data: { body, version: { increment: 1 } },
})
// P2025 here means someone else wrote first — reload and re-apply, do not overwrite
```

- Requires `prisma >=5` (non-unique filters in a unique `where`).
- P2025 is the conflict signal, and it is indistinguishable from "row deleted" — check existence in the recovery path if the difference matters to the user.
- Same shape works as a tenant guard: `where: { id, tenantId }` cannot return another tenant's row.

## Pessimistic Locking

Prisma has no `SELECT ... FOR UPDATE`. Inside an interactive transaction, drop to raw:

```ts
await prisma.$transaction(async (tx) => {
  const [row] = await tx.$queryRaw<Row[]>`SELECT * FROM "Job" WHERE id = ${id} FOR UPDATE`
  // ... decide, then write through tx
})
```

- `FOR UPDATE SKIP LOCKED` is the job-queue primitive: concurrent workers each claim different rows without blocking (→ `pg`).
- Hold locks in a consistent order across the whole codebase. Two transactions taking rows A→B and B→A deadlock deterministically under load; the fix is an ordering convention, not a longer timeout.

## Deciding Between Them

- Counter or balance adjustment with no branch → atomic operator, no transaction.
- Two writes that must both land, inputs known up front → `$transaction([...])`.
- Read, decide, write → interactive transaction, as short as physically possible.
- Long human-scale workflow (draft, review, approve) → not a transaction at all: a state column, an idempotency key, and separate commits.
