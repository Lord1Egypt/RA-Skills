# Authorization — Who May See This Field, This Row, This Edge

Authentication answers "who is this" once, in the context factory. Authorization answers "may this viewer see this specific value" and can only be answered where the value is loaded. Everything below follows from that.

Contents: Where To Enforce · The Four Layers · Null Or Error · The node(id:) Hole · Batch Loaders And Row Checks · Directives · Field Visibility · Multi-Tenancy · Federation And Gateways · Testing · Traps

## Where To Enforce

| Placement | Catches | Misses |
|---|---|---|
| Proxy / gateway by operation name | Nothing reliable | Aliases, fragments, any other path to the same field |
| Whole-document inspection before execution | Simple deny lists | Any field reachable through a different parent |
| Resolver, on the loaded row | Everything, per value | Nothing — but must be written on every path |
| Data layer / repository | Everything, once per access pattern | Fields that read from somewhere else |

- The gateway-by-operation-name pattern is the recurring critical bug: `query AdminStuff` is blocked, `query Innocent { a: adminField }` is not. Operation names are client-chosen labels, not routes.
- Default: enforce in the data layer (a repository that never returns rows the viewer cannot see), with resolver-level checks for field-specific rules. A check the resolver forgets is a hole; a filter the repository applies is a default.
- The graph has many paths to the same node. Any rule expressed as "you cannot reach X" fails; only "this value is not yours" survives, because it is evaluated wherever the value appears.

## The Four Layers

1. **Authentication** — context factory: verify the credential, resolve the viewer, stop. No permission loading yet (`resolvers.md`).
2. **Operation-level** — cheap guards before execution: "anonymous callers may only send these operations", cost budgets per role. Coarse and advisory.
3. **Field-level** — this *type of viewer* may see this *field at all* (`User.ssn` for admins only). Static, expressible as a directive or a resolver wrapper.
4. **Object-level (row)** — this viewer may see *this instance*. Requires the row. This is where real policy lives, and where forgetting one field leaks data.

Layers 3 and 4 are different questions and both are needed: an admin-only field still needs a row check when the admin is scoped to one tenant.

## Null Or Error

- Returning `null` hides existence; returning `FORBIDDEN` confirms the object exists and you cannot see it. Both are legitimate; mixing them within one type is an oracle.
- Decision rule: if the identifier is guessable or enumerable (sequential ids, emails, usernames), return null and treat "not found" and "not permitted" identically — including in timing (`security.md`). If the identifier is a random key the caller already had to know, an explicit error is more useful and reveals nothing.
- With `null`, the field must be nullable, or the denial nulls the parent and effectively becomes an error anyway (SKILL.md Null Propagation). Permission-bearing fields are nullable by design.
- Whichever you choose, make it a documented property of the type so a reviewer can check for consistency, and so clients know whether `null` means "absent" or "denied".

## The node(id:) Hole

- A Relay-style `node(id: ID!): Node` root field reaches every type in the graph from a single entry point. Any type whose permission check lived in the field that "normally" leads to it is now reachable without that check.
- The fix is placement, not removal: the check belongs to the type's own loader, so every path — `node`, a nested edge, a search result, a federation entity reference — hits it.
- Global ids are enumerable: base64 of `Type:1` is trivially decodable and incrementable. Global ids over sequential keys plus a permissive `node` field is an enumeration of your entire database (`schema.md`).
- Same logic for any generic entry point: `search`, `recentActivity`, `admin { … }`, and every federation reference resolver.

## Batch Loaders And Row Checks

The subtle, high-severity interaction:

- A loader batches by id and returns rows. If the permission filter lives in the *field resolver* that called the loader, another field that calls the same loader with an id it obtained elsewhere gets the unfiltered row.
- A loader whose cache key omits the viewer serves one viewer's row to another when the loader outlives the request — the module-scope leak (SKILL.md rule 1, `n-plus-one.md`).
- Filtering inside the batch function is correct and requires care with the contract: a forbidden key must still occupy its slot, as `null` or an `Error`, or every subsequent result shifts onto the wrong key.
- Prefer loaders that are constructed *with* the viewer in scope and enforce visibility in their query (`WHERE tenant_id = $viewerTenant`), so the unfiltered row never enters memory.
- Never authorize by post-filtering an already-batched list in the resolver: the row was loaded, logged, and possibly cached before the check.

