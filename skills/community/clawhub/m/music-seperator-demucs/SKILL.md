---
name: music-seperator-demucs
description: Separate vocals and instrument stems from audio files with Demucs CLI. Use when the user asks for vocal extraction, accompaniment generation, stem splitting, batch separation, output format conversion (wav/flac/mp3), or Demucs performance/memory tuning on CPU/GPU. Also trigger when the user mentions demucs or demucas.
homepage: https://github.com/facebookresearch/demucs
metadata: {"clawdbot":{"emoji":"🎚️","requires":{"bins":["demucs"]},"install":[{"id":"pip","kind":"python","package":"demucs","bins":["demucs"],"label":"Install Demucs (pip)"}]}}
---

# Demucs

Use `demucs` to split music into stems (default: `vocals`, `drums`, `bass`, `other`).

Quick start
- Help: `demucs --help`
- Basic split: `demucs "input.mp3"`
- Output dir: `demucs "input.mp3" -o "D:\\output"`
- Vocals only pair: `demucs "input.mp3" --two-stems vocals`

Prerequisites
- Demucs available: `demucs --help` or absolute path like `D:\demucs-agent-tool\venv\Scripts\demucs.exe --help`.
- FFmpeg available: `ffmpeg -version` must succeed.
- Note: `ffmpeg-python` is only a Python wrapper and does not install `ffmpeg.exe`.

Common options
- Model: `-n htdemucs` (default) or other installed model names.
- Device: `-d cuda` or `-d cpu`.
- Chunking: `--segment 8 --overlap 0.25` to reduce VRAM/RAM pressure.
- No chunking: `--no-split` for short audio with enough memory.
- Equivariant shifts: `--shifts 1..10` (higher quality, slower).
- Parallel jobs: `-j 2` (or more on strong CPUs).

Output format
- Default output is WAV.
- FLAC: `demucs "input.mp3" --flac`
- MP3: `demucs "input.mp3" --mp3 --mp3-bitrate 320 --mp3-preset 2`
- Safer clipping behavior: `--clip-mode rescale` (default) or `--clip-mode clamp`.

Naming and folder layout
- Default output path pattern: `separated/<model>/<track>/<stem>.<ext>`.
- Customize names: `--filename "{track}/{stem}.{ext}"`.
- Variables supported: `{track}`, `{trackext}`, `{stem}`, `{ext}`.

Batch usage
- Multiple files in one call: `demucs "a.mp3" "b.wav" "c.flac" -o "D:\\separated"`.
- Prefer absolute paths for automation scripts and scheduled jobs.

Windows notes
- In venv, executable is usually `venv\\Scripts\\demucs.exe`.
- Use quoted paths when spaces exist: `demucs "D:\\My Music\\song.mp3"`.
- For external programs, prefer absolute executable path instead of shell activation.
- If non-ASCII paths cause tool/runtime issues, copy input to a temporary ASCII path and run Demucs there.

Troubleshooting
- `demucs` not found: run `python -m demucs --help` or call `venv\\Scripts\\demucs.exe` directly.
- `FFmpeg is not installed` / `ffprobe not found`: install FFmpeg and add it to PATH, then verify with `ffmpeg -version`.
- Out of memory: lower `--segment` (for example `6` or `4`), set `-d cpu`, or process fewer tracks at once.
- Slow speed on CPU: reduce `--shifts`, keep chunking enabled, and tune `-j`.
- Install/network failures: use a stable mirror and longer timeout when running pip.
