---
name: hiapi-happyhorse-1-0-video
description: Use when a user asks to create text-to-video with HappyHorse 1.0, HiAPI HappyHorse 1.0, or this specific skill.
metadata:
  short-description: Generate HappyHorse 1.0 videos through HiAPI
---

# HiAPI HappyHorse 1.0 Video

Use this skill when the user wants text-to-video generation through HiAPI's `happyhorse-1-0` model.

## Requirements

- Node.js 18 or newer.
- `HIAPI_API_KEY` must be set in the environment.
- `HIAPI_BASE_URL` is optional and defaults to `https://api.hiapi.ai`.

Important links:

- Get API key: https://www.hiapi.ai/en/register
- Pricing: https://www.hiapi.ai/en/pricing
- Docs: https://docs.hiapi.ai

Never invent a video result. If the API call fails, report the status code, compact error message, and the next action from the Error Guidance section.

## Generate A Video

Run:

```bash
node scripts/hiapi-happyhorse-1-video.mjs \
  --prompt "A wuxia swordswoman leaps across temple rooftops at dusk, silk robes flowing in the wind" \
  --seconds 5 \
  --resolution 1080p \
  --ratio 16:9
```

Supported durations:

- any integer from `3` to `15`

Supported resolutions:

- `720p`
- `1080p`

Supported aspect ratios (`--ratio`, legacy alias `--size`):

- `16:9`
- `9:16`
- `1:1`
- `4:3`
- `3:4`

Optional seed:

- integer from `0` to `2147483647`
- omit it when the user does not request reproducibility

The script creates a video task, polls until it finishes, downloads the video to `outputs/` when possible, and prints JSON with the saved file path or remote URL.

## API Contract

This skill calls:

```text
POST /v1/tasks
GET /v1/tasks/{taskId}
```

with:

```json
{
  "model": "happyhorse-1-0",
  "input": {
    "prompt": "...",
    "duration": 5,
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "seed": 12345
  }
}
```

HappyHorse 1.0 is text-to-video. Do not send image inputs to this model. The CLI maps `--seconds` to `input.duration` and `--ratio` (legacy alias `--size`) to `input.aspect_ratio`. Use `--seed` only when the user requests reproducibility.

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
- HTTP `402`, HTTP `403` with quota text, insufficient balance, credits, quota, or payment errors: tell the user to add credits or check billing at https://www.hiapi.ai/en/dashboard and review pricing at https://www.hiapi.ai/en/pricing.
- HTTP `400`: tell the user to check duration, resolution, aspect_ratio, and seed.
- HTTP `429`: tell the user to wait and retry or reduce concurrent video generations.
- Task failure: ask the user to try a clearer prompt.
- Timeout: explain that video generation may still be running and the user can retry later.
- Optional skill update notice: tell the user the printed update command can be run later.
- Required skill update notice: tell the user the printed update command must be run before using this skill again.
