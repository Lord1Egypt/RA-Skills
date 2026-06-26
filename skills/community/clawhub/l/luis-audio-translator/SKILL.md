---
name: luis-audio-translator
description: Convert, compress, merge, split, clip, inspect, and extract audio locally with FFmpeg, plus decode supported music-cache formats including pure-Python Ximalaya .xm and optional Kugou/local helper formats. Use when Codex needs to process audio/video files, batch-convert music folders, inspect media metadata, or handle local encrypted/cache audio files.
---

# Luis-audio-translator Skill

## Overview

Use this skill for local audio processing through `scripts/luis_audio_translator.py`. It is portable: it does not contain personal paths, API keys, machine identifiers, or bundled proprietary binaries.

The core script works after download when Python is available and FFmpeg is installed on `PATH`. Ximalaya `.xm` decoding is built in and uses only Python. Other encrypted/cache formats may require optional local helper binaries.

## When to Use

- Convert audio formats, including extracting audio from video.
- Compress audio by bitrate.
- Merge multiple audio files in order.
- Split a file into equal-duration parts.
- Clip a time range from an audio/video file.
- Inspect duration, codec, bitrate, sample rate, and audio streams.
- Decode supported local music-cache inputs when the user has configured local helper tools.
- Convert Kugou special formats with `scripts/kugou_audio_converter.py`.

## Prerequisites

- Python 3.8+.
- FFmpeg for conversion, merge, split, clip, and video-to-audio.
- FFprobe for `info` and duration-aware `split`.

Resolution order:

1. Command-line option: `--app-dir <engine-dir>`.
2. Environment variables:
   - `LUIS_AUDIO_TRANSLATOR_ENGINE_DIR`
   - `LUIS_AUDIO_TRANSLATOR_FFMPEG`
   - `LUIS_AUDIO_TRANSLATOR_FFPROBE`
   - `LUIS_AUDIO_TRANSLATOR_UM`
   - `LUIS_AUDIO_TRANSLATOR_MUSIC_TOOL`
   - `LUIS_AUDIO_TRANSLATOR_SILK`
   - `LUIS_AUDIO_TRANSLATOR_KGG_HELPER`
   - `LUIS_AUDIO_TRANSLATOR_KUGOU_INFRA_DLL`
   - `LUIS_AUDIO_TRANSLATOR_KUGOU_DB`
3. System `PATH` for `ffmpeg` and `ffprobe`.

Do not put user-specific paths in `SKILL.md`. If a machine needs a local engine directory, set an environment variable outside the skill.

## How to Run

Resolve paths relative to the directory containing this `SKILL.md`.

Check dependency status:

```powershell
python scripts/luis_audio_translator.py diagnose
```

Convert or extract audio:

```powershell
python scripts/luis_audio_translator.py convert "input.mp4" --format mp3 --bitrate 192k --output-dir "out"
```

Compress:

```powershell
python scripts/luis_audio_translator.py compress "input.wav" --format mp3 --bitrate 96k --output-dir "out"
```

Merge:

```powershell
python scripts/luis_audio_translator.py merge "a.mp3" "b.wav" --format mp3 --output-dir "out" --basename "merged"
```

Split:

```powershell
python scripts/luis_audio_translator.py split "input.mp3" --segment-seconds 300 --format mp3 --output-dir "out"
```

Clip:

```powershell
python scripts/luis_audio_translator.py clip "input.mp3" --start 00:01:20 --duration 45 --format wav --output-dir "out"
```

Inspect:

```powershell
python scripts/luis_audio_translator.py info "input.flac"
```

Decode local cache input:

```powershell
python scripts/luis_audio_translator.py decrypt "input.ncm" --output-dir "out"
```

Decode Ximalaya `.xm` input:

```powershell
python scripts/luis_audio_translator.py decrypt "input.xm" --output-dir "out"
```

Convert Kugou special formats:

```powershell
python scripts/kugou_audio_converter.py diagnose --app-dir "<engine-dir>"
python scripts/kugou_audio_converter.py convert "KugouMusic" --format mp3 --output-dir "out" --recursive --app-dir "<engine-dir>"
```

## Quick Reference

Common output formats: `mp3`, `wav`, `ogg`, `flac`, `m4a`, `m4r`, `mp2`, `aiff`, `ac3`, `wma`, `amr`, `aac`, `opus`, `caf`, `au`, `mka`, `webm`.

Kugou special input formats handled by `kugou_audio_converter.py`: `.kgm`, `.kgma`, `.kgtemp`, `.kgm.flac`, `.kgg`.

Ximalaya input handled by `luis_audio_translator.py decrypt`: `.xm`.

Special output handling:

- `amr` forces 8000 Hz mono.
- `flac` uses signed 16-bit sample format.
- `m4r` uses an MP4 container.

Read `references/core-behavior.md` for supported input-extension lists and optional decode helper behavior.

## Privacy And Portability

- The skill does not embed local usernames, absolute install paths, credentials, or machine IDs.
- The script does not send files or metadata over the network.
- JSON output may include input/output paths because agents need them to continue workflows.
- `--print-command` prints full local paths and should be used only for debugging.

## Pitfalls

- If `diagnose` reports no FFmpeg, install FFmpeg or set `LUIS_AUDIO_TRANSLATOR_FFMPEG`.
- If `split` fails but `convert` works, install FFprobe or set `LUIS_AUDIO_TRANSLATOR_FFPROBE`.
- Decrypt helpers other than `.xm` are optional and environment-specific; ordinary conversion and `.xm` decoding should not depend on them.
- `.kgg` conversion needs `kgg-helper` and a compatible local Kugou `infra.dll`; `KGMusicV3.db` is used when available. Run the Kugou converter's `diagnose` command first.
- `.xm` decoding is implemented in pure Python and does not require Node.js, WebAssembly, or external helpers.
- OpenClaw, Hermes, Claude, and Codex should invoke the script by resolving `scripts/luis_audio_translator.py` relative to `SKILL.md`, not by using a machine-specific absolute path.

## Verification

- Run `python scripts/luis_audio_translator.py diagnose`.
- Run `python -m py_compile scripts/luis_audio_translator.py scripts/kugou_audio_converter.py scripts/xm_audio_decoder.py`.
- Run `python scripts/xm_audio_decoder.py --self-test`.
- Generate or provide a short test media file, then run `info`, `convert`, `merge`, and `split`.
