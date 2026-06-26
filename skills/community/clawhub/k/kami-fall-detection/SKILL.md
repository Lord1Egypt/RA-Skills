---
name: kami-fall-detection-cloud
description: Detect fall events from RTSP camera streams using KamiClaw cloud API. No local GPU needed.
version: 1.0.9
author: kami-smarthome
tags:
 - smart-home
 - fall-detection
 - elderly-care
 - cloud-ai
 - rtsp
 - camera
triggers:
 - detect fall
 - fall detection cloud
 - check for falls
 - monitor elderly
 - cloud fall detection
 - home assistant
 - smart home
metadata:
 openclaw:
  requires:
   bins:
   - python3
   - ffmpeg
   env:
   - KAMICLAW_API_KEY
  primaryEnv: KAMICLAW_API_KEY
  emoji: "🚨"
  hardware:
   cpu: "4+ cores (x86_64 / ARM64)"
   memory: "8 GB+"
   storage: "20 GB+"
   gpu: "optional (speed up ONNX inference)"
   network:
   - "RTSP camera access (LAN)"
   - "Internet (KamiClaw API)"
   devices:
   - "RTSP IP camera"
---

# Kami Fall Detection (Cloud)

Detect fall events from RTSP camera streams using the KamiClaw cloud API. No local GPU needed — all inference runs server-side.

---

## 🚀 Quick Start

1. **Get API key** → https://kamiclaw-skill.kamihome.com (200 free credits for new users)
2. **Tell the agent**: Your API key + RTSP camera URL
3. **Choose notifications**: Feishu / Telegram / Discord (any combination)
4. **Agent configures everything** automatically
5. **Run!** → Monitors 24/7, alerts instantly on fall detection

---

## What It Does

- 🎥 Monitors RTSP camera streams continuously
- 🧠 Uses cloud AI to detect fall events (active falling, fallen posture, etc.)
- 📱 Sends instant notifications via Feishu, Telegram, or Discord
- 💾 Saves alarm video clips for review (optional)
- 🔄 Auto-reconnects if stream drops

---

## 🔒 Privacy & Data Policy

**In short:** Only 8-second alarm clips are sent to the cloud for AI analysis. No continuous streaming, no audio, no full video.

| What | Local | Cloud |
|------|-------|-------|
| Video stream / file | ✅ Processed locally | ❌ Never sent |
| 8-second alarm clips | ✅ Saved (optional) | ✅ Sent for AI analysis |
| Audio | ❌ Not collected | ❌ Not collected |

