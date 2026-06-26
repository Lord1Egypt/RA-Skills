---
name: grok-image-api
description: Work with OpenAI-compatible image generation and image editing endpoints. Use when the user wants to generate images from prompts, edit images with prompts and optional masks, test an image endpoint, or integrate /v1/images/generations or /v1/images/edits into scripts or projects.
---

# Grok Image API

Use this skill to work with image endpoints that expose:

- `POST /v1/images/generations`
- `POST /v1/images/edits`

Prefer practical workflows: generate or edit an image, save the result locally, and then send or reuse the saved file.

## Quick start

Prefer the bundled script:

- `scripts/grok_image_api.py generate` for text-to-image
- `scripts/grok_image_api.py edit` for image editing
- `scripts/grok_image_api.py probe` to verify the endpoint is reachable

Default environment variables:

- `IMAGE_API_BASE_URL`
- `IMAGE_API_KEY`

## Workflow

1. Identify the task: generate or edit.
2. Load credentials through environment variables.
3. For generation, send JSON to `/v1/images/generations`.
4. For editing, send multipart form data to `/v1/images/edits` with `image` and optional `mask`.
5. Save the returned image locally. If the API returns a URL, download it locally by default.
6. If the user is on QQ and wants the image delivered, reply with a `<qqimg>` tag pointing to the local file or returned URL.

## Generation

Example:

```bash
IMAGE_API_BASE_URL="https://example.com/v1" \
IMAGE_API_KEY="..." \
python3 scripts/grok_image_api.py generate \
  --style anime \
  --preset-size portrait \
  --prompt "a cozy cyberpunk tea shop at night" \
  --out /tmp/generated.png
```

Use `--size` or `--preset-size`, `--style`, `--model`, `--n`, and `--extra key=value` when needed.

## Editing

Example:

```bash
IMAGE_API_BASE_URL="https://example.com/v1" \
IMAGE_API_KEY="..." \
python3 scripts/grok_image_api.py edit \
  --image /absolute/path/input.png \
  --style cute \
  --prompt "replace the background with a sunset beach" \
  --out /tmp/edited.png
```

Add `--mask /absolute/path/mask.png` if the API supports masked edits.

## Notes

- Assume this service is not a full chat-completions endpoint.
- Do not call unrelated routes unless the user explicitly says they exist.
- Avoid echoing secrets back to the user.
- Prefer local saved files for messaging channels that can upload local images.
- Default output directory is a local `output/grok-images/` folder when `--out` is omitted.

## References

Read `references/api-notes.md` when you need a compact reminder of request/response patterns, presets, and output behavior.
