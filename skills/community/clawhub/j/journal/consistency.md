# Consistency — Lapses, Restarts, And Making It Stick

Scope: the practice that stopped, or never started. Most journaling failures are logistics, not motivation.

**Contents:** [The Restart Protocol](#the-restart-protocol) · [Friction Inventory](#friction-inventory) · [Where To Put The Slot](#where-to-put-the-slot) · [The Two-Day Rule](#the-two-day-rule) · [Streaks, Honestly](#streaks-honestly) · [Nudging](#nudging) · [Diagnosing A Lapse](#diagnosing-a-lapse) · [Scaling The Floor](#scaling-the-floor)

**Before diagnosing anything**, read `## Practice` in `~/Clawic/data/journal/memory.md`: last entry date, current and longest run, usual slot, median length, and every practice already abandoned. A lapse diagnosis without the previous lapse in hand repeats the advice that already failed.

## The Restart Protocol

Four steps, in this order, no substitutions:

1. **Write today's entry now.** One sentence is a complete entry. Do it inside this session, not tonight.
2. **Do not backfill.** No catch-up entry, no summary of the missed weeks, no apology paragraph (Rule 6). Reconstructing a gap converts resuming into a project with a backlog, and the backlog always wins.
3. **Say nothing about the gap** unless the user raises it. If they do, it is worth exactly one line inside today's entry, and it is usually the most useful line in it: what was happening when the writing stopped.
4. **Halve the commitment.** Whatever cadence they had, restart at half. Someone who was writing daily restarts at three days a week. Restarting at the old level is what produces the second lapse two weeks later.

Restarting is not a failure state to be fixed. A practice with four restarts in a year and 180 entries beats an unbroken 40-day streak that ended in March.

## Friction Inventory

The practice dies at whichever step costs the most. Walk them in order and fix the first one that is not near-zero:

| Step | Common cost | Fix |
|---|---|---|
| Remembering | No cue at all; relying on intention | Attach it to an existing anchor: after the first coffee, after closing the laptop, after brushing teeth |
| Getting to the file | Opening an app, navigating folders, choosing where | One command or one shortcut, straight into today's file, pre-named (`storage.md`) |
| Deciding what to write | The blank page | A single standing opener, the same one every day, so there is nothing to choose (`prompts.md`) |
| Deciding how much | An implied standard of a "proper entry" | Explicit floor of one sentence, stated out loud |
| Deciding whether it is good | Editing while writing | Freewriting mechanics: no going back (`capture.md`) |
| Finishing | Not knowing when to stop | Fixed timer or fixed length, never a quality bar |
| Anything else | Unknown | Ask them where it stopped last time; they usually know the exact step |

Fix one step at a time. A redesign that fixes all six is a new practice, and new practices have the same failure rate as the last one.

## Where To Put The Slot

| Slot | What it produces | Fails when |
|---|---|---|
| First thing, before input | Generative, unguarded, planning-heavy — the only slot morning pages work in | The user checks a phone first; the day's agenda has already arrived |
| Commute or transit | High completion, dictated (`capture.md`) | The material is private and the space is not |
| Between tasks | Interstitial, highest resolution for work review | Requires a workday with visible transitions |
| End of workday | Closes the work loop, protects the evening | Gets skipped whenever the day overran, which is the day worth writing |
| Before sleep | Processing, emotional, best recall of the day | Tiredness shortens entries to nothing; anxious material at bedtime keeps some people awake |
| Weekend only | Sustainable for review-oriented practice | Loses the daily series any analysis needs (Rule 8) |

Pick one slot, not two. Two slots means neither is the cue.

## The Two-Day Rule

**Never miss twice.** One missed day is noise; two consecutive is the start of the run that ends the practice — the second miss is where the identity flips from "someone who journals" to "someone who used to".

- The rule is a floor, not a streak: after one miss, the next day's entry is mandatory and may be one sentence.
- After two misses, the restart protocol runs and the cadence halves. Do not attempt to resume at the old level.
- Applied to weekly practices, the same rule reads: never skip two consecutive weeks.

## Streaks, Honestly

- Streaks work until the first break, then they invert: the counter that motivated on day 20 is the reason someone does not come back on day 21. This is the mechanism behind most abandoned journals, and it is why `nudge` defaults to false.
- If the user wants a streak, use two counters, not one: **current run** and **entries in the last 30 days**. The second one survives a break, which is exactly what the first one cannot do.
- Never display a broken streak unprompted. The number is stored in `## Practice`; showing it after a lapse is a punishment with no upside.
- A "streak" that is being maintained with one-word entries is worth naming once, without judgment: the floor is doing its job, and it is also hiding that the practice has become a checkbox.

## Nudging

`nudge` is false by default. When the user turns it on:

- **Nudge with an opening, not a reminder.** "You mentioned the interview was Thursday — want to write about it?" works; "you haven't journaled in 5 days" is a guilt notification and produces avoidance.
- One nudge per lapse, ever. A second one for the same gap converts the tool into a nag and the practice into an obligation.
- Never nudge during a period the user has described as hard, and never nudge from a Red Flags context — that is a check-in, not a streak reminder (SKILL.md Red Flags).
- On-this-day resurfacing ("a year ago you wrote about the move") is a separate opt-in from streak nudges, because it can surface grief material without warning. Off unless asked, and never for entries in `## Read Scope`.

## Diagnosing A Lapse

| What they say | Actual cause | Move |
|---|---|---|
| "I got too busy" | The slot was in the part of the day that gets eaten first | Move the slot earlier, or to a transition that survives a bad day |
| "I had nothing to write" | The bar is a "proper entry" | Restate the floor: one sentence, and mean it |
| "It felt pointless" | Nothing was ever read back | Run one weekly review over what exists (`review.md`); the practice earns its keep on the reread, not the write |
| "It started feeling like homework" | Template, streak, or cadence obligation | Drop the template, halve the cadence, turn off the counter |
| "It was making me feel worse" | Rumination, not processing — a real risk, not a motivation problem | Go to `difficult-entries.md` before doing anything else about consistency |
| "Someone might read it" | A real privacy problem, not a habit problem | `privacy.md`: encryption, location, read scope, and what leaves the folder |
| "I stopped when the notebook filled" | The container ended and nothing replaced it | Pre-create the next container; in files, this failure mode disappears |
| Anything else | Unknown | Ask what was happening the week it stopped; the answer is usually a life event, and the fix is halving the cadence, not motivation |

## Scaling The Floor

Raise the commitment only after four consecutive weeks at the current level:

1. One sentence, three days a week.
2. One sentence, daily.
3. Five minutes, daily.
4. Ten minutes or three pages, daily.
5. Add a second practice (`practices.md`), never before this point.

Drop a level on the first lapse rather than the second. Dropping a level is a maintenance action, not a defeat, and it is the thing that keeps the entry count going up over a year.

**Write in the same turn:** last entry date, current run, longest run, entries in the last 30 days, usual slot, and the floor currently in force, to `## Practice` in `memory.md`; a lapse with its diagnosed cause and the adjustment made, to the same section (this is the record that stops the next lapse getting the same failed advice); any accepted cadence, nudge time, or resurfacing schedule, to `## Due`; `nudge` and `review_cadence` changes to `config.yaml`. Formats: `memory-template.md`.
