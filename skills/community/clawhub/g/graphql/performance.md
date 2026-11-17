# Performance — Latency, Payload, And The Cost Of A Shape

Batching is the first fix and has its own file (`n-plus-one.md`); caching is the second and has another (`caching.md`). What is left is where GraphQL-specific latency actually comes from: per-request compilation, tree depth, payload size, and the parts of the response the client is waiting on but does not need yet.

Contents: Where The Time Goes · Parse And Validate · Depth Is Latency · Response Size · @defer And @stream · Selective Work · Serverless And Edge · Measuring · Load Testing · Traps

## Where The Time Goes

Profile before optimizing; the order of suspicion for a slow operation:

1. N+1 round trips — statement count scaling with page size (`n-plus-one.md`).
2. One genuinely slow resolver — one wide span in the trace, everything else short.
3. Serial depth — nothing is slow, but three levels of 40 ms cannot overlap.
4. Payload size — the server finished in 60 ms and the client rendered at 900 ms.
5. Parse and validation — visible only at high request rates or with very large documents.

- Attribute time per *field path*, not per operation. An operation is a composite; the fix lives at one path.
- Server timing and client-perceived timing diverge over cellular links: a 400 KB response is fast in your office and slow everywhere else.

## Parse And Validate

- Every request without persisted documents pays parse plus validation before a single resolver runs. Validation cost grows with document size and schema size, and is entirely repeated work for a document you have already seen a thousand times.
- Cache the parsed-and-validated document keyed by its hash. Most mature servers do this; verify yours does rather than assuming, and check the cache is bounded so a flood of unique documents cannot grow it without limit.
- Persisted queries or trusted documents remove the problem at the source: the server holds the document, the client sends a hash (`caching.md`, `security.md`).
- Schema construction is startup work, not request work. Building the schema per request — easy to do accidentally in serverless handlers — dominates everything else on this page.

## Depth Is Latency

- Children resolve only after their parent, so a chain of dependent fields adds latency: three levels at 40 ms is 120 ms of irreducible serial time no matter how well each level batches.
- Sibling fields overlap; nested ones do not. Restructuring a query so two independent branches sit side by side at the root turns serial time into parallel time with no server change.
- Cross-service depth is the expensive version: each level is a network hop plus its own serialization. Federation adds one per subgraph boundary crossed (`federation.md`).
- The flattening lever is schema design: a field that returns the data a client always fetches two hops away (`post.authorName` beside `post.author.name`) removes a hop for a denormalization cost you must then keep consistent. Use it where the pattern is universal, not to paper over a badly-shaped graph.

## Response Size

- GraphQL's promise is that clients ask for less. In practice payloads grow because fragments accumulate: every component adds fields, nobody removes them, and the query used by the home screen selects 200 fields.
- Measure bytes per operation in production and alert on growth. A 10× payload regression looks like nothing in a diff — one fragment spread.
- Duplicate objects are the hidden multiplier: the same author appearing on 50 posts is serialized 50 times. Normalized clients deduplicate on receipt but the bytes already crossed the network.
- Compression is mandatory and not a strategy: gzip flatters repetitive JSON, so a badly-shaped response looks acceptable compressed and still costs parse time and memory on a phone.
- Cap the *result*, not only the query: a document scoring within budget can still return an enormous payload. A response-size ceiling that fails loudly beats an out-of-memory on a mobile client.
- Field selection is the client's lever and the server's blind spot — publish per-operation payload sizes back to client teams or nobody will trim anything.

## @defer And @stream

- `@defer` splits a slow fragment out of the initial response; `@stream` sends list items as they are produced. Both turn one response into an incremental stream over multipart or SSE.
- Both are **draft-stage additions, not part of the ratified spec**: server support varies, client support varies more, and the wire format has changed between implementations. Verify both ends before designing around them, and keep a non-incremental fallback.
- They improve *perceived* latency and never total work: the slow resolver is still slow, the user just sees the fast fields first. If the slow field is what the user came for, deferring it makes the page feel broken instead of slow.
- Errors can arrive in a later payload, after the client has rendered — the error handling path must cope with an error for a branch already on screen (`errors.md`).
- Every proxy, CDN and load balancer between you and the user must pass an incremental response through unbuffered. One buffering hop turns streaming back into a single slow response, with no error to show for it.
- Cheaper alternative that always works: split the screen into two operations, render the fast one, fire the slow one alongside.

## Selective Work

- A resolver only runs if its field is selected — that is the free half of the optimization. The other half is not doing work in the parent that only one child needs.
- Read `info` to skip an expensive join when the fields it feeds were not requested (`resolvers.md`). Keep it to a data decision; never let it change business results.
- Do not eagerly `Promise.all` a parent's fields. Returning an object whose properties are promises lets the executor await only what was selected.
- Expensive computed fields (aggregations, scores, permission-heavy checks) belong behind their own field so the cost follows the request, rather than inside a parent everyone loads.
- Cancellation: when the client disconnects, in-flight resolvers keep running unless an abort signal on the context is honored (`production.md`). Under a retry storm this is the difference between degraded and dead.

## Serverless And Edge

- Cold starts dominate: schema construction, plugin registration and codegen artifacts must all happen at module load, cached across invocations, never per request.
- Module scope persists on warm instances. That is what makes the shared-loader leak specifically dangerous here (`n-plus-one.md`).
- Connection pools do not work when every instance opens its own: use a pooler in front of the database, or an HTTP data layer.
- Subscriptions do not fit a request-scoped runtime — they need a long-lived process or a managed realtime service (`subscriptions.md`).
- Response streaming (`@defer`) needs a platform that supports streaming responses; many serverless runtimes buffer the whole body.

## Measuring

- Per-resolver tracing (an OpenTelemetry span per field, or the server's built-in tracing plugin) is the only view that attributes time to a field path. Sample it in production; full tracing on every request is itself a load.
- Track per-operation: p50/p95 latency, statement count, rows loaded, bytes returned, error rate. Operation *name* is the key — group by it, and reject unnamed operations in production so the data is usable.
- Field-level usage telemetry serves double duty: it drives deprecation decisions (`schema-evolution.md`) and shows which expensive fields nobody actually requests.
- Watch the gap between total operation time and the sum of resolver time. A large gap is parse, validation, serialization, or waiting on a limiter.

## Load Testing

- Load-test the operations your clients actually send, taken from the registry or from production logs. A synthetic "typical query" tests a shape nobody uses.
- Include the worst legitimate operation, not the average — the p99 shape is what falls over.
- Test with realistic page sizes and realistic cache states. A benchmark that hits a warm loader cache measures the loader.
- Verify the limiter under load too: a cost limiter that itself walks the AST for every request is a cost you must measure.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Optimizing resolvers before counting statements | Statement count scaling with page size is the first thing to rule out, and usually the answer | Count statements per operation first |
| Building the schema per request | Dominates every other cost | Build once at module load |
| No parsed-document cache | Every request re-parses and re-validates | Cache by document hash, bounded |
| `@defer` as the answer to a slow field | Perceived latency only; the slow field is still slow | Fix the resolver, or split into two operations |
| Judging payload by compressed size | Parse and memory on the client are uncompressed | Measure raw bytes per operation |
| Flattening the schema to reduce depth | Denormalized fields drift from their source | Restructure the query, or flatten only universal patterns |
| Tracing everything in production | The tracing is now the load | Sample, and keep per-operation aggregates always on |
| Load test built from a hand-written query | Tests a shape no client sends | Replay the operation registry |
