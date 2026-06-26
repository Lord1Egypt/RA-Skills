---
name: openclaw-video-editor
description: Local ffmpeg-based video editing skill. Provides tested helpers for subtitles, background blur, color grading, two-pass loudness normalization, scene-detected highlight reels, vertical conversion for shorts, and clean audio-only extraction for transcription/podcast workflows. Honest scope: no AI segmentation, no transcription model, no external network calls.
license: MIT
metadata: {"openclaw":{"requires":{"bins":["ffmpeg","ffprobe","python3"]},"primaryEnv":null,"homepage":"https://clawhub.ai/gopendrasharma89-tech/openclaw-video-editor"}}
---

# openclaw-video-editor

v6.1.0

A small, honest video editing skill for OpenClaw built on `ffmpeg`, `ffprobe`, and `python3`. It runs entirely on the local machine. No external services, no AI segmentation, no transcription model.

## Scope

This skill provides:

- `scripts/check_deps.sh` — verify `ffmpeg`, `ffprobe`, `python3` are installed before any workflow runs.
- `scripts/generate_srt.py` — convert Whisper / Deepgram / AssemblyAI / generic word-timing JSON into `.srt`, `.vtt`, or `.ass`.
- `scripts/highlight_reel.py` — detect scene changes via ffmpeg and assemble a short highlight reel.
- `scripts/apply_lut.py` — apply a real `.cube` 3D LUT (`lut3d`), or use a named filter preset (`warm`, `cool`, `bw`, `high-contrast`, `faded`).
- `scripts/loudnorm_two_pass.py` — automate the two-pass `loudnorm` workflow end-to-end.
- `scripts/make_vertical.py` — letterbox, center-crop, or blur-fill a horizontal video into a 9:16 vertical.
- `scripts/extract_audio.py` (NEW in v5.1.0) — extract a clean audio-only track for transcription, podcast editing, or music analysis. Auto-picks codec from output extension (mp3, m4a, aac, wav, flac, opus, ogg). Supports trim, resample, channel forcing, and one-pass loudness normalization.
- `scripts/extract_clip.py` (NEW in v6.1.0) — cut a clip out of a video by start/end timestamps. Fast path uses ffmpeg stream-copy (no re-encode, lossless, faster than real-time, snaps to the nearest keyframe before `--start`). Pass `--accurate` for frame-accurate cuts via re-encode. Accepts plain seconds, `MM:SS`, `MM:SS.mmm`, `HH:MM:SS`, `HH:MM:SS.mmm`.

This skill does not perform:

- AI background removal or subject segmentation
- Voice cloning or generative video
- Transcription (it only formats word timings into subtitle files; pair with a separate STT tool)
- Any remote API calls

## Required binaries

```bash
bash scripts/check_deps.sh
```

Returns non-zero if `ffmpeg`, `ffprobe`, or `python3` is missing.

## Workflows

### 1. Generate subtitles from a transcript

```bash
python3 scripts/generate_srt.py transcript.json subtitles.srt
python3 scripts/generate_srt.py transcript.json subtitles.vtt
python3 scripts/generate_srt.py transcript.json subtitles.ass --font Helvetica --fontsize 28
```

Tunable: `--max-chars`, `--max-words`, `--max-duration` for non-English language tuning.

In v5.1.0, the script now rejects unsupported output extensions explicitly (e.g. `.xml` would silently produce SRT-shaped data with a fake suffix before — now exits 2 with a list of allowed extensions) and surfaces malformed-transcript JSON values (non-numeric `start`/`end`) as a clean one-line error instead of a Python traceback.

### 2. Burn subtitles into a video

```bash
ffmpeg -i input.mp4 \
  -vf "subtitles=subtitles.srt:force_style='Alignment=2,MarginV=30,Outline=2,Shadow=1'" \
  -c:a copy output.mp4
```

`Alignment=2` is bottom-center. Use `Alignment=8` for top-center.

### 3. Background blur (privacy filter, not subject segmentation)

True shallow-depth-of-field requires AI segmentation, which this skill does not include. The filter below is a full-frame blur:

```bash
ffmpeg -i input.mp4 -vf "boxblur=20:1" -c:a copy blurred.mp4
```

If you already have a binary alpha matte (`mask.mp4`, subject white, background black, frame-aligned), you can composite a blurred background behind the original subject:

