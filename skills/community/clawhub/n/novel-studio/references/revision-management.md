# Revision Management

## 1. Goal

Allow the agent to detect likely revision feedback from normal conversation, ask the user for confirmation, determine scope, and then revise affected outputs without breaking workflow consistency.

This mechanism exists so the user does not always need to issue rigid commands like `反馈：` before the system can react.

---

## 2. Core rule

The agent may proactively detect likely revision feedback from ordinary conversation.

However, detection alone does **not** authorize automatic modification.

Before applying changes, the agent must:
1. summarize the detected feedback
2. classify the feedback type
3. identify likely affected scope
4. identify conflicts with prior settings if any
5. ask the user whether to record it as formal feedback
6. ask whether to revise prior settings, add a new rule, or only adjust the current batch

---

## 3. Feedback types

Common types include:
- style feedback
- plot feedback
- character feedback
- structure feedback
- direction feedback

The type should shape the impact analysis.

---

## 4. Required confirmation questions

When likely revision feedback is detected, the agent should explicitly confirm:
- whether this should be recorded as formal feedback
- what files or stages it likely affects
- whether it conflicts with prior settings
- whether the user wants to override prior settings or add a new constraint

---

## 5. Override vs add-on rule

The agent must distinguish between:
- overriding an earlier decision
- adding a new requirement on top of the earlier decision

If unclear, ask.

---

## 6. Scope analysis rule

Before revising outputs, analyze whether the feedback affects:
- only the current batch
- the current stage outputs
- upstream planning or character assets
- discovery-level project positioning

Do not treat all feedback as local.

---

## 7. Revision order rule

When revision is confirmed, revise in this order:
1. upstream constraint files or planning assets
2. current operational files
3. downstream content files
4. recap and state

This prevents internal project contradictions.

---

## 8. Formal revision record

When a revision is confirmed as formal, record:
- feedback summary
- feedback type
- affected scope
- whether earlier settings were overridden
- revision status

Recommended artifact:
- `06_反馈与修订.md`

This file should remain the canonical human-readable revision record for:
- the current active formal revision
- the latest closed formal revision
- current revision gate
- current scope / conflict / plan summary
- latest revision result summary

---

## 9. State requirement

The state file should reflect:
- revision active / inactive
- latest formal feedback summary
- affected stages and files
- override mode
- scope summary
- conflict summary
- revision plan summary
- revision result summary
- current revision gate
- whether revision results are awaiting user approval
- latest closed revision snapshot

---

## 10. Lifecycle gates

For the formal revision workflow, use these gates:
- `awaiting_revision_scope_confirmation`
- `awaiting_revision_plan_approval`
- `awaiting_revision_result_approval`

Do not silently invent extra gate names for this lifecycle unless the workflow itself is expanded.

---

## 11. Revision actions

When using helper scripts or equivalent internal actions:
- `record_revision_feedback` starts a formal revision and opens the scope-confirmation gate
- `update_revision_scope` records affected stages/files and opens the plan-approval gate
- `result_pending` records the revision result and opens the result-approval gate
- `close` closes the active revision after approval and preserves the latest closed snapshot
- `reject` keeps the revision active, records the rejection reason, and sends the workflow back to plan approval

---

## 12. Hard safety rule

Do not silently modify previously approved outputs based only on an ambiguous conversational remark.

If the feedback may materially affect prior files or stage logic, confirm first.
