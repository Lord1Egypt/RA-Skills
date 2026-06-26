# Kami Conflict Detection

Real-time multi-camera physical conflict (fighting, shoving, scuffling) detection for RTSP camera streams or local video files. Uses YOLO for person pre-filtering and a remote multimodal LLM API for conflict analysis.

**Multi-camera capable.** A single process can monitor an arbitrary number of RTSP cameras concurrently (e.g. `living_room` + `office_door` + …). The YOLO ONNX session and conflict analyzer are loaded **once and shared** across all cameras; each camera owns an independent frame grabber, worker thread and snapshot directory. Push channels (Feishu / Discord / Telegram) are shared — every camera uses the same webhooks. The process keeps running across detections — it does NOT exit on event.

## How It Works

For each configured camera, a dedicated worker thread polls the stream, uses YOLO to count persons in each frame, and when 2+ people are detected, collects multiple frames and sends them to the Kami detection API for conflict analysis. When a conflict is confirmed, the worker saves a per-camera video clip covering the moments before and after the incident, prints an alert JSON line tagged with the camera name to stdout, pushes the alert to every configured channel, and **immediately resumes monitoring**. The process keeps running until the user stops it (Ctrl+C / OpenClaw shutdown).

```
For each camera (parallel worker thread):
  Read stream → YOLO counts persons → 2+ people? → Collect frames → LLM analysis
                                                                        ↓
                                            Conflict? → save per-camera clip
                                                     → push alert (stdout / inbox / Feishu / Discord / Telegram)
                                                     → resume monitoring (no exit)
```

## Quick Start

```bash
# 1. Install dependencies
bash setup.sh

# 2. Configure cameras and API key in config.json (recommended), then run:
.venv/bin/python conflict_detector_last.py

# Or for a one-off single-camera run via CLI override:
.venv/bin/python conflict_detector_last.py \
  --rtsp_url rtsp://192.168.1.100/live/stream1 \
  --camera_name living_room \
  --kami_api_key YOUR-API-KEY
```

## Installation

```bash
bash setup.sh
```

