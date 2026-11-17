# Testing — Tests That Catch What GraphQL Actually Breaks

Resolver unit tests pass while the API is broken. The failures that reach production are integration-shaped: nullability propagation, missing loaders, permission holes on alternate paths, and schema changes nobody checked against real client documents. Test those.

Contents: The Test Pyramid Here · Executing Operations · What Not To Unit Test · N+1 Assertions · Authorization Tests · Nullability Tests · Schema Tests · Mocking · Client Tests · Subscription Tests · Load And Limits · Traps

## The Test Pyramid Here

| Level | Tests | Catches | Cost |
|---|---|---|---|
| Schema assertions | The SDL itself | Breaking changes, unpaginated lists, missing directives | Milliseconds; run on every save |
| Operation tests | Execute a document against a real schema and a real database | Nullability, resolver wiring, N+1, permissions | Seconds; the bulk of the suite |
| Service/unit tests | Business logic behind resolvers | Domain rules | Fast; unchanged by GraphQL |
| Client document tests | Generated types plus a mocked link | Fragment shape, cache updates | Fast |
| End-to-end | Real client against a deployed stack | Transport, auth, CORS | Slow; a handful of paths |

- The middle row is where GraphQL-specific bugs live and where most codebases have the least coverage.
- Skip the HTTP layer in operation tests: execute the document directly against the schema with a constructed context. Same executor, same resolvers, no server, no port.

## Executing Operations

```
result = execute(schema, parse(document), rootValue, makeContext({viewer}), variables)
assert result.errors is undefined
assert result.data.user.posts.edges.length == 2
```

- Assert on `errors` explicitly in every test. A test that only checks `data.user.name` passes while three sibling fields are failing, because partial success is normal (`errors.md`).
- Use the *real* schema, not a test schema: a test schema drifts and stops testing what ships.
- Build the context through the same factory production uses, with the viewer swapped. A hand-built test context omits the loaders and hides every N+1 (`resolvers.md`).
- Use a real database with a per-test transaction rolled back afterwards. Mocked data layers cannot catch the failures in this file.
- Test documents should be the ones clients actually send: pull from the operation registry where one exists, so the suite tracks real usage (`schema-evolution.md`).

## What Not To Unit Test

- A resolver called directly as a function skips validation, argument coercion, default resolvers, null propagation and the executor's concurrency — that is, everything specific to GraphQL. It tests a function you could have tested in the service layer.
- Directly-called resolver tests also encourage fat resolvers, because that is the only place the logic being tested lives (`resolvers.md`).
- Exception: a complex `__resolveType` or a custom scalar's three functions are worth unit-testing in isolation, including the literal path that variables never exercise.

## N+1 Assertions

- Count database statements per operation and assert a ceiling. Instrument the driver in test mode, reset the counter per test, assert.
- The assertion that catches regressions is *page-size independent*: run the same query against 2 rows and 20 rows and assert the statement count is identical. Any loader that goes missing fails immediately.
- Do this once per list-bearing operation, not once per resolver. Half a dozen such tests cover a whole schema's worth of loaders.
- Assert rows loaded as well as statements: three statements loading 10 000 rows to render 20 is the other failure (`n-plus-one.md`).

## Authorization Tests

- For every protected field: owner sees it, authenticated stranger does not, anonymous does not. Anything not covered by a test is not enforced (`authorization.md`).
- Test the alternate paths, not just the obvious one — through `node(id:)`, through a nested edge, through search, through a federation reference resolver. That is where the holes are.
- A schema-wide guard test: enumerate every field in the schema and fail on any field absent from an explicit public/protected allowlist. New fields then fail the build until someone decides, which is the only mechanism that scales.
- Cross-request leak test: run two operations sequentially in one process as two different viewers, assert the second gets its own data. Catches the module-scope loader.

## Nullability Tests

- Make a downstream dependency fail and assert what survives. The point is to discover which branch of the response disappears, before an incident does it for you.
- Specifically test: a list element failing (`[T!]` versus `[T]`), a non-null field returning null, and a permission denial on a non-null field. Each has a different blast radius (SKILL.md Null Propagation).
- Assert `errors[].path` and `errors[].extensions.code`, not the message — a test asserting on message text breaks on every wording change and passes when the code is wrong.

## Schema Tests

- Assert properties of the SDL itself, cheaply and on every change:
  - Every field returning a list either takes pagination arguments or is on an explicit bounded allowlist.
  - Every mutation returns a payload type, never a scalar.
  - Every type implementing `Node` has `id: ID!`.
  - No field marked with an auth directive that has no implementation.
  - No new custom scalar without a codegen mapping.
- A committed schema snapshot makes every schema change visible in the diff, where a reviewer sees it. It is not a substitute for the breaking-change checker; it is what makes the check's output reviewable.
- Run the breaking-change check in CI against the deployed schema and against recorded operations (`schema-evolution.md`).

## Mocking

- Auto-generated mocks from the schema are useful for two things: rendering a client before the server exists, and fuzzing every field for null-handling. They are useless for correctness, because they assert your own schema back at you.
- Client tests should mock at the *link* layer with real documents and typed fixtures, not by stubbing hooks — stubbing the hook skips the cache, which is where the bugs are (`client.md`).
- Fixtures must be generated from the schema so a field rename breaks them. Hand-written fixtures are hand-written types with extra steps (`codegen.md`).

## Client Tests

- Test the cache, not the request: fire a mutation with a mocked response, assert the cached list and the rendered output. That is where "the UI did not update" lives.
- Test list insert and delete explicitly — the two cases normalization cannot infer.
- Test the pagination field policy: two pages merge into one list, and switching a filter starts a new list rather than appending.
- Test the error path with a response carrying both `data` and `errors`; most client code has never been run against one.

## Subscription Tests

- Test the async iterator directly: publish, assert the next yield. No socket needed.
- Test with two server instances against one broker — the failure that never reproduces with a single process (`subscriptions.md`).
- Test permission revocation mid-stream and token expiry mid-connection.
- Test reconnect: drop, publish during the gap, reconnect, assert the re-sync produces correct state with no duplicates.

## Load And Limits

- Assert that each limit actually fires: a document over the token cap, over the depth limit, over the alias cap, over the complexity budget — each returns the expected code. Limits are configuration, and configuration reverts unnoticed (`security.md`).
- Assert the *inverse* too: your largest legitimate operation passes every limit. This is the test that stops a limit tightening from breaking a customer.
- Load-test with operations from the registry and include the worst legitimate shape, not the average (`performance.md`).
- Test the CSRF posture: a request with `Content-Type: text/plain` must be rejected; a `GET` carrying a mutation must be rejected.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Calling resolvers as plain functions | Skips validation, coercion, propagation, concurrency | Execute documents against the real schema |
| Not asserting on `errors` | Partial success passes a data-only assertion | Assert `errors` is empty, or assert its exact shape |
| Hand-built test context | Omits loaders; hides every N+1 | Reuse the production context factory |
| Mocked data layer everywhere | Cannot catch statement counts, transactions, or permission filters | Real database, transaction per test, rollback |
| Fixed-size N+1 assertions | A regression at 20 rows passes at 2 | Assert statement count is equal across two page sizes |
| Asserting on error messages | Breaks on wording, passes on wrong code | Assert `extensions.code` and `path` |
| Auto-mocks as correctness tests | They assert your schema back at you | Mocks for rendering and fuzzing only |
| Testing limits are configured, never that they fire | Configuration reverts unnoticed | One test per limit, plus one for the largest legitimate operation |
