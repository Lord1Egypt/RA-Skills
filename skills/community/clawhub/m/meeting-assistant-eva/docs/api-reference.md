# API Reference

## Vexa REST API

Base URL: `http://localhost:8056`
Authentication: `X-API-Key: dGosC39FSoaw0UpIVdhroaz42heFR0ou4bC5yiIc`

**Critical**: Use `X-API-Key` header, NOT `Authorization: Bearer`.

---

### Bots

#### POST /bots — Join Meeting
```json
// Request
{
  "platform": "google_meet",        // "google_meet" | "zoom" | "teams"
  "native_meeting_id": "abc-def-ghi", // extracted from meeting URL
  "bot_name": "OpenClaw Assistant",
  "language": "zh"                  // transcription language hint
}

// Response 201
{
  "id": 7,
  "platform": "google_meet",
  "native_meeting_id": "pmn-eatb-cyf",
  "status": "requested",            // → joining → awaiting_admission → active | failed
  "bot_container_id": "c724c8b7",
  "created_at": "2026-03-14T04:35:00Z"
}
```

Status lifecycle: `requested → joining → awaiting_admission → active → completed | failed`

#### DELETE /bots/{platform}/{native_meeting_id} — Leave Meeting
```
DELETE /bots/google_meet/pmn-eatb-cyf
Response 200: {"message": "Stop request accepted and is being processed."}
```

#### GET /bots/status — List Running Bots
```json
// Response 200
{"running_bots": []}
```

---

### Meetings

#### GET /meetings — List All Meetings
```json
// Response 200
{
  "meetings": [{
    "id": 7,
    "platform": "google_meet",
    "native_meeting_id": "pmn-eatb-cyf",
    "status": "active",
    "start_time": "2026-03-14T04:35:00Z",
    "end_time": null,
    "data": {
      "recordings": [...],
      "status_transition": [...]
    }
  }]
}
```

---

### Chat

#### POST /bots/{platform}/{id}/chat — Send Chat Message
```json
// Request — IMPORTANT: field is "text", NOT "message"
{"text": "Hello from the bot!"}

// Response 202
{"message": "Chat message sent", "meeting_id": 7}
```

**Encoding**: Always send as UTF-8. Use Python `requests` with
`json.dumps(..., ensure_ascii=False).encode("utf-8")` for Chinese text.
PowerShell `Invoke-WebRequest` garbles non-ASCII unless explicitly encoded.

#### GET /bots/{platform}/{id}/chat — Read Chat Messages
```json
// Response 200
{
  "messages": [
    {
      "sender": "Zero G",
      "text": "你好",
      "timestamp": 1773460975107,
      "is_from_bot": false
    },
    {
      "sender": "OpenClaw Assistant",
      "text": "你好！",
      "timestamp": 1773461026833,
      "is_from_bot": true
    }
  ],
  "meeting_id": 7
}
```

---

### Transcripts

#### GET /transcripts/{platform}/{id} — Get Transcript
```json
// Response 200
{
  "id": 7,
  "platform": "google_meet",
  "status": "active",
  "start_time": "2026-03-14T04:35:00Z",
  "segments": [
    {
      "speaker": "Zero G",
      "text": "这是测试",
      "created_at": "2026-03-14T04:36:00Z"
    }
  ],
  "recordings": [{
    "id": 470635713526,
    "status": "in_progress",
    "media_files": [{
      "type": "audio",
      "format": "wav",
      "duration_seconds": 180.6,
      "file_size_bytes": 5780584
    }]
  }]
}
```

**Note**: `segments` is populated only when a participant's **microphone** is active
and audio is transcribed by Whisper. Screen-share system audio is NOT captured.

---

### Recordings

#### GET /recordings — List Recordings
```json
{
  "recordings": [{
    "id": 470635713526,
    "meeting_id": 7,
    "status": "in_progress",
    "media_files": [{
      "id": 531961809228,
      "type": "audio",
      "format": "wav",
      "duration_seconds": 180.6,
      "file_size_bytes": 5780584
    }]
  }]
}
```

