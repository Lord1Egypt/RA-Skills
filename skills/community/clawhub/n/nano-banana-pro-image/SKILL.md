---
name: nano-banana-pro
description: "Generate and edit images using Google's Nano Banana Pro (Gemini 3 Pro Image / Imagen Pro) — the premium AI image generation model optimized for professional asset production with advanced reasoning ('Thinking'), high-fidelity text rendering, and complex multi-turn creation. Supports text-to-image and image editing with up to 6 reference images, resolutions up to 4K, and 14+ aspect ratios. Available via Atlas Cloud API. Use this skill whenever the user wants to generate high-quality professional images, create AI art with precise text, edit photos with AI, produce marketing assets, infographics, menus, diagrams, or any visual content requiring detailed text rendering. Also trigger when users mention Nano Banana Pro, Gemini 3 Pro Image, Imagen Pro, or ask for premium/professional-grade AI image generation, concept art, product photography, or visual assets with complex compositions."
source: "https://github.com/AtlasCloudAI/nano-banana-2-skill"
homepage: "https://github.com/AtlasCloudAI/nano-banana-2-skill"
metadata:
  openclaw:
    requires:
      env:
        - ATLASCLOUD_API_KEY
    primaryEnv: ATLASCLOUD_API_KEY
---

# Nano Banana Pro Image Generation & Editing

Generate and edit images using Google's Nano Banana Pro (Gemini 3 Pro Image) — the premium AI image generation model designed for professional asset production, utilizing advanced reasoning ("Thinking") to follow complex instructions and render high-fidelity text in images.

Nano Banana Pro excels at infographics, menus, diagrams, marketing assets, and any task requiring precise text rendering and complex multi-object composition.

> **Data usage note**: This skill sends text prompts and image URLs/data to Atlas Cloud API for image generation. No data is stored locally beyond the downloaded output files.

> **Security note**: API keys are read exclusively from environment variables (`ATLASCLOUD_API_KEY`) and passed via HTTP headers — never embedded in URL query strings or command arguments. All user-provided text (prompts, file paths) must be passed through JSON request bodies to prevent shell injection. When constructing curl commands, always use a JSON payload (`-d '{...}'`) rather than string interpolation in the shell. File paths should be validated before use. The skill does not execute any user-provided code — it only sends structured API requests and downloads output files.

---

## Nano Banana Pro vs Nano Banana 2

| Feature | Nano Banana Pro | Nano Banana 2 |
|---------|:--------------:|:-------------:|
| Focus | Professional quality, complex tasks | Speed, high-volume generation |
| Text rendering | Superior — best for infographics, menus | Good |
| Thinking mode | Enabled by default | Not available |
| Reference images (object) | Up to 6 | Up to 10 |
| Character consistency images | Up to 5 | Up to 14 |
| Resolution | Up to 4K | Up to 4K |

Choose Nano Banana Pro when quality and text precision matter. Choose Nano Banana 2 when speed and cost matter.

---

## Pricing

| Resolution | Atlas Cloud Standard | Atlas Cloud Developer |
|:----------:|:-------------------:|:--------------------:|
| **1K** | $0.126 | $0.098 |
| **2K** | $0.126 | $0.098 |
| **4K** | $0.126 | $0.098 |

Atlas Cloud uses flat-rate pricing regardless of resolution.

---

## Available Models

| Model ID | Tier | Price | Best For |
|----------|------|-------|----------|
| `google/nano-banana-pro/text-to-image` | Standard | $0.126/image | Production, high-quality output |
| `google/nano-banana-pro/text-to-image-developer` | Developer | $0.098/image | Prototyping, experiments |
| `google/nano-banana-pro/edit` | Standard | $0.126/image | Production editing |
| `google/nano-banana-pro/edit-developer` | Developer | $0.098/image | Budget editing, experiments |

---

## Atlas Cloud API

### Setup
1. Sign up at https://www.atlascloud.ai
2. Console → API Keys → Create new key
3. Set env: `export ATLASCLOUD_API_KEY="your-key"`

### Parameters

**Text-to-Image:**

