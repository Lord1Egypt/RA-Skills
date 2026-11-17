---
name: graphql
slug: graphql
version: 1.0.2
description: >-
  Designs, debugs, and hardens GraphQL schemas, resolvers, and clients: N+1 batching, nullability, cost limits,
  subscriptions, federation. Use when writing or reviewing a schema, SDL, or resolvers; when a query is slow or fires
  hundreds of database queries; when the response says "Cannot return null for non-nullable field", comes back with an
  errors array, or nulls a whole branch; when designing mutations, cursor pagination, custom scalars, unions, or input
  types; when an Apollo, Relay, or urql cache will not update after a mutation; when subscriptions drop or never fire;
  when adding depth, alias, complexity, or persisted-query limits, disabling introspection, or masking errors; when a
  schema change breaks clients; or when composing Apollo Federation subgraphs and entity references. Not for consuming
  someone else's GraphQL API (api) or for designing REST endpoints (rest-api).
homepage: https://clawic.com/skills/graphql
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: 💠
    os:
    - linux
    - darwin
    - win32
    displayName: GraphQL
    configPaths:
    - ~/Clawic/data/graphql/
---

User preferences and memory live in `~/Clawic/data/graphql/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/graphql/` or `~/clawic/graphql/`), move it to `~/Clawic/data/graphql/`.

## When To Use

- Writing or reviewing a schema, SDL, resolvers, mutations, or a Relay-style connection
- Diagnosing GraphQL-specific failures: N+1 query storms, non-null propagation blanking a response, partial data with errors, caches that never update
- Hardening a public or partner endpoint: depth, alias, token and complexity limits, trusted documents, introspection policy, error masking
- Evolving a live schema without breaking clients: deprecation, breaking-change checks in CI, field usage telemetry
- Splitting or composing a graph: federation subgraphs, entity keys, reference resolvers
- Not for calling somebody else's GraphQL API (their rate limits, their cursors, their auth) — that is `api`; not for REST resource design — that is `rest-api`

## Quick Reference

| Situation | Play |
|---|---|
| One list query fires hundreds of SQL statements | A per-request DataLoader on every relation field (→ `n-plus-one.md`), never a module-level loader |
| `Cannot return null for non-nullable field X.y` | The resolver returned null or threw; the error climbs to the nearest nullable ancestor (→ Null Propagation) |
| Response has `data` AND `errors` | Normal. Branch on `errors[].extensions.code`, never on the message (→ Error Codes, `errors.md`) |
| Whole response is `data: null` | Every ancestor up to the root field was non-null — make one of them nullable (→ Null Propagation) |
| Designing a list field | Relay connection with `first`/`after`, capped at `max_page_size` (→ `pagination.md`) |
| Designing a mutation | `<Verb><Entity>Input` in, payload with the modified entity plus typed user errors out (→ `mutations.md`) |
| Public endpoint, unknown clients | Trusted documents first, cost limits second (→ `security.md`, Cost Model) |
| Deciding who may see a field | Enforce inside the resolver on the loaded row, not at the gateway (→ `authorization.md`) |
| Apollo/Relay cache stale after a mutation | The payload lacks `id` + `__typename`, or the change was a list insert (→ `client.md`) |
| Subscription never fires, or fires once and dies | Protocol mismatch, single-instance pub/sub, or expired connection token (→ `subscriptions.md`) |
| `PersistedQueryNotFound` in a loop | APQ hash mismatch between client, server and CDN (→ `caching.md`) |
| Same entity resolved by two services | Federation entity keys and reference resolvers (→ `federation.md`) |
| Schema change about to ship | Run the breaking-change matrix and a check against recorded operations (→ `schema-evolution.md`) |
| Types drifting from the schema | Generate them; never hand-write resolver or operation types (→ `codegen.md`) |
| "Should this be GraphQL at all" | Cost-benefit against a REST or BFF baseline (→ `rest-migration.md`) |
| Anything else | Reproduce with the smallest document that still fails, then delete one field at a time until it passes — the field you deleted names the file to open |

Depth on demand: `debug.md` symptom→cause chains · `schema.md` type design · `resolvers.md` execution and context · `n-plus-one.md` batching · `pagination.md` connections and cursors · `mutations.md` writes and uploads · `errors.md` failure modelling · `authorization.md` access control · `security.md` DoS and disclosure · `performance.md` cost and latency · `caching.md` HTTP, CDN, APQ, entity cache · `subscriptions.md` realtime · `federation.md` multi-service graphs · `client.md` Apollo, Relay, urql · `codegen.md` typed schema and operations · `testing.md` tests that catch real regressions · `schema-evolution.md` shipping changes safely · `production.md` transport, timeouts, observability · `rest-migration.md` adoption and coexistence · `commands.md` toolkit.

