---
name: implementation-self-review
description: Use after an implementation pass to self-review responsibility boundaries, necessity, defensive branches, naming, tests, documentation iteration scope, and same-class issues before final delivery.
---

# Implementation Self Review

## Purpose

Run this skill after the first implementation pass, before final delivery, or when the user questions code organization, necessity, naming, defensive checks, iteration scope, or repeated rework. Treat it as a compact engineering self-review, not a broad rewrite mandate.

## Use When

Use this skill when:

1. A first implementation pass exists and needs a compact engineering self-review before final delivery.
2. The user questions responsibility boundaries, file organization, naming, defensive checks, abstraction necessity, tests, documentation iteration scope, or repeated rework.
3. One issue may imply same-class problems that should be scanned before more edits.

Do not use this skill when:

1. The user asks for a full pull request or code review; use a code-review skill instead.
2. The user asks for a security audit or threat model; use the relevant security skill instead.
3. The task is architecture design, product planning, or requirements discussion before implementation.
4. There is no implementation change or concrete implementation proposal to review.

## Required Inputs

Before reviewing, gather:

1. The changed files, diff, or a concise implementation summary.
2. The user's concern, if the review was triggered by feedback.
3. The repo's active collaboration, architecture, and feature-planning rules.
4. Verification commands already run, or the commands still needed before delivery.

If changed files or a diff are unavailable, say the review is limited to the visible summary and avoid making file-specific claims.

## Review Workflow

1. Identify the changed behavior and the files touched.
2. Compare the change against the repo's active architecture and collaboration rules.
3. Review the implementation with the gates below.
4. Report concrete findings first; if there are no issues, say that clearly and list residual risks.
5. Fix issues only when the user asked for implementation or the current task is already an implementation task.

## Gates

### Placement Gate

Ask:

1. Does adding this code to the current file make the file's responsibility unclear?
2. Does splitting it into new files make the feature harder to review, trace, or delete?
3. Can the behavior be read from the local structure without jumping across many thin files?

Prefer existing local patterns and compact organization. Add a new file only when it clarifies a real responsibility boundary or avoids meaningful crowding.

### Necessity Gate

For each new type, field, interface, config, abstraction, helper, and state value, ask:

1. Is it needed by the current accepted contract?
2. Is it only a future-facing placeholder?
3. Can it be removed, merged, or expressed by an existing name or field?

Flag overdesign explicitly. Prefer removing unused structure over documenting why it might be useful later.

### Boundary And Defense Gate

For each `nil`, empty, default, fallback, or defensive branch, ask:

1. Is this a real boundary where untrusted or optional input enters?
2. Is this masking a constructor or caller contract that should be strict?
3. Would failing fast at setup make the invariant clearer?

Keep defenses at entry/configuration boundaries. Avoid internal defensive checks that make ownership unclear.

### Naming Gate

For long names or repeated terms, ask:

1. Does the surrounding type/file already provide part of the meaning?
2. Is the name describing implementation mechanics rather than domain intent?
3. Can the term be shortened without losing review clarity?

Prefer clean domain names over stacked qualifiers.

### Error Semantics Gate

For each error path, ask:

1. Does the error category match the actual failure: invalid input, authentication failure, authorization denial, business rejection, conflict/idempotency, dependency failure, or internal error?
2. Does the caller receive enough information to recover or debug without exposing sensitive internals?
3. Are expected denials represented as expected outcomes rather than unexpected exceptions?
4. Is there any hidden fail-open or silent fallback behavior?
5. Are retries safe, explicitly discouraged, or bounded by idempotency?

Prefer explicit error semantics over catch-all internal errors.

### Observability Gate

For important state changes, security boundaries, external calls, and failure paths, ask:

1. Is there enough logging or telemetry at the boundary where the failure can be understood?
2. Does the log include useful correlation context, such as request id, actor id, resource id, route/action, external dependency name, and sanitized error reason?
3. Is sensitive data excluded or redacted, such as tokens, secrets, credentials, authorization headers, personal data, and raw payloads?
4. Is logging placed at the ownership boundary instead of duplicated across every helper?
5. Are expected business denials distinguishable from unexpected system failures?

Prefer concise boundary logs over noisy internal logs.

### Configuration And Secret Gate

For each new configuration or secret, ask:

1. Is this configuration required by the current contract, or can the behavior be fixed and simpler?
2. Is the default behavior explicit and safe for production?
3. If a required value is missing, should the system fail closed, fail open, or start disabled? Is that choice documented near the boundary?
4. Are secrets provided through environment or secret management placeholders rather than committed plaintext?
5. Are secrets excluded from logs, errors, tests, snapshots, and generated docs?
6. Is rotation or revocation relevant now, or intentionally out of scope?

Prefer fewer configuration knobs. Add configuration only when deployment variance is real.

### State And Concurrency Gate

When the change introduces state transitions, one-time use, creation, exchange, or idempotency, ask:

