# Project Notes, Status Updates, and Handovers

Project notes fail in one specific way: they become a single file appended to forever, where the current status is buried on line 340 and the last four updates contradict each other. Everything here exists to prevent that.

**Contents:** [One File per Update](#one-file-per-update) · [The Status Note](#the-status-note) · [Status Vocabulary](#status-vocabulary) · [Blockers](#blockers) · [The Shared Project Box](#the-shared-project-box) · [Handover and Closeout](#handover-and-closeout) · [Project Traps](#project-traps)

**Before writing an update**, read `~/Clawic/data/projects/<project>.md` (the shared box: objective, status, decisions, milestones) and the open rows for this project in `actions.md`. A status update written without last period's blockers repeats them as if they were new.

## One File per Update

`projects/YYYY-MM-DD_<project>-status.md`, one per reporting period. Never one growing file.

The reason is retrieval, not tidiness: "what did we say in June" is a question people actually ask, usually because the answer differs from what happened. A per-update file answers it by filename; an append-only document requires reading the whole thing.

What *is* cumulative — objective, current status, decisions, milestones — lives in the shared project file (`~/Clawic/data/projects/<project>.md`), which is rewritten in place. Two homes, two growth patterns, no contradiction.

## The Status Note

```markdown
---
date: 2026-07-20
type: project-update
title: "Atlas: beta slips two weeks, seeding is the blocker"
tags: [atlas]
project: atlas
status: at-risk
---

# Atlas — 2026-07-20

**Status:** at-risk (was on-track 2026-07-13) · **Next milestone:** beta, 2026-08-29 (was 08-15)

## Since last update
- Onboarding flow merged
- Two of five beta customers confirmed

## Blockers
| Blocker | Waiting on | Since | Impact |
|---|---|---|---|
| Staging data seeding | @bob | 2026-07-08 | beta date, +2 weeks |

## Changed since last update
- Beta 2026-08-15 → 2026-08-29, cause: seeding blocker

## Next
| Task | Owner | Due |
|---|---|---|
| Seed staging from a prod snapshot | @bob | 2026-07-30 |
| Confirm remaining 3 beta customers | @me | 2026-08-04 |
```

- **The title states the status change**, not the project name. "Atlas update" is unfindable among twelve of them; "Atlas: beta slips two weeks" answers the search.
- **`Changed since last update` is the section executives read.** Every date change names its cause. A slipped date with no cause reads as an estimate that was never real.
- **`status` in frontmatter, with the previous value inline.** The transition is the information; the current value alone hides that it changed three times.
- Percent-complete is only worth writing when it derives from something countable (12 of 18 endpoints). An invented percentage is a fabricated number and it always drifts to 90%.

## Status Vocabulary

Three values, with thresholds so the label is not a mood:

| Status | Threshold | Obligation |
|---|---|---|
| `on-track` | Next milestone date unchanged and no blocker older than 7 days | Nothing beyond the update |
| `at-risk` | Milestone date is achievable only if a named blocker clears, or any blocker is 7+ days old | Name the blocker, the owner, and what unblocks it |
| `blocked` | Milestone date cannot be met with current information | New date in the same update, or an explicit "date unknown until X" |

A project that reports `on-track` and then slips has skipped `at-risk`. The rule that prevents it: a blocker older than 7 days forces `at-risk` regardless of confidence.

## Blockers

- **Every blocker has a person, not a team.** "Waiting on infra" never resolves; "waiting on @bob" does.
- **`Since` is a date, and age is the escalation trigger.** 7 days → `at-risk`. 14 days → raised outside the project, with the cost named. 21 days → the plan changes, because the blocker has proven it is not clearing.
- **A blocker on yourself is a priority problem, not a blocker.** Record it as an action with a date; calling it a blocker outsources the responsibility.
- Blockers older than 14 days also get a row in `## Open Threads` in `memory.md`, so the weekly review sees them even when the project is not discussed (`journal.md`).

## The Shared Project Box

`~/Clawic/data/projects/<project>.md` is shared with every other skill that touches work. The notes stay in `notes/`; the box holds the durable spine.

```markdown
# Atlas

status: active
owner: @me
started: 2026-05-02
objective: five paying beta customers by Q3

## Decisions
- 2026-07-14 Pricing stays at three tiers — `notes/decisions/2026-07-14_pricing-tiers.md`

## Milestones
- 2026-08-29 Beta with five customers (was 08-15)

## Updates
- 2026-07-20 at-risk, seeding blocker — `notes/projects/2026-07-20_atlas-status.md`
```

- **Identity is the project name**, which is the filename slug. Read the folder before creating: a project that exists under another spelling gets updated, never duplicated.
- **One line per update, with the pointer.** The content stays in the note. Copying the update into the box is how the two start disagreeing.
- **Closing is a status line, never a deletion**: `status: done — 2026-09-01` or `status: cancelled — 2026-09-01`. The file is the record of what was delivered. Past ~20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- **Amounts carry their currency in the value** (`4200 EUR`, not `€4200`); dates are ISO. Other skills read and total these.
- **Foreign structure wins.** If the file already exists with different headings, add under the closest one rather than restructuring it.
- Clients and stakeholders are pointers to `~/Clawic/data/contacts/contacts.md`, never copied in.

## Handover and Closeout

A handover is the one project artifact that is read cold by someone with no context, so it is written for a stranger and it goes to `artifacts/`, not to a status note.

```markdown
# Handover — Atlas
*Read when taking over Atlas, or returning to it after a break. Written 2026-08-30.*

State: beta live with 4 of 5 customers.
Where things are: repo, staging, and the beta tracker (links).
Decisions that constrain you: three tiers (`notes/decisions/2026-07-14_pricing-tiers.md`).
Landmines: staging seeding is manual; the vendor SOC 2 is unresolved.
People: @alice owns pricing, @bob owns infra.
First thing to do: confirm the fifth beta customer (open in `actions.md`).
```

Closeout, at the end of a project, is four lines in the shared box and nothing more: what was delivered, what was cut, what it cost against the estimate, and the one thing to do differently. A closeout longer than a page is written for nobody.

## Project Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| One growing project file | Current status buried mid-file; June's version unrecoverable | One note per update, cumulative spine in the shared box |
| "Atlas update" as a title | Twelve identical titles, none findable | Title states the status change |
| Invented percent-complete | Drifts to 90% and stays there | Countable denominator or nothing |
| Slipping a date with no cause | The next estimate is believed less, correctly | Every date change names its cause |
| `on-track` with a 10-day blocker | The slip arrives as a surprise it never was | 7-day rule forces `at-risk` |
| "Waiting on the platform team" | No person, so no resolution | Name the person |
| Duplicating the project into the notes folder | The shared box and the note disagree within a month | Box holds the spine, note holds the content |
| Handover written as a status update | The reader has no context and the update assumes all of it | Handover template above, in `artifacts/` |
| Deleting the project file at closeout | The record of what was delivered disappears with it | `status: done — <date>` |

**Write triggers for this file** — in the same turn: the update to `~/Clawic/data/notes/projects/<date>_<project>-status.md`; the status, milestone change, decision line and update pointer to `~/Clawic/data/projects/<project>.md`; every next-step row to `actions.md`; blockers older than 14 days to `## Open Threads` in `memory.md`; stakeholders to the shared `~/Clawic/data/contacts/contacts.md`; a handover or closeout to `artifacts/<kebab-name>.md` with its `## Boxes` line. Formats, keys and thresholds: `memory-template.md`.
