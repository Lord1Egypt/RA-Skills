---
name: habit-trigger-detective
description: "Use when someone keeps failing the same habit or falling into the same bad one despite motivation. Turns a trigger journal into a statistical trigger analysis - time-of-day, location, company, device, emotional state, preceding actions - and outputs ranked cues, the habit loop, and reengineered if-then plans."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [habits, behavior-change, trigger-analysis, habit-loop, if-then-plans, self-tracking]
---

# Habit Trigger Detective

## Overview

"I know what I should do. I just don't do it." The failure of habits is rarely
motivation — it's **unidentified triggers**. The cigarette happens after coffee,
the doomscroll starts when the phone is on the nightstand, the snack raids
happen at 22:47, the skipped workouts cluster on days with early meetings.
People try to change the behavior while leaving the cue architecture intact.

Behavioral science ( habit-loop research, implementation-intention studies)
says: identify the CUE → understand the REWARD → reengineer the loop. This
skill does the boring-but-decisive part: **statistics over a trigger journal**.

For 5-7 days the user logs each occurrence (wanted or unwanted behavior):
time, location, who's around, device in hand, emotional state 1-5, what they
were doing in the previous 30 minutes, and subjective urge strength. The
analyzer then:

1. Computes **lift** for every factor value — how much more likely the
   behavior is when that factor is present vs. baseline (like market-basket
   analysis).
2. Finds **time-of-day hotspots** (binned into morning/afternoon/evening/night).
3. Detects the **preceding-action chain** — the 1-2 step behavioral runway
   that most reliably precedes the behavior.
4. Assembles the **habit loop**: cue → routine → (inferred) reward.
5. Generates **reengineered if-then plans** (implementation intentions) and
   **cue disruption** moves — ranked by expected impact.

## When to Use

- "I keep failing to [exercise / meditate / write / practice language]"
- "I can't stop [snacking / vaping / doomscrolling / online shopping / biting nails]"
- Any behavior the user wants more of or less of, occurring 3+ times/week
- After a streak broke: "figure out WHY it broke"
- Pre-building a new habit into an existing routine ("habit stacking" needs
  to know which anchor routines exist)

**Don't use for:** addiction-level issues (alcohol, drugs, gambling, eating
disorders — refer to professionals; this is a self-tracking tool, not
therapy), or one-off behaviors with no repetition.

## The method

### Phase 1 — Journal (5-7 days, 30 seconds per entry)

The user logs each occurrence with a fixed schema (scripts/trigger_log.py
interactive mode, or a paper template in references/journal-template.md):

```
timestamp | behavior (smoke/scroll/snack/skip-workout...) | wanted/unwanted
location (home/work/commute/other) | alone | with-partner | with-friends | with-colleagues
device (none/phone/laptop/tv) | emotional_state 1-5 | urge 1-5
prev_action: what you were doing in the last 30 min (free text)
```

Critical: also log 5+ **baseline entries** — random moments when the urge was
NOT present. Without a baseline, "80% of events happened at home" is
meaningless (maybe you're home 80% of the time). Lift is computed against
this baseline.

### Phase 2 — Analysis

For every factor value (e.g., location=commute):

```
P(behavior | factor)     count_events_with_factor / count_all_factor_rows
P(behavior | no factor)
lift = P(behavior|factor) / P(behavior|no factor)
```

- lift > 1.5 with enough samples = a real cue candidate
- The analyzer flags statistical honesty: values with < 3 samples are marked
  LOW-CONFIDENCE, never surfaced as top triggers.

Preceding-action chains: normalize prev_action text (lowercase, keyword map),
compute P(behavior | prev_action) the same way, and find 2-step chains
(A→B→behavior) when the data supports them.

### Phase 3 — Intervention design

For each top trigger, two moves:
1. **Cue disruption** — make the cue harder to reach (phone charger out of
   bedroom; no snacks at home → the 22:47 raid requires a walk to the store).
2. **If-then reengineering** — keep the cue + reward, swap the routine
   ("IF urge after coffee > 3, THEN 10 squats + gum"). Implementation
   intentions with a concrete cue roughly double follow-through in the
   meta-analyses (Gollwitzer & Sheeran 2006: d≈.65).

## Files

| File | Purpose |
|---|---|
| `scripts/trigger_log.py` | Interactive 30-second journal entries → JSONL |
| `scripts/trigger_analysis.py` | Lift analysis, hotspots, chains, habit loop, if-then plans |
| `references/journal-template.md` | Paper template + emotion/urge anchors |
| `references/behavior-science.md` | Habit loop, implementation intentions, reward inference, references |

## Usage

```bash
# Log an occurrence (interactive prompts, 30 seconds)
python3 scripts/trigger_log.py log

# Log a baseline (non-event) moment
python3 scripts/trigger_log.py baseline

# Analyze after 5+ days (needs >= 8 events + 5 baselines)
python3 scripts/trigger_analysis.py journal.jsonl

# Include a specific if-then replacement behavior
python3 scripts/trigger_analysis.py journal.jsonl --replacement "10 squats"
```

## Workflow

1. Define ONE behavior with the user. One at a time.
2. Have them journal 5-7 days (events + baselines). Nudge daily if you're
   the agent; accept imperfect entries — the analyzer tolerates free text.
3. Run the analysis. Walk through RANKED TRIGGERS with the user — recognition
   ("yes! it's always after the work call") is the moment the skill pays off.
4. Pick the top 1-2 triggers ONLY. Design cue disruption + if-then plan.
5. Week 2: journal again; compare lift tables — did the cue decouple?

## Common Pitfalls

1. **No baseline entries** → every percentage is noise. The analyzer refuses
   to rank triggers below 5 baselines.
2. **Journaling multiple behaviors at once** muddies statistics. One behavior
   per journal file.
3. **Judging the entries.** The journal is a sensor, not a confessional. If
   the user starts sanitizing ("I'll skip logging the embarrassing ones"),
   the analysis dies. State this explicitly on day 1.
4. **Sample size overconfidence.** 3 events at location=X with lift 4.0 is
   a hypothesis, not a trigger. The script marks these LOW-CONFIDENCE —
   don't build plans on them.
5. **Attacking the routine, not the cue.** "Just resist harder" fails;
   cue removal succeeds structurally. Prefer environmental changes over
   willpower prescriptions.
6. **Week-2 verification skipped.** Triggers drift; re-run the analysis
   after any intervention and compare.

## Example Session

> 6 days of vaping urges, 11 events, 7 baselines. Analysis output:
> `LIFT 3.1 — location=commute (6/11 events, 0/7 baselines)` +
> `LIFT 2.4 — prev_action="coffee"` + hotspot 08:00-09:00.
> Habit loop: morning commute coffee → vape (nicotine + break from podcast)
> → alertness ritual. Reengineered: IF coffee on commute, THEN nicotine gum
> + podcast continues; car vape pack removed (cue disruption).
> Week 2 re-analysis: commute lift 3.1 → 1.2. Decoupled.

## Verification Checklist

- [ ] Journal has events AND baselines (≥5) before analysis
- [ ] Top triggers have lift ≥ 1.5 and ≥3 supporting events
- [ ] Each recommended if-then plan names the SPECIFIC cue (time/place/state)
- [ ] Cue-disruption option given alongside willpower option
- [ ] Week-2 re-analysis planned to verify decoupling
