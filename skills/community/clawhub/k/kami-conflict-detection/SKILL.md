---
name: kami-conflict-detection
description: |
  Detect physical conflicts (fighting, shoving, scuffling) between 2+ people from one or many
  RTSP camera streams concurrently. Continuous mode: a single Python process monitors every
  configured camera in parallel, pushes a per-camera alert (stdout / inbox file / Feishu /
  Discord / Telegram) on each detected event, and keeps running — it does NOT exit on
  detection.
version: 2.0.4
author: kami-smarthome
tags:
  - smart-home
  - conflict-detection
  - fight-detection
  - violence-detection
  - yolo
  - rtsp
  - surveillance
  - security
  - edge-ai
  - multi-camera
  - openclaw
triggers:
  - detect fighting
  - detect conflict
  - detect physical conflict
  - check for fighting
  - is anyone fighting
  - detect scuffle
  - detect shoving
  - monitor for fights
  - start conflict monitoring
  - begin violence detection
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
    emoji: "🥊"
---

# Kami Conflict Detection

Detect physical conflicts (fighting, shoving, scuffling) between 2+ people from one or many RTSP camera streams concurrently. Continuous mode — the process never exits on detection; every confirmed event is pushed as an alert tagged with the originating camera, then monitoring resumes.

## Privacy Policy

For privacy policy details, see: <https://kamiclaw-skill.kamihome.com/privacy>

## How It Works

1. **YOLO pre-filter** — lightweight person detection counts people in each frame (must be ≥ `min_persons`, default 2).
2. **Multi-frame collection** — collects N frames with a configurable time gap.
3. **LLM conflict analysis** — frames are sent to the Kami detection API for violence/conflict judgment.
4. **Continuous alerting** — on a confirmed conflict, the worker saves a per-camera video clip, pushes an alert with `camera = <camera_name>` to every configured channel, and **immediately resumes monitoring**. The process keeps running until the user stops it (Ctrl+C / OpenClaw shutdown).

> Multi-camera: every entry in `config.json -> cameras[]` runs in its own worker thread inside the same process. The YOLO ONNX session, the conflict analyzer and all push channels are shared once across cameras. Push channels are **shared** — no per-camera webhook split. Stranger / clip / log lines are namespaced by camera name.

## When to Use

- Monitor one or many camera feeds for physical fights or scuffles
- Detect shoving, pushing, or violent behavior between people
- Run conflict detection on a local video file for testing
- Set up automated surveillance alerts for physical altercations

## Installation

```bash
bash setup.sh
```

