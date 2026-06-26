# Memories.ai V2 API — Complete Endpoint Reference

**Base URL:** `https://mavi-backend.memories.ai/serve/api/v2`
**Auth:** `Authorization: <api-key>` (no Bearer prefix)
**Content-Type:** `application/json`
**Docs:** https://api-tools.memories.ai/llms.txt
**OpenAPI:** https://api-tools.memories.ai/api-reference/openapi.json
**Console:** https://api-platform.memories.ai

---

## Social Media — Transcripts

### Simple Transcript (Sync)
Fast audio-to-text. Returns immediately. ~$0.02/video.

| Endpoint | Method |
|----------|--------|
| `/youtube/video/transcript` | POST |
| `/tiktok/video/transcript` | POST |
| `/instagram/video/transcript` | POST |
| `/twitter/video/transcript` | POST |

**Request:**
```json
{
  "video_url": "https://...",
  "channel": "rapid"
}
```
- `channel`: Optional. YouTube recommends `"rapid"` for fastest results.

**Response:**
```json
{
  "code": "0000",
  "data": [
    {
      "data": [
        {"start": "1.48", "dur": "4.84", "text": "..."}
      ]
    }
  ]
}
```
- YouTube returns `start`/`dur` string pairs.
- TikTok returns WebVTT format in `transcript` field.

### MAI Transcript (Async)
AI-powered dual-layer transcription: visual scene descriptions (Gemini VLM) + speech-to-text (Whisper). ~$0.11/40s video.

| Endpoint | Method |
|----------|--------|
| `/youtube/video/mai/transcript` | POST |
| `/tiktok/video/mai/transcript` | POST |
| `/instagram/video/mai/transcript` | POST |
| `/twitter/video/mai/transcript` | POST |

**Request:**
```json
{
  "video_url": "https://...",
  "callback_url": "https://your-webhook.com/callback"
}
```
- `callback_url`: Optional. If omitted, uses project-level default webhook.

**Response:**
```json
{
  "code": "0000",
  "data": {
    "task_id": "abc123..."
  }
}
```

**Webhook Callback Payload:**
```json
{
  "code": "0000",
  "task_id": "abc123...",
  "data": {
    "videoTranscript": {
      "data": {
        "data": [
          {"start_time": 0.0, "end_time": 16.0, "transcript": "Scene description..."}
        ]
      }
    },
    "audioTranscript": {
      "data": {
        "data": [
          {"start_time": 0.0, "end_time": 0.74, "text": "Speech text..."}
        ]
      }
    }
  }
}
```

---

## Social Media — Metadata

Get video details, stats, author info. ~$0.01/call.

| Endpoint | Method |
|----------|--------|
| `/youtube/video/detail` | POST |
| `/tiktok/video/detail` | POST |
| `/instagram/video/detail` | POST |
| `/twitter/video/detail` | POST |

**Request:**
```json
{
  "video_url": "https://..."
}
```
or:
```json
{
  "video_id": "7543017294226558221"
}
```

---

## Social Media — Comments

~$0.01/call.

| Endpoint | Method |
|----------|--------|
| `/youtube/video/comment` | POST |
| `/tiktok/video/comment` | POST |
| `/instagram/video/comment` | POST |
| `/twitter/video/comment` | POST |

**Request:**
```json
{
  "video_id": "...",
  "limit": 100
}
```

---

## Task Status

Poll async task status.

| Endpoint | Method |
|----------|--------|
| `/task/{task_id}` | GET |

**Response:**
```json
{
  "status": "pending | processing | completed | failed",
  "data": { ... },
  "error": "..."
}
```

---

## Embeddings

### Text Embedding
| Endpoint | Method |
|----------|--------|
| `/embeddings/text` | POST |

```json
{"text": "Your text here"}
```

### Image Embedding
| Endpoint | Method |
|----------|--------|
| `/embeddings/image` | POST |

```json
{"image_url": "https://..."}
```

### Video Embedding
| Endpoint | Method |
|----------|--------|
| `/embeddings/video` | POST |

```json
{"video_url": "https://..."}
```

---

## AI Chat — Vision Language Models (VLM)

Chat with videos using AI models.

| Endpoint | Provider | Method |
|----------|----------|--------|
| `/gemini/vlm/chat` | Google Gemini | POST |
| `/nova/vlm/chat` | Amazon Nova | POST |
| `/qwen/vlm/chat` | Alibaba Qwen | POST |

**Request:**
```json
{
  "video_url": "https://...",
  "messages": [
    {"role": "user", "content": "What happens in this video?"}
  ]
}
```

---

## AI Chat — Image Language Models (ILM)

Chat with images using AI models.

| Endpoint | Provider | Method |
|----------|----------|--------|
| `/gemini/ilm/chat` | Google Gemini | POST |
| `/nova/ilm/chat` | Amazon Nova | POST |
| `/qwen/ilm/chat` | Alibaba Qwen | POST |
| `/gpt/ilm/chat` | OpenAI GPT-4V | POST |

**Request:**
```json
{
  "image_url": "https://...",
  "messages": [
    {"role": "user", "content": "Describe this image"}
  ]
}
```

---

## AI Chat — VU Chat Completions

