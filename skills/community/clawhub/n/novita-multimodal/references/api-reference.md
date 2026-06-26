# API Reference

## Base Configuration

| Item | Value |
|------|-------|
| Base URL | `https://api.novita.ai` |
| Auth Header | `Authorization: Bearer <API_KEY>` |
| Content-Type | `application/json` |

## Get API Key

https://novita.ai/settings/key-management

## Model Catalog

https://novita.ai/models

## Pricing

https://novita.ai/pricing

| Model | Price |
|-------|-------|
| Seedream 5.0 Lite | $0.035/image |
| Vidu Q3 Pro | $0.0179-0.1429/second |
| MiniMax Speech 2.8 | $60-100/1M characters |
| GLM ASR | $0.021/Mt |

---

## Text-to-Image

**POST** `/v3/seedream-5.0-lite`

### Request

```json
{
  "prompt": "A cute cat sitting on a windowsill"
}
```

### Response

```json
{
  "images": [
    {
      "url": "https://..."
    }
  ]
}
```

---

## Image Editing

**POST** `/v3/seedream-5.0-lite`

### Request

```json
{
  "prompt": "Convert to oil painting style",
  "reference_images": ["https://example.com/image.jpg"]
}
```

### Response

```json
{
  "images": [
    {
      "url": "https://..."
    }
  ]
}
```

---

## Text-to-Video (Async)

**POST** `/v3/async/vidu-q3-pro-t2v`

### Request

```json
{
  "prompt": "Ocean waves crashing on beach at sunset",
  "duration": 4
}
```

### Response

```json
{
  "task_id": "xxx-xxx-xxx"
}
```

---

## Image-to-Video (Async)

**POST** `/v3/async/vidu-q3-pro-i2v`

### Request

```json
{
  "prompt": "Gentle camera pan with wind blowing",
  "images": ["https://example.com/image.jpg"]
}
```

### Response

```json
{
  "task_id": "xxx-xxx-xxx"
}
```

---

## TTS - Text to Speech (Async)

**POST** `/v3/async/minimax-speech-2.8-turbo`

### Request

```json
{
  "text": "Hello, welcome to Novita AI",
  "voice_setting": {
    "voice_id": "male-qn-qingse",
    "speed": 1.0
  },
  "audio_setting": {
    "format": "mp3"
  }
}
```

### Available Voices

| Voice ID | Description |
|----------|-------------|
| `male-qn-qingse` | Male, youthful |
| `male-qn-jingying` | Male, professional |
| `female-shaonv` | Female, young |
| `female-yujie` | Female, mature |

### Response

```json
{
  "task_id": "xxx-xxx-xxx"
}
```

---

## STT - Speech to Text

**POST** `/v3/glm-asr`

### Request

```json
{
  "file": "https://example.com/audio.mp3"
}
```

**Note:** `file` accepts audio URL or Base64 encoded string. Supported formats: .wav, .mp3. Max size: 25MB, max duration: 30 seconds.

### Response

```json
{
  "text": "Transcribed text content"
}
```

---

## Task Result Query

**GET** `/v3/async/task-result?task_id={task_id}`

### Response

```json
{
  "task_id": "xxx",
  "status": "TASK_STATUS_SUCCEED",
  "output": {
    "video_url": "https://..."
  }
}
```

### Status Values

| Status | Meaning |
|--------|---------|
| `TASK_STATUS_QUEUED` | Queued |
| `TASK_STATUS_PROCESSING` | Processing |
| `TASK_STATUS_SUCCEED` | Completed |
| `TASK_STATUS_FAILED` | Failed |

---

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Invalid request | Check parameters |
| 401 | Unauthorized | Check API Key |
| 402 | Insufficient balance | Top up at https://novita.ai/billing |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Retry later |

---

## Support

- Console: https://novita.ai/console
- Discord: https://discord.gg/novita
- Documentation: https://docs.novita.ai
