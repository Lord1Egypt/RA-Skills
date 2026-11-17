---
name: Plan
slug: plan
version: 1.0.3
description: >-
  Plans tasks before execution: decides when to plan vs act directly, sizes plan depth to
  risk, and structures steps, estimates, and rollbacks. Use when work has multiple steps,
  dependencies, or irreversible actions (deploys, migrations, deletions, sending anything
  external), when success criteria are unclear or an estimate would be a guess, when
  execution drifts off plan or a one-shot attempt failed, when resuming or handing off
  multi-day work, or when the user asks to plan, scope, break down, or estimate a task.
  Not for personal productivity systems or time blocking (that is productivity).
homepage: https://clawic.com/skills/plan
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🗺️
    displayName: Plan
    configPaths: ["~/Clawic/data/plan/"]
---

User preferences, the outcome log, and active plans live in `~/Clawic/data/plan/` (see `setup.md` on first use). If you have data at an old location (`~/plan/` or `~/clawic/plan/`), move it to `~/Clawic/data/plan/`.

## When To Use

- A task has multiple steps, dependencies between them, or any irreversible action (deploy, migration, delete, send)
- Success criteria are unclear, or the estimate would be a guess
- The user asks for a plan, breakdown, scoping, or estimate before work starts
- Execution has drifted from an existing plan, or a one-shot attempt just failed
- Resuming or handing off work that spans sessions or days
- Not for personal productivity systems, time blocking, or calendars — that is `productivity`
- Not for managing a portfolio of ongoing projects — that is `projects`

Modes: act-as (plan your own execution — the default) and advise (draft a plan the user will execute); both use the same depth rules. Always make the risk decision first, even when the answer is "no plan needed".

## Quick Reference

| Situation | Do this |
|-----------|---------|
| Done before successfully, fully reversible | Execute directly (L0) |
| Single deliverable, ≤30 min (`quick_task_minutes`), reversible | Think through steps, no doc (L1) |
| Multi-step, >30 min, or any irreversible step | Bullet plan, share with human (L2) |
| Dependencies across components, or spans >1 day | Milestone plan with checkpoints (L3) → `long-horizon.md` |
| High stakes AND novel task type | Full plan, human validation before step 1 (L4) → `approval.md` |
| Estimate high/low ratio >3x | Spike first → `estimation.md`, `strategies.md` |
| A step has no attachable done-check | Convert to decision doc or spike → `decomposition.md` |
| Execution drifting from the plan | 2-consecutive-deviation trigger → `replanning.md` |
| Step blocked, or scope added mid-flight | Block and bolt-on protocols → `replanning.md` |
| Human approves instantly, or "just do it" | → `approval.md` |
| Resuming yesterday's (or last week's) plan | Resume protocol → `long-horizon.md` |
| Anything else / unsure | Plan at L2 — the cost is asymmetric (Core Rule 8) |

Depth on demand: `decomposition.md` steps, altitude, done-checks · `estimation.md` ranges, spikes, calibration · `risk.md` irreversibility, rollback, blast radius · `strategies.md` sequential, parallel, iterative, spike, checkpoint · `replanning.md` deviations, blocks, abandonment · `approval.md` validation, checkpoints, scope changes · `long-horizon.md` multi-day, resume, handoff · `outcomes.md` logging and learning · `setup.md` first use.

## Core Rules

1. **A plan's value is the risk decision, not the step list.** Force it early: what single assumption could invalidate the whole approach, and can it be tested cheaply first? A to-do list with no risk ordering adds ceremony, not safety (`risk.md`).
2. **Depth = the highest level any single signal triggers, never an average.** A 20-minute task with one irreversible step is L2, not L1 — the short duration does not dilute the irreversibility.
3. **Irreversibility dominates.** One irreversible step anywhere forces at least L2 — you cannot iterate your way out of a deleted database or a sent email. Classification and blast radius in `risk.md`.
4. **Every step carries an observable done-check.** A step you cannot attach a check to is not a step, it is a hope: "investigate X" becomes "decision doc: X vs Y, with the pick". Check catalog in `decomposition.md`.
5. **Order by information, not convenience.** The step most likely to invalidate the plan goes as early as dependencies allow. Migration example: write and test the rollback script as step 1, not last — if rollback is impossible, you want to know before touching data.
6. **Estimates are ranges; ratio >3x means spike first.** If the high/low ratio exceeds 3x, that is not an estimate, it is an unknown. 2-8h (4x) → spike; 3-6h (2x) → plan. Building and calibrating ranges in `estimation.md`.
7. **Detail decays past the first unknown.** Steps written beyond it are speculation you will rewrite. Plan in steps to the first checkpoint; milestones beyond (`long-horizon.md`).
8. **When uncertain, plan — the cost is asymmetric.** A bullet plan costs minutes; a failed one-shot costs the redo plus the cleanup plus the trust.

