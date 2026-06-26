---
name: phosor-ai
version: 1.0.0
description: Generate AI videos (text-to-video, image-to-video) with optional custom LoRA styles via the Phosor AI platform. Supports importing images and LoRA models from external URLs. Use when the user wants to create videos from text prompts, animate images, or apply custom LoRA models.
license: MIT-0
metadata:
  author: phosor
  openclaw:
    requires:
      env: [PHOSOR_API_KEY, PHOSOR_BASE_URL]
      bins: [python3]
      config: [phosor-pending.json]
    primaryEnv: PHOSOR_API_KEY
    homepage: https://phosor.ai
---

# Phosor AI

Generate AI videos (text-to-video, image-to-video) with optional custom LoRA styles via the Phosor AI platform.

For detailed API endpoints, parameters, pricing, and limits, see [references/api.md](references/api.md).

## Setup

1. Sign up or log in at [phosor.ai](https://phosor.ai)
2. Go to **Settings → API Keys** to generate your API key
3. Set it as an environment variable:

```bash
export PHOSOR_API_KEY="your-api-key-here"
```

> **Keep your API key secret.** Do not commit it to version control or share it publicly. All API calls are authenticated and billed through this key.

The CLI script is at `scripts/phosor_client.py`. All commands output JSON to stdout.

**Local files used by the CLI:**
- Writes `phosor-pending.json` to track pending job states locally

## Quick Start

### Text-to-Video

```bash
# Submit T2V job (480p, 81 frames, 16fps)
python3 scripts/phosor_client.py submit "A cat walking on a beach at sunset" \
  --width 854 --height 480 --num-frames 81 --fps 16

# Check status
python3 scripts/phosor_client.py status <request_id>

# Get result (video URL)
python3 scripts/phosor_client.py result <request_id>
```

### Image-to-Video

**Two-step flow**: upload image first, then submit with the returned S3 key.

```bash
# Step 1: Upload image
python3 scripts/phosor_client.py upload-image /path/to/photo.jpg
# Returns: {"file_id": "img-xxx", "s3_key": "images/img-xxx.jpg", ...}

# Step 2: Submit I2V job using the s3_key as image_url
python3 scripts/phosor_client.py submit "The person in the photo starts dancing" \
  --image-url "images/img-xxx.jpg" --width 854 --height 480
```

### With Custom LoRA

Upload your own LoRA model, then use it in video generation.

```bash
# Upload LoRA (two .safetensors: high_noise + low_noise)
python3 scripts/phosor_client.py upload-lora high_noise.safetensors low_noise.safetensors --name "My Style"

# Check upload status
python3 scripts/phosor_client.py lora-status <lora_id>

# Use in inference
python3 scripts/phosor_client.py submit "A person walking" --lora-id <lora_id> --lora-scale 1.0

# Or import LoRA from URLs
python3 scripts/phosor_client.py import-lora \
  "https://example.com/high_noise.safetensors" \
  "https://example.com/low_noise.safetensors" \
  --name "My Style"
```

## CLI Commands

### Job Management

- `submit <prompt>` — Submit inference job (T2V/I2V). Options: `--width`, `--height`, `--num-frames`, `--fps`, `--steps`, `--guidance`, `--image-url`, `--lora-id`, `--lora-scale`, `--seed`, `--negative-prompt`, `--model`
- `status <request_id>` — Get job status
- `result <request_id>` — Get job result (video URL)
- `poll` — Poll all pending jobs
- `list` — List locally tracked pending jobs
- `history` — Get job history. Options: `--limit`

### File Upload

- `upload-image <file>` — Upload image for I2V
- `import-image <url>` — Import image from URL. Options: `--filename`
- `upload-lora <high_noise_file> <low_noise_file>` — Upload LoRA (two .safetensors). Options: `--name`
- `import-lora <high_noise_url> <low_noise_url>` — Import LoRA from URLs. Options: `--name`

### LoRA Management

- `loras` — List LoRA models. Options: `--limit`, `--offset`
- `lora-status <lora_id>` — Get LoRA upload status
- `delete-lora <lora_id>` — Delete a LoRA model

### Utilities

- `check-key` — Validate API key
- `models` — List available models
- `quotas` — Get quota usage/limits

## Key Constraints

### Resolutions (exact pairs only)

- **480p landscape** — 854 × 480, max 161 frames
- **480p portrait** — 480 × 854, max 161 frames
- **720p landscape** — 1280 × 720, max 161 frames
- **720p portrait** — 720 × 1280, max 161 frames
- **1080p landscape** — 1920 × 1080, max 153 frames
- **1080p portrait** — 1080 × 1920, max 153 frames

### Frame Alignment

Frames must follow `1 + 4*k` where `k >= 1` (e.g. 5, 9, 13, ... 81, 85, ...). Server auto-aligns down.

### Inference Parameters

- `frames_per_second` — default: 16, range: 4–30
- `num_inference_steps` — default: 4, range: 4
- `guidance_scale` — default: 1.0, range: 1.0–3.5
- `lora_scale` — default: 1.0, range: 0.0–2.0

### Two-Step Upload Rule

Files must be uploaded before use:

1. **Image** → `upload-image` / `import-image` → returns `s3_key` → use as `--image-url`
2. **LoRA** → `upload-lora` / `import-lora` → returns `lora_id` → use as `--lora-id`

## Queue Flow

```
PENDING → PROCESSING → COMPLETED / FAILED
```

The `poll` command checks all locally-tracked pending jobs and removes completed/failed ones.

## Pricing

- **480p** — $0.0002 per frame (0.002 credits)
- **720p** — $0.0006 per frame (0.006 credits)
- **1080p** — $0.0012 per frame (0.012 credits)
- **LoRA multiplier** — 1.25x

Exchange rate: 10 credits = $1 USD. Credits pre-deducted, auto-refunded on failure.

## Version History

### 1.0.0 (2026-03-21)

- Initial release
- Text-to-video and image-to-video generation (Wan 2.2 14B)
- Custom LoRA support (upload, import, use in inference)
- 16 CLI commands
- Model registry with `GET /api/v1/models` endpoint
- Supported models: `wan/2.2-14b/text-to-video`, `wan/2.2-14b/image-to-video`
