---
name: hiapi-gpt-image-2
description: Generate images with HiAPI's GPT Image 2 family via the HiAPI unified async task API. Use when a user asks to create or edit an image with GPT Image 2, HiAPI GPT Image 2, or this specific skill.
metadata:
  short-description: Generate GPT Image 2 images through HiAPI
---

# HiAPI GPT Image 2

Use this skill when the user wants image generation through the HiAPI GPT Image 2 family.

## Requirements

- Node.js 18 or newer.
- `HIAPI_API_KEY` must be set in the environment.
- `HIAPI_BASE_URL` is optional and defaults to `https://api.hiapi.ai`.

Important links:

- Get API key: https://www.hiapi.ai/en/register
- Pricing: https://www.hiapi.ai/en/pricing
- Docs: https://docs.hiapi.ai

Never invent an image result. If the API call fails, report the status code, compact error message, and the next action from the Error Guidance section.

## Generate An Image

Run:

```bash
node scripts/hiapi-gpt-image-2.mjs --prompt "Create a launch poster for an AI note app" --aspect-ratio 16:9
```

Supported models:

- `gpt-image-2`
- `gpt-image-2-pro`
- `gpt-image-2-image-to-image`
- `gpt-image-2-image-to-image-pro`

For image-to-image requests, use one of the image-to-image models and pass `--input-url` once per reference image. The API field is `input.input_urls`; supported count is 1 to 5 images.

Supported aspect ratios:

- `auto`
- `1:1`
- `3:2`
- `2:3`
- `16:9`
- `9:16`
- `4:3`
- `3:4`
- `5:4`
- `4:5`
- `2:1`
- `1:2`
- `3:1`
- `1:3`
- `21:9`
- `9:21`

Supported resolutions:

- `1K`
- `2K`
- `4K`

Pro models (`gpt-image-2-pro`, `gpt-image-2-image-to-image-pro`) only support `1K` and `2K`, and a narrower aspect ratio set (no `2:1`, `1:2`, `3:1`, `1:3`, `9:21`; plain pro also has no `auto`).

Cross-field constraints for `gpt-image-2` and `gpt-image-2-image-to-image`:

- `aspect_ratio=auto` (or omitted) only supports `resolution=1K`.
- `aspect_ratio=1:1` cannot be combined with `resolution=4K`.

The script writes generated data URI images to `outputs/` and prints JSON with the saved file paths or remote URLs.

## API Contract

This skill calls:

```text
POST /v1/tasks
GET /v1/tasks/{taskId}
```

with:

```json
{
  "model": "gpt-image-2",
  "input": {
    "prompt": "...",
    "aspect_ratio": "16:9",
    "resolution": "1K"
  }
}
```

Image-to-image:

```json
{
  "model": "gpt-image-2-image-to-image-pro",
  "input": {
    "prompt": "...",
    "input_urls": ["https://example.com/source.png"],
    "aspect_ratio": "auto",
    "resolution": "2K"
  }
}
```

`POST /v1/tasks` returns `data.taskId`. Poll `GET /v1/tasks/{taskId}` until status is `success`. Expected image output is in `data.output[]`, commonly:

```json
{
  "data": {
    "status": "success",
    "output": [{ "type": "image", "url": "https://cdn.example.com/image.png" }]
  }
}
```

For details, read `references/api.md` and `references/output.md`.

## Check Configuration

Run:

```bash
node scripts/check-config.mjs
```

Use `--live` only when you want to verify that the configured key can reach the HiAPI pricing endpoint.

## Error Guidance

- Missing `HIAPI_API_KEY`: tell the user to create or copy a key from https://www.hiapi.ai/en/register and export it.
- HTTP `401` or `403`: tell the user to verify the HiAPI API key.
- HTTP `402`, insufficient balance, credits, quota, or payment errors: tell the user to add credits or check billing at https://www.hiapi.ai/en/dashboard and review pricing at https://www.hiapi.ai/en/pricing.
- HTTP `429`: tell the user to wait and retry or reduce concurrent image generations.
- Content policy or safety errors: ask the user to revise the prompt.
- No extractable image: explain that this skill expects `data.output[]` to contain an image URL or data URI after the task succeeds.
- Optional skill update notice: tell the user the printed update command can be run later.
- Required skill update notice: tell the user the printed update command must be run before using this skill again.
