---
name: midi-pianoroll-render
description: Use when a MIDI file needs rendering as a piano roll image.
version: 1.0.0
author: open source contribution
license: MIT
metadata:
  hermes:
    tags: [music, midi, piano-roll, visualization, sheet-music-alternative]
---

# MIDI Piano Roll Renderer

## When to Use

- A MIDI file must be turned into a **piano-roll picture** for reading, teaching, or sharing.
- The user wants to **see a song's structure**: melody vs. accompaniment, chord progression, key, tempo.
- Choosing between a **vertical** falling-notes layout (default — easiest to play along, time flows down, inspired by Synthesia) and a **horizontal** DAW-style roll (option for wide screens / long phrases).

Turns any MIDI file into a polished piano-roll PNG: colored note blocks with note letters inside, a large chord track, automatic key + tempo detection, and a chromatic color legend. Two orientations are supported: **vertical** (time ↓ down, Synthesia-style falling notes — default) and **horizontal** (time → right, classic DAW style).

## Requirements

- Python 3.8+ with `mido` and `Pillow` (`pip install mido pillow`)
- A bold monospace TTF for labels — the scripts use `consolab.ttf` (Windows Consolas Bold) and silently fall back to PIL's default font elsewhere

## Usage

```bash
# vertical roll (time ↓ down, portrait) — DEFAULT, best for playing along
python scripts/render_vertical.py song.mid song_vertical.png

# horizontal roll (time → right, DAW-style) — option for wide screens / long phrases
python scripts/render_any.py song.mid song_roll.png
```

Common options (both scripts):

| Flag | Meaning |
|------|---------|
| `--bars N` | Render exactly N bars (skips auto-detection) |
| `--start N` | Start from bar N (skip an empty intro) |
| `--mel T` | Force melody track index |
| `--acc T` | Force accompaniment/bass track index |

Example:

```bash
# Skip a sparse 10-bar intro, start at the main groove, force track roles
python scripts/render_any.py mario.mid mario_roll.png --mel 1 --acc 6 --start 10
```

## What it does automatically

- **Track picking** — melody = the note-rich track with the highest average pitch; accompaniment = the note-richest remaining track. Override with `--mel` / `--acc` when a MIDI has odd instrumentation (e.g., a percussion track with a higher average pitch).
- **Key detection** — correlates the duration-weighted pitch-class profile against major/minor templates, then annotates the key signature accidental count, e.g. `Key: Gm (bb)`, `Key: C# (#######)`.
- **Chord labels** — per-bar weighted pitch-class template matching (triads, 7ths, maj7, sus2/sus4). Consecutive identical chords are merged into one label. Labels are anchored at the chord's entry beat, not centered over the merged span.
- **Bar count (vertical script)** — measures the shortest note in the window and guarantees it at least ~30 px tall by stretching the canvas; never renders fewer than 4 bars. With an explicit `--bars`, the canvas keeps a 4:3-derived height instead.
- **Note letters** — every melody note gets its name (C, D#, …) inside the block; very short notes get an auto-shrunk font so the letter always fits.
- **Adaptive legend** — the 13-swatch chromatic legend and the metadata line auto-shrink to fit narrow canvases.

## Rendering conventions (dark theme)

- One bright palette color per pitch class (12 colors), accompaniment in muted steel blue.
- Black-key lanes darker than white-key lanes; thin dark lines separate every semitone row; bold white lines mark octaves (labeled C2…C7) and bar lines.
- Legend strip is always drawn below the grid, never overlapping it.
- Chord labels in bold yellow, large (110–150 px): top banner (horizontal) or left column (vertical).

## Known limitations

- The chord/key heuristics are simple template matches: fast runs and chromatic passing tones can produce wrong labels (e.g., `Emaj7` for a plain C major passage) and enharmonic oddities (`A#m` with 7 sharps instead of the conventional `Bbm`). Labels are advisory — hand-correct for publication.
- Percussion tracks can win the melody pick on sparse files; check the printed `melody=<idx>` line and override if needed.
- MIDI files with very long silent intros render nearly empty — use `--start` to jump into the music.

## Files

- `scripts/render_vertical.py` — vertical renderer (default; falling-notes style, best for playing)
- `scripts/render_any.py` — horizontal renderer (DAW-style alternative)

Both are standalone (stdlib + mido + Pillow) and safe to copy into any project.

## Example images

- `assets/tetris_vertical.png` — vertical: Tetris (Korobeiniki) theme, 4 bars, A minor 80 BPM
- `assets/september_horizontal.png` — horizontal: Wake Me Up When September Ends, 8 bars, G major 104 BPM