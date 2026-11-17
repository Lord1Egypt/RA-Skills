# Paper Trigger Journal Template

Print or copy this. One behavior per journal. 30 seconds per entry.
The journal is a SENSOR, not a confessional — honest beats flattering.

## Event entry (when the behavior / urge HAPPENS)

```
Date/time : ____-__-__ __:__
Location  : home / work / commute / other: ______
Company   : alone / partner / friends / colleagues
Device    : none / phone / laptop / tv
Mood      : 1 😞 — 2 😕 — 3 😐 — 4 🙂 — 5 😄  → __
Urge      : 1 barely — 3 noticeable — 5 overwhelming → __
Last 30 min I was: ___________________________
```

## Baseline entry (random moment, NO urge — 2/day minimum)

Set 2 random phone alarms. When one fires and there is NO urge:

```
Date/time : ____-__-__ __:__
Location  : ______________
Company   : ______________
Device    : ______________
Mood      : __
Last 30 min I was: ___________________________
```

## Rules

1. Log EVERY occurrence you notice — including "small" ones.
2. Never judge entries. Sanitized data = useless analysis.
3. If you miss logging an event, log it later from memory and mark it "late".
4. Baselines are as important as events. Don't skip them.
5. 5-7 days is enough; 8+ events and 5+ baselines minimum for analysis.

## After the week

Run `trigger_analysis.py journal.jsonl` (or transcribe entries to JSONL):
each line `{"ts":"2026-09-14T22:47:00","behavior":"doomscroll","location":
"home","company":"alone","device":"phone","emotional_state":2,"urge":4,
"prev_action":"in bed","type":"event"}` — baselines use `"type":"baseline"`
and omit "behavior".
