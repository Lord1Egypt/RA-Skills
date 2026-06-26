# Phaya API — Full Endpoint Reference

Base URL: `https://your-api-host/api/v1`
Auth header: `Authorization: Bearer <api_key>`
Rate limit: 60 requests/minute per key.

---

## Image Generation

### Text-to-Image (Z-Image via KIE.ai) — 1.0 credit

| Method | Path |
|--------|------|
| POST | `/text-to-image/generate` |
| GET | `/text-to-image/status/{job_id}` |
| GET | `/text-to-image/history` |

**Request body:**
```json
{
  "prompt": "string (required, max 1000 chars)",
  "aspect_ratio": "1:1 | 4:3 | 3:4 | 16:9 | 9:16 (default: 1:1)"
}
```

**Status response:** `{ "status": "PENDING|QUEUED|PROCESSING|COMPLETED|FAILED", "image_url": "..." }`

---

### Seedream 5.0 (ByteDance via KIE.ai) — 1.5 credits

| Method | Path |
|--------|------|
| POST | `/seedream/create` |
| GET | `/seedream/status/{job_id}` |
| POST | `/seedream/callback` |

**Request body:**
```json
{
  "prompt": "string (required, max 2995 chars)",
  "image_urls": ["url1"],
  "aspect_ratio": "1:1 | 4:3 | 3:4 | 16:9 | 9:16 | 2:3 | 3:2 | 21:9 (default: 1:1)",
  "quality": "basic | high (default: basic)"
}
```

Note: `image_urls` is a list (max 1 item) for image-to-image mode. Credits deducted on completion, not creation.

**Status response:** `{ "status": "processing|completed|failed", "image_url": "..." }`

---

### Nano Banana 2 (via KIE.ai) — 2/3/4 credits (1K/2K/4K)

| Method | Path |
|--------|------|
| POST | `/nano-banana/create` |
| GET | `/nano-banana/status/{job_id}` |
| POST | `/nano-banana/callback` |

**Request body:**
```json
{
  "prompt": "string (required, max 20000 chars)",
  "image_input": ["url1", "url2"],
  "aspect_ratio": "1:1 | 1:4 | 1:8 | 2:3 | 3:2 | 3:4 | 4:1 | 4:3 | 4:5 | 5:4 | 8:1 | 9:16 | 16:9 | 21:9 | auto (default: 1:1)",
  "google_search": false,
  "resolution": "1K | 2K | 4K (default: 1K)",
  "output_format": "jpg | png (default: jpg)"
}
```

Note: `image_input` is a list of up to 14 URLs.

**Status response:** `{ "status": "processing|completed|failed", "image_url": "...", "image_urls": ["..."] }`

Note: `image_urls` (plural) is also populated with all result images.

---

## Video Generation

> **Cancel endpoints** (`POST /<service>/cancel/{job_id}`): All cancellable video services return `{ "success": bool, "message": string }`. A job can only be cancelled while in `processing` state; already-terminal jobs return `success: false`.

### Image-to-Video — Local FFmpeg (Ken Burns zoom) — 0.5 credits

| Method | Path |
|--------|------|
| POST | `/image-to-video/create` |
| GET | `/image-to-video/status/{job_id}` |

**Request body:**
```json
{
  "image_url": "url (required)",
  "music_url": "url (optional)",
  "duration": 5,
  "image_format": "auto | jpeg | png | gif | webp (default: auto)",
  "zoom": {
    "mode": "center | top_left | top_right | bottom_left | bottom_right | pan_right | pan_left | pan_up | pan_down | none (default: center)",
    "speed": 0.0015,
    "max_scale": 1.5,
    "pan_speed": 1.0
  }
}
```

Note: `zoom` is an optional object (not a boolean). Omit it to disable Ken Burns effect.

**Status response:** `{ "status": "processing|completed|failed", "video_url": "..." }`

---

### Sora 2 Image-to-Video (via KIE.ai) — 8.0 credits

| Method | Path |
|--------|------|
| POST | `/sora2-video/create` |
| GET | `/sora2-video/status/{job_id}` |
| POST | `/sora2-video/cancel/{job_id}` |
| POST | `/sora2-video/callback` |

**Request body:**
```json
{
  "prompt": "string (required, max 2000 chars)",
  "image_urls": ["url1", "url2"],
  "aspect_ratio": "landscape | portrait | square (default: landscape)",
  "n_frames": "5 | 10 | 15 | 20 (default: 10, as string)",
  "remove_watermark": true,
  "character_id_list": ["char_id1"]
}
```

