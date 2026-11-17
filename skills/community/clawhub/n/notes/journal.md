# Daily Notes and Reviews

The daily note is a container, not a diary. Its job is to hold what happened until the review turns it into something the user can act on. This file covers the daily note, the weekly review, the monthly rollup, and how the cadence survives a missed week.

**Contents:** [Daily Note](#daily-note) · [Weekly Review](#weekly-review) · [Monthly Rollup](#monthly-rollup) · [Missed Days and Restart](#missed-days-and-restart) · [Journal Traps](#journal-traps)

**At the start of a session**, check the `## Due` table in `~/Clawic/data/notes/memory.md` against today's date and state any overdue review in one line — a statement, not a question. Cadence comes from `review_cadence` and `review_day`.

## Daily Note

One file per day, `journal/YYYY-MM-DD.md`, created on first write of the day and never in advance. An empty daily note pre-created for a week is scaffolding that trains the user to ignore the folder.

```markdown
---
date: 2026-07-26
type: journal
tags: [daily]
---

# 2026-07-26

## Happened
- Pricing decision landed → `decisions/2026-07-14_pricing-tiers.md`
- Vendor call moved to Tuesday

## Meant
- Three meetings this week produced no decision; the pattern is agenda-less standing calls

## Open
- SOC 2 confirmation still blocked on vendor, 8 days

## Tomorrow
1. Churn pull for Q2
2. Onboarding proposal review
```

- **Happened / Meant / Open / Tomorrow.** The `Meant` section is what separates a journal from a log — a day recorded with no interpretation is a day that will never be re-read.
- **The daily note links, it does not duplicate.** A meeting gets its own note; the daily note carries one line and the pointer. Copying the meeting into the journal creates two versions and the search returns both.
- **`Tomorrow` is capped at three.** A list of nine is a wish list, and its failure teaches the user to distrust the whole practice.
- If `review_cadence: none`, daily notes still work; only the review rows disappear from `## Due`.

## Weekly Review

Runs on `review_day` (default Friday). Twenty to thirty minutes, five passes, always the same order — the order is what makes it fast:

1. **Actions.** Open `actions.md`. Every overdue row gets one of four verdicts: done, new date, blocked-with-owner, or deleted. An item carried three weeks running with no verdict is deleted and said out loud — carrying it a fourth time is the practice lying to itself.
2. **Inbox.** Triage `quick/` to zero (`capture.md`).
3. **Threads.** `## Open Threads`: anything waiting more than 14 days gets escalated to a person with a date or dropped.
4. **Notes.** Skim the week's notes for a claim that deserves its own note (a decision that was never recorded, a pattern across three meetings).
5. **Next week.** Three commitments, each already a row in `actions.md` with a date.

Output, appended to `reviews/<year>.md`:

```markdown
## Week of 2026-07-20
Completed: 6 · Carried over: 2 · Created: 9 · Inbox at zero: yes
- Shipped: pricing decision, vendor shortlist
- Carried: SOC 2 confirmation (blocked on vendor since 2026-07-18)
- Pattern: three meetings produced no decision and no action
- Next week: churn pull (2026-07-30), onboarding proposal (2026-08-02), SOC 2 chase (2026-07-29)
```

The **pattern line is the deliverable**. Counts tell the user the review ran; the pattern is what changes anything. If two consecutive reviews produce no pattern line, the review has become bookkeeping and should be shortened, not abandoned.

## Monthly Rollup

Cheap, because the weekly reviews already did the work: read the four week blocks, write one entry.

```markdown
## July 2026
Notes: 21 (14 meeting, 3 decision, 4 quick) · Untriaged at month end: 0 · Tags merged: 2
- Decisions: pricing tiers, vendor shortlist
- Recurring blocker: vendor responsiveness, 3 weeks
- Corpus: 64 notes; index in use since 2026-06
```

The monthly is also the maintenance slot — its `## Due` row is `Tag + orphan-link sweep`, and it runs the tag audit and dead-link check from `retrieval.md`.

## Missed Days and Restart

The failure mode of every journaling practice is the guilt gap: three days missed, then abandonment.

- **Never backfill.** A daily note written four days late is fiction with a date on it. Write today's, and put anything worth keeping from the gap in a single `Happened` line: "Mon-Wed: vendor negotiation, notes in `meetings/`."
- **A skipped weekly review is not skipped, it is late.** Run it against the actual period covered and label it — "Weeks of 07-13 and 07-20 (combined)". Two weeks in one pass is fine; pretending the first week did not exist loses its carried actions.
- **Streaks are not the metric.** The metric is whether `actions.md` is trusted. A practice with 40% attendance and a trusted tracker beats a perfect streak of empty notes.
- **Shrink before quitting.** When the cadence is failing, cut the daily note to `Happened` and `Tomorrow` and keep the weekly review intact. The review is the part that produces value; the daily note is the part that feeds it.

## Journal Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Pre-creating a week of empty daily notes | Trains the user to skip the folder, and inflates the corpus count | Create on first write |
| Journal as the only place notes live | A date is the one thing nobody remembers six months later | Typed notes by subject; journal links to them |
| Copying meeting content into the daily note | Two versions of the same thing, both returned by search | One line and a pointer |
| Nine priorities for tomorrow | Guarantees failure and discredits the practice | Three, each with a date in `actions.md` |
| Backfilling missed days | Invents detail and dates it | One `Happened` line for the gap |
| Reviewing by reading everything | Takes two hours, gets abandoned after three weeks | Five fixed passes, 20-30 minutes |
| Counting instead of concluding | The review runs and nothing changes | The pattern line is the deliverable |
| Carrying an action indefinitely | The tracker stops being believed, and then so does the whole system | Third carry-over is a delete |

**Write triggers for this file** — in the same turn: the daily note to `~/Clawic/data/notes/journal/<date>.md`; the review block to `reviews/<year>.md` (append, cut by year); the `Weekly review`, `Inbox triage` and `Tag + orphan-link sweep` rows in `## Due` with today's date; every verdict from pass 1 back into `actions.md`; any pattern that becomes a standing rule into `## Conventions` or `artifacts/<kebab-name>.md`. Formats and thresholds: `memory-template.md`.
