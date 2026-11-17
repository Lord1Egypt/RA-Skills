# Errors — Modelling Failure Instead of Throwing It

GraphQL's default failure channel is a side array that clients must remember to read. Everything here is about deciding, per failure, whether it belongs in that array or in the schema. The dividing rule is SKILL.md rule 7.

Contents: The Three Layers · Anatomy · Data Or Errors · Result Unions · Masking · Codes · Partial Data · Errors In Lists · Logging And Correlation · Traps

## The Three Layers

| Layer | Where it shows up | HTTP status | Client handling |
|---|---|---|---|
| Transport | Network failure, 401 from a proxy, 5xx HTML from an edge | Any | Retry/backoff logic; never parseable as GraphQL |
| Request | Parse or validation failure, cost limit exceeded | 400 commonly, 200 in older servers | Bug in the client or a limit hit — never retry unchanged |
| Field | A resolver returned null or threw | 200 with `data` and `errors` | Per-field handling; the response is still usable |

- Clients that only check `response.ok` see field errors as success and render undefined. Clients that treat any `errors` entry as total failure throw away valid partial data. Both are common; both are wrong.
- Request-level failures have no `data` key at all. Field-level failures have `data` with nulls. Distinguishing them is one `'data' in response` check.

## Anatomy

```json
{ "data": { "user": { "name": "Ada", "posts": null } },
  "errors": [ { "message": "Upstream timeout",
                "path": ["user","posts"],
                "locations": [{"line":3,"column":5}],
                "extensions": { "code": "INTERNAL_SERVER_ERROR", "requestId": "01J…" } } ] }
```

- `path` is the only reliable way to know *which* field failed — indispensable when the same field appears under several parents or aliases. Clients that log only `message` cannot tell which of 50 list items failed.
- `locations` refers to the document text, which is useless in production if the client sends a persisted-query hash. Do not build tooling around it.
- `extensions` is the extension point: put the code, the request id, and (for validation) the input path there. Everything a client branches on lives here.
- Nothing in the response tells the client how many errors are "the same" error — deduplicate by `code` plus `path` prefix if you surface them to users.

## Data Or Errors

Decide per failure with these questions:

1. Will a competent client always want to handle this specific case? → data.
2. Is it an expected outcome of a correct request (already taken, out of stock, not found)? → data.
3. Would a retry with the same input reasonably succeed? → errors array (transient), and mark it as such.
4. Is it a bug, an outage, or something no client action fixes? → errors array, masked.

- "Not found" is the genuinely contested case. As data, it forces every caller to handle a `NotFound` member; as null plus an error, it is easy to ignore. Default: null for a lookup by id the client chose (they can see the null), typed data for a lookup that is part of a business flow.
- Authorization failures are a third case: returning null hides existence, returning an error confirms it. Choose per type from the threat model, then be consistent within that type or the difference becomes an oracle (`authorization.md`).

## Result Unions

```graphql
union PublishPostResult = PublishPostSuccess | PostNotFound | NotAuthorized | ValidationFailed
```

- What they buy: a generated client gets an exhaustive discriminated union, so a new failure member becomes a compile error at every call site instead of a silent fallthrough.
- What they cost: every call site needs inline fragments on every member, the schema grows a type per outcome, and adding a member is semi-breaking for exhaustive clients (`schema.md`).
- The lighter variant is the `userErrors` list in the payload (`mutations.md`): one shape everywhere, no exhaustiveness. Most teams that adopt unions do so only for mutations with real business outcomes and keep reads on nullable fields plus the errors array.
- Give every error member a shared interface (`interface UserFacingError { message: String! }`) so clients can render an unknown member instead of crashing.
- Recorded in `error_style`; a stated preference switches which shape this skill emits.

## Masking

- In production, every unexpected error becomes one generic message and one code. The unmasked original goes to your logs with the same request id. Most servers do this by default only when an environment flag says production — verify rather than assume.
- What leaks when masking is off: SQL text and table names, file paths and framework versions in stack traces, upstream hostnames, and validation "Did you mean …" suggestions that rebuild your schema field by field (`security.md`).
- Errors you throw deliberately (validation, permission) must be distinguishable from ones you did not, or masking either leaks everything or hides your own messages. The usual mechanism is a base class or a marker in `extensions` that the formatter recognizes as safe to pass through.
- Do not mask in development — a masked error during local work costs an hour and teaches nothing.
- Timing is a channel masking does not cover: "user not found" returning in 5 ms and "wrong password" in 200 ms tells an attacker which accounts exist regardless of the message.

## Codes

- Define the set as an enum in the schema (or a documented constant list) and share it with clients. Codes that exist only as strings in server code drift the same way messages do.
- Standard codes and their first move: SKILL.md Error Codes. Add domain codes above that layer (`INSUFFICIENT_FUNDS`, `SEAT_TAKEN`), never below it.
- One code per condition, forever. Reusing `BAD_USER_INPUT` for eleven different validation failures forces clients back to parsing messages.
- Version nothing: add codes, never repurpose them. A client that treats an unknown code as "unexpected failure" degrades correctly; one that sees a repurposed code does the wrong thing confidently.

## Partial Data

- Partial success is the normal case, not an edge case: `data` populated, one branch null, one entry in `errors`. UIs that render only when `errors` is empty throw away work the server already paid for.
- The design lever is nullability: a nullable field lets the rest of the response survive; a non-null one takes its parent down with it (SKILL.md Null Propagation). Error design and nullability design are the same decision made twice.
- Tell clients which fields are allowed to be null for availability reasons. "This can be null when the recommendations service is down" belongs in the field description.
- `@defer`/`@stream` change the shape of partial results: errors can arrive in a later incremental payload, after the client has already rendered (`performance.md`).

## Errors In Lists

- One failing element in `[Post!]` nulls the entire list. If elements can fail independently, the type must be `[Post]` and the client must handle holes — or the resolver must filter failures out and report the count.
- Filtering without saying so is a data-integrity lie: a page showing 18 of 20 items with no indication is worse than a hole. If you filter, expose the fact (`extensions.omittedCount`, or a field on the connection).
- A batch loader returning an `Error` in one position produces exactly this per-element failure; throwing from the batch function fails all of them (`n-plus-one.md`).

## Logging And Correlation

- Attach one request id to the context, put it in `extensions` on every error, and log it on every server-side line. Support conversations then start with an id instead of a screenshot.
- Log the operation *name* and the variables' *keys*, never raw variables — they carry passwords, tokens and personal data (`production.md`).
- Log the error once, where it is caught and formatted, not at every level it passes through. Duplicate error lines make rate graphs meaningless.
- Alert on error *rate by code and by field path*, not on total error count: a 100% failure rate on one rarely-used field is invisible in an aggregate that is 0.3%.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Client checks only `response.ok` | Field errors ship with HTTP 200 | Check `errors` and `data` on every response |
| Client treats any error as total failure | Discards valid partial data | Handle per `path` |
| Branching on `error.message` | Prose changes without notice | Branch on `extensions.code` |
| Masking disabled in production | Leaks SQL, paths, upstream names | Mask everything unexpected, keep the original in logs |
| One code reused for many conditions | Clients cannot distinguish outcomes | One code per condition, added never repurposed |
| Filtering failed list elements without reporting it | The page lies about completeness | Report the omission, or use a nullable element type |
