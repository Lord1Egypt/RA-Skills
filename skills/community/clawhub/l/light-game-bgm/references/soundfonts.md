# Soundfonts, instruments & rendering reference

## The realism ladder (read this first)

1. **From-scratch oscillator synthesis** (sine/triangle + ADSR) → always sounds
   like a *synth*. Fine for chiptune; a dead end if the user wants "real".
2. **Soundfont + FluidSynth** → real *sampled* instruments. The sweet spot for a
   CLI/offline workflow. This is what this skill uses.
3. **Dedicated VST sample libraries** (e.g. Spitfire BBC SO Discover, free) → true
   recorded-section realism, but they're plugins that need a DAW/host — **not**
   loadable by the FluidSynth CLI. If the user needs this tier, export the MIDI
   and hand it off to Logic/Reaper.
4. **AI music generation** (Suno/Udio) → finished real-sounding audio, but not
   controllable/editable.

Be honest about this ceiling with the user. Within tier 2, *how you write the
MIDI* matters as much as the soundfont (see SKILL.md).

## Choosing a soundfont — bigger is NOT better

| | **GeneralUser GS** (~30 MB) | **FluidR3_GM** (~140 MB) |
|---|---|---|
| Philosophy | Musicality-first: restrained, warm, pre-balanced | Fidelity-first: big raw samples, bright, forward |
| Strings | soft, dark, sit **back** in the mix (great as a bed) | loud, bright, jump **forward** (expose the "sample-library" feel) |
| Best for | gentle/cozy pieces mixed by ear, no DAW | material you'll balance yourself per-track |
| Default | **Start here for light town/RPG BGM** | Use when you want brighter leads/brass |

Lesson learned on this project: for a soft, cozy town theme, GeneralUser GS won
by *blending* better — its understated strings avoided the stiff stock-library
exposure that FluidR3's forward strings reintroduced.

## Getting the soundfonts

```bash
# GeneralUser GS (ships as a zip; extract the .sf2 inside)
curl -sL -o gu.zip "https://www.dropbox.com/s/4x27l49kxcwamp5/GeneralUser_GS_v1.471.sf2?dl=1"
unzip -o gu.zip -d gu && find gu -name '*.sf2' -exec mv {} GeneralUser.sf2 \;

# FluidR3_GM (already a raw .sf2)
curl -sL -o FluidR3.sf2 \
  "https://github.com/fhunleth/midi_synth/releases/download/v0.1.0/FluidR3_GM.sf2"
```

Validate any download is a real soundfont (must start with the RIFF magic) —
download mirrors often hand back an HTML redirect page instead:

```bash
xxd file.sf2 | head -1   # want: 5249 4646 ... ("RIFF")
```

Note: FluidSynth's Homebrew build does **not** load macOS's `gs_instruments.dls`
("Not a SoundFont file"). Stick to `.sf2`.

## Rendering (always dry; reverb comes in post)

```bash
fluidsynth -ni -R 0 -C 0 -g 0.8 -r 44100 -F out_dry.wav GeneralUser.sf2 song.mid
#            │   │    │    │
#            │   │    │    └ gain
#            │   │    └ chorus OFF
#            │   └ reverb OFF  (we do convolution reverb ourselves)
#            └ no shell, no MIDI input
```

## General MIDI program numbers used on this project (0-indexed)

| Voice | Program | Notes |
|---|---|---|
| Music Box | 10 | the signature cozy-town lead/sparkle |
| Celesta | 8 | glassy alternative lead |
| Glockenspiel | 9 | brighter sparkle |
| Orchestral Harp | 46 | warm, believable arpeggios |
| Violin (solo) | 40 | upper voice of a string *dialogue* |
| Cello (solo) | 42 | lower voice of a string *dialogue* |
| String Ensemble 1 | 48 | full pad (forward) |
| Slow Strings | 49 | **slow attack — best pad**, mimics real bowing-in |
| Acoustic Bass | 32 | round, bouncy town-theme bass |
| Acoustic Grand | 0 | believable lead substitute for strings |
| Nylon Guitar | 24 | cozy lead/accompaniment |

Drums live on **channel 9** (GM percussion): 36 kick, 42 closed hat, 70 maracas/shaker.

## Useful CC (control change) numbers

| CC | Name | Use |
|---|---|---|
| 1 | Modulation | adds vibrato depth — wakes up sampled strings |
| 7 | Channel volume | static per-voice level |
| 10 | Pan | 0 L · 64 C · 127 R — split cello L / violin R for dialogue |
| 11 | Expression | **dynamic swells within a phrase** (the "breathing") |
| 91 | Reverb send | keep low if doing reverb in post |
