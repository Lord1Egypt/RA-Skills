---
name: krea-image-api
description: Generate images via Krea.ai API — Nano Banana 2 (default), Flux, Imagen 4, Seedream 3, Ideogram 3.0, Nano Pro/base. Returns direct URLs.
homepage: https://docs.krea.ai/developers/introduction
version: 1.0.2
metadata: {"openclaw":{"emoji":"🎨","requires":{"env":["KREA_API_TOKEN"]},"primaryEnv":"KREA_API_TOKEN","homepage":"https://docs.krea.ai/developers/introduction"}}
---

# Krea Image API

You are a skill that generates images using the Krea.ai HTTP API and returns direct image URLs.

## Supported models

User says model name → you map to endpoint:

| User alias(es)                              | Endpoint path                                        | Best for                                      |
|---------------------------------------------|------------------------------------------------------|-----------------------------------------------|
| `nano banana 2`, `nano2`, `flash`, **default** | `/generate/image/google/nano-banana-flash`           | Fastest/cheapest, intelligent multi-image     |
| `flux`, `flux-dev`, `bfl`                   | `/generate/image/bfl/flux-1-dev`                     | Versatile generation, LoRAs, custom ratios    |
| `imagen`, `imagen4`, `imagen-4`, `google`   | `/generate/image/google/imagen-4-fast`               | Photorealism, typography, fast output         |
| `seedream`, `seedream3`, `bytedance`        | `/generate/image/bytedance/seedream-3`               | Photorealism, flexible resolution             |
| `ideogram`, `ideogram3`, `ideogram-3`       | `/generate/image/ideogram/ideogram-3`                | Flat/graphic styles, text-in-image            |
| `nano banana pro`, `nano pro`, `pro`        | `/generate/image/google/nano-banana-pro`             | Typography, photorealism, 4K res              |
| `nano banana`, `nano`, `nano1`              | `/generate/image/google/nano-banana`                 | Base/original model                           |

Default model is **Nano Banana 2** (`/generate/image/google/nano-banana-flash`) — use it unless user specifies otherwise. Always confirm model choice in your response.

## When to use

Explicit image generation requests only. Skip for video/text/audio.

## Rate limits & best practices ⚠️

Krea enforces **rate limits** (requests/min, compute units/hour — varies by plan). To avoid 429 errors:

- Max **1 job submission every 10 seconds**.
- **Poll interval: 5-8 seconds** (never <5s) — image gen takes 15-120s depending on model/resolution.
- Max **40 polls per job** (~5 min total).
- If 429: Wait 30s before retrying anything.
- High batchSize (>2) or 4K res = longer queues.

## Auth

```
Authorization: Bearer KREA_API_TOKEN
```

If missing: "Krea API token not configured — set KREA_API_TOKEN env."

## Workflow

### 1. Pick model & build JSON
Required: `prompt`. Optional: `width`/`height` (512–2368), `batchSize` (1–4), `aspectRatio` ("16:9"), `imageUrls`.

**Steps param**: Only for Flux (`steps: 28`). Omit for all Nano Banana, Ideogram, Imagen, Seedream.

### 2. POST job
`https://api.krea.ai{endpoint_path}`  
Headers: Auth + `Content-Type: application/json`

### 3. **Poll carefully** (key improvement)
```
GET https://api.krea.ai/jobs/{job_id}
```
- **Delay 6 seconds between polls** (respects rate limits, accounts for 15-90s gen times).
- Check `status`:
  | Status      | Action                          |
  |-------------|---------------------------------|
  | `backlogged`/`queued`/`processing` | Continue polling                |
  | `completed` + `result.urls` | Extract & return URLs           |
  | `failed`/`cancelled` | Report error                    |
- **Max 40 polls** (~4 min). Timeout → "Job timed out — complex prompts take longer, try simpler or check quota."
- **Rate limit handling**: If 429 response, wait **60s** then retry poll (don't spam).

### 4. Respond
Success: 
```
Generated with [MODEL]: [summary]

[Image URLs as list/markdown]
```
Failure: Error summary + suggestion (e.g. "Rate limited — wait 1 min", "Out of compute — upgrade plan").

## Model tips

| Model              | Tips & timing estimate                                                   |
|--------------------|--------------------------------------------------------------------------|
| **Nano Banana 2**  | **Default**: Rich scenes; fast (15-30s), batchSize 1-4, aspectRatio     |
| Flux               | Detailed photo/style (30-90s), steps:20-40                               |
| Imagen 4 Fast      | Product shots (20-45s)                                                   |
| Seedream 3         | Photoreal "8K detail" (45-120s)                                          |
| Ideogram 3.0       | Text-in-image, "poster style" (30-60s)                                   |
| Nano Banana Pro    | Typography/4K photoreal (25-60s)                                         |
| Nano Banana        | Basic scenes (20-45s), webhook support                                   |

## Config
KREA_API_TOKEN from https://krea.ai/settings/api-tokens
