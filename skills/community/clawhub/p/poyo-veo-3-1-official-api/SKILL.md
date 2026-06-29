---
name: poyo-veo-3-1-official-api
description: Veo 3.1 Official video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `veo3.1-fast-official`, `veo3.1-lite-official`, `veo3.1-quality-official`, text-to-video, image-to-video, first/last-frame video, reference video, audio control, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/veo-3-1-official","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Veo 3.1 Official Video Generation

Use this skill for Veo 3.1 Official jobs on PoYo. It helps agents prepare text-to-video, image-to-video, first/last-frame, and reference-guided video payloads, then submit async tasks and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Veo 3.1 Official, `veo3.1-fast-official`, `veo3.1-lite-official`, or `veo3.1-quality-official`.
- The task is text-to-video, image-to-video, first/last-frame video, reference-guided video, or short product/social video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `veo3.1-fast-official`: use when the user wants the fast official model.
- `veo3.1-lite-official`: use when the user explicitly asks for the lite official model.
- `veo3.1-quality-official`: use when the user explicitly asks for the quality official model or supported high-resolution output.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is optional and controls text-only, image-to-video, first/last-frame, or reference workflows.
- `generation_type` can be `frame` or `reference` when required by image count and model support.
- `duration` supports documented values for the selected model and mode.
- `aspect_ratio` supports `16:9`, `9:16`, and `auto` for supported image-guided modes.
- `resolution` supports the documented resolution values for the selected model.
- `sound` controls whether audio is generated when supported.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private source images, private videos, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, example payloads, and polling notes.
- Use `scripts/submit_veo_3_1_official.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Veo 3.1 Official, include:

- chosen model id
- whether the request is text-to-video, image-to-video, first/last-frame, or reference-guided
- final payload or concise parameter summary
- selected duration, aspect ratio, resolution, and sound setting when relevant
- whether source images or reference media are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
