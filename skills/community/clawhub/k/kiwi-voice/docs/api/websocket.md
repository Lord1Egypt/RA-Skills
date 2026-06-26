# WebSocket Events

Kiwi exposes a real-time event stream via WebSocket for building custom integrations and UIs.

## Connection

```
ws://localhost:7789/api/events
```

Connect using any WebSocket client. The dashboard uses this endpoint for live updates.

### JavaScript Example

```javascript
const ws = new WebSocket('ws://localhost:7789/api/events');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`[${data.event}]`, data.data);
};
```

### Python Example

```python
import websocket
import json

def on_message(ws, message):
    event = json.loads(message)
    print(f"[{event['event']}] {event.get('data', {})}")

ws = websocket.WebSocketApp(
    "ws://localhost:7789/api/events",
    on_message=on_message
)
ws.run_forever()
```

## Event Format

All events follow the same structure:

```json
{
  "event": "WAKE_WORD_DETECTED",
  "data": {"text": "kiwi"},
  "timestamp": 1709000000.0,
  "source": "listener"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `event` | string | Event type name |
| `data` | object | Event-specific payload |
| `timestamp` | float | Unix timestamp |
| `source` | string | Module that emitted the event |

## Event Types

### Core Pipeline

| Event | Data | Description |
|-------|------|-------------|
| `STATE_CHANGED` | `{"old": "IDLE", "new": "LISTENING"}` | Assistant state transition |
| `WAKE_WORD_DETECTED` | `{"text": "kiwi"}` | Wake word detected |
| `SPEECH_RECOGNIZED` | `{"text": "turn on the lights", "language": "en"}` | STT transcription complete |
| `SPEAKER_IDENTIFIED` | `{"name": "Owner", "priority": 0, "confidence": 0.95}` | Speaker identified by voiceprint |

### LLM

| Event | Data | Description |
|-------|------|-------------|
| `LLM_TOKEN` | `{"token": "Hello"}` | Streaming LLM token |
| `LLM_COMPLETE` | `{"text": "Hello! How can I help?"}` | Full LLM response complete |

### TTS

| Event | Data | Description |
|-------|------|-------------|
| `TTS_STARTED` | `{"text": "Hello!", "provider": "kokoro"}` | TTS playback started |
| `TTS_FINISHED` | `{}` | TTS playback finished |

### Security

| Event | Data | Description |
|-------|------|-------------|
| `APPROVAL_REQUESTED` | `{"speaker": "Guest", "command": "..."}` | Telegram approval requested for voice command |
| `APPROVAL_RESOLVED` | `{"approved": true, "speaker": "Guest"}` | Approval resolved |
| `EXEC_APPROVAL_REQUESTED` | `{"command": "git push", "request_id": "..."}` | OpenClaw exec approval requested |
| `EXEC_APPROVAL_RESOLVED` | `{"approved": true, "request_id": "..."}` | Exec approval resolved |

### Other

| Event | Data | Description |
|-------|------|-------------|
| `SOUL_CHANGED` | `{"soul": "comedian", "name": "Comedian"}` | Personality switched |
| `ERROR` | `{"message": "...", "source": "tts"}` | Error occurred |

## Client Commands

Send JSON messages to the server:

### Ping

```json
{"type": "ping"}
```

Response:

```json
{"event": "pong"}
```

Use this to keep the connection alive or check connectivity.
