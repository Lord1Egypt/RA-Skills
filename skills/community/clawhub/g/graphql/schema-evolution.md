# Schema Evolution — Changing A Contract With No Version Number

GraphQL's answer to versioning is "do not": one schema, additive forever, fields deprecated and eventually removed on evidence. That only works with a checker in CI and usage telemetry in production. Without both, "we never version" means "we break clients and find out from support".

Contents: The Breaking Change Matrix · Why Input And Output Differ · Safe By Construction · The Deprecation Loop · Usage Telemetry · Checks In CI · Registry And Operation Checks · Renames And Moves · Semi-Breaking Changes · Versioning When You Must · Traps

## The Breaking Change Matrix

| Change | Output position | Input position (arguments, input fields) |
|---|---|---|
| Add a field | Safe | Safe if optional; **breaking** if required |
| Remove a field | **Breaking** | Safe for the server, breaking for callers still sending it if it becomes unknown |
| Nullable → non-null | Safe (clients get a stronger guarantee) | **Breaking** (callers who omitted it now fail validation) |
| Non-null → nullable | **Breaking** (clients assumed a value) | Safe (an optional argument accepts what was required) |
| Change the type | **Breaking** unless it is a strict widening of the same shape | **Breaking** |
| Add an enum value | **Semi-breaking** (exhaustive clients hit an unknown branch) | Safe |
| Remove an enum value | **Breaking** | **Breaking** |
| Add a union member / interface implementer | **Semi-breaking** | n/a |
| Remove a union member | **Breaking** | n/a |
| Add a field to an interface | Safe for clients, **breaking for every implementing type** until they add it | n/a |
| Add an argument | Safe if optional; **breaking** if required | — |
| Change an argument default | **Semi-breaking**: silent behaviour change for callers who omitted it | — |
| Rename anything | **Breaking** — it is a remove plus an add | **Breaking** |
| Add `@deprecated` | Safe; changes nothing at runtime | Safe (the target must be optional) |

## Why Input And Output Differ

The two columns move in opposite directions and this is the single most-missed rule in schema review.

- Outputs flow server → client. Promising *more* (non-null) is safe; promising *less* (nullable) breaks a client that assumed a value.
- Inputs flow client → server. Requiring *less* (optional) is safe; requiring *more* (non-null) breaks every caller that omitted the field.
- Same rule, one sentence: you may always strengthen what you give and weaken what you demand.
- The corollary nobody likes: an input field can essentially never become required after launch. Add it optional with a server-side default, migrate callers, and only tighten if you can prove every caller sends it (`schema.md`).

## Safe By Construction

- New capability = new field, never a changed one. `publishedAtUtc` beside `publishedAt` costs one deprecation cycle and breaks nobody.
- New behaviour on an existing field = new argument, optional, defaulting to the old behaviour.
- New failure mode = a new member in an existing result union (semi-breaking, announce it) or a new code in the errors enum (safe if clients handle unknown codes as generic failures, `errors.md`).
- Enum growth is safe in inputs and hazardous in outputs — the client-side fallback branch is what makes output enums evolvable, and it must exist before you add the value.
- Prefer nullable outputs from day one: making an output field non-null later is safe, the reverse is not. Every non-null field you ship is a promise you cannot walk back (SKILL.md rule 2).

## The Deprecation Loop

1. Ship the replacement field. Both live side by side.
2. Mark the old one `@deprecated(reason: "Use X; …")` with a migration instruction, not the word "deprecated".
3. Tell the client teams — the reason string reaches nobody who is not already reading introspection.
4. Watch field usage until it reaches zero, for at least `deprecation_window_days` (default 90) and never less than `slowest_client_cycle_days`.
5. Remove, and treat the removal as a deploy with a rollback plan.

- The window exists for clients you cannot force-upgrade: shipped mobile builds, partner integrations, that one internal script. If every client is a web bundle you deploy, the window can be days; one shipped mobile build or partner integration in the mix raises it to that client's own cycle — record it as `slowest_client_cycle_days` and let it floor the window.
- Zero usage for a week is not zero usage: a monthly report job selects the field once a month. Measure across a period longer than `slowest_client_cycle_days`.
- A deprecated field still costs: it still resolves, still runs its query, still appears in cost estimates. Deprecation is a migration signal, not a performance improvement.

