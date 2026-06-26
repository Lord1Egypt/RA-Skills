---
name: kami-image-search
description: A skill by Kami SmartHome. Capture frames from your camera, describe them with AI, and search your visual history using natural language.
version: 1.0.0
author: kami-smarthome
tags:
  - smart-home
  - kami
  - smarthome
  - text-to-image search
  - image-search
  - visual-search
  - camera
  - rtsp
  - faiss
  - embedding
  - ai-vision
  - kamivision
  - monitoring
  - home-assistant
  - iot
  - edge-ai
triggers:
  - smart home
  - kami
  - text to image search
  - home assistant
  - image search
  - search image
  - find image
  - visual search
  - kami image
  - kami smart home
  - search camera
  - what did the camera see
  - find photo
  - search photos
  - look up image
  - camera history
  - check camera
metadata:
  openclaw:
    requires:
      bins:
        - python3.10
      hardware:
        cpu: "2+ cores (x86_64 / ARM64)"
        memory: "2 GB+"
        storage: "5 GB+"
        gpu: "optional"
      network:
        - "RTSP camera access (LAN)"
        - "Internet (KamiClaw API)"
      devices:
        - "RTSP IP camera"
    emoji: "🔍"
---

# Kami Image Search

> Search your camera's visual history with natural language.

Monitor your camera feed, capture frames automatically, and retrieve matching images by simply describing what you're looking for. Powered by the Kamivision cloud API for AI description and embedding generation.

### Features

- 🔍 Natural language image search
- 📸 Automatic frame capture from video streams
- 🧠 AI-powered image description (Kamivision API)
- 📁 Manual image import (JPEG / PNG / BMP / WebP)
- 🔁 Built-in duplicate frame detection
- ⏱ Time-range filtering
- 🏠 Designed for Kami SmartHome ecosystem

### Scenarios

- Doorstep delivery verification
- Home activity review
- Pet or child monitoring playback
- Batch photo indexing and retrieval

## Installation

```bash
bash setup.sh
```

Checks for Python 3.10, creates `.venv/`, and installs `opencv-python-headless`, `numpy`, `requests`, `Pillow`, `faiss-cpu`. Idempotent.

## Prerequisites

- Python 3.10 (setup.sh auto-detects system / pyenv / conda; auto-installs via conda or pyenv if missing)
- `image_config.json` configured with your stream URL(s) and Kamivision API key
- RTSP/RTMP camera(s) online and reachable (for capture mode)

## Kamivision API Key Setup

This skill requires a `KAMIVISION_API_KEY` to access the Kamivision cloud API.

**Check**: Read the `KAMIVISION_API_KEY` field in `image_config.json`.