| Parameter | Type | Required | Default | Options |
|-----------|------|----------|---------|---------|
| `prompt` | string | Yes | - | Image description |
| `aspect_ratio` | string | No | 1:1 | 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |
| `resolution` | string | No | 1k | 1k, 2k, 4k |
| `output_format` | string | No | png | png, jpeg |

**Image Editing** — same as above plus:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `images` | array of strings | Yes | 1-10 image URLs to edit |

### Workflow: Submit → Poll → Download

```bash
# Step 1: Submit
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateImage" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/nano-banana-pro/text-to-image",
    "prompt": "A professional infographic showing quarterly revenue growth with bar charts and annotations",
    "aspect_ratio": "16:9",
    "resolution": "2k"
  }'
# Returns: { "code": 200, "data": { "id": "prediction-id" } }

# Step 2: Poll (every 3-5 seconds until "completed" or "succeeded")
curl -s "https://api.atlascloud.ai/api/v1/model/prediction/{prediction-id}" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY"
# Returns: { "code": 200, "data": { "status": "completed", "outputs": ["https://...url..."] } }

# Step 3: Download
curl -o output.png "IMAGE_URL_FROM_OUTPUTS"
```

**Image editing example:**

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateImage" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/nano-banana-pro/edit",
    "prompt": "Replace the text on the sign with: Grand Opening Sale — 50% Off",
    "images": ["https://example.com/storefront.jpg"],
    "resolution": "2k"
  }'
```

**Polling logic:**
- `processing` / `starting` / `running` → wait 3-5s, retry (Pro model may take longer than Nano Banana 2 due to Thinking mode)
- `completed` / `succeeded` → done, get URL from `data.outputs[]`
- `failed` → error, read `data.error`

### Atlas Cloud MCP Tools (if available)

If the Atlas Cloud MCP server is configured, use built-in tools:

```
atlas_quick_generate(model_keyword="nano banana pro", type="Image", prompt="...")
atlas_generate_image(model="google/nano-banana-pro/text-to-image", params={...})
atlas_get_prediction(prediction_id="...")
```

---

## Implementation Guide

1. **Check API key**: Ensure `ATLASCLOUD_API_KEY` is set. If not, ask the user to sign up at https://www.atlascloud.ai and set `export ATLASCLOUD_API_KEY="your-key"`.

2. **Extract parameters**:
   - Prompt: the image description — Nano Banana Pro handles complex, detailed prompts well
   - Aspect ratio: infer from context (infographic→3:4 or 9:16, banner→16:9, menu→3:4, social post→1:1)
   - Resolution: default 1k, use 2k/4k for professional output
   - For editing: identify source image URL(s) or local file path

3. **Choose model tier**:
   - Standard for production use
   - Developer if user wants to save costs or is experimenting

4. **Sanitize inputs**: Ensure user-provided prompts and file paths do not contain shell metacharacters. Always pass prompts inside JSON payloads (never via shell interpolation). Validate that image file paths exist and are readable before encoding.

5. **Execute**: POST to Atlas Cloud generateImage API → poll prediction (may take 10-30s due to Thinking mode) → download result

6. **Present result**: show file path, offer to open

## Prompt Tips for Nano Banana Pro

Nano Banana Pro excels at understanding complex, structured prompts. Take advantage of its Thinking mode:

- **Text in images**: Include exact text in quotes — Pro renders text with high fidelity. Example: `"A cafe chalkboard menu reading: 'Today's Special — Matcha Latte $5.50'"`
- **Infographics**: Describe data, layout, and annotations. Example: `"An infographic showing 3 steps of coffee brewing with numbered icons and captions"`
- **Marketing assets**: Specify brand colors, text placement, and style. Example: `"A product banner with dark background, gold accents, text 'Limited Edition' top-center"`
- **Complex compositions**: Describe spatial relationships and multiple objects. Example: `"A still life with a ceramic vase left-center, three oranges arranged in front, and a linen cloth draped over the table edge"`
- **Style**: "photorealistic", "editorial illustration", "minimalist flat design", "watercolor"
- **Lighting**: "studio lighting", "natural window light", "dramatic chiaroscuro"