## Core Rules

1. **Every field that touches a datastore goes through a per-request batch loader.** Round trips without batching for a page of N parents each exposing M relation fields: `1 + N×M`; with loaders: `1 + M`. A page of 50 posts with author and comments is 101 queries versus 3. Build loaders in the per-request context factory — a module-level loader caches one viewer's rows and serves them to the next request (→ `n-plus-one.md`).
2. **Nullable by default; non-null only where the value cannot fail.** `String!` is a promise about your worst day, not your happy path. A non-null field that resolves to null nulls its nearest nullable ancestor, and `[Post!]!` turns one bad row into a nulled branch (→ Null Propagation).
3. **Every list field is paginated and capped.** Reject `first > max_page_size` (default 100) with a `BAD_USER_INPUT` error inside the resolver; clamping without saying so is only safe when clients terminate on `pageInfo.hasNextPage` rather than on how many items came back. An uncapped list argument is the cheapest denial of service a schema can offer.
4. **Limit before you parse, then again after.** Depth and complexity are validation rules that run on an already-parsed AST — a multi-megabyte document of nested braces exhausts memory in `parse()` before any of them execute. Ordered pipeline: body-size cap → token cap → parse → depth/alias/directive/complexity validation → execute (→ Cost Model).
5. **Mutations return the modified entity, never `Boolean`.** Payload shape: the entity (so a normalized client cache updates itself from `__typename` + `id`) plus a typed list of user errors. `deleteX: Boolean` forces every client into a blind refetch (→ `mutations.md`).
6. **Mutation root fields run serially, query root fields do not.** The spec guarantees document-order execution for top-level mutation selections only; sibling query fields may run in any order and concurrently. Never encode a sequence in a query, and never let a mutation's second root field depend on the first unless both are top-level siblings.
7. **Recoverable failures are data; unexpected failures are the errors array.** "Email already taken", "not found", "this row is not yours" → typed payload or result union, so clients handle them at compile time. Bugs, timeouts and downstream outages → throw, and let the errors array carry them (→ `errors.md`).
8. **Mask errors in production and branch on `extensions.code`.** The message is prose and changes without notice; the code is the contract. Stack traces, SQL fragments and the validator's "Did you mean" suggestions are schema disclosure on a public endpoint (→ `security.md`).
9. **Deprecate on a clock set by your slowest client, remove on evidence.** `@deprecated(reason: "Use X")` hides nothing and blocks nothing; removal is safe only after `deprecation_window_days` (default 90, floored by `slowest_client_cycle_days`) with zero operations selecting the field in usage telemetry over that same period (→ `schema-evolution.md`).

## Null Propagation

The most misread behaviour in GraphQL. A field error nulls the field; if that field is non-null, the error climbs to the nearest **nullable** ancestor and nulls that instead. It never stops at a non-null boundary.

| Declaration | Resolver returns null or throws | Result |
|---|---|---|
| `author: User` | null | `author: null`, one entry in `errors` |
| `author: User!` | null | The parent object becomes null; `errors[].path` still points at `author` |
| `posts: [Post!]!`, one element fails | element error | The whole list becomes null, then climbs to the parent |
| `posts: [Post]!`, one element fails | element error | That slot becomes null; the rest of the list survives |
| Non-null chain all the way up to a non-null root field | anything fails | `data: null` — the entire response is discarded |

- Design consequence: non-null is for values the resolver cannot fail to produce (a `NOT NULL` column, a computed value). Anything crossing a network boundary is nullable.
- Null holes (`[Post]`) push a null check into every client loop. Prefer filtering failed elements server-side and reporting the count in `extensions` over shipping holes.
- Client-controlled nullability and semantic-non-null are active community proposals, not ratified spec — do not design as if the escape hatch exists (→ Where Experts Disagree).

## Error Codes

`extensions.code` is the machine-readable contract. The codes common servers emit, and the first move for each:

| Code | Meaning | First move |
|---|---|---|
| `GRAPHQL_PARSE_FAILED` | Document is not valid GraphQL | Client bug, usually a query assembled by string concatenation |
| `GRAPHQL_VALIDATION_FAILED` | Valid syntax, wrong against this schema | Client and server drifted — regenerate operations (`codegen.md`) |
| `BAD_USER_INPUT` | Arguments parsed, business validation failed | Fix the input; if this outcome is routine, model it as data instead (rule 7) |
| `UNAUTHENTICATED` | Missing or invalid credentials | Transport-level auth, before resolvers run |
| `FORBIDDEN` | Authenticated but not permitted | Per-row check in the resolver; choose null-versus-error deliberately (`authorization.md`) |
| `PERSISTED_QUERY_NOT_FOUND` | APQ hash unknown to this server | Expected once per new document; a loop means a hashing or CDN mismatch (`caching.md`) |
| `INTERNAL_SERVER_ERROR` | Masked unexpected failure | Correlate by request or trace id in server logs, never by message text |

