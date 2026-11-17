# Adoption And Coexistence — Should This Be GraphQL, And How Do You Get There

Most GraphQL disappointments are adoption failures, not technical ones: a graph that mirrors REST resources one-to-one, or a graph adopted where one endpoint per screen would have been simpler and faster. Answer the first question before the second.

Contents: When GraphQL Wins · When It Loses · The Honest Cost Ledger · Strangler Migration · Do Not Transliterate · Wrapping REST · Coexistence · BFF Versus One Graph · Team Readiness · Rolling Back · Traps

## When GraphQL Wins

| Signal | Why |
|---|---|
| Many client surfaces with different data needs | One schema serves all; no per-client endpoint proliferation |
| Deeply linked data the UI traverses | One round trip replaces a waterfall of dependent REST calls |
| Mobile clients on slow links | Selecting fields removes real bytes; a waterfall removes real seconds |
| Frontend teams blocked on backend endpoint work | The composition moves to the client team |
| A schema several teams contribute to | Federation gives autonomy with one client-facing contract (`federation.md`) |

## When It Loses

| Signal | Better |
|---|---|
| One client, endpoints shaped by that client | REST or RPC; the graph adds a layer and buys nothing |
| Bulk export, file download, streaming bytes | HTTP with ranges and content types; GraphQL responses are JSON documents |
| Simple CRUD over a handful of tables | REST plus a generated client; the flexibility is unused overhead |
| Caching public, mostly-read content is the priority | REST caches at the CDN for free; GraphQL needs deliberate work (`caching.md`) |
| Public API for unknown developers | Every client can compose an expensive query — the cost-limiting problem is permanent (`security.md`) |
| The team has no capacity for cost limits, telemetry and schema checks | The prerequisites are not optional; without them GraphQL is a liability |

- The strongest honest signal in the "loses" column: nobody is asking for flexibility. If every client wants the same data, an endpoint returning it is faster to build and to serve.

## The Honest Cost Ledger

What you pay, once, regardless of framework:

- Cost limits and rate limiting by cost, or trusted documents (`security.md`).
- Per-field authorization discipline (`authorization.md`).
- Batching discipline on every relation field, forever (`n-plus-one.md`).
- A caching strategy you build, instead of HTTP caching you inherit (`caching.md`).
- Schema checks and usage telemetry, or you never remove anything (`schema-evolution.md`).
- Codegen wired into both builds (`codegen.md`).

None is exotic and all six must exist before the first external client. A GraphQL endpoint missing three of them is worse than the REST API it replaced.

## Strangler Migration

The pattern that works, in order:

1. Stand the GraphQL endpoint up beside REST. Nothing is removed, nothing is deprecated, no rewrite is scheduled.
2. Pick one screen with a real waterfall — three or more dependent REST calls. Migrate exactly that screen and measure round trips and bytes before and after.
3. Model that screen's slice of the domain properly: entities, edges, connections. Not one field per REST endpoint.
4. Repeat per screen. The schema grows outward from real usage instead of being designed in one sitting against an imagined client.
5. Only after several screens: consider retiring the REST endpoints that no longer have callers, using the same usage-telemetry discipline as field removal (`schema-evolution.md`).

- Never start with "port the whole API". The result is a transliteration nobody can improve later, because every field has a client.
- Never start with the hardest domain. Start where the waterfall is visible, so the first migration produces a number you can show.

## Do Not Transliterate

The failure mode, concretely:

```graphql
# transliterated REST — one root field per endpoint
type Query { getUser(id: ID!): User, getUserPosts(userId: ID!): [Post!]!, getPostComments(postId: ID!): [Comment!]! }

# a graph — entry points plus edges
type Query { viewer: User, user(id: ID!): User, node(id: ID!): Node }
type User { posts(first: Int, after: String): PostConnection! }
type Post { comments(first: Int, after: String): CommentConnection! }
```

- Symptoms of a transliterated schema: `getX` field names, ids as arguments where an edge belongs, no connections, parallel `user` and `userId` fields, one root field per former endpoint (`schema.md`).
- The cost is that clients still make N calls, now through one endpoint with more ceremony. Every benefit in the "wins" table depends on traversal, which a transliterated schema does not offer.
- Root fields are entry points, and there should be few: `viewer`, a lookup per major entity, search, `node`. Everything else is reached by traversal.
- Test: can a client render the screen in one operation? If not, the edges are missing.

