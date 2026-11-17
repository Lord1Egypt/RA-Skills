---
name: phosor-ai-skills
description: Create videos with MiniMax H3 Standard or Turbo (text-to-video, image-to-video, and reference-to-video) through Phosor AI, then use the same skill for images, speech, LLM chat (Qwen3.8 27B, OpenAI-compatible), LoRA workflows, and e-commerce product or model photography. Use when the user wants to create H3 video from text, images, or references, compare Standard and Turbo, use the Phosor API, generate images or speech, chat with or call the Qwen3.8 27B LLM, use a custom LoRA, create e-commerce photography, or manage generation jobs.
license: MIT-0
metadata:
  author: phosor.ai
  version: "1.4.1"
  api_version: "v1.3.0"
  homepage: https://phosor.ai
---

# Phosor AI

MiniMax H3 Standard and Turbo are the primary video workflows in this skill. Use H3 for text-to-video, image-to-video, or reference-to-video, then use the same Phosor API for images, speech, LLM chat, LoRA workflows, and e-commerce product or model photography when needed.

For detailed API endpoints, parameters, pricing, and limits, see [references/api.md](references/api.md).

Before preparing or troubleshooting an H3 prompt, read [references/h3-prompt-guide.md](references/h3-prompt-guide.md). It covers actual dialogue versus camera/visual text, silence, reference/voice binding and enhancement preview.

Submit the original prompt. Every H3 video submission performs mandatory prompt processing, including structured input; there is no opt-out. If processing fails, stop generation and follow the refund path for any deducted credits. Previews cannot bypass submission checks or lock the later execution text. The optional `avoid_model_limitations` boolean defaults to `false` and controls adaptation only. The optional `unrestricted_enhancement` boolean (default `false`, CLI `--unrestricted-enhancement`) runs processing on an open model that does not refuse mature or sensitive creative themes; use it only when the user asks for it or the default processing refuses a legitimate creative prompt. Safety checks are unchanged.

## Setup

Set your API key:

```bash
export PHOSOR_API_KEY="your-api-key-here"
```

