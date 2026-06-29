---
name: poyo-sora-2-official-api
description: Sora 2 Official video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `sora-2-official`, text-to-video, optional single-image guided video, 4/8/12/16/20 second duration, vertical or landscape video, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/sora-2-official","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Sora 2 Official Video Generation

Use this skill for `sora-2-official` video jobs on PoYo. It helps agents prepare text-to-video and optional single-image guided video payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Sora 2 Official, `sora-2-official`, PoYo Sora official, or OpenAI Sora through PoYo.
- The task is text-to-video, image-guided video, cinematic short video drafting, product motion concepts, or social video generation.
- The workflow needs a PoYo async submit payload, task status polling, or callback URL guidance.

## Model Selection

- `sora-2-official`: use for text-to-video and optional single-image guided video on PoYo.

## Key Inputs

- `prompt` is required inside `input`.
- `duration` can be `4`, `8`, `12`, `16`, or `20` when supported by current PoYo docs.
- `aspect_ratio` can be `16:9` or `9:16`.
- `image_urls` is optional and supports at most one reference image according to current PoYo docs.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images or private URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_sora_2_official.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Sora 2 Official, include:

- chosen model id
- whether the request is text-to-video or image-guided video
- final payload or concise parameter summary
- selected duration and aspect ratio
- whether a reference image is involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