- Transport status is orthogonal: a completely failed execution is still commonly HTTP 200 with an `errors` array. A client that only checks `response.ok` misses every field error.
- Define your own codes as a closed enum shared with clients. Free-form code strings end up as unparseable as messages.

## Cost Model

Static cost estimate for a document, computed before execution:

```
cost(field) = own_cost + multiplier × Σ cost(children)
multiplier  = the field's page-size argument (first / last / limit), default 1 for non-list fields
```

Worked example with `own_cost = 1` for every field:

```graphql
query { users(first: 50) { name posts(first: 20) { title comments(first: 10) { body } } } }
```

`comments` = 1 + 10×1 = 11 · `posts` = 1 + 20×(1 + 11) = 241 · `users` = 1 + 50×(1 + 241) = 12101. Three levels with polite-looking page sizes costs twelve thousand units — which is why a depth limit alone stops nothing.

- Calibrate the budget from your own traffic: score every operation in the registry or a week of logs, take the highest legitimate score, set the ceiling above it. A round number picked by taste either rejects real clients or admits the attack.
- Aliases multiply breadth at constant depth: `a: users(first:100){…} b: users(first:100){…}` repeated 50 times is one shallow, cheap-looking document. Cap aliases and total tokens alongside depth.
- Cost is an estimate; latency is truth. Pair the limiter with a per-request timeout (`production.md`) so a cheap-scoring but slow document still dies.

## Output Gates

Before emitting a schema, resolver, or client operation, verify:

