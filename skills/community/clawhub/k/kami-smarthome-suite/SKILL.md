---
name: kami-smarthome-suite
description: "Kami SmartHome skill bundle. One-click installer for the entire Kami SmartHome ecosystem with centralized configuration (API key, cameras, notifications) — no more configuring each skill individually."
version: 1.0.0
author: kami-smarthome
tags:
  - smart-home
  - kami
  - smarthome
  - suite
  - bundle
  - camera
  - rtsp
  - detect
  - video
  - image-search
  - package-detection
  - fall-detection
  - conflict-detection
  - face-recognition
  - surveillance
  - security
triggers:
  - kami smart home
  - kami smarthome suite
  - install kami skills
  - install all kami
  - smart home suite
  - kami home assistant
  - install kami suite
  - kami all skills
  - smart home bundle
metadata:
  openclaw:
    requires:
      bins:
        - python3.10
      hardware:
        cpu: "4+ cores (x86_64 / ARM64)"
        memory: "8 GB+"
        storage: "20 GB+"
        gpu: "optional (speeds up ONNX inference)"
      network:
        - "RTSP camera access (LAN)"
        - "Internet (KamiClaw API)"
      devices:
        - "RTSP IP camera"
    emoji: "🏠"
---

# Kami SmartHome Suite

## Overview

Kami SmartHome Suite is the one-stop installer for the **kami-smarthome** ecosystem. By installing this single skill, users get:

1. **Batch download** — install all 6 ecosystem skills from ClawHub in one go
2. **Guided configuration** — interactive setup for API key and notification channels; **all skills are ready to use immediately after configuration**
3. **Centralized config management** — to change anything later, edit one file and run `configure.sh --distribute` to sync

> **Configure once, run everywhere** — one config file controls all skills.

## Included Skills

This suite bundles the following 6 standalone skills:

| # | Skill | Emoji | Description | Use case |
|---|-------|-------|-------------|----------|
| 1 | **kami-package-detection**   | 📦 | Continuous package/parcel monitoring on RTSP streams using YOLO-World ONNX with smart notification | Doorstep delivery alerts |
| 2 | **kami-image-search**        | 🔍 | Periodic frame capture + VLM captioning + FAISS index for natural-language image search | Search historical frames |
| 3 | **kami-video-search**        | 📹 | Continuous video segmentation + VLM scene description + natural-language clip search | Search historical clips |
| 4 | **kami-fall-detection**      | 🚨 | Frame-difference detection + KamiClaw cloud inference for fall events | Elder / lone-resident care |
| 5 | **kami-conflict-detection**  | 🥊 | Multi-person physical conflict (fight/shove) detection with event-driven alarm JSON | Security alerting |
| 6 | **kami-suspicious-person**   | 🕵️ | Stranger recognition via SCRFD + ArcFace, detects unregistered face loitering | Doorway / stranger-loiter alerts |

### Skill Map

```
kami-smarthome-suite (this skill — installer entry point)
├── kami-package-detection    ── Package / delivery detection
├── kami-image-search         ── Image search
├── kami-video-search         ── Video recording & search
├── kami-fall-detection       ── Fall detection (cloud API)
├── kami-conflict-detection   ── Conflict / fight detection
└── kami-suspicious-person    ── Stranger / suspicious-person detection
```

## Installation

All Kami SmartHome skills are published on **ClawHub** and installed via `clawhub install`.

### Option 1: One-click install (recommended)

```bash
# Install the suite
clawhub install kami-smarthome-suite

# Run setup.sh — auto-installs all 6 skills + guides centralized config
bash {baseDir}/setup.sh
```

`setup.sh` performs:
1. One-shot install of all 6 Kami ecosystem skills from ClawHub
2. Detect / install Python 3.10:
   - **Debian/Ubuntu**: prefer conda → pyenv → system python3.10 (avoids `python3.10-venv` sudo dependency)
   - **Other systems**: prefer system python3.10 → pyenv → conda
   - If none found: auto-install (conda preferred → pyenv as fallback), no sudo required; only pyenv source build will ask for sudo when build-deps are missing
