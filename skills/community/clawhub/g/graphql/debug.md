# Debugging — Symptom To Cause

Work symptom-first. Each chain is ordered by probability and every step is a check, not a guess. The universal first move: get the exact document, the exact variables, and the full response including `errors` — most reports are missing one of the three, and the missing one is usually where the answer is.

Contents: The Universal First Three · Field Is Null · Cannot Return Null · data Is null · Everything Slow · Slow Only At Scale · Validation Error · Cache Not Updating · Subscription Silent · Works In Playground, Not In App · Persisted Query Loop · Federation Fetch Missing · Intermittent Nulls · Truly Stuck

## The Universal First Three

1. Read `errors[].path` and `errors[].extensions.code` — the path names the failing field, the code names the layer (SKILL.md Error Codes).
2. Reproduce with the smallest document that still fails. Delete one field at a time; the field whose removal fixes it is the subject.
3. Run the same document with a server-side trace or per-resolver timing. "Which resolver" is a fact, not a hypothesis.

## Field Is Null, No Error

The response has no `errors` entry and the field is null anyway — so no resolver threw.

1. Is there a resolver at all? With none, the executor reads `parent[fieldName]`; a spelling difference (`created_at` versus `createdAt`) returns `undefined` with no error, forever (`resolvers.md`).
2. What did the parent actually return? Log the parent object at the field's resolver. A partial parent that never loaded the property is the second cause.
3. Was the field skipped? `@skip`/`@include` remove the key entirely — `undefined`, not `null`. Check the variables you actually sent.
4. Is a permission check returning null by design? Grep the field's resolver and its loader for a viewer check (`authorization.md`).
5. Fragment on the wrong type: `... on Article { … }` where the value is a `Post` matches nothing and produces no error. Check `__typename` in the response.

## Cannot Return Null For Non-Nullable Field X.y

1. Something *did* fail — read the `errors` entry at that path, not just the message on the parent.
2. If there is no other error, the resolver returned null cleanly: same checks as above, but now with a non-null declaration turning silence into a visible failure.
3. Trace the propagation: the reported path is where the null originated, the nulled object in `data` is the nearest nullable ancestor (SKILL.md Null Propagation).
4. Decide which is wrong — the data or the schema. A field that can legitimately be absent must be nullable; a field that must exist needs the resolver fixed.
5. Common source: a list element. `[Post!]` with one bad element nulls the whole list, and the message names the element's field, not the list.

## The Whole Response Is data: null

- Every ancestor from the failing field to the root was non-null, so the error climbed all the way out. Find the single entry in `errors` and follow its `path` — the deepest segment is the actual failure.
- If there is no `errors` array either, this is a request-level failure (parse, validation, a limiter) and no resolver ran. Check the HTTP status and the response body shape.
- A root field declared non-null (`viewer: Viewer!`) is what makes this reachable at all. That declaration is why one deep failure blanks a whole page.

## Everything Is Slow

1. Count database statements for the operation. Scaling with page size = N+1 (`n-plus-one.md`).
2. Per-resolver trace: one wide span = one slow resolver; many short spans in a band = N+1; a staircase = serial depth (`performance.md`).
3. Gap between total time and the sum of resolver time = parse/validation (no document cache), serialization (huge payload), or waiting on a limiter.
4. Response size: a fast server and a slow screen is bytes, not resolvers. Measure raw payload per operation.
5. Cold path: schema built per request, or a cold serverless instance. Check whether the second identical request is fast.

## Slow Only At Scale / Only In Production

| Difference | Check |
|---|---|
| Data volume | Same operation against production-sized data locally; N+1 is invisible at 3 rows |
| Missing index | The sort or filter argument used in production but not in your test (`pagination.md`) |
| Cold caches | Entity cache and document cache empty after a deploy (`caching.md`) |
| Concurrency | Connection pool exhaustion — latency rises for everything at once, not for one field |
| Different client documents | Production clients select fields your test document does not; pull the real operation from the registry |
| Warm module scope | A leak or a stale loader that only exists on a long-lived process (`n-plus-one.md`) |

## Validation Error The Client Did Not Expect

