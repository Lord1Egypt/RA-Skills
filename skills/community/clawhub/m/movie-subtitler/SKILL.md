---
name: movie-subtitler
description: >-
  Download a foreign-language movie/video (or take a local file), transcribe and translate it to
  English with WhisperX, and recreate the video with English subtitles. Use on requests like
  "get English subs for this", "translate this movie", "subtitle this YouTube film". Fully local:
  yt-dlp → WhisperX → ffmpeg.
metadata:
  openclaw:
    emoji: "🎬"
    homepage: https://github.com/NelsonScott/movie-subtitler
    requires:
      bins:
        - ffmpeg
    install:
      - kind: brew
        formula: ffmpeg
      - kind: brew
        formula: yt-dlp
      - kind: uv
        package: whisperx
---

# movie-subtitler

Foreign-language video in → English-subtitled video out. One script does the whole pipeline.

## Prerequisites

- **ffmpeg** — audio extraction and video mux/burn.
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg` (Debian/Ubuntu) or your distro's package manager
- **yt-dlp** — only needed if `--input` is a URL rather than a local file.
  - macOS: `brew install yt-dlp`
  - Linux: `pip install -U yt-dlp` or `sudo apt install yt-dlp`
- **whisperx** — the transcribe/translate engine, on both macOS and Linux. Install it into a
  Python virtualenv, e.g.:
  ```bash
  python3 -m venv ~/.venvs/whisperx
  source ~/.venvs/whisperx/bin/activate
  pip install whisperx
  ```
  (or `uv pip install whisperx` if you use `uv`.) A venv install commonly isn't left on `PATH`,
  so point the script at it with `WHISPERX_BIN` (see below) if `command -v whisperx` doesn't
  find it — e.g. `WHISPERX_BIN=~/.venvs/whisperx/bin/whisperx`.
- **GPU is optional.** The script auto-detects `nvidia-smi`: if present (Linux/Windows with an
  NVIDIA GPU) it uses WhisperX's CUDA default (float16); otherwise it falls back to
  `--compute_type float32` for CPU (including Apple silicon) inference. CPU-only transcription
  is slower but works fine — expect roughly ⅓–½ of the video's runtime (see below).

If any of `whisperx`/`yt-dlp`/`ffmpeg` aren't on `PATH`, set `WHISPERX_BIN`, `YTDLP_BIN`, or
`FFMPEG_BIN` to their full paths before running the script.

## TL;DR — how to run it

```bash
./subtitle.sh \
  --input "https://www.youtube.com/watch?v=..." \
  --lang tr
```

- `--input` — URL (anything yt-dlp handles) or a local file path.
- `--lang` — source language code (`tr`, `pt`, `es`, `ja`, `fr`, ...). **Always pass it**;
  check the video first (`yt-dlp --skip-download --print "%(title)s"`) if unsure.
- Output lands in the **current directory** as `<name>.subbed.mp4` + `<name>.subbed.eng.srt`
  (srt basename matches the video so VLC auto-pairs the sidecar; override with `-o`/`--outdir`
  and `--name`).
- Default is a fast **soft-mux** (subs as a selectable track, no re-encode — Plex/players
  handle it fine). Pass `--burn` only if subs must be in the pixels (slow full re-encode).
- `--no-translate` keeps subs in the original language. `--model small` trades accuracy for speed.

## Known limitation: no speaker labels (diarization)

This skill doesn't label who's speaking. We tried bolting on `whisperx --diarize` (pyannote) and
it didn't hold up in practice, so it was left out. If you want to add it, here's what to know
going in:

- **Why a naive bolt-on doesn't work:** in translate mode, Whisper emits long (20-30s) subtitle
  cues, since alignment isn't possible on translated text. That means a single `[SPEAKER_NN]`
  label ends up stamped across an entire multi-person exchange — wrong, and a wall of text on
  screen. The speaker clusterer can also over-split a small cast into extra spurious IDs,
  especially with music or overlapping dialogue in the mix.
- **A design that would work better:** (1) transcribe in the *original* language with alignment
  enabled, giving short, per-word-timed cues with clean speaker turns; (2) translate each cue to
  English separately (an LLM works well here) while preserving timing and speaker labels — this
  step can also infer real character names from context instead of generic `SPEAKER_NN` IDs.
  Passing `--min_speakers`/`--max_speakers` to pyannote helps when you know the cast size.
  Diarization is the most compute-hungry step in the whole pipeline (roughly +50% runtime on
  CPU), so a GPU helps a lot if you go this route. It also needs `pyannote` installed alongside
  whisperx and an `HF_TOKEN` environment variable with access to pyannote's gated models on
  Hugging Face.

**Run it in the background** — WhisperX on CPU takes roughly ⅓–½ of the video's runtime
(a 2h movie ≈ 30–60 min; faster with a GPU). It prints `[movie-subtitler] DONE: <path>` at the end.

## Gotchas

- Whisper only translates **into English**, not between arbitrary language pairs.
- When translating, the script passes `--no_align`: WhisperX's per-language alignment models
  can't align translated English text to foreign audio, so we keep plain Whisper timestamps.
  They're accurate to ~1s, fine for subtitles.
- If the download 403s or fails, yt-dlp is probably stale: upgrade it (`pip install -U yt-dlp`
  or `brew upgrade yt-dlp`, depending on how you installed it).

## Files

- `subtitle.sh` — the whole pipeline (download → audio extract → whisperx → mux/burn).