## Directives

- `@auth(requires: ADMIN)` in SDL is readable, greppable, and enforced by a schema transform or plugin — genuinely useful for layer 3 (field visibility by role).
- It cannot do layer 4: the directive runs with the parent and arguments, not the loaded row. A rule like "the author, or a moderator of that space" is not expressible there.
- Custom directives are invisible to generated client types: clients cannot discover which fields they may request, they only get errors (`codegen.md`).
- Directive-based rules must be enforced server-side by an actual transform. A directive nobody implemented is documentation that reviewers mistake for a control — grep the schema for directives with no matching implementation.

## Field Visibility

- Hiding a field from the *schema* per viewer (a filtered schema per role) is possible and expensive: the schema becomes viewer-dependent, so caching, codegen, registry checks and client tooling all fragment. Use it for genuinely separate audiences (a partner API versus the internal one), not for individual roles.
- The cheaper posture is one schema where privileged fields return null or error for everyone else, documented as such.
- Introspection reveals field *names*, never values. Hiding a field name is not a control (`security.md`).
- New fields default to visible. The review question for every schema PR is "who may read this", and the answer belongs in the field description or in the directive.

## Multi-Tenancy

- Tenant scoping belongs in the data layer, not in resolvers: every query carries the tenant predicate because the repository adds it, not because someone remembered.
- The tenant comes from the authenticated context, never from an argument. An argument-supplied `tenantId` is a horizontal-privilege-escalation vulnerability with extra steps.
- Loader keys must include the tenant when a loader can serve more than one, or the cross-tenant leak reappears inside a single request.
- Cross-tenant references (a shared catalog, a marketplace) are explicit types with their own rules, not an exception to the predicate.

## Federation And Gateways

- The gateway is not a trust boundary for subgraphs: each subgraph must authenticate and authorize independently, because a compromised or misconfigured gateway otherwise grants everything.
- The viewer must be propagated to every subgraph in a form each can verify (the original token, or a signed internal assertion). Passing a bare `x-user-id` header means anything that can reach a subgraph can impersonate anyone.
- Reference resolvers (`__resolveReference`) are entry points exactly like `node(id:)`: the gateway can ask any subgraph for any entity by key. Apply the same row check there.
- `@requires`/`@provides` move data across service boundaries; a field a subgraph may compute is not automatically a field the caller may see (`federation.md`).

## Testing

- Write per-field tests from the *attacker's* side: for each protected field, one test as the owner, one as an authenticated stranger, one as an anonymous caller. Anything not covered is not enforced (`testing.md`).
- Add a schema-wide test that enumerates every field and fails on any field not present in an explicit allowlist of "public" or "protected". New fields then fail the build until somebody decides.
- Test the alternative paths, not just the obvious one: through `node(id:)`, through a nested edge, through search, through a federation reference.
- Regression-test the loader boundary: two viewers in one process, sequentially, asserting that the second does not receive the first's row.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Permission check in the field that "normally" leads to the type | `node(id:)`, search and federation references reach it otherwise | Check in the type's own loader |
| Post-filtering an already-loaded batch | The row was loaded, logged and cached before the check | Filter inside the query |
| `tenantId` accepted as an argument | Any caller can name any tenant | Tenant from the authenticated context only |
| `@auth` directive with no implementation | Reads like a control, enforces nothing | Grep for unimplemented directives; enforce in a transform |
| Mixing null-for-denied and error-for-denied in one type | Becomes an existence oracle | One documented convention per type |
| Bare `x-user-id` header between gateway and subgraphs | Anything reaching a subgraph can impersonate | Propagate a verifiable token or signed assertion |
