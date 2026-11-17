# Gym Load Planner

**Stop guessing your weights.** Estimate your true 1RM from any hard set,
get exact loading tables for your goal (strength / hypertrophy /
endurance), follow a progression plan with automatic deloads, solve plate
math instantly, and track whether you're actually getting stronger.

## The problem

Walk into any gym and ask ten people why they're lifting the weight
they chose. You'll hear "feels right", "what I always do", "the app said".
Meanwhile the entire science of getting stronger reduces to: **apply a
load you can barely complete for the target reps, recover, then apply
slightly more**. The arithmetic is trivial but nobody does it — they add
weight randomly, stall, and quit. Others fail to deload, accumulate
fatigue, and stall that way.

## What it does

- `one-rm` — Epley + Brzycki consensus e1RM from any set of ≤ 12 reps,
  with rep-max predictions.
- `table` — %-1RM loading table per goal with reps/sets/rest.
- `plan` — N-week block: linear or double progression, deload every 4th
  week at −10 %.
- `plates` — exact per-side plate stack for any target weight; nearest
  loadable when the target is off-grid.
- `log add/show/next` — record sets, watch e1RM trend, get the next
  session's load according to your progression rule.

## Quick start

```bash
python3 scripts/gym_load.py one-rm --weight 100 --reps 8
python3 scripts/gym_load.py table --one-rm 125 --goal strength
python3 scripts/gym_load.py plan --one-rm 125 --goal strength --weeks 8
python3 scripts/gym_load.py plates --target 92.5 --bar 20
python3 scripts/gym_load.py log add --lift "bench press" --weight 80 --reps 8
python3 scripts/gym_load.py log next --lift "bench press" --rule double
```

Stdlib-only Python 3. Log is a local JSON file — no cloud, no accounts.

## Who needs this

Over 300 million people worldwide participate in strength training
(IHRSA/Health & Fitness Association estimates). Virtually every one of
them faces the load-selection question multiple times per session, and
the two failure modes — random loading and never deloading — are the top
self-coaching errors. Coaches automate this; everyone else can now too.

## Disclaimer

Educational tool. Use spotters for heavy lifts; form before load. Not
medical advice.

## License

MIT © 2026 Denis Voronin
