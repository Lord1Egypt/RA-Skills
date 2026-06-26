# Agent Usage Guide

This document describes how to use the Meeting Assistant as a Claude Code agent.
The agent joins meetings autonomously, monitors activity, and communicates via meeting chat.

## How It Works

Claude Code IS the agent — no separate AI service is needed. The workflow:

1. You open a Google Meet and share the link with Claude Code
2. Claude Code calls the Vexa API to send the bot into the meeting
3. The bot ("OpenClaw Assistant") joins as a participant
4. You can talk to the bot directly through the meeting's chat panel
5. Claude Code polls chat every 5 seconds and responds with AI analysis

## Joining a Meeting

### Google Meet (Recommended)

```
Give Claude Code the meeting URL:
  https://meet.google.com/xxx-xxxx-xxx

Claude Code will:
  1. Verify Vexa is running
  2. Send POST /bots to join
  3. Wait for status: active
  4. Send a welcome message in the chat
```

### Zoom (Not Currently Working)
Zoom requires native SDK binaries not included in `vexaai/vexa-lite`.
See [Troubleshooting](troubleshooting.md#zoom-sdk-missing).

## Chatting with the Bot

Once the bot is in the meeting, send messages in the Google Meet chat panel.
The bot responds to messages that match any of these triggers:

| Trigger | Example | Bot Action |
|---|---|---|
| Contains `?` or `？` | `What was decided just now?` | AI answer |
| Mentions bot name | `OpenClaw, summarize` | AI response |
| Contains `助手` | `助手你好` | AI response |
| Starts with `/` | `/summary` | AI command |
| Starts with `!` or `！` | `!help` | AI command |
| Starts with `请` or `请问` | `请问这个怎么处理` | AI response |
| Medical keywords (medical mode) | `剂量` `处方` | AI explanation |

Messages from other participants that don't match triggers are silently logged
for context in the analysis loop.

## Analysis Loop

Every 30 seconds (configurable), the bot runs an analysis cycle:

1. **Screenshot** — Attempts to capture meeting screen (currently limited by Vexa)
2. **Transcript delta** — Fetches new speech segments since last cycle
3. **Claude analysis** — If there's new content, Claude analyzes it
4. **Chat suggestion** — If Claude has something useful to share, it sends to chat

## Claude Code Tool Definitions

When used as a Claude Code skill, the following tools are available via `agent_tool.py`:

| Tool | Description |
|---|---|
| `meeting_start` | Join a meeting URL and start the assistant |
| `meeting_stop` | Leave the meeting and generate summary |
| `meeting_status` | Get current bot and meeting status |
| `meeting_send_chat` | Send a chat message to the meeting |
| `meeting_get_transcript` | Get transcript segments |
| `meeting_screenshot` | Attempt to get a meeting screenshot |
| `meeting_read_chat` | Read all chat messages |
| `meeting_get_summary` | Get session summary (post-meeting) |
| `meeting_get_logs` | Get session analysis logs |

## Direct API Usage (Claude Code calling Vexa directly)

Claude Code can also call the Vexa API directly without the Python wrapper.
All calls use the user token in `X-API-Key` header.

### Join a Meeting
```python
import requests

VEXA = "http://localhost:8056"
KEY  = "dGosC39FSoaw0UpIVdhroaz42heFR0ou4bC5yiIc"

resp = requests.post(f"{VEXA}/bots",
    headers={"X-API-Key": KEY},
    json={
        "platform": "google_meet",
        "native_meeting_id": "pmn-eatb-cyf",   # from URL: meet.google.com/{id}
        "bot_name": "OpenClaw Assistant",
        "language": "zh"
    })
bot = resp.json()
print(f"Bot created: id={bot['id']}, status={bot['status']}")
```

### Send Chat Message
```python
# IMPORTANT: field name is "text", NOT "message"
requests.post(f"{VEXA}/bots/google_meet/pmn-eatb-cyf/chat",
    headers={"X-API-Key": KEY, "Content-Type": "application/json; charset=utf-8"},
    data=json.dumps({"text": "你好！我是 OpenClaw 助手。"}, ensure_ascii=False).encode("utf-8"))
```

### Read Chat
```python
resp = requests.get(f"{VEXA}/bots/google_meet/pmn-eatb-cyf/chat",
    headers={"X-API-Key": KEY})
messages = resp.json().get("messages", [])
for msg in messages:
    print(f"{msg['sender']}: {msg['text']}")
```

### Get Transcript
```python
resp = requests.get(f"{VEXA}/transcripts/google_meet/pmn-eatb-cyf",
    headers={"X-API-Key": KEY})
data = resp.json()
for seg in data.get("segments", []):
    print(f"{seg['speaker']}: {seg['text']}")
```

### Leave Meeting
```python
requests.delete(f"{VEXA}/bots/google_meet/pmn-eatb-cyf",
    headers={"X-API-Key": KEY})
```

### Check Bot Status
```python
resp = requests.get(f"{VEXA}/bots/status", headers={"X-API-Key": KEY})
print(resp.json())  # {"running_bots": [...]}
```

## Meeting URL Parsing

The `MeetingBot._parse_meeting_url()` method handles these formats:

| Platform | URL Format | Extracted ID |
|---|---|---|
| Google Meet | `https://meet.google.com/abc-defg-hij` | `abc-defg-hij` |
| Zoom | `https://zoom.us/j/123456789` | `123456789` |
| Zoom (with password) | `https://zoom.us/j/123?pwd=abc` | `123` (passcode stored separately) |
| Teams | `https://teams.microsoft.com/l/meetup-join/...` | full URL |

## Operating Modes

### General Mode (default)
- Standard meeting assistance
- Responds to questions about meeting content
- Summarizes key points
- Tracks decisions and action items

### Medical Mode
```python
assistant.start(url, mode="medical")
```
- Additional focus on medical terminology
- Flags prescriptions, diagnoses, dosages
- Multilingual medical term explanation (zh/en)
- Stricter response triggers for medical keywords

## Session Data

Each session creates a directory under `recordings/bot_{timestamp}/`:

```
recordings/bot_20260314_040142/
├── session.json           # Metadata (URL, mode, start/end time)
├── transcript_log.json    # All transcript segments captured
├── suggestions_log.json   # All messages sent by bot
├── screenshots/           # Screen captures (if available)
└── analysis/
    └── cycle_log.jsonl    # Per-cycle analysis log (JSON Lines)
```

## Configuration

Key settings in `config.json`:

```json
{
  "chat_poll_interval": 5,          // seconds between chat polls
  "screenshot_interval": 30,        // seconds between analysis cycles
  "bot": {
    "vexa_url": "http://localhost:8056",
    "vexa_api_key": "dGosC39FSoaw0UpIVdhroaz42heFR0ou4bC5yiIc",
    "bot_name": "OpenClaw 助手",
    "auto_transcribe": true
  },
  "claude": {
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "analysis_interval_cycles": 1   // analyze every N cycles
  },
  "whisper_language": "zh"
}
```
