---
name: project-workflow-scheduler
description: Break a project, objective, or task list into safe, bounded one-time OpenClaw cron work blocks with dependencies, risk classification, and strong isolated agentTurn payloads. Use when an agent needs to stage multi-step work over time without autonomy theater, especially for overnight blocks, next-day follow-up, recap jobs, checkpoints, low-risk internal analysis, documentation cleanup, audits, asset prep, CRM cleanup, support follow-up, or phased project execution.
---

# Project Workflow Scheduler

Turn a multi-step project into a supervised sequence of one-time cron jobs.

## Use this pattern

1. Evaluate whether the work is cron-friendly.
2. Break it into bounded blocks.
3. Classify each block.
4. Schedule only the safe blocks.
5. Document what was scheduled and why.
6. Reassess after results before scheduling the next risky phase unless the user already approved the full sequence.

Use the cron tool to propose or create one-time isolated `agentTurn` jobs. Bias toward fewer, better, well-scoped jobs.

## Decide if a block is cron-friendly

Prefer blocks that are:
- clearly scoped
- auditable
- low-risk or reversible
- likely completable in one run
- rich enough in context that a future isolated run can succeed without the parent session

Good candidates:
- project documentation cleanup
- page or site audits
- asset curation
- follow-up checks
- support-ticket follow-up prep
- prep for the next project phase
- safe internal analysis work
- low-risk build prep tasks
- recap, QA, and checkpoint passes

Do not schedule:
- live login flows
- interactive browser approval flows
- customer-facing sends without explicit approval
- destructive actions
- infra or config changes without explicit approval
- purchases or commitments
- vague "keep working until done" missions
- work that depends on unstable browser state or fresh credential prompts
- work that will likely require repeated subjective decisions from the user

## Classify every block

Use exactly these buckets:
- **Safe to schedule**
- **Needs user approval first**
- **Blocked by missing access**
- **Should never be scheduled unattended**

If a block is not clearly in the first bucket, do not schedule it.

## Break work into blocks

Keep blocks small enough to finish in one run. Prefer fewer, better blocks over many tiny ones.

For each block define:
- **Block name**
- **Objective**
- **Inputs/context to include**
- **Preconditions**
- **Earliest safe run time**
- **Expected output**
- **Announce results or not**
- **Whether a follow-up block should be scheduled later**

Split large work by:
- phase
- dependency
- risk boundary
- handoff point
- natural checkpoint

Examples of clean splits:
- audit -> recap -> implementation prep
- cleanup -> QA -> follow-up
- research -> asset prep -> doc update
- migration audit -> staged change block -> verification block

Avoid stuffing multiple fragile decisions into one run.

## Handle dependencies

Mark each block as one of:
- independent
- depends on earlier block output
- depends on user approval
- depends on missing access

If later work depends on likely outputs from earlier runs, write the later block so it explicitly references the expected artifacts or decisions to look for.

Do not pre-schedule risky downstream blocks unless the user already approved that sequence.

## Write strong cron payloads

Assume isolated `agentTurn` runs.

Every scheduled block prompt should include:
- the project name and current phase
- the exact scope of this block
- what already happened
- what inputs/files/systems to inspect
- what to produce by the end of the run
- what not to do
- how to report blockers
- whether to recommend the next block instead of executing it

Good payload traits:
- bounded
- concrete
- context-rich
- explicit about success criteria
- explicit about forbidden actions

Good prompt shape:

```text
Project: <name>
Block: <name>
Objective: <one clear outcome>

Context:
- <important prior state>
- <known files, folders, systems, links>
- <assumptions that are safe>

Do:
- <step 1>
- <step 2>
- <step 3>

Do not:
- <unsafe or out-of-scope actions>
- <customer-facing or destructive work>

Expected output:
- <deliverable>
- <short recap>
- <recommended next block if appropriate>

If blocked:
- report the blocker, what you tried, and the safest next step
```

## Avoid autonomy theater

Do not present scheduled work as autonomous ownership.

The point is to create supervised, accountable work blocks that:
- run later
- stay bounded
- leave an audit trail
- make reassessment easy

Prefer:
- checkpoint jobs
- recap jobs
- verification jobs
- prep jobs
- follow-up jobs

Not:
- giant open-ended production runs
- fuzzy missions with no stopping rule
- chains that assume too much hidden context

## Scheduling guidance

Prefer one-time jobs over recurring jobs for project orchestration.

Common patterns:
- same-night audit, prep, or cleanup block
- next-morning recap block
- next-day follow-up block after review
- staged overnight sequence where each later block is safe only if earlier output is likely predictable

Bias toward manual reassessment before scheduling the next risky phase.

## Documentation guidance

When orchestration materially changes project state, recommend updating project docs so future sessions know:
- what was scheduled
- why it was scheduled
- dependencies and assumptions
- what results to look for next

If useful, suggest a short handoff note or README update.

## Output format

Produce:
1. **Short orchestration plan**
2. **Block-by-block schedule proposal**
3. **Recommended cron payload text for each scheduled block**
4. **Assumptions, dependencies, and risks**
5. **Doc update suggestions** if orchestration materially changes project state

If the user has not yet approved scheduling, stop at the proposal. If the user already approved scheduling, create only the safe blocks and clearly note what still requires reassessment or approval.

## Example set

Read `references/examples.md` when you need concrete patterns for:
- website migration overnight blocks
- CRM cleanup
- support follow-up chain
- audit + recap + next-step sequence
- multi-phase projects where only early phases are safe to pre-schedule
