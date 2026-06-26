# Kami Suspicious Person Detector

Real-time unregistered face loitering detection for sensitive areas. Uses SCRFD + ArcFace ONNX models directly (no insightface package dependency) for face detection and recognition. Cross-platform: works on Linux, macOS, and Windows with CPU inference. The script runs continuously — each time a stranger loiters beyond the threshold, it outputs an alarm JSON line to stdout and keeps monitoring.

**Multi-camera capable.** A single process can monitor an arbitrary number of RTSP cameras concurrently (e.g. `living_room` + `office_door` + …). The SCRFD + ArcFace ONNX models AND the registered face database are loaded **once and shared** across all cameras; each camera owns an independent frame grabber, stranger tracker and snapshot directory. Push channels (Feishu / Discord / Telegram) are shared — every camera uses the same webhooks. The face database is a fixed directory `<skill_dir>/face_db/` and is NOT configurable.

## How It Works

The detector monitors an RTSP camera stream (or local video file), detects faces, compares them against a registered face database, and tracks unregistered faces over time. When a stranger remains in view longer than the configured threshold (default: 5 minutes), the script outputs an alarm JSON to stdout, saves a face snapshot, and continues monitoring. A per-stranger cooldown prevents repeated alerts for the same person.

```
Start script → Monitor stream → Stranger detected → Track duration
                                                        ↓
                              Duration >= threshold → Output alarm JSON → Continue monitoring
```

## Quick Start

```bash
# 1. Install dependencies
bash setup.sh

# 2. (Optional) Add registered faces to the database
#    See "Face Database" section below

# 3. Run detection
.venv/bin/python suspicious_person_detector.py --rtsp_url rtsp://192.168.1.100/live/stream1
```

## Installation

```bash
bash setup.sh
```

