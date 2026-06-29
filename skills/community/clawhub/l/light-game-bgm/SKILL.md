---
name: light-game-bgm
description: >-
  Compose light, melodic, loopable background music in the spirit of classic
  cozy game town, village, and overworld themes (the calm 2D RPG / retro
  online-game vibe) and render it to a real playable audio file using sampled
  instruments. Use this whenever the user wants to create original music, a
  game soundtrack, BGM, a chiptune or town/overworld theme, a calm instrumental
  loop, or asks you to "make a song", "write some music", or produce a seamless
  looping audio track — even if they don't say the word "skill". Also use it
  when an existing track sounds too synthetic or stiff (the "stock
  General-MIDI" sound) and the user wants more realistic instruments,
  expressive strings, concert-hall space, or a clean loop. Covers the full
  pipeline: waveform synthesis OR (preferred) MIDI + soundfont rendering,
  expressive performance, convolution reverb, and seamless looping.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - fluidsynth
        - ffmpeg
    install:
      # note: brew formula is `fluid-synth` but the binary is `fluidsynth`
      - kind: brew
        formula: fluid-synth
        bins: [fluidsynth]
      - kind: brew
        formula: ffmpeg
        bins: [ffmpeg]
      # python libraries (no CLI binary of their own)
      - kind: uv
        package: mido
      - kind: uv
        package: numpy
      - kind: uv
        package: scipy
    os: [macos, linux]
    emoji: "🎵"
---

<!-- Triggering is decided entirely by the `description` field above (ClawHub
     and Anthropic both work this way); there is deliberately no separate
     "trigger" section in the body. Python deps: numpy, scipy, mido. -->

# Light game BGM composer

Produce original, nostalgic, loopable instrumental music and render it to an
actual audio file the user can play. This skill captures a pipeline that was
tuned on a real cozy 2D-game town theme, including the mistakes that taught
each lesson.

## The core insight

Two things, in order, decide whether the music sounds real:

1. **Use sampled instruments, not hand-built oscillators.** From-scratch
   synthesis can only ever sound like a synth. Write the piece as **MIDI** and
   render it through **FluidSynth + a soundfont** so every note plays a recorded
   instrument sample.
2. **Perform the MIDI; don't just place notes.** A correct-but-static MIDI
   played through a great soundfont still sounds like the stiff, stock
   General-MIDI cliché. The realism comes from *how the notes are played* —
   dynamics, timing, articulation. This is the part people underestimate.

There is a hard ceiling: truly recorded-section realism needs dedicated VST
libraries in a DAW, which the CLI can't load. Be upfront about this and offer
the MIDI export as the bridge. See `references/soundfonts.md` (realism ladder).

## Environment check

```bash
python3 -c "import numpy, scipy" && echo ok      # synthesis + reverb math
python3 -c "import mido" || pip install mido       # MIDI authoring
which fluidsynth || brew install fluid-synth       # soundfont renderer
which ffmpeg                                        # wav -> mp3
```

Then fetch a soundfont (see `references/soundfonts.md`). **Default to
GeneralUser GS** for light/cozy pieces — it's pre-balanced and blends; the
bigger FluidR3_GM is brighter and more forward (good for leads, can over-expose
strings). Bigger is not better.

## Workflow

### 1. Decide the musical brief
Key (major = bright/cozy), tempo (~100–120 BPM for town themes), instrument
roster, and form. A satisfying loop form is **A → A′ (variation) → B (contrast)
→ A″ (return)**, ~32 bars ≈ 70 s at 110 BPM.

### 2. Write the composition as a per-song Python script
Import `scripts/midi_helpers.py` and build one `NoteBuilder` per voice. Keep the
note data (melody, chords, counter-lines) in the song script — it changes every
time — and lean on the helpers for the reusable expression machinery. See the
**template** below.

### 3. Apply the expression layer (this is what kills the fake feeling)
- **Humanize timing** — nudge note starts a few ticks (`hum=`). Perfectly
  quantized = robotic.
- **Velocity variation** (`vvar=`) — no two notes identical.
- **CC11 swells** (`.swell(...)`) — phrases breathe louder/softer. The single
  biggest fix for stiff string pads.
- **Legato / held common tones** (`held_runs(...)`) — sustain a chord tone
  across bar lines instead of re-attacking it every bar. Block chords that
  re-hit every downbeat are *the* stock-library giveaway.
- **Slow-attack patch for pads** (Slow Strings, prog 49) — mimics bowing in.
- **A little vibrato** (`vib=`, CC1) on strings.
- **Pan voices** (CC10) — e.g. cello left, violin right, so a two-part string
  **dialogue** (call-and-response) reads spatially. Giving strings their own
  conversing lines beats parking them on block-chord pads.

### 4. Render dry
```bash
fluidsynth -ni -R 0 -C 0 -g 0.8 -r 44100 -F song_dry.wav GeneralUser.sf2 song.mid
```
Reverb/chorus OFF — the next step owns the space.

### 5. Concert-hall reverb + seamless loop
```bash
python3 scripts/hall_reverb_loop.py --input song_dry.wav --output song_loop.wav \
    --bpm 110 --beats 128 --decay 2.1 --x2
```
`--beats` = bars × beats/bar (the loop body length). The script convolves a
synthesised hall impulse response and, for a loop, **wraps the post-loop tail
(note releases + reverb) back onto the start** so it repeats with no click and
no fade. `--decay` sets room size (1.2 room · 2.1 hall · 3.5 cathedral).
`--x2` writes a two-loop file to audition the seam.

### 6. Verify, then encode
```bash
python3 scripts/verify_loop.py --input song_loop_x2.wav --bpm 110 --beats 128
ffmpeg -y -i song_loop.wav -af "loudnorm=I=-15:TP=-1.5" -b:a 192k song_loop.mp3
```
Don't ship a loop you haven't verified — `verify_loop.py` confirms the seam jump
is inaudible (jump/rms well under 0.06) and nothing clips.

### 7. Deliver
Give the user the **mp3** (plays everywhere), and offer the **.mid** (for a DAW)
and the per-song **.py** (to tweak the composition). Present concrete next-step
options (longer bridge, wider panning, bigger/smaller hall, different lead
instrument) rather than asking open-ended questions.

## Per-song script template

```python
import sys; sys.path.insert(0, 'scripts')
from midi_helpers import NoteBuilder, new_midi, held_runs, realize, midi

BPM, TPB = 110, 480
mid = new_midi(BPM, TPB)

# --- melody (music box, centered) ---
lead = NoteBuilder(0, 10, TPB, pan=64, rev=55, vol=104, seed=1)
lead.line([(0,'A4',1),(1,'F#4',1),(2,'D4',1.5),(3.5,'E4',.5)], vel=90, gate=0.9, hum=8)
# ... more phrases ...

# --- strings as a dialogue: cello left, violin right ---
cello  = NoteBuilder(4, 42, TPB, pan=36, vib=30, rev=68, vol=92, seed=2)
violin = NoteBuilder(1, 40, TPB, pan=92, vib=38, rev=70, vol=84, seed=3)
cello.line([(64,'G3',1),(65,'A3',1),(66,'B3',2)], vel=66, gate=0.97)   # call
violin.line([(72,'B4',1),(73,'C#5',1),(74,'D5',2)], vel=62, gate=0.96) # answer
cello.swell(128, base=76, amp=28); violin.swell(128, base=72, amp=30)

# --- soft pad via held common tones (legato, no re-attacks) ---
voicing = [['D3','F#3','A3'], ['C#3','E3','A3'], ...]   # one per bar
pad = NoteBuilder(5, 49, TPB, pan=64, vib=18, rev=90, vol=50, seed=4)
for start, pitch, dur in held_runs(voicing):
    pad.note(start, pitch, dur, vel=30, gate=0.99, hum=20)
pad.swell(128, base=55, amp=22)

for nb in (lead, violin, cello, pad):
    mid.tracks.append(nb.track())
mid.save('song.mid')
```

(A complete, working realisation of this exact arrangement — a full
cello/violin-dialogue town theme with the four-section loop form — was built in
the parent project; look for the per-song MIDI builder and post-processing
script there as a reference implementation if present.)

## Bundled resources
- `scripts/midi_helpers.py` — `NoteBuilder` (humanize, velocity, CC11 swells,
  panning), `held_runs` (legato pads), `realize` (arps), `midi`/`new_midi`.
- `scripts/hall_reverb_loop.py` — convolution hall reverb + seamless-loop wrap.
- `scripts/verify_loop.py` — objective seam/clipping check.
- `references/soundfonts.md` — realism ladder, GeneralUser GS vs FluidR3,
  download + validation, GM program numbers, CC reference.

## Fallback: pure synthesis (no soundfont)
If FluidSynth/soundfonts are unavailable, you can still synthesise from
oscillators with numpy (sine/triangle + ADSR + simple reverb) and write a WAV
directly. Accept that it will sound chiptune/synthetic — set that expectation
with the user rather than presenting it as realistic.