No `sudo` required. The script will:
- Auto-bootstrap **Python 3.10** in user space (via [uv](https://github.com/astral-sh/uv)) — no system-level package manager needed
- Create a `.venv/` virtual environment
- Install all pip dependencies (`onnxruntime`, `opencv-python-headless`, `numpy`, `requests`)
- Auto-download a pre-exported YOLO ONNX bundle from `https://publicfiles.xiaoyi.com/kami-conflict-detection-model.zip` (extracted to a temp folder, then `.onnx` is moved next to the script and the temp folder is deleted) — **no `.pt` conversion / no `ultralytics` install**.
- Create `alerts/` output directory

## API Key

This skill requires a Kami API key for the conflict analysis LLM service.

**If you don't have a key yet, register and obtain one at:**
> https://kamiclaw-skill.kamihome.com
You can enjoy a free credit limit of 200 credits.

Provide the key via:
- `config.json` (recommended) — the value persists across runs
- Command line: `--kami_api_key YOUR-KEY` (overrides `config.json` for this run only)

## Configuration File (config.json)

A `config.json` file in the skill directory persists user-provided values so you don't have to pass them on every run. Empty fields are ignored. Command-line arguments take priority over `config.json`.

```json
{
  "cameras": [
    {
      "name": "living_room",
      "rtsp_url": "rtsp://192.168.1.100/live/stream1"
    },
    {
      "name": "office_door",
      "rtsp_url": "rtsp://192.168.1.101/live/stream1"
    }
  ],
  "kami_api_key": "YOUR-KAMI-KEY",
  "feishu_webhook": "",
  "feishu_secret": "",
  "feishu_app_id": "",
  "feishu_app_secret": "",
  "discord_webhook": "",
  "telegram_bot_token": "",
  "telegram_chat_id": ""
}
```

Resolution order at runtime: **`--rtsp_url` (single-camera CLI override)** → **`cameras[]` in `config.json`** → empty (fatal). When OpenClaw asks the user for these values, write the answers into `config.json`.

### Multi-Camera Mode

The `cameras` array can contain one or many entries. All entries are monitored concurrently inside a **single Python process** (single-process / multi-thread / shared-model architecture):

| Field | Required | Behaviour when empty |
|-------|----------|----------------------|
| `name` | recommended | Free-form human-readable label (e.g. `living_room`, `front_door`, `office`). The agent should ask for it together with the `rtsp_url`. If the user does not provide one, the script auto-assigns `camera_0`, `camera_1`, … by array index and logs the assignment. The name is written into every alarm as `alert.camera`, prefixed to `alert.message` as `[name]`, and used as the snapshot subdirectory under `alerts/`. |
| `rtsp_url` | **yes** | Entry is skipped if empty. Accepts `rtsp://...`, `http(s)://...`, or a local file path. |

**Push channels are shared by all cameras.** The `feishu_webhook` / `discord_webhook` / `telegram_*` fields apply to every detected event; there is no per-camera webhook split. Every alert payload carries `"camera": "<name>"` and an `[<name>]` prefix in `message`, so the receiving operator can tell which camera fired the alarm.

**Continuous mode.** A detected conflict NEVER terminates the process. The worker pushes the alert and resumes monitoring on the same stream. The process only exits on Ctrl+C, all streams ending, or a fatal startup error.

## Prerequisites

- Linux/macOS shell with `curl` (or `wget`) and `unzip` available
- `yolov8s-worldv2.onnx` model file in the skill directory (auto-downloaded as a pre-exported ONNX bundle on first run if missing — see [Model File](#model-file) below)
- One or more RTSP cameras online and network-reachable, OR a local video file for testing
- Kami API key (see above)
- `setup.sh` has been run at least once

> Python 3.10 is **not** a manual prerequisite — `setup.sh` will install it locally without sudo if missing.

### Model File

The YOLO ONNX model is auto-fetched on first run from:

```
https://publicfiles.xiaoyi.com/kami-conflict-detection-model.zip
```

The zip extracts into a folder called `kami-conflict-detection-model/` containing one or more `.onnx` files (currently `yolov8s-worldv2.onnx`). The script:

1. downloads the zip,
2. extracts it,
3. moves the `.onnx` files next to `conflict_detector_last.py`,
4. deletes the extracted folder and the zip.

No `.pt` download, no `ultralytics` package install, no on-device ONNX export step. If the automatic download fails, manually fetch the zip, unzip it, and place `yolov8s-worldv2.onnx` in the skill directory.

## Parameters

### Required (via `config.json` or CLI)

| Parameter | Description |
|-----------|-------------|
| `cameras[]` (config.json) **or** `--rtsp_url` + `--camera_name` (CLI) | Video sources. Provide cameras as an array in `config.json`, or override with a single source on the CLI. Each entry accepts an RTSP URL or a local file path. |
| `--kami_api_key` | Kami API key for conflict analysis. Register at https://kamiclaw-skill.kamihome.com — you can enjoy a free credit limit of 200 credits. |

### Optional

| Parameter | Default | Type | Description |
|-----------|---------|------|-------------|
| `--rtsp_url` | *(empty)* | str | Single-camera CLI override. When set, takes priority over `cameras[]` in `config.json`. |
| `--camera_name` | *(empty)* | str | Camera name used together with `--rtsp_url`. Defaults to `camera_0` if omitted. |
| `--yolo_model` | `yolov8s-worldv2.onnx` | path | Path to the YOLO ONNX model file. |
| `--conf_threshold` | `0.25` | float (0-1) | YOLO detection confidence threshold. Lower detects more persons but may include false positives. |
| `--min_persons` | `2` | int | Minimum number of persons in frame to trigger LLM analysis. A conflict requires at least 2 people. |
| `--sample_interval` | `1.0` | float (seconds) | How often to run YOLO person detection on the stream. Lower values increase CPU usage but improve responsiveness. |
| `--multi_frame_count` | `3` | int | Number of frames to collect before sending to LLM. More frames give the LLM better context but increase latency. |
| `--multi_frame_gap` | `0.5` | float (seconds) | Time gap between collected frames. Spreads frames over time to capture motion progression. |
| `--buffer_seconds` | `30` | int (seconds) | Ring buffer duration. Stores recent frames in memory for video clip export when a conflict is detected. |
| `--clip_before` | `5` | int (seconds) | Seconds of video to include before the conflict moment in the exported clip. |
| `--clip_after` | `5` | int (seconds) | Seconds of video to include after the conflict moment. The script waits this long after detection before exporting. |
| `--output_dir` | `./alerts` | path | Root directory for saved video clips. Per-camera subfolders (`alerts/<camera_name>/`) are created automatically. |
| `--fps` | `15` | int | Frame rate for the video stream reader. Should match or approximate the camera's actual frame rate. |

### Parameter Tuning Guide

| Scenario | Adjustment |
|----------|------------|
| Missing persons in frame | Lower `--conf_threshold` (e.g., 0.25→0.15) |
| Too many false person detections | Raise `--conf_threshold` (e.g., 0.25→0.4) |
| Want to detect solo aggression | Set `--min_persons 1` (not recommended, high false positive rate) |
| High CPU usage | Increase `--sample_interval` (e.g., 1.0→3.0) |
| LLM analysis too slow | Reduce `--multi_frame_count` (e.g., 3→2) |
| Want longer video clips | Increase `--clip_before` and `--clip_after` |
| Memory constrained | Reduce `--buffer_seconds` (e.g., 30→15) |

## Output Format

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
  "message": "[living_room] Warning: Physical conflict detected. Two people are engaged in a physical altercation. Video clip saved to alerts/living_room/conflict_living_room_20260521_143022.mp4. Please review and take appropriate action."
}
```

| Field | Description |
|-------|-------------|
| `alert` | Event type, always `"conflict_detected"` |
| `camera` | The camera name that fired this alert (matches a `cameras[].name` entry, or `camera_0`/`camera_1`/… if auto-assigned) |
| `timestamp` | Alert time formatted as `YYYY-MM-DD HH:MM:SS` |
| `description` | LLM-generated description of the conflict |
| `video_clip` | File path to the saved MP4 video clip (under `alerts/<camera_name>/`) |
| `snapshot_image` | File path to a single representative JPEG frame (between `clip_before` and `clip_after`, resized to a 640px long side). Embedded inline in Feishu / Discord / Telegram pushes. |
| `clip_duration` | Total duration of the saved clip |
| `message` | Pre-formatted alert message ready for display, prefixed with `[<camera_name>] ` |

## Exit Codes

| Code | Meaning | Typical Action |
|------|---------|----------------|
| `0` | Normal exit — Ctrl+C, all streams ended, no fatal error. | End session. |
| `1` | Runtime error — model missing, no camera configured, API key not set. | Check `conflict_detector.log` for details. |

> Continuous mode: detected conflicts do NOT terminate the process — they only push alerts. The process stays alive until interrupted.

## Log File

All operational logs are written to `conflict_detector.log` in the script directory. Logs go to stderr (not stdout) to keep stdout clean for JSON output only.

## Examples

```bash
# Recommended: write cameras[] + kami_api_key into config.json once,
# then just run the script with no extra args. All cameras run in parallel.
.venv/bin/python conflict_detector_last.py

# Single-camera CLI override (one-off, e.g., for testing a video file)
.venv/bin/python conflict_detector_last.py \
  --rtsp_url /home/user/test_fight_video.mp4 \
  --camera_name test_video \
  --kami_api_key YOUR-API-KEY

# Longer video clips, faster sampling
.venv/bin/python conflict_detector_last.py \
  --clip_before 10 \
  --clip_after 10 \
  --sample_interval 0.5
```

---

## Alarm Push Channels (Detailed)

Beyond the default JSON stdout output, alarms can be simultaneously pushed to external messaging platforms. These are **pure push notifications** — they only send alerts OUT, they do NOT let you interact with the detector via those apps. (For interactive control via app, see [OpenClaw Channel Integration](#openclaw-channel-integration) below.)

All channels are optional. Configure any combination via command-line arguments or `config.json`. Push channels are **shared by all cameras** — every detected event is pushed to the same set of webhooks, but the `camera` field in the payload (and the `[<name>]` prefix in `message`) tells the receiver which camera fired the alarm.

### 1. Feishu (Lark) — Custom Bot Webhook

| Parameter | config.json field | Description |
|-----------|-------------------|-------------|
| `--feishu_webhook` | `feishu_webhook` | Webhook URL (required) |
| `--feishu_secret` | `feishu_secret` | Signing secret (optional) |
| `--feishu_app_id` | `feishu_app_id` | Self-built app App ID. **Required only for inline image rendering** — used to upload the conflict snapshot via Feishu OpenAPI and embed it as an `img` element inside the card. |
| `--feishu_app_secret` | `feishu_app_secret` | Self-built app App Secret, paired with `feishu_app_id`. |

**How to obtain the webhook:**

1. Open Feishu PC/web → Go to the target group chat
2. Click "..." (group settings) → **Bots** → **Add Bot** → **Custom Bot**
3. Give it a name (e.g., "Conflict Alert") → **Done**
4. Copy the **Webhook URL** (format: `https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx`)
5. (Optional) Enable **Signing Verification** → copy the secret key

**How to obtain `feishu_app_id` / `feishu_app_secret` (only needed for inline image):**

1. Open <https://open.feishu.cn/app> → **Create Custom App** (“创建企业自建应用”)
2. In **Credentials & Basic Info** copy `App ID` + `App Secret`
3. Under **Permissions & Scopes**, add `im:resource` (image upload). Enabling additional `im:message` scopes is optional and only needed for two-way bots, not for image upload.
4. Add the same app to the chat group used by the webhook so the uploaded image_key is renderable there.

> Without `feishu_app_id` + `feishu_app_secret`, the snapshot falls back to a clickable URL via the sm.ms public image host. With them, the image renders inline directly in the card.

> Push language: **Chinese**

### 2. Discord — Channel Webhook

| Parameter | config.json field | Description |
|-----------|-------------------|-------------|
| `--discord_webhook` | `discord_webhook` | Webhook URL |

**How to obtain:**

1. Open Discord → Go to the target text channel
2. Click the gear icon (Edit Channel) → **Integrations** → **Webhooks**
3. Click **New Webhook** → Give it a name → Select the channel
4. Click **Copy Webhook URL** (format: `https://discord.com/api/webhooks/123456/abcdef...`)

> Push language: **English**
> Mainland China note: Requires a proxy. Pass `--proxy http://host:port` on the command line.

### 3. Telegram — Bot API

| Parameter | config.json field | Description |
|-----------|-------------------|-------------|
| `--telegram_bot_token` | `telegram_bot_token` | Bot token |
| `--telegram_chat_id` | `telegram_chat_id` | Target chat/group/channel ID |

**How to obtain:**

1. Open Telegram, search for **@BotFather**
2. Send `/newbot` → follow the prompts to name your bot
3. Copy the **bot token** (format: `123456789:ABCdefGHI...`)
4. Add the bot to your target group (or just DM the bot)
5. Get the **chat ID**:
   - DM `@userinfobot` → it replies with your User ID (for private messages)
   - Or call `https://api.telegram.org/bot<TOKEN>/getUpdates` after sending a message in the group → find `"chat":{"id":-100xxxxx}` in the response
   - Group/channel IDs are negative numbers (e.g., `-1001234567890`)

> Push language: **English**
> Mainland China note: Requires a proxy. Pass `--proxy http://host:port` on the command line.

### Proxy Configuration

For Discord and Telegram in mainland China, pass the proxy on the command line:

```bash
.venv/bin/python conflict_detector_last.py \
  --discord_webhook https://discord.com/api/webhooks/... \
  --proxy http://192.168.1.1:7890
```

> The proxy is only used for Discord/Telegram. Feishu does not go through the proxy.

---

## OpenClaw Channel Integration

The push channels above are one-way: they only send alarm notifications OUT.

If you want to **directly interact with OpenClaw via a messaging app** (e.g., send a message in Telegram to trigger detection, or receive OpenClaw's conversational responses), you need to configure **OpenClaw Channels** in `openclaw.json`. This bypasses the OpenClaw backend chat window, letting the app become the primary interface.

### Feishu Channel

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxxxxx",
      "appSecret": "xxxxxxxxxxxxxxxx"
    }
  }
}
```

**How to obtain:** Create an app in [Feishu Open Platform](https://open.feishu.cn/), get the App ID and App Secret, then enable the bot messaging capability.

### Telegram Channel

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "123456789:ABCdefGHIjklMNO...",
      "dmPolicy": "open",
      "proxy": "http://192.168.1.1:7890"
    }
  }
}
```

| Field | Description |
|-------|-------------|
| `botToken` | Same bot token from @BotFather (same one used for push, or a different bot) |
| `dmPolicy` | `"open"` = accept messages from anyone; `"pairing"` = require `/pair` + approval; `"allowlist"` = only allow specific User IDs |
| `proxy` | **Must** include protocol prefix (`http://` or `socks5://`). Required in mainland China. |

**`dmPolicy` options:**

| Policy | Behavior |
|--------|----------|
| `open` | Any Telegram user can DM the bot and interact with OpenClaw |
| `pairing` | User sends `/pair` to the bot → terminal shows a CODE → run `openclaw pairing approve telegram <CODE>` to approve |
| `allowlist` | Only User IDs listed in `allowFrom` are allowed. Example: `"allowFrom": ["tg:123456789"]` |

> To find your Telegram User ID: DM `@userinfobot` on Telegram, or check the terminal logs during pairing.

### Discord Channel

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "MTUwODM4Mzk4...",
      "dmPolicy": "open",
      "allowFrom": ["*"],
      "requireMention": true
    }
  }
}
```

| Field | Description |
|-------|-------------|
| `token` | Bot token from [Discord Developer Portal](https://discord.com/developers/applications) → Application → Bot → Token |
| `dmPolicy` | Same as Telegram: `"open"` / `"pairing"` / `"allowlist"` |
| `allowFrom` | `["*"]` = accept all; or specific User IDs like `["discord:123456"]` |
| `requireMention` | If `true`, the bot only responds when @mentioned; if `false`, responds to all messages in allowed channels |
| `guilds` | (Optional) Restrict to specific server IDs: `["1234567890"]` |

**How to create a Discord bot:**

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** → name it → **Bot** tab → click **Reset Token** → copy the token
3. Under **Privileged Gateway Intents**, enable **MESSAGE CONTENT INTENT**
4. **OAuth2** tab → **URL Generator** → select scopes: `bot` → permissions: `Send Messages`, `Read Message History` → copy the invite URL
5. Open the invite URL in your browser to add the bot to your server

> **Important:** Discord channel in `openclaw.json` does **NOT** support a `proxy` field. If you need a proxy for Discord, set it via environment variable:
> ```bash
> export HTTPS_PROXY=http://192.168.1.1:7890
> ```

### Push Channels vs. OpenClaw Channels — Summary

| | Alarm Push Channels (this skill) | OpenClaw Channels (openclaw.json) |
|---|---|---|
| Direction | One-way: skill → app (notification) | Two-way: user ↔ OpenClaw (conversation) |
| Purpose | Send alarm messages when events detected | Allow user to trigger/control skills via messaging apps |
| Configuration | `--feishu_webhook` / `--discord_webhook` / `--telegram_bot_token` | `openclaw.json` → `channels` block |
| Requires | Webhook URLs or bot token | Full bot setup + OpenClaw runtime |

---

## File Structure

```
kami-conflict-detection/
├── conflict_detector_last.py   # Main detection script
├── yolov8s-worldv2.onnx        # YOLO person detection model
├── setup.sh                    # Environment setup script
├── requirements.txt            # Python dependencies
├── config.json                 # Persistent user configuration (cameras, API key, push)
├── SKILL.md                    # OpenClaw skill definition
├── README.md                   # This file
├── .venv/                      # Virtual environment (created by setup.sh)
├── alerts/                     # Alert video clips output (per-camera subfolders)
│   ├── <camera_name>/
│   │   └── conflict_<camera_name>_YYYYMMDD_HHMMSS.mp4
│   └── pending.jsonl           # Alarm inbox consumed by the heartbeat task
└── conflict_detector.log       # Runtime log file
```

## Troubleshooting

**Virtual environment not found**
→ Run `bash setup.sh`

**Model file missing (`yolov8s-worldv2.onnx`)**
→ The script will auto-download the pre-exported ONNX bundle on first run from `https://publicfiles.xiaoyi.com/kami-conflict-detection-model.zip`, extract it, move `yolov8s-worldv2.onnx` next to the script, and delete the temp folder. If this fails (e.g. no internet, `unzip` missing), manually fetch the zip, unzip it, and place the `.onnx` in the skill directory.

