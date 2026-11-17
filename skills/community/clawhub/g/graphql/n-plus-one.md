# N+1 — Batching Every Field That Touches Data

The defining performance failure of GraphQL, and the one that never appears in a unit test: each field resolves independently, so a list of N parents asking for one relation each issues N queries. The arithmetic and the loader placement rule are SKILL.md rule 1; this file is how to get it right and how to find it when it is already wrong.

Contents: Spotting It · The Batch Function Contract · Loader Placement · Keys · Priming And Clearing · Nested N+1 · Batching Is Not Caching · When Not To Use A Loader · Alternatives · Measuring

## Spotting It

- Symptom: latency scales with page size. Ten items are fine, a hundred are ten times slower, and the database shows one statement repeated with different bind parameters.
- The log signature is the giveaway — identical SQL, sequential timestamps, one per row. Turn on statement logging for one request and count; do not reason about it from the resolver code.
- It hides behind ORMs: a lazy relation accessed in a resolver looks like a property read in the diff and is a round trip at runtime.
- It hides behind microservices too: N HTTP calls to a peer service is the same failure with worse constants and no SQL log to catch it.
- A loader in the codebase proves nothing. Grep for relation fields whose resolver does not go through one — new fields are added without loaders constantly, and nothing fails.

## The Batch Function Contract

```
batchFn(keys: readonly K[]) -> Promise<Array<V | Error>>
```

Three rules, and violating any of them corrupts data rather than slowing it down:

1. **Same length as `keys`.** Return one entry per requested key.
2. **Same order as `keys`.** `WHERE id IN (...)` returns rows in whatever order the database likes. Build a `Map` keyed by id and map over `keys` — never trust the row order.
3. **Missing means a slot, not a gap.** A key with no row returns `null` (or an `Error` instance for that position). Filtering it out shifts every subsequent result onto the wrong key: user 7 receives user 8's data, with no failure anywhere, forever.

```
const rows = await db.users.whereIn('id', keys)
const byId = new Map(rows.map(r => [String(r.id), r]))
return keys.map(k => byId.get(String(k)) ?? null)
```

- Returning an `Error` object in a position rejects only that key's promise. Throwing from the batch function rejects *every* key in the batch — one bad row fails a whole page.
- The batch fires when the current microtask queue drains: everything the executor requested in the same tick coalesces into one call. An `await` on something unrelated between two `.load()` calls splits them into two batches, which is why a `for` loop with `await` inside defeats the loader entirely (`resolvers.md`).
- Cap the batch. An unbounded batch turns a 10 000-item page into a 10 000-parameter `IN` clause that the planner handles badly or the driver rejects; set a maximum batch size so it splits into several statements.

## Loader Placement

- One loader instance per request, built in the context factory. Module-level loaders leak rows between users (SKILL.md rule 1) — the security failure, not the performance one.
- Loaders that need the viewer take it as a closure variable at construction time, not as part of the key. A loader whose cache key ignores the viewer is the same leak in a smaller box.
- In subscriptions, "per request" means per delivered message, not per connection: a connection-scoped loader caches the first payload for the life of the socket (`subscriptions.md`).
- In serverless, module scope survives between invocations on a warm instance. Every "it only leaks in production" report starts here.

## Keys

- Default cache keys compare by identity (`===`). Object keys therefore never hit the cache: two structurally identical filter objects are two entries and two batches. Supply a key function that serializes them.
- Numeric versus string ids are different keys: `1` and `"1"` both round-trip through your database as the same row and through the loader as two. Normalize with `String(key)` at both ends of the batch function.
- Composite keys (tenant + id) serialize to a delimiter-joined string, and the delimiter must be one that cannot appear in either part.
- A loader keyed by *query* rather than by *id* (`postsByAuthor`) is legitimate and common; it just batches less, because different filters cannot merge. Keep one loader per access pattern rather than one god-loader with a filter argument.

## Priming And Clearing

- After loading a list, prime the item loader with what you already have: fetching 50 posts then priming `postLoader` with each of them means a later `post(id:)` in the same document costs nothing.
- Priming does not overwrite an existing entry. Clear first if the value could be stale.
- After a mutation writes a row, clear that key — otherwise a query field in the same response reads the pre-mutation value out of the loader cache and the client sees its own write missing.
- `clearAll()` after any mutation is the blunt, correct default when in doubt; per-key clearing is an optimization that repays only in mutation-heavy documents.
- Loader caches live for one request. Cross-request caching is a different layer with different invalidation rules (`caching.md`); do not extend a loader's lifetime to get it.

## Nested N+1

- Batching one level pushes the problem down: `users → posts → comments` with loaders at every level is 3 round trips; with loaders at only the first is 1 + N + N×M.
- The depth×fanout arithmetic is what the cost limiter is really guarding (SKILL.md Cost Model): even perfectly batched, three levels of 50/20/10 loads 50 + 1000 + 10000 rows into memory to serve one response. Batching fixes the round trips, not the volume — page sizes still have to be capped.
- Cross-service depth is worse: each level is a network hop whose latency adds. Two hops of 40 ms nested inside a list is 80 ms of unavoidable serial time no matter how well you batch.
- Federation adds a hop per subgraph boundary crossed, and a boundary crossed twice in one plan is two fetches (`federation.md`).

## Batching Is Not Caching

- Deduplication within a request (the same id requested twice → one load) is the loader's caching. It is per-request, in-memory, and never invalidated by anyone else's write.
- A loader in front of Redis or an entity cache is fine; a loader *as* the cross-request cache is not, because nothing evicts it and nothing bounds it.
- Do not put a loader in front of an authorization decision. The cache is keyed by row id, and the answer depends on the viewer (`authorization.md`).

## When Not To Use A Loader

- One-to-one field on an already-loaded parent: the value is already in `parent`; a loader adds a hop and a cache entry for nothing.
- Genuinely singular root fields (`viewer`, `settings`): nothing to batch.
- A subtree that one join can serve entirely — projecting from `info` and loading once beats N batched loads (`resolvers.md`).
- Writes. Batching mutations hides which write failed and makes partial failure unreportable (`mutations.md`).

## Alternatives

| Approach | Round trips for a 3-level tree | Cost |
|---|---|---|
| No batching | `1 + N + N×M` | The failure this file exists for |
| Per-level loaders | one per level (3) | A loader per relation, forever, forgotten on new fields |
| Lookahead join from `info` | 1 | Complex SQL, row multiplication on multi-branch trees, coupling between parent and children |
| Whole-document compiler (Hasura, PostGraphile) | 1 | You inherit their schema conventions and lose hand-written resolver freedom |
| ORM with built-in relation batching | one per level, automatic | Only inside that ORM; a hand-written repository beside it reverts to N+1 unnoticed |

Default: per-level loaders everywhere, lookahead only for a measured hot path.

## Measuring

- Count statements per operation, not per request: one number, logged at the end of every operation in development, makes a regression obvious in the diff that caused it.
- Assert it in tests. A test that runs a two-level query against a real database and asserts "at most 3 statements" catches every missing loader a reviewer would not (`testing.md`).
- In tracing, the shape to look for is a wide band of identical short spans under one parent field (`production.md`).
- Rank by rows loaded, not by statements: 3 statements loading 10 000 rows to render 20 is a different bug, and capping the page size is the fix.
