---
name: nanobanana-plus
description: "Use nanobanana-plus CLI to generate images with per-call model switching and aspect ratio control. Direct CLI invocation - no server required. Supports: node nanobanana-plus.mjs generate --prompt 'desc' --filename 'out.png' [--aspect-ratio 16:9] [--model gemini-3.1-flash-image-preview]. Also supports check and models."
version: 1.5.4
license: Apache-2.0
homepage: https://github.com/webkubor/nanobanana-plus
store: https://clawhub.ai/webkubor/nanobanana-plus
author: webkubor
compatibility:
  platforms:
    - openclaw
metadata:
  openclaw:
    emoji: "🍌"
    requires:
      bins: ["node"]
    install:
      - id: node-brew
        kind: brew
        formula: node
        bins: ["node"]
        label: "Install Node.js (brew)"
---

# nanobanana-plus for OpenClaw

Direct CLI invocation - no HTTP server required.

## Quick Start

```bash
# Set your API key (once)
export NANOBANANA_GEMINI_API_KEY="your_key_here"

# Generate an image
node nanobanana-plus.mjs generate --prompt "a cute cat" --filename cat.png
```

## Commands

### Generate Image

```bash
node nanobanana-plus.mjs generate \
  --prompt "一只橘猫坐在雨天窗台上" \
  --filename "cat-window.png" \
  --aspect-ratio "16:9"
```

**Options:**

| Flag             | Description                                 |
| ---------------- | ------------------------------------------- |
| `--prompt`       | Image description (required)                |
| `--filename`     | Output file path                            |
| `--aspect-ratio` | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9` |
| `--model`        | Model name (see below)                      |
| `--output-count` | Number of images (1-8)                      |

### List Available Models

```bash
node nanobanana-plus.mjs models
```

### Health Check

```bash
node nanobanana-plus.mjs check
```

## Models

| Model                            | Description                                               |
| -------------------------------- | --------------------------------------------------------- |
| `gemini-3.1-flash-image-preview` | Nano Banana 2 (default) - fast, quota-efficient           |
| `gemini-3-pro-image-preview`     | Nano Banana Pro - higher quality                          |
| `imagen-4.0-ultra-generate-001`  | Imagen 4 Ultra - best realism (requires Pro key)          |
| `imagen-4.0-fast-generate-001`   | Imagen 4 Fast - balanced speed/quality (requires Pro key) |

Example with specific model:

```bash
node nanobanana-plus.mjs generate \
  --prompt "majestic snowy mountain, photorealistic" \
  --filename mountain.png \
  --model "gemini-3-pro-image-preview" \
  --aspect-ratio "16:9"
```

## Environment

The CLI uses these environment variables (set once in your shell):

```bash
export NANOBANANA_GEMINI_API_KEY="your_key"  # Recommended
# or
export GEMINI_API_KEY="your_key"  # Fallback
```

## Notes

- No server needed - CLI generates images directly
- `edit` and `restore` are not supported in CLI mode (use MCP server for these features)
- Image files are saved locally and printed with `MEDIA:` prefix for chat providers
