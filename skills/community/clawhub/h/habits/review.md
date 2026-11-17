# Check-ins, Reviews, and Graduation

Four cadences with four different agendas. Each writes its result; a review that produces no written change was a conversation.

**At the start of every session**, check `## Due` in `~/Clawic/data/habits/memory.md` against today's date and state any overdue item in one line — a statement, not a question. Before running any review, read the relevant month's logs and `## Patterns`.

**Contents:** [The Four Cadences](#the-four-cadences) · [Daily Check-in](#daily-check-in) · [Weekly Review](#weekly-review) · [Monthly Rollup](#monthly-rollup) · [Quarterly Audit](#quarterly-audit) · [Graduation](#graduation) · [Retirement](#retirement) · [Pausing](#pausing) · [Keeping the Due Table Honest](#keeping-the-due-table-honest)

## The Four Cadences

| Cadence | Default | Job | Writes |
|---|---|---|---|
| Daily check-in | Every day, `checkin_style: batch` | Fill today's cells. Nothing else | `logs/<year>-<month>.md` |
| Weekly review | `review_day` (default Sunday) | Rates, the shape of the misses, one change | Log, roster notes, `reviews/<year>.md`, `## Due` |
| Monthly rollup | First session of a new month | Month figures, best-streak updates, log rollover | `reviews/<year>.md`, roster, new log file |
| Quarterly audit | Every 3 months | What stays, what graduates, what is retired | Roster, `## Retired`, `## Patterns`, `## Due` |

Each accepted cadence is a row in `## Due` with its last-run date. A cadence that is not in the table gets skipped for a quarter and nobody notices.

## Daily Check-in

One interruption, one line, no analysis.

- **Batch by default**: a single question covering every habit scheduled today. Per-habit prompting costs one interruption per habit and is ignored by week two (`checkin_style`).
- **Skip habits whose cell is already filled.** Asking twice teaches the user to stop answering.
- **Skip the prompt entirely if the user is mid-task on something else.** A check-in that interrupts work is a check-in that gets turned off.
- **No coaching in a check-in.** A pattern noticed today waits for the weekly review, unless it is a second consecutive miss (Rule 6) or a Red Flag.
- Response format: acknowledge in one line, name the streak or rate only if the user asked or a threshold was crossed (best streak beaten, a band change).

## Weekly Review

Fixed agenda, five to eight lines of output, exactly one change.

1. **Rates.** Each habit's 28-day rate with its denominator, and its band (Rule 5). Say "no change" explicitly where that is the answer.
2. **Shape of the misses.** Scattered, clustered on a weekday, or a cliff — the shape, not the count (`troubleshooting.md`).
3. **Streaks.** Current and best, second in the sentence unless `primary_metric: streak`.
4. **The one change**, or none. If none, say so as a decision.
5. **Slot check.** Is a slot free, and has it been ≥14 days since the last addition (Rule 7)? If not, the answer to "can I add one" is no, with the date it becomes yes.
6. **Anything the user wants to raise.** One question, at the end, not the beginning.

Never turn the weekly review into a redesign session. A weekly review that changes three habits produces a month of unattributable data.

Write the review as a short entry in `reviews/<year>.md` — date, each habit's rate, the change made — and update the `Last run` cell in `## Due`. Three months of these entries is what makes the quarterly audit possible without recomputing anything.

## Monthly Rollup

Runs on the first session of a new month, before any logging.

- **Create the new log file** with a column per active habit and add its `## Boxes` line (`tracking.md`).
- **Compute the closed month's figures**: completions of scheduled days per habit, over the calendar month. Label them as month figures — they are not comparable with the rolling 28-day rate, and a closed month is not comparable with a month-to-date.
- **Update any best streak** in the roster row, with the date it ended.
- **Reset the freeze budget.**
- **Compare with the previous month** only on the same measure. One line per habit: better, same, worse, with the two numbers.
- **Check the roster against reality**: any habit with no entries at all last month is either paused or dead — say which (`relapse.md`).

## Quarterly Audit

The clear-out. It is the only cadence allowed to change several habits at once, because its purpose is composition rather than tuning.

Run each active habit through four questions, in order:

| Question | If no |
|---|---|
| Does the Why still hold? | Retire it |
| Has it been ≥95% for 8 weeks? | It stays active; go to the next habit |
| Is it now automatic — done without deciding? | It stays active |
| Would the slot serve a habit the user wants more? | Graduate it (below) |

Then, on the roster as a whole:

- Count active habits against `max_active_habits`. Over the ceiling is the finding, and something is retired or graduated to fix it.
- Read `## Retired` before proposing anything new: a habit dropped twice is not proposed a third time in the same form.
- Read `## Patterns` and state the two or three that are now supported by enough data to act on (Rule 8).
- Confirm the cadences in `## Due` are still wanted. An unwanted review is the reason reviews stop.

Write the audit as an entry in `reviews/<year>.md`. If it produced a substantial written verdict — a plan for the next quarter, a composition rationale — that goes to `artifacts/audit-<year>-q<n>.md` with its `## Boxes` line.

## Graduation

A habit graduates when it has run at ≥95% for 8 consecutive weeks and the user does not deliberate about it any more. Graduation is a promotion, not a deletion.

- **Move the row to `## Retired`** with the outcome `graduated`, the final rate, the best streak, and the date. The record is the point: it is the evidence a habit was built, and it is what stops the same habit being re-proposed as new.
- **Stop logging it.** Tracking has a real ongoing cost and it is now buying nothing.
- **Keep one check.** Add a row to `## Due` for a 3-month spot check on a graduated habit: still happening, yes or no. A graduated habit that quietly stopped is easier to restart at month 3 than at month 12.
- **Raising the floor is the alternative to graduating**, and only one of them happens. If the user wants more of the behavior, raise the floor once, hold 8 weeks at the new level, and it graduates from there. Doing both at once loses the record and the level.
- **A slot opens.** Say so, and say when a new habit may be added (Rule 7).

## Retirement

Retirement is a legitimate, frequent, and healthy outcome. Say it as a decision.

Grounds: the Why expired; three honest redesigns left it below 50%; it was inherited from someone else's system; the user does not want it and has not for weeks; or the slot is worth more elsewhere.

The row moves to `## Retired` with: final 28-day rate, best streak, the date, the outcome (`graduated` · `dropped` · `superseded`), and one line on what was tried. The last field is what makes the next quarter's proposal different rather than identical.

Never delete a habit row. Deleting erases the record of what was tried, which is the most expensive data this skill holds.

## Pausing

Distinct from retirement: a pause has an end date and preserves the streak.

- Used for a known, bounded interruption — travel, a deadline week, surgery recovery (`disruptions.md`).
- The roster row gets `paused until <date>`. Paused days are `-`, not `n`, and do not enter the rate denominator.
- A pause with no end date is a retirement that nobody wanted to declare. Set the date, and if it passes twice without resumption, retire it.
- Add the resumption to `## Due` so the pause ends on purpose rather than by being forgotten.

## Keeping the Due Table Honest

- Every row: what, every how often, last run, next due. Computed, never estimated.
- Check it at session start and state overdue items once, in one line. Do not repeat the reminder in the same session.
- A cadence overdue by more than two intervals is not overdue, it is unwanted — propose dropping it or changing its frequency rather than reminding a third time.
- Every accepted cadence from anywhere in this skill lands here: check-in time, review day, monthly rollup, quarterly audit, partner check-in, contract end date, graduated-habit spot check, freeze-budget reset.

**At the end of every review**, write in the same turn: the entry in `reviews/<year>.md`; the `Last run` and `Next due` cells in `## Due`; any roster change including moves to `## Retired`; any finding with enough samples in `## Patterns`; and the new log file with its `## Boxes` line at month rollover (`memory-template.md`).
