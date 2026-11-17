# The First 30 Days

A designed habit and a running habit are different problems. This is the window where most habits die, and almost all of the deaths are structural rather than motivational.

**Before starting a new habit**, read `## Habits` in `~/Clawic/data/habits/memory.md`: Rule 7 blocks a new habit while any existing one is under 80%, and the roster is the only place that says.

## The Gate Before Day 1

Four checks. A failure on any of them means the habit does not start today.

| Check | Passing looks like | If it fails |
|---|---|---|
| Slot available | Active habits < `max_active_habits` (default 3) | Retire or graduate one first (`review.md`) |
| Existing habits healthy | Every active habit ≥80% over 28 days | Fix the weakest one; a new habit steals exactly the attention it needs |
| Two weeks since the last addition | Last `Started` date in the roster is ≥14 days old | Wait. Two habits started in the same week fail together |
| All six fields filled | Habit Anatomy complete, cue named and existing | Back to `design.md` |

The gate is the single highest-value rule in this file: it is the difference between a roster of three habits at 90% and a roster of eight at 30%.

## The Ramp

Do not start at the target. Start below the floor and let the level rise on its own.

| Days | What is asked | Purpose |
|---|---|---|
| 1-7 | The floor only, every scheduled day. Doing more is fine and is not requested | Establish the cue→behavior link, which is the only thing week 1 builds |
| 8-14 | Still the floor. Note when the behavior started happening before you thought about it | First automaticity signal; also the point where an unreliable cue is exposed |
| 15-30 | Floor unchanged. If the user has voluntarily exceeded it on ≥70% of days, the habit is finding its own level | Never raise the floor here — the excess is a signal, not a mandate |

Raising the floor before day 30 is the most common cause of the week-3 collapse: the user made a promise while motivated, the level became the requirement, and the requirement is now unmeetable on a normal day.

## Week-by-Week Failure Signatures

| Week | Typical failure | Cause | Fix |
|---|---|---|---|
| 1 | Missed day 2 or 3 | The cue did not fire — usually the anchor did not happen that day | Check whether the *anchor* occurred. If it did not, the anchor is unreliable, not the habit (`design.md`) |
| 1-2 | Done, but at a different time each day | No real cue; the user is remembering | Re-anchor before adding anything else |
| 2 | Feels pointless, no visible result | Correct and expected — 30 days is too short for most outcomes | Show the rate, restate the Why, change nothing |
| 3 | Sharp drop, motivation gone | Novelty spent; the honeymoon level was the actual requirement | Drop to the true floor and say explicitly that the floor is the whole habit |
| 3-4 | One weekday consistently missed | Schedule collision that only appears after a full cycle | A smaller variant for that day (`troubleshooting.md`) |
| 4 | Rate fine, user wants to add three more habits | The success is real and the impulse is the trap | One habit per two weeks (Rule 7); park the others in `## Habits` as `planned` |

## The Fresh-Start Effect and How to Use It

Temporal landmarks — a Monday, the first of the month, a birthday, a move, a new job — measurably raise the rate at which people begin aspirational behavior (Dai, Milkman and Riis). Two consequences, one useful and one dangerous:

- **Useful:** if the user is within a few days of a landmark and undecided, start then. The starting energy is free.
- **Dangerous:** the same effect is why January rosters have eight habits. The landmark raises the willingness to start, not the capacity to sustain. The gate above applies unchanged on January 1.

Corollary for restarts: a lapsed habit does not need a landmark to resume, and waiting for Monday costs four days of evidence (`relapse.md`).

## The First Log Entry

Write the log before the first completion, not after. An empty grid with today's date and the habit's column already present removes the "where do I even record this" friction on day 1, and it is the only pre-created structure this skill allows.

- Create `~/Clawic/data/habits/logs/<year>-<month>.md` with the habit as a column and today's row.
- Add its `## Boxes` line in `memory.md` in the same turn.
- Set the `Started` date in the roster row. The rate window in Rule 5 counts from this date, and a habit younger than 14 days is reported as "too early to say".

## What Not To Do in Month 1

- **No streak visualization before day 14.** A three-day streak is not information, and losing it produces a real abandonment risk for zero prior benefit.
- **No stakes, no forfeits, no public commitments.** Stakes on an unproven design punish the design (`accountability.md`).
- **No app migration.** Moving trackers in week 2 is displacement activity; the format costs nothing and the migration costs the habit.
- **No second habit "because they're related".** Related habits are the ones most likely to share a failure cause.
- **No outcome measurement.** Weighing daily during a month-1 training habit attaches the habit to a number that moves for unrelated reasons (`analysis.md`).

## Graduating Out of Month 1

At day 30, run the numbers once and say them plainly:

- 28-day rate, and which band it lands in (Rule 5).
- The shape of the misses: scattered (design is fine), clustered on a weekday (schedule collision), or a cliff at a date (a context change).
- One change, or explicitly no change. "No change" is the correct answer in the 80-94% band and should be said as a decision, not as silence.
- Whether a slot is now free for the next habit — two weeks after this date, not today.

**At the end of the first session that starts a habit**, write in the same turn: the roster row in `## Habits` with `Started` set, the log file with its `## Boxes` line, and any cadence the user accepted (check-in time, review day) as a row in `## Due` (`memory-template.md`).