```bash
ffmpeg -i input.mp4 -i mask.mp4 \
  -filter_complex "[0:v]boxblur=20:1[bg];[0:v][1:v]alphamerge[fg];[bg][fg]overlay=format=auto" \
  -c:a copy composited.mp4
```

Producing the matte itself is out of scope.

### 4. Color grading

Filter presets (no LUT file required):

```bash
python3 scripts/apply_lut.py input.mp4 - graded.mp4 --preset warm
python3 scripts/apply_lut.py input.mp4 - graded.mp4 --preset bw
```

Real `.cube` LUT:

```bash
python3 scripts/apply_lut.py input.mp4 lut.cube graded.mp4 --strength 0.8
```

### 5. Audio normalization (two-pass loudnorm)

```bash
# Broadcast (-23 LUFS, EBU R128)
python3 scripts/loudnorm_two_pass.py input.mp4 normalized.mp4

# Streaming platforms (-14 LUFS)
python3 scripts/loudnorm_two_pass.py input.mp4 normalized.mp4 --target-lufs -14
```

The script runs Pass 1, parses the JSON measurement block from ffmpeg's stderr, and runs Pass 2 with the measured offsets applied. Video is copied without re-encoding.

In v5.1.0, the script now pre-flights the input with `ffprobe` and refuses cleanly when the source has no audio stream, instead of failing inside Pass 1 with an opaque "could not find measurement JSON" error.

### 6. Highlight reel via scene detection

```bash
python3 scripts/highlight_reel.py input.mp4 highlight.mp4 --duration 30 --threshold 0.4
```

### 7. Watermarking

```bash
# Bottom-right text watermark
ffmpeg -i input.mp4 \
  -vf "drawtext=text='@yourhandle':x=w-tw-20:y=h-th-20:fontsize=24:fontcolor=white@0.7:box=1:boxcolor=black@0.4:boxborderw=8" \
  -c:a copy watermarked.mp4

# Image overlay (logo)
ffmpeg -i input.mp4 -i logo.png \
  -filter_complex "[0:v][1:v]overlay=W-w-20:20" \
  -c:a copy watermarked.mp4
```

### 8. Make vertical 9:16 for shorts

`make_vertical.py` offers three modes:

```bash
# Letterbox: original aspect inside a black 1080x1920 frame
python3 scripts/make_vertical.py input.mp4 vertical.mp4 --mode letterbox

# Crop: center-crop to 9:16
python3 scripts/make_vertical.py input.mp4 vertical.mp4 --mode crop

# Blur-fill: original centered, blurred copy of itself fills the bars
python3 scripts/make_vertical.py input.mp4 vertical.mp4 --mode blur-fill
```

`blur-fill` is the most popular look for repurposing horizontal content as shorts.

### 9. Extract a clean audio track (NEW in v5.1.0)

The most common ask for a video editor: "give me just the audio so I can transcribe / re-mix / podcast it".

```bash
# Quick MP3 extraction
python3 scripts/extract_audio.py input.mp4 podcast.mp3

# 16 kHz mono WAV - the canonical format for ASR / Whisper / Vosk
python3 scripts/extract_audio.py input.mp4 transcribe.wav \
  --sample-rate 16000 --channels 1

# Lossless FLAC for archival
python3 scripts/extract_audio.py input.mp4 archive.flac

# Small Opus file for messaging / web
python3 scripts/extract_audio.py input.mp4 web.opus --bitrate 64k

# Trim to a 30-second clip starting at 1:15
python3 scripts/extract_audio.py input.mp4 clip.mp3 --start 75 --duration 30

# Auto-leveled output for podcast intake (single-pass loudnorm -16 LUFS)
python3 scripts/extract_audio.py input.mp4 leveled.mp3 --normalize
```

Output codec is auto-detected from the extension:

| Extension | Codec | Default bitrate | Notes |
|---|---|---|---|
| `.mp3` | libmp3lame | 192k | Widest player compatibility |
| `.m4a` | aac | 192k | iTunes / Apple Music native |
| `.aac` | aac | 192k | Raw ADTS stream |
| `.wav` | pcm_s16le | (lossless) | Best for ASR pipelines |
| `.flac` | flac | (lossless) | Archival, ~50% smaller than wav |
| `.opus` | libopus | 96k | Best small-file quality |
| `.ogg` | libvorbis | 192k | Open-source MP3 alternative |

