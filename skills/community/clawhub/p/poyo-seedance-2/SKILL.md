---
name: poyo-seedance-2
description: Seedance 2 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `seedance-2`, `seedance-2-fast`, text-to-video, first/last-frame image-to-video, multimodal image/video/audio references, 4s-15s clips, optional audio, and seed control.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/video-series/seedance-2","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Seedance 2 Video Generation

Use this skill for Seedance 2 jobs on PoYo. It covers standard and fast variants, text-to-video, first/last-frame control, and multimodal reference-to-video workflows.

## Use When

- The user explicitly asks for `Seedance 2`, `Seedance 2.0`, `seedance-2`, or `seedance-2-fast`.
- The task is a 4-second to 15-second video clip from text, first/last frames, or multimodal references.
- The workflow needs generated audio, reproducible `seed`, or reference images, videos, and audio.

## Model Selection

- `seedance-2`: default standard-quality variant; supports `480p`, `720p`, and `1080p`.
- `seedance-2-fast`: faster, lower-cost variant; supports `480p` and `720p` only.

## Key Inputs

- `prompt`, `resolution`, and `duration` are required inside `input`.
- `duration` supports integer values from `4` to `15`.
- `aspect_ratio` is optional and supports `1:1`, `21:9`, `4:3`, `3:4`, `16:9`, `9:16`.
- `image_urls` supports up to two images for first and last frame control.
- `reference_image_urls`, `reference_video_urls`, and `reference_audio_urls` support multimodal reference-to-video workflows.
- Do not combine `image_urls` with any `reference_*_urls` field in the same request.
- `generate_audio` and `seed` are optional.

## Execution

- Read `references/api.md` for endpoint details, field constraints, example payloads, and polling notes.
- Use `scripts/submit_seedance_2.sh` to submit a raw JSON payload from the shell.
- If the user only needs a curl example, adapt one from `references/api.md` instead of rewriting from scratch.
- After submission, report the `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with this model family, include:
- chosen model id
- whether the request is text-to-video, first/last-frame, or multimodal reference-to-video
- final payload or a concise parameter summary
- whether generated audio or seed control is enabled
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
