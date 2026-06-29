# Setup and Pre-Flight (MiniMax)

Extended pre-flight for music-craft-minimax: platform notes, required and
optional dependencies, the ask-the-user pattern, and local analysis memory.
Load this before the first MiniMax generation or analysis in a session.

## Pre-Flight Check (extended)

The platform detection block is the same as `music-craft` (run it first). The required and optional lists are extended for MiniMax.

## Platform Notes

- macOS/Linux are the primary targets: use `python3`, `command -v`, and normal shell `export`/`PATH` checks.
- Windows is partial support only: prefer PowerShell, use `python` or `py -3`, and verify env vars with `Get-ChildItem Env:MINIMAX_API_KEY` or `Test-Path Env:MINIMAX_API_KEY`.
- On Windows, `ffmpeg` and `mmx` are PATH-sensitive; if `Get-Command`/`where.exe` cannot find them, restart the shell or add the install directory to `PATH`.
- If Windows path/dependency issues keep blocking analysis, use WSL for the script-heavy parts instead of claiming full native support. For the full WSL2 setup, follow the base skill's [`windows-wsl-setup.md`](../../music-craft/references/windows-wsl-setup.md).
- If the MiniMax API or `mmx` CLI is unavailable, MiniMax cloud features such as cover and the lyrics API cannot run. Continue only with local-capable analysis tools (`ffmpeg`, `librosa`, Whisper) or switch to a local backend in `music-craft`.
- **v1.5.0:** URL download tools (`yt-dlp`, `curl` against streaming endpoints) and image-pipeline packages (`opencv-python`, `pylette`, `mediapipe`, `rapidocr`, `open_clip`) are gone from the recommended list. URL downloads now live in the private `music-source-fetch` skill; the image pipeline has been removed entirely. See the v1.5.0 changes note in [`free-tool-inputs.md`](free-tool-inputs.md).

## Required (skill will not work without these)

| Check | What it is | How to verify | If missing |
|---|---|---|---|
| `music_generate` tool | The runtime's built-in music generation tool | Inspect the active runtime's tool list | Tell the user: "This skill needs a `music_generate` tool, but the active runtime does not expose one. Configure a music provider in OpenClaw and try again." Stop. |
| `MINIMAX_API_KEY` env var | API key for the MiniMax Music 2.6 plan | `test -n "$MINIMAX_API_KEY" && echo "OK"` | Tell the user: "This skill needs the `MINIMAX_API_KEY` environment variable. Get one from your MiniMax account and export it. If you do not have a MiniMax Token Plan, use `music-craft` instead — it works with any provider." Stop. |
| `mmx` CLI | The MiniMax CLI for fine-flag control | `command -v mmx && mmx --version` (macOS/Linux) or `Get-Command mmx; mmx --version` (PowerShell) | Ask the user: install via the MiniMax install guide, or skip mmx-specific features and use the `music_generate` tool with prompts. Do not block — `mmx` is optional if the runtime has MiniMax configured, but Windows support is only partial and depends on PATH visibility. |
| `python3` | Required for the analysis scripts | `command -v python3` (macOS/Linux) or `python` / `py -3` (Windows PowerShell) | Tell the user: "The analysis pipeline (emotion analysis, mashup) needs Python 3.9+." Propose an install command for the active shell. Block emotion analysis if missing. |

## Optional (skill works without these, but quality improves with them)

| Tool | What it unlocks | Install per platform |
|---|---|---|
| `ffmpeg` | Audio conversion (WAV for analysis, MP3 export, trimming) | `apt install ffmpeg` · `brew install ffmpeg` · `winget install Gyan.FFmpeg` (restart PowerShell after install so PATH updates apply) |
| `librosa` | Audio analysis (BPM, key, energy, structure) | `pip install librosa numpy scipy` |
| `parselmouth` | Better pitch tracking (Praat under the hood) | `pip install praat-parselmouth` |
| `scikit-learn` | Audio clustering (segment detection) | `pip install scikit-learn` |

> **v1.5.0:** `yt-dlp` is no longer a recommended binary for this skill. URL downloads (YouTube, JioSaavn, mx3.ch) moved to the private `music-source-fetch` skill — install and run them there instead. Image-pipeline packages (`opencv-python`, `pylette`, `mediapipe`, `rapidocr`, `open_clip`) have been removed from the optional list because the image pipeline itself is gone.

The full per-platform install table is in the base skill's [Pre-Flight Check](../../music-craft/references/setup-and-preflight.md).

## The "ask the user" pattern

Same as the base skill: for each missing optional tool, present three options — install (propose exact command, let user approve), skip (use the simple path), or cancel. Never auto-install.

If `MINIMAX_API_KEY` is missing, the redirect is to the base skill, not "install MiniMax" — the user may not have a Token Plan at all.

## Local analysis memory (separate from generation)

Generation runs on MiniMax's cloud — your laptop just sends the prompt and downloads the MP3, so generation itself uses negligible local memory.

**However, this skill's local analysis scripts run on your machine and can use real memory.** Before running the full analysis pipeline, check available memory:

