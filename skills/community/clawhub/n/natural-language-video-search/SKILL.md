---
name: natural-language-video-search
description: >
  Semantic search over video files using Gemini embeddings.
  Index dashcam, security camera, or any mp4 footage, then search
  with natural language queries to find and auto-trim matching clips.
version: 0.2.3
metadata:
  clawdbot:
    requires:
      env:
        - GEMINI_API_KEY
      bins:
        - python3
        - uv
        - ffmpeg
    primaryEnv: GEMINI_API_KEY
    homepage: https://github.com/ssrajadh/sentrysearch
    emoji: "🎥"
---

# Natural Language Video Search

Search video files using natural language queries powered by Gemini Embedding 2's native video-to-vector embedding.

## What This Skill Does

This skill lets you index video files (dashcam footage, security camera recordings, any mp4) into a local vector database, then search them by describing what you're looking for in plain English. The top match is automatically trimmed and saved as a clip.

For Tesla dashcam footage, an optional telemetry overlay can burn speed, GPS, location, and turn signal data onto trimmed clips.

## Setup

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.11+.

1. Clone and install:

```bash
git clone https://github.com/ssrajadh/sentrysearch.git
cd sentrysearch
uv sync
```

For Tesla overlay support (reverse geocoding):

```bash
uv sync --extra tesla
```

2. Set your Gemini API key:

```bash
sentrysearch init
```

This prompts for your key, writes it to `.env`, and validates it with a test embedding. You can also set `GEMINI_API_KEY` directly as an environment variable.

## Commands

### Index video files

```bash
sentrysearch index <directory_or_file>
```

Options: `--chunk-duration` (default 30s), `--overlap` (default 5s), `--no-preprocess`, `--target-resolution`, `--target-fps`, `--skip-still` / `--no-skip-still`, `--verbose`

### Search indexed footage

```bash
sentrysearch search "<natural language query>"
```

Options: `-n` / `--results` (default 5), `-o` / `--output-dir`, `--trim` / `--no-trim`, `--threshold` (default 0.41), `--overlay` / `--no-overlay` (Tesla telemetry), `--verbose`

### Apply Tesla telemetry overlay

```bash
sentrysearch overlay <video_file>
sentrysearch overlay <video_file> -o output.mp4
```

Burns a HUD overlay onto a Tesla dashcam video showing speed, GPS coordinates, location name, and turn signal status. Reads telemetry from SEI NAL units embedded in Tesla firmware 2025.44.25+. Also available as `--overlay` flag on the search command to automatically overlay the trimmed clip.

### Check index stats

```bash
sentrysearch stats
```

## How It Works

Video files are split into overlapping chunks. Still-frame detection can skip chunks with no meaningful visual change, eliminating unnecessary API calls — this is the primary cost saver for idle footage like sentry mode or security cameras. Chunks are also preprocessed (reduced frame rate and resolution) to shrink upload size and speed up transfers, though the Gemini API bills based on video duration at a fixed token rate, not file size, so preprocessing does not reduce per-chunk token cost. Each chunk is embedded as raw video using Gemini Embedding 2 (no transcription or captioning). Vectors are stored in a local ChromaDB database. Text queries are embedded into the same vector space and matched via cosine similarity. The top match is auto-trimmed from the original file via ffmpeg.

## When To Use This Skill

- User asks to search through video files or footage
- User wants to find a specific moment in a video by describing it
- User asks to index or organize video footage for search
- User mentions dashcam, security camera, or surveillance clips
- User wants to find and extract a clip from a longer video
- User has Tesla dashcam footage and wants speed/GPS/location overlay on clips
- User wants to apply telemetry overlay to a Tesla video

## Example Interactions

User: "Search my dashcam footage for a white truck cutting me off"
Action: Run `sentrysearch search "white truck cutting me off"`

User: "Index all the video files in my Downloads folder"
Action: Run `sentrysearch index ~/Downloads`

User: "Search for a red light and include the Tesla overlay on the clip"
Action: Run `sentrysearch search "running a red light" --overlay`

User: "Add the speed and GPS overlay to this Tesla video"
Action: Run `sentrysearch overlay /path/to/tesla_video.mp4`

User: "How much footage do I have indexed?"
Action: Run `sentrysearch stats`

## Rules

- Always run `sentrysearch init` or confirm GEMINI_API_KEY is set before indexing or searching.
- If ffmpeg is not found on PATH, the bundled `imageio-ffmpeg` fallback is used automatically.
- Indexing costs ~$2.84/hour of active footage with default settings. Cost is driven by the number of chunks sent to the API — footage with long idle periods (sentry mode, security cameras) will be significantly cheaper since still-frame skipping eliminates those chunks entirely. Warn the user before indexing large directories.
- Search results include similarity scores. Scores below the threshold (default 0.41) trigger a low-confidence prompt before trimming.
- The Tesla overlay requires firmware 2025.44.25+ for SEI metadata. Videos without Tesla metadata will skip the overlay gracefully.
- Requires Python 3.11+.
