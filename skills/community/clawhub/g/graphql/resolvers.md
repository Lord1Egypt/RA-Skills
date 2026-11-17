# Resolvers — Execution, Context, And The Chain

Mental model: the executor walks the selection set breadth-first, calling `resolve(parent, args, context, info)` for each field. A field resolver only ever sees what its parent returned. Most "impossible" resolver bugs are a wrong assumption about that sentence.

Contents: The Four Arguments · Default Resolvers · Execution Order · The Context Factory · Returning Partials · Abstract Types · Projection From info · Directives · Where Logic Belongs

## The Four Arguments

| Argument | Is | Trap |
|---|---|---|
| `parent` | Exactly what the parent resolver returned | Not a database row; not the full entity unless the parent loaded it |
| `args` | Validated against the schema, defaults applied | Type-valid, never business-valid: `first: -5` passes the type system |
| `context` | Per-request bag: viewer, loaders, transaction, tracing span | Anything module-level here is shared between users (SKILL.md rule 1) |
| `info` | The AST of this field's selection, path, schema, variables | Reading it is a superpower and a coupling; see Projection |

- `args` is validated for shape only. Range, length, format and cross-field rules are yours (`errors.md`).
- `parent` on a root field is the `rootValue`, usually undefined. Root resolvers therefore load; child resolvers traverse.

## Default Resolvers

- With no resolver defined, the executor reads `parent[fieldName]`. If the value is a function it calls it with `(args, context, info)` — the signature is *shifted*, which is why a hand-written class method occasionally receives arguments it did not expect.
- Consequence: a schema field with no resolver returns `undefined` with no error when the property is spelled differently (`created_at` versus `createdAt`). With a non-null type this nulls the parent; with a nullable type the null is indistinguishable from real data, forever.
- Do not write pass-through resolvers that only return `parent.x` — they add lines and hide nothing. Write resolvers only where the field does work.
- Field aliases never reach the resolver: `a: user` and `b: user` both call the same resolver twice with identical arguments. Batching and caching happen in the loader, not by the executor noticing.

## Execution Order

- Sibling fields of a **query** are executed concurrently and in unspecified order. Nothing may depend on which finished first.
- Root fields of a **mutation** are executed serially in document order — the only ordering guarantee in the spec. Two mutations in one document run one after the other; two *nested* mutation fields do not get that guarantee.
- Depth is sequential by construction: children start only after the parent resolves. A slow parent stalls everything under it, which is what makes deep chains latency-additive (`performance.md`).
- Returning a promise is normal; returning a promise from a field the executor treats as a plain value (a custom scalar `serialize`) is not — scalars serialize synchronously.
- A thrown error in one sibling does not cancel the others: they keep running and their results still ship. Cancellation is your job via an abort signal on the context (`production.md`).

## The Context Factory

The context factory runs once per request and is the security boundary for everything below it.

```
context = {
  viewer,                 // resolved from the auth header, once
  loaders: makeLoaders(), // fresh instances per request  (SKILL.md rule 1)
  db,                     // pooled client, not a per-request connection
  abortSignal,            // cancel downstream work when the client disconnects
  requestId,              // travels into every log line and errors[].extensions
}
```

- Authenticate here, authorize in resolvers. The factory answers "who is this?"; only the resolver knows which row is being asked for (`authorization.md`).
- Loaders are constructed here and nowhere else. A loader built at module scope survives across requests, and its cache is keyed by id with no viewer dimension — request B reads the row loaded for request A. This is the highest-severity mistake in the whole skill.
- Keep the factory cheap: it runs before any limit check, so expensive work here is a free DoS amplifier. Verify the token, do not load the user's permission tree until a resolver asks.
- Do not open a database transaction per request by default. Long GraphQL reads hold it open across every resolver in the tree and exhaust the pool; open transactions inside the mutation that needs one.
- Subscriptions have a *connection* context established once at handshake and a per-message execution — the difference is where token expiry bites (`subscriptions.md`).

