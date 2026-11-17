# Logging, Streaks, and Rate Math

The mechanics of recording a day and computing the numbers that get reported. Every formula here is the canonical one for this skill.

**Before reporting any number**, read the current month's log at `~/Clawic/data/habits/logs/<year>-<month>.md`, and the previous month's file if the window crosses the boundary. A rate quoted without reading the log is a guess.

**Contents:** [The Log Grid](#the-log-grid) · [Which Day a Completion Belongs To](#which-day-a-completion-belongs-to) · [Scheduled Days by Frequency](#scheduled-days-by-frequency) · [Completion Rate](#completion-rate) · [Streak Math](#streak-math) · [Streak Freezes](#streak-freezes) · [Logging Etiquette](#logging-etiquette) · [Missing and Backfilled Days](#missing-and-backfilled-days) · [Quantities Alongside the Yes](#quantities-alongside-the-yes) · [Importing from a Tracker App](#importing-from-a-tracker-app) · [Month Rollover](#month-rollover)

## The Log Grid

One file per month, one row per date, one column per active habit. Full format in `memory-template.md`.

| Symbol | Meaning | Counts as scheduled | Counts as completed |
|---|---|---|---|
| `y` | Done, at least the floor | yes | yes |
| `n` | Scheduled and missed | yes | no |
| `-` | Not scheduled that day | no | no |
| `f` | Freeze used — a planned, declared miss | no | no |
| *(blank)* | Unknown; the day was never logged | no | no |

The distinction between `n` and blank is the one that keeps the data honest: `n` is evidence of a miss, blank is absence of evidence. Blanks lower the confidence of the window; they never lower the rate.

## Which Day a Completion Belongs To

Calendar midnight is the wrong boundary for humans. Use `day_boundary` (default 04:00): anything completed before that time is logged against the previous date.

Formula: `log_date = completion_datetime − day_boundary`, truncated to the date. A 01:30 workout on the 12th logs to the 11th. A 05:00 run logs to the 12th.

Consequences worth stating once to the user: a habit done at 02:00 does not break the previous day's streak, and it also does not count twice. Night-shift workers usually want a boundary near the middle of their sleep, not 04:00 (`capacity.md`).

## Scheduled Days by Frequency

The denominator of every rate. Compute it, never estimate it.

| Frequency | Scheduled days in a window | Notes |
|---|---|---|
| `daily` | Every day in the window | 28 in a 28-day window |
| `weekdays` | Mon-Fri only; Sat/Sun are `-` | 20 in a 28-day window |
| `N×/week` | `N × (whole weeks in the window)` | Weeks bounded by `week_start`; a partial week at the edge is excluded, not prorated |
| `weekly` | One per week window | 4 in a 28-day window |
| `every-N-days` | Computed forward from the last `y`: next scheduled = last completion + N days | A miss does not shift the schedule — the next slot stays where the calendar put it |

Freeze days (`f`) are subtracted from scheduled days for every frequency. Days before the habit's `Started` date are not scheduled.

## Completion Rate

```
rate = completed_days ÷ scheduled_days      over a rolling 28-day window
```

Worked example. Habit `gym`, `3×/week`, 28-day window with `week_start: monday`. Four whole weeks → scheduled = 12. Log shows 9 sessions and one freeze week where only 2 were scheduled after the freeze. Scheduled = 12 − 1 = 11, completed = 9, rate = 9 ÷ 11 = **82%** → the 80-94% band, so the answer is "working, change nothing" (Rule 5).

Reporting rules:

- **28 days, always.** Not "this month", which is a variable-length window that makes two consecutive reports incomparable. Month figures belong in the monthly review, labelled as such (`review.md`).
- **Under 14 days of data → no rate.** Say the sample is too small and give the raw counts instead.
- **Blanks shrink the window, not the score.** With 6 blank days, report the rate over the 22 known days and say the window is 22 of 28.
- **State the denominator whenever it is not obvious**: "9 of 11 scheduled" reads honestly; "82%" alone invites a comparison with a daily habit's 82%, which is a much larger number of events.

For `N×/week` habits the weekly view is the one the user thinks in: report satisfied weeks (3 of 4) alongside the rate.

## Streak Math

| Frequency | Current streak | Breaks when |
|---|---|---|
| `daily` | Consecutive days ending today or yesterday with `y` | Any `n` |
| `weekdays` | Consecutive weekdays with `y`; weekends are transparent | Any weekday `n` |
| `N×/week` | Consecutive **weeks** where completions ≥ N | A week ends below N |
| `weekly` | Consecutive weeks with ≥1 `y` | A week with none |
| `every-N-days` | Consecutive scheduled slots hit | A scheduled slot passes with no `y` |

Rules that stop the counter from lying:

- **Never store the current streak.** Recompute it from the log every time. A stored counter drifts the first time a day is corrected, and a wrong streak is worse than no streak.
- **Best streak is stored**, in the roster row, with the date it ended. It is the one number that cannot be recovered once a monthly log is archived and the window has moved past it.
- **A streak ending yesterday is still alive today** until today's scheduled slot passes. Do not announce a break at 09:00 for a habit whose cue is at 21:00.
- **Freezes are transparent to the streak** and count toward the freeze budget, not against the run.
- Report the streak **after** the rate unless `primary_metric: streak` (Rule 4).

## Streak Freezes

A freeze is a miss the user declares in advance, for a reason they name, that keeps the streak intact. It exists because the alternative — a broken streak on a day with a legitimate reason — is a known abandonment trigger (Rule 6).

- Budget: `streak_freeze_budget` per calendar month, default 1. Unused budget does not carry over.
- Declared **before or on the day**, never retroactively. Retroactive freezes are how a 200-day streak becomes fiction.
- Logged as `f` with the reason in the note column.
- Budget exhausted and another legitimate day arrives → that is maintenance mode, not a freeze: the habit is formally paused with an end date, and the streak is preserved across the pause (`disruptions.md`).
- Freezes on an avoid-habit are meaningless — a clean-day counter cannot be frozen through a lapse (`quitting.md`).

## Logging Etiquette

- **One line, no ceremony.** "Logged." Not a paragraph, not a celebration, unless the user has asked for one (`checkin_style`).
- **A miss gets the same tone as a completion.** Any difference in warmth between `y` and `n` teaches the user to stop reporting misses, and the missing data destroys the diagnosis.
- **Never ask twice in one day.** If today's cell is already filled, the check-in for that habit is done.
- **Batch by default.** One question covering every habit due today costs one interruption; per-habit prompting costs three and gets ignored by week two.
- **Multiple days reported at once** ("I did it Monday and Tuesday") is fine — those are recalled, not guessed, and the user is asserting them. Reconstructing a week they cannot recall is not (below).
- **Never add a habit to the log without a roster row.** A column with no definition has no frequency, so it has no denominator.

## Missing and Backfilled Days

| Situation | Do |
|---|---|
| User says "I forgot to log, but I did it Tuesday" | Write `y` for Tuesday. Recall is data |
| User says "I probably did most of last week" | Leave blank. Say the window is incomplete and report over known days |
| Gap of several weeks, user cannot recall | Leave blank and treat it as a lapse for diagnosis, not as misses (`relapse.md`) |
| User wants to mark yesterday `y` to save a streak they did not earn | Refuse the edit in one neutral line and log `n`. A fabricated streak makes every future number meaningless, and the user knows it, which is why the streak stops motivating |
| Correcting a genuine mistake in a past cell | Edit in place, no annotation needed — the cell is the record, not an audit trail |

## Quantities Alongside the Yes

Some habits carry a natural number. Keep the grid binary and put the number in parentheses inside the habit's own cell: `y (32 min)`, `y (14 pages)`. The rate math stays valid, and the series stays readable; the `Note` column is left for reasons — a freeze's declared cause, a lapse's trigger.

Escalate out of the log when the number is the point: a series the user wants to analyse over months belongs in its own box — body metrics to the shared `~/Clawic/data/health/`, spending to `~/Clawic/data/finances/`, anything else to `~/Clawic/data/habits/<plural-noun>.md` with its `## Boxes` line (`memory-template.md`).

## Importing from a Tracker App

When `external_tracker` names an app, that app is the source of truth and this skill does not double-log. Import on review day rather than daily.

- Ask the user to export; do not attempt to reach the service. Most exports are CSV with one row per completion, or one column per habit.
- Map their frequency semantics before importing. Apps differ on the two things that matter: whether a "skip" counts as scheduled, and whether the week starts Monday or Sunday. A mismatch on either silently shifts every rate.
- Import into the monthly grid using the same symbols; anything the export does not distinguish becomes blank, never `n`.
- Historical best streaks from the app go into the roster row as `Best`, with `(imported)` and the date — imported streaks are not comparable to computed ones because the app's freeze and skip rules were different.
- Strip any token or account identifier from the export before writing anything (`memory-template.md`).

## Month Rollover

At the first log of a new month:

1. Create `logs/<year>-<month>.md` with a column for every **active** habit, retired ones dropped.
2. Add its `## Boxes` line and remove the line for any month older than 24 months only if the file is deleted — never orphan a file by deleting its index line.
3. Rate windows cross files: a 28-day window on the 10th reads both the current and the previous file.
4. Reset the freeze budget.

**After every logging turn**, the day's cells are written to `logs/<year>-<month>.md` before the reply ends, and a beaten best streak is written to the roster row in `memory.md` in the same turn (`memory-template.md`). A number reported but not written is a number that will be recomputed wrong next week.
