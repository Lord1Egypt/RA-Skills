# Phosor AI API Reference

Base URL: `https://phosor.ai`

All endpoints require `X-API-Key` header unless noted otherwise.

## Endpoints

### Models

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/models` | None | List available models |

### Inference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/inference/submit` | Submit video generation job |
| GET | `/api/v1/inference/status/{request_id}` | Get job status + progress |
| GET | `/api/v1/inference/result/{request_id}` | Get completed video result |
| GET | `/api/v1/inference/history` | Get user's job history |

### Storage — Image

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/storage/image/upload` | Multipart image upload |
| POST | `/api/v1/storage/image/import` | Import from public URL |

### Storage — LoRA

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/storage/lora/upload` | Upload two .safetensors files (high_noise + low_noise) |
| POST | `/api/v1/storage/lora/import` | Import from two HTTPS URLs |

### LoRA Management

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/loras` | List LoRA models |
| GET | `/api/v1/loras/{lora_id}/status` | Get processing status |
| DELETE | `/api/v1/loras/{lora_id}` | Soft delete |

## Inference Submit Parameters

| Parameter | Type | Required | Default | Range |
|-----------|------|----------|---------|-------|
| `prompt` | string | Yes | — | — |
| `model` | string | No | `wan/2.2-14b/text-to-video` | See supported models |
| `width` | int | No | 854 | See resolutions |
| `height` | int | No | 480 | See resolutions |
| `num_frames` | int | No | 81 | Auto-aligned to 1+4k |
| `frames_per_second` | int | No | 16 | 4–30 |
| `num_inference_steps` | int | No | 4 | 4 |
| `guidance_scale` | float | No | 1.0 | 1.0–3.5 |
| `seed` | int | No | random | — |
| `negative_prompt` | string | No | "" | — |
| `image_url` | string | No | — | S3 key from upload-image |
| `lora_id` | string | No | — | LoRA model ID |
| `lora_scale` | float | No | 1.0 | 0.0–2.0 |

## Supported Resolutions

| Preset | Width | Height | Max Frames |
|--------|-------|--------|-----------|
| 480p landscape | 854 | 480 | 161 |
| 480p portrait | 480 | 854 | 161 |
| 720p landscape | 1280 | 720 | 161 |
| 720p portrait | 720 | 1280 | 161 |
| 1080p landscape | 1920 | 1080 | 153 |
| 1080p portrait | 1080 | 1920 | 153 |

Only these exact pairs are accepted. Frame alignment: `valid_frames = 1 + 4*k` where `k >= 1`.

## Pricing

### Inference (10 credits = $1 USD)

| Resolution | Per-Frame (USD) | Per-Frame (Credits) |
|-----------|----------------|-------------------|
| 480p | $0.0002 | 0.002 |
| 720p | $0.0006 | 0.006 |
| 1080p | $0.0012 | 0.012 |

LoRA multiplier: 1.25x (applied when any LoRA is specified).

Credits are pre-deducted on submit. On failure/timeout, credits are automatically refunded.

## Limits & Quotas

| Resource | Limit |
|----------|-------|
| Rate limit | 1000 requests / 60 seconds per API key |
| Concurrent jobs | Tier-based: Starter=1, Standard=5, Pro=20 |
| Max API keys per user | 10 |
| Max LoRAs per user | 20 |
| LoRA file format | `.safetensors` only (two files: high_noise + low_noise) |
| Max LoRA file size | 2048 MB |
| Uploaded LoRA expiry | 1 day (auto-cleaned) |
| Image formats | JPEG, PNG, WebP |
| Queue timeout | 3000s (auto-refund) |
| Execution timeout | 2400s (auto-refund) |

## Response Formats

### Models Response
```json
{"models": [{"model_id": "wan/2.2-14b/text-to-video", "description": "Wan 2.2 Text-to-Video 14B", "model_type": "video", "model_mode": "text-to-video", "metadata": {}}]}
```

### Submit Response
```json
{"request_id": "<job_id>", "status": "queued"}
```

### Status Response
```json
{"request_id": "...", "status": "queued|processing|completed|failed", "progress": 0-100}
```

### Result Response
```json
{"data": {"video": {"url": "..."}, "seed": 12345}, "request_id": "..."}
```

### Error Codes
| Code | Meaning |
|------|---------|
| 400 | Validation error |
| 401 | Invalid API key or email not verified |
| 402 | Insufficient credits |
| 404 | Job not found |
| 429 | Rate limit or concurrency limit exceeded |
| 503 | Queue at capacity |
