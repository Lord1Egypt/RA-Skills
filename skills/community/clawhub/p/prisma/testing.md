# Testing — Against a Real Database, Fast Enough to Keep

Default position: test Prisma code against the same engine production uses. Prisma's job is generating SQL, so a mocked client asserts that your mock matches your expectations and proves nothing about the query. Mocks are for the code *around* the query.

## Choosing the Target

| Approach | Fidelity | Cost | Verdict |
|---|---|---|---|
| Real engine in a container (Testcontainers, compose, CI service) | Full | Container startup, once per run | Default |
| Shared dev/CI server, isolated per worker | Full | Cheapest of the real options | Default when a server already exists |
| SQLite standing in for PostgreSQL | Low: no enums, no arrays, different case sensitivity, different JSON (→ `providers.md`) | Very cheap | Only for projects whose production database is SQLite |
| Mocked client (`jest-mock-extended`, in-memory fakes) | None for SQL | Free | Unit tests of logic that merely receives rows |
| Anything else | — | — | Extract the logic from the query and unit-test the logic |

## Isolation Between Tests

| Strategy | How | Trade-off |
|---|---|---|
| Transaction rollback per test | Run the test inside `$transaction`, throw at the end to roll back | Fastest; requires code that accepts an injected client, and cannot test code that opens its own transaction |
| Truncate between tests | `TRUNCATE ... RESTART IDENTITY CASCADE` on every table | Simple and universal; serial tests only |
| Schema per worker | `?schema=test_${WORKER_ID}` in the URL, migrate each once | Real parallelism on PostgreSQL, one-time setup cost per worker |
| Database per worker | Separate database per worker | Strongest isolation, slowest setup |
| Template database | Migrate once, `CREATE DATABASE t TEMPLATE base` per worker | Fast clones on PostgreSQL; the template must have no active connections |

Rollback per test, when the code base is written for it:

```ts
type Db = Prisma.TransactionClient
async function withRollback(fn: (db: Db) => Promise<void>) {
  const ROLLBACK = new Error('rollback')
  try {
    await prisma.$transaction(async (tx) => { await fn(tx); throw ROLLBACK })
  } catch (e) { if (e !== ROLLBACK) throw e }
}
```

This is why service functions should take `Db` as a parameter (→ `transactions.md`). Code that reaches for the global client cannot be isolated this way, and that constraint is the real reason to inject it.

## Setting Up the Test Database

```bash
# Fast path for tests: no history, no shadow database
DATABASE_URL=$TEST_URL npx prisma db push --skip-generate --force-reset

# When the test must also prove the migrations work
DATABASE_URL=$TEST_URL npx prisma migrate deploy
```

- `db push` is right for the everyday suite (it is faster and the history is irrelevant), and wrong for the job that verifies migrations. Run both: `db push` in the unit/integration suite, `migrate deploy` in one dedicated CI job.
- Generate once per run, not per worker: `prisma generate` is a build step, not a test fixture.
- Wait for readiness before migrating. A CI service container accepting TCP is not a database accepting queries — retry `SELECT 1` with backoff rather than sleeping a fixed number of seconds.

## Seed Data

- Factories over fixture files: a function per model with sensible defaults and an overrides argument keeps tests readable and lets each one state only what it cares about.
- Deterministic values for anything asserted; random values (with a logged seed) for anything that should not matter. Random data in an assertion is a flaky test with a delay fuse.
- Keep `prisma/seed.ts` for development data and CI demo environments. A test suite that depends on the dev seed breaks whenever someone improves the demo.
- Create related rows with nested writes, not with a chain of awaits: fewer round trips and the FK order is handled for you.

## What Deserves a Test

- Every raw SQL query — types will not catch a renamed column, and raw is where they bite hardest (→ `raw-sql.md`).
- Every client extension, including whether it still applies inside `$transaction` (→ `extensions.md`).
- Uniqueness and referential behavior you rely on: assert that the duplicate insert throws P2002, and that deleting the parent does what the schema says. This is a test of the migration, not of Prisma.
- Retry and conflict paths: force P2034 with two concurrent serializable transactions instead of trusting the retry loop by inspection.
- Query counts on hot endpoints, as an N+1 regression guard:

```ts
let count = 0
prisma.$on('query', () => { count++ })
await loadDashboard()
expect(count).toBeLessThanOrEqual(5)
```

## Mocking, When It Is Right

```ts
const db = mockDeep<PrismaClient>()
db.user.findUnique.mockResolvedValue({ id: '1', email: 'a@b.c' } as User)
```

Legitimate for: a handler's branching on results, error mapping (P2002 → 409), and code where the database is incidental. Not legitimate for anything asserting *what* was queried — a mock that returns whatever you told it also accepts the query you wrote wrong.

## Migration Testing

- One CI job restores a production-shaped dump (anonymized), runs `migrate deploy`, and fails on error. That job catches the migrations that only fail against real data volume or real constraint violations.
- Assert row counts before and after a destructive migration. A rename that became DROP + ADD passes every unit test and loses a column of data (`SKILL.md` rule 3).
- Time it. A migration that takes four minutes on production volume is a deployment plan, not a surprise for release night.

## CI Shape

```yaml
# service: postgres  →  wait for readiness  →  db push  →  test  →  (separate job) migrate deploy
env:
  DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test?schema=public
```

- Run `prisma generate` in the build step and cache `node_modules` carefully: a cached install that skips `postinstall` ships a stale client and produces failures that look like schema errors (→ `deployment.md`).
- Parallel workers need separate schemas or separate databases. Sharing one and hoping the tests do not collide produces failures that only reproduce under load.