Note: `image_urls` is a list (1–5 images); `n_frames` is a string literal, not an integer.

**Cancel response:** `{ "success": true, "message": "Job cancelled successfully" }` (or `{"success": false, "message": "Job already completed"}` if already terminal)

**Status response:** `{ "status": "processing|completed|failed|cancelled", "video_url": "..." }`

---

### Sora 2 Text-to-Video (via KIE.ai) — 8.0 credits

| Method | Path |
|--------|------|
| POST | `/sora2-text-to-video/create` |
| GET | `/sora2-text-to-video/status/{job_id}` |
| POST | `/sora2-text-to-video/cancel/{job_id}` |

**Request body:**
```json
{
  "prompt": "string (required, max 2000 chars)",
  "aspect_ratio": "landscape | portrait (default: landscape)",
  "n_frames": "10 | 15 (default: 10, as string)",
  "remove_watermark": true
}
```

**Status response:** `{ "status": "processing|completed|failed|cancelled", "video_url": "..." }`

---

### Sora 2 Character Creation — 0.5 credits

| Method | Path |
|--------|------|
| POST | `/sora2-character/create` |
| GET | `/sora2-character/status/{job_id}` |
| GET | `/sora2-character/list` |
| POST | `/sora2-character/cancel/{job_id}` |

**Request body:**
```json
{
  "character_file_url": "url (required, mp4/mov/webm/m4v/avi, 1-4s, max 100MB)",
  "character_prompt": "string (optional, max 5000 chars)",
  "safety_instruction": "string (optional, max 5000 chars)"
}
```

**Status response:** `{ "status": "processing|completed|failed|cancelled", "character_id": "string" }`

Note: Response contains `character_id` (a reusable ID for `sora2-video.character_id_list`), not a media URL.

---

### Seedance 1.5 Pro (ByteDance via KIE.ai) — 2–35 credits

| Method | Path |
|--------|------|
| POST | `/seedance-video/create` |
| GET | `/seedance-video/status/{job_id}` |
| POST | `/seedance-video/cancel/{job_id}` |
| POST | `/seedance-video/callback` |

**Request body:**
```json
{
  "prompt": "string (required, min 3, max 2500 chars)",
  "input_urls": ["url1", "url2"],
  "aspect_ratio": "1:1 | 21:9 | 4:3 | 3:4 | 16:9 | 9:16 (default: 16:9)",
  "resolution": "480p | 720p | 1080p (default: 720p)",
  "duration": "4 | 8 | 12 (default: 8, as string)",
  "fixed_lens": false,
  "generate_audio": false
}
```

Note: `input_urls` is a list (max 2); `duration` is a string literal.

**Credit table (no-audio / with-audio):**

| Resolution | 4s | 8s | 12s |
|---|---|---|---|
| 480p | 2 / 3 | 3 / 6 | 4 / 8 |
| 720p | 3 / 6 | 6 / 12 | 9 / 18 |
| 1080p | 6 / 12 | 12 / 23 | 18 / 35 |

**Status response:** `{ "status": "processing|completed|failed", "video_url": "...", "audio_url": "..." }`

Note: `audio_url` is populated when `generate_audio=true`; otherwise `null`.

---

### Kling 2.6 Motion Control (via KIE.ai) — 1.21–1.82 credits/sec

| Method | Path |
|--------|------|
| POST | `/kling-motion-control/create` |
| GET | `/kling-motion-control/status/{job_id}` |
| POST | `/kling-motion-control/cancel/{job_id}` |
| POST | `/kling-motion-control/callback` |

**Request body:**
```json
{
  "prompt": "string (optional, max 2500 chars)",
  "input_urls": ["image_url"],
  "video_urls": ["motion_ref_url"],
  "character_orientation": "image | video (default: video)",
  "mode": "720p | 1080p (default: 720p)"
}
```

Note:
- `input_urls`: exactly 1 reference image (jpg/png, max 10MB, min 300px, aspect ratio 2:5 to 5:2)
- `video_urls`: exactly 1 motion reference video (mp4/mov, max 100MB, max 30 sec)
- `character_orientation: "image"` → max 10s output; `"video"` → max 30s output
- Credits: 720p = 1.21/sec, 1080p = 1.82/sec

**Status response:** `{ "status": "processing|completed|failed", "video_url": "..." }`

---

