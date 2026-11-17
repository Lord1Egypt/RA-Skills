# Worker Execution and Review

## Contents

- Roles and launch gates
- Worker execution receipts
- Reviewer inputs and outputs
- State, commits, and notifications

## 1. Default roles

- Worker: `gpt-5.6-sol/high`.
- Reviewer mode: `inherited_subagent` by default; it inherits the Worker's model and reasoning.
- Explicit `self_review` creates no separate Reviewer and must not be described as independent.
- An independent Reviewer must not review code or artifacts it implemented or integrated.
- A requested model is not effective until the target creation, configuration handshake plus formal dispatch, current-task audit, or explicit subagent spawn has an enforcement receipt.
- If a requested configuration is unavailable, stop before execution and record `mismatch`; do not silently accept a fallback while claiming the request.

The Reviewer may be the read-only current task, a separate task, or a nested subagent. For a single Worker, default to a full-history Worker-managed subagent created after task/code reading but before active Goal creation, implementation reasoning, or product writes. `self_review` is available only when selected in the launch configuration.

Apply [session-topology.md](session-topology.md) before launch. Record how the selected topology excludes implementation context; a pre-execution fork is one valid construction, not the only one.

## 2. Worker launch gates

Before starting, the Worker must:

1. read project rules, all required package documents, and its assigned GOAL;
2. inspect coordination state, current HEAD, working tree, and write scope;
3. verify that every material design gate is closed;
4. verify that the validation matrix is frozen;
5. verify explicit user authorization and the absolute GOAL path, but do not create the active Goal until the Reviewer readiness gate below passes;
6. leave token budget unset unless the user specified one;
7. record Worker/Reviewer task or subagent IDs, session modes, sources, owners, and independence construction;
8. verify an `enforced` model/reasoning receipt for every assigned context;
9. apply the confirmed review mode: create the default full-history inherited Reviewer and record `READY_REVIEW`, or record `SELF_REVIEW_READY` without creating a subagent;
10. for independent review, verify that the Reviewer context excludes implementation reasoning for this batch;
11. only then create the Worker active Goal, record its ID in the technical receipt, and begin implementation.

## 3. Per-item execution receipts

Record at least:

- baseline commit, data version, runtime configuration, or evidence snapshot;
- actual modified or operated paths;
- implementation details and rationale;
- deviations from frozen design;
- added or changed tests and checks;
- exact commands, exit states, counts, and durations;
- failures, interruptions, timeouts, and retries;
- commit, artifact, checkpoint, or trace locator;
- residual risk;
- self-review conclusion.

Do not report interrupted or failed commands as passing. Broad tests supplement but do not replace focused negative evidence.

## 4. Reviewer inputs

A review request must identify:

- work-item ID;
- exact design location;
- execution-record location;
- exact commit, diff, artifact, or checkpoint;
- commands and results already run;
- known risks and untested scope;
- the only review document the Reviewer may modify.

The Reviewer must inspect the real implementation or artifact, not only the Worker summary or test names.

## 5. Review outputs

Append a record for every iteration containing:

- time, Reviewer identity, requested model/reasoning, enforcement receipt, and actual settings when observable;
- exact reviewed snapshot;
- design-conformance analysis;
- positive and negative validation quality;
- `P0/P1/P2/P3` findings;
- evidence, impact, recommended repair, and recommended validation for each finding;
- per-item `approved` or `rework_required` verdict;
- part-level integrated-audit verdict;
- uninspected scope and residual risk.

### 5.1 Finding materiality and disposition

Severity is not assigned from theoretical possibility alone. Evaluate each finding by owned business impact, plausible reachability, evidence strength, and whether the task or public contract promises the behavior.

Classify every observation as one of:

- `blocking`: violates a confirmed business path or acceptance criterion, a real consumer-facing contract, or a high-consequence persistence/authorization/identity/concurrency/recovery/security invariant;
- `follow_up`: useful defense-in-depth or maintainability improvement that does not prevent the supported task from working correctly;
- `out_of_scope`: speculative, impossible under current invariants, owned by another layer, or outside documented input limits.

`P0/P1` are normally blocking when evidenced. `P2` blocks only with realistic reachability, an explicit contract, or high-consequence impact. Long-tail `P2` cases such as thousand-level JSON nesting, extreme payload sizes, or raw lower-level parser failures are non-blocking unless the application explicitly owns and supports that boundary. `P3` never blocks unless the task explicitly promotes it to acceptance scope.

Do not require bespoke wrappers, schema expansion, or broad negative matrices for non-blocking observations. Consolidate them into one residual section. The first review should return all blocking findings it can identify; focused re-review must not reopen unrelated speculative hardening.

An inherited Reviewer is read-only for product files and writes only its review record. In `self_review`, the Worker writes a concise record covering exact snapshot, design/document coverage, validation, findings, residual risk, and `SELF` verdict. Approval requires no open `blocking` finding; unresolved `follow_up` or `out_of_scope` observations remain visible but do not force rework.

## 6. State transitions

```text
pending
  -> Worker completes the item and records evidence
     -> implemented_pending_review
        -> selected review mode rework_required: remain in this state; Worker repairs
        -> selected review mode approved: Worker verifies REVIEW or SELF receipt and marks approved
```

Any later relevant implementation change invalidates the old approval. Return the item to `implemented_pending_review` and review the new exact snapshot.

## 7. Commit gates

Unless project policy says otherwise:

- use a reviewable commit for a coherent item or closed slice;
- keep every intermediate commit loadable and runnable;
- exclude unrelated changes;
- review an exact commit or explicitly identified staged diff;
- inspect sensitive files, process-document commit rules, generated artifacts, and the working tree before final commit;
- do not modify or commit code when the user requested review only.

## 8. Notifications

- A dispatched Worker notifies the parent task when blocked, when a design decision is needed, when review is ready, and when work completes.
- A Worker operating directly in the current user task reports normally and does not notify itself.
- A Reviewer notifies the Worker or Orchestrator with the review-record path and exact verdict.
