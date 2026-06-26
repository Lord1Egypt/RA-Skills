---
name: poyo-seedream-4-5
description: Seedream 4.5 image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `seedream-4.5`, `seedream-4.5-edit`, 2K/4K output, multi-reference editing, and higher image counts.
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/image-series/seedream-4-5", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---

# PoYo Seedream 4.5 Image Generation and Editing

Use this skill for Seedream 4.5 jobs on PoYo. It covers high-resolution generation, multi-reference image workflows, and edit requests.

## Use When

- The user explicitly asks for `Seedream 4.5`, `seedream-4.5`, or `seedream-4.5-edit`.
- The task is high-resolution generation, image-to-image, or edit.
- The workflow needs multiple reference images or higher output counts.

## Model Selection

- `seedream-4.5`: standard generation entry point.
- `seedream-4.5-edit`: use when the request explicitly edits supplied images.

## Key Inputs

- `prompt` is required.
- `image_urls` supports up to 10 images and is required for `seedream-4.5-edit`.
- `size` can be a resolution token like `2K`/`4K` or an aspect ratio like `1:1`, `16:9`, `21:9`.
- `n` controls output count from `1` to `15`.

## Execution

- Read `references/api.md` for endpoint details, model ids, key fields, example payloads, and polling notes.
- Use `scripts/submit_seedream_4_5.sh` to submit a raw JSON payload from the shell.
- If the user only needs a curl example, adapt the example from `references/api.md` instead of rewriting from scratch.
- After submission, report the `task_id` clearly so follow-up polling is easy.

## Output expectations

When helping with this model family, include:
- chosen model id
- final payload or a concise parameter summary
- whether reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
