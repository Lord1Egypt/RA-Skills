# Gig Setlist Builder — Reference

## 1. Why sets die
Every experienced booker knows the shape of a bad night: strong-ish start,
energy plateau, crowd thins at minute 25, band plays its best song to a
half-empty room. The causes are structural, not talent:

- **Peaks in the wrong place** (best song first, filler closer);
- **Transition cliffs** — key collisions and BPM jumps >12 % between
  adjacent songs break dance momentum;
- **No valley** — a 45-minute all-high-energy set exhausts the room, and
  the last third lands flat;
- **Runtime drift** — sets that run 4 minutes long get their power cut by
  venue curfew.

## 2. The energy arc
Live-proven template per set (energy 1–10):

```
slot%:   0    15   30   45   60   75   90   100
target:  7.5  8.5  7.0  4.5  5.5  8.0  9.5  10
         ^open      ^first peak   ^valley   ^rebuild ^closer
```

Interpolated per slot position. The algorithm minimizes total
`|song_energy − arc_target|` greedily slot by slot, subject to transition
penalties.

## 3. Transition penalties
- **BPM**: `penalty = max(0, |Δbpm|/bpm_prev − 0.12) × 40`. Under 12 % is
  a natural-feeling change; above it, a stumble. (DJs ladder BPM in 2–4 %
  steps.)
- **Key**: circle-of-fifths distance between adjacent songs. Pitch-class
  distance matrix: E→A = 1 step, E→F = 5 steps (tritone-ish clash for
  root-movement ears). **Relative minor/major counts as 0** — Am→C feels
  like the same room. Penalty = `distance × 1.5`, distance 0–6.
- **Valley stacking**: adjacent slots both ≤ energy 4 adds a penalty
  (one breather is pacing, two is a nap).

## 4. Selection algorithm
For each set: compute slots = songs fitting `--minutes` (average 4.2 min
if songs lack duration). For slot i, choose the unused song minimizing:

    2.0×|energy − arc(i)| + bpm_penalty(prev→song) + key_penalty(prev→song)

`must_play` songs are pre-seeded into their best arc slots before greedy
fill. Encore mode: best unused energy-10 song is held back.

Greedy (not global optimum) is a feature here: sets are built left to
right exactly like a bandleader does, and the transition report exposes
every weak seam the greedy choice made so a human can swap.

## 5. Reading the report
```
  3  Am      -> C       dist 0  (relative - smooth)
  4  128 BPM -> 148 BPM +15.6% HARD (walk it or MC over)
```
- `smooth` — nothing to do.
- `ok` — audible but normal.
- `HARD` — flagged swap candidates: the tool lists unused songs that would
  bridge both key and BPM.

## 6. Runtime management
Total set minutes vs `--minutes`: if over, cut suggestions are ranked by
lowest `energy contribution` (energy × singalong-ness proxy), never cutting
`must_play`. Breaks are inserted between sets with the clock printed.

## 7. Song book format
```json
{"songs": [
  {"title": "Pride of Elm St", "key": "E",  "bpm": 132, "energy": 8,
   "minutes": 4.1, "must_play": true},
  {"title": "Slow Burn",       "key": "Am", "bpm": 76,  "energy": 3,
   "minutes": 5.0, "tags": ["ballad"]}
]}
```
Keys use letter + optional `#`/`b` + optional `m` for minor.
`minutes` optional (default 4.2).
