---
name: fal-image-gen
description: Generate images via fal.ai and BytePlus Seedream APIs. Supports single image, batch parallel, and reference-guided generation. Use when you need to generate a photo, poster, or visual asset from a text prompt or reference images.
metadata: {"category": "image-generation", "tags": ["fal", "flux", "seedream", "image-gen", "reference-guided", "batch"], "runtime": "python", "env": ["FAL_API_KEY", "BYTEPLUS_API_KEY"]}
---

# FAL Image Generation

Generate professional images via fal.ai and BytePlus Seedream APIs.

## Environment Variables

```bash
export FAL_API_KEY="your_fal_api_key"
export BYTEPLUS_API_KEY="your_byteplus_api_key"  # for Seedream backend
```

## Model Router

Two backends available. The agent can offer model choice to users, or auto-select based on task.

### Backend: fal.ai

| Task | Model | Flag | Price |
|------|-------|------|-------|
| Reference-guided (i2i) | `fal-ai/nano-banana-pro/edit` | (default when refs provided) | $0.15 |
| Text-to-image | `fal-ai/flux-2-pro` | (default when no refs) | ~$0.05 |
| Poster/Infographic (t2i) | `fal-ai/nano-banana-pro` | `--model nbp` | $0.15 |
| Text in image | `fal-ai/ideogram/v3` | — | — |

**NBP strengths**: Best text rendering (5/5), JSON structured prompts, 4K resolution.

### Backend: BytePlus Seedream

| Task | Model | Flag | Price |
|------|-------|------|-------|
| Text-to-image | `seedream-4-5-251128` | `--model seedream` | **$0.03** |
| Reference-guided (i2i) | `seedream-4-5-251128` | `--model seedream --refs ...` | **$0.03** |

**Seedream strengths**: 5x cheaper, up to 14 reference images, natural color rendering with proper prompting.

### Model Aliases

| Alias | Routes to |
|-------|-----------|
| `seedream`, `byteplus`, `sd` | BytePlus Seedream |
| `nbp`, `nano-banana-pro`, `poster` | fal.ai NBP t2i |
| `flux`, `flux-2-pro` | fal.ai Flux |

### Auto-Selection Logic

```
User specifies model → use that model
No model specified → BytePlus Seedream (DEFAULT — $0.03, best photo quality)
"--model nbp" or "--model poster" → fal.ai NBP (when text rendering is critical)
"--model flux" → fal.ai Flux (fast t2i fallback)
"--model fal" → fal.ai default routing (NBP for refs, Flux for no refs)
```

**Why Seedream default**: 5x cheaper ($0.03 vs $0.15), supports up to 14 refs, excellent photo realism, proper aspect ratio control (1920x2400 for 4:5, etc.).

### Desaturation (per-model)

Each backend needs different color control:
- **Seedream** → Lighting-based or Magazine editorial description
- **NBP** → Kodak Portra 400 analog film description

## Script Usage

Place the generation script at `{baseDir}/skills/fal-image-gen/scripts/generate.py`.

### Single Image
```bash
uv run {baseDir}/skills/fal-image-gen/scripts/generate.py \
  --prompt "A mountain temple at golden hour, low angle, 24mm f/8..." \
  --aspect-ratio 9:16 \
  --output {baseDir}/output/
```

### With Reference Images
```bash
uv run {baseDir}/skills/fal-image-gen/scripts/generate.py \
  --prompt "..." \
  --refs "https://img1.jpg" "https://img2.jpg" \
  --aspect-ratio 4:5
```

### Seedream (BytePlus) — Text-to-Image
```bash
uv run {baseDir}/skills/fal-image-gen/scripts/generate.py \
  --prompt "Travel poster with dramatic mountain scenery..." \
  --model seedream \
  --output {baseDir}/output/
```

### Seedream (BytePlus) — With Reference Images
```bash
uv run {baseDir}/skills/fal-image-gen/scripts/generate.py \
  --prompt "Using this poster layout, create..." \
  --model seedream \
  --refs "https://example.com/ref1.jpg" "https://example.com/ref2.jpg" \
  --output {baseDir}/output/
```

### Poster Mode — NBP (JSON Structured Prompt)
```bash
uv run {baseDir}/skills/fal-image-gen/scripts/generate.py \
  --prompt '{"meta":{...},"poster_structure":{...},"design_style":{...}}' \
  --model nano-banana-pro \
  --aspect-ratio 3:4 \
  --output {baseDir}/output/
```

### Batch Parallel (from JSON)
```bash
uv run {baseDir}/skills/fal-image-gen/scripts/generate.py \
  --prompts-json batch.json \
  --output {baseDir}/output/
```

JSON format for batch (mix models freely):
```json
[
  {"prompt": "...", "refs": ["url1", "url2"], "aspect_ratio": "9:16", "label": "scene_a"},
  {"prompt": "...", "model": "seedream", "refs": ["url1"], "label": "scene_b"},
  {"prompt": "{...json...}", "model": "nano-banana-pro", "label": "poster"}
]
```

## Output

- Images saved to `output/YYYY-MM-DD/` with descriptive filenames
- Prints `MEDIA: /path/to/image.png` for gateway delivery
- Each `MEDIA:` line triggers the gateway to send the image

## Aspect Ratio Guide

| Platform | Ratio | Notes |
|----------|-------|-------|
| Xiaohongshu / Stories | 9:16 | Vertical full-screen |
| Instagram Feed (2026) | 3:4 | New optimal — taller than 4:5, more screen real estate |
| Instagram Feed (legacy) | 4:5 | Still supported, less tall |
| Instagram Carousel | 3:4 | Mixed carousels = highest engagement (2.33%) |
| Banner / Website | 16:9 | Landscape |
| Square | 1:1 | Generic / WeChat Moments |
| Poster (default) | 3:4 | Best for designed travel posters |

## Limits

| Backend | Max refs | Speed | Cost |
|---------|----------|-------|------|
| **BytePlus Seedream** | **14** | ~15-40s | **$0.03/img** |
| fal.ai NBP | 4 | ~15-25s | $0.15/img |
| fal.ai Flux | 0 | ~5-10s | ~$0.05/img |

- Batch: generates all images in parallel (async), can mix backends
- BytePlus URLs expire after 24 hours — script auto-uploads to fal.ai storage for permanent URLs

## Resolution Tiers (Seedream)

Use `--resolution` flag (or `"resolution"` key in batch JSON):

| Tier | Pixels (4:5) | Total | Best For |
|------|-------------|-------|----------|
| `standard` | 1920x2400 | ~4.6M | Social media, fast generation |
| `high` (default) | 2560x3200 | ~8M | Download, zoom, high quality |
| `max` | 3200x4000 | ~12.8M | Print, ultra-high quality |

API limits: min 3,686,400 px, max 16,777,216 px.

```bash
# Standard (fast, social media)
uv run generate.py --prompt "..." --resolution standard

# High (default)
uv run generate.py --prompt "..."

# Max (print quality)
uv run generate.py --prompt "..." --resolution max
```
