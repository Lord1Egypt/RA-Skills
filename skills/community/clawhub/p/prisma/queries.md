# Queries — The Client API and Its Sharp Edges

Every Prisma query compiles to one SQL statement per relation level. Most surprises are semantic, not syntactic: a filter that silently disappears, a relation predicate that matches rows with no relations, a pagination scheme that drops a row when two records share a timestamp.

## Contents

- Reads and their throw variants
- Filters that behave unexpectedly
- Shaping the result
- Pagination
- Ordering
- Writes and nested writes
- Bulk writes
- Upsert and its race
- Aggregation and grouping
- Search
- Recipes

## Reads and Their Throw Variants

| Call | Returns | Use |
|---|---|---|
| `findUnique` | Row or `null` | Lookup by `@id`/`@unique`; batched with other `findUnique` calls in the same tick |
| `findUniqueOrThrow` | Row or throws P2025 | The 90% case in a request handler — removes the null branch |
| `findFirst` | First match or `null` | Any non-unique predicate; pair with `orderBy` or "first" is arbitrary |
| `findMany` | Array (possibly empty) | Lists — always with `take` |
| `count` / `aggregate` / `groupBy` | Numbers | See Aggregation |

`findUnique` accepts extra non-unique filters alongside the unique key (`prisma >=5`): `where: { id, tenantId }` fails with P2025 rather than returning another tenant's row. This is both the cheapest tenant guard and the optimistic-lock primitive (→ `transactions.md`).

## Filters That Behave Unexpectedly

- `undefined` removes the condition; `null` matches SQL NULL. This is the highest-severity semantic in the client (`SKILL.md` rule 6).
- Relation filters: `some` = at least one related row matches; `none` = no related row matches; **`every` is vacuously true for rows with zero related rows** — `where: { posts: { every: { published: true } } }` returns every author who has never written. Pair it with `some: {}` when you mean "has posts, all published".
- `NOT` on a nullable column excludes NULLs: `where: { NOT: { status: 'archived' } }` drops rows where `status` is NULL, because NULL ≠ 'archived' is unknown in SQL. Write `OR: [{ status: null }, { NOT: { status: 'archived' } }]` when NULL means "not archived".
- `AND`/`OR` take arrays; an empty `OR: []` matches nothing while an empty `AND: []` matches everything. Building either from a filtered list of user inputs is how a search page returns zero results with no error.
- `contains`/`startsWith` are case-sensitive on PostgreSQL until you add `mode: 'insensitive'`, which exists on PostgreSQL and MongoDB only. MySQL is case-insensitive by default through its collation, which is why the same code behaves differently across environments (→ `providers.md`).
- `in: []` (empty array) matches nothing, which is usually correct and occasionally a silent empty page after a `.map()` upstream returned nothing.
- Filtering on a relation's scalar requires going through the relation (`where: { author: { is: { role: 'ADMIN' } } }`), and `is: null` / `isNot: null` is how you ask for missing optional relations.

## Shaping the Result

- `select` and `include` are mutually exclusive at the same level; nest `select` inside `include` to prune relation fields.
- `omit` (`prisma >=5.13`) removes fields from the default set — the clean way to keep `passwordHash` out of every result without listing every other column. It can also be set globally on the client constructor, which is the only version of this rule that cannot be forgotten at a call site.
- Selecting fewer columns is the cheapest optimization available on wide tables: it changes bytes over the wire per row, and on a distant database that dominates (→ `performance.md`).
- `_count` belongs in `select`: `select: { id: true, _count: { select: { posts: true } } }` returns the count in the same round trip.

## Pagination

**Offset** — `skip`/`take`. Simple, supports jumping to page N, and the database still walks every skipped row: page 1000 at 50 per page reads 50,050 rows to return 50.

**Cursor** — constant cost at any depth, no jumping:

```ts
const page = await prisma.post.findMany({
  take: 20,
  skip: cursor ? 1 : 0,          // skip the cursor row itself
  cursor: cursor ? { id: cursor } : undefined,
  orderBy: [{ createdAt: 'desc' }, { id: 'desc' }],
})
```

- The `orderBy` must be deterministic. Ordering by `createdAt` alone with two rows sharing a millisecond skips or repeats a row at the page boundary — always append a unique tie-breaker.
- `take: -20` with a cursor walks backwards, returning the rows before it.
- The cursor field must be unique, and the index must cover the full `orderBy` tuple or the "cheap" pagination sorts the table on every page.
- Total counts are a second query. On large tables, prefer "has more" (fetch `take + 1`) over an exact total (→ `performance.md`).

## Ordering

- `orderBy` accepts an array; order in the array is the sort priority.
- Sort by a relation aggregate: `orderBy: { posts: { _count: 'desc' } }`. Sort by a to-one relation field: `orderBy: { author: { name: 'asc' } }`.
- NULL placement (`orderBy: { updatedAt: { sort: 'desc', nulls: 'last' } }`) is available where the provider supports it; MySQL and SQLite have fixed NULL ordering and ignore the ask.
- `distinct` is applied by the query engine on connectors without native support, which means it deduplicates **after** the limit: `distinct: ['authorId'], take: 10` can return fewer than 10 rows. For reliable deduplicated pages, use `groupBy` or raw SQL (→ `raw-sql.md`).

