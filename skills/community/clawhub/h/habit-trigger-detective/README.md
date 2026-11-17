# Habit Trigger Detective

**"I know what I should do. I just don't do it." — the problem was never
motivation. It's unidentified triggers.**

## The problem

The cigarette happens after coffee. The doomscroll starts when the phone is
on the nightstand. The snack raids hit at 22:47. The skipped workouts
cluster on early-meeting days. People try to change the BEHAVIOR while
leaving the CUE ARCHITECTURE intact — then blame their willpower when the
loop fires again.

Habit research (Wood, Gollwitzer, Lally) is clear: habits run on
cue → routine → reward, executed with near-zero deliberation. Willpower is
the wrong lever. Identified cues and concrete if-then plans are the right
one — implementation intentions roughly double follow-through (meta-analytic
d ≈ 0.65 across 94 studies).

But nobody can name their real triggers from memory. Memory collapses
everything into "it just happens." You need data.

## The solution

**Week 1 — Journal (30 seconds per entry).** Log each occurrence: time,
location, company, device, mood 1-5, urge 1-5, what you were doing in the
previous 30 minutes. Critically: also log ~5+ *baseline* moments with no
urge — without them, "80% of events happen at home" is meaningless if you're
home 80% of the time.

**Analyze.** `trigger_analysis.py` computes **lift** for every factor —
how much more likely the behavior is when the factor is present — plus
time-of-day hotspots, preceding-action chains, a confound detector, and an
inferred habit loop with reward hypothesis.

**Intervene.** The output gives cue-disruption moves (environmental design)
and reengineered if-then plans built on your *measured* top cues, not your
guessed ones.

**Week 2 — Verify.** Journal again, re-run, compare lift tables. Target:
top cue lift collapses toward 1.0 = decoupled.

## Quick start

```bash
# log an occurrence (interactive, 30s)
python3 scripts/trigger_log.py event

# log a no-urge baseline moment
python3 scripts/trigger_log.py baseline

# after 5-7 days (needs >=8 events + >=5 baselines)
python3 scripts/trigger_analysis.py ~/trigger_journal.jsonl

# with your chosen substitute routine
python3 scripts/trigger_analysis.py ~/trigger_journal.jsonl \
    --replacement "open the e-reader instead"
```

## What you get

```
--- DEVICE ---
  lift >99   phone        events 11  baselines 4
--- TIME OF DAY ---
  lift 2.60  night (23-06)  events 6  baselines 0
--- PRECEDING ACTION ---
  36% in bed / 36% bored / 18% wait
HABIT LOOP: CUE alone+phone+home → ROUTINE scroll → REWARD mood repair
IF-THEN: IF urge hits with phone in hand (lift >99), THEN open the e-reader
Cue disruption: physical distance from the device in that window
```

Statistical honesty is enforced: minimum event/baseline counts before
ranking, LOW-CONFIDENCE flags on thin cells, confound detection when two
factors always co-occur.

## Who needs this

- Anyone who has failed the same New Year's resolution 3+ times
- People quitting vaping/snacking/doomscrolling who keep "mysteriously"
  relapsing
- People BUILDING habits (exercise, writing, language practice) who can't
  find a stable slot — the hotspot table doubles as the anchor-routine list
- Coaches and therapists as a structured homework tool (self-tracking,
  not treatment — see scope note in references)

## Files

- `SKILL.md` — full method, workflow, pitfalls
- `scripts/trigger_log.py` — interactive journal
- `scripts/trigger_analysis.py` — lift analysis + habit loop + if-then plans
- `references/journal-template.md` — paper journal template
- `references/behavior-science.md` — the research, statistical rules,
  reward inference, sources

## Scope

For ordinary habits: screens, snacks, exercise, practice, spending. NOT a
treatment for substance dependence, eating disorders, or compulsive
behavior — those need professional support.

## License

MIT © Denis Voronin
