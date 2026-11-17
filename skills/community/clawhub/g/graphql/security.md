# Security — Denial Of Service And Disclosure

Threat model specific to GraphQL: one endpoint, one HTTP verb, and a client that composes the query. Everything a REST API bounds by route, GraphQL must bound by analysis. Access control is a separate craft — `authorization.md`.

Contents: The Layered Defense · Limits That Actually Bind · Trusted Documents · Introspection And Suggestions · CSRF And Transport · Batching Amplification · Injection · Rate Limiting By Cost · Subscriptions · Disclosure Checklist

## The Layered Defense

Ordered, because a later layer cannot protect the one before it (SKILL.md rule 4):

| Layer | Stops | Cost of skipping |
|---|---|---|
| Body size cap at the proxy | Multi-megabyte documents | Memory exhaustion before your code runs |
| Token cap before parse | `{a{a{a…` nesting bombs | `parse()` dies first; no validation rule ever runs |
| Depth limit | Recursive traversal through cyclic types | Unbounded traversal of `friends { friends { … } }` |
| Alias and directive caps | Breadth amplification at depth 2 | 1000 aliased copies of one expensive field |
| Complexity budget | Expensive-but-legal shapes | The Cost Model example: 12 101 units in three levels |
| Per-request timeout | Cheap-scoring, slow queries | A limiter that approves what your database cannot serve |
| Trusted documents | Everything above, structurally | You are relying on estimates instead of an allowlist |

- Skipping the token cap is the most common gap: teams add a depth-limit validation rule and believe they are covered, when a document large enough to kill the parser never reaches validation.
- Every limit rejects with a request-level error and no `data`. Return a distinguishable code so a legitimate client that grew too big can tell the difference from a bug.

## Limits That Actually Bind

- Calibrate from measured traffic, never from a round number: score every operation your clients actually send, take the highest legitimate value, and set the ceiling above it with headroom. Guessing produces either rejected customers or an admitted attack.
- Off-the-shelf hardening packages (GraphQL Armor and equivalents) ship intentionally tight defaults — a depth around 6 and low alias caps — which will reject legitimate documents in most real schemas. Adopt them, then raise each limit against your own operation registry rather than disabling the ones that fire.
- Introspection is itself an expensive query: the full introspection document is deeply nested by construction, and any depth limit low enough to matter will block it. Exempt it deliberately or disable it, but know which you did.
- Recursion through cyclic types is what makes depth dangerous: `user { posts { author { posts { … } } } }` is finite in the schema and unbounded in the document.
- Log every rejection with the operation name and the score. A limiter nobody monitors is discovered by a customer, not by you.

## Trusted Documents

The strongest defense available, and the one that removes the estimation problem entirely.

- Build step: extract every document from client source, hash it, publish the manifest to the server. At runtime the server accepts a hash and refuses anything unregistered — arbitrary queries become structurally impossible.
- Available whenever you control every client (first-party web and mobile). Impossible for a public or partner API, which is exactly where cost limits remain mandatory.
- Distinct from automatic persisted queries (APQ), which register on first sight for bandwidth and cacheability and therefore accept *any* document (`caching.md`). APQ is a performance feature; a trusted-document allowlist is a security control. Confusing them is common and expensive.
- Deployment ordering matters: the manifest must reach the server before the client build that uses it, and old manifests must stay valid while old app versions are in the wild. Keep several versions live.
- With an allowlist you can precompute each document's cost once at registration and reject expensive ones at build time, where a developer sees the failure.

## Introspection And Suggestions

- Disabling `__schema` and `__type` raises the cost of automated scanning and does not hide your schema: it leaks through your own client bundles, error messages, and field-name guessing.
- The suggestion leak is the part teams miss. Validation errors of the form "Cannot query field `passwordHsh` on type `User`. Did you mean `passwordHash`?" let a scanner recover the schema field by field with introspection fully off. Public tooling automates it. Disable suggestions in the same change that disables introspection, or the change is theater (SKILL.md Traps).
- `__typename` remains available even with introspection disabled in most servers — it is not part of the introspection system for this purpose. Do not rely on hiding type names.
- Authenticated introspection is a reasonable middle: partners and internal tooling keep their tooling, anonymous scanners get nothing. Recorded in `introspection_in_prod`.
- A public schema is not a vulnerability in itself. If knowing your field names is dangerous, the fix is authorization, not obscurity.

