# The Miss and the Restart

What to do the moment a streak breaks, the day after, and after a lapse measured in weeks. Diagnosing a habit that has been mediocre for a month is a different job (`troubleshooting.md`); this is about discontinuities.

**Before responding to a miss**, read the current month's log to see whether this is the first, the second, or one of many — the response is entirely different in each case (Rule 6) — and `## What Works` in `memory.md` for how this person has reacted to a break before.

**Contents:** [The Escalation Ladder](#the-escalation-ladder) · [What to Say](#what-to-say) · [The Abstinence Violation Effect](#the-abstinence-violation-effect) · [Restart After a Long Lapse](#restart-after-a-long-lapse) · [Relapse into an Avoid-Habit](#relapse-into-an-avoid-habit) · [The Restart Protocol Artifact](#the-restart-protocol-artifact) · [Serial Restarters](#serial-restarters)

## The Escalation Ladder

| Event | Interpretation | Action |
|---|---|---|
| First miss | Noise. Every rate above 90% contains misses | Log `n`. One neutral line. Change nothing, propose nothing |
| Second consecutive miss | The design has a fault the first miss revealed | Stop and diagnose now — the third is much more likely than the second was (`troubleshooting.md`) |
| Third consecutive miss | The habit is dead in its current form | Say so. Redefine or pause it; do not log weeks of `n` against a habit nobody is attempting |
| Misses scattered, rate holding ≥80% | Working as designed | No action. Naming scattered misses as a problem invents one |
| Every habit missed the same day | Capacity event, not habit failure | Do not diagnose habits (`capacity.md`, `disruptions.md`) |
| Streak of 60+ days broken | Highest-risk moment in the whole domain | See below — the response here decides whether the habit survives |

The long-streak break deserves its own handling because the loss is disproportionate to the event: one missed day removed a number the user had been building for two months, and the rate barely moved. Say both facts in the same breath — "streak reset, 28-day rate 96%" — before anything else. The rate is the evidence that nothing real was lost.

## What to Say

The wording is the intervention. Three rules:

1. **Neutral, short, and first.** "Logged, missed Tuesday." No sympathy, no encouragement, no reframe. Anything longer signals that the miss was significant.
2. **Never ask why on the first miss.** The question implies an account is owed, and the next miss goes unreported to avoid it. Ask on the second, and ask about conditions rather than reasons: *what was different about Tuesday?*
3. **No recovery plan the user did not request.** An unsolicited plan after one miss says the system considers them off track, which is exactly the framing that produces abandonment.

What never appears: "don't worry", "tomorrow's a new day", "you've got this", any streak-loss commiseration, any suggestion of making it up with a double session tomorrow. Doubling is not recovery — it raises the floor on the day after a bad day, which is the worst possible day to raise it.

## The Abstinence Violation Effect

Marlatt's relapse-prevention work names the mechanism: after a lapse, the damage comes from the interpretation, not the lapse. The user who reads one missed day as evidence of a stable trait ("I never finish anything") abandons; the user who reads it as a situation ("Tuesday was a 14-hour day") resumes. This is the whole reason misses are logged flat.

Operationally, three moves interrupt it:

- **Restate the base rate.** A 90% habit misses ~3 days a month by definition. The user is comparing themselves to 100%, which no habit reaches.
- **Attribute to the condition, not the person.** Name the specific thing that was different about the day. Even a partial explanation blocks the trait reading.
- **Keep the schedule.** The next scheduled day is unchanged; the habit is not "restarting", it is continuing with one gap. Never announce a restart after one miss — the word itself concedes that the run ended.

The same mechanism, at higher intensity, is what turns one cigarette into a resumed pack-a-day (`quitting.md`).

## Restart After a Long Lapse

Weeks or months since the last completion. The old habit is not paused, it is gone — the cue association has decayed and the context that supported it has usually changed.

Restart parameters, all deliberately below the old level:

| Parameter | Setting | Why |
|---|---|---|
| Floor | Half the previous floor, or the two-minute version, whichever is smaller | The old floor is now unproven; treating it as known is the most common restart failure |
| Frequency | One step down: `daily` → `weekdays`, `4×/week` → `2×/week` | An easy schedule that is met beats the old one that is not |
| Cue | Re-picked from the *current* day, never reused on assumption | The old anchor frequently no longer happens; verify it does before reusing it |
| Streak | Starts at zero. The old best streak stays in the roster as history | Reclaiming the old number is not available, and pretending otherwise poisons the counter |
| Duration at this level | 14 days minimum before any increase | Long enough to prove the new cue fires |

Two things to say out loud at restart: what specifically ended it last time (from the log's shape and `## Patterns`), and what is different now. If nothing is different, the restart will end the same way — change the cue, the floor, or the environment before starting (`environment.md`).

Do not wait for Monday. The fresh-start effect is real but a week of delay costs a week of evidence, and the delay itself is often the avoidance (`starting.md`).

## Relapse into an Avoid-Habit

Different physics: the event happened, and the risk is escalation rather than decay.

1. **Log the lapse the day it happens**, with the trigger and the circumstances. The trigger inventory in `artifacts/quit-<thing>.md` is built from exactly these entries and is the reason the next attempt is better designed (`quitting.md`).
2. **Distinguish a lapse from a resumption.** One instance is a lapse; the same trigger firing three times in a week without interception is a resumption, and the plan needs rebuilding rather than restarting.
3. **Do not reset the clean-day counter to zero silently.** Record both: days clean before the lapse, and the new count. The prior run is the evidence that the plan works.
4. **The next 48 hours decide it.** The intervention window after a lapse is short — re-establish the substitution behavior at the next occurrence of the trigger, not tomorrow in general.
5. **Escalating substances** — alcohol, nicotine, anything with physical dependence — a lapse after a long clean period can restore tolerance and consumption quickly. If the lapse involved heavy drinking or the user describes withdrawal symptoms, that is the Red Flags table in SKILL.md, not a habit conversation.

## The Restart Protocol Artifact

After the second restart of the same habit, write the protocol down instead of re-deriving it: `~/Clawic/data/habits/artifacts/restart-<habit>.md`, with its `## Boxes` line and a read condition of "read whenever `<habit>` has lapsed".

Contents: what the habit's floor and cue were, the two or three conditions that have ended it historically, the restart parameters that worked last time, and the one thing to change before starting again. Six lines is enough. Deriving this from scratch every time is why the third attempt is usually no better designed than the first.

## Serial Restarters

A user on their fifth restart of the same habit is not failing at discipline; the habit is wrong in one of three ways, and the log says which.

| Pattern across restarts | Diagnosis | Move |
|---|---|---|
| Each attempt lasts 2-3 weeks, same shape | The floor is set at the motivated level every time | Restart at a floor small enough to feel unserious, and hold it for 8 weeks |
| Each attempt ends at a context change (term, season, travel) | The habit depends on a context that is not permanent | Design the two versions up front, one per context (`disruptions.md`) |
| Attempts end without a visible cause and the user shrugs | The Why does not survive contact with a bad day | Re-derive the Why, or retire the habit honestly — five failed attempts is data (`design.md`, `review.md`) |

Retiring a habit after repeated honest attempts is a legitimate outcome and frees a slot (Rule 7). Say it as a decision, not as a concession.

**After any miss, lapse, or restart**, write in the same turn: the `n` or `f` cells in `logs/<year>-<month>.md`; the condition that caused it in `## Patterns` of `memory.md` once it has been seen twice; the new floor, cue and `Started` date in the roster row on a restart; and `artifacts/restart-<habit>.md` with its `## Boxes` line from the second restart onward (`memory-template.md`).
