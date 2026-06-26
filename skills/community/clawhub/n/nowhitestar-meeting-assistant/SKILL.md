---
name: meeting-assistant
description: "Native macOS meeting automation for OpenClaw: calendar/window detection, prompt-before-recording, ScreenCaptureKit system audio + microphone recording, local whisper-cli transcription, and agent-generated meeting notes. No BlackHole or virtual audio device required. Use when you need automatic meeting detection, recording, transcription, and final summaries delivered by an OpenClaw agent."
---

# Meeting Assistant

Native macOS meeting automation for OpenClaw: calendar/window detection → prompt before recording → system audio + microphone recording → local transcription → agent-generated meeting notes.

## Architecture

```text
Google Calendar / Window Detector
          ↓
 schedule.json → scheduler_daemon.py
          ↓
 meeting_daemon.py ask_record
          ↓
 notify.py prompt: Start recording?
          ↓
 record_audio.py → AudioDaemon.app (Unix socket)
          ↓
 ScreenCaptureKit system audio + AVFoundation microphone
          ↓
 WAV → transcribe.py → whisper-cli
          ↓
 transcript.txt + summary_request queue
          ↓
 OpenClaw heartbeat agent → final summary.md → user notification
```

## Key Features

- **No BlackHole required** — captures system audio directly with ScreenCaptureKit.
- **Native AudioDaemon** — a signed macOS app bundle for stable TCC privacy permissions.
- **System audio + microphone** — records remote speaker audio and local microphone input.
- **Half-duplex mixing** — prioritize system audio while others speak; fade to microphone during system silence.
- **Meeting detection** — detects Zoom, Tencent Meeting, Google Meet, Feishu/Lark, WeChat calls, and browser-based meetings.
- **Local transcription** — uses `whisper-cli` from whisper.cpp.
- **OpenClaw agent summaries** — transcription writes a `summary_request` into the agent queue; the OpenClaw agent generates the final meeting notes and notifies the user.

## Install

Clone the full repository first. `setup.sh` needs repository files and should not be run via `curl | bash`.

```bash
git clone https://github.com/Nowhitestar/meeting-assistant.git
cd meeting-assistant
bash meeting-assistant/scripts/setup.sh
```

If you are already inside the skill folder that contains `SKILL.md` and `scripts/`, you can run:

```bash
bash scripts/setup.sh
```

The installer will:

1. Check macOS, Homebrew, and Python
2. Install `sox`, `ffmpeg`, `whisper-cpp`, `terminal-notifier`, `gogcli`, and `cloudflared`
3. Create `~/.config/meeting-assistant/config.json`
4. Compile the window scanner and guide Accessibility permission setup
5. Build and sign `AudioDaemon.app`
6. Guide Microphone and Screen & System Audio Recording permissions
7. Optionally configure Google Calendar
8. Install LaunchAgent background services
9. Run basic verification tests

## macOS Permissions

| Component | Permission | Purpose |
|---|---|---|
| `AudioDaemon.app` | Microphone | Record local microphone audio |
| `AudioDaemon.app` | Screen & System Audio Recording | Capture system audio via ScreenCaptureKit |
| `window_scanner` | Accessibility | Read window titles to detect meetings/calls |

If system audio is missing, open:

System Settings → Privacy & Security → **Screen & System Audio Recording** → enable `AudioDaemon.app`.

## Google Calendar and Privacy

Calendar authorization uses `gog`; refresh tokens are stored in the system Keychain. The repository and skill package must never contain real `client_secret*.json`, refresh tokens, API keys, or personal calendar IDs.

Recommended setup:

```bash
# 1. In Google Cloud Console, enable Calendar API and create a Desktop OAuth client.
# 2. Download the JSON locally.
# 3. Import credentials and authorize Calendar access.
gog auth credentials ~/Downloads/client_secret_xxx.json
gog auth add your.email@example.com --services calendar
gog auth list
# 4. After auth succeeds, delete the Downloads copy of client_secret_xxx.json.
```

Then enable Google Calendar in `~/.config/meeting-assistant/config.json`:

```json
{
  "calendars": [
    {
      "type": "google",
      "enabled": true,
      "gog_account": "your.email@example.com",
      "watch_calendars": ["primary"]
    }
  ]
}
```

If credentials were ever posted in chat or committed publicly: delete the OAuth client, revoke the token, create a fresh client, and authorize again.

## Configuration

Config path: `~/.config/meeting-assistant/config.json`

Key fields:

