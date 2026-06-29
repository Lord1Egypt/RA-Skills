---
name: poyo-runway-gen-4-5
description: Runway Gen-4.5 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `runway-gen-4.5`, text-to-video, optional single-image guidance, 5 or 10 second clips, aspect ratio control, seeded output, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/runway-gen-4-5","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Runway Gen-4.5 Video Generation

Use this skill for Runway Gen-4.5 video jobs on PoYo. It helps agents prepare text-to-video and optional single-image guided video payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Runway Gen-4.5, Runway Gen 4.5, or `runway-gen-4.5`.
- The task is text-to-video, reference-image guided video, short product motion, cinematic concept video, or social video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `runway-gen-4.5`: use for Runway Gen-4.5 video generation through PoYo.

## Key Inputs

- `prompt` is required inside `input`.
- `duration` supports the documented clip lengths for this model.
- `aspect_ratio` controls the output framing.
- `image_urls` is optional and supports at most one reference image according to current PoYo docs.
- `seed` is optional for supported deterministic workflows.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential source images, private prompts, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_runway_gen_4_5.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Runway Gen-4.5, include:

- chosen model id
- whether the request is text-to-video or image-guided video
- final payload or concise parameter summary
- selected duration and aspect ratio when relevant
- whether a reference image is involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
