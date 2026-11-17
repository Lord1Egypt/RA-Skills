# ADHD, Low Mood, Shift Work, and Caregiving

The standard protocol assumes a day with a stable shape, an anchor that fires, and a reward response that works. When one of those is missing the defaults are wrong — not the user. Everything here is a **standing** condition; a bounded interruption with an end date is `disruptions.md`.

**Before changing any default**, read `## Context` in `~/Clawic/data/habits/memory.md` and `config.yaml`. The constraint is usually already recorded, and asking someone to re-explain their diagnosis, their rota or their caring load is the fastest way to lose them.

**Contents:** [The Defaults That Change](#the-defaults-that-change) · [ADHD](#adhd) · [Low Mood and Depression](#low-mood-and-depression) · [Shift Work](#shift-work) · [Chronic Illness, Pain, and Fatigue](#chronic-illness-pain-and-fatigue) · [Caregiving](#caregiving) · [What Never Goes to a Low-Capacity User](#what-never-goes-to-a-low-capacity-user) · [When It Is Not Capacity](#when-it-is-not-capacity)

## The Defaults That Change

Applied whenever any condition in this file is in play. These are `config.yaml` values, so they are written once and stop being a negotiation.

| Setting | Standard | Low-capacity default | Why |
|---|---|---|---|
| `max_active_habits` | 3 | 1, two once the first holds 8 weeks | Attention is the binding constraint, and it is the one that is short |
| Floor | Two-minute version | The version doable on the worst day of the worst *week*, not the worst day of a normal week | The bad days are frequent enough to define the habit rather than to be exceptions |
| `primary_metric` | completion-rate | completion-rate, and the streak is not shown unless asked | A counter that resets on a symptom is a punishment schedule |
| `stakes_allowed` | false | false, and not offered | Adds financial or social cost at the exact moment capacity fails (`accountability.md`) |
| `checkin_style` | batch | batch, or `none` on request | One prompt a day is the ceiling; three is a reason to uninstall |
| Rule 5, `<50%` band | Halve the floor or re-anchor | Cut to one habit **first**, then halve the floor | With three habits at 30% there is nothing to diagnose — the roster is the fault |
| Adding a habit | Every existing habit ≥80% and 14 days since the last addition (Rule 7) | The same, but the first habit holds ≥80% for eight weeks | Two weeks of ≥80% is the honeymoon reading; it does not predict here |

Two things do **not** change: the rate is still computed over 28 days from the log (Rule 4), and a miss is still logged flat (Rule 6). Softening the data to be kind produces a diagnosis that is wrong in the direction that hurts most.

## ADHD

Initiation runs on interest, urgency and visibility rather than on intention, so a habit that depends on remembering a plan loses to whatever is currently interesting. Design for the moment of starting; the behavior itself is rarely the problem.

- **Externalize the cue physically.** An object out of sight is not a cue. Object in the path, never in the drawer, and the tidy version of a room is usually the version where nothing gets done (`environment.md`).
- **Body doubling first**, ahead of every incentive scheme — a scheduled session with another person present, with no accountability content at all (`accountability.md`).
- **Novelty decay is the signature failure**: a high rate for two or three weeks, then a cliff, repeating at every floor including the smallest. Distinguish it from the week-3 honeymoon collapse of `starting.md` — that one is cured by a smaller floor, this one is not. The fix is scheduled variation of the *form* while the cue, the floor and the frequency stay fixed: a new route, a different room, a changed playlist, a different book.
- **Transitions are where it fails, not the habit.** The cost is stopping what came before. Anchor to a transition that already forces a stop — leaving the building, the end of a call, the car door closing — never to a moment inside an absorbing activity.
- **Chain length: two links, not the standard three** (`routines.md`) — an explicit exception, because per-link reliability is lower and the chain multiplies it.
- **Time blindness makes "later today" a non-schedule.** Every habit has a named anchor or it does not exist. A visible timer at the start converts an open-ended session into a bounded one, which is what makes starting cheap.
- **Medication timing is a scheduling constraint like any other**: place the habit inside the window the user already knows is reliable for them, and never advise on the medication.
- What reliably fails: reminders as a substitute for a cue (they habituate in about two weeks, `troubleshooting.md`), elaborate trackers, point systems, and adding the second habit early.

## Low Mood and Depression

**Check the Red Flags table in SKILL.md first.** Two weeks of missing everything with flat mood and no enjoyment anywhere is not a tracking problem: say so plainly, drop the tracking pressure, and route to a clinician. Nothing below replaces that.

Where habit work is still appropriate:

- **Activity precedes mood, not the reverse.** Behavioral activation — scheduling the action and doing it before wanting to — is the mechanism, and in Jacobson's component analysis of CBT the activation component alone performed comparably to the full package. Consequence for the protocol: never wait for motivation to return before restarting, and never frame the habit as something to be enjoyed yet.
- **One habit, and a floor small enough to sound unserious.** Sit up. Open the curtains. Two minutes outside. The floor is the whole habit and it is said out loud as such.
- **No streak, no stakes, no forfeits, no public commitment.** Every one of them converts a symptom into a failure event.
- **The rate is not a performance report during an episode.** Report it only when asked, and state the base rate alongside it: a 90% habit misses three days a month by definition (`relapse.md`).
- **Self-punishment or shame language attached to a miss suspends tracking entirely** — that is the Red Flags row, and the correct move is to remove every stake and revisit only the Why.
- **What the habit is for here is evidence, not treatment.** Say it once: the log exists so a bad week can be compared against a real record rather than against a memory that is currently unreliable.

## Shift Work

- **The weekday is meaningless; the shift is the schedule.** Convert every frequency to shift-relative terms — "after the first shift of a block", "on rest days", "not on nights" — and set the scheduled days from the rota, never from the calendar.
- **Move `day_boundary`** to roughly the middle of the user's sleep instead of the 04:00 default (`tracking.md`). For someone finishing at 07:00 and sleeping until mid-afternoon, a boundary near 10:00 keeps a post-shift session on the day it belongs to. It is a declared preference: write it to `config.yaml`.
- **Two cue sets, one per shift type**, both written in the roster row. No single anchor exists in both a day shift and a night shift, and pretending otherwise produces a habit that works one week in three.
- **Report the rate per shift type when they differ by more than one band.** An averaged 60% can be 90% on days and 25% on nights, which are two different problems and one of them is not a habit problem.
- **`every-N-days` is usually the honest frequency** on a rotating rota, because it computes forward from the last completion rather than from a week the rota ignores (`tracking.md`).
- **Sleep debt is upstream.** A habit that fails on the third consecutive night shift is a sleep problem, not a design problem — hand that part to `sleep` and keep the habit's floor at the version that survives it.

## Chronic Illness, Pain, and Fatigue

- **The floor must be safe on a bad day**, and for an energy-limiting condition "safe" sometimes means not done. Where a condition involves post-exertional symptoms, the floor is set with the clinician's pacing advice, not against it.
- **Boom-and-bust looks like the honeymoon sawtooth and is not it.** The distinguishing sign: in boom-and-bust the good day is followed by a day *worse* than baseline. The fix is a **ceiling** rather than a floor — cap the good-day version, which is the one instruction in this skill that limits doing more.
- **`N×/week` or `every-N-days` over `daily`.** A daily schedule on an unpredictable condition manufactures misses that carry no information.
- **Flares are pauses** with an approximate end date, and they are frequent enough that the pause is a normal state rather than an exception (`disruptions.md`).
- **Never a streak.** An unpredictable symptom resetting a counter is the counter punishing the symptom.
- **Report against available days.** "Done on 8 of the 11 days you were able" is the true measurement; a rate computed against a schedule the body did not have is a fiction in both directions.

## Caregiving

- **The constraint is interruptibility, not time.** A 20-minute habit that cannot be paused is harder than a 40-minute one that can. Choose behaviors that survive being cut off at 30 seconds, and define what counts as done when they are: started *is* done here, legitimately.
- **Anchor to the other person's routine** — the nap, the medication round, the school run, the carer's arrival. In a day built around someone else, those are the only reliable events.
- **One habit, and it belongs to the carer.** A habit that serves the household is a task; it does not go in this roster.
- **A respite window is the slot**, and it is the first thing to protect and the first thing given away. Naming it as the habit's slot is what stops it being spent on admin.
- **A newborn starts as a step change** and is handled as a disruption while an end date is credible; it moves here once the load is clearly the new baseline (`disruptions.md`).
- Expect the roster to shrink, and say it as a decision rather than letting it erode unannounced: one habit held through a caring year beats four abandoned in month two.

## What Never Goes to a Low-Capacity User

- Stakes, forfeits, or any consequence attached to a miss — including tone (`accountability.md`).
- Streak-led reporting, streak visualizations, or a milestone celebration that implies the next miss costs something.
- A second new habit before the first has held eight weeks.
- A reminder offered as the fix for a missing cue. It patches the symptom and habituates (`troubleshooting.md`).
- "Do it at the same time every day" to someone whose day has no fixed shape.
- A comparison with a higher-capacity period of their own life. It is the same demotivating comparison as comparing with another person, with the added weight of being about them.
- Unsolicited encouragement after a miss. Neutral and short, exactly as for everyone else (`relapse.md`).

## When It Is Not Capacity

Capacity is what the log looks like across **all** habits at once. A single failing habit is never evidence of it.

- Two habits at 85% and one at 20% is one bad design, not a capacity ceiling — diagnose the third normally (`troubleshooting.md`).
- Every habit dropped in one week, then everything fine again, is a bounded event (`disruptions.md`).
- Everything failing in an unremarkable week, with three habits on the roster, is a roster problem: cut to one (Rule 7).
- A user who describes low capacity while the log shows a stable roster gets the honest answer — the data does not show it — said once, without argument, and the constraint is recorded in `## Context` anyway. The next collapse will say which of the two readings was right.

**Whenever a capacity constraint is described, changed, or resolves**, write it in the same turn: the constraint and what it changes in `## Context` of `memory.md`; every adjusted default (`max_active_habits`, `day_boundary`, `checkin_style`, `primary_metric`, `stakes_allowed`) as its key in `config.yaml`, because those are declarations rather than observations; the shift-relative frequency and the second cue set in the roster row; and what worked or backfired for this person in `## What Works` (`memory-template.md`).
