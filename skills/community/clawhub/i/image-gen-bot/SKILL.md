---
name: image-gen-bot
description: Generate images from text prompts using FLUX via Together.ai. Returns image URL. Prompts are auto-enhanced for best results.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "🎨"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# Image Gen Bot

Generate images from natural language descriptions using FLUX.1-schnell via Together.ai. Accepts any text prompt — prompts are automatically enhanced by Claude before generation for better visual results. Returns a URL to the generated image.

## When to Use

- Generating logos, icons, or brand visuals for projects
- Creating illustrations or artwork for content
- Visualizing concepts, products, or designs
- Generating images for reports or presentations
- Any task requiring original visual output from a text description

## Usage Flow

1. Provide a `task` string describing the desired image
2. Optionally set `width`, `height` (default 1024×1024, max 1440)
3. Optionally set `steps` (default 4, max 8 — higher = slower but better quality)
4. AIProx enhances your prompt via Claude, then routes to FLUX generation
5. Returns an `image_url` with the generated image

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Network | api.together.xyz | Image generation (server-side) |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "a minimalist logo for an AI agent marketplace, dark background, cyan circuit board accents, clean sans-serif typography",
    "spend_token": "$AIPROX_SPEND_TOKEN"
  }'
```

## Make Request — With Dimensions

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "wide banner illustration of autonomous robots collaborating in a glowing digital city",
    "width": 1344,
    "height": 768,
    "spend_token": "$AIPROX_SPEND_TOKEN"
  }'
```

### Response

```json
{
  "image_url": "https://together-cdn.com/generated/flux-abc123.png",
  "prompt": "A minimalist logo featuring a stylized circuit board node pattern arranged in a circular emblem. Dark charcoal background (#1a1a2e), vibrant cyan accent lines (#00e5ff), clean geometric shapes suggesting connectivity and intelligence. Modern sans-serif wordmark below.",
  "width": 1024,
  "height": 1024,
  "model": "FLUX.1-schnell"
}
```

## Trust Statement

Image Gen Bot generates images based on prompts you provide. Generated images are returned via URL from Together.ai's CDN and are not stored by AIProx. Prompts are enhanced transiently by Claude and not logged beyond the transaction. Your spend token is used for payment only.
