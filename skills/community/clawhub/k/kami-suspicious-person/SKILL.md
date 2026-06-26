---
name: kami-suspicious-person
description: Detect unregistered faces loitering in sensitive areas. Supports one OR many RTSP cameras concurrently in a single process (shared ONNX models, per-camera tracker). Runs continuously, outputs alarm JSON to stdout each time a stranger exceeds the loiter threshold, then keeps monitoring. No local GPU needed for face detection (CPU inference via ONNX).
version: 2.0.4
author: kami-smarthome
tags:
  - smart-home
  - face-recognition
  - stranger-detection
  - loitering-detection
  - surveillance
  - security
  - insightface
  - arcface
  - rtsp
  - edge-ai
triggers:
  - detect stranger
  - detect unknown person
  - detect unregistered face
  - stranger loitering
  - unknown face detection
  - suspicious person
  - face recognition alert
  - start suspicious person monitoring
  - begin stranger detection
metadata:
  openclaw:
    requires:
      bins:
        - python3.10
      hardware:
        cpu: "4+ cores (x86_64 / ARM64)"
        memory: "8 GB+"
        storage: "10 GB+"
        gpu: "optional (speeds up ONNX inference)"
      network:
        - "RTSP camera access (LAN)"
        - "Internet (KamiClaw API)"
      devices:
        - "RTSP IP camera"
    emoji: "🕵️"
---

# Kami Suspicious Person Detection

Detect unregistered face loitering events in sensitive areas. The script runs continuously and outputs an alarm JSON line to stdout each time a stranger exceeds the loiter threshold. It does NOT exit after an alarm — it keeps monitoring. Set `run_time: 0` for unlimited operation.

Uses ONNX models directly (no insightface package dependency):
- **SCRFD** (`det_10g.onnx`) — face detection + 5-point landmarks
- **ArcFace** (`w600k_r50.onnx`) — 512-dim face embedding extraction

## Privacy Policy

For privacy policy details, see: <https://kamiclaw-skill.kamihome.com/privacy>

## How It Works

1. **Face detection + landmarks** (CPU): SCRFD detects faces every `sample_interval` seconds.
2. **Face alignment + embedding**: ArcFace extracts 512-dim embeddings from aligned 112×112 face crops.
3. **Database matching**: Compare embeddings against the registered face database via cosine similarity. Registered faces are skipped.
4. **Stranger tracking**: Track unregistered faces across frames using sliding-average embedding.
5. **Loiter alarm**: When a stranger stays longer than `loiter_threshold`, output alarm JSON to stdout and save a face snapshot. After `cooldown`, the same stranger can trigger again if still present.

## When to Use

- Monitor a camera feed for unregistered/unknown people
- Detect strangers loitering in restricted or sensitive areas
- Get real-time alerts when an unknown face stays too long in view
- Run continuous face recognition surveillance

## Installation

```bash
bash setup.sh
```