All paths are validated against the same shell-metachar allowlist used by the other helpers. The script pre-flights the input with `ffprobe` and refuses cleanly when the source has no audio stream, when the output extension is unknown, or when `--bitrate` is malformed.

### 10. Format conversions

```bash
# 1080p H.264 with reasonable quality
ffmpeg -i input.mp4 -vf "scale=-2:1080" \
  -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 160k output_1080p.mp4
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success |
| 1 | ffmpeg / ffprobe failure mid-processing |
| 2 | bad arguments, unsafe path, missing input, unsupported output, no audio stream, etc. |

## Safety properties

- All workflows run locally. No remote API calls.
- Python helpers use `subprocess.run` with argument lists (never `shell=True`), and reject paths with shell metacharacters via a strict regex allowlist.
- The skill never modifies system configuration, environment variables, or other plugins.
- The skill only reads input files and writes output files at the paths the user provides.

## Known limitations

- Inputs must be valid video/audio files reachable on the local filesystem.
- The blur compositing path requires a pre-existing per-frame alpha matte. Producing the matte is out of scope.
- `make_vertical.py --mode blur-fill` does a full re-encode; the other modes also re-encode the video stream. Audio is copied where possible.

## v6.1.0 changes

- Added `scripts/extract_clip.py`: cut a sub-clip by `--start` + (`--end` or `--duration`). Fast stream-copy path is the default (no re-encode, lossless, faster than real-time; snaps to the nearest keyframe before the requested start). `--accurate` switches to a libx264 CRF re-encode for frame-accurate cuts. `--no-audio` drops the audio track. Timestamps accept seconds, `MM:SS[.mmm]`, and `HH:MM:SS[.mmm]`. Pre-flights with ffprobe to reject sources without a video stream, validates that `--end > --start`, clamps ranges that exceed source duration, and uses the same safe-path policy as the rest of the skill.
- Exit codes follow the rest of the skill: 0 success, 1 ffmpeg runtime failure, 2 argument / path / format errors. All other scripts unchanged.

## v6.0.0 changes

**Major-version bump to force a registry summary refresh.**

The public ClawHub listing for this skill was still showing the v4.0.0 marketing copy ("Pro-Studio v4.0.0. AI-powered background removal...") even though SKILL.md has been honest since v4.1.0. The same sticky-summary refresh that worked at v5.0.0 had partially regressed by v5.1.0, and a v5.2.0 patch publish did not refresh it either. v6.0.0 republishes with the honest description as a major-version bump so the registry, the SKILL.md, and the actual code all agree again. No code changes vs v5.1.0 / v5.2.0; same 7 scripts, same CLI flags, same exit codes.

## v5.1.0 changes

**New tool**

- `scripts/extract_audio.py` — clean audio-only extraction with auto-codec selection (mp3, m4a, aac, wav, flac, opus, ogg), optional `--sample-rate`, `--channels`, `--start`, `--duration`, and `--normalize`. Pre-flights the input via ffprobe, validates the output extension, and refuses unsafe paths. The 16 kHz mono WAV preset is the canonical input format for ASR pipelines, so this one tool closes the gap between video file and transcription.

**Bug fixes**

- `generate_srt.py` no longer leaks a Python `ValueError` traceback when a transcript field like `start` or `end` is not a number. The script now raises a `TranscriptFormatError` with a one-line message ("transcript field 'start' must be a number, got 'not-a-number'") and exits 2.
- `generate_srt.py` now rejects unsupported output extensions explicitly. Previously `.xml` and other unknown extensions silently produced SRT-shaped data with a fake suffix. Allowed extensions: `.srt`, `.vtt`, `.ass`.
- `loudnorm_two_pass.py` now pre-flights the input with `ffprobe -select_streams a` and refuses cleanly when the source has no audio stream, instead of failing inside Pass 1 of loudnorm with an opaque "could not find measurement JSON in ffmpeg stderr" error.

**No breaking changes**: every v4.2.0 / v5.0.0 CLI flag, output filename, and behaviour is preserved. v5.1.0 only adds patterns and removes footguns.

## License

MIT. See `LICENSE`.
