# Federation — One Graph, Several Teams

Federation composes independently deployed subgraphs into one schema a client queries as if it were monolithic. It solves an organizational problem — teams shipping on their own cadence — and charges you a query planner, a composition step in the deploy path, and a new class of cross-service performance bug. Adopt it for the org chart, not for the graph size.

Contents: When It Is Worth It · The Alternatives · Entities And Keys · Reference Resolvers · Cross-Subgraph N+1 · Extending Types · Composition Failures · Auth Across Subgraphs · Performance · Operating It · Traps

## When It Is Worth It

| Signal | Verdict |
|---|---|
| Several teams deploying separately, owning disjoint entities | Federation earns its cost |
| One team, one repository, a large schema | Modularize the schema; do not federate |
| Wrapping existing REST services behind one graph | A gateway or BFF is simpler (`rest-migration.md`) |
| Merging two products after an acquisition | Federation, or a namespaced stitching layer |
| "The schema file is getting long" | Split the files; the schema is one artifact either way |

- The real cost is that a schema change can now fail at *composition*, in someone else's deploy, hours after your merge. Every team must be able to run the composition check locally or the model does not hold.
- Federation is not a performance strategy: it adds a hop per boundary crossed. The graph gets slower and the teams get faster.

## The Alternatives

- **Schema stitching**: the gateway holds the mapping and the delegation logic. Older, still viable, and centralizes the coupling in one place — which is the opposite of what federation is for. Reasonable when one team owns the composition and the subgraphs cannot be changed.
- **Namespaced monolith**: one service, modules with clear ownership, one deploy. Keeps everything simple and fails only when teams must deploy independently.
- **BFF per client**: each client surface gets its own graph over shared services. Removes cross-team schema negotiation entirely at the cost of duplicated resolvers.
- Recorded under Tooling: which gateway (or none) is in play changes every command and directive name below.

## Entities And Keys

An entity is a type that more than one subgraph can contribute fields to, identified by a key.

```graphql
# products subgraph
type Product @key(fields: "id") { id: ID!, name: String!, price: Money! }

# reviews subgraph
type Product @key(fields: "id") { id: ID!, reviews: [Review!]! }
```

- The key must be **stable, globally unique for that type, and resolvable by every subgraph that declares it**. A key that is unique only within a tenant produces cross-tenant collisions at the gateway.
- Compound keys (`@key(fields: "sku warehouse")`) are legal and mean every referencing subgraph must carry both parts.
- Multiple keys on one entity let different subgraphs reference it by whatever they hold — useful and worth the extra resolver.
- The key fields travel between services in every plan. Choosing a heavy field as the key means shipping it constantly.
- A type without a key cannot be extended by another subgraph: value types must be identical wherever they are declared, or composition fails.

## Reference Resolvers

- The gateway asks a subgraph "here is a key, give me your fields" through the entity-resolution entry point (`__resolveReference` in JavaScript implementations, the equivalent hook elsewhere).
- The reference resolver receives *only the key fields*, never the whole object. Code that reads `reference.name` because the field happens to be there in one plan breaks when the planner takes a different route.
- It is a public entry point: anything that can reach the subgraph can request any entity by key. Apply the same row-level authorization you apply to `node(id:)` (`authorization.md`).
- Returning `null` from a reference resolver leaves the entity's fields null in the composed response — which, for a non-null field, nulls the parent (SKILL.md Null Propagation). Deleted entities referenced from another subgraph are the common cause.
- The gateway sends entity references in **batches** (one call with an array of representations per subgraph per plan step). Reference resolvers therefore receive many keys at once in practice — batch inside them, or the boundary becomes an N+1 with network latency instead of database latency.

## Cross-Subgraph N+1

- The shape: query 50 products from subgraph A, ask for `reviews` from subgraph B. The planner batches the 50 keys into one call to B, and B then resolves reviews per product. Without a loader inside B, that is 50 queries behind one HTTP hop — invisible in the gateway's trace, which shows a single healthy fetch.
- Every subgraph therefore needs its own batching discipline (`n-plus-one.md`); federation moves the problem, it does not solve it.
- Nested boundary crossings multiply: A → B → A is two extra hops and a plan that re-enters the first subgraph. The planner will do it with no warning; the trace shows it as three fetches for one query.
- Design entities so that a client's common query crosses at most one boundary. Where a path crosses three, that is a signal the ownership split is wrong, not that the planner needs tuning.

## Extending Types