No `sudo` required. The script will:
- Auto-bootstrap **Python 3.10** in user space (via [uv](https://github.com/astral-sh/uv)) — no system-level package manager needed
- Create a `.venv/` virtual environment
- Install all pip dependencies (`onnxruntime`, `opencv-python-headless`, `numpy`)
- Create required directories (`alerts/`, `face_db/`, `models/`)
- Download SCRFD (`det_10g.onnx`, ~16MB) and ArcFace (`w600k_r50.onnx`, ~166MB) models

Works on Linux and macOS. No GPU or insightface package needed.

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
  "loiter_threshold": "300",
  "feishu_webhook": "",
  "discord_webhook": "",
  "telegram_bot_token": "",
  "telegram_chat_id": ""
}
```

> The face database path is **not** in `config.json`. It is fixed at `<skill_dir>/face_db/` and shared by every camera — just place per-person photo folders inside (see [Face Database](#face-database)).

Resolution order for each field: **command-line argument** → **config.json** → empty (skipped, except `loiter_threshold` which falls back to built-in default `300` seconds = 5 minutes). When OpenClaw asks the user for these values, write the answers into `config.json`. The `loiter_threshold` field is the **loitering alert threshold in seconds**; the agent should ask every first launch whether to keep `300` or change it (e.g., `60` for testing, `600` for less sensitive).

### Multi-Camera Mode

The `cameras` array can contain one or many entries. All entries are monitored concurrently inside a **single Python process** (single-process / multi-thread / shared-model architecture):

- The SCRFD + ArcFace ONNX models are loaded **once** and shared across all camera threads.
- The registered face database is **globally shared** — a single `FaceDatabase` instance is loaded from the fixed location `<skill_dir>/face_db/` and queried by every camera.
- Inference is serialized via an internal lock to keep CPU latency predictable.
- Each camera owns its own `FrameGrabber` thread, `StrangerTracker`, alert cooldown table and snapshot subdirectory `alerts/<camera_name>/`.

**Per-camera fields:**

| Field | Required | Behaviour when empty |
|-------|----------|----------------------|
| `name` | recommended | Free-form human-readable label (e.g. `living_room`, `front_door`, `office`). The agent should ask for it together with the `rtsp_url`. If the user does not provide one, the script auto-assigns `camera_0`, `camera_1`, … by array index and logs the assignment. The name is written into every alarm as `alert.camera`, prefixed to `alert.message` as `[name]`, and used as the snapshot subdirectory under `alerts/`. Stranger tracking IDs are namespaced as `<camera_name>_STR_NNNN` so cross-camera collisions are impossible. |
| `rtsp_url` | **yes** | Entry is skipped if empty. Accepts `rtsp://...`, `http(s)://...`, or a local file path. |

**Face database (fixed, shared by all cameras):** the directory `<skill_dir>/face_db/` is the single registered-face set. **It is NOT a config field** — the user only needs to place per-person photo folders inside (see [Face Database](#face-database)). If the directory is empty or missing, every detected face is treated as a stranger and may trigger alarms.

**CLI override.** Passing `--rtsp_url` on the command line forces single-camera mode and ignores the `cameras` array entirely (camera name defaults to `camera_0`). `--face_db` may point to an alternative directory for the run, but normal operation just uses the fixed `face_db/`.

## Face Database

The face database stores registered personnel. Faces in the database are considered "known" and will NOT trigger alerts.

### Directory Structure

```
face_db/
├── John_Smith/
│   ├── front.jpg
│   ├── side.jpg
│   └── another_angle.png
├── Jane_Doe/
│   └── photo1.jpg
├── Security_Guard_01/
│   ├── img1.jpg
│   └── img2.jpeg
└── face_db.pkl          ← auto-generated cache (do not edit manually)
```
If the face database is not enabled, everyone will be treated as strangers.

### Naming Rules

| Item | Rule | Example |
|------|------|---------|
| Person folder name | Any valid directory name. This becomes the person's identity label. Use underscores or hyphens instead of spaces. | `John_Smith/`, `guard-01/` |
| Image files | Must have extension `.jpg`, `.jpeg`, `.png`, or `.bmp`. Filename itself does not matter. | `photo1.jpg`, `front_view.png` |
| Image content | Each image should contain exactly ONE clearly visible face of that person. | — |

### Best Practices

- Use 2-5 photos per person for better accuracy (different angles, lighting)
- Ensure faces are clearly visible and not occluded
- Minimum recommended face size in photos: 112x112 pixels
- Avoid group photos — use single-person portraits
- If the database is empty or missing, ALL detected faces are treated as strangers

### Building the Cache

The main script auto-builds `face_db.pkl` on first run. To pre-build manually:

```bash
.venv/bin/python build_face_db.py --face_db ./face_db
```

If you add/remove photos, delete `face_db.pkl` and re-run to rebuild.

## Parameters

### Required

For multi-camera deployments, configure the `cameras` array in `config.json` (see [Multi-Camera Mode](#multi-camera-mode)). The CLI flags below are kept for legacy single-camera mode.

| Parameter | Description |
|-----------|-------------|
| `--rtsp_url` | Single-camera CLI override. Accepts RTSP URL (e.g., `rtsp://192.168.1.100/live/stream1`) or local file path (e.g., `/path/to/video.mp4`). When provided, ignores `config.json -> cameras[]`. |

### Optional

| Parameter | Default | Type | Description |
|-----------|---------|------|-------------|
| `--det_model` | `models/det_10g.onnx` | path | Path to the SCRFD face detection ONNX model. |
| `--rec_model` | `models/w600k_r50.onnx` | path | Path to the ArcFace face recognition ONNX model. |
| `--face_db` | `<skill_dir>/face_db/` | path | Shared face database directory (used by every camera). Defaults to the fixed `<skill_dir>/face_db/`; only override on the command line for unusual setups. If the directory is empty or missing, every detected face is treated as a stranger. |
| `--db_match_threshold` | `0.4` | float (0-1) | Cosine similarity threshold for database matching. A detected face with similarity >= this value to any registered face is considered "known". Increase to reduce false matches (stricter); decrease to be more lenient. |
| `--stranger_match_threshold` | `0.35` | float (0-1) | Cosine similarity threshold for cross-frame stranger tracking. Used to determine if a stranger in the current frame is the same person seen in previous frames. Lower than `db_match_threshold` because appearance varies more across frames. |
| `--loiter_threshold` | `300` | int (seconds) | How long a stranger must remain in view before triggering an alert. Default is 300 seconds (5 minutes). Set lower for more sensitive detection. |
| `--sample_interval` | `2.0` | float (seconds) | How often to run face detection on the video stream. Lower values increase CPU usage but improve tracking accuracy. |
| `--det_thresh` | `0.5` | float (0-1) | Face detection confidence threshold. Faces below this confidence are ignored. Lower to detect more faces (may include false positives); raise to only detect clear faces. |
| `--min_face_size` | `40` | int (pixels) | Minimum face width/height in pixels. Faces smaller than this are skipped. Helps filter out distant or blurry faces. |
| `--output_dir` | `./alerts` | path | Directory where alert face snapshots are saved. Created automatically if it doesn't exist. |
| `--run_time` | `0` | int (seconds) | Maximum run time. `0` means unlimited (runs until stream ends or user interrupt). |
| `--cooldown` | `300` | int (seconds) | Per-stranger alert cooldown. Same stranger won't re-alert within this window. |
| `--fps` | `15` | int | Frame rate for the video stream reader thread. Should match or be close to the camera's actual frame rate. |
| `--expire_seconds` | `600` | int (seconds) | Stranger tracking expiry. If a stranger is not seen for this many seconds, their tracking record is removed. Prevents stale records from accumulating. |

### Parameter Tuning Guide

| Scenario | Adjustment |
|----------|------------|
| Too many false "stranger" alerts for known people | Increase `--db_match_threshold` (e.g., 0.45→0.5) or add more photos to face_db |
| Same stranger gets multiple tracking IDs | Decrease `--stranger_match_threshold` (e.g., 0.35→0.30) |
| Want faster alerts | Decrease `--loiter_threshold` (e.g., 300→60 for 1-minute alerts) |
| Same stranger alerts too often | Increase `--cooldown` (e.g., 300→600) |
| High CPU usage | Increase `--sample_interval` (e.g., 2.0→5.0) |
| Missing distant faces | Decrease `--min_face_size` (e.g., 40→20) |
| Too many false face detections | Increase `--det_thresh` (e.g., 0.5→0.6) |

## Output Format

The script runs continuously and prints a JSON alarm line to stdout each time a stranger loitering event is detected. It does NOT stop after an alarm.

When alarm triggers (each line is from one camera; multi-camera mode interleaves output):

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
  "message": "[living_room] Warning: Stranger living_room_STR_0001 detected loitering in sensitive area for 5m12s, exceeding alert threshold. Face snapshot saved to alerts/living_room/living_room_STR_0001_20250115_143022.jpg. Please review and take appropriate action."
}
```

When no alarm (normal exit, all camera workers ended):

```json
{
  "alarm": false,
  "type": null,
  "detail": "All camera workers exited",
  "run_seconds": 3600.0,
  "cameras": ["living_room", "office_door"]
}
```

| Field | Description |
|-------|-------------|
| `alarm` | `true` for stranger loitering events, `false` for normal exit summary |
| `type` | Event type, always `"stranger_loitering"` for alarms |
| `camera` | Camera name (`cameras[].name` or auto id `camera_0`/`camera_1`/…) the alarm came from |
| `timestamp` | ISO 8601 timestamp of the alert |
| `stranger_id` | Per-camera tracking ID, namespaced as `<camera_name>_STR_NNNN` |
| `duration_seconds` | Total time the stranger has been in view (seconds) |
| `duration_display` | Human-readable duration string |
| `face_image` | File path to the saved face snapshot (best quality frame), under `alerts/<camera_name>/` |
| `hit_count` | Number of frames in which this stranger was detected |
| `message` | Pre-formatted alert message; always prefixed with `[<camera_name>] ` |

## Exit Codes

| Code | Meaning | Typical Action |
|------|---------|----------------|
| `0` | Normal exit — run_time exceeded, video ended, or user interrupt. | Session complete. |
| `1` | Runtime error — failed to open stream, crash, etc. | Check `suspicious_person.log` for details. |

## Log File

All operational logs are written to `suspicious_person.log` in the script directory. Logs go to stderr (not stdout) to keep stdout clean for JSON output only.

## Examples

```bash
# Basic usage with RTSP camera
.venv/bin/python suspicious_person_detector.py \
  --rtsp_url rtsp://192.168.1.100/live/stream1

# Test with a local video file, 1-minute alert threshold
.venv/bin/python suspicious_person_detector.py \
  --rtsp_url /home/user/test_video.mp4 \
  --loiter_threshold 60

# Strict matching, faster sampling
.venv/bin/python suspicious_person_detector.py \
  --rtsp_url rtsp://192.168.1.100/live/stream1 \
  --db_match_threshold 0.5 \
  --sample_interval 1.0 \
  --loiter_threshold 180

# Limit single round to 1 hour
.venv/bin/python suspicious_person_detector.py \
  --rtsp_url rtsp://192.168.1.100/live/stream1 \
  --run_time 3600
```

---

## Alarm Push Channels (Detailed)

Beyond the JSON stdout output, alarms can be simultaneously pushed to external messaging platforms. These are **pure push notifications** — they only send alerts OUT, they do NOT let you interact with the detector via those apps. (For interactive control via app, see [OpenClaw Channel Integration](#openclaw-channel-integration) below.)

All channels are optional. Configure any combination via command-line arguments or `config.json`.

### 1. Feishu (Lark) — Custom Bot Webhook

| Parameter | config.json field | Description |
|-----------|-------------------|-------------|
| `--feishu_webhook` | `feishu_webhook` | Webhook URL |
| `--feishu_secret` | *(command-line only)* | Signing secret (optional) |

**How to obtain:**

1. Open Feishu PC/web → Go to the target group chat
2. Click "..." (group settings) → **Bots** → **Add Bot** → **Custom Bot**
3. Give it a name (e.g., "Stranger Alert") → **Done**
4. Copy the **Webhook URL** (format: `https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx`)
5. (Optional) Enable **Signing Verification** → copy the secret key

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
.venv/bin/python suspicious_person_detector.py \
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
kami-suspicious-person/
├── suspicious_person_detector.py   # Main detection script (ONNX-based)
├── build_face_db.py                # Face database builder utility
├── setup.sh                        # Environment setup + model download
├── requirements.txt                # Python dependencies (no insightface)
├── SKILL.md                        # OpenClaw skill definition
├── README.md                       # This file
├── .venv/                          # Virtual environment (created by setup.sh)
├── models/                         # ONNX models (downloaded by setup.sh)
│   ├── det_10g.onnx                # SCRFD face detection model
│   └── w600k_r50.onnx              # ArcFace face recognition model
├── face_db/                        # Registered face database
│   ├── <person_name>/xxx.jpg       # Person photos
│   └── face_db.pkl                 # Auto-generated embedding cache
├── alerts/                         # Alert snapshots output
│   └── STR_XXXX_YYYYMMDD_HHMMSS.jpg
└── suspicious_person.log           # Runtime log file
```

## Troubleshooting

**Virtual environment not found**
→ Run `bash setup.sh`

**Model download fails**
→ Check network connectivity. The script downloads from GitHub Releases (~180 MB total). Try again or download manually.

**No faces detected**
→ Lower `--det_thresh` (e.g., 0.3); ensure faces in frame are large enough (>40px).

**Too many false stranger alerts for known people**
→ Increase `--db_match_threshold` (e.g., 0.45→0.5); add more reference photos to `face_db/`.

**Same stranger triggers repeatedly**
→ Increase `--cooldown` (e.g., 300→600).

**Feishu/Discord/Telegram push not working**
→ Check:
  - Webhook URL / bot token correct?
  - Proxy configured? (Discord/Telegram in mainland China require proxy)
  - Network reachable? (try `curl <webhook_url>` manually)
  - Check `suspicious_person.log` for push error messages