## Wrapping REST

- A resolver calling an internal REST service is a normal, permanent architecture — not a transitional hack. The graph is the composition layer; the services stay as they are.
- Every wrapped call needs the same batching discipline as a database: N HTTP calls to a peer service is an N+1 with worse constants and no SQL log to catch it (`n-plus-one.md`). If the peer has no batch endpoint, that is the first thing to ask for.
- Latency adds per hop and per level of nesting. A three-level tree over three services is three sequential round trips at best (`performance.md`).
- Map upstream failures deliberately: a 404 becomes null, a 403 becomes a permission decision, a 500 becomes a masked error. Leaking an upstream status code into `extensions` tells clients about services they should not know exist (`errors.md`).
- Set a timeout per upstream call, strictly below the operation timeout (`production.md`). One slow dependency otherwise consumes the whole budget.
- Do not auto-generate a schema from OpenAPI and ship it. It produces a transliteration with more types and no edges.

## Coexistence

- Run both indefinitely. There is no requirement to remove REST, and "we must finish the migration" is what produces rushed, badly-modelled schema.
- Keep one source of truth for business rules: a service layer both entry points call. Two implementations of the same rule diverge within a quarter (`resolvers.md`).
- Auth must be identical across both. Two authorization implementations is the way one of them ends up weaker (`authorization.md`).
- Some things stay REST forever and should: file upload and download, webhooks you receive, health checks, OAuth callbacks, anything a third party must integrate with using standard tooling.
- Publish which surface is canonical for each capability, or internal clients pick at random and you maintain both paths for everything.

## BFF Versus One Graph

| Model | Owner | Buys | Costs |
|---|---|---|---|
| One shared graph | A platform team, or federated teams | One contract, one place to optimize | Cross-team negotiation on every change |
| BFF per client surface | Each client team | Zero negotiation, screen-shaped schemas | Duplicated resolvers and rules across BFFs |
| Federated graph | Teams own subgraphs | Autonomy plus one client contract | Query planning, composition in the deploy path (`federation.md`) |

- A BFF is the right first step when one client team wants to move now and the organization is not ready for a shared schema. It is also the easiest thing to consolidate later, because each BFF documents exactly what one surface needs.
- The failure mode of BFFs is business logic migrating into them. Keep them composition-only.

## Team Readiness

- Someone must own the schema. Without an owner, the schema becomes the union of every PR and no two types agree on conventions.
- Schema review must be a real gate with a written convention document, or the naming, nullability and pagination decisions in `schema.md` get made independently forty times.
- Client teams need codegen wired in from the first screen, not later — retrofitting types onto hand-written documents is a project of its own (`codegen.md`).
- Budget for the operational prerequisites in the ledger above *before* the first external client, not after the first incident.

## Rolling Back

- The reversible position is coexistence: REST endpoints still deployed, still tested, still monitored. Rolling back one screen is then a client deploy.
- Deleting the REST endpoints early is what makes the decision irreversible. Keep them until the GraphQL path has survived a peak season.
- If GraphQL is being abandoned, do it by surface, in the same strangler order in reverse, and keep the schema serving until usage telemetry shows zero.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Porting the whole REST API at once | Produces a transliteration every client then depends on | Strangle one waterfall screen at a time |
| One root field per former endpoint | Clients still make N calls, with more ceremony | Few entry points, edges for traversal |
| Generating the schema from OpenAPI | More types, no edges, no design | Model the domain by hand from real screens |
| Wrapping REST without batching | N+1 with network latency, invisible in SQL logs | Batch loaders per upstream; ask for batch endpoints |
| Duplicating business rules in resolvers | Two implementations diverge within a quarter | One service layer both entry points call |
| Leaking upstream status codes to clients | Exposes internal topology | Map to domain errors and masked failures |
| Adopting GraphQL with no cost limits or telemetry | Worse than the REST API it replaced | The six-item ledger before the first external client |
| Deleting REST endpoints early | Removes the rollback | Coexist until the graph has survived peak load |
