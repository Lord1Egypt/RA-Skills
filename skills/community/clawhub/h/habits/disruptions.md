# Travel, Illness, and Life Events

What to do when the week changed rather than the habit. Everything here is a **bounded** interruption with an end the user can name; a standing condition that changes the baseline is `capacity.md`.

**Before changing anything for a disruption**, read `## Context` in `~/Clawic/data/habits/memory.md` (constraints the user already declared), `## Habits` for what is already paused and its end date, and `## Patterns` — a trip that happens every month usually already has a row.

**Contents:** [Bounded or Standing](#bounded-or-standing) · [Three Mechanisms, Not One](#three-mechanisms-not-one) · [Maintenance Mode](#maintenance-mode) · [Travel](#travel) · [Illness and Injury](#illness-and-injury) · [Deadline Weeks](#deadline-weeks) · [Context Deletion: Moving, New Job, New Term](#context-deletion-moving-new-job-new-term) · [Step Changes](#step-changes) · [The Return](#the-return) · [Recurring Disruptions](#recurring-disruptions)

## Bounded or Standing

One question decides which file applies: **can the user name a date after which this is over?**

| Event | Shape | Handled by |
|---|---|---|
| Trip, conference, holiday | Bounded, dates known | Here |
| Acute illness, surgery recovery, injury | Bounded, dates approximate | Here |
| Deadline week, exam period, house move | Bounded | Here |
| New job, new city, new term, new season | Bounded transition, permanent result | Here — rebuild the cue, then it is normal life |
| Newborn, bereavement, a family member's illness | Starts bounded, may become the baseline | Here first; `capacity.md` when the end date stops being credible |
| ADHD, depression, chronic illness, shift rota, ongoing caregiving | No end date | `capacity.md` |

A disruption suspends the protocols temporarily. A standing condition changes the defaults permanently. Applying the wrong one produces either a habit that is paused forever or a user asked to meet a standard their week cannot contain.

## Three Mechanisms, Not One

| Mechanism | Use when | Cell | Streak | Denominator | Defined in |
|---|---|---|---|---|---|
| Freeze | One declared day, budget remaining | `f` | Intact | Excluded | `tracking.md` |
| Pause / maintenance mode | A bounded stretch of days | `-` | Preserved across the pause | Excluded | Here and `review.md` |
| Redesign | The constraint has no end date | Normal | Recomputed from the new definition | Normal | `capacity.md` |

Everything else is an ordinary miss: an unplanned day off is `n`, logged flat, no mechanism required (`relapse.md`). The mechanisms exist to keep honest data honest, not to protect a number — a pause declared after the fact is the same fiction as a retroactive freeze.

## Maintenance Mode

A declared, reduced floor for a declared period, agreed **before or on the first day**. It exists because the alternative — a full roster logged `n` through a hospital week — produces a rate that is wrong and a diagnosis built on it that is worse.

1. **Keep exactly one habit.** The keystone if one has been detected (`routines.md`); otherwise the highest-rate one, because it is the likeliest to survive and it carries the return.
2. **Halve its floor, or drop to the two-minute version**, whichever is smaller, and write the number down. "I'll do what I can" is not a floor and produces no data.
3. **Pause the rest** with `-` cells and `paused until <date>` in the roster row (`review.md`).
4. **Put the resumption date in `## Due`** in the same turn. A pause without a scheduled end is a retirement nobody declared.
5. **Review on that date.** Extend once at most; a second extension means the event was never bounded and the roster needs redesigning around the new baseline (`capacity.md`).

Reporting during and after: paused days are outside the denominator, so the 28-day rate on return is computed from the days before the pause plus the days after it. Say that when reporting — "84% over the 19 scheduled days in the window" reads as a working habit, and "46%" reads as a failure that did not happen.

## Travel

- **Two versions per habit, designed at home.** The home version and the away version both live in the roster row's note. Designing the away version in an airport is designing it while it is already failing.
- **The away version has no equipment, no place and no booking**: bodyweight instead of the gym, the book on the phone, three minutes instead of twenty. This is the no-equipment fallback of `design.md`, written out rather than improvised.
- **The cue has to travel too, and most do not.** "After I put the kettle on" does not exist in a hotel; "after I put my shoes on" does. Pick the away cue from things the user does in every bedroom they have ever slept in.
- **Time zones.** `day_boundary` is local time (`tracking.md`). Do not re-log days when crossing zones and do not compensate for a lost or gained hour — the day the user lived is the day it counts. Say it once and never again.
- **Under three nights**: no mode change. The away version or one freeze covers it.
- **Over a week**: maintenance mode, one habit, with the resumption date set before departure.
- **The week after is the risk, not the week away.** The common shape is a rate that holds during the trip and falls on return, because the home cue has to be re-established and nobody scheduled it. Check it against this person's own log before asserting it — four trips (`analysis.md`).

## Illness and Injury

- **Acute illness is a pause, not a miss.** A fever logged as `n` teaches nothing, lowers a rate for a cause that will not repeat, and invites a diagnosis of a habit that is fine.
- **Set an approximate end date anyway**, and revise it. An open pause during illness is where a habit quietly ends.
- **Return by length of absence**: ≤14 days out → resume at the floor on the next scheduled day, no ramp. More than 14 days out → it is a restart, with the restart parameters (`relapse.md`).
- **Injury usually leaves a working habit intact.** The behavior is unavailable, the cue is not: keep the cue and substitute the behavior — the shoulder injury turns the swim into a walk at the same time, and the cue never decays.
- **Recovery has its own ramp**, and it belongs to the clinician who set it. Track adherence to their ramp; never design a progression.
- **Training through illness or injury to protect a streak is a Red Flag** (SKILL.md): break the streak deliberately and record why.

## Deadline Weeks

- **Predictable crunch is not a disruption, it is the schedule.** If it happens every month-end, the frequency is wrong for this life and the fix is in the design, not in an exception negotiated four times a year (`design.md`).
- One habit at the maintenance floor; everything else paused with the deadline as the end date.
- **Do not pause the habit that regulates the crunch.** The walk, the sleep window, the shutdown routine are the ones that make the week survivable; they are the last to go, not the first.
- No new habits, no floor increases and no stakes during a crunch week (`accountability.md`).
- If a crunch week arrives with the month's freeze budget already spent, that is maintenance mode rather than one more freeze (`tracking.md`).

## Context Deletion: Moving, New Job, New Term

A context change deletes the cue and leaves the behavior intact (SKILL.md, Failure Classes). Treating it as a motivation problem is the standard error.

1. **Name the anchor that no longer exists.** The commute, the office kitchen, the campus timetable, the light at 19:00.
2. **Wait for the new day to have a shape.** Roughly two weeks: an anchor picked on day 2 in a new job is picked from a week that will not repeat.
3. **Choose the replacement anchor from what already happens reliably** in the new context, and verify it fired every day for a week before building on it (`design.md`).
4. **Restart at the floor for 14 days.** The behavior is known; the cue is not.
5. **The streak does not carry across.** It belonged to the old context. The best streak stays in the roster as history (`tracking.md`).

Seasons count as context changes and are the most predictable of all: dark at 17:00 deletes evening outdoor habits every year. Once the pattern has four samples, the habit gets a written winter version in its roster note, designed in September rather than discovered in November.

## Step Changes

A newborn, a bereavement, a move abroad, a family member becoming ill. These start as disruptions and sometimes become the baseline.

- **Pause everything except one two-minute habit.** Not two.
- **Anchor to the other person's routine**, not to a clock: feeds, naps, the medication round, the school run. In a household rearranged around someone else, those are the only reliable events left.
- **Nothing is retired during a step change.** Retiring loses the design, and the design is the part that took work; a paused row costs nothing.
- **Set a review date rather than a resumption date** — 6 or 8 weeks out — and at that review decide between resuming, extending once, and moving the roster onto low-capacity defaults (`capacity.md`).
- Grief and acute stress follow the same shape and need no habit conversation at all in the first weeks: state the pause, set the review date, stop.

## The Return

The trip does not end the habit; the first week back does.

- **The resumption date is set before the disruption starts**, in `## Due`, and it is a statement on the day, not a question (`review.md`).
- **Resume one habit on day 1 back, at the floor, and nothing else that week.** Restoring three habits at once on the Monday after a two-week absence reproduces the January roster and fails the same way (Rule 7).
- **Never make up missed days.** Doubling raises the floor in the week least able to carry it (`relapse.md`).
- **Report the rate with the pause excluded, and say the denominator.** This is the single highest-value sentence of the whole return.
- **If the return date passes twice without resumption**, the habit is retired rather than paused — say so as a decision (`review.md`).

## Recurring Disruptions

Anything that has happened four times is not a disruption. Monthly travel, a term calendar, a rotating on-call week, quarterly close — these are the year, and a habit designed for the other three weeks is a habit that fails one week in four by construction.

- Set the frequency to what the year actually contains, not what a good month contains (`design.md`). A `3×/week` habit that is honestly `2×/week` in every travel month is a `2×/week` habit with bonus weeks.
- Or design the two versions permanently, one per context, both in the roster row, and stop treating the switch as an event (`relapse.md`).
- Record the shape in `## Patterns` with its sample count; four samples is what turns "travel wrecks it" from a feeling into a design input (`analysis.md`).

**Whenever a disruption is declared, entered, or ended**, write it in the same turn: the `-` cells and the maintenance floor's `y`/`n` cells in `logs/<year>-<month>.md`; `paused until <date>` and the away or winter version in the roster row of `memory.md`; the resumption or review date as a row in `## Due`; the travel variant of a routine inside `artifacts/routine-<name>.md`; a hard constraint the user described in `## Context`; and the shape in `## Patterns` once it has been seen twice (`memory-template.md`).
