# Performance — Count the Queries, Then the Rows, Then the Bytes

Order of investigation, always: how many round trips, how many rows each one reads, how many bytes come back. Skipping to indexes is the common waste — a perfectly indexed query executed 300 times per request is still 300 round trips.

## Measure Before Touching Anything

```ts
const prisma = new PrismaClient({
  log: [{ emit: 'event', level: 'query' }],
})
prisma.$on('query', (e) => {
  if (e.duration > 50) console.warn(e.duration, e.query, e.params)
})
```

- The event carries the emitted SQL, the parameters and the duration in milliseconds. Threshold the log — an unfiltered query log on a busy service is its own performance problem.
- `DEBUG=prisma:query` is the zero-code version for a one-off investigation.
- Count queries per request, not per query type. The number that matters is "how many statements did this endpoint send", and it is usually a surprise.
- Take the emitted SQL and run it directly against the database with the engine's own plan tool. Prisma cannot tell you why a statement is slow; the database can (→ `pg`, `sql`).
- Client-side metrics and OpenTelemetry tracing exist behind preview features; useful for a fleet, unnecessary to answer a single endpoint's question.

## The Query Count Model

```
queries per operation = 1 + (relations included at each level, with the query strategy)
```

- One `findMany` with three includes is 4 statements regardless of row count. This is not N+1, and rewriting it as raw SQL usually buys one round trip, not an order of magnitude.
- Real N+1 comes from control flow: a `for` loop over rows calling `findUnique`, a GraphQL resolver per field, or `await` inside `.map()` without batching.
- Exception worth knowing: `findUnique`/`findUniqueOrThrow` on the same model in the same event-loop tick are collapsed into one `WHERE id IN (...)`. So a `Promise.all` of 100 `findUnique` calls is 1 query, while the same 100 calls awaited sequentially in a loop are 100. Nothing else — not `findFirst`, not `findMany` — batches.
- GraphQL resolvers still need a DataLoader for anything except that `findUnique` shape, or load the whole tree in one query at the root and pass it down.

## Relation Load Strategy

Where supported (`relationLoadStrategy`, `prisma >=5.7`, `relationJoins` preview, PostgreSQL and MySQL):

| Strategy | Shape | Wins when |
|---|---|---|
| `join` | One statement, relations aggregated as JSON in the database | Round-trip latency dominates: distant database, deep nesting, small relation payloads |
| `query` | One statement per relation, joined in the query engine | Wide or duplicated relation rows: the join would multiply parent columns across every child |

Measure on real data rather than reasoning about it. A parent with 40 columns and 500 children pays for those 40 columns 500 times in a join; a three-level nest across a 30 ms link pays 4 × 30 ms in the query strategy.

## Indexing for Prisma's Access Paths

- Prisma indexes `@id` and `@unique` only; foreign keys are yours on PostgreSQL, mandatory under `relationMode = "prisma"` (`SKILL.md` rule 4).
- Write the index from the query, not from the model: filter columns first (equality), then the sort column. `where: { tenantId }, orderBy: { createdAt: 'desc' }` wants `@@index([tenantId, createdAt(sort: Desc)])`.
- `mode: 'insensitive'` emits `ILIKE`/`lower()`-style predicates that a plain B-tree index cannot serve. The fix is a functional index, which the schema cannot express — write it in a migration and remember the diff will keep proposing to drop it (→ `migrations.md`).
- `contains` with a leading wildcard never uses a B-tree. Either accept the scan on a small table or move to a real search structure (→ `queries.md`, Search).
- Every index costs write throughput and disk. Add them from measured plans, and review unused ones per business cycle rather than per sprint.

## Payload Size

- Default reads return every scalar column. On a table with a large `Json` blob or a text body, `select` of the four fields the UI renders can cut the response by an order of magnitude — measure the row width before optimizing anything cleverer.
- `include` on a to-many relation with no `take` loads the whole relation. `include: { comments: { take: 3, orderBy: { createdAt: 'desc' } } }` is almost always what the screen actually needs.
- Global `omit` on the client keeps heavy or sensitive columns out of every default result set (→ `queries.md`).
- Relation counts through `_count` instead of loading rows to call `.length` is the same answer for a fraction of the bytes.

## Counts

| Need | Approach | Cost |
|---|---|---|
| "Has more" for a paginated list | Fetch `take + 1`, compare length | Free — it is the same query |
| Exact total for a filtered admin view | `count({ where })` | Index scan at best, full scan when the filter is unindexed |
| Total rows in a big table for a dashboard | Approximate count from database statistics via `$queryRaw` | Constant, and stale by design |
| A number rendered on every page view | Maintained counter column updated with `{ increment: 1 }` | One extra write per event, contention on the counter row |

`count()` is not cached by anything. On the request path it runs every render.

## Round Trips and Latency

```
floor latency = statements × round-trip time
```

A page issuing 8 statements against a database 30 ms away cannot finish faster than 240 ms, no matter how fast the queries are. Consequences, in order of leverage: co-locate the app and the database (same region, ideally same zone); collapse independent reads with `Promise.all` or `$transaction([...])`, which still ships them as one round trip's worth of pipelining; then reduce the statement count with the join strategy or one hand-written query.

## Bulk Work

- One statement over N rows always beats N statements: `updateMany` over a filter, `createMany` in chunks, or a raw `INSERT ... ON CONFLICT` for bulk upserts (→ `queries.md`).
- Chunk large bulk inserts at 1,000-5,000 rows — parameter limits (PostgreSQL: 65,535 bind parameters) and lock duration both argue against one giant statement.
- Long-running jobs should not hold an interactive transaction. Batch with a resume key and commit per batch (→ `migrations.md`, backfills).

## Caching

- Nothing in Prisma Client caches results between requests. Repeated identical reads hit the database every time.
- Prisma Accelerate adds a managed cache with `cacheStrategy: { ttl, swr }` per query plus a connection pool in front of the database; it is a hosted dependency, so weigh it as one.
- Application-side caching in front of Prisma is ordinary cache work: cache what is read far more often than written, and invalidate on the write path in the same transaction boundary that produced the change.

## Checklist

- Did you count statements per request before optimizing?
- Is the slow thing the round trip count, the rows read, or the bytes returned? Name it before changing code.
- Does each hot query have an index matching its filter-then-sort shape?
- Does every list endpoint have a `take` and a deterministic `orderBy`?
- Is any `count()` on the request path avoidable?
- After the change: same measurement, same conditions, and the query log to prove the statement count moved.