### Veo 3.1 (Google via KIE.ai) — 15 credits (fast) / 50 credits (quality)

| Method | Path |
|--------|------|
| POST | `/veo31-video/create` |
| GET | `/veo31-video/status/{job_id}` |
| POST | `/veo31-video/cancel/{job_id}` |
| POST | `/veo31-video/callback` |

**Request body:**
```json
{
  "prompt": "string (required, max 2000 chars)",
  "model": "veo3_fast | veo3 (default: veo3_fast)",
  "image_urls": ["url1", "url2", "url3"],
  "generation_type": "TEXT_2_VIDEO | FIRST_AND_LAST_FRAMES_2_VIDEO | REFERENCE_2_VIDEO (optional)",
  "aspect_ratio": "16:9 | 9:16 | Auto (default: 16:9)",
  "seeds": 12345,
  "enable_translation": true,
  "watermark": "string (optional, max 50 chars)"
}
```

Note: `image_urls` is a list (max 3, optional); `model: "veo3"` = 50 credits, `"veo3_fast"` = 15 credits; `seeds` must be between 10000 and 99999 if provided.

**Status response:** `{ "status": "processing|completed|failed|cancelled", "video_url": "...", "origin_url": "...", "resolution": "..." }`

---

## Audio / Music / Speech

### Text-to-Music (Suno via KIE.ai) — 3.0 credits

| Method | Path |
|--------|------|
| POST | `/text-to-music/generate` |
| GET | `/text-to-music/status/{job_id}` |
| GET | `/text-to-music/history` |

**Request body:**
```json
{
  "prompt": "string (required, max 2000 chars)",
  "style": "string (optional, max 100 chars, e.g. 'lofi hip hop')",
  "title": "string (optional, max 200 chars)",
  "instrumental": false,
  "model": "V3 | V3_5 | V4 | V5 (default: V4)",
  "negative_tags": "string (optional, max 500 chars)",
  "vocal_gender": "m | f (optional)",
  "style_weight": 0.5,
  "weirdness_constraint": 0.5,
  "audio_weight": 0.5
}
```

Note: Generates 2 tracks. Response contains `audio_url` (first track) and `audio_urls[]` (both tracks).

**Status response:** `{ "status": "PENDING|QUEUED|PROCESSING|COMPLETED|FAILED", "audio_url": "...", "audio_urls": ["...", "..."] }`

---

### Text-to-Speech (Google Gemini TTS) — token-based

| Method | Path | Auth |
|--------|------|------|
| POST | `/text-to-speech/generate` | required |
| GET | `/text-to-speech/status/{job_id}` | required |
| GET | `/text-to-speech/history` | required |
| GET | `/text-to-speech/voices` | **none** |

Note: `GET /text-to-speech/voices` requires no authentication. Response: `{ "voices": [{"name": "Zephyr", "description": "..."}, ...] }`

**Request body:**
```json
{
  "prompt": "string (required, max 500000 chars)",
  "voice": "Zephyr (default) | Algenib | Algieba | Aoede | Autonoe | Callirrhoe | Despina | Erinome | Fenrir | Iapetus | Kore | Laomedeia | Leda | Orus | Sadaltager | Schedar | Umbriel | Vindemiatrix | Zubenelgenubi",
  "slow": false,
  "language": "en | th | ja | zh-CN | ko | null (auto-detect)"
}
```

**Status response:** `{ "status": "PENDING|PROCESSING|COMPLETED|FAILED", "audio_url": "..." }`

---

## LLM / AI

### Phaya-GPT Chat (Gemini via OpenRouter) — token-based

| Method | Path |
|--------|------|
| POST | `/phaya-gpt/chat/completions` |
| GET | `/phaya-gpt/models` |
| GET | `/phaya-gpt/pricing` |

**Request body:**
```json
{
  "messages": [{"role": "user|system|assistant", "content": "string"}],
  "model": "string (optional, defaults to configured model)",
  "temperature": 0.7,
  "max_tokens": null,
  "stream": false,
  "web_search": false
}
```

**Non-streaming response** (flat dict, NOT OpenAI choices[]):
```json
{
  "success": true,
  "id": "string",
  "model": "Phaya-GPT",
  "message": {"role": "assistant", "content": "string"},
  "usage": {"prompt_tokens": 10, "completion_tokens": 50, "total_tokens": 60},
  "credits_used": 0.001,
  "finish_reason": "stop"
}
```

