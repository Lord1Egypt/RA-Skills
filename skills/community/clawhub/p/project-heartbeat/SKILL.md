---
name: project-heartbeat
description: Design controlled continuation loops for long-running projects. Use when a task is too large for one session, benefits from periodic wake-ups, and needs explicit continue conditions, stop boundaries, pending-decision handling, progress logging, and resume rules. Ideal for workspace refactors, long skill development, research tracks, and other cumulative engineering work.
metadata:
  openclaw:
    prePublishChecks:
      - clawhub-release-auditor
  homepage: https://clawhub.ai/daowuu/project-heartbeat
---

# Project Heartbeat

Project heartbeat is for **controlled continuation**, not endless automation.

## Use this skill when
- the project has a real home (for example `Projects/<name>/`)
- the work can continue in small, concrete steps
- progress should survive interruptions
- some blocked actions can be deferred without stopping the whole project
- you want wake-up cadence plus explicit stop conditions

## Do not use this skill when
- the work is small enough for one session
- there is no canonical project state
- the only remaining step is a human approval or external action
- the project has no clear next step

## v0 scope
This version focuses on what is practical now:
- fit check
- cadence recommendation
- continue conditions
- hard stop vs soft block boundary model
- pending decision backlog contract
- progress logging contract
- continuation integrity rules
- summary + handoff contract
- resume protocol

More advanced ideas such as model-routing and automatic blocked-path rerouting belong in the deferred backlog until the system has more real usage evidence.

A stronger strategic heartbeat mode is also valid when a project has many unfinished modules and should not fall into `waiting-human` merely because no fresh external input arrived. In that mode, each cycle should first re-evaluate the whole project against its original vision, then choose one smallest high-value move that most helps the system converge toward that vision.

## Workflow

1. **Fit check**
   - Confirm the project is large enough and structured enough for heartbeat.

2. **Choose cadence**
   - Pick a wake interval that matches the project intensity.
   - **30 seconds** is reasonable for active projects needing close monitoring.
   - **5–15 minutes** is better for normal ongoing work.
   - **30–60 minutes** is suitable for low-intensity sustained projects.
   - Prefer longer cadences for normal operation; reserve short intervals for debug/active-polish phases.

3. **Define continue conditions**
   - Only continue if there is a concrete next step already visible in project artifacts.

4. **Define boundaries**
   - Separate:
     - hard stop boundaries
     - soft block boundaries

5. **Define progress artifacts**
   - Every wake cycle should leave behind a durable trace.

6. **Check continuation integrity**
   - A cycle does not count as progress unless it produces at least one real artifact update.
   - No artifact, no progress.

7. **Define summary + handoff behavior**
   - Every cycle should leave a concise human-facing summary.
   - `waiting-human` and `closed` must hand work back explicitly rather than stopping silently.

8. **Define resume protocol**
   - Humans should be able to return and understand what moved, what blocked, and what still needs approval.

## Boundary model

### Hard stop boundaries
Must stop the loop:
- budget exhausted
- safety boundary reached
- explicit human-only action with no meaningful bypass path
- repeated no-progress cycles
- no clear next step for multiple wake cycles

### Soft block boundaries
Do not automatically stop the whole loop if other work remains:
- repository creation pending approval
- publish pending confirmation
- one branch of work blocked while other internal improvements remain

Soft blocks should be recorded in a pending-decision backlog so they can be surfaced later.

## Continuation integrity

A heartbeat loop should not be allowed to survive on continuation language alone.

### False continuation
False continuation happens when the agent says it continued, started, or progressed, but the project has no real new artifact to show for that cycle.

### Minimum artifact rule
A cycle should count as real progress only if it leaves at least one durable change such as:
- `STATE.md` updated
- task/backlog file updated
- `PENDING-DECISIONS.md` updated
- `HEARTBEAT-LOG.md` updated
- a new project/review/decision/doc artifact created
- a real tracked child task started

### No-op rule
If a cycle produced no durable artifact, treat it as a no-op. Repeated no-op cycles should escalate toward stop conditions rather than being narrated as progress.

## Scripts

### `scripts/fit_check.py`
Quick fit assessment for whether a project is ready for heartbeat-style continuation.

### `scripts/render_plan.py`
Renders a practical heartbeat plan: cadence, continue conditions, stop boundaries, backlog location, and resume guidance.

## References

- `references/boundaries.md`
- `references/examples.md`
- `references/pending-decisions-template.md`
- `references/heartbeat-log-template.md`
- `references/continuation-integrity.md`
- `references/summary-handoff.md`
- `references/deferred-backlog.md`
