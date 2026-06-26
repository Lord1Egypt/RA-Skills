---
name: gemini-image-gen
description: Generate images using Google Gemini via OpenRouter API. Supports text-to-image and reference-image-guided generation. Use when the user asks to generate, create, draw, or design images/illustrations/covers/avatars.
---

# Gemini Image Generation

Generate images via `google/gemini-3.1-flash-image-preview` on OpenRouter. Cheap ($0.25/M in, $1.5/M out), fast, good quality.

## Quick Start

```bash
python3 scripts/generate.py "a watercolor illustration of a cozy café" -o output.png
```

With reference image (style/character guidance):
```bash
python3 scripts/generate.py "same character but waving hello" -o wave.png --ref reference.png
```

Script path: `skills/gemini-image-gen/scripts/generate.py`

## Requirements

- `OPENROUTER_API_KEY` environment variable (or `--api-key` flag)
- Python 3.10+ (stdlib only, no pip installs needed)

## How It Works

1. Calls OpenRouter `/chat/completions` with `modalities: ["text", "image"]`
2. Optionally encodes a reference image as base64 in the message
3. Extracts generated image from `choices[0].message.images[0].image_url.url` (data:image/png;base64,...)
4. Decodes and saves to output path

## Prompt Engineering Tips (from experience)

### Aspect Ratio & Composition
- Gemini respects aspect ratio instructions in the prompt
- For vertical (e.g. phone wallpaper, Xiaohongshu cover): add "vertical composition, 3:4 aspect ratio"
- For horizontal (e.g. banner): add "horizontal composition, 16:9 aspect ratio"
- For square: add "square composition, 1:1 aspect ratio"
- **Always specify** — without it, Gemini defaults to roughly square and may crop awkwardly

### Character Consistency
- When using `--ref`, describe the character features explicitly in the prompt AND provide the reference image
- Key details to specify: hair color/style, eye color, clothing, accessories, expression
- Example: "same character from reference: silver-to-ice-blue gradient shoulder-length hair, ice-blue eyes, cream cardigan over light blue shirt, snowflake earring"
- Gemini is decent at maintaining consistency but drifts on small details — always re-specify distinguishing features

### Style Control
- Name the art style explicitly: "soft watercolor illustration", "anime cel-shading", "photorealistic", "flat vector", "oil painting"
- For warm/cozy tone: "warm color palette, cream and peach gradient background, bokeh light spots"
- For dark/moody: "dark gradient background, deep navy to black, subtle glow effects"
- Mentioning a well-known art style works: "in the style of Studio Ghibli", "Makoto Shinkai lighting"

### Text in Images
- Gemini can render short text in images but it's unreliable for CJK characters
- For English text: works reasonably well if you specify font style ("bold sans-serif", "handwritten script")
- For Chinese/Japanese: **avoid** — it usually garbles characters. Add text overlays with a separate tool (e.g. ImageMagick, Pillow) instead

### Common Pitfalls
- **Body proportions**: Gemini sometimes compresses/distorts figures. Add "natural human body proportions, do not squash or stretch" for character art
- **Hands**: Still a weak spot. Minimize visible hands or describe hand pose explicitly
- **Multiple subjects**: More than 2-3 subjects increases inconsistency. Keep scenes focused
- **Batch generation**: For generating multiple variations, run the script multiple times — each call is independent. Do NOT ask for "4 options" in one prompt

## Sending Images on Feishu

⚠️ **Critical**: Images must be saved to a path within `localRoots` (typically your OpenClaw workspace dir). `/tmp` is NOT whitelisted on Feishu.

```python
# Save to workspace, not /tmp
output_path = "my_image.png"  # relative to workspace

# Send via message tool:
#   media: "file://<workspace_path>/my_image.png"
#   (use 'media' parameter, NOT 'filePath')
```

After sending, clean up temporary images to avoid workspace clutter.

## Advanced: Calling from Python (without CLI)

```python
import os, sys
sys.path.insert(0, "skills/gemini-image-gen/scripts")
from generate import generate

generate(
    prompt="a cute robot reading a philosophy book",
    output="robot.png",
    ref_image=None,  # or path to reference image
)
```

## Model Alternatives

| Model | Cost | Notes |
|-------|------|-------|
| `google/gemini-3.1-flash-image-preview` | $0.25/$1.5 per M tokens | **Default.** Best balance of cost and quality |
| `google/gemini-3.1-pro-preview` | $2/$12 per M tokens | Higher quality but 8x more expensive |
| `openai/gpt-image-1` | varies | OpenAI's image model, different API format — not supported by this script |

## Troubleshooting

- **"No image in response"**: Check `.debug.json` file created alongside output. Usually means the prompt triggered safety filters or the model returned text-only.
- **Garbled/distorted output**: Try rephrasing. Add "high quality, detailed" and be more specific about composition.
- **API error 429**: Rate limited. Wait 30s and retry.
- **API error 402**: Insufficient credits on OpenRouter.
