---
name: poyo-seedance-2-mini
description: Seedance 2.0 Mini video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `seedance-2-mini`, text-to-video, image-to-video, first-frame and last-frame guidance, reference image/video/audio guidance, 480p, 720p, duration, aspect ratio, audio generation, polling, and webhooks.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/seedance-2-mini","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Seedance 2.0 Mini Video Generation

Use this skill for Seedance 2.0 Mini video jobs on PoYo. It helps agents prepare text-to-video, image-to-video, first/last-frame, and multimodal reference payloads, submit async tasks, and explain polling or webhook follow-up.

## Use When

- The user explicitly mentions Seedance 2.0 Mini, Seedance Mini, `seedance-2-mini`, or PoYo Seedance video generation.
- The task is short-form text-to-video, first-frame image-to-video, first/last-frame video, or reference-guided video generation.
- The workflow needs PoYo async task submission, task status polling, or callback URL guidance.

## Model Selection

- `seedance-2-mini`: use for Seedance 2.0 Mini text, image, video reference, or audio reference workflows.

## Key Inputs

- `prompt` is required inside `input`.
- `image_urls` is optional for first-frame or first/last-frame workflows and should not be combined with reference URL fields.
- `reference_image_urls`, `reference_video_urls`, and `reference_audio_urls` are optional for reference-to-video workflows.
- `reference_audio_urls` should be used with at least one reference image or reference video.
- `resolution` supports documented Mini output presets.
- `aspect_ratio` controls output framing.
- `duration` controls clip length when supported by the current PoYo docs.
- `generate_audio` controls whether PoYo should generate an audio track when supported.
- `seed` can help reproduce supported generation behavior.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not submit confidential prompts, private media URLs, private reference files, or private callback URLs unless the user trusts PoYo and the callback receiver.

## Execution

- Read `references/api.md` for endpoint details, model id, common fields, example payloads, and polling notes.
- Use `scripts/submit_seedance_2_mini.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with Seedance 2.0 Mini, include:

- chosen model id
- whether the request is text-to-video, image-to-video, or reference-to-video
- final payload or concise parameter summary
- selected resolution, aspect ratio, duration, audio setting, and seed when relevant
- whether first/last frames or reference media are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
