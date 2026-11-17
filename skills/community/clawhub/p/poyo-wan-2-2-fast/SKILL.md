---
name: poyo-wan-2-2-fast
description: Wan 2.2 Fast video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `wan2.2-text-to-video-fast`, `wan2.2-image-to-video-fast`, fast text-to-video, image-to-video, first/last-frame images, 480p, 720p, seed control, task submission, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/wan-2-2-fast","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Wan 2.2 Fast Video Generation
## PoYo Links

- Model page: <https://poyo.ai/models/wan-2-2-fast>
- API docs: <https://docs.poyo.ai/api-manual/video-series/wan2.2-text-to-video-fast>
- API key page: <https://poyo.ai/dashboard/api-key>


Use this skill for Wan 2.2 Fast video jobs on PoYo. It helps agents prepare text-to-video and image-to-video payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Wan 2.2 Fast, `wan2.2-text-to-video-fast`, `wan2.2-image-to-video-fast`, or PoYo Wan 2.2 video generation.
- The task is prompt-based video, single-image animation, or first/last-frame image-to-video.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `wan2.2-text-to-video-fast`: generate video from a text prompt.
- `wan2.2-image-to-video-fast`: animate one required image and optionally use a second image as the last frame.

## Key Inputs

- `prompt` is required inside `input`.
- `aspect_ratio` is used by text-to-video and supports documented landscape or portrait values.
- `image_urls` is required for image-to-video and supports one or two URLs.
- `resolution` can be `480p` or `720p`.
- `seed` is optional when reproducible generation behavior is useful.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private image URLs, private callback URLs, or generated media URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model ids, common fields, example payloads, and polling notes.
- Use `scripts/submit_wan_2_2_fast.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Wan 2.2 Fast, include:

- chosen model id
- whether the request is text-to-video or image-to-video
- final payload or concise parameter summary
- selected resolution, aspect ratio, and seed when relevant
- whether one or two source images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
