# Recurring Meetings — Charters, Expiry Dates And Kill Reviews

**Before creating, changing or killing a series**, read `## Series` in `~/Clawic/data/meetings/memory.md` (or `~/Clawic/data/meetings/series.md` if `## Boxes` points there), `series_review_days` and `cost_per_attendee_hour` in `config.yaml`, and the series charter in `artifacts/` if `## Boxes` names one — the charter is the design, and changing the invite without changing the charter loses the change. **Check `## Due`** and state an overdue kill review in one line.

**Contents:** [Creating A Series](#creating-a-series) · [The Charter](#the-charter) · [The Kill Review](#the-kill-review) · [Shrink, Merge, Async, Kill](#shrink-merge-async-kill) · [The Zombie Catalog](#the-zombie-catalog) · [Handing A Series Over](#handing-a-series-over) · [Killing It Well](#killing-it-well)

## Creating A Series

A recurring meeting is a standing withdrawal from everyone's week; it earns that only if the work recurs at the same rhythm. Five things at creation, or it becomes a zombie by quarter two:

1. **A purpose type that genuinely repeats.** `decide` and `align` recur; a `generate` session almost never does, and an `inform` series is a newsletter with worse attendance.
2. **An expiry date, always** — default `series_review_days` (90), or ~13 occurrences for a weekly. Set it in the calendar invite's recurrence end, not only in your head: the calendar is where zombie meetings are born.
3. **A cadence matched to the decision rate, not to the calendar's convenience.** If two of the last four occurrences had nothing to decide, the cadence is one step too fast. Weekly → biweekly → monthly, and back up only on evidence.
4. **A named owner who is a person.** A series owned by a team is a series nobody can cancel.
5. **A kill test written at creation**, while it is still cheap to be honest: "if fewer than two blockers arrive in three consecutive weeks, it becomes async". Writing the kill test later means writing it while defending the meeting.

**Cadence starting points**, adjusted by evidence: team sync weekly · 1-on-1 weekly or biweekly · leadership sync weekly · cross-team coordination biweekly · steering or governance monthly · board or QBR quarterly · strategy or planning offsite half-yearly. Anything more frequent than daily is not a meeting, it is a workflow problem.

## The Charter

One page per series, at `~/Clawic/data/meetings/artifacts/charter-<series>.md`, read at every kill review and whenever someone proposes changing the meeting. It exists because the fifth person to inherit a series has no idea why it started.

```markdown
# Charter — Weekly Leads
*Read before changing this meeting's shape, and at every kill review. Written 2026-07-26.*

Purpose type: align. Output: one prioritized list of cross-team blockers with owners.
Owner: me. Attendees: 6 leads (decision ceiling 8). Cadence: weekly, 25 min, Tue 10:00 CET.
Timeboxes: blockers 12 · decisions 6 · close 5 (80% of 25 min = 20).
Not this meeting: status (async thread Monday), design debate (own session), 1-on-1 topics.
Expires 2026-10-01. Kill test: fewer than two blockers in three consecutive weeks → async.
```

- **The "not this meeting" line does most of the work.** Series rot by accretion: every topic with no home lands in the standing meeting until the original purpose has 8 minutes.
- **Attendance is a list of roles, not of names**, so a departure does not silently re-scope the room.
- **Any change to cadence, length or attendees is a charter edit**, made in the same turn as the invite change.

## The Kill Review

Run at the expiry date, or quarterly for anything without one (`## Due`). It is a real review with a real possible outcome, not a ritual re-approval.

**Step 1 — Price it.** `attendees × hours × occurrences_per_quarter` = person-hours per quarter. A weekly 1h with 8 attendees is `8 × 1 × 13` = 104 person-hours a quarter; at 80/h that is ~8,300. Quote person-hours when `cost_per_attendee_hour` is unset — an undisputable number beats an estimated one.

**Step 2 — Ask the four questions**, in this order:

| Question | A failing answer |
|---|---|
| What did this meeting decide in the last quarter? | "Nothing, but it keeps us aligned" |
| What would break if it stopped for six weeks? | Nobody can name a concrete consequence |
| Could the output be produced by one person plus a document? | Yes, and the attendees would rather read it |
| Would you create this meeting today at that price? | Silence, or "not at that size" |

**Step 3 — Decide one of five**: keep as is · shrink · merge · convert to async · kill. "Keep and monitor" is not an outcome; it is a kill review that failed to happen.

- **Ask the attendees anonymously first** when the owner is the chair. Nobody tells the person who runs a meeting that it is a waste, so the honest data only arrives in writing and unattributed.
- **Attendance decay is the leading indicator.** When people start sending delegates or skipping, the review is already overdue.
- **A meeting nobody prepares for has already been killed** by everyone except the calendar.

## Shrink, Merge, Async, Kill

Cheapest intervention first; killing is not the default answer, it is the last one.

- **Shrink the room before the slot.** Cost is linear in attendees and the decision ceiling is 8; dropping four "for visibility" attendees to the recap distribution halves the price and speeds up the room.
- **Shrink the slot.** 60 → 25 forces the agenda to name its output. If the work genuinely does not fit, it is two meetings with two purposes, not one long one.
- **Halve the cadence with a written escape.** Weekly → biweekly plus a thread for the off week; if the thread is silent for a month, the answer was monthly all along.
- **Merge only when the attendee lists overlap by most of the room and the purpose type matches.** Merging a `decide` and an `inform` meeting produces a long meeting that does neither.
- **Convert to async** when the purpose is `inform`, `status` or `review`: a written update with a named comment deadline and a default, plus one live escape hatch for deadlock (`meeting-load.md`).
- **Kill** when nobody can name what breaks. Trial-kill for six weeks first if the room is nervous — a suspension nobody notices is the cheapest possible proof.

## The Zombie Catalog

Recognizable species; each has a specific cause and a specific fix.

| Zombie | How it got there | Fix |
|---|---|---|
| The status round-robin | Started as a decision meeting; the decisions moved elsewhere and the updates stayed | Async thread; keep only what the writing exposes |
| The meeting whose owner left | Recurrence has no end date, nobody feels entitled to cancel | Reassign or kill — an unowned series is always killed |
| The meeting held so nobody feels excluded | Politics, not work | Recap distribution solves inclusion; the meeting does not |
| The habit meeting | It has always been on Tuesdays | Kill test against the four questions |
| The meeting that is really a 1-on-1 with an audience | Two people talk, six listen | Two-person slot; the six get the recap |
| The prep meeting for another meeting | The real meeting has no agenda | Fix the agenda of the real meeting instead |
| The one that only exists to chase action items | No ledger, so the chase needs a room | One ledger, one weekly sweep (`follow-through.md`) |
| The recurring meeting cancelled three times in a row | It is already dead; the calendar has not been told | Kill it, and say what replaces it |

## Handing A Series Over

- **Hand over the charter, not the invite.** A new owner without the charter re-derives the purpose from the attendee list, which is how a decision meeting becomes a status meeting.
- **Transfer the recurrence ownership in the calendar too**, or the meeting dies when the old owner's account is deactivated.
- **The new owner runs a kill review within their first three occurrences.** Inheriting a meeting is the best moment to cancel it, and the only moment where cancelling costs nothing politically.

## Killing It Well

- **Announce it with what replaces it.** "The Thursday sync stops; blockers go in the channel and I'll answer by end of day" — a kill with no replacement teaches people the meeting was load-bearing after all, and it reappears under a new name.
- **Delete the recurrence, do not just stop attending.** A meeting nobody attends stays on twelve calendars for years.
- **Record what replaced it.** The killed list is what stops a cancelled meeting from being reinvented two quarters later by someone who was not there.
- **Set a check-in date, once.** Six weeks after the kill, ask whether anything actually broke; then close the question permanently.

**Write in the same turn as any series change**: the row in `## Series` of `~/Clawic/data/meetings/memory.md` with its cadence, owner, purpose type, attendee count and expiry date, the charter at `~/Clawic/data/meetings/artifacts/charter-<series>.md` with its `## Boxes` line, the next kill review as a row in `## Due`, a killed series in the `## Killed` table (series, date killed, what replaced it) of `~/Clawic/data/meetings/series.md`, and any norm the review exposed in `## Meeting Norms` (`memory-template.md`). A kill review whose conclusion lives only in the chat gets rerun from zero next quarter, and the meeting survives it.
