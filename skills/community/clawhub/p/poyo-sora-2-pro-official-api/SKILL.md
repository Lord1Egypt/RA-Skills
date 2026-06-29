---
name: poyo-sora-2-pro-official-api
description: Sora 2 Pro Official video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `sora-2-pro-official`, text-to-video, optional single-image guidance, aspect ratio control, 4 to 20 second clips, 720p, 1024p, or 1080p output, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/sora-2-pro-official","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Sora 2 Pro Official Video Generation

Use this skill for Sora 2 Pro Official video jobs on PoYo. It helps agents prepare text-to-video and optional single-image guided video payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Sora 2 Pro Official, Sora 2 Pro official API, or `sora-2-pro-official`.
- The task is text-to-video, single-image guided video, cinematic concept video, product motion, or social video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `sora-2-pro-official`: use for Sora 2 Pro Official video generation through PoYo.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is optional and supports at most one reference image according to current PoYo docs.
- `aspect_ratio` is optional and should match the selected workflow.
- `duration` is optional and supports the documented clip lengths for this model.
- `resolution` is optional and supports documented output values.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_sora_2_pro_official.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Sora 2 Pro Official, include:

- chosen model id
- whether the request is text-to-video or image-guided video
- final payload or concise parameter summary
- selected duration, aspect ratio, and resolution when relevant
- whether a reference image is involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
