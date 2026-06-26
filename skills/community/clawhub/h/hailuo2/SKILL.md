---
name: poyo-hailuo-02
description: Use PoYo AI Hailuo 02 for prompt-optimized video generation and image-to-video workflows through the `https://api.poyo.ai/api/generate/submit` endpoint. Use when a user wants standard or pro video jobs, optional prompt optimization, end-frame control, or PoYo payloads for `hailuo-02` and `hailuo-02-pro`.
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/hailuo-02", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---

# PoYo Hailuo 02 Video Generation

Use this skill to submit and track PoYo jobs for the Hailuo 02 family.

## Quick workflow

1. Choose the right model id for the requested output.
2. Build the request body for `POST https://api.poyo.ai/api/generate/submit`.
3. Send Bearer-authenticated JSON with `Authorization: Bearer <POYO_API_KEY>`.
4. Save the returned `task_id`.
5. Poll unified task status or wait for `callback_url` notifications.

## Request rules

- Require top-level `model`.
- Keep prompts concrete and outcome-focused.
- Require `input.prompt` unless the user already supplied a full payload.
- Use `input.image_urls` only when the task needs reference or source images.
- Use `input.duration` when the clip length matters.
- Use `input.resolution` when quality/cost tradeoffs matter.

## Model selection

### `hailuo-02`

Use for general generation with this model variant.
### `hailuo-02-pro`

Use for higher-quality or premium jobs.

## Execution

- Read `references/api.md` for endpoint details, model ids, key fields, example payloads, and polling notes.
- Use `scripts/submit_hailuo_02.sh` to submit a raw JSON payload from the shell.
- If the user only needs a curl example, adapt the example from `references/api.md` instead of rewriting from scratch.
- After submission, report the `task_id` clearly so follow-up polling is easy.

## Output expectations

When helping with this model family, include:
- chosen model id
- final payload or a concise parameter summary
- whether reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook

Notes:

Needs POYO_API_KEY from https://poyo.ai
PoYo.ai - Premium AI API Platform | Image, Video, Music & Chat APIs - 80% Cheaper
