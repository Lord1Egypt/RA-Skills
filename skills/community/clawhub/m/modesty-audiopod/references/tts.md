# Text to Speech Reference

## API Endpoint

**All requests:** `POST https://api.skillboss.co/v1/pilot`
**Auth:** `Authorization: Bearer $SKILLBOSS_API_KEY`

```json
{
  "type": "tts",
  "inputs": {
    "text": "Hello world",
    "voice": "alloy",
    "speed": 1.0
  },
  "prefer": "balanced"
}
```

## Generate Parameters

| Field | Required | Description |
|-------|----------|-------------|
| text | yes | Text to speak (max 5000 chars) |
| voice | no | Voice name or ID (e.g. `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`) |
| speed | no | 0.25 - 4.0 (default: 1.0) |
| language | no | ISO code, auto-detected if omitted |

## Voice Types

- **50+ production-ready voices** — multilingual, supporting 60+ languages with auto-detection
- **Custom clones** — request via SkillBoss API Hub with voice sample

## Voice Identification

Voices can be referenced by name: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

## Response Format

```python
result = pilot({"type": "tts", "inputs": {"text": "Hello world", "voice": "alloy"}, "prefer": "balanced"})
audio_url = result["data"]["result"]["audio_url"]
```

Response structure:
```json
{
  "data": {
    "result": {
      "audio_url": "https://..."
    }
  }
}
```

Result path: `result["data"]["result"]["audio_url"]`
