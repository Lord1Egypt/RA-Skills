# Phosor AI API Reference

## Contents

- [Endpoints](#endpoints)
- [Video Inference Submit Parameters](#video-inference-submit-parameters)
- [S2V Inference Submit Parameters](#s2v-inference-submit-parameters)
- [Animate Inference Submit Parameters](#animate-inference-submit-parameters)
- [Image Inference Submit Parameters](#image-inference-submit-parameters)
- [Supported Video Resolutions](#supported-video-resolutions)
- [Supported S2V / Animate Resolutions](#supported-s2v--animate-resolutions)
- [Supported Image Resolutions](#supported-image-resolutions)
- [Pricing](#pricing)
- [Concurrency Limits](#concurrency-limits)
- [Limits & Quotas](#limits--quotas)
- [Response Formats](#response-formats)
- [Chat Completions (LLM)](#chat-completions-llm)
- [H3 prompt and dialogue preparation](#h3-prompt-and-dialogue-preparation)
- [MiniMax H3 Image pricing](#minimax-h3-image-pricing)

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
| POST | `/api/v1/inference/submit` | Submit video or image generation job |
| GET | `/api/v1/inference/status/{request_id}` | Get job status + progress |
| GET | `/api/v1/inference/result/{request_id}` | Get completed result (video or image URL) |
| GET | `/api/v1/inference/history` | Get user's job history |

### Chat (LLM)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/chat/completions` | OpenAI-compatible chat completions for `qwen3.8-27b` (alias `/v1/chat/completions`). Synchronous or SSE streaming — no `request_id` polling |

### Storage — Image / Audio

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/storage/image/upload` | Multipart image or audio upload (images: jpg/png/webp; audio for S2V: mp3/wav/flac/aac/ogg/m4a) |
| POST | `/api/v1/storage/image/import` | Import from public URL |

### Storage — LoRA

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/storage/lora/upload` | Upload two .safetensors files (video LoRA: high_noise + low_noise) |
| POST | `/api/v1/storage/lora/import` | Import from HTTPS URLs (video: two files, image: single file) |

### LoRA Management

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/loras` | List LoRA models |
| GET | `/api/v1/loras/{lora_id}` | Get single LoRA details |
| GET | `/api/v1/loras/{lora_id}/status` | Get processing status |
| POST | `/api/v1/loras/{lora_id}/save` | Activate a LoRA (extend expiry to 7 days) |
| DELETE | `/api/v1/loras/{lora_id}` | Soft delete |

### Image Studio (product & model photography — separate product surface)

All paths below are relative to `/api/v1/image-studio` (e.g. the full path for `/product/suite` is `/api/v1/image-studio/product/suite`). **Every path requires `X-API-Key`, including `GET /pricing`** — there is no unauthenticated Image Studio endpoint.

All generation/analyze endpoints are async: POST returns `{"request_id": "...", "status": "pending"}` immediately; poll `GET /jobs/{request_id}` until `status` is `"done"`, `"error"` or `"cancelled"`.

> Use the returned `request_id` with the Image Studio status endpoint. Image Studio IDs and inference IDs belong to separate namespaces.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/agent/analyze` | AI-analyze an image for the Agent-image workflow (freemium) |
| POST | `/product/analyze` | AI-analyze a product image ahead of `product/suite` (freemium) |
| POST | `/model/analyze` | AI-analyze a garment image ahead of `model/clothing-suite` (freemium) |
| POST | `/product/reference/analyze` | Analyze a reference product page/image for style-matching (free) |
| POST | `/product/suite` | Generate a product image suite (multiple layout types) |
| POST | `/product/scene-compose` | Composite a product into a reference scene |
| POST | `/product/scene-variation` | Generate scene/background variations of a product photo |
| POST | `/product/remove-bg` | Remove background (transparent) |
| POST | `/product/replace` | Replace/refresh the product in an existing scene composite |
| POST | `/product/inpaint` | Masked region fill |
| POST | `/product/erase` | Masked region removal |
| POST | `/product/handheld` | Generate a hand-holding-product shot |
| POST | `/product/translate` | Translate on-image text to other language(s) |
| POST | `/product/outpaint` | Expand canvas beyond original image bounds |
| POST | `/product/recolor` | Recolor product or region |
| POST | `/product/enhance` | AI enhancement/upgrade pass |
| POST | `/product/upscale` | Upscale to 1024×1024 |
| POST | `/model/clothing-suite` | Generate a full garment/model image suite (model shots, selling points, size chart, A+ modules) |
| POST | `/model/real-model-swap` | Swap in a real human model wearing the garment |
| POST | `/model/mannequin-swap` | Swap in a mannequin wearing the garment |
| POST | `/model/model-scene-swap` | Swap the scene/background behind an existing model photo |
| POST | `/model/ai-outfit` | Dress a described model in the garment |
| POST | `/model/ai-wearable` | Generate a model wearing/using an accessory |
| POST | `/model/pose-variation` | Generate pose variations from a source model photo |
| GET | `/jobs/{request_id}` | Poll job status/result (Image Studio's own async namespace) |
| GET | `/pricing` | Live pricing: `per_image_credits`, `per_analyze_credits`, `analyze_daily_free_quota` |
| GET | `/my-works` | List past Image Studio generations (paginated) |
| GET | `/my-works/{request_id}` | One past generation with its inputs and outputs |
| GET | `/my-works/{request_id}/download` | Download the generated images (single file or archive) |
| DELETE | `/my-works/{request_id}` | Soft-delete a past generation |
| POST | `/jobs/{request_id}/cancel` | Cancel a running generation. See "Cancelling" below |
| POST | `/tasks/{task_id}/review` | Submit a per-image review (thumbs) for a finished task |
| GET | `/tasks/{task_id}/review` | Read the review already submitted for a task |
| POST | `/feedback` | Send feedback about a generation |

#### Common parameters

| Parameter | Applies to | Notes |
|-----------|-----------|-------|
| `image_url` | analyze + most edit endpoints | S3 key or URL of the source image; some endpoints alias this as `product_image_url` |
| `model` | all generation endpoints | Optional. Accepted values: `openai:gpt-image-2` and `phosor:phosor-model-api` (Phosor's image model). Analyze endpoints do not take this parameter |
| `aspect_ratio` | most generation endpoints | One of `1:1`, `3:4`, `4:3`, `9:16`, `16:9` (default varies per endpoint, e.g. `3:4` for clothing-suite, `1:1` for most product tools) |
| `count` | most single-image-in-single-image-out endpoints | How many output images to generate, typically clamped 1–20 (varies per endpoint) |
| `prompt` | analyze + most edit endpoints | Free-text hint appended to the service template — not a full prompt replacement |
| `same_style_reference` | `product/suite`, `model/clothing-suite` | Object from a prior `product/reference/analyze` call, used to match layout/style to a reference image |
| `model_attrs` | model-photography endpoints (`real-model-swap`, `mannequin-swap`, `ai-outfit`, `ai-wearable`) | `{gender, age_group, ethnicity, skin_tone, hair_color}` — **required for accurate results**, not reliably inferred from the source image alone |

#### `POST /product/suite` body

| Field | Required | Notes |
|-------|----------|-------|
| `product_image_url` | Yes | (or `image_url`) |
| `layout_types` | No | list[str] of layout type ids |
| `count_per_type` | No | int, default 1 |
| `custom_suggestions` | No | list |
| `product_info` | No | free-text product description/facts (authoritative over what the AI guesses from the image) |
| `same_style_reference` | No | dict from `product/reference/analyze` |
| `brand_config` | No | dict — brand color/font/platform/tone settings |
| `aspect_ratio` | No | `1:1`\|`3:4`\|`4:3`\|`9:16`\|`16:9` |
| `gen_language` | No | language for any on-image text |
| `model` | No | see Common parameters |

Billed count = `len(layout_types) * count_per_type + len(custom_suggestions)` (min 1).

#### `POST /model/clothing-suite` body

| Field | Required | Notes |
|-------|----------|-------|
| `clothing_image_urls` | Yes | list[str], up to 5 used for generation |
| `main_image_types` | No | dict of `{model_shot\|grass_shot\|selling_point\|size_chart: count}` |
| `aplus_types` | No | dict of `{standard_aplus\|mobile_aplus\|basic_aplus\|custom_ratio: count}` |
| `product_info` | No | free-text |
| `brand_config` | No | dict |
| `same_style_reference` | No | dict |
| `aspect_ratio` | No | default `3:4` |
| `gen_language` | No | |
| `model` | No | |

Billed count = sum of all `main_image_types`/`aplus_types` counts (min 1). At least one image type must be selected, or a 400 is returned. Job result includes `grouped_images: [{label, url}]` with a display label per image type (model photo, lifestyle, selling point, size chart, premium A+, mobile A+, standard A+, custom ratio; labels are returned in Chinese), plus `failed_labels` for any type that failed to generate (partial success is normal, not an error state).

#### `GET /jobs/{request_id}` response shape

- `status: "pending"` — includes `partial_images: [{url, label}]` for images completed so far (useful for progressive UIs).
- `status: "done"` — includes `result` (shape varies by feature; generation results always have `images`, `expected_count`, `success_count`; `clothing-suite` also has `grouped_images`/`failed_labels`; analyze results include the AI's structured findings plus `remaining_free_quota`, `daily_free_quota`, `is_free`).
- `status: "error"` — includes a user-facing `error` string (never a raw provider error).

## Video Inference Submit Parameters

| Parameter | Type | Required | Default | Range |
|-----------|------|----------|---------|-------|
| `prompt` | string | Yes | — | Model-specific input and processing limits apply |
| `model` | string | No | `wan/v2.2-a14b/text-to-video` | See supported models |
| `width` | int | No | 854 | See video resolutions |
| `height` | int | No | 480 | See video resolutions |
| `num_frames` | int | No | 81 | Auto-aligned to 1+4k |
| `frames_per_second` | int | No | 16 | 4–60 |
| `num_inference_steps` | int | No | Model-dependent | Consult the selected model contract |
| `guidance_scale` | float | No | Model-dependent | Consult the selected model contract |
| `seed` | int | No | random | — |
| `negative_prompt` | string | No | "" | Not supported by `minimax/h3/*` models; omit this field |
| `image_url` | string | No | — | S3 key from upload-image (required for I2V) |
| `lora_id` | string | No | — | Single LoRA |
| `lora_scale` | float | No | 1.0 | 0.0–1.0 |
| `loras` | array | No | — | Multiple LoRAs: `[{"lora_id":"...","lora_scale":1.0}]` |

## S2V Inference Submit Parameters

Uses the same `/api/v1/inference/submit` endpoint. Set `model` to `wan/v2.2-a14b/speech-to-video`.

| Parameter | Type | Required | Default | Range |
|-----------|------|----------|---------|-------|
| `prompt` | string | Yes | — | Model-specific input and processing limits apply |
| `model` | string | Yes | — | `wan/v2.2-a14b/speech-to-video` |
| `image_url` | string | Yes | — | S3 key from upload-image (reference face image) |
| `audio_url` | string | Yes | — | S3 key from `/api/v1/storage/image/upload` (accepts mp3, wav, flac, aac, ogg, m4a) |
| `width` | int | No | 854 | See S2V/Animate resolutions |
| `height` | int | No | 480 | See S2V/Animate resolutions |
| `num_frames` | int | No | 81 | Auto-aligned to 1+4k |
| `frames_per_second` | int | No | 16 | 4–60 |
| `num_inference_steps` | int | No | Model-dependent | Consult the selected model contract |
| `guidance_scale` | float | No | Model-dependent | Consult the selected model contract |
| `seed` | int | No | random | — |
| `negative_prompt` | string | No | "" | — |

## Animate Inference Submit Parameters

Uses the same `/api/v1/inference/submit` endpoint. Set `model` to `wan/v2.2-a14b/animate`.

| Parameter | Type | Required | Default | Range |
|-----------|------|----------|---------|-------|
| `prompt` | string | Yes | — | Model-specific input and processing limits apply |
| `model` | string | Yes | — | `wan/v2.2-a14b/animate` |
| `image_url` | string | Yes | — | S3 key from upload-image (reference character image) |
| `video_url` | string | Yes | — | URL to motion/pose reference video |
| `width` | int | No | 854 | See S2V/Animate resolutions |
| `height` | int | No | 480 | See S2V/Animate resolutions |
| `num_frames` | int | No | 81 | Auto-aligned to 1+4k |
| `frames_per_second` | int | No | 16 | 4–60 |
| `num_inference_steps` | int | No | Model-dependent | Consult the selected model contract |
| `guidance_scale` | float | No | Model-dependent | Consult the selected model contract |
| `seed` | int | No | random | — |
| `negative_prompt` | string | No | "" | — |

## Image Inference Submit Parameters

Uses the same `/api/v1/inference/submit` endpoint. Set `model` to an image model ID.

| Parameter | Type | Required | Default | Range |
|-----------|------|----------|---------|-------|
| `prompt` | string | Yes | — | Model-specific input and processing limits apply |
| `model` | string | Yes | — | Must be an image model ID (see below) |
| `width` | int | No | 1024 | See image resolutions |
| `height` | int | No | 1024 | See image resolutions |
| `num_images` | int | No | 1 | 1–4 |
| `num_inference_steps` | int | No | varies | 1–8 (z-image turbo), 1–40 (qwen-image) |
| `guidance_scale` | float | No | varies | 1.0–20.0 |
| `seed` | int | No | random | — |
| `negative_prompt` | string | No | "" | — |
| `image_url` | string | No | — | S3 key from upload-image (required for I2I) |
| `strength` | float | No | — | 0.0–1.0 (I2I only: transformation strength) |
| `output_format` | string | No | "png" | "png" or "jpeg" |
| `lora_id` | string | No | — | Single LoRA |
| `lora_scale` | float | No | 1.0 | 0.0–1.0 |
| `loras` | array | No | — | Multiple LoRAs: `[{"lora_id":"...","lora_scale":1.0}]` |

### Wan Video Model IDs

| Model ID | Description |
|----------|-------------|
| `wan/v2.2-a14b/text-to-video` | Wan 2.2 T2V 14B — standard quality (`num_inference_steps`, `guidance_scale` apply) |
| `wan/v2.2-a14b/text-to-video/turbo` | Wan 2.2 T2V turbo — service-selected settings, ~3x cheaper per frame |
| `wan/v2.2-a14b/image-to-video` | Wan 2.2 I2V 14B — standard quality |
| `wan/v2.2-a14b/image-to-video/turbo` | Wan 2.2 I2V turbo |

> Turbo variants ignore `num_inference_steps` / `guidance_scale`. Standard mode caps
> 1080p at 81 frames; turbo allows 153.

### LTX-Video Model IDs

| Model ID | Type | Required inputs |
|----------|------|-----------------|
| `ltx-video/v2.3/image-audio-to-video` | Image(+Audio)-to-Video | `prompt`, `image_url`; `audio_url` optional |

Frame-based. `resolution_tier` + `aspect_ratio` (`480p`/`720p`/`1080p` × `16:9`/`9:16`/`1:1`)
or explicit `width`/`height` from: 854×480, 1280×720, 1920×1080, 480×854, 720×1280, 1080×1920,
480×480, 720×720, 1080×1080. Default 1280×720, fps 24, duration 5s
(`num_frames` = `duration × fps + 1`). Max frames: 480p 481, 720p 241, 1080p 121 —
**not** subject to the Wan `1+4k` alignment.

Pricing reference checked 2026-11-04: 480p USD 0.0008/frame; 720p USD 0.0012/frame.
Use supported size presets only. Confirm current prices before quoting 1080p. A 121-frame 720p request estimates USD 0.1452.

### MiniMax H3 Model IDs

Duration-based (ignores `num_frames` / `frames_per_second`; output is fixed 24fps).

| Model ID | Type | Required inputs |
|----------|------|-----------------|
| `minimax/h3/text-to-video` | Text-to-Video | `prompt`
| `minimax/h3/text-to-video/turbo` | Text-to-Video Turbo | `prompt` |
| `minimax/h3/image-to-video` | Image-to-Video | `prompt`, `image_url`
| `minimax/h3/image-to-video/turbo` | Image-to-Video Turbo | `prompt`, `image_url` (optional `end_image_url`) |
| `minimax/h3/reference-to-video` | Reference-to-Video | `prompt`, plus at least one of `reference_image_urls` / `reference_video_urls` |
| `minimax/h3/reference-to-video/turbo` | Reference-to-Video Turbo | `prompt`, plus at least one of `reference_image_urls` / `reference_video_urls` |

| Parameter | Default | Allowed values |
|-----------|---------|----------------|
| `resolution_tier` | `480p` | `480p`, `768p` |
| `aspect_ratio` | `16:9` | `16:9`, `4:3`, `1:1`, `3:4`, `9:16` |
| `duration` | `5` | 4–15 seconds |
| `reference_audio_urls` | — | array; Ref2VA only |
| `reference_image_labels` | — | array, same order as `reference_image_urls`; what each picture shows (e.g. `["Shen Yu - character", "A Man - character", "coop - scene"]`) |
| `reference_video_labels` | — | array, same order as `reference_video_urls` |
| `reference_audio_labels` | — | array, same order as `reference_audio_urls` |
| `use_ref_video_audio` | `false` | also use each reference video's own soundtrack |

Frame sizes: 480p → 832×480 (16:9), 640×480 (4:3), 480×480 (1:1), 480×640 (3:4), 480×832 (9:16).
768p → 1344×768, 1024×768, 768×768, 768×1024, 768×1344.

**Naming your references.** Uploaded files are stored under generated ids, so a prompt
that says "Shen Yu reaches into the coop" cannot be matched to a picture by name on its own.
Pass `reference_image_labels` alongside `reference_image_urls` (same order) and the platform
binds each name in your prompt to the right picture while building the model prompt.
With reference labels, write names naturally. Without labels, positional picture references can identify the assets.

**Ref2VA reference caps** — differ per tier and per variant, and the image cap is
higher when sending images only:

`minimax/h3/reference-to-video`

| Limit | 480p | 768p |
|-------|------|------|
| Reference images (with videos/audio) | 5 | 5 |
| Reference images (images only) | 9 | 9 |
| Reference videos | 3 | 3 |
| Reference audios | 3 | 3 |

Total reference video length 15.1s (all videos combined), reference video FPS ≤ 24,
reference audio ≤ 10s each, reference image longest edge ≤ 2048px, aspect ratio ≤ 4.0.

### Audio Model IDs

| Model ID | Description |
|----------|-------------|
| `qwen3-tts/text-to-speech/1.7b` | Qwen3-TTS CustomVoice — takes `text` (≤500 chars), not `prompt` |

Parameters: `text` (required), `speaker` (default `Sohee`), `language` (default `Chinese`),
`seed`, `temperature` (0.0–2.0, default 0.9), `top_p` (default 1.0), `top_k` (1–200, default 50),
`repetition_penalty` (1.0–2.0, default 1.05).

### S2V / Animate Model IDs

| Model ID | Description |
|----------|-------------|
| `wan/v2.2-a14b/speech-to-video` | Wan 2.2 Speech-to-Video 14B (lip-sync from audio + face image) |
| `wan/v2.2-a14b/animate` | Wan 2.2 Animate 14B (motion transfer from video + character image) |

### Image Model IDs

| Model ID | Description |
|----------|-------------|
| `openai/gpt-image-2/text-to-image` | GPT Image 2 Text-to-Image — 5 sizes: **1024×1024**, **1920×1072** / **1072×1920** (1080p), **2560×1440** / **1440×2560** (2K). Always 1 image; ignores `num_inference_steps` / `guidance_scale` / `output_format` |
| `flux2/dev/text-to-image` | FLUX.2-dev Text-to-Image — own resolution whitelist, always 1 image |
| `flux2/dev/image-edit` | FLUX.2-dev Image Edit |
| `qwen-image/v2512/text-to-image` | Qwen Image 2512 Text-to-Image |
| `qwen-image/v2512/text-to-image/lora` | Qwen Image 2512 T2I with LoRA |
| `qwen-image/v2511/image-edit` | Qwen Image Edit 2511 — multi-image reference editing |
| `z-image/turbo/text-to-image` | Z-Image Turbo Text-to-Image |
| `z-image/turbo/text-to-image/lora` | Z-Image Turbo T2I with LoRA |
| `z-image/turbo/image-to-image` | Z-Image Turbo Image-to-Image |
| `z-image/turbo/image-to-image/lora` | Z-Image Turbo I2I with LoRA |

## Supported Video Resolutions

| Preset | Width | Height | Max Frames (turbo) | Max Frames (standard) |
|--------|-------|--------|-------------------|----------------------|
| 480p landscape | 854 | 480 | 161 | 161 |
| 480p portrait | 480 | 854 | 161 | 161 |
| 720p landscape | 1280 | 720 | 161 | 161 |
| 720p portrait | 720 | 1280 | 161 | 161 |
| 1080p landscape | 1920 | 1080 | 153 | 81 |
| 1080p portrait | 1080 | 1920 | 153 | 81 |

Only these exact pairs are accepted. Frame alignment: `valid_frames = 1 + 4*k` where `k >= 1`.

> Standard (non-turbo) model: 1080p max is 81 frames due to generation time constraints.

## Supported S2V / Animate Resolutions

| Preset | Width | Height | Max Frames |
|--------|-------|--------|------------|
| 480p landscape | 854 | 480 | 161 |
| 480p portrait | 480 | 854 | 161 |
| 512p square | 512 | 512 | 161 |
| 720p landscape | 1280 | 720 | 161 |
| 720p portrait | 720 | 1280 | 161 |

Only these exact pairs are accepted. Frame alignment: `valid_frames = 1 + 4*k` where `k >= 1`.

## Supported Image Resolutions

| Preset | Width | Height |
|--------|-------|--------|
| Square small | 512 | 512 |
| Square | 1024 | 1024 |
| Landscape | 1024 | 768 |
| Portrait | 768 | 1024 |
| Wide landscape | 1280 | 768 |
| Tall portrait | 768 | 1280 |

Only these exact pairs are accepted.

## Pricing

> Video/image inference pricing below is a static reference and can drift — verify against support before relying on it for billing-sensitive integrations. Image Studio has its own pricing surface with a live endpoint (`GET /api/v1/image-studio/pricing`) — always prefer that over any static table for Image Studio.

### Video Inference (10 credits = $1 USD)

| Resolution | Per-Frame (USD) | Per-Frame (Credits) |
|-----------|----------------|-------------------|
| 480p | $0.0009375 | 0.009375 |
| 720p | $0.001875 | 0.01875 |
| 1080p | $0.0025 | 0.025 |

LoRA multiplier: 1.2x (applied when any LoRA is specified).

### MiniMax H3 (per output second)

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

### S2V Inference (10 credits = $1 USD)

| Resolution | Per-Frame (USD) | Per-Frame (Credits) |
|-----------|----------------|-------------------|
| 480p | $0.0009375 | 0.009375 |
| 512p | $0.0013125 | 0.013125 |
| 720p | $0.001875 | 0.01875 |

### Animate Inference (10 credits = $1 USD)

| Resolution | Per-Frame (USD) | Per-Frame (Credits) |
|-----------|----------------|-------------------|
| 480p | $0.00125 | 0.0125 |
| 512p | $0.00175 | 0.0175 |
| 720p | $0.0025 | 0.025 |

### Image Inference (10 credits = $1 USD)

| Model | Per Image (USD) | Per Image (Credits) |
|-------|----------------|-------------------|
| GPT Image 2 T2I | $0.03 | 0.3 |
| FLUX.2-dev T2I | $0.006 | 0.06 |
| FLUX.2-dev Image Edit | $0.012 | 0.12 |
| qwen-image T2I | $0.015 | 0.15 |
| qwen-image T2I + LoRA | $0.018 | 0.18 |
| qwen-image-edit | $0.003 | 0.03 |
| z-image turbo | $0.0025 | 0.025 |
| z-image turbo + LoRA | $0.003 | 0.03 |

GPT Image 2 and FLUX.2-dev are fixed at one image per request. For batch-capable models, total cost = per-image price x accepted `num_images` (1-4). LoRA pricing is built into the model-specific rate (no separate multiplier).

### LLM chat (per 1M tokens, 10 credits = $1 USD)

| Model | Input | Output | Input credits | Output credits |
|-------|-------|--------|---------------|----------------|
| `qwen3.8-27b` | $0.2125 | $1.275 | 2.125 | 12.75 |

Cached input is billed as input; thinking tokens are billed as output. A reservation for estimated input + `max_tokens` is placed when the request starts and settled to actual `usage` when it ends. Each response reports `usage.credits_charged`.

### Audio (10 credits = $1 USD)

| Item | Cost |
|------|------|
| Qwen3-TTS | $0.00003 per character |
| Minimum charge | $0.003 per request |

### Image Studio Pricing

Image Studio (see below) charges a **flat per-image rate for every generation endpoint**, and a **freemium daily-quota rate for analyze endpoints**. Both numbers are computed live server-side — call `GET /api/v1/image-studio/pricing` (or `phosor_client.py studio-pricing`) to get the current `per_image_credits`, `per_analyze_credits`, and `analyze_daily_free_quota`. Partial success (e.g. 3 of 5 images generated) bills only the successes; the rest is auto-refunded.

## Concurrency Limits

Model API inference jobs run concurrently up to a per-account cap; going over returns `429`.

| Tier | Plan | Concurrent Model API jobs |
|------|------|---------------------------|
| Free | — | 1 |
| 1 | Starter | 2 |
| 2 | Standard | 4 |
| 3 | Pro | 8 |

> Image Studio runs on its own pool and does not consume this quota.

## Limits & Quotas

| Resource | Limit |
|----------|-------|
| Rate limit | 1000 requests / 60 seconds per API key |
| Concurrent jobs | Tier-based: Free=1, Starter=2, Standard=4, Pro=8 |
| Max API keys per user | 10 |
| Max LoRAs per user (total) | 20 |
| LoRA file format | `.safetensors` only (video: two files high_noise + low_noise; image: single file) |
| Max LoRA file size | 2048 MB |
| Uploaded LoRA expiry | 1 day (auto-cleaned) |
| Saved LoRA expiry | 7 days from save (auto-cleaned) |
| Max image file size | 20 MB |
| Max video file size | 50 MB |
| Image formats | JPEG, PNG, WebP |
| Queue timeout | 3000s (auto-refund) |
| Execution timeout | 2400s inference (auto-refund) |

## Response Formats

### Models Response
```json
{"models": [{"model_id": "wan/v2.2-a14b/text-to-video", "description": "Wan 2.2 Text-to-Video 14B", "model_type": "video", "model_mode": "text-to-video", "metadata": {}}]}
```

### Submit Response
```json
{"request_id": "<request_id>", "status": "queued"}
```

### Status Response
```json
{"request_id": "...", "status": "queued|processing|completed|failed", "progress": 0-100}
```

### Result Response (Video)
```json
{"data": {"video": {"url": "..."}, "seed": 12345}, "request_id": "..."}
```

### Result Response (Image)
```json
{"data": {"image": {"url": "..."}, "images": [{"url": "..."}, ...], "seed": 12345}, "request_id": "..."}
```

`data.images` is an array of all generated images. `data.image` is the first image (backward-compatible).

### Error Codes
| Code | Meaning |
|------|---------|
| 400 | Validation error |
| 401 | Invalid API key or email not verified |
| 402 | Insufficient credits |
| 404 | Job not found |
| 429 | Rate limit or concurrency limit exceeded |
| 503 | Temporary unavailability, including maintenance when identified by its error code |

Error diagnostics are English and do not change with the website language or
`Accept-Language`. UI clients and agents may translate their explanation locally.
Preserve HTTP statuses, codes and request identifiers; do not depend on message wording.

During maintenance, new submissions return HTTP 503 with `Retry-After: 600`:

```json
{
  "error": "maintenance",
  "code": "SYSTEM_UPGRADING",
  "message": "The system is being upgraded. Your request was not accepted. Please try again after maintenance ends.",
  "retry_after": 600
}
```

No task is created by this rejection. Wait until maintenance ends before submitting
again; do not automatically resubmit. The public `GET /api/v1/system/status`
returns `{"maintenance":true}` or `{"maintenance":false}` (additional fields may
be present). Retry advice is not an upgrade completion estimate. Ordinary 503
responses without the maintenance marker do not prove an upgrade is in progress.
For HTTP 429, distinguish `capacity`, `quota` and `queue-depth` using
`reject_reason` / `X-Reject-Reason` when provided, and follow `Retry-After`.


## Chat Completions (LLM)

`POST https://phosor.ai/api/v1/chat/completions` — OpenAI Chat Completions format. OpenAI SDKs: `base_url="https://phosor.ai/api/v1"`, `api_key=<Phosor key>`, `model="qwen3.8-27b"`.

**Auth:** `X-API-Key: <key>` or `Authorization: Bearer <key>`. The account email must be verified.

**Model:** `qwen3.8-27b` (Qwen3.8 27B) — text + up to 2 images in, text out; 48K-token context; `max_tokens` 1–8192 (default 1024).

**Accepted fields (anything else → 400 `invalid_request`):**

| Field | Notes |
|-------|-------|
| `model` | required, `qwen3.8-27b` |
| `messages` | required; roles `system` / `user` / `assistant` / `tool`; `content` is a string or parts `[{"type":"text","text":...}, {"type":"image_url","image_url":{"url":...}}]` |
| `max_tokens` | 1–8192, default 1024; `max_completion_tokens` is an alias |
| `temperature`, `top_p`, `seed`, `presence_penalty`, `frequency_penalty`, `user` | standard |
| `stop` | string or up to 4 strings |
| `stream`, `stream_options` | SSE when `stream: true`; the final usage chunk is always sent |
| `response_format` | `{"type":"json_object"}` (JSON mode) or `{"type":"text"}` |
| `tools`, `tool_choice` | OpenAI function-tool format |
| `enable_thinking` | Phosor extension, default `false`; reasoning returned in `message.reasoning_content` (stream: `delta.reasoning_content`) |
| `n` | `1` only |

**Images:** at most 2 per request across all messages; `https://` URL or `data:image/(png|jpeg|webp);base64,...`; 4 MB or smaller each.

**Response:** OpenAI `chat.completion`; `id` = `chatcmpl-<request_id>`; `usage` = `{prompt_tokens, completion_tokens, total_tokens, credits_charged}`.

**Streaming:** `data: {chat.completion.chunk}` events, then `data: [DONE]`. The last data chunk before `[DONE]` carries `usage` incl. `credits_charged` (its `choices` may be empty). A stream without `[DONE]` is incomplete.

**Errors** — `{"error": {"message", "type", "code"}}`:

| HTTP | `code` | Action |
|------|--------|--------|
| 400 | `invalid_request` | Fix the body (unknown field, model, images, `max_tokens`, `n`); do not retry unchanged |
| 401 | `invalid_api_key` | Check the key |
| 402 | `insufficient_credits` | Lower `max_tokens` or add credits |
| 403 | `email_not_verified` | Verify the account email |
| 429 | `rate_limited` | 60 requests/min per key exceeded; wait `Retry-After` / back off |
| 429 | `capacity_busy` | Model at capacity (not queued); wait `Retry-After` seconds |
| 503 | `service_unavailable` | Temporarily unavailable, not charged; retry later |

**Rate limit:** 60 chat requests/min per API key. Chat does not use the per-account concurrent job slots of `/api/v1/inference/submit`.

```bash
curl https://phosor.ai/api/v1/chat/completions \
  -H "X-API-Key: $PHOSOR_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3.8-27b","messages":[{"role":"user","content":"Hello"}],"max_tokens":256}'
```

## H3 prompt and dialogue preparation

Read [h3-prompt-guide.md](h3-prompt-guide.md) for reference binding, actual spoken words, silence and enhancement. POST `/api/v1/inference/prompt/enhance` previews text without creating a video job; check `enhanced` and `reason`.

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
