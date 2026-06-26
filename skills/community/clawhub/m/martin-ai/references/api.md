# SkillBoss API Hub — API Reference

**Base URL:** `https://api.skillbossai.com/v1`

**Authentication:** All requests require `Authorization: Bearer <SKILLBOSS_API_KEY>`

SkillBoss API Hub uses a **single unified endpoint** `/v1/pilot` that automatically routes to the best available model. All capabilities — chat, image, video, audio, embeddings, search — are accessed through this one endpoint.

---

## /v1/pilot — Unified Routing (Recommended)

```
POST /pilot
```

All AI capabilities use this endpoint with a `type` field to specify the operation.

### Chat (LLM Text Generation)

**Request:**
```json
{
  "type": "chat",
  "inputs": {
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 4096,
    "response_format": {"type": "json_object"}
  },
  "prefer": "balanced"
}
```

**Response:**
```json
{
  "data": {
    "result": {
      "choices": [{
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "Hello! How can I help?"
        },
        "finish_reason": "stop"
      }],
      "usage": {
        "prompt_tokens": 15,
        "completion_tokens": 8,
        "total_tokens": 23
      }
    }
  }
}
```

**Result path:** `data.result.choices[0].message.content`

**`prefer` options:** `"price"` | `"quality"` | `"balanced"`

---

### Embeddings

**Request:**
```json
{
  "type": "embedding",
  "inputs": {
    "text": "Your text here"
  }
}
```

Or batch: `"text": ["text1", "text2", "text3"]`

**Response:**
```json
{
  "data": {
    "result": {
      "data": [{"index": 0, "embedding": [0.123, -0.456, ...], "object": "embedding"}],
      "usage": {"prompt_tokens": 5, "total_tokens": 5}
    }
  }
}
```

**Result path:** `data.result.data[0].embedding`

---

### Text-to-Speech (TTS)

**Request:**
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

**Response:**
```json
{
  "data": {
    "result": {
      "audio_url": "https://..."
    }
  }
}
```

**Result path:** `data.result.audio_url`

---

### Speech-to-Text (STT)

**Request:**
```json
{
  "type": "stt",
  "inputs": {
    "audio_data": "<base64-encoded-audio>",
    "filename": "audio.mp3"
  }
}
```

**Response:**
```json
{
  "data": {
    "result": {
      "text": "Transcribed text here..."
    }
  }
}
```

**Result path:** `data.result.text`

---

### Image Generation

**Request:**
```json
{
  "type": "image",
  "inputs": {
    "prompt": "A sunset over mountains",
    "width": 1024,
    "height": 1024,
    "negative_prompt": "blurry",
    "seed": 12345
  },
  "prefer": "quality"
}
```

**Response:**
```json
{
  "data": {
    "result": {
      "image_url": "https://..."
    }
  }
}
```

**Result path:** `data.result.image_url`

---

### Video Generation

**Request:**
```json
{
  "type": "video",
  "inputs": {
    "prompt": "A cat playing piano",
    "duration": 5,
    "resolution": "720p"
  }
}
```

**Response:**
```json
{
  "data": {
    "result": {
      "video_url": "https://..."
    }
  }
}
```

**Result path:** `data.result.video_url`

---

### Web Search

**Request:**
```json
{
  "type": "search",
  "inputs": {
    "query": "latest AI news"
  },
  "prefer": "balanced"
}
```

**Result path:** `data.result`

---

### Web Scraping

**Request:**
```json
{
  "type": "scraping",
  "inputs": {
    "url": "https://example.com"
  }
}
```

**Result path:** `data.result`

---

## /v1/pilot — Discover Mode

```json
{
  "discover": true,
  "keyword": "optional search term"
}
```

Returns all supported capability types.

---

## /v1/pilot — Recommend Mode

```json
{
  "type": "chat",
  "prefer": "quality",
  "limit": 3,
  "include_docs": true
}
```

Returns recommended models for the given type.

---

## Response Format Summary

| Capability | type | Result Path |
|-----------|------|------------|
| LLM Chat | `chat` | `data.result.choices[0].message.content` |
| Image Generation | `image` | `data.result.image_url` |
| TTS | `tts` | `data.result.audio_url` |
| STT | `stt` | `data.result.text` |
| Embeddings | `embedding` | `data.result.data[0].embedding` |
| Video | `video` | `data.result.video_url` |
| Search | `search` | `data.result` |
| Scraping | `scraping` | `data.result` |

---

## Pricing

Pricing is automatically optimized based on the `prefer` field:
- `"price"` — lowest cost model for the task
- `"balanced"` — balance of cost and quality
- `"quality"` — highest quality model for the task

For detailed pricing, use Discover mode or visit [skillbossai.com](https://skillbossai.com).

---

## Resources

- **Docs:** https://skillbossai.com/docs
- **API Hub:** https://api.skillbossai.com
