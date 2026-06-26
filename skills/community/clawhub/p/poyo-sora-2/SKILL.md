---
name: poyo-sora-2
description: Use PoYo AI's Sora 2 video generation models through the `https://api.poyo.ai/api/generate/submit` endpoint. Use when a user wants to generate videos, submit Sora 2 jobs, create text-to-video or image-to-video payloads, poll task status, or prepare PoYo-compatible requests for `sora-2` or `sora-2-private`.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/sora-2","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Sora 2

Use this skill to submit and track Sora 2 video jobs on PoYo AI.

## Quick workflow

1. Choose the model:
   - `sora-2` for standard Sora 2 generation
   - `sora-2-private` for the private standard-quality variant
2. Build the request body.
3. Submit a POST request to `https://api.poyo.ai/api/generate/submit` with Bearer auth.
4. Save the returned `task_id`.
5. Poll unified task status until the job finishes, or rely on `callback_url` if the user has a webhook.

## Request rules

- Require `Authorization: Bearer <POYO_API_KEY>`.
- Require top-level `model`.
- Require `input.prompt`.
- Use `input.image_urls` only for image-to-video; PoYo docs say only one image is supported.
- Use `input.duration` when the user specifies clip length; valid values are `10` or `15`.
- Use `input.aspect_ratio` when needed; valid values are `16:9` or `9:16`.
- Optional stylistic control is available through `input.style` and `input.storyboard`.

## Model selection

### `sora-2`

Use for:
- standard text-to-video generation
- standard image-to-video generation
- default Sora 2 jobs on PoYo

### `sora-2-private`

Use for:
- private standard-quality variant when the user explicitly asks for it
- cases where the user's account/workflow expects the private model id

## Execution

- Read `references/api.md` for payload fields, examples, and polling notes.
- Use `scripts/submit_sora_2.sh` to submit a task from the shell when direct API execution is appropriate.
- If the user needs a raw curl example, adapt one from `references/api.md`.
- After submission, report the `task_id` clearly so follow-up polling is easy.

## Output expectations

When helping with a Sora 2 task, include:
- chosen model
- whether the request is text-to-video or image-to-video
- final payload or summarized parameters
- returned `task_id` if the request was actually submitted
- next step: poll status or wait for webhook