```json
{
  "audio": {
    "backend": "daemon",
    "output_dir": "/path/to/meeting-assistant/meeting-recordings",
    "silence_threshold": 0.01,
    "silence_duration_sec": 300,
    "half_duplex": true
  },
  "transcription": {
    "whisper_cli": "whisper-cli",
    "local_model_path": "~/Models/whisper/ggml-medium.bin",
    "language": "zh"
  },
  "llm": {
    "enabled": true
  }
}
```

Notes:

- `audio.backend=daemon` is the recommended default and does not require BlackHole.
- `mic_device` / `system_audio_device` are only for the legacy SoX fallback path.
- If no external LLM command is configured, summaries are delegated to the OpenClaw agent queue.

## Scripts

All scripts live under `scripts/`:

| Script | Purpose |
|---|---|
| `setup.sh` | Interactive installer |
| `AudioDaemon.app/` | Native signed audio daemon app |
| `audio_daemon.swift` | ScreenCaptureKit + AVFoundation + Unix socket |
| `build_audio_daemon.sh` | Build and sign AudioDaemon |
| `record_audio.py` | Recording control (`start` / `stop` / `status`) |
| `meeting_daemon.py` | Recording workflow control |
| `scheduler_daemon.py` | Meeting scheduler daemon |
| `meeting_detector.py` | Meeting window detector |
| `window_scanner.swift` | Accessibility window scanner |
| `recorder_status.swift` | Floating recording status window |
| `transcribe.py` | whisper transcription + agent queue summary request |
| `agent_notify.py` | OpenClaw agent queue writer |
| `notify.py` | macOS notifications/prompts |
| `check_meetings.py` | Calendar queries |
| `send_summary.py` | Optional Telegram/Zulip/Notion output |
| `webhook_server.py` | Deprecated fallback Google Calendar webhook server |
| `run_calendar_services.py` | Google Calendar webhook + cloudflared tunnel service |
| `summary_template.md` | Meeting notes template |
| `config.example.json` | Example config |
| `com.meetingassistant.*.plist` | LaunchAgent definitions |

## Manual Commands

```bash
# AudioDaemon status
echo '{"action":"status"}' | nc -w 2 -U ~/.config/meeting-assistant/audio_daemon.sock

# Manual recording
python3 scripts/record_audio.py start "Test Meeting"
python3 scripts/record_audio.py stop

# Prompt-based recording flow
python3 scripts/meeting_daemon.py ask_record "Test Meeting" "manual-test"

# Transcribe WAV
python3 scripts/transcribe.py /path/to/meeting-recordings/xxx.wav

# Calendar
python3 scripts/check_meetings.py today
python3 scripts/check_meetings.py upcoming
python3 scripts/check_meetings.py week --json

# Window detection
python3 scripts/meeting_detector.py once
python3 scripts/meeting_detector.py daemon
```

## Troubleshooting

### AudioDaemon has no system audio

```bash
echo '{"action":"status"}' | nc -w 2 -U ~/.config/meeting-assistant/audio_daemon.sock
```

If `sysReady=false`:

1. Open System Settings → Privacy & Security → Screen & System Audio Recording
2. Enable `AudioDaemon.app`
3. Restart AudioDaemon:

```bash
pkill -f audio_daemon
open scripts/AudioDaemon.app
```

### WAV exists but is silent

Usually this is a TCC permission issue or the daemon is not ready. Newer versions refuse to start recording when `sysReady` / `micReady` is false to avoid fake silent WAVs.

### Summary is still a draft

Check the queue:

```bash
cat ~/.config/meeting-assistant/agent-queue.json
```

If there is a `summary_request`, the OpenClaw heartbeat agent will read the transcript and template, overwrite the final summary, and notify the user.

---

# 中文说明

这是一个 macOS 原生会议助手：日历/窗口检测 → 弹窗询问 → 录制系统音频 + 麦克风 → 本地转录 → OpenClaw agent 生成会议纪要。

核心特点：不需要 BlackHole；通过 ScreenCaptureKit 直接捕获系统音频；用 whisper-cli 本地转写；通过 OpenClaw agent queue 生成最终纪要。

快速安装：

```bash
git clone https://github.com/Nowhitestar/meeting-assistant.git
cd meeting-assistant
bash meeting-assistant/scripts/setup.sh
```

Google Calendar 授权使用 `gog`，refresh token 存在系统 Keychain。不要把 `client_secret*.json`、refresh token、API key 或个人日历 ID 提交到公开仓库。