## The Planning Decision

Before executing, scan for signals:

| Signal | One-shot OK | Plan needed |
|--------|-------------|-------------|
| Task done before successfully | ✅ | |
| Clear single deliverable | ✅ | |
| Reversible if wrong | ✅ | |
| Multiple components | | ✅ |
| Dependencies between steps | | ✅ |
| Any irreversible step | | ✅ |
| Touches production data or external users | | ✅ |
| Ambiguous success criteria | | ✅ |
| Estimated > `quick_task_minutes` of work | | ✅ |

**Reversible vs recoverable** — the distinction that decides the column: reversible means undo restores the prior state (git revert); recoverable means a good state is reachable at a cost (restore last night's backup, lose a day of writes). Recoverable-at-cost counts as "plan needed", not "reversible" — full taxonomy and recovery-window decay in `risk.md`.

## Plan Depth Levels

| Level | Trigger | Format |
|-------|---------|--------|
| L0 | Done before successfully, fully reversible | Execute directly |
| L1 | Single deliverable, ≤ `quick_task_minutes`, reversible | Think through steps; no doc |
| L2 | Multi-step, or > `quick_task_minutes`, or any irreversible step | Bullet plan shared with the human |
| L3 | Dependencies between components, or spans >1 day | Milestone plan with checkpoints; persisted (`long-horizon.md`) |
| L4 | High stakes AND novel (this task type never done) | Full plan; human validation before step 1 (`approval.md`) |

Depth = highest single signal (Core Rule 2). Per-type learned defaults override this table once the outcome log has evidence (`outcomes.md`, Current Defaults).

## Plan Format (L2-L4)

```
📋 Plan: [goal]

Why planned: [the signal that triggered planning — one line]

Steps:
1. [step] — [observable output that proves it is done]
2. [step] — [observable output]
3. [step] — [observable output]

Riskiest assumption: [what invalidates the approach] — tested in step [N]
Irreversible steps: [numbers] — rollback: [how, tested in step M] (or "none" + mitigation)

Estimate: [low–high range] — high end fires if [driver]
Validation: [none | human approves before step N]

[The specific question, not "Ready to start?" — approval.md]
```

Rules that make the format work:

- **3-7 steps.** More than 7 means wrong altitude: group into milestones and plan only the first milestone in step detail (`decomposition.md`).
- Every step passes the done-check test (Core Rule 4); activity verbs get converted before the plan ships.
- The rollback is itself a step with a check, placed before the irreversible step (`risk.md`, Rollback Design).
- Scan the hidden-steps checklist — rollback, backup+restore-verify, post-change verification, comms, cleanup, monitoring (`decomposition.md`, The Steps Nobody Writes).

## Executing Against The Plan

- Approval covers what is written. At L3+, a materially different execution needs re-approval, not a retroactive mention — what counts as material is defined in `approval.md`.
- **Replan trigger:** when 2 consecutive steps deviate from plan (skipped, reordered, or output differs from stated), stop and replan instead of patching step-by-step. One deviation is noise; two consecutive means the model of the task is wrong. Deviation taxonomy, blocked steps, scope changes, and the replan procedure: `replanning.md`.
- Record every deviation in the outcome log — deviations are the raw material for next time's plan (`outcomes.md`).

## Learning Loop

Learning rates are asymmetric because evidence costs are asymmetric:

- **Promote depth after ONE failure** attributable to plan depth — and name what the deeper level would have caught. If you cannot name it, it was not a planning failure and no promotion happens.
- **Demote depth after 3 consecutive successes** where the extra depth went unused. Observable signal: plan sections never consulted during execution.
- **Auto-execute after 5 consecutive successful validated runs** of a plan type: ask "Should I auto-start [type] plans without validation?" One failure resets the streak and restores validation. The bar is higher than demotion because this removes a human safety net, not just ceremony. Types in `always_validate` never auto-execute.

Per-type state lives in the Current Defaults block of `~/Clawic/data/plan/outcomes.md`:

```
### Auto-Execute (validation waived by human)
- refactor/small: L2 [streak: 7]

### Validate First
- migration/data: L4 [always — in always_validate]

### Learning
- api/integration: L2, streak 3/5 toward auto-execute proposal
```

Logging: append a record after every L2+ task; L0/L1 only when they failed (a failed "trivial" task is evidence the type needs promotion). Strategy verdicts need a why — "Parallel → merge conflicts" teaches; "Parallel → didn't work" does not. Record format, last-5 analysis, and review cadence: `outcomes.md`.

## Output Gates

Before sharing a plan (L2+), verify:

- Riskiest assumption named, with the step number that tests it?
- Every step has an observable output — no bare activity verbs?
- Irreversible steps listed with a tested rollback, or "none" plus a mitigation?
- Estimate is a range with ratio ≤3x — otherwise did I propose a spike instead?
- Depth equals the highest signal triggered, and `always_validate` types have validation on?
- The closing question is specific enough that its answer proves the plan was read (L3+)?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/plan/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| quick_task_minutes | number (minutes) | 30 | Sets the L1/L2 boundary in the depth table and the "estimated >" signal in The Planning Decision |
| plan_artifact | chat \| file | chat | Where L2 plans live; `file` writes them to `~/Clawic/data/plan/active/` like L3+ (`long-horizon.md`) |
| always_validate | list of task types | migration/*, external-send/* | Types where human validation never demotes and auto-execute is never proposed, regardless of streaks |
| stale_after_days | number (days) | 7 | Resuming a plan idle longer than this re-validates the riskiest assumption first; 4x this forces a full replan (`long-horizon.md`) |

Preference areas to record as the user reveals them:

- **thresholds** — replan sensitivity, promotion/demotion streak lengths, review cadence — affects Learning Loop and `outcomes.md` triggers
- **format** — estimate units, plan verbosity, language of plan docs — affects Plan Format output
- **approval** — task types the user wants to see planned regardless of size, preferred checkpoint question style — affects `approval.md` conduct
- **scope** — domains where the user prefers one-shot execution (bias one level down, irreversibility floor stays) — affects per-type depth defaults

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Planning as procrastination: detailing steps past the first unknown | That detail is speculation; you will rewrite it after the unknown resolves | Steps to the first checkpoint, milestones beyond |
| Steps written as activities ("investigate X") | No observable output means no done-check; plans drift silently | Every step names the artifact or check that proves completion (`decomposition.md`) |
| Uniform depth for every task | L4 on trivial work trains the human to skim-approve; L1 on novel work ships failures | Depth table + learned per-type defaults |
| Sticking to a plan reality has contradicted | A plan is a forecast, not a commitment; adherence becomes sunk cost | 2-consecutive-deviation replan trigger (`replanning.md`) |
| Point estimates | Read as commitments and hide uncertainty | Range with a named high-end driver; ratio >3x → spike first |
| Per-step buffers | Silently consumed; they hide the true range | One plan-level range — the low-high gap IS the buffer (`estimation.md`) |
| Skipping the unwritten steps: rollback, restore-verify, post-change verification, comms | Plans fail disproportionately on steps that were never written | Hidden-steps checklist at plan time (`decomposition.md`) |
| Executing beyond approved scope without saying so | Approval covers the written plan only; burned trust raises validation on everything after | Announce deviations at the deviation; re-approve at L3+ (`approval.md`) |
| Treating silence as approval | An unread validation request protects nobody | Reversible prep only; never cross an irreversible boundary on silence (`approval.md`) |
| Resuming a stale plan blindly | The world moved: dependencies, backups, assumptions | Resume protocol; re-validate past `stale_after_days` (`long-horizon.md`) |
| Logging only failures | Success streaks are what earn auto-execute; unlogged successes mean validating forever | Log every L2+ outcome, success included |

## Where Experts Disagree

- **The plan document vs the planning act.** "Plans are worthless, planning is everything" (Eisenhower) is half right: the act is always worth it; the artifact pays only at boundaries — human validation, multi-session resume, handoff. Solo reversible work → think, don't write; anything crossing a boundary → write.
- **Estimate in time vs relative size.** Relative sizing (points) pays only with a stable velocity to convert it — a team asset. An agent's equivalent is the per-type calibration multiplier from its own outcome log; with that log, time ranges are strictly more informative.
- **Upfront depth vs iterate-and-see.** Iterate when feedback is cheap and steps are reversible; plan upfront when feedback is expensive or steps are irreversible. The depth table IS that frontier — the disagreement dissolves once irreversibility is priced.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/plan (install if the user confirms):

- `decide` — choose between options inside a plan step
- `escalate` — ask-vs-act boundaries beyond planning scope
- `self-improving` — general execution lessons; plan keeps only planning lessons
- `memory` — long-term context and user continuity beyond planning records
- `productivity` — personal productivity systems, time blocking, and reviews; plan covers executing a single task

## Feedback

- If useful, star it: https://clawic.com/skills/plan
- Latest version: https://clawic.com/skills/plan

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/plan.