## Writes and Nested Writes

- A nested write is one transaction. `create` with nested `create`/`connect`/`connectOrCreate` either lands completely or not at all — wrapping it in `$transaction` adds nothing but a held connection.
- Relation operations inside an update: `connect` (link existing), `disconnect`, `set` (replace the whole list), `create`, `createMany`, `update`, `updateMany`, `upsert`, `delete`, `deleteMany`. `set: []` clears a to-many relation; on a required relation it fails instead of orphaning.
- `connectOrCreate` replaces the find-then-create round trip, and still races under concurrency: two requests can both miss and both insert. The unique constraint is what saves you — catch P2002 and retry once (`SKILL.md` rule 9).
- Atomic number operations avoid read-modify-write entirely: `data: { views: { increment: 1 } }`, plus `decrement`, `multiply`, `divide`, `set`. Reading a counter, adding one in JavaScript, and writing it back loses updates under any concurrency at all.
- `update` requires a unique `where` and throws P2025 if nothing matches. `updateMany` takes any filter, returns `{ count }`, and supports no nested writes.
- `delete`/`deleteMany` respect the referential actions in the schema, not the code's expectations: P2003 on delete means a `Restrict` you inherited by default (→ `schema.md`).

## Bulk Writes

| Need | Call | Constraint |
|---|---|---|
| Insert many, count is enough | `createMany` | No nested creates; `skipDuplicates` unsupported on MongoDB and SQL Server |
| Insert many, need the rows | `createManyAndReturn` (`prisma >=5.14`) | PostgreSQL, CockroachDB and SQLite only |
| Different rows, different values | `$transaction([...updates])` | One round trip per statement inside one transaction |
| Same value across a filter | `updateMany` | Returns a count only |
| Insert-or-update in bulk | Raw `INSERT ... ON CONFLICT DO UPDATE` | Prisma has no bulk upsert (→ `raw-sql.md`) |

`createMany` with 100,000 rows builds one enormous statement and can exceed parameter limits (PostgreSQL caps at 65,535 bind parameters — with 8 columns that is ~8,000 rows). Chunk at 1,000-5,000 rows per call and wrap the chunks in a transaction if atomicity matters.

## Upsert and Its Race

`upsert` maps to a native `INSERT ... ON CONFLICT` when the shape allows it (a single unique field in `where`, no nested writes). Outside that shape it degrades to find-then-write in two statements, and two concurrent callers both find nothing:

- Always have the unique constraint the upsert relies on. Without it, the race produces duplicates instead of an error, which is strictly worse.
- Catch P2002 and retry the upsert once. The retry finds the row the other request just wrote.
- Nested `upsert` inside a parent write is the version most likely to take the slow path — check the query log if throughput matters.

## Aggregation and Grouping

```ts
const stats = await prisma.order.groupBy({
  by: ['status'],
  where: { createdAt: { gte: since } },
  _count: { _all: true },
  _sum: { total: true },
  having: { total: { _sum: { gt: 1000 } } },
})
```

- Every field in `by` must appear in `select`-equivalent position; filters on aggregates go in `having`, filters on rows go in `where` — putting a row filter in `having` computes the aggregate first and then discards, which is both slower and a different answer.
- `_count: { _all: true }` counts rows; `_count: { field: true }` counts non-NULL values of that field. They differ exactly where the column is nullable.
- `_avg` and `_sum` on a `Decimal` column return `Prisma.Decimal` (→ `typescript.md`).
- Anything with a window function, a rollup, or a percentile is raw SQL territory (→ `raw-sql.md`).

## Search

- `contains` is `LIKE '%x%'`: no index can serve a leading wildcard, so it degrades linearly with table size. Acceptable up to tens of thousands of rows, never on a hot path over millions.
- Prisma's full-text `search` operator is a preview feature on PostgreSQL and MySQL, and the flag name changed between Prisma 5 and 6 — check the generator block before assuming it is available.
- Serious search means database-native structures Prisma cannot express: a stored `tsvector` with a GIN index, a trigram index for fuzzy matching, or an external engine. Model the column, index it in raw SQL, query it with `$queryRaw` (→ `raw-sql.md`, and `pg` for the PostgreSQL side).

## Recipes

```ts
// Existence check without loading the row
const exists = (await prisma.user.count({ where: { email }, take: 1 })) > 0

// Page plus "has more", without a second count query
const rows = await prisma.post.findMany({ take: pageSize + 1, /* cursor, orderBy */ })
const hasMore = rows.length > pageSize
const page = hasMore ? rows.slice(0, pageSize) : rows

// Find-or-create, race-safe
try {
  return await prisma.tag.create({ data: { name } })
} catch (e) {
  if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === 'P2002') {
    return prisma.tag.findUniqueOrThrow({ where: { name } })
  }
  throw e
}

// Tenant-scoped read that cannot leak
const doc = await prisma.document.findUniqueOrThrow({ where: { id, tenantId } })
```
