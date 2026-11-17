# Action Items — Extraction, Tracking, Chasing

One tracker, absolute dates, and a deletion rule. A commitment list is worth nothing the moment the user stops believing it is complete, and every rule here protects that belief.

**Contents:** [Extraction](#extraction) · [The Tracker](#the-tracker) · [Status and Escalation](#status-and-escalation) · [Chasing Other People](#chasing-other-people) · [The Weekly Sweep](#the-weekly-sweep) · [External Task Apps](#external-task-apps) · [Action Traps](#action-traps)

**Before answering any question about commitments, deadlines, or what someone owes**, read `~/Clawic/data/notes/actions.md` — or the per-owner files if `## Boxes` points there. An answer assembled from the current conversation is wrong by definition: the commitments are in the tracker, not in this session.

## Extraction

An action item is a **commitment**: someone specific, doing something specific, by a specific date. Three tests, all required.

| Heard | Is it an action? | Why |
|---|---|---|
| "I'll send the deck tomorrow" | Yes | Owner, verb, date |
| "We should redesign onboarding" | No | No owner, no date — this is an Open Thread or a project idea |
| "Can you look at this?" / "Sure" | Yes | Acceptance makes it a commitment; the date must be asked for now, not later |
| "Someone needs to call the vendor" | No, until assigned | Record in `## Open Threads` with the question "who calls the vendor?" |
| "Let's revisit in Q3" | No | A reversal trigger on a decision (`decisions.md`), not an action |
| "I'll try to get to it" | No | Not a commitment; goes to `## Open Threads` in `memory.md` |

Extract aggressively but classify honestly. A tracker padded with wishes fails the same way a tracker with gaps does — the user stops using it.

**Resolve dates at extraction time.** "Next week" becomes the date it means, on the day it was said. "End of month" becomes the last working day. The note is read in November and "next week" is then meaningless.

**No date offered?** Ask once, in the moment — this is the one place a question is cheaper than a default, because a guessed date is a commitment the owner never made. If nothing comes back, record it in `## Open Threads` in `memory.md` rather than inventing a deadline.

## The Tracker

`~/Clawic/data/notes/actions.md`, one table, sorted by due date ascending. Full format, keys and scale cut: `memory-template.md`.

```markdown
| Task | Owner | Due | Status | Source |
|---|---|---|---|---|
| Send the pricing deck | @alice | 2026-08-04 | open | `meetings/2026-07-26_product-sync.md` |
```

- **Sorted by date, not grouped by status.** Status sections (`Overdue`, `This week`, `Upcoming`) are wrong the day after they are written and require rewriting the file to stay true; a sort is always correct and overdue is computed against today.
- **Identity is `Task` + `Owner`.** The same commitment restated in a later meeting updates the existing row — new date, source appended — and never becomes a second row. Duplicate rows are the fastest way to lose trust in the count.
- **`Source` is the pointer back to the context**, in the platform's own form: a path, `notion:Page`, `bear:#tag/Title`, `obsidian:[[Note]]`. Without it, a stale item cannot be judged.
- **Owners are `@key` pointers** into the shared `~/Clawic/data/contacts/contacts.md`. The person's details never live in the tracker.
- **One tracker, whatever platform holds the note.** An item captured from a Notion meeting note still lands here. Three apps each holding a third of the commitments is the same as having none.

## Status and Escalation

Computed against today's date, never stored as a section:

| Age | State | What happens |
|---|---|---|
| Due in future | open | Nothing |
| Due today or overdue 1-2 days | overdue | Named in the next session's opening line, once |
| Overdue 3-6 days | overdue, flagged | Offer the four verdicts: done, new date, blocked-with-owner, delete |
| Overdue 7-13 days | stale | The date was wrong. A new date is required; keeping the old one is a lie the tracker tells daily |
| Overdue 14+ days | dead | Delete it, or convert it to a project (`projects.md`). Nothing survives two weeks overdue by accident |

Blocked items are exempt from the ladder only while the blocker has a person and a date: `blocked: waiting on @bob since 2026-07-18`. A blocker with no owner is not a blocker, it is an excuse the tracker is storing.

**State overdue items as a statement, once per session, in one line.** Repeating them every turn is nagging and gets the whole system muted.

## Chasing Other People

- **The chase is an action of yours.** "Alice owes me the deck by 2026-08-04" implies a row owned by `@me`: "follow up on the pricing deck — 2026-08-05".
- **Chase from the source note, not from memory.** Reopening the meeting note gives the exact words and the date they were said, which turns a nag into a reference.
- **Two chases and then escalate or drop.** A third reminder with no new information changes nothing except the relationship.
- Update `Last contact` in the shared `contacts.md` when a chase goes out, so the next skill that talks to that person knows.

## The Weekly Sweep

Runs inside the weekly review (`journal.md`), as its first pass:

1. Every row past due gets one of four verdicts: done, new date, blocked-with-owner, deleted.
2. Completed rows are moved into the week block in `reviews/<year>.md` and deleted from the tracker. A tracker that keeps every completed item stops being readable at about 80 rows.
3. Count what was deleted and say it. "Four items deleted, all 14+ days overdue" is the honest signal that the intake is too loose.
4. Anything carried three weeks running is deleted regardless of protest — the fourth carry is the practice lying to itself.

## External Task Apps

With `action_target: external`, the user's own task system is the source of truth for their tasks. `actions.md` then holds only what the app cannot:

- **Commitments other people made to the user** — most task apps model only your own tasks, so these are the ones that silently disappear.
- **A pointer to where the user's tasks live**, one line, so the tracker is never mistaken for empty.
- The extraction rules, dates and owners are unchanged; only the destination moves. Never write into the external app's storage directly — hand the item to the user in the app's own shape and record the handover as the row's `Status` in `actions.md`.

Never run both as sources of truth. Two lists diverge within one week, and the reconciliation cost exceeds whatever either list was worth.

## Action Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| "ASAP", "soon", "next sprint" | Never becomes overdue, so it is never chased | Absolute date at extraction |
| Extracting wishes as actions | The list inflates and the user stops trusting the count | Three tests: owner, verb, date |
| Status sections in the file | Wrong the next day, and fixing them means rewriting the file | Sort by date, compute status |
| A second row for a restated item | The count is wrong, and both rows go stale | Update in place on `Task` + `Owner` |
| Tracking in whichever app holds the note | Commitments split across three apps | One tracker |
| Keeping everything completed | Unreadable past ~80 rows | Move to `reviews/<year>.md` at the weekly sweep |
| Rolling an overdue date silently | The estimate was wrong and nobody learns why | New date with a cause, or delete |
| Repeating overdue items every turn | Gets the whole system muted | One statement per session |
| Blocked with no owner | Sits forever, immune to the ladder | Blocker needs a person and a date |
| Two sources of truth | They diverge in a week | One, chosen by `action_target` |

**Write triggers for this file** — in the same turn: every extracted commitment as a row in `~/Clawic/data/notes/actions.md`; completions and new dates in place on the same row; completed rows moved to `reviews/<year>.md` at the weekly sweep; owners to the shared `~/Clawic/data/contacts/contacts.md` with `Last contact` updated on every chase; unassigned requests to `## Open Threads` in `memory.md`; the sweep date to the `Weekly review` row in `## Due`. Formats, identity keys and the 60-item scale cut: `memory-template.md`.