- Every list field paginated and capped at `max_page_size`, and non-null used only where the resolver cannot fail — no `[T!]!` over a partially-failable source?
- Every relation field resolved through a loader constructed per request?
- Mutations named `<verb><Entity>`, taking one `Input`, returning the modified entity plus typed user errors?
- Authorization enforced on the loaded row inside the resolver, not by operation name at the edge?
- Cost defenses on — token cap, depth, alias cap, and either a complexity budget or a trusted-document allowlist — plus error masking with a stable `extensions.code` for every failure a client must handle?
- Schema change run through the breaking-change matrix (`schema-evolution.md`) before it merges?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/graphql/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| server_impl | apollo-server \| graphql-yoga \| mercurius \| graphql-js \| gqlgen \| strawberry \| other | apollo-server | Selects the server API in every example: plugin names, context factory, error-formatting hook |
| client_library | apollo \| relay \| urql \| tanstack \| none | apollo | Shapes all client examples: cache configuration, fetch policies, pagination helpers in `client.md` |
| schema_style | schema-first \| code-first | schema-first | Whether guidance is written as SDL or as builder code, and which direction `codegen.md` generates |
| pagination_style | relay-connection \| offset \| simple-list | relay-connection | The shape of every list field emitted, and which section of `pagination.md` applies |
| max_page_size | number (1-1000) | 100 | The cap enforced on `first`/`last`/`limit` in resolvers, and the multiplier ceiling in the Cost Model |
| error_style | errors-array \| union-results | errors-array | Whether recoverable failures become a result union or a payload `userErrors` list (rule 7, `errors.md`) |
| dos_defense | cost-limits \| trusted-documents \| both | cost-limits | Which hardening `security.md` applies first, and whether clients must register documents before deploy |
| introspection_in_prod | on \| off \| authenticated | off | Whether production examples disable `__schema`, and whether field suggestions are blocked with it |
| deprecation_window_days | number (0-365) | 90 | How long a `@deprecated` field must show zero usage before removal is proposed (rule 9) |
| slowest_client_cycle_days | number (0-1095) | 90 | The release cycle of the slowest client surface (web bundle, mobile build, partner integration): floors `deprecation_window_days` and sets the minimum period usage telemetry must cover before a removal (`schema-evolution.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling**: schema registry and check tool (rover, GraphQL Hive, graphql-inspector), linter (graphql-eslint), gateway (Apollo Router, Cosmo, Mesh, none) — affects `schema-evolution.md`, `federation.md`, and the CI examples
- **Conventions**: mutation naming, input and payload suffixes, enum casing, `edges` versus a `nodes` shortcut, global Relay IDs versus type-scoped IDs — affects every schema snippet
- **Platform**: runtime and deployment target (long-lived server, serverless, edge), realtime transport (WebSocket, SSE, polling), datastore and ORM — affects `subscriptions.md`, `production.md`, and the batching examples
- **Limits**: the calibrated ceilings themselves once measured from the operation registry — max depth, alias cap, token cap, complexity budget, response-size ceiling, and the per-layer timeout budget (resolver < request < proxy) — recorded as each is calibrated and reused instead of a round number; affects rule 4, Cost Model, `security.md`, `production.md`, and the limit tests in `testing.md`
- **Safety posture**: how aggressively to surface hardening (masking, introspection, limits) unprompted, and whether destructive schema changes need explicit confirmation before being written
- **Output format**: SDL only versus SDL plus resolver code, whether generated types accompany every snippet, explanation depth
- **Work order**: schema reviewed and agreed before resolvers are written, or both landing together
- **Cadence**: release cadence per client surface (web bundle, mobile build, partner integration) behind `slowest_client_cycle_days`, and how often the schema check, registry or log sampling, and usage review run — affects the deprecation loop and the CI examples in `schema-evolution.md`
- **Constraints**: federation forbidden, offset pagination mandated by legacy clients, fields that must never appear in operation logs or traces

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| One DataLoader shared across requests | Its cache is keyed by id with no viewer or tenant dimension — request B reads the row loaded for request A | Construct loaders in the per-request context factory (`n-plus-one.md`) |
| Non-null everywhere "for better types" | One flaky downstream field nulls its whole ancestor chain, up to `data: null` | Non-null only where the resolver cannot fail (rule 2) |
| Depth limit as the DoS defense | Aliases and page-size arguments blow up breadth at depth 2 | Token, alias and complexity budgets, or trusted documents (Cost Model) |
| Authorization by operation name at the gateway | Aliases, fragments and `node(id:)` reach the same field under other names | Check the loaded row inside the resolver (`authorization.md`) |
| `totalCount: Int!` on every connection | Forces a `COUNT(*)` on every page of every list, routinely costlier than the page itself | Nullable and opt-in, or an estimate that says it is one (`pagination.md`) |
| `Int` for millisecond timestamps or large counters | GraphQL `Int` is signed 32-bit: above 2147483647 serialization raises a field error | `String` or a custom scalar with a declared format; `Float` trades the error for lost precision (`schema.md`) |
| Custom scalar implementing only `serialize` | Inputs stay unvalidated — `parseValue` and `parseLiteral` are what guard the write path | Implement all three and test the literal path; variables and inline literals take different code paths |
| Business validation thrown into the errors array | Clients end up parsing message strings, so every wording change is a silent breaking change | Model it as data (rule 7), or a closed `extensions.code` enum |
| Mutation adds to a list, cache expected to catch up | A normalized cache updates entities it can identify; it cannot know a new node belongs in a list it already holds | Return the modified list or edge, or write an explicit cache update (`client.md`) |
| Introspection disabled, suggestions left on | Errors like "Did you mean `passwordHash`?" rebuild the schema field by field | Disable both together (`security.md`) |
| Resolver awaiting inside a loop over parents | Serializes what the executor would have run concurrently, on top of the N+1 | Batch through the loader; if one query can serve the whole tree, project from `info` (`resolvers.md`) |

## Where Experts Disagree

- **Errors as data versus the errors array.** Result unions give clients exhaustive typed handling of every recoverable outcome; they also multiply schema surface and force fragment spreads at every call site. Default: unions for mutations with real business outcomes, errors array for reads and for anything unexpected. The line moves with `error_style`.
- **Introspection off in production.** One camp calls it theater — the schema leaks through suggestions, error messages and your own client bundles. The other treats it as one cheap layer that raises the cost of automated scanning. Both agree it is worthless alone: disable it only together with field suggestions and a document allowlist.
- **Cost analysis versus trusted documents.** Allowlisting registered operations makes arbitrary-query DoS structurally impossible, and is available whenever you control every client. Cost limits are the only option for a public or partner API. Running both is normal; running neither on a public endpoint is not defensible.
- **Federation versus a single schema.** Federation buys team autonomy and pays in query planning, cross-subgraph batching and a composition step that can fail your deploy. The trigger is organizational — separately deployed teams owning disjoint entities — not graph size (`federation.md`).
- **Code-first versus schema-first.** Code-first keeps types and resolvers together and cannot drift; schema-first keeps the contract reviewable by people who do not read your server language, which is what makes design review real. Pick per service, record it in `schema_style`, never mix inside one service.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/graphql (install if the user confirms):
- `api` — consuming somebody else's GraphQL or REST API
- `rest-api` — designing and building REST endpoints
- `authorization` — the policy models behind field-level checks
- `websocket` — the transport underneath subscriptions

## Feedback

- If useful, star it: https://clawic.com/skills/graphql
- Latest version: https://clawic.com/skills/graphql

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/graphql.
