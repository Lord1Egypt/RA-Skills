---
name: imageflare
description: "Generate and edit images using Cloudflare Workers AI via the `imageflare` CLI. Use when: user asks to generate an image from a text prompt, edit/transform an existing image with AI, or manage Cloudflare AI image model settings. NOT for: non-image AI tasks, local image editing without AI (cropping, resizing), or video generation."
homepage: https://github.com/Sallytion/Imageflare
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires": { "bins": ["imageflare"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "imageflare",
              "bins": ["imageflare"],
              "label": "Install imageflare (pip)",
            },
          ],
      },
  }
---

# ImageFlare Skill

Generate and edit images from your terminal using Cloudflare Workers AI models (Flux, Stable Diffusion, etc.).

## When to Use

✅ **USE this skill when:**

- User asks to generate an image from a text description
- User wants to edit or transform an existing image with AI
- User wants to apply a style from a reference image to another image
- User asks to configure Cloudflare AI credentials or switch models
- User says "create an image", "generate a picture", "edit this photo with AI"

## When NOT to Use

❌ **DON'T use this skill when:**

- Local image manipulation without AI (crop, resize, rotate) → use `convert`/`ffmpeg`/Pillow
- Video generation → not supported
- Non-Cloudflare AI image generation → use other tools
- Viewing or inspecting image metadata → use `identify`, `exiftool`
- The user has not configured Cloudflare credentials yet and doesn't want to → prompt them to run `imageflare config` first

## Setup

Requires a [Cloudflare account](https://dash.cloudflare.com) with [Workers AI](https://developers.cloudflare.com/workers-ai/) access (free tier available).

```bash
# First-time interactive setup (Account ID + API Token + model selection)
imageflare config
```

**Getting credentials:**

| Credential | Where to find it |
|---|---|
| **Account ID** | [Cloudflare dashboard](https://dash.cloudflare.com) → right sidebar of any page |
| **API Token** | *My Profile → API Tokens → Create Token* — select the **Workers AI** template or grant `Workers AI: Read` permission |

Verify setup:

```bash
imageflare config show
```

## Commands

### Generate an Image

```bash
# Basic generation
imageflare generate --prompt "a red fox sitting on a snow-covered log"

# With custom dimensions and seed for reproducibility
imageflare generate --prompt "a sunset over mountains" --width 512 --height 512 --seed 42

# Save to specific path and auto-open
imageflare generate --prompt "cyberpunk cityscape" --output cityscape.png --open

# Use a specific model
imageflare generate --prompt "a cat" --model "@cf/black-forest-labs/flux-1-schnell"
```

### Edit an Existing Image

```bash
# Basic edit
imageflare edit photo.png --prompt "change the background to a beach"

# Edit with a style reference image (up to 3 refs)
imageflare edit photo.png --ref style.png --prompt "style image 0 like image 1"

# Multiple reference images
imageflare edit photo.png --ref ref1.png --ref ref2.png --prompt "combine styles"

# Save to specific path
imageflare edit photo.png --prompt "make it a watercolor painting" --output watercolor.png --open
```

### Configuration

```bash
# Interactive setup wizard
imageflare config

# View current settings
imageflare config show

# List available AI models on your account
imageflare config models

# Set values non-interactively
imageflare config set --account-id YOUR_ID --api-token YOUR_TOKEN
imageflare config set --model "@cf/black-forest-labs/flux-1-schnell"
```

## Common Options

| Flag | Description |
|------|-------------|
| `-p, --prompt` | Text prompt describing what to generate or how to edit (required) |
| `-m, --model` | Cloudflare Workers AI model ID (overrides configured default) |
| `--width` | Output width in pixels (default: 1024) |
| `--height` | Output height in pixels (default: 1024) |
| `--seed` | Random seed for reproducible results |
| `-o, --output` | Output file path (default: `imageflare_<timestamp>.png`) |
| `--open` | Open the saved image automatically after generation |
| `-r, --ref` | (edit only) Additional reference image, repeatable up to 3 times |

## Output

- Images are saved as PNG files
- Default filename: `imageflare_<timestamp>.png` in the current directory
- Use `--output` to specify a custom path
- Use `--open` to auto-open the result in the system image viewer

## Notes

- **Default model:** `@cf/black-forest-labs/flux-2-klein-4b`
- Input images for editing are automatically resized to ≤512×512 (Cloudflare requirement)
- Reference images in edit mode: refer to them in your prompt as `image 0`, `image 1`, etc.
- Config is stored at `~/.config/imageflare/config` (Linux/macOS) or `%APPDATA%\imageflare\config` (Windows)
- No intermediate servers — requests go directly to the Cloudflare Workers AI API
- Free tier available on Cloudflare Workers AI
