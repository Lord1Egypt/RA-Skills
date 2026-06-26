# Deepfake Detection

Detect AI-generated or manipulated images and videos. Detection is powered by a continuously evolving model on [Bittensor Subnet 34](https://bitmind.ai) — adversarial competition between generation and detection miners drives accuracy improvements.

## Getting an API Key

1. Register or log in at [app.bitmind.ai](https://app.bitmind.ai)
2. Go to **API Keys** → [app.bitmind.ai/api/keys](https://app.bitmind.ai/api/keys)
3. Click **Generate New Key**
4. Set as environment variable:

```bash
export BITMIND_API_KEY=your_key_here
```

## API Reference

Base URL: `https://api.bitmind.ai`

Authentication: `Authorization: Bearer <BITMIND_API_KEY>`

---

### POST /detect-image

Analyze an image for AI-generated content.

**Accepts any URL** — the API downloads the image server-side. Direct image links, social media URLs, CDN links all work.

**Input methods:**
- **JSON** — URL or base64 data URI: `{"image": "https://...", "debug": false}`
- **Multipart** — file upload or URL string in `image` field

**JSON (URL):**
```bash
curl -X POST https://api.bitmind.ai/detect-image \
  -H "Authorization: Bearer $BITMIND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image": "https://example.com/photo.jpg"}'
```

**JSON (base64 data URI):**
```bash
curl -X POST https://api.bitmind.ai/detect-image \
  -H "Authorization: Bearer $BITMIND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/jpeg;base64,/9j/4AAQ..."}'
```

**Multipart (file upload):**
```bash
curl -X POST https://api.bitmind.ai/detect-image \
  -H "Authorization: Bearer $BITMIND_API_KEY" \
  -F "image=@photo.jpg"
```

**Response:**
```json
{
  "isAI": false,
  "confidence": 0.23,
  "similarity": 0.05,
  "objectKey": "1704067200000.jpg"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `isAI` | bool | Whether content is detected as AI-generated |
| `confidence` | float | Confidence score (0.0–1.0) |
| `similarity` | float | Similarity to known AI content (0.0–1.0), null if service unavailable |
| `objectKey` | string | Storage key for the processed media |

**Debug response** (`"debug": true`):
```json
{
  "isAI": true,
  "confidence": 0.95,
  "similarity": 0.82,
  "objectKey": "1704067200000.jpg",
  "debug": {
    "raw": 0.88,
    "processingTime": 1.2,
    "region": "us",
    "contentCredentials": {
      "hasCredentials": true,
      "detectedModel": "Adobe Firefly"
    }
  }
}
```

Supported formats: jpeg, png, gif, bmp, webp, avif.

---

### POST /detect-video

Analyze a video for AI-generated content.

**Accepts social media URLs natively** — YouTube, Twitter/X, TikTok, and direct video links. The API extracts and downloads the video server-side.

**Input methods:**
- **JSON** — URL only: `{"video": "https://...", "fps": 1, "debug": false}`
- **Multipart** — file upload or URL string in `video` field

**Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `video` | string | required | Video URL (YouTube, Twitter, TikTok, direct) or file |
| `startTime` | float | 0 | Start time in seconds |
| `endTime` | float | null | End time in seconds (null = entire video) |
| `fps` | int | 1 | Frames per second to analyze (1–30, higher = more accurate but slower) |
| `debug` | bool | false | Include debug info (absurdity, C2PA, timing) |

**JSON (social media URL):**
```bash
curl -X POST https://api.bitmind.ai/detect-video \
  -H "Authorization: Bearer $BITMIND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "https://x.com/user/status/123456", "fps": 1, "debug": true}'
```

**Multipart (file upload):**
```bash
curl -X POST https://api.bitmind.ai/detect-video \
  -H "Authorization: Bearer $BITMIND_API_KEY" \
  -F "video=@video.mp4" -F "fps=1"
```

**Response:**
```json
{
  "isAI": false,
  "confidence": 0.72,
  "similarity": 0.0,
  "objectKey": "1704067200000.mp4",
  "thumbnailObjectKey": "thumbnails/1704067200000/main.jpg"
}
```

**Debug response with absurdity analysis** (`"debug": true`):
```json
{
  "isAI": true,
  "confidence": 0.92,
  "similarity": 0.0,
  "objectKey": "1704067200000.mp4",
  "thumbnailObjectKey": "thumbnails/1704067200000/main.jpg",
  "debug": {
    "raw": 0.78,
    "processingTime": 5.3,
    "region": "us",
    "contentCredentials": {"hasCredentials": false},
    "absurdity": {
      "score": 85,
      "summary": "Man walking through wall in office building",
      "verdict": "Physics-defying movement inconsistent with real footage",
      "metadata": {"frames": 16, "peak": 92}
    }
  }
}
```

| Debug Field | Description |
|-------------|-------------|
| `absurdity.score` | 0–100 absurdity score |
| `absurdity.summary` | Brief description of what the video shows |
| `absurdity.verdict` | Reasoning for the absurdity score |
| `absurdity.metadata` | Frame count analyzed and peak absurdity frame |

Max upload: 100MB (Cloudflare limit).

---

## Detection Signals

The API combines multiple independent signals. Each signal can only **increase** confidence, never decrease it.

### isAI Priority (first match wins)

1. **C2PA metadata** — content credentials indicate AI tool → `isAI = true`
2. **Similarity ≥ 0.7** — matches known AI content in database → `isAI = true`
3. **Absurdity ≥ 0.8** (video only) — physically impossible content AND score > model prediction → `isAI = true`
4. **Model prediction ≥ 0.5** — Subnet 34 detection model → `isAI = true`

### Confidence Calculation

Starts at `max(raw, 1 - raw)`. Additional signals raise the floor:
- C2PA detected model → confidence ≥ 0.95
- Similarity ≥ 0.7 → confidence ≥ similarity score
- Absurdity ≥ 0.8 (video) → confidence ≥ normalized absurdity

---

## Detection Pipeline

### Image

1. **Auth** — validate Bearer token
2. **Cache** — SHA-256 hash check in Redis (1h TTL)
3. **Download** — fetch media from URL server-side (handles any URL, including social media)
4. **Preprocess** — resize, create tensor + service image (local)
5. **C2PA** — extract content credentials (local)
6. **Parallel**: Subnet 34 model detection + similarity matching
7. **Response** — combine signals → isAI + confidence

### Video

1. **Auth** → **Cache** → **Download** (same as image)
2. **Preprocess** — extract frames at specified FPS, generate thumbnail, create tensor
3. **C2PA** — extract content credentials (local)
4. **Parallel** (3-way): Subnet 34 model detection + absurdity analysis + similarity matching
5. **Response** — combine all signals including absurdity → isAI + confidence

### Background (fire-and-forget, no added latency)

- Cache result in Redis
- Upload media to R2 storage

Typical latencies: image ~1–2s, video ~3–10s, cache hit ~50ms.