1. What is the source of truth for the state?
2. What are the allowed states and transitions?
3. What happens on duplicate requests, concurrent requests, retries, and partial failures?
4. Is idempotency handled at the business boundary, storage boundary, or both?
5. Are race-sensitive invariants covered by tests or constrained by storage primitives?
6. Is time read from the correct source for this layer?

Prefer explicit state transitions and tested invariants over implicit best-effort behavior.

### Test Intent Gate

For tests added or changed, ask:

1. Does each important contract have a direct test, including rejection and edge paths?
2. Does the test name describe the behavior or invariant, not only the function under test?
3. Did user-reported concerns become regression tests when practical?
4. Are tests scoped to the risk of the change without overfitting implementation details?
5. Are mocks/fakes asserting meaningful boundary data rather than only returning success?

Prefer behavior-focused tests that explain why the rule exists.

### Code And Documentation Alignment Gate

When code changes behavior, contracts, configuration, API shape, defaults, or operational expectations, ask:

1. Do current-fact docs describe the implemented behavior, not an older or planned behavior?
2. Do tests encode the same contract described by the docs?
3. Are examples, commands, config names, API names, and error semantics consistent across code, tests, and docs?
4. If docs were not updated, is that because the change does not affect user-visible or operator-visible behavior?

Prefer keeping code, tests, and current-fact docs aligned over treating documentation as a separate cleanup task.

### Same-Class Scan Gate

When the user points out one issue, scan for the same class before editing:

1. Similar redundant fields or concepts.
2. Similar over-defensive branches.
3. Similar naming or terminology drift.
4. Similar documentation/test/proto inconsistencies.

Tell the user what same-class scan was done, then make one coherent pass where possible.

### Iteration Scope Gate

When the repository has its own documented feature-planning convention, follow that convention first. If the repository has no explicit convention, use this default cross-project structure:

```text
docs/plans/<feature>/
  README.md
  design.md
  implementation-plan.md
  iterations/
    01-initial.md
  review*.md
```

Default file responsibilities:

1. `README.md`: the single entry point for the feature docs; records current status, timeline, document navigation, and maintenance rules.
2. `design.md`: the current effective design only; do not stack rejected proposals, old configs, or historical alternatives here.
3. `implementation-plan.md`: current implementation state, remaining gaps, tasks, acceptance criteria, and executable verification.
4. `iterations/`: historical evolution records; use numbered files such as `01-initial.md`, `02-*.md`, `03-*.md`.
5. `review*.md`: review records and quality context; useful history, but not the current design source of truth.

Before adding a new feature iteration document, ask:

1. Has the current iteration already been submitted or stabilized?
2. Does the change alter a settled capability boundary, responsibility boundary, default behavior, or configuration contract?
3. Is this just a correction to the current unsubmitted iteration?

If the current iteration is still in progress, treat most contract wording or rule changes as adjustments to that iteration rather than creating a new iteration. Do not let rejected temporary designs pollute current `design.md`.

Add a new iteration when the change alters a settled capability boundary, responsibility boundary, algorithm, configuration semantics, or default behavior. Do not add a new iteration for ordinary bug fixes, test additions, local renames, or corrections to an unsubmitted/current iteration unless they change the current contract.

When an iteration changes the active contract, update all current-fact documents together: `README.md`, `design.md`, and `implementation-plan.md`. Keep rejected or superseded approaches in `iterations/`, and mark them as not adopted if they are listed in the timeline.

Before delivery, scan current-fact docs for stale wording in the language used by the project. Include at least these meaning groups:

1. Unresolved status: `待确认`, `to be confirmed`, `TBD`, `open question`, `pending confirmation`.
2. Legacy configuration or behavior: `旧配置`, `legacy config`, `old config`, `previous behavior`, `legacy behavior`.
3. Deprecated or removed facts: `已废弃`, `deprecated`, `removed`, `obsolete`, `no longer used`.
4. Future-tense implementation language in current facts: `后续实现应`, `should implement later`, `future implementation should`, `to be implemented`.
5. Obsolete API names, obsolete config names, and rejected terminology from the just-finished iteration.

### Rework Stop Gate

If the same concern has been revised five or more times, pause and tell the user:

> This point has been revised at least five times. The contract still looks unstable; I recommend pausing implementation and realigning responsibility boundary, necessity, and acceptance criteria before more edits.

Do not keep pushing through by inventing more implementation changes.

## Output Shape

Use this order:

1. Findings by severity, with file references when reviewing code.
2. Same-class scan result.
3. Required fixes or proposed simplifications.
4. Norms checked.
5. Verification already run or still needed.

Keep the report concise. Do not turn this skill into a full code review unless the user asked for a review.

Example:

```text
Findings:
- P1 path/to/file.go:42: The retry branch can execute a non-idempotent operation twice; move idempotency to the use-case boundary or storage constraint.

Same-class scan:
- Checked related retry and creation paths; no second non-idempotent retry path found.

Required fixes:
- Add an idempotency guard before retrying the operation.

Norms checked:
- Boundary And Defense Gate, State And Concurrency Gate, Test Intent Gate.

Verification:
- Still needed: go test ./...
```

If there are no findings, state that directly, then list any residual risk and verification still needed.