## CSRF And Transport

- A `POST` with `Content-Type: application/json` requires a preflight, so cross-origin CSRF is blocked by the browser. The holes are the content types that count as *simple* requests: `text/plain`, `application/x-www-form-urlencoded`, and `multipart/form-data`.
- A server that parses a body sent as `text/plain` is CSRF-vulnerable to any page on the internet if it authenticates with cookies. Reject non-JSON content types, or require a custom header (any header forces a preflight) on every mutating request.
- `GET` requests must execute queries only, never mutations — a `GET` that mutates is triggerable by an image tag. Servers supporting APQ over `GET` need this check explicitly.
- Prefer `Authorization` headers over cookies for GraphQL endpoints: a bearer token is not sent automatically by the browser, which removes most of the CSRF surface at the source.
- CORS is not authorization. `Access-Control-Allow-Origin: *` on an endpoint authenticated by header is fine; on one authenticated by cookie it is a hole.

## Batching Amplification

- Array-body batching (a JSON array of operations in one request) multiplies every per-request limit by the array length: rate limits, cost budgets and timeouts all apply once to what is really N operations. Servers that support it commonly default it off — leave it off unless a client needs it, then cap the array length and sum the costs.
- Aliases achieve the same amplification inside a single document and cannot be turned off, only capped.
- Mutation batching is worse than query batching: a login mutation aliased 1000 times in one document is a credential-stuffing engine that costs one HTTP request and one rate-limit token. Rate-limit sensitive mutations by *field occurrence count*, not by request.

## Injection

- GraphQL's type system stops type confusion, nothing else. A `String` argument reaching a raw SQL string, a shell command, or a NoSQL query object is exactly as dangerous as anywhere else — parameterize.
- Argument values arrive from variables *and* from inline literals in the document; a custom scalar validating only `parseValue` misses the literal path entirely (`schema.md`).
- Free-form filter or sort arguments are the common injection vector, because they are usually interpolated into a query builder. Enums for sort, closed input objects for filters.
- SSRF: any field that fetches a client-supplied URL (webhook validation, image proxy, "import from URL") needs an allowlist and must block internal ranges and cloud metadata addresses.
- Cursors are user-controlled input that lands in a `WHERE` clause. Validate and, where it matters, sign them (`pagination.md`).

## Rate Limiting By Cost

- Request counting is meaningless when one request can cost a thousand times another. Charge against the same estimate the cost limiter computes (SKILL.md Cost Model): a leaky bucket with a per-minute refill, keyed by API client rather than IP.
- Charge on the *estimate before execution*, then reconcile with measured cost afterwards if you can. Estimate-only lets a cheap-scoring slow query through; measure-only lets the expensive query run before it is charged.
- Return the budget state in `extensions` (remaining, resets at) so well-behaved clients can pace themselves instead of discovering the limit by failing.
- Separate buckets for reads and for sensitive mutations. One shared bucket means a background sync job locks a user out of logging in.

## Subscriptions

- Auth is checked at the handshake and the connection then lives for hours: a token that expires mid-connection keeps working unless you re-validate. Store the token's expiry on the connection and close the socket when it passes.
- Every open subscription is retained server-side memory plus a pub/sub subscription. Cap concurrent subscriptions per user and per connection, or one client opening thousands is a resource exhaustion with no HTTP request to rate-limit.
- Authorize each *published event* against the subscriber, not only the subscription arguments at setup time: permissions change while the socket stays open (`subscriptions.md`).
- The WebSocket handshake is not covered by CORS. Check the `Origin` header yourself in the upgrade handler.

## Disclosure Checklist

Before a GraphQL endpoint faces the internet:

- Errors masked, stack traces and SQL absent from every response?
- Field suggestions disabled together with introspection?
- Token, depth, alias, directive and complexity limits on, calibrated against real operations, and logged when they fire?
- Trusted documents in place if every client is first-party?
- Non-JSON content types rejected; `GET` restricted to queries; array batching off or capped?
- Cost-based rate limiting keyed per client, with sensitive mutations on their own bucket?
- Timing between "not found" and "not permitted" comparable?
- Subscription connections capped, re-validated against token expiry, `Origin` checked?