Note: Access content as `response["message"]["content"]`. The `model` field always returns `"Phaya-GPT"` (display name); the actual upstream default is `google/gemini-3-flash-preview`. Set `"stream": true` for a raw SSE stream; each chunk follows the OpenRouter SSE format ending with `data: [DONE]`.

---

### Text Embeddings (Qwen3 Embedding 8B via OpenRouter) — token-based

| Method | Path |
|--------|------|
| POST | `/embedding/create` |
| GET | `/embedding/pricing` |

**Request body:**
```json
{
  "input": "string or [\"string\", \"string\"]",
  "model": "string (optional, default: qwen/qwen3-embedding-8b)"
}
```

---

### OpenAI-Compatible Proxy

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/chat/completions` | Chat completions (OpenAI-compatible) |
| GET | `/v1/models` | List available models |
| POST | `/v1/embeddings` | Embeddings (OpenAI-compatible) |
| POST | `/v1/responses` | OpenAI Responses API compat |

Full OpenAI SDK drop-in — set `base_url` to `https://your-api-host` and use your Phaya API key. Supports tools, streaming, vision, and all OpenAI request fields.

---

## Media Utilities

### Thai Subtitle Generator (Whisper + PyThaiNLP + FFmpeg) — 0.17 credits/min (min 0.07)

| Method | Path |
|--------|------|
| POST | `/thai-subtitle/generate` |
| GET | `/thai-subtitle/status/{job_id}` |

**Request body:**
```json
{
  "media_url": "url (required, mp4/mov/webm)",
  "script": "string (optional, max 10000 chars; use | for line breaks, \\n\\n for new segments)",
  "animation": "none | word_pop_fade (default: none)",
  "timing_offset_ms": 0
}
```

Note: `timing_offset_ms` range: −300 to +300 ms.

**Status response:** `{ "status": "PENDING|PROCESSING|COMPLETED|FAILED", "video_url": "..." }`

---

### Video Download (yt-dlp → Supabase) — 0.5 credits/10MB

| Method | Path |
|--------|------|
| POST | `/video-download/create` |
| GET | `/video-download/status/{job_id}` |
| GET | `/video-download/supported-platforms` |

**Request body:**
```json
{
  "url": "YouTube/TikTok/etc URL (required)",
  "format": "mp4 | mp3 | best (default: mp4)",
  "quality": "best | 720p | 480p | 360p | audio (default: best)"
}
```

Note: 0.5 credits for first ≤10MB; 0.5 credits per 10MB above that.

**Status response:** `{ "status": "processing|completed|failed", "download_url": "..." }`

---

### FFmpeg Media Utilities

| Method | Path | Description |
|--------|------|-------------|
| POST | `/media/merge-video` | Merge multiple video files |
| POST | `/media/merge-audio-video` | Combine audio + video |
| POST | `/media/merge-audio` | Merge audio tracks |
| POST | `/media/overlay-gif` | Overlay GIF on video |
| POST | `/media/transcribe` | Transcribe audio/video |
| POST | `/media/extract-last-frame` | Extract last frame as image |
| POST | `/media/upload` | Upload file to Supabase storage |
| GET | `/media/status/{job_id}` | Poll media job |
| GET | `/media/queue/stats` | Queue statistics |

---

## User / Account

| Method | Path | Description |
|--------|------|-------------|
| GET | `/user/profile` | Full profile including credits |
| GET | `/user/credits` | Credit balance → `credits_balance` (float) |
| GET | `/user/credits/history` | Transaction history (query: `?limit=20`) |
| POST | `/user/credits/invalidate-cache` | Force-clear Redis credit cache |

**`GET /user/credits` response:**
```json
{
  "success": true,
  "user_id": "uuid",
  "credits_balance": 84.90,
  "credits_balance_formatted": "84.90 เครดิต",
  "currency": "THB",
  "cached": false
}
```

---

## Third-Party Services Summary

| Service | Models / Use |
|---------|-------------|
| KIE.ai | Z-Image, Seedream 5.0, Nano Banana 2, Sora 2 (i2v + t2v), Veo 3.1, Seedance 1.5 Pro, Kling 2.6, Suno music |
| Google Gemini | TTS (`gemini-2.5-flash-preview-tts`) |
| OpenRouter | Phaya-GPT LLM, Qwen3 Embedding 8B |
| Together AI | Whisper Large v3 for Thai subtitle transcription |
| Supabase | Auth, database, file storage (all output URLs) |
| Redis | Job status cache (5s TTL pending, 1h completed), rate limiting |