- `@shareable` marks a field more than one subgraph may resolve. Both must return the same value for the same key, and nothing verifies that: a divergence shows up as a value that changes depending on which subgraph the planner chose.
- `@external` declares a field the subgraph does not own but needs locally, usually to satisfy `@requires`.
- `@requires(fields: "…")` asks the gateway to fetch fields from the owning subgraph before resolving yours. It costs an extra hop per use and is the most common source of surprise latency.
- `@provides(fields: "…")` promises that this subgraph can return the field inline, letting the planner skip a hop. It is a promise the planner trusts and nothing checks — a wrong `@provides` returns stale or null data.
- `@override` moves ownership of a field between subgraphs across a deploy; run it as a two-step migration with both sides live.
- `@inaccessible` hides a field from the composed schema while subgraphs still use it internally — the tool for staging a rollout, and a way to keep a field out of the public API.
- Interfaces spanning subgraphs are the sharpest edge: adding a field to a shared interface forces a coordinated deploy across repositories (`schema.md`).

## Composition Failures

- Composition runs at build time and produces the supergraph. Common failures and their causes:

| Failure | Cause |
|---|---|
| Type mismatch for a shared field | Two subgraphs declare the same field with different types or nullability |
| Missing `@key` on a referenced entity | A subgraph extends a type nobody declared as an entity |
| Value type mismatch | A non-entity type declared differently in two subgraphs |
| Unresolvable field | `@requires` names a field no subgraph provides |
| Enum divergence | The same enum with different members in two subgraphs |

- Composition failure blocks the deploy of *whichever team merged second*, for a reason introduced by the first. That social dynamic is the real tax; a pre-merge composition check against the current supergraph is what makes it bearable.
- Run the check in every subgraph's CI against the published supergraph, not only in the gateway's pipeline (`schema-evolution.md`).

## Auth Across Subgraphs

- The gateway is not a trust boundary. Every subgraph authenticates and authorizes independently, or reaching any subgraph directly grants everything.
- Propagate the viewer as a verifiable credential (the original token, or a signed internal assertion) — never as a plain `x-user-id` header, which anything on the network can forge.
- Reference resolvers and `@requires` both cross ownership boundaries: a field one subgraph may compute is not automatically a field this caller may see. Check in the subgraph that owns the data.
- Rate limits and cost budgets applied only at the gateway are bypassed by direct subgraph access. Keep subgraphs on a private network and still limit them.

## Performance

- Latency is additive per boundary crossing, not per subgraph: a plan with four sequential fetches costs the sum of four round trips plus each subgraph's own work (`performance.md`).
- Read the query plan for your top operations. The planner's choices are not obvious, and a `@provides` or a key change can remove a whole fetch step.
- Response caching at the gateway keys on the whole composed response; entity caching inside each subgraph is usually the better layer (`caching.md`).
- Subscriptions over federation are supported unevenly across gateways and usually route to a single owning subgraph. Verify support before designing a realtime feature into a federated graph (`subscriptions.md`).

## Operating It

- The supergraph is a deployment artifact with a version. Roll it forward and back like code; a gateway serving a supergraph older than a subgraph's deploy is a normal transient state you must survive.
- Deploy order: publish the subgraph schema and let composition succeed *before* the subgraph's new code goes live for additive changes; for removals, reverse it — remove usage, deploy, then remove the field.
- Field-level usage telemetry must be per subgraph *and* per client, or no team can tell whether their deprecated field is safe to remove.
- Give each subgraph an independently reachable health check and its own traces; a gateway-only view hides which service is slow.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Federating to split a large schema in one team | All the cost, none of the autonomy benefit | Modularize inside one service |
| Reference resolver reading non-key fields | It only receives the key; other fields depend on the plan | Load from the key alone |
| No batching inside a reference resolver | The boundary batch becomes N queries behind one hop | Loaders inside every subgraph |
| Key unique only per tenant | Collisions at the gateway across tenants | Globally unique keys |
| `@provides` that is not actually true | The planner trusts it; clients get stale or null data | Only promise fields you resolve locally in that path |
| `x-user-id` header between gateway and subgraph | Trivially forged by anything on the network | Verifiable token or signed assertion |
| Composition checked only in the gateway pipeline | The break is found after merge, in another team's deploy | Check in every subgraph's CI against the published supergraph |
| Assuming the gateway rate limit protects subgraphs | Direct access bypasses it | Limit at both layers, private network |
