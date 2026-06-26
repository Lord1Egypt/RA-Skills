# Phaya Media API

Generate images, videos, audio, and AI chat completions via the Phaya SaaS backend — all through a single, authenticated REST API.

## What It Does

This skill teaches an AI agent how to use the Phaya backend to:

- **Generate images** — Z-Image (1 credit), Seedream 5.0 (1.5 credits), Nano Banana 2 (2–4 credits)
- **Generate videos** — Sora 2 i2v/t2v (8 credits), Veo 3.1 (15–50 credits), Seedance 1.5 Pro (3–35 credits), Kling 2.6 motion control (1.21–1.82 credits/sec), FFmpeg local (0.5 credits)
- **Generate audio/music** — Suno music via KIE.ai (3 credits), Google Gemini TTS (token-based)
- **Run LLM chat** — Phaya-GPT at `/api/v1/phaya-gpt/chat/completions`, plus a full OpenAI-compatible proxy at `/v1/chat/completions`
- **Media utilities** — Thai subtitle generation (Whisper + FFmpeg), yt-dlp video download, FFmpeg merge/overlay/transcribe

## Supported Services

| Category | Service | Provider |
|----------|---------|----------|
| Image | Z-Image | KIE.ai |
| Image | Seedream 5.0 | ByteDance via KIE.ai |
| Image | Nano Banana 2 | KIE.ai |
| Video | Sora 2 (i2v + t2v + character) | KIE.ai |
| Video | Veo 3.1 | Google via KIE.ai |
| Video | Seedance 1.5 Pro | ByteDance via KIE.ai |
| Video | Kling 2.6 motion control | KIE.ai |
| Video | FFmpeg Ken Burns zoom | Local |
| Music | Suno (V3–V5) | KIE.ai |
| Speech | Gemini TTS | Google |
| LLM | Phaya-GPT | OpenRouter |
| Embeddings | Qwen3 Embedding 8B | OpenRouter |
| Subtitles | Whisper Large v3 + PyThaiNLP | Together AI |
| Download | yt-dlp (YouTube, TikTok, etc.) | Local |

## Requirements

- A valid Phaya API key (obtain from your account at the Phaya host)
- `httpx` (Python) or `curl` for making API calls
- No local GPU or model weights required — all generation is done server-side

## Authentication

```
Authorization: Bearer <your_api_key>
```

Check your credit balance:
```
GET /api/v1/user/credits  →  { "credits_balance": 84.90, "credits_balance_formatted": "84.90 เครดิต" }
```

Rate limit: 60 requests/minute per API key.

## How It Works

Every generation endpoint is async. The pattern is:

1. `POST /api/v1/<service>/create` — submit the job, get back `{ "job_id": "uuid" }`
2. `GET /api/v1/<service>/status/{job_id}` — poll every 3–5 seconds
3. When `status` reaches `COMPLETED` (or `completed`), read the result field

Result field names by media type:
- Images → `image_url`
- Videos → `video_url`
- Audio/music → `audio_url` (music also has `audio_urls[]` for both tracks)
- Video download → `download_url`
- Sora 2 character → `character_id`

## Quick Example

```python
import httpx, time

BASE = "https://your-api-host/api/v1"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY"}

# Generate an image
r = httpx.post(f"{BASE}/text-to-image/generate", headers=HEADERS, json={
    "prompt": "A futuristic city at sunset",
    "aspect_ratio": "16:9"
})
job_id = r.json()["job_id"]

while True:
    s = httpx.get(f"{BASE}/text-to-image/status/{job_id}", headers=HEADERS).json()
    if s["status"] == "COMPLETED":
        print("Image URL:", s["image_url"])
        break
    time.sleep(4)
```

## Documentation

- [SKILL.md](SKILL.md) — concise quickstart reference for AI agents
- [endpoints.md](endpoints.md) — full endpoint reference with request schemas, valid enum values, and credit costs
- [examples.md](examples.md) — 18 ready-to-run curl and Python examples covering every service

## Troubleshooting

**Job stuck in `PENDING`/`QUEUED`:** Upstream providers (KIE.ai, Gemini) can queue jobs under high load. Poll for up to 10 minutes before treating as failed.

**`FAILED` status:** Credits are automatically refunded. Check the `error` field in the status response for the reason.

**Rate limit hit (429):** Reduce request frequency; limit is 60 req/min per key.

**Wrong aspect ratio rejected:** Each endpoint has its own allowed values — e.g. Sora 2 uses `"landscape"/"portrait"` not `"16:9"/"9:16"`. See [endpoints.md](endpoints.md) for per-endpoint enums.
