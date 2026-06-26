---
name: poyo-gpt-image-2
description: GPT Image 2 generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `gpt-image-2`, `gpt-image-2-edit`, text-to-image, multi-image editing with `image_urls`, single-image output, `auto` or aspect-ratio sizes, custom `WIDTHxHEIGHT`, and 1K/2K/4K resolution control.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/image-series/gpt-image-2","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo GPT Image 2 Generation and Editing

Use this skill for GPT Image 2 jobs on PoYo. It covers text-to-image generation, reference-image-guided generation, and multi-image editing payloads for `gpt-image-2` and `gpt-image-2-edit`.

## Use When

- The user explicitly mentions `GPT Image 2`, `gpt-image-2`, or `gpt-image-2-edit`.
- The task is text-to-image, image-to-image, or editing one or more supplied images.
- The workflow needs broader aspect-ratio support, custom pixel size, or `1K` / `2K` / `4K` resolution control.

## Model Selection

- `gpt-image-2`: text-to-image generation and optional reference-image-guided generation.
- `gpt-image-2-edit`: editing based on one or more reference images and a text instruction; requires `image_urls`.

## Key Inputs

- `prompt` is required inside `input` and is limited to 4000 characters.
- `image_urls` is required for `gpt-image-2-edit` and supports multiple input images.
- Each request returns a single image.
- `size` supports `auto`, `1:1`, `2:3`, `3:2`, `4:3`, `3:4`, `4:5`, `5:4`, `16:9`, `9:16`, `21:9`, or custom `WIDTHxHEIGHT`.
- `resolution` supports `1K`, `2K`, and `4K`.
- Custom `WIDTHxHEIGHT` sizes require `resolution` to be `2K` or `4K`.
- `auto` size or omitted `size` always uses `1K` resolution.

## Execution

- Read `references/api.md` for endpoint details, model ids, key fields, example payloads, resolution notes, and polling notes.
- Use `scripts/submit_gpt_image_2.sh` to submit a raw JSON payload from the shell.
- If the user only needs a curl example, adapt one from `references/api.md` instead of rewriting from scratch.
- After submission, report the `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with this model family, include:
- chosen model id
- whether the request is text-to-image, reference-guided generation, or editing
- final payload or a concise parameter summary
- selected `size` and `resolution`
- whether reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