## Returning Partials

- A resolver may return a partial object: the child fields the query selected will each be resolved from it. Returning `{ id }` and letting field resolvers fetch the rest is the idiomatic way to avoid over-fetching at the top level.
- The cost is that every child field then needs its own load, which is exactly the N+1 the loaders exist for. Partial-return plus loaders is the pattern; partial-return without loaders is the pathology (`n-plus-one.md`).
- Returning an object whose properties are promises works: the executor awaits per field, so unselected slow fields are never awaited. Returning `await Promise.all([...])` of everything eagerly throws that away.
- Never return a raw ORM entity with lazy relations attached — the lazy loader fires per field, per row, invisibly, and profiling shows nothing but "the ORM".

## Abstract Types

- Interfaces and unions need `__resolveType` (or `resolveType`) or the executor cannot pick a concrete type. Without it, the error is "Abstract type must resolve to an Object type at runtime", pointing at the interface, not at the offending value.
- Two ways to satisfy it: a `__typename` property on the returned object (simplest, works with plain records), or a `resolveType` function on the abstract type. Pick one convention per service.
- `isTypeOf` on each concrete type is the third option and the slowest: the executor tries each candidate in turn.
- Errors thrown inside `__resolveType` surface at the parent field with a confusing path — guard the discriminating property rather than letting an undefined read throw.

## Projection From info

`info` carries the requested selection set. Reading it lets one resolver serve a whole subtree from a single query.

- Use it for: selecting only requested columns; deciding whether an expensive join is needed at all; deciding between a batched loader and a single join.
- Do not use it for: business decisions ("only apply the discount when they asked for `total`"). That makes the response depend on the shape of the query, which is unreproducible for anyone debugging it.
- Fragments and inline fragments make raw `info.fieldNodes` walking wrong — a helper that flattens fragments and variables (`graphql-parse-resolve-info` and equivalents) is the difference between a working projection and a mysterious missing column.
- The projection lives at the top of the subtree and the children must then read `parent`, not re-fetch. Document that coupling in a comment at both ends, or the next person adds a loader call and the join becomes dead weight.
- Whole-tree compilers (Hasura, PostGraphile, join-based resolvers) take this idea to its conclusion: one SQL statement for the entire document. That is a framework choice, not something to hand-roll field by field (`rest-migration.md`).

## Directives

- Type-system directives (`@deprecated`, `@key`, custom `@auth`, `@cost`) annotate the SDL and are applied by transforming the schema at build time or by reading them in a plugin. They are not executed per request by the core executor.
- Executable directives (`@skip`, `@include`) are the only two every server supports; anything custom on the client side needs server support that most libraries do not provide by default.
- `@skip(if:)`/`@include(if:)` remove the field from the *response* entirely — the key is absent, not null. Clients that destructure with a default handle it; clients that check for `null` do not.
- A `@auth` directive is a convenient place to put a check and a poor place to keep it: directive checks run per field with only `parent` in hand, so any rule needing the loaded row still belongs in the resolver (`authorization.md`).
- Custom directives do not appear in generated client types. Anything a client must react to belongs in the data, not in a directive.

## Where Logic Belongs

| Concern | Home | Why not the resolver |
|---|---|---|
| Authentication | Context factory | Runs once; resolvers must not re-parse tokens |
| Authorization on a specific row | Resolver or loader | Only there is the row actually loaded |
| Business rules, invariants | A service layer the resolver calls | Resolvers get unit-tested through the executor; services test directly |
| Data access, batching | Loaders / repositories | One place to add caching, tracing and query budgets |
| Input shape validation | Schema (types, enums, argument defaults) | Free, introspectable, and enforced before your code runs |
| Input business validation | Service layer, surfaced as typed errors | Keeps the same rule identical between GraphQL and any other entry point |

A resolver that is more than roughly a dozen lines is usually holding business logic that a second entry point (a cron job, a REST endpoint, a subscription) will later need and not be able to reach.
