---
name: luci-upload
description: "Upload a video or image to memories.ai. Use when the user wants to upload media, add a video/photo to their memory, or send a file to Luci. This skill is designed to work with luci-memory skill from clawhub"
metadata: {"clawdbot":{"emoji":"📤","requires":{"bins":["python3","ffprobe"],"env":["MEMORIES_AI_KEY"]},"primaryEnv":"MEMORIES_AI_KEY"}}
---

# luci-upload

Upload a video or image file to memories.ai with capture time and location metadata. User can also download LUCI AI app to manually upload as well.

## Setup

Requires `MEMORIES_AI_KEY` — same key as luci-memory. If not found, create `{baseDir}/.env`:

```
MEMORIES_AI_KEY=sk-your-key-here
```

Also requires `ffprobe` (from ffmpeg) for auto-extracting video metadata. Images can be uploaded without ffprobe finding anything — in that case the agent must supply time and location explicitly.

## When to use
- User wants to upload a video or image to memories.ai
- User says "add this video/photo to my memory" or similar
- User wants to send/import media to Luci

## How it works

The script tries to auto-extract capture time and GPS coordinates from the file metadata (via ffprobe). Videos from phones and JPEGs with EXIF usually work; PNGs and screenshots rarely have this info. If metadata is missing, the agent should ask the user for:

1. **When** was it taken? → pass as `--datetime` with `--timezone`
2. **Where** was it taken? → pass as `--location` (geocoded automatically) or `--lat`/`--lon`

The multipart `Content-Type` is chosen by file extension (`.mp4` → `video/mp4`, `.png` → `image/png`, `.jpg` → `image/jpeg`, etc.).

## How to invoke

```bash
# Probe metadata only (no upload) — do this first to check what info is available
bash {baseDir}/run.sh --probe --file /path/to/file

# Upload a video with auto-detected metadata
bash {baseDir}/run.sh --file /path/to/video.mp4

# Upload a video with explicit time and location name (geocoded to lat/lon)
bash {baseDir}/run.sh --file /path/to/video.mp4 --datetime "2025-06-22 14:00:00" --timezone Asia/Shanghai --location "Suzhou, China"

# Upload an image — usually needs explicit time/location since EXIF is often missing
bash {baseDir}/run.sh --file /path/to/photo.png --datetime "2025-09-01 00:00:00" --timezone Asia/Shanghai --location "Shunde, China"

# Upload with explicit coordinates and epoch timestamp
bash {baseDir}/run.sh --file /path/to/video.mp4 --time 1769097600000 --lat 31.3 --lon 120.59
```

## Parameters

| Flag | Short | Description |
|------|-------|-------------|
| `--file` | `-f` | Path to video or image file (required) |
| `--probe` | | Only show extracted metadata, don't upload |
| `--time` | | Start time as epoch milliseconds |
| `--datetime` | | Start time as readable datetime (e.g. `2025-06-22 14:00:00`) |
| `--timezone` | | Timezone for `--datetime` (e.g. `Asia/Shanghai`, `UTC`, `+8`) |
| `--lat` | | Latitude |
| `--lon` | | Longitude |
| `--location` | | Location name to geocode (e.g. `Suzhou, China`) |

## Workflow

1. **Probe first**: run with `--probe` to see what metadata the file has
2. If time and GPS are both present → upload directly
3. If missing (common for images, screenshots), ask the user for the missing info (time and/or location)
4. Upload with all parameters filled in