- `GRAPHQL_VALIDATION_FAILED` means the document does not match *this* server's schema. First question: which schema version is deployed, and which one did the client generate against (`codegen.md`)?
- A field the client knows and the server rejects = the client is ahead, or the deploy rolled back.
- A field the server has and the client is told is unknown = the client is querying a different endpoint or a different subgraph than it thinks.
- Required variable missing is a client bug that typing would have caught at build time.
- If the error appeared without any client change, someone shipped a breaking schema change (`schema-evolution.md`).

## Cache Not Updating After A Mutation

Ordered by frequency; full detail in `client.md`.

1. The mutation payload lacks `id` or `__typename`.
2. The mutation returns a `Boolean` or a count — nothing to merge.
3. The change is a list insert or delete, which normalization cannot infer.
4. Query and mutation selected different fields of the same entity; the untouched field is still old.
5. The component reads through a fragment that omits the changed field.
6. Two types collide on one cache key.
7. The query used `no-cache`, or the client is urql's document cache rather than a normalized one.

## Subscription Never Fires Or Dies After One Event

1. Does the socket even connect? A crossed subprotocol (`graphql-ws` versus `graphql-transport-ws`) closes it with no useful error — check the negotiated subprotocol on both sides (`subscriptions.md`).
2. More than one server instance with an in-memory emitter: the publisher and the subscriber are on different processes. Test with one instance to confirm.
3. Fires once then stops: an error thrown in `resolve` or in the client's handler tore down the stream.
4. Works for minutes then stops: token expiry closing the connection, an idle proxy timeout, or missing pings.
5. Fires for some users only: the filter predicate, or an authorization check evaluated per event.
6. Nothing after a deploy: clients did not resubscribe on reconnect.

## Works In The Playground, Fails In The App

| Difference | Check |
|---|---|
| Auth | The playground carries your session cookie or a dev token; the app sends a header |
| CORS / preflight | The app is cross-origin and the preflight is rejected (`security.md`) |
| Content type | The app sends something other than `application/json` and the server rejects it |
| Variables | The playground has them typed; the app sends a string where an `Int` is expected |
| Persisted queries | The app sends a hash the server does not know (`caching.md`) |
| Document | The app's document includes a fragment or field the playground copy does not |
| Limits | The app's real document exceeds a depth or complexity limit the hand-typed one does not |

## Persisted Query Loop

`PersistedQueryNotFound` repeating forever instead of once:

1. Client and server disagree on the hash — a whitespace or codegen change alters the document text. Log both hashes once.
2. Instances do not share the APQ registry, so each new instance re-learns; a scale-out event makes it constant.
3. A CDN cached the negative response, so the retry never reaches the server.
4. The client's retry sends the full document without the hash extension, so nothing ever registers.
5. Trusted documents (not APQ) reject unregistered documents on purpose — the manifest was not published before the client deployed (`security.md`).

## Federation: A Field Comes Back Null Across A Boundary

1. Read the query plan for the operation. The missing fetch step or the extra one is usually visible immediately.
2. Reference resolver returned null: the entity was deleted, or the key it received is not the key it queries by.
3. The reference resolver read a non-key field that happened to be present in another plan and is absent in this one (`federation.md`).
4. `@provides` promised a field this path does not actually resolve.
5. Composition succeeded with mismatched nullability, and the stricter side is nulling the parent.

## Intermittent Nulls Or Wrong Data For Some Users

Treat as a data-isolation bug until proven otherwise; this is the highest-severity chain here.

1. Is any loader, cache or client constructed at module scope? On a warm process it is shared across requests (SKILL.md rule 1).
2. Does any loader cache key omit the viewer or the tenant (`authorization.md`)?
3. Is a response with private fields reaching a shared cache or a CDN (`caching.md`)?
4. In subscriptions: a loader created in the connection context serves the first event's data forever (`subscriptions.md`).
5. Reproduce deliberately: two viewers, sequential requests, same process. If viewer B sees A's data once, stop and fix before anything else on this page.

## When You Are Truly Stuck

Strip to nothing and add back. Execute `{ __typename }` against the schema with a minimal context — that proves the transport, the auth and the executor. Then add one field, one fragment, one variable at a time until it breaks. The addition that breaks it names the subsystem and the file above to open.
