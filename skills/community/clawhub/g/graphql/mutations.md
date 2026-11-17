# Mutations — Writes That Clients Can Actually Consume

A mutation is judged by what the caller can do with the response without asking again. The payload rule is SKILL.md rule 5; ordering is rule 6.

Contents: The Standard Shape · Naming And Granularity · Idempotency · Partial Failure · Concurrency · Cache Consequences · File Uploads · Deletes · Bulk Writes · Transactions · Traps

## The Standard Shape

```graphql
type Mutation {
  publishPost(input: PublishPostInput!): PublishPostPayload!
}
input PublishPostInput { postId: ID!, publishAt: DateTime, clientMutationId: String }
type PublishPostPayload {
  post: Post                 # nullable: absent when the operation failed
  userErrors: [UserError!]!  # always present, empty on success
  clientMutationId: String
}
type UserError { message: String!, field: [String!], code: UserErrorCode! }
```

- One `input` argument, one payload type, both named after the mutation. Flat argument lists work until the third argument, then every addition is a diff across every client.
- The payload is non-null and the entity inside it is nullable — that way a failure returns errors without nulling the whole mutation field (SKILL.md Null Propagation).
- `userErrors` is non-null and empty on success, so clients write one branch (`if (userErrors.length)`) instead of two null checks.
- `field: [String!]` is the path into the input (`["input","publishAt"]`) so a form can attach the message to the right control. Without it every error lands on a generic banner.
- `code` is a closed enum. The message is for humans and changes; the code is the contract (`errors.md`).
- `clientMutationId` is Relay's echo field for correlating responses. Include it if you use Relay's mutation helpers; skip it otherwise rather than cargo-culting it.

## Naming And Granularity

- Name the *intent*, not the storage operation: `publishPost`, `cancelSubscription`, `assignReviewer` — not `updatePost(input: {status: PUBLISHED})`.
- Intent-named mutations carry their authorization rule and their audit meaning; a generic `updateX` with 20 optional fields has neither, and every permission check inside it becomes a per-field conditional.
- The escape hatch: one `updateXDetails` for genuinely free-form editing of user-owned content (a draft, a profile) alongside intent mutations for state transitions.
- Do not expose a mutation per column. If a form saves eight fields at once, that is one mutation.
- State machines belong in the schema: a `status` enum plus transition mutations makes the illegal transitions unrepresentable, where `updateStatus(status:)` makes them a runtime check you will forget once.

## Idempotency

- Any mutation a client may retry (payments, provisioning, anything behind a flaky network) takes a client-supplied key: either a client-generated entity id or an explicit `idempotencyKey: String!`.
- Server side: store the key with the result, scoped to the mutation and the viewer, and return the stored result on a repeat instead of re-executing. Without storage, "idempotent" means "we hope the second call fails cleanly".
- Pick a retention window and document it (a day covers retry storms; longer costs storage and confuses users who reuse a key deliberately). The window belongs in the field description, because clients cannot discover it.
- Client-generated ids (UUID/ULID chosen by the caller) are the cleanest version: the create is idempotent by construction, and the client can build optimistic UI with the final id already known (`client.md`).
- Mutations with no side effects beyond setting a value to a constant (`archivePost`) are already idempotent — do not add a key mechanism they do not need.

## Partial Failure

- Two failing mutation root fields in one document: the first runs, fails, and the second still executes — serial does not mean transactional (SKILL.md rule 6). A client sending three mutations in one document can get outcome combinations no single request would produce.
- Decide and document: either one mutation per request (simplest, the default), or a batch mutation whose payload reports per-item outcomes.
- Never let a batch mutation return a bare list of entities: the caller cannot tell which of the fifteen inputs failed.
- For a batch, echo the input index or key in each result item — matching by array position across a filtered list is how the wrong record gets marked failed.

## Concurrency

- Lost update: two clients read, both edit, both write, the second overwrites the first with no error. GraphQL does nothing about this on its own.
- Optimistic concurrency: expose a `version: Int!` or an `updatedAt` on the entity, take it in the input, and reject the write when it does not match with a `CONFLICT` user error carrying the current value so the client can merge.
- Field-level merge (accepting only the fields present in the input) reduces but does not eliminate the problem: two clients editing the same field still collide.
- Do not implement optimistic concurrency with the entity's `id` or a hash of the whole row — the hash changes when unrelated fields change and users see spurious conflicts.