> 📄 **Full details:** Read our [Privacy Policy](https://kamiclaw-skill.kamihome.com/privacy) for complete information on data handling, retention, and your rights.

### Quick Tips

- **Disable local storage:** Set `save_alarm_clips: false` to not save clips locally
- **Clean up old files:** `find logs/clips/ -type f -mtime +30 -delete`
- **Protect your API key:** Never commit `config.json` to git

> ℹ️ AI analysis requires sending alarm clips to the cloud API. Processed clips are retained per the provider's data retention policy.

---

## Configuration

All settings are in `config.json`. The agent auto-fills this when you provide values in chat.

### Essential Settings

| Field | Default | Description |
|-------|---------|-------------|
| `api_key` | `""` | **Required.** KamiClaw API key |
| `cameras` | `[]` | **Required.** Array of `{name, rtsp_url}` entries. Single entry: `name` optional, defaults to `"default"`. Two or more entries: every entry must have a unique non-empty `name`. |
| `save_alarm_clips` | `true` | Save alarm video clips to `logs/clips/` |
| `feishu_webhook_url` | `""` | Feishu webhook URL for alarm notifications |
| `telegram_bot_token` | `""` | Telegram bot token for alarm notifications |
| `telegram_chat_id` | `""` | Telegram chat ID (user or group) |
| `discord_webhook_url` | `""` | Discord webhook URL (push notifications) |
| `discord_bot_token` | `""` | Discord bot token (two-way capable) |
| `discord_channel_id` | `""` | Discord channel ID (for bot) |

### Camera Setup

All cameras are declared in the `cameras` array. Each entry has just two fields: `name` and `rtsp_url`.

**Single camera (one entry).** `name` is optional — if omitted it defaults to `"default"`:

```json
{
  "cameras": [
    { "rtsp_url": "rtsp://192.168.1.100/live/stream" }
  ]
}
```

**Multiple cameras (two or more entries).** Every entry **must** have a unique, non-empty `name`. Strongly recommended: pick a meaningful location label so the operator immediately knows which camera triggered.

```json
{
  "cameras": [
    { "name": "front_door", "rtsp_url": "rtsp://192.168.1.101/live/stream" },
    { "name": "backyard",   "rtsp_url": "rtsp://192.168.1.102/live/stream" }
  ]
}
```

- `name` is shown in every Feishu / Telegram / Discord push and tags every log line.
- One worker thread per camera; a single stream loss does not affect the others.
- The skill refuses to start if `cameras` is empty, or if multiple entries are missing/sharing a `name`.

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

### Advanced Settings

| Field | Default | Description |
|-------|---------|-------------|
| `run_time` | `0` | Max run time in seconds; `0` = unlimited |
| `pre_seconds` | `3.0` | Seconds buffered before motion trigger |
| `post_seconds` | `3.0` | Seconds collected after motion trigger |

---

## Notification Setup

Tell the agent which channels you want. They'll guide you through setup.

### Quick Guide

| Channel | Push Only | Two-Way Capable |
|---------|-----------|----------------|
| **Feishu** | Webhook URL | Group Bot (same config) |
| **Telegram** | Bot Token + Chat ID | + Gateway Service |
| **Discord** | Webhook URL | Bot Token + Channel ID |

> 💡 **Discord:** Bot token + channel ID gives you full two-way capability. Webhook is simpler for push-only.

> 💡 **Need help?** Ask OpenClaw for guidance.

---

## Running

```bash
# With config.json (recommended)
.venv/bin/python fall_detect_cloud_skill.py

# Or override the API key on the CLI
.venv/bin/python fall_detect_cloud_skill.py \
    --api_key sk_live_xxxxxxxx
```

Cameras are always declared in `config.json` under the `cameras` array — there is no CLI flag for the RTSP URL.

The skill runs continuously. It does NOT stop after an alarm — it resets and keeps monitoring.

---

## Output Format

**Fall detected:**
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

**Normal exit (run time reached):**
```json
{
  "alarm": false,
  "type": null,
  "detail": "Run time limit reached, no fall detected",
  "frames_processed": 3600,
  "source": "rtsp://192.168.1.100/live/stream"
}
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0`  | Normal exit (run time reached) |
| `1`  | Error (invalid API key, missing config, etc.) |

---

## Advanced: How It Works

<details>
<summary>Click to expand technical details</summary>

### Stage 1 — Change Detection (Local, CPU-only)
- Lightweight frame-differencing on 128×128 grayscale
- Maintains rolling pre-buffer (default 4s)
- Triggers Stage 2 on significant temporal change

### Stage 2 — Cloud Analysis
- Collects post-transition frames (default 4s)
- Resizes clip to 360×360, writes to temp file
- Sends to KamiClaw API (`detectType: FALL`, `detectSubType: SK_FALL_DETECTION`)
- On fall detected: outputs JSON alarm, optionally saves clip, resets to Stage 1

### Auto-Reconnect
- If RTSP stream drops, retries connection every 5 seconds
- Resumes monitoring seamlessly after reconnection

</details>

---

## Agent Setup Flow

**For agents configuring this skill:**

1. Read `config.json` — check whether `api_key` is set and whether `cameras` is a non-empty array.
2. If `api_key` is empty, ask the user: "Please provide your KamiClaw API key. Register at https://kamiclaw-skill.kamihome.com".
3. If `cameras` is empty, ask: "How many RTSP cameras do you want to monitor?"
   - **One camera:** ask only for the RTSP URL. Write `[ { "rtsp_url": "..." } ]` — `name` will default to `"default"` automatically.
   - **Two or more cameras:** for each one, ask both the RTSP URL **and** a unique short location label (e.g. `front_door`, `backyard`, `living_room`). Strongly recommend the user picks meaningful labels — they are shown in every alarm notification. Write `[ { "name": "front_door", "rtsp_url": "..." }, { "name": "backyard", "rtsp_url": "..." } ]`.
4. Ask: "Save alarm video clips? (yes/no, default: yes)" → set `save_alarm_clips`.
5. Ask about each notification channel (Feishu / Telegram / Discord) — guide setup if yes.
6. Write all values to `config.json` (read existing, merge, write back).
7. Optionally run `python fall_detect_cloud_skill.py --list_cameras` to confirm the resolved camera list.
8. Run the skill.

**Never run with an empty `api_key`. Never run with `cameras` empty. When the user has multiple cameras, never accept missing/duplicate names — re-prompt until each camera has a unique label. Never ask the user to manually edit config.json.**

---

## Troubleshooting & Analysis

### Log Files

| File | Content |
|------|---------|
| `logs/app.log` | Application log (rotates daily, keeps 30 days) |
| `logs/alarms.jsonl` | All alarm events + clip analysis results |
| `logs/transitions.jsonl` | All motion trigger events |

### Quick Analysis Commands

```bash
# Count alarms today
grep '"alarm"' logs/alarms.jsonl | grep "$(date +%Y-%m-%d)" | wc -l

# Transitions vs alarms (false positive rate)
wc -l logs/transitions.jsonl logs/alarms.jsonl

# Export alarms as CSV
cat logs/alarms.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    obj = json.loads(line)
    if obj.get('event') == 'alarm':
        print(f\"{obj['_ts']},{obj.get('type','')},{obj.get('fall_type','')},{obj.get('confidence',0)},{obj.get('frame',0)}\")
"
```

### Common Issues

| Issue | Solution |
|-------|----------|
| No alarms detected | Check RTSP stream is active; verify camera angle covers monitoring area |
| Too many false alarms | Adjust camera position; reduce motion sensitivity area |
| API errors | Verify API key is valid; check internet connection |
| Stream disconnects | Check network stability; camera may need reboot |

---

## File Structure

```
kami-fall-detection/
├── SKILL.md                      # Documentation
├── config.json                   # Configuration (auto-managed by agent)
├── fall_detect_cloud_skill.py    # Production entry point
├── setup.sh                      # Installer
└── requirements.txt              # Dependencies
```
