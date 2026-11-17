# Long-Horizon Plans — Multi-Day, Multi-Session, Handoff

A plan that lives only in the conversation dies with the session. This file covers persisting plans, resuming them safely, milestone planning, handoff, and closing them out.

## Persisting the Plan

- L3+ plans — and any L2 when `plan_artifact: file` (SKILL.md, Configuration) — live at `~/Clawic/data/plan/active/<yyyy-mm-dd>-<goal-slug>.md`.
- The file holds: the plan doc, per-step status (done + check result / in progress / pending), deviations so far with their whys, and a "Next action" line.
- Next action is an executable instruction ("run the migration dry-run against the staging copy; expect 14,210 rows"), never a topic ("continue migration").

## Resume Protocol

1. Read the active file; trust its statuses over your memory of the work.
2. Re-run the cheapest check of the last done step — the world moves between sessions: dependencies update, files change, backups rotate.
3. Idle longer than `stale_after_days` (SKILL.md, Configuration) → re-validate the riskiest assumption before resuming.
4. Idle longer than 4x `stale_after_days` → re-run the full planning decision: salvage completed steps, replan the rest.
5. Recovery windows may have expired (`risk.md`, Irreversibility Taxonomy): re-verify every rollback still works before the next irreversible step.

## Milestone Planning

- Detail decays (SKILL.md, Plan Format): the current milestone in steps, later milestones as one line each with their own done-check.
- At each milestone boundary, plan the next milestone in step detail using what the finished one taught, and re-estimate the remaining milestones (`estimation.md`, Re-Estimating Mid-Plan) — the boundary is the cheapest moment to be wrong about the rest.
- A milestone is independently valuable: if the plan died here, what is shipped still stands (`decomposition.md`, Altitude).

## Handoff

- The active file IS the handoff: a fresh session — or a different agent — must be able to execute Next action without the conversation history. Test: does the file name the paths, the expected outputs, and the open decisions, or does it say "as discussed"?
- Deviations travel in the file: the next session's replan trigger counts from recorded deviations, not from zero (`replanning.md`).

## Concurrency

One active plan per goal. A second plan touching the same system gets a conflict line naming the shared resource and which plan owns changes to it until when — two plans silently editing the same schema is how both of their checks pass and the system still breaks.

## Completion

On done or abandoned: append the outcome record (`outcomes.md`), then delete the active file. The log is the memory; `active/` holds only live work — a graveyard of stale actives makes every resume slower and every concurrency check noisier.
