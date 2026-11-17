---
name: "mochi-media-workbench"
description: "Inspect media, extract audio, cut clips and frames, and export SRT/VTT subtitles locally, with optional local speech recognition and resumable chunk caches. Use for Audio and Video Workbench."
metadata: {"openclaw": {"requires": {"anyBins": ["python3", "python"]}, "homepage": "https://mochilab.bz", "version": "1.0.2"}}
---

# Audio and Video Workbench

## Select the local media job

Inspect a user-supplied local media file, then choose audio extraction, clip cuts, frames, subtitle conversion, transcription or a combined package. Read [references/input.md](references/input.md). Files and outputs stay in the active workspace. Use the user's requested time ranges; clarify missing ranges before cutting.

Python 3.10+ is required. Install scripts/requirements.txt in a dedicated virtual environment. Use an installed FFmpeg, or the official imageio-ffmpeg package's local executable. PyAV inspects and decodes the files. The script accepts local supported formats and disables network protocols/playlist demuxers; it does not fetch video URLs.

```text
python3 "{baseDir}/scripts/run.py" --workspace "CURRENT_WORKSPACE" --input "request.json"
```

Clips are transcoded for precise requested boundaries, then their actual durations are probed. Frames become JPEGs plus a contact sheet. User-provided timestamp segments convert to UTF-8 SRT/VTT, JSON and a time-stamped transcript. For a combined package, overlapping captions are trimmed and offset relative to each clip. This exports sidecar subtitles, not burned-in captions. package also returns a ZIP of the outputs.

## Optional local speech recognition

For transcribe only, install scripts/requirements-asr.txt. Choose tiny first on a CPU-only server; base or small use more resources. The engine is faster-whisper on CPU with int8 and 1..8 explicit threads. It runs locally, without a paid transcription API or MochiLab server. First model retrieval needs allowModelDownload:true; downloaded models are cached under this workspace. Prefer modelPath for a pre-downloaded, converted Whisper directory. The helper never downloads model weights when that option is false.

Transcription is segmented into 300-second chunks. Completed chunks are retained in the current workspace and keyed by source, model, decoder, language and engine version. A fresh requestId can reuse completed chunks after interruption; an identical completed requestId reuses verified outputs. No partial export is reported as a completed transcript. A local modelPath is fingerprinted from its model/config/tokenizer/vocabulary files. For a named downloaded model, the model name and engine version identify its cache; supply modelPath when exact model reproducibility matters.

## Review and delivery

Open the actual clip, preview.jpg and subtitle files. Return manifest.json with source hashes, selected timestamps and measured output durations. Recognition output is labeled local-asr and needs transcript review; user-provided captions are labeled separately. A model-written summary is a later task and must not be inserted as if recognized speech. Preserve source files and do not send media to external services unless separately requested.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