## Cache Consequences

- Return the modified entity with `id` and `__typename` and a normalized client cache updates every view of it with no client code at all. This is the entire reason for rule 5.
- Deletes and list insertions are the two cases the cache cannot infer: nothing in the response says "this node left that list". Return the affected parent (or the connection edge) or write an explicit cache update (`client.md`).
- Mutations that change *many* entities (a bulk archive, a re-order) should return the affected collection, not a count. A count forces a refetch of everything the client had.
- Server-side, clear the affected loader keys before the payload's own field resolvers run, or the payload reads the pre-mutation row out of the loader cache (`n-plus-one.md`).

## File Uploads

- Default: do not send bytes through GraphQL. `createUploadUrl` returns a presigned URL and a key; the client `PUT`s to storage; `attachAvatar(key:)` records it. The GraphQL server never touches the payload, uploads survive a server restart, and progress and resumption are the storage provider's problem.
- The multipart request specification (a `multipart/form-data` body with an `operations` map) exists and several servers support it through a plugin. It is a reasonable choice for small internal tools and a poor one for a public endpoint: it widens the CSRF surface (multipart is a simple request that skips preflight) and puts a body parser in front of every request.
- If you do accept multipart: enforce a size cap before parsing, require a custom header so the browser must preflight, and validate the content type server-side from the bytes, not from the declared MIME type.
- Never return the raw storage URL as a permanent field on a private object — issue short-lived signed URLs from a resolver so access follows the same authorization path as everything else (`authorization.md`).

## Deletes

- `deletePost(input:): DeletePostPayload!` returning `deletedPostId: ID` (plus `userErrors`) gives the client exactly what it needs to evict the entity from a normalized cache. A `Boolean` does not.
- Soft delete versus hard delete is a schema decision, not an implementation detail: a soft-deleted entity still resolves by id unless every resolver filters it, and clients will find it through some path you forgot.
- Deleting a node that other fields reference turns those fields null — which is fine if they are nullable and an outage if they are not (SKILL.md rule 2).
- Restore is a separate mutation, not `delete(undo: true)`.

## Bulk Writes

- A bulk mutation is worth defining when clients would otherwise send hundreds of documents; below that, per-item mutations are simpler for both sides.
- Cap the input list length in the schema description and enforce it in the resolver — an uncapped input list is the write-side version of an uncapped `first`.
- Cost the input, not just the output: a document with a 10 000-element input array is cheap to score and expensive to execute unless input size feeds your cost model (`security.md`).
- Long-running bulk work belongs behind a job: the mutation returns a job entity with a status enum, the client polls or subscribes. A mutation that holds a connection open for minutes fails at every proxy timeout between you and the user.

## Transactions

- One mutation, one transaction, opened inside the resolver — never in the context factory, where it would span the whole request and every read in the document (`resolvers.md`).
- The payload's field resolvers run *after* the transaction commits, so they must read committed state. Returning objects loaded inside the transaction and letting child fields lazily re-read is where phantom reads appear.
- Do not span a transaction across two mutation root fields: they are separate resolver invocations with separate error handling, and the second one failing cannot roll the first back.
- Side effects that must not fire on rollback (emails, webhooks, payments) go through an outbox written in the same transaction, not through a call inside the resolver.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `deleteX: Boolean!` | No entity, no id, no way to update a cache | Payload with `deletedXId` |
| Generic `updateEntity(input: {…everything})` | No intent, no per-transition authorization, no audit meaning | Intent-named mutations for state changes |
| Retryable mutation with no idempotency key | A network retry double-charges | Client-supplied key stored with the result |
| Batch mutation returning `[Entity!]!` | Caller cannot map failures back to inputs | Per-item results echoing the input key |
| Payload entity typed non-null | A failed mutation nulls the whole mutation field | Nullable entity, non-null `userErrors` |
| Reading the loader cache inside the payload | Returns the pre-mutation row | Clear affected keys before resolving the payload |
| Uploading bytes through the GraphQL endpoint by default | CSRF surface plus a body parser on the hot path | Presigned URL, upload out of band |