3. Interactive prompts for centralized config (API key, camera URL, notifications)
4. Auto-distribute the centralized config to each skill's local config files

> Idempotent — re-running will not reinstall skills that are already present.

### Option 2: Install individually

You can also install specific skills directly from ClawHub:

```bash
clawhub install kami-package-detection
clawhub install kami-image-search
clawhub install kami-video-search
clawhub install kami-fall-detection
clawhub install kami-conflict-detection
clawhub install kami-suspicious-person
```

After individual installs, run `bash {baseDir}/configure.sh` to apply unified configuration.

## Guided Setup (read this on first use)

> **Agent behavior**: when this skill is triggered, follow this order:
> 1. Check whether sub-skills are installed (any missing sub-skill directory means "not installed") → if missing, run `bash {baseDir}/setup.sh`
> 2. Check whether `kamiclaw_api_key` is empty in `{baseDir}/kami_config.json` → if so, prompt the user
> 3. Check whether `cameras` is empty in `{baseDir}/kami_config.json` → if so, guide the user to add cameras
> 4. **ALWAYS render the full RTSP brand template table below** (all 6 rows) whenever presenting the setup summary or guiding camera configuration. Do NOT abbreviate it to a single sentence like "supports Hikvision, Dahua..." — the user needs to see the actual URL patterns to fill in.
> 5. **ALWAYS show the warning**: ⚠️ Max 2 skills per camera — each skill opens an independent RTSP connection; most consumer cameras support only 2–4 concurrent sessions. Exceeding this causes stream disconnection.
> 6. **ALWAYS present BOTH Feishu config tiers upfront** when asking about notifications. Do NOT just say "Feishu Webhook URL" — list both tiers explicitly so the user can choose:
>    - **Tier 1 (basic)**: only `feishu_webhook_url` (+ optional `feishu_webhook_secret` for signed bots) → alarm snapshots are pushed as clickable image-host links
>    - **Tier 2 (inline images)**: above + `feishu_app_id` + `feishu_app_secret` (self-built app) → snapshots embed INLINE inside the Feishu card (best UX). Provide a one-line hint on how to get them: 飞书开发者后台 → 创建自建应用 → 拿 App ID / App Secret。
> 7. If all checks pass, skip the wizard and execute the user's request directly

### Step 0: Install sub-skills

- **Check**: look for sibling directories `kami-image-search`, `kami-video-search`, etc. next to `{baseDir}`
- **If missing**: run the one-click install:
  ```bash
  bash {baseDir}/setup.sh
  ```
  This script will: download all 6 sub-skills from ClawHub + create venvs + install dependencies
- **If present**: skip and proceed to config check

### Step 1: Configure KamiClaw API key

- **Check**: read the `kamiclaw_api_key` field from `{baseDir}/kami_config.json`
- **If empty**: tell the user 4 of the 6 skills require an API key, and prompt for one
- **How to obtain**: register at https://kamiclaw-skill.kamihome.com (free 200 credits)
- API-dependent skills: image-search, video-search, fall-detection, conflict-detection
- 2 fully-local skills (package-detection, suspicious-person) do not need an API key

### Step 2: Configure notification channels

- **Check**: read the `notifications` section of `{baseDir}/kami_config.json`
- **If all empty**: ask the user whether to set up alarm push (any combination is allowed)
- **Supported channels** (alarm skills `fall-detection` / `package-detection` / `conflict-detection` / `suspicious-person` push automatically when events fire):
  - **Feishu Webhook**: `feishu_webhook_url` (+ optional `feishu_webhook_secret` for signed webhooks) — supported by all 4 alarm skills
  - **Feishu self-built app** *(optional, for inline snapshot images)*: `feishu_app_id` + `feishu_app_secret` — when provided, all 4 alarm skills upload the alarm snapshot via Feishu OpenAPI and embed it INLINE inside the card. Without them, the snapshot falls back to a clickable image-host URL
  - **Telegram Bot**: `telegram_bot_token` + `telegram_chat_id` — supported by all 4 alarm skills (snapshot pushed inline via `sendPhoto`)
  - **Discord Webhook**: `discord_webhook_url` (push-only) — supported by all 4 alarm skills (snapshot attached as multipart, renders inline)
  - **Discord Bot**: `discord_bot_token` + `discord_channel_id` (two-way) — fall-detection & package-detection