No `sudo` required. The script auto-bootstraps **python3.10** in user space (via [uv](https://github.com/astral-sh/uv) when needed), creates `.venv/`, installs dependencies, prepares `alerts/`, `face_db/`, `models/`, and downloads SCRFD + ArcFace models (~180 MB) on first run. Idempotent.

## Prerequisites

- Linux/macOS shell with `curl` (or `wget`) available
- RTSP camera online, OR a local video file for testing
- `setup.sh` has been run at least once
- (Optional) Registered face images in `face_db/<person_name>/xxx.jpg`

> Python 3.10 is **not** a manual prerequisite — `setup.sh` will install it locally without sudo if missing.

## Face Database Setup

```
face_db/
  ├── Alice/
  │   ├── photo1.jpg
  │   └── photo2.jpg
  ├── Bob/
  │   └── photo1.jpg
  └── face_db.pkl   (auto-generated cache)
```

Pre-build the cache:

```bash
.venv/bin/python build_face_db.py --face_db ./face_db
```

## Parameters

Confirm the following before running. The fields marked **(persisted in `config.json`)** can be saved to `config.json` next to the script so the user does not need to provide them every run — see [Configuration Persistence](#configuration-persistence) below.

**Multi-camera note:** RTSP cameras are normally configured via the `cameras` array in `config.json` (see below). The `--rtsp_url` CLI flag is kept only for legacy single-camera mode and, if provided, overrides the `cameras` array entirely. The face database is **fixed at `<skill_dir>/face_db/`** and is shared by every camera — it is NOT a configurable field.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--rtsp_url` | *(persisted in `config.json` → `cameras[].rtsp_url`)* | Single-camera CLI override. Leave empty for multi-camera mode. |
| `--face_db` | `<skill_dir>/face_db/` | Fixed shared face database directory (used by ALL cameras). The user only needs to place photos inside; if it is empty or missing, every detected face is treated as a stranger. |
| `--det_model` | `models/det_10g.onnx` | SCRFD face detection model path |
| `--rec_model` | `models/w600k_r50.onnx` | ArcFace recognition model path |
| `--db_match_threshold` | `0.4` | Cosine similarity threshold for DB matching |
| `--stranger_match_threshold` | `0.35` | Threshold for cross-frame stranger tracking |
| `--loiter_threshold` | `300` *(persisted in `config.json`)* | Loitering alert threshold (seconds). Ask the user every launch whether to keep 300s (5 min) or change it. |
| `--sample_interval` | `2.0` | Face detection sampling interval (seconds) |
| `--cooldown` | `300` | Per-stranger alert cooldown (seconds) |
| `--det_thresh` | `0.5` | Face detection confidence threshold |
| `--min_face_size` | `40` | Minimum face size in pixels |
| `--output_dir` | `alerts/` | Alert output directory |
| `--run_time` | `0` | Max run time in seconds; `0` = unlimited |
| `--fps` | `15` | Video stream frame rate |
| `--expire_seconds` | `600` | Stranger tracking expiry (seconds since last seen) |
| `--inbox_file` | `alerts/pending.jsonl` | Alarm inbox consumed by the heartbeat task |
| `--feishu_webhook` | *(persisted in `config.json`)* | Feishu custom bot webhook URL |
| `--feishu_secret` | *(persisted in `config.json`)* | Feishu signing secret (only if signing enabled) |
| `--feishu_app_id` | *(persisted in `config.json`)* | Feishu self-built app ID. **Required for inline face snapshot rendering** in cards. |
| `--feishu_app_secret` | *(persisted in `config.json`)* | Feishu self-built app secret. Required together with `app_id`. |
| `--discord_webhook` | *(persisted in `config.json`)* | Discord channel webhook URL |
| `--telegram_bot_token` | *(persisted in `config.json`)* | Telegram Bot token |
| `--telegram_chat_id` | *(persisted in `config.json`)* | Telegram target chat/group/channel ID |
| `--proxy` | *(optional, command-line only)* | HTTPS proxy for Discord/Telegram (not used for Feishu) |

**Only ask the user about a parameter if (a) it's still empty in `config.json` AND has no command-line value, OR (b) the user explicitly asks to adjust it. Do NOT pause the conversation for blanket parameter confirmation.**

## Configuration Persistence (`config.json`)

A `config.json` file lives next to the script with the following empty-by-default fields:

```json
{
  "cameras": [
    {
      "name": "",
      "rtsp_url": ""
    }
  ],
  "loiter_threshold": "",
  "feishu_webhook": "",
  "feishu_secret": "",
  "feishu_app_id": "",
  "feishu_app_secret": "",
  "discord_webhook": "",
  "telegram_bot_token": "",
  "telegram_chat_id": ""
}
```

**`cameras` array — one entry per RTSP source.** All cameras run concurrently inside a single process, sharing the loaded SCRFD + ArcFace ONNX models (loaded once), the same face database, and the same set of push channels. Add a new entry to the array for each additional camera (`living_room`, `office_door`, …).

| Camera field | Required | Behaviour when empty |
|--------------|----------|----------------------|
| `name` | recommended | Auto-assigned as `camera_0`, `camera_1`, … in array order. **Used as the camera identifier in every alarm** (`alert.camera`, message prefix `[name]`, snapshot subdirectory `alerts/<name>/`). |
| `rtsp_url` | **yes** | Entry is skipped if empty. |

**Face database — fixed at `<skill_dir>/face_db/`.** This single directory is the shared registered-face set for every camera; it is NOT a config field. The user only needs to place per-person photo folders inside (`face_db/<person_name>/*.jpg`). **If the directory is empty or missing, every detected face is treated as a stranger.**

Resolution order at runtime: **command-line argument** → **`config.json`** → empty (skipped, or built-in default `300` for `loiter_threshold`). For RTSP, CLI `--rtsp_url` forces single-camera mode and ignores the `cameras` array.

**Workflow OpenClaw MUST follow (single-turn, no extra confirmation):**

1. On first launch, read `config.json` and identify which fields are still empty.
2. **Ask the user only for the empty fields**:
   - **Cameras** — for each camera the user wants to monitor, ask for the `rtsp_url` AND a camera `name` **in the same question**:
     - The `name` is a free-form short label, ideally a natural-language tag like `living_room` / `front_door` / `office`. It will appear in every alarm to identify which camera fired the event.
     - When the user is unsure about their RTSP URL format, provide these common brand templates as a reference:
       ```
       TP-Link:  rtsp://<user>:<password>@<ip>:554/stream1
       Hikvision(海康): rtsp://<user>:<password>@<ip>:554/Streaming/Channels/101
       Dahua(大华):    rtsp://<user>:<password>@<ip>:554/cam/realmonitor?channel=1&subtype=0
       ```
       > Note: `<user>` and `<password>` are the camera's login credentials (often `admin`); `<ip>` is the camera's LAN IP. The port is almost always `554`. Substream variants (lower resolution / bandwidth) may use path `102` (Hikvision) or `subtype=1` (Dahua).
     - **If the user only provides the `rtsp_url` and omits the name, IMMEDIATELY tell them: "No camera name provided. The script will auto-assign an incremental id like `camera_0` / `camera_1`. Do you want to proceed with the auto id?"** Only proceed with the auto id once the user accepts (or stays silent / says ok). Do NOT silently assign the auto id without notifying.
     - Persist each camera as an object in the `cameras` array.
   - **Loitering threshold** — explain that the default is `300` seconds (5 minutes) and ask whether to keep it or change it (e.g., `60` for testing, `600` for less sensitive). Persist as integer string.
   - **Push channels** — which to enable (Feishu / Discord / Telegram) and their credentials. Push channels are **shared** across all cameras (no per-camera split); every camera uses the same webhooks.
     - **Feishu**: If the user chooses Feishu, ask for `feishu_webhook`. Then ask for `feishu_app_id` and `feishu_app_secret` (explain: these are needed to upload face snapshots to Feishu so the alert card displays the image inline; without them the card will only show a clickable URL link to the image). Optionally ask for `feishu_secret` if they use webhook signing.
     - **Discord / Telegram**: Ask for the respective webhook URL or bot token + chat_id.
   - **Face database (CRITICAL first-launch reminder)** — On the FIRST launch (or when face_db is empty), the agent MUST prominently remind the user:
     > "The system has a face database at `<skill_dir>/face_db/`. Please place photos of known people inside (e.g., `face_db/Alice/photo1.jpg`). If the directory is empty, **every detected face will be treated as a stranger** and may trigger frequent alarms. You can add photos later and re-run `build_face_db.py` to update."
     This reminder must NOT be skipped or buried in other prompts.
3. **Write the user's answers back into `config.json`** (preserve existing non-empty fields). Subsequent launches skip these prompts.
4. **Immediately in the SAME turn**, run `bash setup.sh` (idempotent) and launch the detector as a background daemon. Do NOT end the turn after step 3 — do NOT wait for the user to say "start" or "begin".
5. If all required fields are already non-empty on entry, skip steps 2–3 and go straight to step 4.

## Alarm Push Channels

Alarms can be pushed through the following channels — all optional, configure any combination:

| Channel | Required Parameters |
|---------|--------------------|
| **Feishu** (custom bot) | `--feishu_webhook` + `--feishu_app_id` + `--feishu_app_secret` (for inline image). Optional: `--feishu_secret` |
| **Discord** (channel webhook) | `--discord_webhook` |
| **Telegram** (Bot API) | `--telegram_bot_token` + `--telegram_chat_id` |

In addition, every alarm is **always** appended to `alerts/pending.jsonl` (the inbox file), which is consumed by the heartbeat task to push to the chat window.

> Refer to the official docs of each platform for how to obtain webhook URLs / bot tokens / chat IDs.
> In mainland China, Discord and Telegram require a proxy (`--proxy` or `HTTPS_PROXY`).
> Push card labels are language-fixed: **Feishu → Chinese**, **Discord/Telegram → English**.

## Usage

```bash
# First time only
bash setup.sh

# (Optional) Pre-build face database
.venv/bin/python build_face_db.py --face_db ./face_db

# Run with RTSP stream
.venv/bin/python suspicious_person_detector.py \
  --rtsp_url rtsp://192.168.1.100/live/stream1

# Run with local video file
.venv/bin/python suspicious_person_detector.py \
  --rtsp_url /path/to/test_video.mp4
```

## Output Format (stdout JSON)

On alarm (each line is from one camera; multi-camera mode interleaves output):

```json
{
  "alarm": true,
  "type": "stranger_loitering",
  "timestamp": "2025-01-15T14:30:22.123456",
  "camera": "living_room",
  "stranger_id": "living_room_STR_0001",
  "duration_seconds": 312.5,
  "duration_display": "5m12s",
  "face_image": "alerts/living_room/living_room_STR_0001_20250115_143022.jpg",
  "hit_count": 48,
  "message": "[living_room] Warning: Stranger living_room_STR_0001 detected loitering ..."
}
```

The `camera` field carries the camera name configured in `cameras[].name` (or the auto id `camera_0`/`camera_1`/…). Stranger IDs are namespaced as `<camera_name>_STR_NNNN` so cross-camera collisions are impossible. Snapshots are saved under `alerts/<camera_name>/`.

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Run time exceeded or stream ended |
| `1` | Video source failure or runtime error |

The script does NOT exit on alarms — it keeps monitoring. Check `suspicious_person.log` for diagnostics.

## Strict Rules (MUST Follow)

- **RULE**: Launch the detector as a background daemon (e.g. `nohup ... &`) so the agent is never blocked.
- **RULE**: Alarms flow via Feishu / Discord / Telegram (all optional) and the inbox file (always). Never tail stdout.
- **RULE**: Every heartbeat consumes `alerts/pending.jsonl`; non-empty → proactive message; empty → `HEARTBEAT_OK`.
- **RULE**: Consumed alarms are MOVED to `alerts/consumed/`, not deleted.
- **RULE**: Before launch, read `config.json`; only ask the user for fields that are empty, and **write the answers back into `config.json`** so subsequent launches are non-interactive.
- **RULE (auto-launch)**: Once at least one `cameras[].rtsp_url` is present in `config.json` (either pre-existing or just written), the agent MUST run `bash setup.sh` and launch the detector as a background daemon **in the same conversation turn**. Never end the turn at "config saved" — the user does NOT need to send a second message like "start it" or "begin monitoring".
- **RULE (loiter prompt)**: Before launch, the agent MUST ask the user whether to keep `loiter_threshold` at its default (`300` seconds = 5 minutes) or change it, and persist the chosen value as an integer string in `config.json`. If the user says "keep default" or "unchanged", write `"300"` so it is no longer treated as empty next time.
- **RULE (multi-camera)**: All cameras in `config.json -> cameras[]` are monitored concurrently inside a single Python process (shared ONNX models, **one shared face_db**, one inference lock, per-camera FrameGrabber + StrangerTracker). Never spawn one process per camera.
- **RULE (camera id)**: Every alarm written to `pending.jsonl`, Feishu, Discord and Telegram MUST include the camera name in the `camera` field. The `message` field MUST be prefixed with `[<camera_name>] `. Snapshots MUST be written under `alerts/<camera_name>/`.
- **RULE (camera name prompt)**: When asking the user for an RTSP URL, the agent MUST in the SAME question also ask for a human-readable camera `name` (e.g. `living_room`, `front_door`). If the user provides the URL but skips the name, the agent MUST EXPLICITLY notify them that an auto id (`camera_0`, `camera_1`, …) will be used; never assign the auto id silently.
- **RULE (shared face_db)**: There is exactly ONE face database, fixed at `<skill_dir>/face_db/`. It is NOT a configurable field in `config.json`. On the **first launch**, the agent MUST prominently remind the user to place registered photos under `face_db/<person_name>/*.jpg`; if the directory is empty or missing, every detected face is treated as a stranger and will trigger alarms. This reminder MUST appear before starting the detector and MUST NOT be skipped.
- **RULE (feishu image)**: When Feishu channel is chosen, the agent MUST ask the user for `feishu_app_id` and `feishu_app_secret` (from a self-built Feishu app with `im:resource` permission). Without these, face snapshots will NOT render inline in the card — only a clickable URL link will be shown. Persist both in `config.json`.
- **RULE (shared push)**: Feishu / Discord / Telegram credentials in `config.json` apply to every camera. There is no per-camera webhook split.
- **RULE**: Warn the user if no push channel is configured.
- **RULE**: Push card labels are language-fixed: Feishu → Chinese, Discord/Telegram → English. The LLM-generated `message` text is not controlled by this skill.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Virtual environment not found | Run `bash setup.sh` |
| Model download fails | Check network connectivity |
| No faces detected | Lower `--det_thresh` (e.g., 0.3); ensure face is large enough |
| Too many false stranger alerts | Increase `--db_match_threshold`; add more reference photos |
| Same stranger triggers repeatedly | Increase `--cooldown` (e.g., 600) |
