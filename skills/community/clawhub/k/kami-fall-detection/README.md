# Kami Fall Detection (Cloud)

Detect fall events from RTSP camera streams using the **KamiClaw cloud API**. No local GPU required — all heavy inference runs server-side. Designed for elderly-care monitoring with optional Feishu alarm notifications.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
  - [KamiClaw API Key](#kamiclaw-api-key)
  - [Cameras](#cameras)
  - [Feishu Notifications (Webhook)](#feishu-notifications-webhook)
  - [Full Config Reference](#full-config-reference)
- [Usage](#usage)
- [Output Format](#output-format)
- [Logs](#logs)
- [Exit Codes](#exit-codes)
- [Troubleshooting](#troubleshooting)

---

## Features

- 🚨 **Real-time fall detection** from RTSP camera streams
- ☁️ **Cloud-based inference** — no local GPU or heavy ML libraries needed
- 🔁 **Auto-reconnect** when the RTSP stream drops
- 🎬 **Automatic alarm clip saving** (MP4) on fall events
- 📩 **Feishu webhook notifications** for instant alerts
- 📝 **Structured logs** (JSON Lines) for alarms and transitions
- ⚙️ **Flexible configuration** via `config.json`, CLI args, or environment variables

---

## How It Works

A two-stage pipeline keeps cloud usage low while maintaining high detection quality:

1. **Stage 1 — Local change detection (CPU only)**
   Lightweight frame-differencing on 128×128 grayscale frames. A rolling pre-buffer (default 4s) is maintained. When a significant temporal change is detected, Stage 2 is triggered.

2. **Stage 2 — KamiClaw cloud analysis**
   The skill collects post-transition frames (default 4s), resizes the clip to a 640×360 letterboxed canvas, writes it to a temp MP4, and sends it to the KamiClaw API (`detectType: FALL`, `detectSubType: SK_FALL_DETECTION`). If a fall is detected, a JSON alarm line is emitted and the clip is optionally saved.

3. **Auto-reconnect**
   If the RTSP stream disconnects, the skill retries every 5 seconds and seamlessly resumes monitoring.

---

## Project Structure

```
kami-fall-detection-cloud/
├── SKILL.md                      # Skill metadata & agent instructions
├── README.md                     # This file
├── config.json                   # Runtime config (api_key, rtsp_url, etc.)
├── fall_detect_cloud_skill.py    # Main entry point
├── feishu_notifier.py            # Feishu webhook/API notification module
├── setup.sh                      # Virtualenv + dependencies installer
└── requirements.txt              # Python dependencies
```

Generated at runtime:

```
logs/
├── app.log                       # Rotating daily application log
├── alarms.jsonl                  # Alarm & clip-analysis events (JSON Lines)
├── transitions.jsonl             # Stage-1 transition events (JSON Lines)
└── clips/                        # Saved alarm MP4 clips
```

---

## Requirements

- **Python 3.8+**
- **OS**: Linux (primary), macOS / Windows supported for development
- **KamiClaw API key** — register at <https://kamiclaw-skill.kamihome.com>
- **RTSP camera** or local video file for input

Python dependencies (installed via `setup.sh`):

- `requests>=2.28.0`
- `opencv-python-headless>=4.7.0`
- `numpy>=1.23.0`

---

## Installation

```bash
bash setup.sh
```

This will:

1. Detect system Python (`python3` → `python` → auto-install via `apt`)
2. Create a `.venv/` virtual environment in the project root
3. Install `requests`, `opencv-python-headless`, and `numpy`

No GPU or heavy ML libraries are required.

---

## Configuration

All runtime parameters live in [`config.json`](./config.json). CLI arguments and environment variables override config values with the following priority:

> **CLI args > environment variables > `config.json` > built-in defaults**

### KamiClaw API Key

1. Register at <https://kamiclaw-skill.kamihome.com>.
2. Copy your API key from the dashboard (format: `sk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`).
3. Set it via one of:
   - `config.json` → `"api_key": "sk_live_..."`
   - CLI: `--api_key sk_live_...`
   - Environment: `export KAMICLAW_API_KEY=sk_live_...`

### Cameras

All RTSP cameras are declared in the `cameras` array. Each entry has just two fields:

```json
{
  "cameras": [
    { "name": "front_door", "rtsp_url": "rtsp://192.168.1.101/live/stream" },
    { "name": "backyard",   "rtsp_url": "rtsp://192.168.1.102/live/stream" }
  ]
}
```

Fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | see rule below | Unique identifier and display label shown in every alarm push and log line. |
| `rtsp_url` | yes | RTSP stream URL (or local video file path) for that camera. |

**Naming rule.**

- **Single camera (one entry):** `name` is optional. If omitted, it defaults to `"default"`.
  ```json
  { "cameras": [ { "rtsp_url": "rtsp://192.168.1.100/live/stream" } ] }
  ```
- **Multiple cameras (two or more entries):** every entry **must** have a unique, non-empty `name` (e.g. `front_door`, `backyard`, `living_room`, `garage`). The skill refuses to start otherwise. The name is what your operator sees on Feishu / Telegram / Discord, so pick something that immediately tells them where the fall happened.

**Onboarding flow.** For each camera you want to monitor:

1. Verify the RTSP URL is reachable (e.g. `ffplay rtsp://...` or VLC).
2. Add an entry to `cameras` with a meaningful `name` and the `rtsp_url`.
3. Run `python fall_detect_cloud_skill.py --list_cameras` to print the resolved list and confirm.

**Concurrency model.** Each camera runs on its own daemon thread; a stream loss on one camera triggers reconnect for that camera only — the others keep monitoring uninterrupted. Pressing `Ctrl+C` signals all workers to stop gracefully.

### Feishu Notifications (Webhook)

Get instant alarm messages in a Feishu group chat.

**Step 1 — Create a Feishu bot in your group**

1. Open the Feishu group chat.
2. Group settings (⋮) → **Add Bot** → **Custom Bot**.
3. Set a name (e.g. `Fall Detection Alert`).
4. Copy the **Webhook URL** — it looks like:
   `https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**Step 2 — Add to `config.json`**

```json
{
  "feishu_webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

Leave the field as `""` to disable Feishu notifications.

---

### Telegram Notifications

1. Create bot via **@BotFather** → get bot token
2. Get chat ID:
   - For private chat: Message the bot, then visit `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - For group: Add bot to group, send a message, use the same URL to get group ID (starts with `-`)
3. Add to `config.json`:
```json
{
  "telegram_bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
  "telegram_chat_id": "123456789"
}
```

> 💡 **Note:** Same config works for both push notifications and (optionally) two-way communication if you run the `telegram-gateway` service.

---

### Discord Notifications

**Option A: Webhook (Push Only)** — Simplest, no bot required

1. Channel Settings (⚙️) → **Integrations** → **Webhooks** → **New Webhook**
2. Copy Webhook URL
3. Add to `config.json`:
```json
{
  "discord_webhook_url": "https://discord.com/api/webhooks/123456789/abcdefghijklmnop"
}
```

**Option B: Bot API (Two-Way Capable)** — Full features

1. Go to https://discord.com/developers/applications
2. Create New Application → Bot → Reset Token (copy it)
3. Enable "Message Content Intent" in Bot settings
4. Invite bot to your server with proper permissions
5. Get channel ID (enable Developer Mode in Discord, right-click channel → Copy ID)
6. Add to `config.json`:
```json
{
  "discord_bot_token": "MTUwNzI2MTY4MTQ1NjExOTgxMQ.G13TXv.xxx",
  "discord_channel_id": "1507263377909481666"
}
```

> ⚠️ **Note:** Bot token + channel ID requires running a gateway service for two-way communication.

---

### Quick Comparison

### Quick Comparison

| Channel | Push Only | Two-Way Capable |
|---------|-----------|----------------|
| **Feishu** | Webhook URL | Group Bot (same config) |
| **Telegram** | Bot Token + Chat ID | + Gateway Service |
| **Discord** | Webhook URL | Bot Token + Channel ID |

> 💡 **Discord:** Use webhook for simple push notifications. Use bot token + channel ID if you want two-way interaction capability.











| Field | Default | Description |
|-------|---------|-------------|
| `api_key` | `""` | KamiClaw API key (sent as `X-API-Key` header) |
| `cameras` | `[]` | Array of `{name, rtsp_url}` entries. Required (must contain at least one entry). For a single entry, `name` is optional and defaults to `"default"`; for multiple entries each must have a unique non-empty `name`. |
| `run_time` | `0` | Max run time in seconds; `0` = unlimited |
| `pre_seconds` | `3.0` | Seconds buffered **before** a transition (applies to every camera) |
| `post_seconds` | `3.0` | Seconds collected **after** a transition (applies to every camera) |
| `save_alarm_clips` | `true` | Save alarm video clips to `logs/clips/` |
| `feishu_webhook_url` | `""` | Feishu webhook URL (push notifications) |
| `telegram_bot_token` | `""` | Telegram bot token |
| `telegram_chat_id` | `""` | Telegram chat ID |
| `discord_webhook_url` | `""` | Discord webhook URL (push notifications) |
| `discord_bot_token` | `""` | Discord bot token (two-way capable) |
| `discord_channel_id` | `""` | Discord channel ID (for bot) |

---

## Usage

**Run with config.json only:**

```bash
.venv/bin/python fall_detect_cloud_skill.py
```

**Override via CLI arguments:**

```bash
.venv/bin/python fall_detect_cloud_skill.py \
    --api_key sk_live_xxxxxxxx \
    --pre_seconds 4 \
    --post_seconds 4 \
    --run_time 0
```

Cameras are always declared in `config.json` under the `cameras` array — there is no CLI flag for the RTSP URL.

The skill runs continuously and prints a JSON alarm line to **stdout** for every detected fall. It does **not** stop after an alarm — it resets state and keeps monitoring. Stream disconnects are handled automatically via auto-reconnect.

---

## Output Format

Each fall alarm is emitted as a single-line JSON object on stdout:

```json
{
  "alarm": true,
  "type": "fall",
  "camera_name": "front_door",
  "fall_type": "active_falling",
  "num_persons": 1,
  "confidence": 0.92,
  "reason": "Person collapsed from standing to floor near bed",
  "frame": 87,
  "source": "rtsp://192.168.1.101/live/stream",
  "clip": "logs/clips/alarm_fall_20260429_143201.mp4"
}
```

The `camera_name` field is populated for every alarm and is rendered into every push notification (Feishu, Telegram, Discord) so the operator immediately sees which location triggered.

When `run_time` is reached without any detected fall:

```json
{
  "alarm": false,
  "type": null,
  "detail": "Run time limit reached, no fall detected",
  "frames_processed": 3600,
  "source": "rtsp://192.168.1.100/live/stream"
}
```

`fall_type` values: `"active_falling"` (visible transition) or `"fallen_posture"` (person at floor level in a fallen pose).

---

## Logs

All logs are written under `logs/`:

| File | Format | Content |
|------|--------|---------|
| `logs/app.log` | Human-readable | Application log (rotates daily, keeps 30 days) |
| `logs/alarms.jsonl` | JSON Lines | Every alarm + every clip analysis result |
| `logs/transitions.jsonl` | JSON Lines | Every Stage-1 transition event |
| `logs/clips/` | MP4 | Saved alarm video clips (when `save_alarm_clips=true`) |

**alarms.jsonl — alarm entry:**

```json
{"event": "alarm", "alarm": true, "type": "fall", "fall_type": "active_falling", "num_persons": 1, "confidence": 0.92, "reason": "...", "frame": 87, "source": "rtsp://...", "_ts": "2026-04-27T14:33:15+0800"}
```

**alarms.jsonl — clip analyzed, no alarm:**

```json
{"event": "clip_analyzed", "frame": 120, "source": "rtsp://...", "fall_detected": false, "confidence": 0.97, "reason": "...", "_ts": "2026-04-27T14:33:15+0800"}
```

**transitions.jsonl:**

```json
{"event": "transition", "frame": 83, "source": "rtsp://...", "_ts": "2026-04-27T14:31:58+0800"}
```

**Quick analysis tips:**

```bash
# Count alarms today
grep '"alarm"' logs/alarms.jsonl | grep "$(date +%Y-%m-%d)" | wc -l

# Compare transitions vs alarms (false-positive rate)
wc -l logs/transitions.jsonl logs/alarms.jsonl
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0`  | Run time limit reached (normal exit) |
| `1`  | Invalid API key, missing config, or fatal error |

---

## Troubleshooting

- **`KamiClaw API key required`** — Provide it via `--api_key`, `KAMICLAW_API_KEY`, or `config.json`.
- **`No cameras configured`** — Add at least one entry to `cameras` in `config.json`.
- **`Invalid or expired API key`** — Regenerate the key at <https://kamiclaw-skill.kamihome.com>.
- **`Cannot open stream, retrying...`** — The skill auto-retries every 5 seconds. Verify the RTSP URL and network reachability.
- **Feishu notifications not delivered** — Confirm the webhook URL is complete, the custom bot is enabled in the group, and no IP allowlist/keyword restrictions are blocking the payload.
- **Too many false positives** — Increase `pre_seconds` / `post_seconds` for longer clips, or review `logs/transitions.jsonl` vs `logs/alarms.jsonl` to tune thresholds.