No `sudo` required. The script auto-bootstraps **python3.10** in user space (via [uv](https://github.com/astral-sh/uv) when needed), creates `.venv/`, installs dependencies, and prepares `alerts/`. Idempotent — safe to re-run.

## Prerequisites

- Linux/macOS shell with `curl` (or `wget`) and `unzip` available
- `yolov8s-worldv2.onnx` model file in the skill directory (auto-downloaded as a pre-exported ONNX bundle from `https://publicfiles.xiaoyi.com/kami-conflict-detection-model.zip` on first run if missing — no `.pt` conversion required)
- One or more RTSP cameras online, OR a local video file for testing
- Kami API key (`--kami_api_key` or write to `config.json`). Register at <https://kamiclaw-skill.kamihome.com> for a free 200-credit quota.
- `setup.sh` has been run at least once

> Python 3.10 is **not** a manual prerequisite — `setup.sh` will install it locally without sudo if missing.

## Parameters

Confirm the following before running. The fields marked **(persisted in `config.json`)** can be saved to `config.json` next to the script so the user does not need to provide them every run — see [Configuration Persistence](#configuration-persistence) below.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--rtsp_url` | *(empty; see `cameras[]` in `config.json`)* | Single-camera CLI override. When set, takes priority over `cameras[]`. |
| `--camera_name` | *(empty)* | Optional camera name used together with `--rtsp_url`. Defaults to `camera_0`. |
| `--kami_api_key` | *(persisted in `config.json`)* | Kami API key |
| `--yolo_model` | `yolov8s-worldv2.onnx` | YOLO model file path |
| `--conf_threshold` | `0.25` | YOLO confidence threshold |
| `--min_persons` | `2` | Minimum person count to trigger LLM analysis |
| `--sample_interval` | `1.0` | YOLO pre-filter interval (seconds) |
| `--multi_frame_count` | `3` | Frames per LLM analysis |
| `--multi_frame_gap` | `0.5` | Gap between collected frames (seconds) |
| `--buffer_seconds` | `30` | Ring buffer duration for clip export |
| `--clip_before` | `5` | Seconds of video before the conflict |
| `--clip_after` | `5` | Seconds of video after the conflict |
| `--output_dir` | `alerts/` | Root directory for saved video clips. Per-camera subfolders (`alerts/<camera_name>/`) are created automatically. |
| `--fps` | `15` | Video stream frame rate |
| `--inbox_file` | `alerts/pending.jsonl` | Alarm inbox consumed by the heartbeat task |
| `--feishu_webhook` | *(persisted in `config.json`)* | Feishu custom bot webhook URL |
| `--feishu_secret` | *(persisted in `config.json`)* | Feishu signing secret (only if signing enabled) |
| `--feishu_app_id` | *(persisted in `config.json`)* | Feishu **self-built app** App ID. Required only if you want the conflict snapshot to render **inline** inside the Feishu card (uploads the image to Feishu and embeds it via `image_key`). |
| `--feishu_app_secret` | *(persisted in `config.json`)* | Feishu self-built app App Secret, paired with `--feishu_app_id`. |
| `--discord_webhook` | *(persisted in `config.json`)* | Discord channel webhook URL |
| `--telegram_bot_token` | *(persisted in `config.json`)* | Telegram Bot token |
| `--telegram_chat_id` | *(persisted in `config.json`)* | Telegram target chat/group/channel ID |
| `--proxy` | *(persisted in `config.json`)* | HTTPS proxy for Discord/Telegram (not used for Feishu). Mainland-China users MUST set this for Discord/Telegram. |

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
  "kami_api_key": "",
  "feishu_webhook": "",
  "feishu_secret": "",
  "feishu_app_id": "",
  "feishu_app_secret": "",
  "discord_webhook": "",
  "telegram_bot_token": "",
  "telegram_chat_id": ""
}
```

**`cameras` array — one entry per RTSP source.** All cameras run concurrently inside a single process, sharing the loaded YOLO ONNX model, the conflict analyzer and the same set of push channels. Add a new entry to the array for each additional camera (e.g. `living_room`, `office_door`, …).

| Camera field | Required | Behaviour when empty |
|--------------|----------|----------------------|
| `name` | recommended | Free-form short label written into every alert as `alert.camera`, prefixed to `alert.message` as `[name]`, and used as the snapshot subdirectory under `alerts/<name>/`. If the user does not supply one, the script auto-assigns `camera_0`, `camera_1`, … and logs the assignment. |
| `rtsp_url` | **yes** | Entry is skipped if empty. Accepts `rtsp://...`, `http(s)://...`, or a local file path. |

Resolution order at runtime: **`--rtsp_url` (single-camera CLI override)** → **`cameras[]` in `config.json`** → empty (fatal: `EXIT_ERROR`).

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
   - **Kami API key** — required for the LLM conflict analysis.
   - **Push channels** — which to enable (Feishu / Discord / Telegram) and their credentials. Push channels are **shared** across all cameras (no per-camera split); every camera uses the same webhooks.
     - **Feishu** — ask for `feishu_webhook` (required). If the user wants the conflict snapshot to render **inline inside the Feishu card**, ALSO ask for `feishu_app_id` + `feishu_app_secret` (self-built app credentials, used only to upload the snapshot via OpenAPI to obtain an `image_key`). Without app credentials the snapshot falls back to a clickable image-host URL.
     - **Discord** — ask for `discord_webhook`. The conflict snapshot is attached as multipart so it renders inline automatically. Mainland-China users MUST also provide `proxy`.
     - **Telegram** — ask for `telegram_bot_token` + `telegram_chat_id`. The conflict snapshot is delivered via `sendPhoto` and renders inline. Mainland-China users MUST also provide `proxy`.
3. **Write the user's answers back into `config.json`** (preserve existing non-empty fields). Subsequent launches skip these prompts.
4. **Immediately in the SAME turn**, run `bash setup.sh` (idempotent) and launch the detector. Do NOT end the turn after step 3 — do NOT wait for the user to say "start" or "begin".
5. If all required fields are already non-empty on entry, skip steps 2–3 and go straight to step 4.

## Alarm Push Channels

Alarms can be pushed through the following channels — all optional, configure any combination:

| Channel | Required Parameters |
|---------|--------------------|
| **Feishu** (custom bot) | `--feishu_webhook` (required); `--feishu_secret` (optional, signing); `--feishu_app_id` + `--feishu_app_secret` (optional, **enables inline snapshot image** via Feishu OpenAPI `image_key`) |
| **Discord** (channel webhook) | `--discord_webhook` (snapshot attached as multipart, renders inline) |
| **Telegram** (Bot API) | `--telegram_bot_token` + `--telegram_chat_id` (snapshot delivered via `sendPhoto`, renders inline) |

Beyond app push, every alarm is **always** delivered through two redundant local channels:

1. **stdout JSON line** — OpenClaw reads stdout line-by-line and reports each alert in chat (no exit; the process keeps running).
2. **Inbox file `alerts/pending.jsonl`** — appended on every alarm; consumed by the heartbeat task as a fallback.

> Refer to the official docs of each platform for how to obtain webhook URLs / bot tokens / chat IDs.
> In mainland China, Discord and Telegram require a proxy (`--proxy` or `HTTPS_PROXY`).
> Push card labels are language-fixed: **Feishu → Chinese**, **Discord/Telegram → English**.

## Usage

```bash
# First time only
bash setup.sh

# Multi-camera mode (recommended): write cameras[] into config.json once,
# then just run the script with no extra args.
.venv/bin/python conflict_detector_last.py

# Single-camera CLI override (one-off, e.g., for testing a video file)
.venv/bin/python conflict_detector_last.py \
  --rtsp_url /path/to/test_video.mp4 \
  --camera_name test_video \
  --kami_api_key YOUR-API-KEY
```

## Output Format (stdout JSON)

When a conflict is detected, the worker prints one JSON line and continues monitoring:

```json
{
  "alert": "conflict_detected",
  "camera": "living_room",
  "timestamp": "2026-05-21 14:30:22",
  "description": "Two people are engaged in a physical altercation",
  "video_clip": "alerts/living_room/conflict_living_room_20260521_143022.mp4",
  "snapshot_image": "alerts/living_room/snapshot_living_room_20260521_143022.jpg",
  "clip_duration": "10s",
  "message": "[living_room] Warning: Physical conflict detected. ..."
}
```

> The `snapshot_image` field is a single representative frame captured **between `clip_before` and `clip_after`** windows (i.e. at the conflict moment), resized to a 640px long side and saved as JPEG. It is embedded inline in the Feishu / Discord / Telegram cards.

## Exit Codes

| Code | Meaning | OpenClaw Action |
|------|---------|-----------------|
| `0` | Normal exit (Ctrl+C, all streams ended, no fatal error) | Inform user; optionally restart |
| `1` | Runtime error (model not found, missing API key, no camera configured) | Report error; check `conflict_detector.log` |

> Continuous mode: detected conflicts do NOT terminate the process — they only push alerts. The process stays alive until interrupted.

## Strict Rules (MUST Follow)

- **RULE**: Alarms flow via (a) stdout JSON line, (b) inbox file, (c) Feishu (optional), (d) Discord (optional), (e) Telegram (optional). Never rely on a single channel.
- **RULE (continuous mode)**: A detected conflict NEVER terminates the process. The worker pushes the alert and resumes monitoring on the same stream. There is no `exit 10`; there is no detect-report-restart loop.
- **RULE (multi-camera)**: All cameras in `config.json -> cameras[]` are monitored concurrently inside a single Python process (shared YOLO ONNX session, shared analyzer, one inference lock, per-camera FrameGrabber + worker thread). Never spawn one process per camera.
- **RULE (camera id)**: Every alarm written to `pending.jsonl`, Feishu, Discord and Telegram MUST include the camera name in the `camera` field. The `message` field MUST be prefixed with `[<camera_name>] `. Snapshots MUST be written under `alerts/<camera_name>/`.
- **RULE (camera name prompt)**: When asking the user for an RTSP URL, the agent MUST in the SAME question also ask for a human-readable camera `name` (e.g. `living_room`, `front_door`). If the user provides the URL but skips the name, the agent MUST EXPLICITLY notify them that an auto id (`camera_0`, `camera_1`, …) will be used; never assign the auto id silently.
- **RULE (shared push)**: Feishu / Discord / Telegram credentials in `config.json` apply to every camera. There is no per-camera webhook split.
- **RULE (feishu inline image)**: To render the conflict snapshot inline inside the Feishu card, the agent MUST ask the user for `feishu_app_id` AND `feishu_app_secret` (self-built app credentials) when configuring Feishu. Without them, the snapshot falls back to a clickable sm.ms URL (or plain text path). The webhook alone is NOT sufficient for inline image rendering.
- **RULE (snapshot)**: Every conflict alarm MUST carry a `snapshot_image` field pointing to a JPEG saved under `alerts/<camera_name>/snapshot_<camera_name>_YYYYMMDD_HHMMSS.jpg`. The frame is captured between `clip_before` and `clip_after` (i.e. at the conflict moment) and resized to a 640px long side for consistent display across push channels.
- **RULE**: Every heartbeat consumes `alerts/pending.jsonl`; non-empty → proactive chat summary; empty → `HEARTBEAT_OK`.
- **RULE**: Consumed alarms are MOVED to `alerts/consumed/`, not deleted.
- **RULE**: Before launch, read `config.json`; only ask the user for fields that are empty, and **write the answers back into `config.json`** so subsequent launches are non-interactive.
- **RULE (auto-launch)**: Once at least one camera (with `rtsp_url`) and `kami_api_key` are present in `config.json` (either pre-existing or just written), the agent MUST run `bash setup.sh` and launch the detector **in the same conversation turn**. Never end the turn at "config saved" — the user does NOT need to send a second message like "start it" or "begin detection".
- **RULE**: Warn the user if no push channel is configured (chat-window push still active).

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Virtual environment not found | Run `bash setup.sh` |
| Model file missing | `setup.sh` (or first script run) auto-downloads the ONNX bundle from `https://publicfiles.xiaoyi.com/kami-conflict-detection-model.zip`, extracts it, moves the `.onnx` next to the script and deletes the temp folder. If automatic download fails, manually fetch the zip, unzip it, and move `yolov8s-worldv2.onnx` into the skill directory. |
| `unzip` not found | Install `unzip` (e.g. `apt install unzip` / `brew install unzip`) and rerun `setup.sh`. |
| RTSP connection failure | Verify camera is online; check `cameras[].rtsp_url` |
| LLM API failure | Check `kami_api_key`; verify network to the Kami API endpoint |
| No alerts generated | See `conflict_detector.log`; try lowering `--conf_threshold` |
| Script exits with code 1 | Check log; common causes: missing model, no camera configured, missing API key |
| Feishu card shows snapshot path instead of an inline image | Provide `feishu_app_id` + `feishu_app_secret` (self-built app); without them the script falls back to sm.ms URL / local path. |
| Discord / Telegram push silently fails | Mainland-China users must set `proxy` in `config.json` (or `--proxy`). Feishu does NOT need a proxy. |
