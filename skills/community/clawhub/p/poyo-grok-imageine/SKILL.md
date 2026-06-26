---
name: poyo-grok-imagine
description: Grok Imagine video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `grok-imagine`, text-to-video, image-to-video, 6s/10s clips, and `fun` / `normal` / `spicy` mode control.
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/grok-imagine", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---

# PoYo Grok Imagine Video Generation

Use this skill for `grok-imagine` jobs on PoYo. It covers short text-to-video, image-to-video, and mode-based styling.

## Use When

- The user explicitly asks for `Grok Imagine` or `grok-imagine`.
- The task is a 6-second or 10-second clip.
- The workflow needs text-to-video, image-to-video, or `mode` styling.

## Core Capability

- `grok-imagine` is a single-model video entry point. Use `image_urls` for image-to-video and `mode` for `fun`, `normal`, or `spicy` style control.

## Key Inputs

- `prompt` is required.
- `image_urls` is for image-to-video and supports one image.
- `duration` supports `6` and `10`.
- `aspect_ratio` supports `1:1`, `2:3`, `3:2` for text-to-video.
- `mode` supports `fun`, `normal`, `spicy`.

## Execution

- Read `references/api.md` for endpoint details, model ids, key fields, example payloads, and polling notes.
- Use `scripts/submit_grok_imagine.sh` to submit a raw JSON payload from the shell.
- If the user only needs a curl example, adapt the example from `references/api.md` instead of rewriting from scratch.
- After submission, report the `task_id` clearly so follow-up polling is easy.

## Output expectations

When helping with this model family, include:
- chosen model id
- final payload or a concise parameter summary
- whether reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
