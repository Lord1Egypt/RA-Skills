# Designing a Habit

Turning "I want to be healthier" into a row that can be answered yes or no tonight. Every field here maps to a column of the roster in `memory.md`.

**Before designing anything**, read `## Habits` in `~/Clawic/data/habits/memory.md` (or `roster.md` if `## Boxes` points there) and `## What Works`. Designing a habit this person already tried and dropped, in the same form, is the most common wasted turn in this domain.

**Contents:** [From Wish to Behavior](#from-wish-to-behavior) · [Picking the Cue](#picking-the-cue) · [Setting the Floor](#setting-the-floor) · [Choosing the Frequency](#choosing-the-frequency) · [Writing the Why](#writing-the-why) · [Do-Habits vs Avoid-Habits](#do-habits-vs-avoid-habits) · [Quantity Habits](#quantity-habits) · [Skill-Practice Habits](#skill-practice-habits) · [Identity Framing](#identity-framing) · [The Design Interview](#the-design-interview)

## From Wish to Behavior

The conversion is mechanical. Take the stated wish, ask what the smallest observable act that produces it is, and keep descending until it passes the bedtime test: can this be answered yes or no by bedtime, by someone who was not there?

| Wish | Not a habit because | Behavior |
|---|---|---|
| "Get in shape" | No observable act, no day | Walk 20 min after lunch, weekdays |
| "Read more" | "More" is a comparison, not an event | Read 1 page in bed before lights out |
| "Be less on my phone" | Absence of an act — nothing to log | Phone charges in the kitchen from 22:00 (`quitting.md`) |
| "Learn Spanish" | An outcome measured in years | 10 min of review after breakfast |
| "Stop being late" | An outcome of a chain of behaviors | Set out clothes and bag the night before |
| "Meditate regularly" | Frequency undefined | 3 min after the morning alarm, daily |

Two behaviors are worse than one behavior that produces two outcomes. When the user names three wishes, look for the single act that touches all three before proposing three rows — a 20-minute morning walk can be the exercise habit, the sunlight habit and the thinking habit, and it is one line in the log.

## Picking the Cue

The cue is an event that already happens without effort, at a stable time, in a stable place. Rank candidates by reliability, not by convenience.

| Cue quality | Example | Reliability |
|---|---|---|
| Existing physical action, fixed place | "After I put the kettle on" | Highest — the place does half the remembering |
| Existing action, variable place | "After I close the laptop" | Good, until a day breaks the location |
| Transition between contexts | "When I walk in the door" | Good; transitions are where new behavior fits |
| Clock time with an alarm | "07:30 alarm" | Mediocre alone — an alarm is dismissible and habituates in ~2 weeks |
| Another new habit | "After my new morning journal" | Worst — the chain is only as reliable as the newest link (`routines.md`) |
| A feeling ("when I feel like it", "when motivated") | — | Not a cue. Reject and re-anchor |

Cue selection rules:

- The cue must **precede** the behavior with no gap. "After coffee, sometime that morning" is not a cue; the gap is where the habit dies.
- Prefer a cue that happens on **every scheduled day**. A cue that only fires on weekdays cannot support a daily habit — that habit needs two cues, one per context.
- Say the cue out loud in the format of Rule 3 before writing the row: *after `<anchor>`, I will `<minimum>` in `<location>`*. If it cannot be said in that form, the design is not finished.
- A cue that already carries another habit is a stack — three links maximum, one new (`routines.md`).

## Setting the Floor

The floor is what gets logged. It is not the ambition; it is the version that survives a fever, a deadline, and a 23:40 arrival home.

Test, in order:
1. **Two-minute start.** The floor can be begun in under two minutes with nothing to fetch, install, change into, or decide.
2. **Worst-day test.** Ask: would you do this on the worst day of last month? If the answer needs a qualifier, halve it and ask again.
3. **No-equipment fallback.** If the floor needs a place or a device, define the fallback version that does not (`disruptions.md`).

| Ambition | Floor that gets logged | Why this floor |
|---|---|---|
| Run 5k | Put shoes on and step outside | The threshold act; the run is what usually follows |
| Write a novel | Open the file and write one sentence | Removes the blank-page decision, which is the actual obstacle |
| Gym 4×/week | Enter the gym and do one set | The commute is the expensive part, not the workout |
| Meditate 20 min | 3 slow breaths, seated | 20 min is a target for good weeks and a skip trigger on bad ones |
| Floss | One tooth | Absurd on purpose; absurdity is what keeps it from being skipped |

Doing more than the floor is normal and is logged as the same `y`. Never introduce a partial credit scheme — the moment "half done" exists, every day becomes a negotiation.

## Choosing the Frequency

| Frequency | Use when | Streak semantics |
|---|---|---|
| `daily` | The behavior benefits from zero decisions and the cue exists every day | Breaks on any miss; strongest formation, most fragile counter |
| `weekdays` | The cue is tied to work context and weekends have a different shape | Weekend days are `-`, not misses |
| `N×/week` | The act is costly (training, long study) and the specific day does not matter | Streak counts satisfied weeks, not days — the window depends on `week_start` |
| `weekly` | Reviews, calls, admin, long-form work | One satisfied occurrence per window; a missed week is a full miss |
| `every-N-days` | Recovery-bound activity (heavy lifting, skin treatment) or deliberately spaced practice | Next scheduled day computed from the last completion, not from a calendar |

Choosing rule: **daily whenever the cost per instance is under ~10 minutes**, because a daily habit needs no scheduling decision and the decision is the expensive part. Above ~30 minutes per instance, use `N×/week` and let the user place the days. Between the two, prefer daily with a small floor and let the long version happen on the days that allow it.

Frequency mistakes that show up as "discipline problems": a `daily` habit whose cue only exists on workdays; a `3×/week` habit the user always attempts on Friday, Saturday, Sunday, giving four empty days and one crowded weekend; a `weekly` habit with no fixed day, which is functionally unscheduled.

## Writing the Why

One sentence, in the user's own words, captured at design time when motivation is high — it is written for the day it is low. Two failure modes: a generic Why ("it's healthy") that persuades nobody, and a borrowed Why from someone else's reasons.

Extract it by asking once, then stop: what changes in your life if this is true in six months? Keep the concrete half of the answer, drop the abstraction. "So I can carry my kid up the stairs without stopping" survives day 40; "improve cardiovascular health" does not.

The Why is also the retirement test: when a habit no longer serves its Why, it is retired rather than repaired (`review.md`).

## Do-Habits vs Avoid-Habits

They share a roster but almost nothing else. Get the `Type` right at design time.

| | `do` | `avoid` |
|---|---|---|
| Logged event | The behavior happened | The day passed without it |
| Cue role | Trigger to start | Trigger to intercept and substitute |
| Floor | Smallest version of the act | Not applicable — there is a rule, and a substitution behavior |
| Failure shape | Nothing happened | Something happened, usually at a predictable time |
| Streak meaning | Consecutive completions | Consecutive clean days; a single lapse has a different weight |
| Design work | Cue, floor, frequency | Trigger inventory, friction, substitution, escalation plan (`quitting.md`) |

An avoid-habit designed with do-habit machinery — "resist scrolling, daily, minimum: don't" — is untrackable and fails within days. Convert it: every avoid-habit gets a paired do-habit that occupies the same trigger.

## Quantity Habits

Some habits carry a number: pages, steps, grams, minutes, glasses. The number is not the habit.

- Log the yes/no against the **floor**, and record the quantity in the note column only if the user wants the series. Two columns, one decision.
- A quantity that must be tracked as a series belongs in a shared box, not in the habit log: body measurements go to `~/Clawic/data/health/`, spending to `~/Clawic/data/finances/`. The habit log stays binary so the rate math stays valid.
- Never move the floor upward because the user has been exceeding it. That converts a working habit into a target and drops it a band (Rule 5). Raise the floor once at graduation, deliberately (`review.md`).

## Skill-Practice Habits

Practicing an instrument, a language, or a craft has a shape the standard model handles badly: quality of the session matters, sessions vary in length, and progress is not linear.

- Track **the session happening**, never its quality — quality ratings turn into self-assessment and self-assessment turns into avoidance.
- Set the floor at the setup act (open the case, open the app), because for skill practice the setup is the barrier and the session extends itself.
- Keep the content plan outside the habit log; the habit answers "did I sit down", the plan answers "to do what". A plan that lives in the habit row makes both harder to change.
- Expect plateaus. A stable rate with no felt progress is a curriculum problem, not a habit problem — the habit is working and something else needs to change.

## Identity Framing

Use it when the user already believes a version of the claim ("I'm someone who trains, I've just stopped"). It converts each completion into evidence and makes a miss survivable, because one miss does not unmake an identity.

Skip it when the claim is not yet credible to them. Telling someone who has never sustained anything that they are "a consistent person" invites the contradiction, and the miss then falsifies the identity rather than the design. For that user: two-minute floor, count the evidence, and let the identity be their conclusion rather than your premise (`Where Experts Disagree` in SKILL.md).

## The Design Interview

Maximum one question per unresolved field, and only if the default cannot resolve it. Defaults that usually can: frequency from the cost per instance, floor from the two-minute test, `Type` from the wording of the wish.

1. What does the day look like where this happens? — extracts the cue and the location at once.
2. What is the smallest version you would still count? — then halve their answer, and say you are halving it.
3. What changes if this is true in six months? — the Why, in their words.

Then read back the row in one line and write it: *after `<cue>`, `<minimum>`, `<frequency>` — because `<why>`*.

**When a habit is designed, redefined, or rejected**, write it in the same turn: a new or changed row in `## Habits` of `memory.md` with all six fields, or — if the user tried this design before and dropped it — a line in `## What Works` recording which form failed, so the next proposal is a different one (`memory-template.md`).
