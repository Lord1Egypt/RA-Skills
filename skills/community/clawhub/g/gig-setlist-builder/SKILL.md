---
name: gig-setlist-builder
description: Builds live setlists that actually work on stage — energy arc (open strong, mid-set valley, closer peak), key compatibility via circle-of-fifths distance, BPM jump caps so dancers don't stumble, timed to your slot with breaks. Input your song book (key/BPM/energy/minutes), get a printable set order with running clock, transition report, and an ASCII energy curve. For bar bands, wedding/corporate acts, and DJs.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [music, live-gig, setlist, band, dj, performance]
---

# Gig Setlist Builder

A great set is engineering, not a shuffled playlist: open strong in the
first 90 seconds, keep adjacent songs key- and BPM-compatible so transitions
don't clear the floor, give the room a breather mid-set, and end on your
biggest gun. This skill does that arithmetic on YOUR song book.

## When to trigger
- "help me build the setlist for Saturday's gig (2×45 minute sets)"
- "we have 40 songs, what order should we play?"
- "our sets always die in the middle — fix the flow"
- "DJ set, 90 minutes, house/techno, need BPM-laddered order"
- preparing any live performance: bar gig, wedding, corporate, open mic

## How it works

1. **Song book JSON** (see `sample_songbook.json`): each song with title,
   key (e.g. `E`, `Am`, `F#m`), BPM, energy 1–10, minutes, optional
   `must_play` and `tags`.
2. **Run** `scripts/setlist_builder.py sample_songbook.json --minutes 45
   --sets 2 --break-min 15`.
3. **Energy arc template**: slots get target energies interpolated from a
   live-proven shape — open 7–8, first peak by slot 3, controlled valley
   4–5 around the middle, rebuild to a 9–10 closer. Per set.
4. **Transition scoring** picks the best unused song per slot:
   - **BPM jump penalty**: >±12 % between adjacent songs is punished
     (dancers stumble; vinyl-era DJs call it the death jump);
   - **Key distance**: circle-of-fifths steps between adjacent keys
     (relative minor counts as distance 0 — the classic smooth move);
   - **energy deviation** from the arc target.
   `must_play` songs are guaranteed a slot (error if they don't fit).
5. **Output**: ordered setlist with running clock (song start times,
   breaks inserted), per-transition report (`Am→C: smooth (relative)`,
   `132→96 BPM: -27% HARD - swap or MC over it`), ASCII energy curve, total
   runtime check against your slot.

## Pitfalls encoded
- **Never open with your biggest song** — you peak at minute 3 and spend
  the set declining; the arc saves the 10 for last.
- **The mid-set valley is deliberate**: 45 minutes at energy 9 exhausts a
  room; the breather makes the last third hit harder.
- **Two slow songs in a row** kills bars; adjacent-energy smoothing
  prevents stacked valleys beyond one slot.
- **BPM cliff both ways** — jumping 132→96 reads as an error to a dance
  floor; walk it down over 2–3 songs instead.
- **Encores need ammo**: if `--encore` is set, the top-energy unused song
  is reserved, not burned as the closer.

## Examples

```bash
# Two 45-minute sets, 15-min break
python3 scripts/setlist_builder.py sample_songbook.json --minutes 45 --sets 2 --break-min 15

# One 90-minute DJ-style set, encore reserved
python3 scripts/setlist_builder.py dj_songs.json --minutes 90 --sets 1 --encore

# Must-plays only (wedding couple's songs)
python3 scripts/setlist_builder.py sample_songbook.json --minutes 40 \
  --sets 1 --only-must
```

## Output contract
- per-set ordered songs with start clock and cumulative minutes
- transition report (key move, BPM delta, verdict)
- ASCII energy curve per set
- runtime vs slot verdict (FITS / OVER by N min — cut suggestions ranked
  by lowest energy contribution)
