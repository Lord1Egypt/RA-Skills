# Clients — Normalized Caches, Fragments, And Why The UI Did Not Update

Every client-side GraphQL bug in this file has the same root: the cache is a graph of normalized entities, not a list of responses, and the developer reasoned about it as a list of responses. Library-specific names below follow `client_library` (default Apollo); the mechanics are the same in Relay and urql.

Contents: The Normalized Cache · Cache Keys · Fetch Policies · Why The UI Did Not Update · List Mutations · Optimistic Updates · Fragments · Pagination In The Cache · Error Handling · Subscriptions · SSR And Hydration · Traps

## The Normalized Cache

- On every response the cache splits objects out of the tree and stores each under a key, replacing them in the tree with references. Two queries touching the same entity share one copy; updating it once updates every view.
- The mechanism needs an identity. Without one, the object is stored *inline inside its parent*, so the same user fetched by two queries becomes two unrelated copies that drift.
- Normalization is per object, not per query: a query result is a shallow document of references. Evicting an entity therefore affects every query that referenced it.
- urql's default document cache does none of this — it caches whole responses keyed by document plus variables, and invalidates by `__typename` overlap. That is a deliberate and much simpler model; the normalized cache is opt-in (Graphcache). Know which you have before debugging "the cache did not update".

## Cache Keys

- Default key: `__typename` plus `id` (or `_id`). Missing either one means no normalization, with no warning.
- Always select `id` and `__typename` in every query, on every object you will later mutate. Most clients add `__typename` automatically; none can add `id` for you.
- Types with a different identity field (`code`, `sku`, `slug`) need explicit key configuration per type. Types with no identity at all (value objects, aggregates, connection payloads) should be declared keyless so the client stores them inline instead of colliding them.
- The collision to fear: two different types configured to key on the same field, or a type keyed on a field that is unique only per parent. `Address:1` under two different users is one cache entry and the second write wins.
- Server-side global ids (`schema.md`) remove this whole class of problem — one key space, no per-type configuration.

## Fetch Policies

| Policy | Reads cache | Hits network | Use for |
|---|---|---|---|
| `cache-first` (default) | yes | only on a miss | Most reads |
| `cache-and-network` | yes, then updates | always | Screens where staleness is visible and refresh is cheap |
| `network-only` | no | always | After a flow that invalidated more than the cache can know |
| `no-cache` | no | always, result not stored | One-off sensitive reads |
| `cache-only` | yes | never | Rendering from state you know is loaded |

- `cache-first` will never notice a server-side change nobody told it about. That is the intended behaviour and the source of most "stale data" reports.
- A partially-cached result counts as a miss: if the new query selects one field the cache lacks, the whole query goes to the network. Adding a field to a shared fragment can therefore change the cache-hit rate of unrelated screens.
- `no-cache` still normalizes nothing *and* shares nothing — two components using it fetch twice.

## Why The UI Did Not Update

Work down this list; it is ordered by frequency.

1. The mutation payload omitted `id` or `__typename` — the cache received an object it cannot match to the one on screen.
2. The mutation returned a `Boolean` or a bare count, so there was nothing to merge (SKILL.md rule 5).
3. The change was a list membership change (insert or delete), which normalization cannot infer — see below.
4. The query and the mutation selected *different fields* of the same entity: the cache merged what it got and the missing field is still the old value.
5. The component reads through a fragment that does not include the changed field.
6. Two entities collided on one cache key (see Cache Keys), so the update landed on the wrong object.
7. The query used `no-cache`, so it never participated.

## List Mutations

- A normalized cache updates *entities*; it cannot know that a newly created node belongs in a list it already holds, or that a deleted one should leave. Nothing in the response says so.
- Three fixes, in order of preference:
  1. Return the affected **connection or parent** from the mutation, so the list itself is part of the payload.
  2. Write an explicit cache update that inserts or removes the reference in the cached list.
  3. Refetch the affected query — correct, simplest, and the most bandwidth.
- Deletes need eviction *and* removal from every list: evicting the entity leaves dangling references, which most clients filter out of lists automatically but which can still surface as a null in a non-list field.
- `refetchQueries` on every mutation is the pattern teams fall into; it works and it turns every write into several reads. Reserve it for changes whose blast radius you genuinely cannot enumerate.

## Optimistic Updates

