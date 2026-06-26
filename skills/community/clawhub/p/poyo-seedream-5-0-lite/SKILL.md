---
name: poyo-seedream-5-0-lite
description: Seedream 5.0 Lite image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `seedream-5.0-lite`, `seedream-5.0-lite-edit`, 2K/3K output, multi-reference editing, and aspect-ratio control.
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/image-series/seedream-5-0-lite", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---

# PoYo Seedream 5.0 Lite Image Generation and Editing

Use this skill for Seedream 5.0 Lite jobs on PoYo. It fits efficient high-resolution generation, image editing, and flexible size control.

## Use When

- The user explicitly asks for `Seedream 5.0 Lite`, `seedream-5.0-lite`, or `seedream-5.0-lite-edit`.
- The task is high-resolution generation, image-to-image, or edit.
- The workflow needs 2K/3K output or direct aspect-ratio control.

## Model Selection

- `seedream-5.0-lite`: standard generation entry point.
- `seedream-5.0-lite-edit`: use when the request explicitly edits supplied images.

## Key Inputs

- `prompt` is required.
- `image_urls` supports up to 10 images and is required for edit workflows.
- `size` can be `2K`, `3K`, or an aspect ratio like `1:1`, `16:9`, `21:9`.
- `n` controls output count from `1` to `15`.

## Execution

- Read `references/api.md` for endpoint details, model ids, key fields, example payloads, and polling notes.
- Use `scripts/submit_seedream_5_0_lite.sh` to submit a raw JSON payload from the shell.
- If the user only needs a curl example, adapt the example from `references/api.md` instead of rewriting from scratch.
- After submission, report the `task_id` clearly so follow-up polling is easy.

## Output expectations

When helping with this model family, include:
- chosen model id
- final payload or a concise parameter summary
- whether reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