- **If already configured (non-empty)** → Use it directly, no need to ask.
- **If empty** → Ask the user if they already have an API Key:
  - **Yes** → Enter the key directly. It will be saved to `image_config.json`.
  - **No** → Register at [Kamivision Flow](https://kamiclaw-skill.kamihome.com/) to obtain your API key. 🎁 **New users get 200 free credits on first registration.**

## Parameter Confirmation

Before running, confirm these key settings in `image_config.json`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `cameras` | (array) | Camera list. Each entry requires `STREAM_URL` and `DEVICE_ID` |
| `cameras[].STREAM_URL` | — | RTSP/RTMP/HTTP camera stream URL |
| `cameras[].DEVICE_ID` | `CAM-001` | Unique camera device identifier |
| `cameras[].CAPTURE_INTERVAL` | `10` | Seconds between frame captures (per-camera override) |
| `KAMIVISION_API_KEY` | — | Your Kamivision API key (shared across all cameras) |
| `SIMILARITY_THRESHOLD` | `0.35` | Search similarity threshold (0.0–1.0) |
| `SEARCH_TOP_K` | `5` | Max results per search |
| `TIME_ZONE_OFFSET` | `0` | UTC offset in hours for local time display (e.g. `-12` for UTC+12, `8` for UTC+8) |

### Multi-Camera Configuration Example

```json
{
  "cameras": [
    {
      "STREAM_URL": "rtsp://192.168.1.100/stream",
      "DEVICE_ID": "CAM-FRONT",
      "CAPTURE_INTERVAL": 10
    },
    {
      "STREAM_URL": "rtsp://192.168.1.101/stream",
      "DEVICE_ID": "CAM-BACK",
      "CAPTURE_INTERVAL": 15
    }
  ],
  "KAMIVISION_API_KEY": "your-api-key",
  "DATA_DIR": "./image_data",
  "TIME_ZONE_OFFSET": -12
}
```

- Each camera runs as an independent background process
- `DEVICE_ID` must be unique across all cameras
- Camera entries can override global defaults (`CAPTURE_INTERVAL`, `OUTPUT_WIDTH`, `SKIP_DUPLICATE`, etc.)
- Legacy single-camera config (without `cameras` array) is still supported for backward compatibility

### Common Brand RTSP Templates

**MUST show this table to the user** when configuring cameras, so they can pick a URL pattern based on their brand:

| Brand key | Brand | URL pattern |
|-----------|-------|-------------|
| `hikvision` | Hikvision | `rtsp://{user}:{pwd}@{ip}:554/Streaming/Channels/101` (`101`=ch1 main, `102`=ch1 sub) |
| `dahua` | Dahua | `rtsp://{user}:{pwd}@{ip}:554/cam/realmonitor?channel=1&subtype=0` (`subtype=0` main, `1` sub) |
| `tplink` | TP-Link | `rtsp://{user}:{pwd}@{ip}:554/stream1` (`stream1` main, `stream2` sub) |
| `ezviz` | EZVIZ | `rtsp://admin:{verify_code}@{ip}:554/H264/ch1/main/av_stream` |
| `uniview` | Uniview | `rtsp://{user}:{pwd}@{ip}:554/media/video1` |
| `reolink` | Reolink | `rtsp://{user}:{pwd}@{ip}:554/h264Preview_01_main` |

**Ask the user: do any parameters need to be changed?**

## Usage

### Start Capture

```bash
# Start all cameras
.venv/bin/python image_search.py --start-capture

# Start a specific camera
.venv/bin/python image_search.py --start-capture --device CAM-FRONT
```

### Stop Capture

```bash
# Stop all cameras
.venv/bin/python image_search.py --stop-capture

# Stop a specific camera
.venv/bin/python image_search.py --stop-capture --device CAM-FRONT
```

### Check Status

```bash
# Status of all cameras
.venv/bin/python image_search.py --status

# Status of a specific camera
.venv/bin/python image_search.py --status --device CAM-FRONT
```

### Import Images

```bash
# Single image
.venv/bin/python image_search.py --import /path/to/photo.jpg --json

# Entire directory (recursive)
.venv/bin/python image_search.py --import /path/to/photos/ --json
```

### Search

```bash
# Search across all cameras
.venv/bin/python image_search.py --search "keys on the table" --json

# Search a specific camera only
.venv/bin/python image_search.py --search "keys on the table" --device CAM-FRONT --json
```

### Search with Time Range

```bash
.venv/bin/python image_search.py \
  --search "person in blue jacket" \
  --time-start 1754538000 --time-end 1754541600 \
  --json
```

## Output (stdout JSON)

```json
{
  "status": "ok",
  "query": "keys on the table",
  "count": 1,
  "results": [
    {
      "image_name": "CAM-FRONT_1754538507.jpg",
      "image_path": "/opt/image_data/CAM-FRONT/20250815/CAM-FRONT_1754538507.jpg",
      "description": "A set of keys and a wallet on a table",
      "device_id": "CAM-FRONT",
      "timestamp": 1754538507,
      "time": "2025-08-15 10:00:07 AM",
      "score": 0.7823
    }
  ]
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (config issue, stream failure, API error, runtime exception) |

## Troubleshooting

- `bash: .venv/bin/python: No such file or directory` → Run `bash setup.sh`
- `OpenCV cannot open stream` → Check camera is online and `STREAM_URL` is correct
- `Kamivision API error` → Verify `KAMIVISION_API_KEY` and network connectivity
- `Unsupported file format` → Only JPEG, PNG, BMP, WebP are supported
- `No search results` → Ensure images have been captured/imported; try lowering `SIMILARITY_THRESHOLD`
- `FAISS index load failed` → Index may be corrupted; system rebuilds automatically, re-import data if needed

## Privacy Notice

This skill involves camera video stream frame capture and cloud-based image analysis. Please review the following privacy information before use:

### Cloud API Calls

- Relies on **KamiClaw API** for VLM image description and text embedding
- Data sent to the cloud is used solely for real-time inference and **will not be persistently stored or used for model training**
- API communication uses HTTPS encryption

### Local Data Storage

- Captured frames are stored in the working directory; users can delete them at any time
- Supports `retention_days` parameter for automatic expiration and deletion of historical data
- API Key is cached in `~/.kami/credentials.json` (permission 600, readable only by the current user)

### User Control

- Camera URL is configured by the user; this skill will not auto-discover or connect to cameras
- You can stop the skill at any time, delete local frame data and index files
- You can revoke your API Key at any time to terminate cloud access

> For more details on our privacy policy, visit: https://kamiclaw-skill.kamihome.com/privacy
