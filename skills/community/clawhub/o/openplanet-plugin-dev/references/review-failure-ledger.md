<!--
SOURCE: github.com/XertroV/tm-plugin-skills — skills/openplanet-reviewer/references/failure-ledger.md
AUTHOR: XertroV
LICENSE: CC0-1.0 OR Unlicense (public-domain equivalent; free to reuse, modify, redistribute)
ATTRIBUTION: imported into openplanet-plugin-dev (tomekdot) as a review-procedure reference.
NOTE: this file is an external review checklist, not Openplanet API documentation — use it
when reviewing a finished plugin/PR/release for subtle runtime/state/UI/architecture failures.
-->
# Failure ledger

Use this as a mechanism checklist, not a keyword linter. Mark each applicable
class caught, N/A, or not tested.

## UI and callbacks

### UI callback failure containment

Risky action execution escapes a render callback, leaving UI scopes dangling and
stopping later callbacks. Trace transitive calls, including dynamic callbacks.
Require a real coroutine boundary for throwing/yielding/I/O/game-mutation work
and balance all UI/style/clip/scissor scopes on every actual path.

### Duplicate render dispatch

The same window or draw surface is submitted from multiple callbacks in one
frame. Assign one owner per overlay state and use stable explicit IDs.

### Interactive identity drift

Labels, ordering, localization, duplicated components, or loop positions change
ImGui identity. Require explicit stable IDs composed from persistent domain
identity and scope.

### Exception-safe scope restoration

Token counts or parallel depth helpers pass while an early return or throw leaks
window/table/child/style/clip/scissor state. Probe failure after each begin/push.

## State, mode, and lifetime

### Wrong game/application mode

Code reaches editor/playground/map/server objects outside its valid mode. Model
mode explicitly and fail closed with a concise reason and remediation.

### Plugin/game state desynchronization

Callbacks, packets, retries, or overlapping tasks apply out of order or outlive
the map/editor/server/session/reload snapshot that created them. Require
generation ownership, post-yield revalidation, explicit retry/reorder semantics,
and cleanup after partial teardown.

### Async terminal-state completeness

Loading/busy/in-progress flags or waiters have no error/timeout/cancel terminal.
Enumerate exactly one terminal state and cleanup for every exit.

### Transactional mutation restoration

Patches, hooks, intercepts, temporary modes, or settings survive early return,
throw, cancel, unload, or transition. Treat mutation as a transaction with one
idempotent rollback owner.

### Manual engine-reference ownership

`MwAddRef`, retained nods, or tasks leak or double-release. Build a balance graph
across every terminal path and repeated failure.

### Zero-progress and boundary behavior

A timeout before item zero causes negative indexing, queue stalls, skipped work,
or cleanup bypass. Test zero, one, exact limit, partial progress, and concurrent
queue mutation.

### Mutation-result truthfulness

Expected/replicated state advances, or queued work is removed, before engine
application is verified. Require validate → apply → observe → commit → ack.

## Component and module boundaries

### Component visibility versus intent

Remote or programmatic actions activate invisible/undrawn controls. Default to
`force = false`; return cause and next step when control is not visible.

### Export/module identity mismatch

Importer/exporter topology or shared identity assumptions differ between LSP,
generator, and Openplanet. Prefer ordinary exports unless shared identity/state
is required; validate dependent load and unload order in game.

### Architecture erosion

Callbacks contain business engines, multiple modules derive the same truth,
boolean combinations encode illegal states, god objects mix protocol/state/UI,
or public mutation bypasses owners. Findings require concrete correctness or
change-safety impact, not aesthetics.

## Networking and synchronization

### Network architecture mismatch

Transport architecture was copied without classifying data, cadence, ordering,
loss consequence, consistency, and recovery. Document those properties first.

Probe:

- exact frame consumption and length bounds;
- fragmentation and partial writes;
- sole writer and ordering;
- count and byte backpressure;
- duplicate/replay/reorder/drop/delay;
- stale connection/session/map epochs;
- retry/coalescing per traffic class; and
- reconciliation after poisoned expected state.

## Evidence rule

A new class entry should state trigger, impact, invariant, evidence, reviewer
probe, and prevention/evidence gate. A hypothesis must include one concrete next
probe.