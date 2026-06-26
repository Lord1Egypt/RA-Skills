---
name: nano-banana-pro-pptx
description: Generate PowerPoint presentations with AI images using Gemini. Each slide is a full-bleed image. Use for creating visual presentations, slideshows, or image-based decks from a topic prompt. Requires --slides N.
metadata:
  credentials:
    - name: GEMINI_API_KEY
      description: Gemini API key (required)
      required: true
    - name: GEMINI_BASE_URL
      description: Custom/proxy API base URL (optional)
      required: false
---

# nano-banana-pro-pptx: AI-Generated Image Presentations

Generate a PowerPoint presentation where every slide is a single full-bleed AI-generated image. Gemini handles both the narrative planning and image generation end-to-end.

## Usage

Run the script using absolute path (do NOT cd to skill directory first):

```bash
uv run ~/.openclaw/workspace/skills/nano-banana-pro-pptx/scripts/generate_pptx.py \
  --prompt "your presentation topic" \
  --slides N \
  [--filename "output.pptx"] \
  [--resolution 1K|2K|4K] \
  [--api-key KEY] \
  [--base-url URL]
```

## Arguments

| Argument | Required | Default | Description |
|---|---|---|---|
| `--prompt` | Yes | — | Topic/theme for the presentation |
| `--slides` | Yes | — | Number of slides (1–50) |
| `--filename` | No | Auto-generated slug | Output `.pptx` filename or full path |
| `--resolution` | No | `1K` | `1K` (1024px), `2K` (2048px), `4K` (4096px) |
| `--api-key` | No | `$GEMINI_API_KEY` | Gemini API key |
| `--base-url` | No | `$GEMINI_BASE_URL` | Custom API base URL |

The script checks for API key in this order:
1. `--api-key` argument (use if user provided key in chat)
2. `GEMINI_API_KEY` environment variable

If neither is available, the script exits with an error message.

The script checks for base URL in this order:
1. `--base-url` argument (use if user provided URL in chat)
2. `GEMINI_BASE_URL` environment variable

If neither is available, the script uses the default Gemini API base URL.


## Instructions

1. Always use the absolute path to the script — never `cd` to the skill directory
2. `--slides` is always required — ask the user if not provided
3. Default to `--resolution 1K` for drafts; suggest `2K` for final output
4. Omit `--filename` to let the script auto-generate a slug from the prompt (do not construct the filename yourself)
5. Confirm the output file path to the user after completion
6. If `GEMINI_API_KEY` is not set in the environment, remind the user to set it or pass `--api-key`

## Workflow

1. Draft at `1K` resolution to verify narrative and composition
2. Regenerate at `2K` or `4K` for final delivery

## Environment Variables

- `GEMINI_API_KEY` — required (or pass `--api-key`)
- `GEMINI_BASE_URL` — optional, for custom/proxy endpoints