## Usage Telemetry

- Field-level usage — which client, which operation, which field, how often — is what turns "we think nobody uses it" into a removal you can defend. Without it the choice is guessing or never removing.
- Collect the client name and version on every request (a header the client sets, enforced in production). Usage without a client dimension tells you a field is used but not by whom, which does not let you go talk to anyone.
- Reject unnamed operations in production: `query { … }` with no name is invisible in every telemetry view (`production.md`).
- Field usage doubles as a performance signal — expensive fields nobody requests are dead weight (`performance.md`).

## Checks In CI

- Every schema change runs a diff against the currently deployed schema and classifies each change as safe, dangerous or breaking. Breaking fails the build unless explicitly acknowledged in the PR.
- The check is much stronger with operations attached: a change that is *technically* breaking but touches a field no recorded operation selects can be approved automatically. This is how large schemas keep moving.
- Run the check against the deployed schema, not against the previous commit — long-lived branches otherwise validate against a schema nobody runs.
- In a federated graph, every subgraph runs composition *and* the breaking-change check against the published supergraph, in its own CI (`federation.md`).
- Commit a schema snapshot so every change appears in the diff a human reviews. The checker classifies; the snapshot is what makes a reviewer notice.

## Registry And Operation Checks

- A schema registry stores every deployed schema version, the composed supergraph, and the set of known client operations. It is the input to every check above.
- Register client operations at build time — the same artifact that powers trusted documents (`security.md`) and persisted queries (`caching.md`). One manifest, three uses.
- Keep old operation manifests as long as the corresponding client versions are alive. Dropping them makes the checker approve a removal that breaks a shipped mobile build.
- Without a registry: a nightly job sampling operation strings from production logs into a table is the cheap substitute — it catches the operations that actually run, and misses the ones that ran before you started sampling.

## Renames And Moves

- A rename is a remove plus an add. Do it as: add the new name, deprecate the old, migrate, remove.
- Moving a field to a different parent type is two changes with the same rule; keep the old path resolving from the new source during the window.
- Changing a field's *type* is not possible safely — model it as a new field with the new type and deprecate the old, even when the change looks harmless (`Int` → `Float` breaks a client parsing integers).
- Moving a field between subgraphs is an ownership change with tooling of its own (`@override`), and still needs both sides live across a deploy (`federation.md`).

## Semi-Breaking Changes

Changes the checker calls safe and clients experience as breakage:

- A new enum value or union member reaching an exhaustive client.
- A changed argument default, altering results for callers who omitted the argument with nothing to signal it.
- A field that starts returning null more often (an upstream became flaky) — the type did not change, the reality did.
- A tightened validation rule on an existing input: same types, newly rejected values.
- A change in ordering, page size default, or which items a filter matches. Nothing in the type system describes these, so nothing checks them.

Announce all of these like breaking changes, and write the ones that are not expressible in the type system into the field description where a client author will see them.

## Versioning When You Must

- Field-level versioning (`searchV2`) is ugly, honest and local: the old field keeps working, the new one is opt-in, the deprecation loop cleans up. Use it when a behaviour change genuinely cannot be additive.
- Endpoint-level versioning (`/graphql/v2`) doubles the surface, the telemetry and the deploy: use only for a full API generation with a defined sunset date.
- Never version by adding a `version` argument that switches behaviour: the same field then has two shapes and one type, which no client can be typed against.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Making an input field required after launch | Every existing caller fails validation | Optional with a server default, migrate, then consider tightening |
| Making an output field nullable "for safety" | Breaks clients that assumed a value | Ship nullable from day one; tightening later is the safe direction |
| Removing on a calendar with no usage data | The one client you forgot is a shipped mobile build | Zero usage for a full window, measured per client |
| `@deprecated` with no replacement named | Nobody migrates; the field lives forever | Migration instruction in the reason string |
| Checking against the previous commit | Long-lived branches validate against a schema nobody runs | Check against the deployed schema |
| Adding an output enum value without a client fallback | Exhaustive clients hit an unhandled branch | Ship the fallback branch first, then the value |
| Changing an argument default | Silent behaviour change for existing callers | New argument, or new field |
| Dropping old operation manifests | The checker approves a removal that breaks live clients | Keep manifests as long as their client versions live |
