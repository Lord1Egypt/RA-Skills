---
name: music-analysis
description: "Analyze music/audio files locally without external APIs. Extract tempo, pocket/groove feel, pulse stability, swing proxy, section/repetition structure, key clarity, harmonic tension, timbre descriptors, temporal mood-energy journeys, and lyric-aware emotional reads where real Whisper lyrics can override the vibe when the words are clearly darker, warmer, or more intense than the arrangement alone suggests. Use when asked to 'listen to this', 'hear the music', audit tracks, compare mixes, inspect structure, or generate producer-facing notes from audio files."
---

# Music Analysis (Local, No External APIs)

Primary tool: a **full listen** that combines snapshot analysis, structure, groove, harmonic tension, temporal mood mapping, and optional Whisper lyric alignment into one report.

## 1. Full Listen — primary / recommended

```bash
python3 skills/music-analysis/scripts/listen.py /path/to/audio.mp3
python3 skills/music-analysis/scripts/listen.py track.mp3 --json
python3 skills/music-analysis/scripts/listen.py track.mp3 --out report.txt
python3 skills/music-analysis/scripts/listen.py track.mp3 --json --out report.json
```

**What it does in one pass:**
1. Snapshot analysis: tempo, pulse stability, swing proxy, key clarity, harmonic tension, timbre, structure
2. Whisper lyric transcription and filtering first — keep only real lyric text, drop artifact tags like `[MUSIC]`
3. Temporal listen: windowed energy / mood / tension journey
4. Synthesis layer that aligns lyrics with peak / tension / quiet windows and lets the lyric layer override the final vibe when confidence is high

### Human-readable output structure

- **SNAPSHOT**
  - groove/pocket
  - structure summary + repeated sections
  - harmony (key clarity + tension)
  - timbre descriptor tags
- **INSTRUMENT READ**
  - likely instrument palette (strong/likely/possible confidence)
  - per-section instrument entrances and exits
  - how instruments color the emotional feel
  - written as natural language, not clinical data
- **TEMPORAL JOURNEY**
  - opening / middle / closing mood-energy-tension read
  - peak / quietest / tensest moments
  - mood journey and transition count
- **EMOTIONAL READ**
  - explainable emotion summary based on measured features
- **LYRICS**
  - Whisper segment count
  - excerpt or graceful skip note
- **SYNTHESIS**
  - lyric-energy/tension alignment
  - peak / tension / quiet lyric moments
- **ALIGNED TIMELINE**
  - per-window moments where transitions / lyrics / tension spikes occur

## 2. Snapshot Analysis — standalone

```bash
python3 skills/music-analysis/scripts/analyze_music.py /path/to/audio.mp3
python3 skills/music-analysis/scripts/analyze_music.py track.mp3 --json
```

Reports:
- tempo / pulse stability / pulse confidence / swing proxy / pocket
- key estimate / key clarity / chroma entropy / harmonic change / tonal motion / tension
- timbre descriptors (brightness, richness, low-end, contrast, dynamic range)
- section labels (A/B/C...) and repeated material detection
- explainable emotional read with reasons

## 3. Temporal Listen — standalone

```bash
python3 skills/music-analysis/scripts/temporal_listen.py /path/to/audio.mp3
python3 skills/music-analysis/scripts/temporal_listen.py track.mp3 --json
```

Reports:
- sliding-window timeline (4s windows, 2s hops)
- energy contour
- mood labels
- harmonic tension + tonal motion
- transition types (drop hits, pulls back, tightens harmonically, shifts color, evolves)
- narrative arc (mountain / ascending / descending / plateau / wave)

## Interpretation rules

- **Structure labels are similarity labels**, not verse/chorus claims.
- **Swing proxy is a feel estimate**, not drummer-grade microtiming truth.
- **Emotion is explainable**, derived from pulse + timbre + harmonic tension rather than a black-box mood guess.
- **Lyrics can override the final vibe** when filtered Whisper text is confident and emotionally clear.

## Audio sourcing

The tool needs a real audio file on disk.
- Direct file (mp3, wav, flac, ogg, m4a — anything ffmpeg/librosa can read)
- YouTube / supported URLs: `yt-dlp -x --audio-format mp3 -o "output.mp3" "URL_OR_SEARCH"`

## Whisper lyrics transcription

`listen.py` uses:
- CLI: `/opt/homebrew/bin/whisper-cli`
- Model: `~/.local/share/whisper-cpp/ggml-large-v3-turbo.bin`
- Preprocess: convert input to mono 16kHz WAV via ffmpeg
- Fallback: skip gracefully if Whisper is missing or errors

## Dependencies

Python:
- librosa
- numpy

System:
- ffmpeg
- ffprobe

## Workspace hygiene

- Keep temporary audio files in a dedicated temp/output folder for the skill.
- Avoid modifying unrelated project files while working on audio analysis tasks.