Get an API key at [phosor.ai](https://phosor.ai) → Settings → API Keys.

The CLI script is at `scripts/phosor_client.py`. All commands output JSON to stdout.

## Error handling

API diagnostics are in English regardless of the website language or
`Accept-Language`. Explain errors to the user in their preferred language, using
the HTTP status and documented error codes rather than matching English wording.
Keep any `request_id` / `X-Request-ID` for troubleshooting.

HTTP 503 with `error: maintenance` or `code: SYSTEM_UPGRADING` means the system is
being upgraded and this request was not accepted. Do not mark it as a failed
generation job or automatically resubmit it. Tell the user to wait until maintenance
ends; the public `GET /api/v1/system/status` endpoint reports `maintenance: true`
or `maintenance: false`. `Retry-After` is retry advice, not a completion estimate.
A generic 503 is temporary unavailability and does not establish a planned upgrade.

For 429 responses, inspect `reject_reason` / `X-Reject-Reason` and `Retry-After`
when provided. Distinguish API key quota, server capacity and queue wait limits.
See [references/api.md](references/api.md#error-codes) for the response contract.

## Base URL

The client talks to `https://phosor.ai` by default, over HTTPS. Get your key from phosor.ai → Settings → API Keys.

```bash
python3 scripts/phosor_client.py --api-key <your-key> check-key
```

The bundled client connects only to `https://phosor.ai` over HTTPS. Redirects are rejected.

Note: `studio-analyze` / `studio-suite` `--image-url` must be the **full https S3 URL** returned by `upload-image`, not the bare S3 key path — a bare key errors with `unsupported URL scheme`.

## H3 model map

Use an exact model ID. Each H3 mode has a Standard and Turbo variant; Turbo is the faster option for the same input shape. H3 uses duration, resolution tier, and aspect ratio rather than Wan's frame controls.

| Input | Standard | Turbo |
|------|----------|-------|
| Text to video | `minimax/h3/text-to-video` | `minimax/h3/text-to-video/turbo` |
| Image to video | `minimax/h3/image-to-video` | `minimax/h3/image-to-video/turbo` |
| Reference to video | `minimax/h3/reference-to-video` | `minimax/h3/reference-to-video/turbo` |

Choose Standard or Turbo from the exact model ID before submitting. H3 output is 24fps and billed per output second; see the pricing section for current rates.

## LLM chat — Qwen3.8 27B

`qwen3.8-27b` is a text model (category LLM) behind the OpenAI-compatible
`POST /api/v1/chat/completions`. Unlike the generation models it is **synchronous**:
the answer is in the response (or the SSE stream) — there is no `request_id`, `status` or `result` step.

```bash
# One-shot answer (JSON response on stdout, includes usage.credits_charged)
python3 scripts/phosor_client.py chat "Summarize the plot of Hamlet in 3 sentences." --max-tokens 300

# Stream text to stderr as it arrives; assembled JSON still goes to stdout
python3 scripts/phosor_client.py chat "Write a haiku about autumn." --stream

# System prompt, JSON mode, thinking, images (URL or local file, max 2, 4 MB each)
python3 scripts/phosor_client.py chat "Extract name and email" --system "Reply as JSON" --json-mode
python3 scripts/phosor_client.py chat "Is 391 prime?" --thinking --max-tokens 4096
python3 scripts/phosor_client.py chat "What is in this photo?" --image ./photo.jpg

# Full conversation or tool calling: pass OpenAI-format JSON (inline or @file)
python3 scripts/phosor_client.py chat --messages @messages.json --tools @tools.json --tool-choice auto
```

Rules an agent must follow:

- Send only the documented fields (`model`, `messages`, `max_tokens`, `temperature`, `top_p`, `stop`,
  `stream`, `stream_options`, `response_format`, `tools`, `tool_choice`, `enable_thinking`, `seed`,
  `presence_penalty`, `frequency_penalty`, `n`=1, `user`). Any other field returns `400 invalid_request`.
- Limits: 48K-token context, `max_tokens` 1–8192 (default 1024), at most 2 images per request.
- Cost: USD 0.2125 per 1M input tokens and USD 1.275 per 1M output tokens (2.125 / 12.75 credits).
  Credits for the estimated input plus `max_tokens` are reserved up front, then settled to actual use —
  keep `max_tokens` close to what you need. Thinking tokens are billed as output. Read
  `usage.credits_charged` from the response.
- `402 insufficient_credits`: lower `max_tokens` or ask the user to add credits.
  `429 rate_limited` (60 requests/min per key) or `429 capacity_busy`: wait `Retry-After` seconds, then retry.
  `503 service_unavailable`: not charged; retry later. Do not retry a `400` unchanged.

Direct HTTP (any OpenAI SDK works with `base_url="https://phosor.ai/api/v1"`):

```bash
curl https://phosor.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $PHOSOR_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3.8-27b","messages":[{"role":"user","content":"Hello"}],"max_tokens":256,"stream":true}'
```

Full field, streaming and error reference: [references/api.md](references/api.md#chat-completions-llm).

## Generation examples

Read [generation examples](references/generation-examples.md) for copyable video, image, speech and LoRA commands. Read only the section matching the selected model.

## CLI Commands

| Command | Description | Key Arguments |
|---------|-------------|---------------|
| `check-key` | Validate API key | — |
| `submit` | Submit inference job (T2V/I2V/S2V/Animate/T2I/I2I) | `prompt`, `--width`, `--height`, `--num-frames`, `--fps`, `--steps`, `--guidance`, `--image-url`, `--audio-url`, `--video-url`, `--lora-id`, `--lora-scale`, `--loras`, `--seed`, `--negative-prompt`, `--model`, `--num-images`, `--strength`, `--output-format` |
| `status` | Get job status | `request_id` |
| `result` | Get job result (video or image URL) | `request_id` |
| `poll` | Poll all pending jobs | — |
| `list` | List locally tracked pending jobs | — |
| `history` | Get job history | `--limit` |
| `upload-image` | Upload image for I2V or I2I | `file` |
| `import-image` | Import image from URL | `url`, `--filename` |
| `upload-lora` | Upload LoRA (two .safetensors for video) | `high_noise_file`, `low_noise_file`, `--name` |
| `import-lora` | Import LoRA from URLs (one or two files) | `high_noise_url`, `[low_noise_url]`, `--name` |
| `loras` | List LoRA models | `--limit`, `--offset` |
| `lora-status` | Get LoRA upload/import status | `lora_id` |
| `save-lora` | Activate a LoRA (extends expiry to 7 days) | `lora_id`, `--name` |
| `delete-lora` | Delete a LoRA model | `lora_id` |
| `chat` | Chat with the Qwen3.8 27B LLM (OpenAI-compatible, synchronous; `--stream` for SSE) | `prompt`, `--system`, `--messages`, `--image`, `--model`, `--max-tokens`, `--temperature`, `--top-p`, `--stop`, `--seed`, `--json-mode`, `--tools`, `--tool-choice`, `--thinking`, `--stream` |
| `submit-tts` | Submit a text-to-speech job (Qwen3-TTS) — keys off `text`, not a prompt | `text`, `--speaker`, `--language`, `--seed`, `--temperature`, `--top-p`, `--top-k`, `--repetition-penalty` |
| `models` | List available video/image models (static offline reference) | — |
| `studio-features` | List Image Studio endpoints, fields, billing (static offline reference) | — |
| `studio-pricing` | Get live Image Studio pricing | — |
| `studio-analyze` | AI-analyze a product/garment image or reference URL (freemium) | `--target agent\|product\|model\|reference`, `--image-url`, `--url`, `--prompt`, `--language` |
| `studio-layouts` | List the layout template library (query, then select) — static asset on the **web front** (phosor.ai), not a `/api/v1` endpoint; needs no key; on a self-hosted deployment set `PHOSOR_WEB_BASE_URL` if the web front is not the gateway host | `--module` (product\|clothing), `--type` (selling_point\|aplus\|white_bg\|scene\|closeup\|size_chart) |
| `studio-suite` | Generate a product image suite | `--image-url`, `--layout-types`, `--count-per-type`, `--custom-suggestions`, `--template-ids` (ids from `studio-layouts`, auto-expanded to custom_suggestions like the UI's manual pick — use this to get **text-callout selling-point / A+ layouts** and model templates), `--product-info`, `--aspect-ratio`, `--gen-language`, `--model`, `--same-style-reference` |
| `studio-clothing-suite` | Generate a model/garment image suite | `--image-urls`, `--main-image-types`, `--aplus-types`, `--product-info`, `--brand-config`, `--aspect-ratio`, `--gen-language`, `--model`, `--same-style-reference` |
| `studio-status` | Get Image Studio job status (separate id space, same `request_id` key) | `request_id` |
| `studio-cancel` | Cancel a running generation — queued images refunded, already-generating ones charged | `request_id` |
| `studio-my-works` | List past Image Studio generations | `--task-type`, `--limit`, `--offset` |
| `studio-call` | Generic call for any other Image Studio endpoint (remove-bg, replace, inpaint, erase, handheld, translate, outpaint, recolor, enhance, upscale, scene-compose, scene-variation, real-model-swap, mannequin-swap, model-scene-swap, ai-outfit, pose-variation, ai-wearable) | `method`, `path`, `--json` |

## Image Studio (Product & Model Photography)

Image Studio is a separate product surface for e-commerce sellers — AI product photography and model/clothing photography — reached through the **same gateway and API key** as video/LoRA, under the `/api/v1/image-studio` prefix. It has its own async namespace - the same key name `request_id`, but a **separate id space**: an Image Studio `request_id` is not valid on `/api/v1/inference/status/...` and vice versa - and its own pricing (flat per-image rate + freemium analyze quota, not per-frame). Full endpoint/parameter reference: [references/api.md](references/api.md#image-studio-product--model-photography--separate-product-surface).

### Quick Start: Product Suite

```bash
# 1. Upload the product photo
python3 scripts/phosor_client.py upload-image /path/to/product.jpg
# Returns: {"file_id": "img-xxx", "s3_key": "images/img-xxx.jpg", ...}

# 2. (Optional) AI-analyze it first for richer generation context
python3 scripts/phosor_client.py studio-analyze --target product --image-url "images/img-xxx.jpg"

# 3. Generate a product image suite
python3 scripts/phosor_client.py studio-suite --image-url "images/img-xxx.jpg" \
  --layout-types "white_background,lifestyle_scene" --count-per-type 2

# 4. Poll for the result
python3 scripts/phosor_client.py studio-status <request_id>
```

### Quick Start: Clothing/Model Suite

```bash
python3 scripts/phosor_client.py upload-image /path/to/garment.jpg
python3 scripts/phosor_client.py studio-clothing-suite \
  --image-urls "images/img-xxx.jpg" \
  --main-image-types '{"model_shot":2,"selling_point":1}' \
  --aplus-types '{"standard_aplus":1}'
python3 scripts/phosor_client.py studio-status <request_id>
```

### Quick Start: One-off Edits (remove-bg, inpaint, translate, etc.)

The long tail of single-purpose editing endpoints doesn't get a dedicated subcommand — use `studio-call` with the exact field names from [references/api.md](references/api.md#image-studio-product--model-photography--separate-product-surface):

```bash
python3 scripts/phosor_client.py studio-call POST /product/remove-bg \
  --json '{"image_url": "images/img-xxx.jpg", "count": 2}'
python3 scripts/phosor_client.py studio-status <request_id>
```

### Key facts

- **Every Image Studio call requires `X-API-Key`** (`PHOSOR_API_KEY`), including `GET /pricing` — there is no unauthenticated endpoint under this prefix.
- **All generation/analyze endpoints are async**: POST returns `{"request_id": "...", "status": "pending"}`; poll `studio-status <request_id>` until `status` is `"done"`, `"error"` or `"cancelled"`. Image Studio ids live in a **separate id space** from video/LoRA: Use `studio-status` for these IDs; `status`/`result` are for inference. The automatic `poll` command routes tracked Studio jobs to their own status endpoint.
- **Cancelling**: `POST /jobs/{request_id}/cancel` stops a running generation. Images still queued are refunded; images already generating are charged and cannot be stopped; images already delivered bill once through the normal path. The response reports the split as `refunded_queued`, `charged_running` and `already_done`, and the task then polls as `status: "cancelled"` - not an error.
- **Pricing is per-image, not per-frame**: call `studio-pricing` for the live rate. Partial success (e.g. 3 of 5 images) bills only the successes.
- **Analyze is freemium**: `agent/analyze`, `product/analyze`, `model/analyze` share a daily free quota before per-call billing kicks in.
- **`model_attrs` matters for model-photography endpoints** (real-model-swap, mannequin-swap, ai-outfit, ai-wearable) — pass `{gender, age_group, ethnicity, skin_tone, hair_color}` explicitly; it is not reliably inferred from the source image alone.
- Run `studio-features` for the full offline endpoint/field catalog without leaving the terminal.

## Key Constraints

### Video Resolutions (exact pairs only)

| Preset | Width × Height | Max Frames (turbo) | Max Frames (standard) |
|--------|---------------|-------------------|----------------------|
| 480p landscape | 854 × 480 | 161 | 161 |
| 480p portrait | 480 × 854 | 161 | 161 |
| 720p landscape | 1280 × 720 | 161 | 161 |
| 720p portrait | 720 × 1280 | 161 | 161 |
| 1080p landscape | 1920 × 1080 | 153 | **81** |
| 1080p portrait | 1080 × 1920 | 153 | **81** |

> Standard (non-turbo) mode: 1080p is capped at 81 frames due to generation time limits.

### S2V / Animate Video Resolutions (exact pairs only)

| Preset | Width x Height | Max Frames |
|--------|---------------|------------|
| 480p landscape | 854 x 480 | 161 |
| 480p portrait | 480 x 854 | 161 |
| 512p square | 512 x 512 | 161 |
| 720p landscape | 1280 x 720 | 161 |
| 720p portrait | 720 x 1280 | 161 |

### Image Resolutions (exact pairs only)

| Preset | Width × Height |
|--------|---------------|
| Square small | 512 × 512 |
| Square | 1024 × 1024 |
| Landscape | 1024 × 768 |
| Portrait | 768 × 1024 |
| Wide landscape | 1280 × 768 |
| Tall portrait | 768 × 1280 |

### MiniMax H3 Frame Sizes (`--resolution-tier` + `--aspect`)

| Tier | 16:9 | 4:3 | 1:1 | 3:4 | 9:16 |
|------|------|-----|-----|-----|------|
| 480p | 832 × 480 | 640 × 480 | 480 × 480 | 480 × 640 | 480 × 832 |
| 768p | 1344 × 768 | 1024 × 768 | 768 × 768 | 768 × 1024 | 768 × 1344 |

`duration` is 4–15 seconds (default 5). Output FPS is fixed at 24 and
`frames_per_second` is ignored.

### Ref2VA Reference Limits (`minimax/h3/reference-to-video`)

Caps differ per tier, and the image cap is higher when you send **only** images:

| Limit | 480p | 768p |
|-------|------|------|
| Reference images (with videos/audio present) | 5 | 5 |
| Reference images (images only) | 9 | 9 |
| Reference videos | 3 | 3 |
| Reference audios | 3 | 3 |

| Limit | Value |
|-------|-------|
| Total reference video length | 15.1 s (across all reference videos) |
| Reference video FPS ceiling | 24 |
| Reference audio length | 10 s each |
| Reference image longest edge | 2048 px |
| Reference image aspect ratio | ≤ 4.0 |

### FLUX.2-dev Resolutions (exact pairs only)

| Width × Height |
|---------------|
| 2048 × 1536 · 1536 × 2048 |
| 2048 × 1152 · 1152 × 2048 |
| 2048 × 2048 · 1024 × 1024 |

> FLUX.2-dev does not accept the general image resolution list above, and always
> returns exactly 1 image.

### Frame Alignment (video only)

Frames must follow `1 + 4*k` where `k >= 1` (e.g. 5, 9, 13, ... 81, 85, ...). Server auto-aligns down.

### Video Inference Parameters

| Parameter | Default | Range |
|-----------|---------|-------|
| `frames_per_second` | 16 | 4–60 |
| `num_inference_steps` | Model-dependent | Consult the selected model contract |
| `guidance_scale` | Model-dependent | Consult the selected model contract |

### Image Inference Parameters

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| `num_images` | 1 | 1–4 | Number of images to generate |
| `num_inference_steps` | varies | 1–4 (z-image turbo), 1–40 (qwen-image) | Model-dependent max |
| `guidance_scale` | varies | 1.0–20.0 | — |
| `strength` | — | 0.0–1.0 | Image-to-image only: how much to transform the source |
| `output_format` | png | png, jpeg | Output file format |

### Concurrency

Model API inference jobs run concurrently up to a per-account cap; over it the submit
returns `429` and you retry after a job finishes.

| Tier | Plan | Concurrent Model API jobs |
|------|------|---------------------------|
| Free | — | 1 |
| 1 | Starter | 2 |
| 2 | Standard | 4 |
| 3 | Pro | 8 |

Image Studio runs on its own pool and does **not** consume this quota — a suite and a
video generation can run at the same time.

### Multiple LoRAs

```bash
python3 scripts/phosor_client.py submit "A person dancing" \
  --loras '[{"lora_id": "lora-abc", "lora_scale": 0.8}, {"lora_id": "lora-def", "lora_scale": 0.5}]'
```

### Two-Step Upload Rule

Files must be uploaded before use — direct URLs are NOT supported in `submit --image-url`:

1. **Image** → `upload-image` / `import-image` → returns `s3_key` → use as `--image-url`
2. **LoRA** → `upload-lora` / `import-lora` → returns `lora_id` → use as `--lora-id`

## Queue Flow

```
PENDING → PROCESSING → COMPLETED / FAILED
```

The `poll` command checks all locally-tracked pending jobs and removes completed/failed ones.

## MiniMax H3 Pricing (per output second)

<!-- Generated H3 pricing: do not edit these rates by hand. -->

H3 charges per output second. Confirm currently effective rates with [GET /api/v1/pricing/config](https://phosor.ai/api/v1/pricing/config).

10 credits = USD 1. Prices and billing are in USD.

| Model | 480p USD/sec | 768p USD/sec | 480p credits/sec | 768p credits/sec |
|---|---:|---:|---:|---:|
| `text-to-video`, `image-to-video` | $0.0045 | $0.012 | 0.045 | 0.12 |
| `text-to-video/turbo`, `image-to-video/turbo` | $0.006 | $0.012 | 0.06 | 0.12 |
| `reference-to-video` | $0.0045 | $0.012 | 0.045 | 0.12 |
| `reference-to-video/turbo` | $0.006 | $0.012 | 0.06 | 0.12 |

Reference-to-video adds reference inputs to the output charge:

| Model | Tier | Output USD/sec | Reference images | Reference audio USD/clip | Reference video USD/sec |
|---|---|---:|---|---:|---:|
| `reference-to-video` | 480p | $0.0045 | first 5 free, then $0.0075 each | $0 | $0.0045 |
| `reference-to-video` | 768p | $0.012 | first 5 free, then $0.0075 each | $0 | $0.012 |
| `reference-to-video/turbo` | 480p | $0.006 | first 5 free, then $0.0025 each | $0 | $0.006 |
| `reference-to-video/turbo` | 768p | $0.012 | first 5 free, then $0.0025 each | $0 | $0.012 |

```text
inputs_usd = round(max(image_count - free_image_count, 0) * image_rate
                   + audio_count * audio_rate
                   + round(sum(actual_reference_video_seconds), 3) * reference_video_rate, 6)
total_usd = round(output_billable_seconds * output_rate + inputs_usd, 6)
total_credits = round(total_usd * 10, 4)
```

Reference video uses the actual combined duration of all clips, even when longer than the output; it is not capped at output duration. Reference audio remains free. Rounding follows the Gateway (Python rounding).

Turbo 768p example: 5 output seconds + 9 images + 14.75 reference-video seconds + 3 audio clips = USD 0.247.

Existing task charges remain as recorded; current rates do not reprice past tasks.

## Wan Video Pricing (per frame)

| Tier | Standard | + LoRA | Turbo |
|------|----------|--------|-------|
| 480p | $0.0009375 | $0.00125 | $0.0003125 |
| 512p | $0.0013125 | $0.001625 | $0.0004375 |
| 720p | $0.001875 | $0.0021875 | $0.000625 |
| 1080p | $0.0025 | $0.003 | $0.0010938 |

LoRA multiplier on turbo: 1.2x.

## S2V Pricing (per frame)

| Tier | Cost |
|------|------|
| 480p | $0.0009375 |
| 512p | $0.0013125 |
| 720p | $0.001875 |

## Animate Pricing (per frame)

| Tier | Cost |
|------|------|
| 480p | $0.00125 |
| 512p | $0.00175 |
| 720p | $0.0025 |

## Image Pricing (per image)

| Model | USD | Credits |
|-------|-----|---------|
| GPT Image 2 T2I | $0.03 | 0.3 |
| FLUX.2-dev T2I | $0.006 | 0.06 |
| FLUX.2-dev Image Edit | $0.012 | 0.12 |
| qwen-image T2I | $0.015 | 0.15 |
| qwen-image T2I + LoRA | $0.018 | 0.18 |
| qwen-image-edit | $0.003 | 0.03 |
| z-image turbo (T2I / I2I) | $0.0025 | 0.025 |
| z-image turbo + LoRA | $0.003 | 0.03 |

Flat per image at every resolution. Multiply by `num_images` (1–4) where the model
supports it; FLUX.2-dev is fixed at 1 image per request.

GPT Image 2, like FLUX.2-dev, is fixed at one image per request.

## Availability and business boundaries

Model API prices do not price Image Studio suites or Drama workflows. Use their
own contracts and price sources. Use model IDs returned by the current model catalog.

Price reference checked 2026-11-04; live Model API prices take precedence. A price
configuration is not proof of submission availability or successful delivery.

## LLM Pricing (per 1M tokens)

| Model | Input | Output | Input credits | Output credits |
|-------|-------|--------|---------------|----------------|
| `qwen3.8-27b` | $0.2125 | $1.275 | 2.125 | 12.75 |

Billed on actual `usage` (cached input at the input rate, thinking tokens as output);
each response reports `usage.credits_charged`.

## Audio Pricing

| Item | Cost |
|------|------|
| Qwen3-TTS | $0.00003 per character |
| Minimum charge | $0.003 per request |

Exchange rate: 10 credits = $1 USD. Credits pre-deducted, auto-refunded on failure.
Live rates: `GET /api/v1/pricing/config` — always prefer it over any table here.

<!-- H3-IMAGE-PRICING -->
## MiniMax H3 Image pricing

Text-to-image: `minimax/h3/text-to-image`. Fixed price per generated image:

| Resolution tier | USD/image | credits/image |
|---|---:|---:|
| 1K | 0.0175 | 0.1750 |
| 1.5K | 0.0180 | 0.1800 |
| 2K | 0.0187 | 0.1870 |
| 3K | 0.0338 | 0.3380 |
| 4K | 0.0550 | 0.5500 |

1 USD = 10 credits. USD and credits use at most four decimal places. Billing uses the supported width/height preset's pixel-area tier; do not infer a tier from the longest edge or invent custom sizes. PNG/JPEG/WebP and aspect ratio do not add a surcharge within a tier. One image per request. Check the target environment's `/api/v1/pricing/config` for effective prices before submission; availability follows that environment's model catalog. Prompt processing runs automatically and is not a configurable API parameter.
<!-- /H3-IMAGE-PRICING -->

## MiniMax H3 Image quick start

```bash
python3 scripts/phosor_client.py submit "A ceramic cup in soft daylight" \
  --model minimax/h3/text-to-image --width 1024 --height 1024 --output-format webp
```

One image per request. Use exact supported dimensions. Prompt processing is automatic.
For reference-to-video labels, use `--reference-image-labels '["Alice", "Garden"]'`
with two reference image URLs in the same order; video and audio labels work likewise.

Wan Turbo uses service-selected frame counts and FPS; do not infer output duration
from requested frame controls. Confirm the model contract before quoting duration.
