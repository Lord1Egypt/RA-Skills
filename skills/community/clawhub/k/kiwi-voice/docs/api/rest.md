# REST API

Base URL: `http://localhost:7789`

All endpoints return JSON. The API is served by the same aiohttp server as the dashboard.

## Status & Config

### `GET /api/status`

Returns current service state and metrics.

```json
{
  "state": "LISTENING",
  "language": "en",
  "tts_provider": "kokoro",
  "is_speaking": false,
  "is_processing": false,
  "is_running": true,
  "uptime_seconds": 3600,
  "active_speaker": "Owner",
  "active_soul": "default",
  "homeassistant_connected": true
}
```

### `GET /api/config`

Returns current configuration (safe fields only, no secrets).

```json
{
  "language": "en",
  "tts_provider": "kokoro",
  "tts_qwen_backend": "local",
  "tts_voice": "af_heart",
  "stt_model": "large",
  "stt_device": "cuda",
  "wake_word": "kiwi",
  "wake_word_engine": "openwakeword"
}
```

### `PATCH /api/config`

Update configuration at runtime.

**Request:**

```json
{
  "language": "ru",
  "wake_word": "jarvis",
  "tts_default_style": "cheerful"
}
```

**Response:**

```json
{"updated": {"language": "ru"}}
```

---

## Speakers

### `GET /api/speakers`

List all known speaker profiles.

```json
{
  "speakers": [
    {
      "id": "spk_001",
      "name": "Owner",
      "priority": 0,
      "is_blocked": false,
      "auto_learned": false,
      "sample_count": 42,
      "last_seen": "2026-02-25T10:30:00"
    }
  ]
}
```

### `DELETE /api/speakers/{speaker_id}`

Remove a speaker profile.

```json
{"deleted": "spk_001"}
```

### `POST /api/speakers/{speaker_id}/block`

Block a speaker.

```json
{"blocked": "spk_001"}
```

### `POST /api/speakers/{speaker_id}/unblock`

Unblock a speaker.

```json
{"unblocked": "spk_001"}
```

---

## Languages

### `GET /api/languages`

```json
{
  "current": "en",
  "available": ["en", "ru", "es", "pt", "fr", "it", "de", "tr", "pl", "zh", "ja", "ko", "hi", "ar", "id"]
}
```

### `POST /api/language`

Switch language at runtime.

**Request:** `{"language": "ru"}`

**Response:** `{"language": "ru"}`

---

## Souls (Personalities)

### `GET /api/souls`

List all available personalities.

```json
{
  "souls": [
    {"id": "default", "name": "Default", "description": "Balanced assistant", "nsfw": false},
    {"id": "comedian", "name": "Comedian", "description": "Funny and witty", "nsfw": false},
    {"id": "siren", "name": "Siren", "description": "Flirty 18+", "nsfw": true}
  ]
}
```

### `GET /api/soul/current`

```json
{
  "id": "default",
  "name": "Default",
  "description": "...",
  "nsfw": false,
  "model": "claude-sonnet"
}
```

### `POST /api/soul`

Switch personality.

**Request:** `{"soul": "comedian"}`

**Response:**

```json
{
  "soul": "comedian",
  "name": "Comedian",
  "nsfw": false,
  "model": "claude-sonnet"
}
```

---

## TTS

### `POST /api/tts/test`

Speak a test phrase through the current TTS provider.

**Request:** `{"text": "Hello, I am Kiwi!"}` (optional — uses default if omitted)

**Response:**

```json
{"status": "speaking", "text": "Hello, I am Kiwi!"}
```

---

## Controls

### `POST /api/stop`

Stop current TTS playback.

```json
{"status": "stopped"}
```

### `POST /api/reset-context`

Reset conversation context (clears LLM history).

```json
{"status": "context_reset"}
```

### `POST /api/restart`

Restart the service.

```json
{"status": "restarting"}
```

### `POST /api/shutdown`

Shutdown the service.

```json
{"status": "shutting_down"}
```

---

## Home Assistant

### `GET /api/homeassistant/status`

```json
{"enabled": true, "connected": true}
```

### `POST /api/homeassistant/command`

Send a voice command to Home Assistant via the Conversation API.

**Request:**

```json
{"text": "turn on bedroom lights", "language": "en"}
```

**Response:**

```json
{
  "response": "Done, bedroom lights are on.",
  "command": "turn on bedroom lights"
}
```

---

## Web Audio

### `WebSocket /api/audio`

Bidirectional audio streaming for the browser microphone. See [Web Microphone](../features/web-microphone.md) for protocol details.