- All channels are optional; skipped channels just fall back to JSON output without push
- ⚠️ Discord / Telegram may be unreachable from some regions. If a proxy is needed, set `HTTPS_PROXY` in your shell rc (e.g. `~/.bashrc`) yourself — **the suite intentionally does NOT manage proxy settings**

### Step 3: Configure cameras

- **Check**: read the `cameras` section of `{baseDir}/kami_config.json`
- **If empty or user wants to add**: ask for camera name + RTSP URL
- **MUST render the full brand table below verbatim** (all 6 rows with actual URL patterns). Do NOT condense into a one-liner like "supports Hikvision, Dahua..." — users need the full URL patterns to copy-paste:

| Brand | URL pattern |
|-------|-------------|
| Hikvision | `rtsp://{user}:{pwd}@{ip}:554/Streaming/Channels/101` (`101`=ch1 main, `102`=ch1 sub) |
| Dahua | `rtsp://{user}:{pwd}@{ip}:554/cam/realmonitor?channel=1&subtype=0` (`subtype=0` main, `1` sub) |
| TP-Link | `rtsp://{user}:{pwd}@{ip}:554/stream1` (`stream1` main, `stream2` sub) |
| EZVIZ | `rtsp://admin:{verify_code}@{ip}:554/H264/ch1/main/av_stream` |
| Uniview | `rtsp://{user}:{pwd}@{ip}:554/media/video1` |
| Reolink | `rtsp://{user}:{pwd}@{ip}:554/h264Preview_01_main` |

> ⚠️ **Max 2 skills per camera.** Each skill opens an independent RTSP connection; most consumer cameras support only 2–4 concurrent sessions. Exceeding this causes stream disconnection. If you need more coverage, add a second camera or use the sub-stream.

- After the user provides camera info, write it into `kami_config.json` under `cameras`
- Naming tip: use short, lowercase names (e.g. `front`, `back`, `garage`); names must be unique
- If the brand is not listed, the user can type the raw RTSP URL directly

### Configuration complete → all skills ready

After the user provides values:

1. Write the values back into the corresponding fields of `{baseDir}/kami_config.json`
2. Run distribution:
   ```bash
   bash {baseDir}/configure.sh --distribute
   ```
