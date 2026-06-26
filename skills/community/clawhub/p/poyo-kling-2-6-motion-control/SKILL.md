---
name: poyo-kling-2-6-motion-control
description: Kling 2.6 Motion Control on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-2.6-motion-control`, motion transfer, character animation, orientation control, and 720p/1080p output.
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/kling-2.6-motion-control", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---

# PoYo Kling 2.6 Motion Control

Use this skill for `kling-2.6-motion-control` jobs on PoYo. It is for strict motion transfer workflows that require both a character image and a reference video.

## Use When

- The user explicitly asks for `Kling 2.6 Motion Control` or `kling-2.6-motion-control`.
- The task is motion transfer from a reference video to a target character image.
- The workflow depends on `character_orientation` and explicit resolution control.

## Core Capability

- `kling-2.6-motion-control` is not a general video model. Use it only when the task requires character animation from a supplied image plus a supplied motion video.

## Key Inputs

- `image_urls` is required, supports one character image, and should clearly show head, shoulders, and torso.
- `video_urls` is required, supports one reference video, and must be 3-30 seconds.
- `character_orientation` is required and supports `image` or `video`.
- `resolution` is required and supports `720p` or `1080p`.
- `prompt` is optional scene guidance only.

## Execution

- Read `references/api.md` for endpoint details, model ids, key fields, example payloads, and polling notes.
- Use `scripts/submit_kling_2_6_motion_control.sh` to submit a raw JSON payload from the shell.
- If the user only needs a curl example, adapt the example from `references/api.md` instead of rewriting from scratch.
- After submission, report the `task_id` clearly so follow-up polling is easy.

## Output expectations

When helping with this model family, include:
- chosen model id
- final payload or a concise parameter summary
- whether reference images are involved
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