| Script | Models loaded | Approx peak RAM |
|---|---|---|
| `analyze_vocal_emotion.py` | `parselmouth` (Praat) + `scipy` | ~500 MB |
| `analyze_audio.py` | `librosa` + `transformers` (MERT or MIT AST) | 2–4 GB |
| `extract_lyrics_whisper.py` | `whisper` model (tiny/base/medium) | 1–5 GB depending on model size |
| `extract_stems.py` | `Demucs` (htdemucs) | 2–4 GB |
| `per_stem_analysis.py` | reads `stems.json`; `ffprobe` optional | negligible |
| `hybrid_remix.py` | `ffmpeg`; MiniMax only for explicit stem-cover smoke tests | negligible local |
| `emotion_to_prompt.py` | calls MiniMax API — negligible local | <100 MB |
| `compute_audio_embedding.py` | MERT model | 1–2 GB |
| `classify_instruments.py` | MIT AST | 1–2 GB |

**Combined (full analysis pipeline on a 4-min song):** ~6–10 GB peak on top of OS and other apps. On unified-memory systems (Apple Silicon, integrated graphics), this competes directly with macOS/Windows and your other applications. On dedicated-GPU systems (NVIDIA, AMD), model memory is taken from system RAM unless you have CUDA acceleration.

**Recommendations:**
- Close heavy apps (browser with many tabs, IDE, Docker) before running the full pipeline
- For `extract_lyrics_whisper.py`, use `medium` by default for lyrics. Use `small` only for quick drafts; it can hallucinate confident wrong-language lyrics. Use `large-v2` when singing is complex, noisy, or multilingual.
- Cross-check extracted lyrics with web lyrics or user-provided lyrics before building final prompts, especially when Whisper returns a surprising language or a short looping transcript.
- For `extract_stems.py`, the `--model` flag controls Demucs model choice. Default `htdemucs` is the normal 4-stem model; `htdemucs_ft` is opt-in and has non-commercial weight licensing; `htdemucs_6s` adds guitar/piano with quality caveats.
- If you run out of memory, run analysis steps individually rather than via `analysis_orchestrator.py` (which loads everything)

Optional dependency compatibility notes from v1.3.0 feedback (audio-only as of v1.5.0):

- `allin1` is problematic on macOS arm64 through its `madmom` dependency path; treat it as experimental unless install verification passes.
- `autochord` is fragile with current Keras/H5 stacks unless a working pin is verified.
- Verify optional installs with targeted import commands before depending on them in a workflow.

The `scripts/smoke_test.py` script verifies the environment is set up; it does **not** test memory headroom. Run your own memory check before running the full analysis.

## Whisper (for `extract_lyrics_whisper.py` and the lyrics workflow)

Whisper is a **Python package** (`openai-whisper`, MIT), and the `whisper`
CLI is just a thin wrapper. It is **not** in the standard `python3` — it
lives in whichever Python you installed it into. The scripts here
`import whisper` and will fail loudly on a Python that does not have it.

**How to find the right Python on any machine:**

1. `which whisper` — gives the path of the CLI (e.g. `/opt/homebrew/bin/whisper`,
   `/usr/local/bin/whisper`, `~/.local/bin/whisper`).
2. Read the shebang of the CLI: `head -1 "$(which whisper)"` — this is
   the Python that has Whisper installed (e.g. `#!/opt/homebrew/bin/python3.11`
   or `#!/usr/bin/env python3.11`).
3. Use that exact Python to call `extract_lyrics_whisper.py` (and any
   other script that does `import whisper`).

So instead of:

```bash
python3 scripts/extract_lyrics_whisper.py /tmp/song.mp3 --model medium
```

you typically need:

```bash
<path-from-shebang> scripts/extract_lyrics_whisper.py /tmp/song.mp3 --model medium
```

**If Whisper is not installed at all**, the script outputs a JSON
`{"error": "openai-whisper not installed", "install": "pip install openai-whisper"}`
and exits 0. The skill falls back gracefully. **Do not auto-install.** Show
the user the install command and the model sizes, and wait for consent.

**On a fresh install**, Whisper's first run downloads the chosen model
into `~/.cache/whisper/` (~75 MB for `tiny`, ~3 GB for `large`).

**Whisper model sizes (speed vs accuracy):**

| Model | Size | 3:00 song CPU transcription | RAM peak |
|---|---|---|---|
| `tiny` | ~75 MB | ~3–5 s | ~0.5 GB |
| `base` | ~150 MB | ~5–10 s | ~0.7 GB |
| `small` | ~500 MB | ~10–20 s | ~1 GB |
| `medium` | ~1.5 GB | ~40–60 s | ~2.5 GB |
| `large-v3-turbo` | ~3 GB | ~90–150 s | ~3.5 GB |

**Quality rule:** never use `small` or below for final prompts. The
skill defaults to `medium`. Use `small` only for quick drafts or
previews. The `extract_lyrics_whisper.py` script also runs the
`lyrics_sanity_warnings` function on the output and surfaces three risk
patterns: language mismatch with the expected language, looping
hallucinations (same segment repeated 3+ times), and unusually low
vocabulary variety. The skill requires the agent to read those warnings
before treating the transcript as final.

**On sharing the Whisper install with other apps:** Whisper is a
general-purpose transcription engine, and any tool on the machine
(global voice-to-text, dictation apps, accessibility tooling, other
analysis scripts) may share the same `pip` install. The skill never
touches other apps' configurations and does not assume the install is
shared — it only needs `import whisper` to succeed in the Python it is
being run with.