Unified vision-understanding chat endpoint with model selection.

| Endpoint | Method |
|----------|--------|
| `/vu/chat/completions` | POST |

**Request:**
```json
{
  "model": "gemini:gemini-2.5-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "input_file", "file_uri": "https://video.mp4", "mime_type": "video/mp4"},
        {"type": "text", "text": "Analyze this video"}
      ]
    }
  ],
  "max_tokens": 1000,
  "temperature": 0.7
}
```

**Available Models:**
- `gemini:gemini-3-flash-preview`
- `gemini:gemini-2.5-flash`
- `nova:nova-lite-v1`
- `qwen:qwen2.5-vl-72b-instruct`

---

## Video Processing

### Extract Frames
| Endpoint | Method |
|----------|--------|
| `/video/extract-frames` | POST |

```json
{
  "video_url": "https://...",
  "interval_seconds": 5
}
```

### Clip Video
| Endpoint | Method |
|----------|--------|
| `/video/clip` | POST |

```json
{
  "video_url": "https://...",
  "start_time": 10,
  "end_time": 30
}
```

### Split Video
| Endpoint | Method |
|----------|--------|
| `/video/split` | POST |

```json
{
  "video_url": "https://...",
  "segments": [
    {"start": 0, "end": 30},
    {"start": 30, "end": 60}
  ]
}
```

### Edit Video (AI-powered)
| Endpoint | Method |
|----------|--------|
| `/video/edit` | POST |

```json
{
  "video_url": "https://...",
  "instructions": "Add subtitles and trim the first 5 seconds"
}
```

---

## Upload & Storage

### Upload from URL
| Endpoint | Method |
|----------|--------|
| `/upload` | POST |

```json
{
  "url": "https://direct-video-url.mp4",
  "name": "my_video"
}
```

### Upload File (Multipart)
| Endpoint | Method |
|----------|--------|
| `/upload` | POST (multipart/form-data) |

Form field: `file`

### Get Signed Upload URL
| Endpoint | Method |
|----------|--------|
| `/upload/signed-url` | POST |

```json
{
  "filename": "video.mp4",
  "content_type": "video/mp4"
}
```

### Get Asset Metadata
| Endpoint | Method |
|----------|--------|
| `/{asset_id}/metadata` | GET |

### Download Asset
| Endpoint | Method |
|----------|--------|
| `/asset/{asset_id}/download` | GET |

### Delete Asset
| Endpoint | Method |
|----------|--------|
| `/asset/{asset_id}` | DELETE |

---

## Asset Transcription

Generate transcription for uploaded assets.

| Endpoint | Method |
|----------|--------|
| `/asset/{asset_id}/transcription` | POST |

```json
{
  "model": "whisper",
  "speaker_diarization": false
}
```

---

## Stream Processing

### Start Audio Stream Transcription
| Endpoint | Method |
|----------|--------|
| `/stream/audio/start` | POST |

```json
{
  "stream_url": "rtmp://...",
  "callback_url": "https://your-webhook.com/callback"
}
```

### Stop Audio Stream
| Endpoint | Method |
|----------|--------|
| `/stream/audio/stop` | POST |

```json
{"stream_id": "..."}
```

### Start Video Stream Moderation
| Endpoint | Method |
|----------|--------|
| `/stream/video/start` | POST |

```json
{
  "stream_url": "rtmp://...",
  "callback_url": "https://your-webhook.com/callback",
  "detect_logo": true
}
```

### Stop Video Stream
| Endpoint | Method |
|----------|--------|
| `/stream/video/stop` | POST |

```json
{"stream_id": "..."}
```

---

## Human Re-identification (ReID)

Track people across videos using reference images.

| Endpoint | Method |
|----------|--------|
| `/human/reid` | POST |

```json
{
  "video_url": "https://...",
  "reference_images": ["https://face1.jpg", "https://face2.jpg"]
}
```

---

## Pricing Summary

| Endpoint | Cost |
|----------|------|
| Simple Transcript | ~$0.02/video |
| MAI Transcript | ~$0.11/40s video (base $0.10 + tokens + duration) |
| Video Metadata | $0.01/call |
| Comments | $0.01/call |
| VLM/ILM Chat | Token-based pricing |
| Embeddings | Token-based pricing |
| Video Processing | Varies by operation |

---

## Webhook Infrastructure

**Default Webhook:** `https://demo.memories-ai.org/webhooks/memories/callback`

**Webhook Server:** `webhooks/memories_webhook.py` (FastAPI, port 8765)

| Webhook Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhooks/memories/callback` | POST | Receive MAI results |
| `/webhooks/memories/caption` | POST | Alias for VEA compat |
| `/webhooks/memories/result/{task_id}` | GET | Query stored result |
| `/webhooks/memories/results` | GET | List recent results |
| `/webhooks/memories/result/{task_id}` | DELETE | Delete stored result |
| `/health` | GET | Health check |

Results stored as: `webhooks/results/<task_id>.json`

---

## Error Codes

| Code | Meaning |
|------|---------|
| `"0000"` | Success |
| HTTP 401 | Invalid API key |
| HTTP 429 | Rate limit exceeded |
| HTTP 500+ | Server error (retry with backoff) |