#### GET /recordings/{id}/media/{media_id}/download — Get Download URL
```json
{
  "download_url": "/recordings/.../raw",
  "filename": "audio.wav",
  "content_type": "audio/wav",
  "file_size_bytes": 5780584
}
```

#### GET /recordings/{id}/media/{media_id}/raw — Download Raw File
Returns binary audio file (WAV). Only available for recordings in current container run.

---

### Screen (Bot Output Only)

#### POST /bots/{platform}/{id}/screen — Bot Presents Content to Meeting
```json
// Request
{
  "type": "url",       // "url" | "image" | "html"
  "url": "https://example.com",
  "start_share": true
}
```
This makes the **bot** share its screen to the meeting. It does NOT capture
what the user is sharing.

#### DELETE /bots/{platform}/{id}/screen — Stop Bot's Screen Share

---

### Voice/TTS

#### POST /bots/{platform}/{id}/speak — Bot Speaks in Meeting
```json
{"text": "Hello, I have an important update."}
```
Triggers TTS so the bot speaks aloud in the meeting.

---

## Whisper API (via Proxy)

Base URL: `http://localhost:8000`
(proxied through `whisper-proxy` container which rewrites model parameter)

#### POST /v1/audio/transcriptions
```
Content-Type: multipart/form-data

file=<audio.wav>
model=default          ← proxy rewrites this to Systran/faster-whisper-base
language=zh            ← optional
```

Response:
```json
{"text": "转录的文字内容"}
```

---

## Python Client Classes

### `MeetingBot`
Location: `scripts/meeting_bot.py`

```python
from scripts.meeting_bot import MeetingBot

bot = MeetingBot()           # loads config.json automatically
bot.join("https://meet.google.com/abc-def-ghi")
bot.send_chat("Hello!")
messages = bot.read_chat()
segments = bot.get_transcript()
bot.leave()
```

Key methods:
| Method | Description |
|---|---|
| `join(url, bot_name=None, language=None)` | Parse URL + POST /bots |
| `leave()` | DELETE /bots/{platform}/{id} |
| `status()` | GET /bots/status |
| `send_chat(message)` | POST /bots/{p}/{id}/chat with `{"text": message}` |
| `read_chat()` | GET /bots/{p}/{id}/chat → list of messages |
| `get_transcript(since=None)` | GET /transcripts/{p}/{id} → segments list |
| `get_full_transcript_text()` | Formatted string of all transcript entries |

### `MeetingAssistantLoop`
Location: `scripts/meeting_bot.py`

```python
from scripts.meeting_bot import MeetingBot, MeetingAssistantLoop

bot = MeetingBot()
assistant = MeetingAssistantLoop(bot)
assistant.start("https://meet.google.com/abc-def-ghi", mode="general", interval=30)
# Blocks until KeyboardInterrupt or assistant.stop()
```

### `MeetingClaudeClient`
Location: `scripts/claude_client.py`

```python
from scripts.claude_client import MeetingClaudeClient

client = MeetingClaudeClient(config)
analysis = client.analyze_meeting_state(
    screenshot_path="/path/to/screen.png",
    transcript_entries=[{"speaker": "A", "text": "..."}],
    mode="general"
)
# Returns: {"analysis": "...", "chat_message": "..." or None}

reply = client.respond_to_chat(
    user_message="What was decided?",
    sender="Zero G",
    context_screenshot=None,
    mode="general"
)
# Returns: str reply text

summary = client.generate_final_summary(session_dir, mode="general")
# Returns: markdown summary string
```

### `MeetingAssistantTool`
Location: `scripts/agent_tool.py`

High-level tool interface for use as a Claude Code tool:

```python
from scripts.agent_tool import MeetingAssistantTool

tool = MeetingAssistantTool()
print(tool.tool_definitions())  # returns Anthropic tool_use format

result = tool.handle_tool_call("meeting_start", {
    "meeting_url": "https://meet.google.com/abc-def-ghi",
    "mode": "general"
})
```
