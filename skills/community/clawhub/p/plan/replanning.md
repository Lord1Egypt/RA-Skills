# Replanning — Deviations, Blocks, Abandonment

A plan is a forecast, not a commitment. This file is what to do when reality disagrees: which deviations trigger a replan, how to replan without losing finished work, and when to stop entirely.

## Deviation Taxonomy

| Deviation | Counts toward the 2-consecutive trigger? | Response |
|---|---|---|
| Step skipped | Yes | Record why it seemed skippable |
| Steps reordered | Yes | Record what forced the order change |
| Output differs from the stated check | Yes | Record the gap |
| Step blocked externally | No — it is a block | Blocked Step protocol below |
| Human adds scope mid-flight | No — immediate decision | Bolt-on test below |
| Assumption falsified | No — immediate replan | Replan procedure below |

The trigger itself (canonical: SKILL.md, Executing Against The Plan): 2 consecutive counted deviations → stop and replan. One deviation is noise; two consecutive means the model of the task is wrong, and patching step-by-step is executing a plan you know is broken.

## Replan Procedure

1. Stop executing.
2. List completed steps whose checks passed — they survive. Steps "done" without a passing check re-enter as work.
3. Re-run the planning decision on the remaining work — signals may have changed class (something reversible may now be recoverable-at-cost).
4. Head the new plan: "Replaces plan of [date] at step N — cause: [the deviation or falsified assumption]."
5. L3+: re-approval (`approval.md`). L2: announce the replacement, then continue.
6. Log the replan (`outcomes.md`) — replan records are the highest-signal entries the learning loop gets.

## Blocked Step

- One timeboxed unblock attempt; state the box before starting ("20 minutes on the auth error, then I escalate").
- Parallel-safe steps exist (nothing depends on the blocked one) → park the block, continue, and say so.
- Nothing parallel-safe → escalate with three things: the blocker, what was tried, the specific decision or access needed. "I'm blocked" without those three re-blocks on the reply.

## Mid-Flight Scope Change

Bolt-on test — BOTH must hold: the request touches files/systems already in the plan, AND it adds no new irreversible step.

- Both hold → add as a named step with its own check, announce it, adjust the estimate (`estimation.md`, Re-Estimating Mid-Plan).
- Either fails → separate plan. Default order: finish the current plan first; offer the swap explicitly, never silently interleave two plans.

## Sunk Cost

Completed steps justify nothing. The only question: from the current state, does the remaining work still reach the goal more cheaply than any alternative — including stopping? Time already spent appears nowhere in that question. If you notice yourself defending the plan because of how much of it is done, that is the signal to re-run the question.

## Abandonment

- Abandon when the **goal** is invalidated: the need disappeared, or the riskiest assumption was falsified with no viable pivot. A merely wrong plan is a replan, not an abandonment.
- Salvage pass before closing: artifacts with passing checks worth keeping, the rollback of any half-done irreversible work, and the lesson.
- Record ❌ with the falsified assumption named (`outcomes.md`). An abandoned plan with its lesson recorded is cheap tuition; unrecorded, it is pure loss — and the next plan pays it again.