- The optimistic response must be shaped like the real one, including `__typename` on every object, or the cache cannot normalize it and the UI shows nothing until the server replies.
- The temporary id problem: an optimistic create needs an id before the server assigns one. Either the client generates the id and sends it in the mutation (also giving you idempotency, `mutations.md`), or the cache must reconcile a temporary key with the real one afterwards, which is where duplicate rows come from.
- Rollback is automatic on error and visually abrupt: the row appears, then vanishes. Pair it with an error message, or the user assumes it worked.
- Do not use optimistic updates for anything whose failure is likely or whose reversal is confusing (payments, irreversible state transitions). Use them for the cheap, near-certain cases: toggles, likes, reordering.
- Optimistic inserts into a sorted or paginated list are a guess about position; with keyset pagination the item may belong on a page the client has not loaded (`pagination.md`).

## Fragments

- Fragment colocation — each component declaring the fields it needs — is what keeps queries from accumulating fields nobody reads. The screen's query is the composition of its components' fragments.
- A fragment spread on the wrong type matches nothing and produces no error: the fields are simply absent at runtime. Type-aware generation catches this at build time; hand-written documents do not (`codegen.md`).
- Fragment names are global per document and must be unique; the convention `ComponentName_propName` prevents collisions and makes generated types readable.
- Relay enforces data masking: a component can only read fields declared in *its own* fragment, even if the query fetched more. That is the feature — it makes deleting a field safe, because the compiler proves nobody else read it. Other clients leave you to enforce it by discipline.
- A field removed from a fragment stays in the cache and disappears from the component. A field added is fetched by every query that spreads the fragment — including screens you did not think about.

## Pagination In The Cache

- Without a field policy, page two *replaces* page one in the cache and the list flickers back to its first page. The policy tells the cache how to merge pages of the same field.
- `keyArgs` decides what makes a *different list* versus a *different page*: filters and sort belong in `keyArgs`; `after`, `before`, `first`, `last` must not. Getting this backwards is the "filters bleed between tabs" bug.
- Apollo ships `relayStylePagination()` for the standard connection shape; anything custom needs a hand-written `merge` and `read`.
- Relay handles this natively through its pagination container, at the price of adopting the full Relay contract (global ids, a `node` field, the compiler).
- Refetching a paginated list resets it to one page unless the policy handles it — a "pull to refresh" that discards the user's scroll position without warning is this bug.

## Error Handling

- Two channels, and they are not interchangeable: GraphQL errors from the response's `errors` array, and network/transport errors from the request itself. Code that checks only one misses half the failures (`errors.md`).
- The error policy decides what happens to partial data: the default discards the data when any error is present; the permissive setting delivers `data` and `errors` together. For a screen where one widget can fail independently, the default throws away everything the server successfully produced.
- Branch on `extensions.code`, never on the message.
- Retries belong on network errors and on explicitly transient codes only. Retrying a validation failure loops forever.

## Subscriptions

- A reconnect does not restore subscriptions automatically in every client — verify. Events published during the gap are gone (`subscriptions.md`).
- The correct pattern on connect: run a query to establish current state, then apply live events on top, discarding any the state already includes. This needs a version or sequence on the entity.
- Subscription payloads flow into the same normalized cache: return the full entity with `id` and `__typename` and every view updates for free.
- An exception thrown inside a subscription handler can tear down the whole subscription in some clients. Catch inside the handler.

## SSR And Hydration

- Server-rendered pages must ship the cache state alongside the HTML, and the client must restore it *before* the first render, or every query refetches and the page flashes.
- Never share one client instance between requests on the server — that is the module-scope leak, client side: one user's cache serving another's page.
- Data that must not reach the browser must not enter the cache: the extracted cache state is embedded in the HTML in plain text.
- Time-dependent and viewer-dependent fields rendered on the server and hydrated on the client are the standard hydration-mismatch source; render them client-only or make the server value authoritative.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Mutation payload without `id`/`__typename` | The cache cannot match the entity | Always select both in the payload |
| `refetchQueries` on every mutation | Turns every write into several reads | Return the modified entity; refetch only for wide blast radius |
| Optimistic response missing `__typename` | Never normalizes; nothing renders until the server replies | Shape it exactly like the real response |
| Page arguments included in `keyArgs` | Every page becomes a separate list | Only filters and sort in `keyArgs` |
| Filters excluded from `keyArgs` | Results from one filter appear under another | Filters and sort in `keyArgs` |
| Checking only `networkError` or only `graphQLErrors` | Half the failures are invisible | Handle both channels |
| Sharing one client instance across SSR requests | One user's cache serves another's page | New client per request |
| Two types keyed on the same field | Silent cache collision, second write wins | Explicit per-type key configuration, or global ids |
