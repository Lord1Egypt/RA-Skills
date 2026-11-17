# The Behavior Science Pack

Working notes behind trigger_analysis.py: habit loops, implementation
intentions, reward inference, statistical honesty. Sources at the end.

## 1. The habit loop

Charles Duhigg's popularization of Wendy Wood's research: habits run on
**cue → routine → reward**, stored in the basal ganglia and executed with
near-zero deliberation. Two consequences drive this skill:

1. The routine is the OUTPUT of the loop, not the problem. Attacking it with
   willpower fights the architecture. Changing the CUE or substituting the
   ROUTINE (keeping cue+reward) works with it.
2. Once identified, cues fire the loop automatically — which is why "I'll
   just decide not to" fails at 22:47 every night. The decision isn't
   happening at that moment at all.

Wood's lab found ~43% of daily behavior is habitual (repeated in same
context), and context stability is what automates behavior — which cuts both
ways: stable context = easy habit formation AND hard habit removal. That's
why the analysis output feeds **context disruption** moves.

## 2. Implementation intentions (if-then plans)

Gollwitzer's work: specifying **when/where/how** of a goal ("IF it is 7:30
after breakfast at the kitchen table, THEN I open my notebook and write one
sentence") roughly doubles goal attainment vs. goal intentions alone.
Meta-analysis: Gollwitzer & Sheeran 2006, 94 studies, d ≈ 0.65.

Why it works: the specified cue gets "instantiated" — attention becomes
tuned to it, and the response initiates automatically when the cue appears.
The plan must name a CONCRETE cue (time, place, preceding event, internal
state) and a CONCRETE first action (≤ 2 minutes to start; the "one sentence"
trick from composition research).

Bad: "I'll exercise more when I have time."
Good: "IF I put my phone on the charger at 21:00, THEN I do the 10 squats
next to the bookshelf."

The analyzer builds if-then plans from the TOP-LIFT cue, not from whatever
cue the user guessed on day 1 — that's the whole point of measuring.

## 3. Reward inference

The journal doesn't capture the reward directly; infer it from three
journal signals:

| Signal | Likely reward class |
|---|---|
| High urge + emotional_state ≤ 2 | mood repair (escape/relief) |
| Urge follows boredom markers (prev_action = tv/scroll/wait) | stimulation |
| Behavior is social (company ≠ alone) | connection/belonging |
| Urge follows stress markers (work, deadline, conflict) | tension release |
| Time-anchored (same hour daily) | structure/transition ritual |

The reward hypothesis shapes the substitute routine: a stimulation-seeking
doomscroller needs a novel input (podcast, puzzle), not "sit with the
silence". A transition-ritual smoker after coffee needs a replacement ritual
(gum + walk to the window), not raw nicotine math.

## 4. Statistical honesty rules

The analyzer enforces:

- **Baseline requirement.** Lift divides by P(behavior | factor absent).
  With no baseline rows, there is no denominator — refuse to rank.
- **Minimum cell size.** Any factor value with < 3 event rows or < 2
  baseline rows is LOW-CONFIDENCE; never surfaced as a top trigger.
- **No double-dipping.** Time bins are disjoint; a 22:47 event can't also
  count in the "evening" and "night" bins.
- **Confounded pairs.** If two factors always co-occur (coffee AND commute
  in every event), the report says "confounded — can't separate with this
  data; probe next week by varying one" instead of pretending to know.

Lift interpretation cheat sheet:

```
lift ≥ 2.0   strong cue — build the if-then plan on it
1.5 - 2.0    real but partial — combine with time bin
1.2 - 1.5    weak — note it, don't build on it
< 1.2        noise
```

## 5. The weekly loop

```
Week 1: journal (events + baselines)  → analysis → recognition moment
        → pick top 1-2 triggers → cue disruption + if-then plan
Week 2: journal again → re-analysis → compare lift tables
        lift dropped toward 1.0 = cue decoupled
        lift unchanged = plan failed, pick different lever
Week 3+: maintenance journaling only on relapses (why did TODAY fire?)
```

Relapse handling: a relapse isn't failure, it's DATA. Log it with full
context; often the relapse reveals a second cue the first week missed
(the Friday cue under the weekday-only hypothesis).

## 6. Habit stacking (for building wanted habits)

The same journal reveals ANCHOR routines — high-frequency, stable-context
behaviors (coffee, commute, phone-on-charger, post-shower). New habits
attach best to existing anchors:

"After [anchor], I will [new 2-minute action] in [same location]."

The analyzer's hotspot table doubles as the anchor list: stable daily
time-bins are candidate anchor slots.

## 7. Scope and safety

This skill is self-tracking and self-experimentation for ordinary habits
(snacking, screens, exercise, practice routines, spending). It is NOT a
treatment for substance dependence, eating disorders, gambling, or
compulsive behavior. If the user describes loss-of-control, withdrawal,
or significant distress → recommend professional support (physician,
therapist, addiction services) and stop the self-optimization framing.

## Sources

- Wood, W., Quinn, J. M., & Kashy, D. A. (2002). Habits in everyday life:
  thought, emotion, and action. JPSP, 83(6), 1281-1297.
- Gollwitzer, P. M., & Sheeran, P. (2006). Implementation intentions and
  goal achievement: A meta-analysis. Advances in Experimental Social
  Psychology, 38, 69-119.
- Duhigg, C. (2012). The Power of Habit. (popularization; loop model)
- Fogg, B. J. (2019). Tiny Habits. (anchor→tiny action model)
- Lally, P., et al. (2010). How are habits formed: modelling habit
  formation in the real world. European J. Social Psychology, 40, 998-1009.
  (median 66 days to automaticity — set expectations accordingly)
