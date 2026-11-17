# Jet Lag Protocol Planner

**You land in Tokyo at 9 AM after an 10-hour flight. Your body thinks it's 2 AM.
You drink coffee, get blasted by morning sun on the way to the hotel — and
just made your jet lag WORSE.** Light at the wrong biological moment pushes
your circadian clock in the *wrong direction*. Jet lag isn't fatigue to be
power-through; it's a phase-alignment problem with a known solution:
correctly-timed light, correctly-timed low-dose melatonin, and graduated
sleep shifting.

This tool computes your personal, day-by-day protocol:

```
python3 scripts/jetlag.py --home-tz 3 --dest-tz 9 --wake-home 07:00 --pre-days 3
```

Output (excerpt, Moscow → Tokyo):

```
=== Jet-lag protocol: advance (eastward), 6 h total ===
Day -3   home   wake 06:00  SEEK light 02:00–06:00 ...
Flight day  dest  CBTmin 00:30  SEEK 20:30–00:30  AVOID 00:30–04:30 ...
Dest day 1 ...
--- In-flight rules --- / --- First days at destination ---
```

## The real-world problem
- ~500M long-haul passengers/year; multi-day productivity and vacation loss
  is the norm, and almost everyone improvises wrong (bright light on arrival
  morning after eastward flight = phase delay = the exact opposite of help).
- Generic advice ("get sunlight!") is direction-blind. This tool computes
  direction (including the >12 h wrap: LA→Tokyo is a *westward* −7 h plan,
  not +17 h), your CBTmin position each day, and the SEEK/AVOID windows that
  move with it.
- Pre-trip shifting math: how many hours you can realistically pre-pay
  (≤1 h/day, capped 2–3 h) so landing misalignment is smaller.

## What's inside
- `SKILL.md` — trigger conditions, protocol steps, pitfalls (melatonin-timed-
  wrong, napping into the afternoon, ignoring the wrap)
- `references/circadian-science.md` — CBTmin model, light & melatonin
  phase-response curves, alignment-rate limits, in-flight doctrine
- `scripts/jetlag.py` — pure-stdlib planner; `--json` mode; tested east/west,
  wrap-around, sub-1h, and pre-trip cases

Safety: timing arithmetic on established circadian science; not medical
advice. Melatonin 0.3–1 mg is a timing tool, not a sleeping pill; consult a
clinician for children, pregnancy, or interacting medications.

MIT © Denis Voronin