**RTSP connection failure**
→ Verify the camera is online, check the URL format in `cameras[].rtsp_url`, confirm network connectivity.

**API key error**
→ Ensure your Kami API key is valid. If you don't have one, register at https://kamiclaw-skill.kamihome.com. You can enjoy a free credit limit of 200 credits.

**No alerts generated**
→ Check `conflict_detector.log`. Common causes:
  - Fewer than 2 people in frame (YOLO pre-filter not triggered)
  - YOLO confidence too high — try `--conf_threshold 0.15`
  - LLM API returning "no conflict" — review the video to confirm actual conflict exists

**Script exits immediately with code 1**
→ Check log for details. Usually: model file missing, no camera configured (empty `cameras[]` and no `--rtsp_url`), or API key not provided.

**Feishu/Discord/Telegram push not working**
→ Check:
  - Webhook URL / bot token correct?
  - Proxy configured? (Discord/Telegram in mainland China require proxy — set `proxy` in `config.json` or pass `--proxy`)
  - Network reachable? (try `curl <webhook_url>` manually)
  - Check `conflict_detector.log` for push error messages

**Feishu card snapshot is just a URL/path, not an inline image**
→ The skill renders the snapshot inline only when `feishu_app_id` + `feishu_app_secret` are provided. Without them, it falls back to a clickable sm.ms URL or the local file path. Add a self-built Feishu app (see [Alarm Push Channels → Feishu](#1-feishu-lark--custom-bot-webhook)) and write the App ID / Secret into `config.json`.

**`unzip` not found during `setup.sh`**
→ Install `unzip` (e.g. `apt install unzip` / `brew install unzip`) and rerun `bash setup.sh`. The model bundle is distributed as a zip and requires `unzip` to extract.
