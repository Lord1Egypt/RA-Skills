# Production — Transport, Timeouts, And Knowing What Ran

Everything a GraphQL endpoint needs that is not schema design: the HTTP contract, the limits that must be on before it faces traffic, and the telemetry that makes an incident answerable. Hardening rationale lives in `security.md`; this is the operational surface.

Contents: The HTTP Contract · Deploy Checklist · Timeouts And Cancellation · Observability · Logging · Health And Readiness · Rollout · Incident Playbook · Multi-Client Operation · Traps

## The HTTP Contract

- One endpoint, `POST` for everything, `GET` for queries only. A `GET` that executes a mutation is triggerable by an image tag.
- Accept `application/json` bodies. Reject `text/plain` and form encodings — they are simple requests that skip preflight and reopen CSRF (`security.md`).
- The GraphQL-over-HTTP media type `application/graphql-response+json` is what a spec-compliant client negotiates; servers commonly still answer `application/json`. Support both on the way in, and do not build client logic that depends on which comes back.
- Status codes: a field error ships with HTTP 200 and an `errors` array; a request-level failure (parse, validation, limit) is a 4xx in modern servers and was a 200 in older ones. Clients must handle both (`errors.md`).
- Array-body batching multiplies every per-request limit by the array length. Off by default is the right default; if on, cap the array and sum the costs.
- Require an operation name on every request in production and reject anonymous operations. Without it, every telemetry view is unusable.
- Require a client identity header (name plus version) and reject requests without it. It costs one client change and is what makes deprecation decisions possible (`schema-evolution.md`).

## Deploy Checklist

Before an endpoint takes external traffic:

- Errors masked; stack traces and SQL absent from responses; field suggestions disabled with introspection (`security.md`).
- Token, depth, alias, directive and complexity limits on, calibrated against real operations, and logged when they fire.
- Per-request timeout set, below every proxy timeout in front of it.
- Body size capped at the proxy, before the parser.
- Parsed-document cache on and bounded; schema built once at startup.
- Trusted documents or APQ configured, with a registry shared across instances (`caching.md`).
- Cost-based rate limiting keyed per client, sensitive mutations on their own bucket.
- Operation name and client identity required; unnamed operations rejected.
- Tracing sampled, per-operation metrics always on.
- Loaders constructed per request — grep for module-scope loader construction one more time (SKILL.md rule 1).

## Timeouts And Cancellation

- GraphQL has no built-in per-operation timeout. Without one, a query the cost limiter approved can hold a connection until the proxy kills it — and the resolvers keep running after the client is gone.
- Set the layered budget so each layer is strictly smaller than the one in front: client < load balancer < server operation < individual resolver. Inverted, the outer layer kills the request while the inner one keeps working, and you get load with no observable requests.
- Put an abort signal on the context and honor it in every I/O call. Without it, cancellation is decorative: the executor stops caring about the result and the database still runs the query.
- Database statement timeouts are the backstop that always works, because they are enforced where the work happens.
- Under a retry storm, uncancelled work is the amplifier: every abandoned request still costs full server and database time while the client is already retrying.

## Observability

- Per-operation, always on: request rate, p50/p95/p99 latency, error rate by code, statement count, rows loaded, response bytes. Keyed by operation name and client.
- Per-field, sampled: a span per resolver. This is the only view that attributes latency to a field path (`performance.md`). Full tracing on every request is itself load.
- Field usage counters, always on, aggregated coarsely: which fields each client selects, and how often. Drives deprecation and reveals expensive fields nobody wants (`schema-evolution.md`).
- Limit rejections as a first-class metric, split by which limit fired. A limiter nobody watches is discovered by a customer.
- Alert on error rate *by code and by field path*, not on total errors: a 100% failure rate on one field is invisible inside an aggregate of 0.3%.
- Cache hit rates per layer — entity cache, document cache, CDN. A hit rate that quietly drops to zero after a deploy is a common and otherwise silent regression.

## Logging

