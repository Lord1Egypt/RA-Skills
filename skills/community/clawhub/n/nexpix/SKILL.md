---
name: nexpix
description: "AI image generation via Cloudflare Workers AI (free tier, FLUX models) with premium EvoLink fallback. Use when generating images from text prompts, creating visual assets, product mockups, or social media graphics. Triggers: 'generate image', 'create image', 'nexpix', '/canvas', image generation requests. Supports CLI, programmatic API, Discord slash commands, and Telegram bot integration. Zero cost on free tier (10K neurons/day)."
---

# NexPix — Cloudflare Image Generation

Two-tier image generation with intelligent routing. Free by default.

## Quick Start

### CLI

```bash
# Generate an image (free tier)
nexpix "a sunset over the ocean with sailboats"

# Specify size
nexpix "cyberpunk cityscape" --size 1024x768

# Premium quality (EvoLink fallback)
nexpix "product photo of a clay jar" --quality premium

# Force a specific route
nexpix "logo design" --route workers-ai
nexpix "4K wallpaper" --route evolink

# Check usage/quota
nexpix --status
```

### Programmatic

```javascript
const nexpix = require('./nexpix');

const result = await nexpix.generate({
  prompt: "a futuristic city at night",
  quality: "standard",   // standard | premium
  width: 1024,
  height: 1024,
});

console.log(result.filepath);  // local path to saved image
console.log(result.source);    // 'workers-ai' or 'evolink'
console.log(result.cost);      // 0 for free tier
```

### Messaging Integration

```
Discord:  /canvas a mountain landscape at dawn
Telegram: /canvas a mountain landscape at dawn
```

See `references/messaging-integration.md` for slash command manifests.

## Architecture

### Routing Logic

1. **Standard quality** → Cloudflare Workers AI (free, FLUX.1-schnell)
2. **Premium / 4K quality** → EvoLink API (~$0.12-0.20/image)
3. **Image editing / img2img** → EvoLink (Workers AI is text-only)
4. **Quota > 90% used** → Auto-fallback to EvoLink
5. **Workers AI failure** → Auto-fallback to EvoLink

### Models (Workers AI — Free Tier)

| Model | Speed | Quality | Key |
|-------|-------|---------|-----|
| FLUX.1-schnell | ~1-3s | Good | `flux-schnell` (default) |
| FLUX.2-dev | ~5-10s | Great | `flux-2-dev` |
| Stable Diffusion XL | ~3-5s | Good | `sdxl` |
| DreamShaper 8 LCM | ~2-4s | Good | `dreamshaper` |

### Pricing Tiers

| Tier | Cost | Limit | Provider |
|------|------|-------|----------|
| **Free** | $0/month | 10K neurons/day (~50-100 images) | Cloudflare Workers AI |
| **Pro** | ~$0.12-0.20/image | Unlimited | EvoLink API |
| **Enterprise** | Custom | Custom | Self-hosted Workers |

## Requirements

- **Cloudflare account** with Workers AI enabled
- **API token** stored at `ACCESS/cloudflare-workers-ai.env`
- **Node.js** 18+
- *Optional:* `EVOLINK_API_KEY` for premium fallback

## File Layout

| File | Purpose |
|------|---------|
| `nexpix.js` | Core module (routing, generation, tracking) |
| `bin/nexpix` | CLI entry point |
| `scripts/deploy-worker.sh` | Deploy/update Cloudflare Worker |
| `references/messaging-integration.md` | Discord + Telegram setup |

## Output

Images saved to `~/.openclaw/media/workers-ai/` (free) or `~/.openclaw/media/evolink/` (premium).

Print `MEDIA:<absolute_path>` for OpenClaw auto-attach.

## Usage Tracking

All generations logged to `notes/image-gen-tracking.json`:
- Daily neuron usage vs quota
- Cost per image ($0 for free tier)
- Cumulative savings vs paid alternatives
- Generation history (last 500)

Check with `nexpix --status` or programmatically via `nexpix.getStatus()`.

## Installation

```bash
clawhub install nexpix
```
