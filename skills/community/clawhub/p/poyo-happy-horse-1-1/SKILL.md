---
name: poyo-happy-horse-1-1
description: Happy Horse 1.1 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `happy-horse-1.1`, text-to-video, image-to-video, reference-to-video, aspect ratio, duration, resolution, seed control, task submission, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/happy-horse-1-1","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Happy Horse 1.1 Video Generation

Use this skill for Happy Horse 1.1 video jobs on PoYo. It helps agents prepare text-to-video, image-to-video, and reference-to-video payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Happy Horse 1.1, HappyHorse 1.1, `happy-horse-1.1`, or PoYo Happy Horse video generation.
- The task is prompt-based video, first-frame image-to-video, reference-driven short video, or short creative video drafting.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `happy-horse-1.1`: use for text-to-video, image-to-video, and reference-to-video workflows.

## Key Inputs

- `prompt` is required for text-to-video and reference-to-video workflows.
- `image_urls` is used only for image-to-video and should contain one first-frame image URL.
- `reference_image_urls` is used only for reference-to-video and should not be combined with `image_urls`.
- `aspect_ratio` controls output framing.
- `resolution` controls output resolution when supported by the current PoYo docs.
- `duration` controls clip length when supported by the current PoYo docs.
- `seed` can help reproduce supported generation behavior.
- `enable_safety_checker` can be set when the workflow needs PoYo safety checking.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private source images, private reference images, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_happy_horse_1_1.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Happy Horse 1.1, include:

- chosen model id
- whether the request is text-to-video, image-to-video, or reference-to-video
- final payload or concise parameter summary
- selected aspect ratio, resolution, duration, and seed when relevant
- whether source or reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