- One structured line per operation: request id, operation name, client name and version, viewer id, duration, statement count, bytes, error codes. That single line answers most incident questions without a trace.
- Log variable *keys*, never variable values — they carry passwords, tokens, and personal data. Redact by allowlist, not by denylist.
- Never log the full document at info level in production: with persisted queries you have a hash that is smaller and stable; without them, documents are large and repetitive.
- Log each error once, where it is formatted, not at every level it passes. Duplicate lines make error-rate graphs meaningless.
- The request id belongs in `extensions` on every error response and in every server log line, so a user's screenshot resolves to a trace (`errors.md`).

## Health And Readiness

- Liveness: the process answers. Do not put a database query behind it or a database blip restarts every instance.
- Readiness: the schema is built, the registry manifest is loaded, and dependencies are reachable. An instance that starts serving before its APQ manifest loads produces a burst of `PersistedQueryNotFound`.
- Health checks must not run a real GraphQL operation against real data — that is a public, unauthenticated execution path. Use a trivial `{ __typename }` at most.
- In a federated graph every subgraph needs its own reachable health check; a gateway-only view hides which service is failing (`federation.md`).

## Rollout

- Schema changes and code deploy together, but their *safe order* differs: additive changes go schema-then-usage; removals go remove-usage-then-schema (`schema-evolution.md`).
- Publish the trusted-document or APQ manifest before the client build that needs it, and keep several versions live — clients in the wild lag your deploys.
- Canary on operation-level metrics, not on overall error rate: a change that breaks one operation is invisible in an aggregate.
- Rolling deploys disconnect every subscription in waves. Stagger instances and jitter client reconnect backoff or the reconnect storm becomes the outage (`subscriptions.md`).
- Keep a rollback that is a deploy of the previous artifact, and verify the previous schema is still compatible with the manifests currently live.

## Incident Playbook

| Symptom | First move |
|---|---|
| Latency up across all operations | Database or pool saturation; check statement count per operation, not resolver code |
| Latency up on one operation | Per-field trace on that operation; look for a missing loader or a lost index |
| Error rate up with one code | Group by field path — one field, one dependency |
| `PersistedQueryNotFound` spike | Instances not sharing the registry, or a manifest that did not deploy (`debug.md`) |
| Limit rejections spike | A client shipped a bigger document; compare against the registry before raising the limit |
| Memory climbing on one instance | Unbounded document cache, subscription buffers, or a module-scope cache with no eviction |
| One user reports another user's data | Stop. Module-scope loader or a shared cache without a viewer key. Highest severity (`debug.md`) |

- Kill switches worth having ready: disable introspection, tighten the complexity ceiling, disable a specific expensive field (return null with a code), and reject a specific client version.
- Field-level kill switches beat endpoint-level ones: turning off one expensive field degrades a screen; turning off the endpoint stops the product.

## Multi-Client Operation

- Web bundles redeploy in minutes; mobile builds live for months; partner integrations live for years. Every removal decision is bounded by the slowest of them — that bound is `slowest_client_cycle_days` (`schema-evolution.md`).
- Version the client identity and use it: telemetry per client version is what tells you the last old build finally drained.
- Keep old operation manifests for as long as their client versions are alive, or the schema checker will approve a removal that breaks a shipped app (`schema-evolution.md`).
- A partner-facing endpoint needs cost limits regardless of what your first-party clients do — you cannot allowlist documents you do not write (`security.md`).

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| No per-operation timeout | An approved query holds a connection until a proxy kills it | Layered budget, each smaller than the one outside it |
| Abort signal ignored in resolvers | Cancellation is decorative; the work continues | Honor the signal in every I/O call; database statement timeout as backstop |
| Anonymous operations allowed | Every telemetry view is unusable | Require and reject on absence |
| Logging variable values | Passwords and personal data in logs | Log keys only, redact by allowlist |
| Health check running a real query | A public unauthenticated execution path | `{ __typename }` at most |
| Alerting on total error rate | A fully broken field hides in the aggregate | Alert by code and by field path |
| Array batching left on by default | Multiplies every per-request limit | Off, or capped with summed cost |
| Manifest deployed after the client | A burst of unregistered-document failures | Publish the manifest first, keep versions live |