3. After distribution: tell the user that all skills are ready to use
4. **MUST show the user the Included Skills capability table** (see [Included Skills](#included-skills) above) so the user knows what is now available and which trigger phrases to use. This step is mandatory — do not end the turn until the table has been presented. The `configure.sh --distribute` command also prints the same summary to stdout; relay it verbatim if you do not want to retype the table.

### Updating configuration later

To change the API key or notification channels later:

```bash
# Re-run the interactive wizard
bash {baseDir}/configure.sh

# Or edit directly and redistribute
vim {baseDir}/kami_config.json
bash {baseDir}/configure.sh --distribute
```

## Prerequisites

- `clawhub` CLI installed (used to pull skills from ClawHub)
- Network access (for skill download + KamiClaw API calls from some skills)

> **Python 3.10 is required**. `setup.sh` selects detection priority by OS family (Debian/Ubuntu prefers conda/pyenv; other systems prefer system python3.10) and auto-installs via conda when missing. Other dependencies are managed by each sub-skill.

## Hardware Requirements

Recommended minimum hardware for each skill:

| Skill | CPU | Memory (RAM) | Storage | GPU | Notes |
|-------|-----|--------------|---------|-----|-------|
| kami-package-detection | 2+ cores | 2 GB | 500 MB | not required | YOLO-World ONNX, CPU-only |
| kami-image-search | 2+ cores | 2 GB | 5 GB+ | not required | FAISS index + SQLite frame history |
| kami-video-search | 2+ cores | 2 GB | 10 GB+ | not required | Stores video segments, scales with retention |
| kami-fall-detection | 1+ core | 1 GB | 200 MB | not required | Local does frame-diff only; inference runs in cloud |
| kami-conflict-detection | 4+ cores | 4 GB | 1 GB | optional (accelerates) | Local YOLO person detection + multi-frame analysis |
| kami-suspicious-person | 4+ cores | 4 GB | 1.5 GB | optional (accelerates) | SCRFD + ArcFace ONNX (~1 GB) |

**Recommended config to run all 6 skills concurrently**:
- CPU: 4+ cores (x86_64 / ARM64)
- Memory: 8 GB+
- Storage: 20 GB+ free space
- Network: stable connection (RTSP pull + API calls)
- OS: Linux (Ubuntu 20.04+ recommended)

> If you only enable a subset of skills, refer to the corresponding rows above.

## Centralized Configuration

### Design

The suite uses a **central config + auto-distribute** model:

```
kami_config.json (Single Source of Truth)
       │
       ▼  configure.py --distribute
       ├── kami-image-search/image_config.json
       ├── kami-video-search/stream_config.json
       ├── kami-fall-detection/config.json
       ├── kami-package-detection/config.json
       ├── kami-conflict-detection/config.json
       ├── kami-suspicious-person/config.json
       └── ~/.kami/credentials.json + cameras.json (cached for any skill)
```

### Central config file `kami_config.json`

Located in the suite directory, it contains the following sections:

| Section | Description | Skills affected |
|---------|-------------|-----------------|
| `kamiclaw_api_key` | KamiClaw API key | The 4 cloud-API skills |
| `cameras` | Map of named cameras (`name -> {stream_url}`) | All 6 skills (auto-distributed) |
| `notifications` | Feishu / Telegram / Discord push settings | fall-detection, package-detection, conflict-detection, suspicious-person |
| `skills.<name>.cameras` | Per-skill camera selector: `[]` = all, `["front"]` = filter by name | Selects which cameras each skill receives |
| `skills.<name>` | Per-skill tuning parameters | The corresponding skill |

Edit this file once and every skill is configured.

### Multi-Camera Support

The suite manages multiple cameras under the top-level `cameras` map. Give each camera a short, unique name (the dict key); each skill references cameras by that name.

```json
{
  "cameras": {
    "front":  { "stream_url": "rtsp://..." },
    "back":   { "stream_url": "rtsp://..." },
    "garage": { "stream_url": "rtsp://..." }
  },
  "skills": {
    "kami-image-search":      { "cameras": [] },                  // all cameras
    "kami-package-detection": { "cameras": ["front", "garage"] }  // filter by name
  }
}
```

**Naming tip.** Use short, lowercase, meaningful names (room or location, e.g. `front`, `back`, `garage`). Names must be unique inside `cameras`. If you skip naming, the suite auto-assigns `cam1`, `cam2`, ... in order.

- Interactive mode: the wizard asks for a name, press Enter to auto-assign.
- CLI mode: `--add-camera NAME=URL` (explicit) or `--add-camera URL` (auto-assigned).

All 6 skills support native multi-camera: each selected camera runs as an independent background process.

> ⚠️ **Max 2 skills per camera.** Each skill opens an independent RTSP connection; most consumer cameras support only 2–4 concurrent sessions. Exceeding this causes stream disconnection. If you need more coverage, add a second camera or use the sub-stream.

Recommended combos per camera placement:

| Camera position | Suggested skills (pick up to 2) |
|----------------|------------------|
| Front door / porch | `package-detection` + `suspicious-person` |
| Living room / hallway | `fall-detection` + `conflict-detection` |
| Garage / warehouse | `package-detection` + `image-search` |
| General coverage | `image-search` + `video-search` (full archival) |

**`image-search` vs `video-search`:**

| | image-search | video-search |
|--|--|--|
| Capture | Periodic snapshots (every N seconds) | 24/7 continuous video recording |
| Storage | Light (~5 GB) | Heavy (30 GB+) |
| Search result | Single matching frame | Video clip with context |
| Best for | "Was there a package?" quick lookups | "What happened yesterday afternoon?" full replay |

Use `image-search` alone for lightweight event spot-checks; add `video-search` when you need complete footage for evidence or review.

### Common Brand RTSP Templates

Don't remember your camera's RTSP path? The wizard ships built-in templates for the most common IP-camera brands. Pick `[t]emplate-add` instead of `[a]dd` and just fill in IP / username / password.

| Brand key | Brand | URL pattern |
|-----------|-------|-------------|
| `hikvision` | Hikvision | `rtsp://{user}:{pwd}@{ip}:554/Streaming/Channels/101` (`101`=ch1 main, `102`=ch1 sub) |
| `dahua` | Dahua | `rtsp://{user}:{pwd}@{ip}:554/cam/realmonitor?channel=1&subtype=0` (`subtype=0` main, `1` sub) |
| `tplink` | TP-Link | `rtsp://{user}:{pwd}@{ip}:554/stream1` (`stream1` main, `stream2` sub) |
| `ezviz` | EZVIZ | `rtsp://admin:{verify_code}@{ip}:554/H264/ch1/main/av_stream` |
| `uniview` | Uniview | `rtsp://{user}:{pwd}@{ip}:554/media/video1` |
| `reolink` | Reolink | `rtsp://{user}:{pwd}@{ip}:554/h264Preview_01_main` |

Usage:

```bash
# List all built-in templates
bash {baseDir}/configure.sh --list-templates

# Interactive: pick a brand, fill in fields, the URL is rendered for you
bash {baseDir}/configure.sh
#   Choice: t
#   Pick: 1 (hikvision)
#   Camera IP: 192.168.1.64
#   Username: admin
#   Password: pass@123      (special chars are auto URL-encoded)
#   Built URL: rtsp://admin:pass%40123@192.168.1.64:554/Streaming/Channels/101
```

> Special characters in user / password (e.g. `@`, `:`, `#`) are automatically URL-encoded so the resulting RTSP URL is always valid. If your camera brand isn't listed, just type the raw RTSP URL via `[a]dd` or `--add-camera`.

### Usage

```bash
# Mode 1: interactive wizard (prompts each field, supports add/edit/delete cameras)
bash {baseDir}/configure.sh

# Mode 2: set API key directly
bash {baseDir}/configure.sh sk_live_xxxxxxxx

# Mode 3: edit manually then distribute
vim {baseDir}/kami_config.json
bash {baseDir}/configure.sh --distribute

# Mode 4: show current config
bash {baseDir}/configure.sh --show

# Mode 5: add / remove cameras non-interactively (repeatable)
bash {baseDir}/configure.sh --add-camera rtsp://10.0.0.1/stream             # auto-named cam1
bash {baseDir}/configure.sh --add-camera front=rtsp://10.0.0.1/stream       # explicit name
bash {baseDir}/configure.sh --remove-camera front

# Mode 6: list common-brand RTSP URL templates
bash {baseDir}/configure.sh --list-templates
```

### Distribution Map

| Skill | Target file | Distributed fields |
|-------|-------------|--------------------|
| `kami-image-search`       | `image_config.json`  | `cameras: [{STREAM_URL, DEVICE_ID}, ...]` (all selected cameras), `KAMIVISION_API_KEY`, `CAPTURE_INTERVAL`, `RETENTION_DAYS` |
| `kami-video-search`       | `stream_config.json` | `cameras: [{STREAM_URL, DEVICE_ID}, ...]` (all selected cameras), `KAMI_API_KEY`, `SEGMENT_DURATION`, `RETENTION_DAYS` |
| `kami-fall-detection`     | `config.json`        | `cameras: [{rtsp_url, name}, ...]` (all selected cameras), `api_key`, `feishu_webhook_url`, `feishu_app_id`, `feishu_app_secret`, `telegram_bot_token`, `telegram_chat_id`, `discord_webhook_url`, `discord_bot_token`, `discord_channel_id`, `pre_seconds`, `post_seconds`, `save_alarm_clips` |
| `kami-package-detection`  | `config.json`        | `cameras: [{rtsp_url, device_id}, ...]` (all selected cameras), `conf_threshold`, `run_time`, `alarm_cooldown`, `feishu_webhook_url`, `feishu_app_id`, `feishu_app_secret`, `telegram_bot_token`, `telegram_chat_id`, `discord_webhook_url`, `discord_bot_token`, `discord_channel_id` (pure local inference, no API key) |
| `kami-conflict-detection` | `config.json`        | `cameras: [{rtsp_url, name}, ...]` (all selected cameras), `kami_api_key`, `feishu_webhook`, `feishu_app_id`, `feishu_app_secret`, `discord_webhook`, `telegram_bot_token`, `telegram_chat_id` |
| `kami-suspicious-person`  | `config.json`        | `cameras: [{rtsp_url, name}, ...]` (all selected cameras), `feishu_webhook`, `feishu_app_id`, `feishu_app_secret`, `discord_webhook`, `telegram_bot_token`, `telegram_chat_id` (pure local inference, no API key) |

> Power-user tip: each skill's argparse also accepts env vars (`KAMI_API_KEY`, `FEISHU_WEBHOOK_URL`, `TELEGRAM_*`, `DISCORD_WEBHOOK_URL`, `HTTPS_PROXY`) as a fallback. If you need an HTTPS proxy for Discord / Telegram, export `HTTPS_PROXY` in your shell rc — proxy settings are out of scope for `kami_config.json`.

### Integration with setup.sh

`setup.sh` automatically enters the centralized config flow after installing all skills. If skipped, run `bash configure.sh` later anytime.

## Exit Codes

| Exit code | Meaning |
|-----------|---------|
| `0` | All skills installed successfully |
| `1` | Some skills failed to install (check logs) |
| `2` | Prerequisite missing (no `clawhub`, or neither conda nor pyenv is usable and Python 3.10 cannot be installed) |

## Troubleshooting

**`clawhub` CLI not available**
```
clawhub: command not found
```
→ Install the ClawHub CLI first.

**A skill failed to install**
```
[!] kami-xxx (failed, exit 1)
```
→ Retry: `clawhub install kami-xxx`

**KamiClaw API key not configured**
→ Run `bash configure.sh` or register at https://kamiclaw-skill.kamihome.com

**Config changes have no effect**
→ After editing `kami_config.json`, run `bash configure.sh --distribute` to push the changes to each skill.

## Privacy Notice

This suite involves camera streams, image capture and face recognition. Please review the following privacy notes before use:

### Cloud API calls

- 4 skills depend on **KamiClaw API** (image-search, video-search, fall-detection, conflict-detection); 2 skills (package-detection, suspicious-person) run **fully locally**
- Data sent to the cloud is used only for real-time inference and is **not persisted nor used for model training**
- API traffic uses HTTPS encryption

### Local data storage

- Captured frames, video segments, etc. are stored under each skill's working directory and can be cleaned manually
- `image-search` and `video-search` honor a `retention_days` parameter for automatic expiry
- The API key and camera list are cached in `~/.kami/` (mode 600, current user only)

### Face data (kami-suspicious-person)

- The face feature database is built and matched fully locally — **nothing is uploaded to any server**
- Files are stored under `face_db/`, fully under user control
- Removing the `face_db/` directory wipes all face data

### User control

- Users freely choose which skills to enable; disabled skills collect nothing
- All camera URLs are user-supplied; skills do not auto-discover or auto-connect cameras
- Users can stop a skill, delete local data, or revoke the API key at any time

> Privacy policy details: https://kamiclaw-skill.kamihome.com/privacy
