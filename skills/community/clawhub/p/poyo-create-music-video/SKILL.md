---
name: poyo-create-music-video
description: Create music videos on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `create-music-video`, AI Music Video, visualized music videos, task_id plus audio_id inputs, callbacks, and status retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/create-music-video","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Create Music Video

## PoYo Links

- Model page: <https://poyo.ai/models/create-music-video>
- API docs: <https://docs.poyo.ai/api-manual/music-series/create-music-video>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `create-music-video` jobs on PoYo. It helps agents prepare music-video payloads from a source music task and audio track, submit async tasks, and explain result retrieval.

## Use When

- The user explicitly wants to create a music video with PoYo, `create-music-video`, or AI Music Video.
- The user has a completed PoYo music `task_id` and an `audio_id` and asks for a request payload, server-side curl command, callback setup, or status retrieval.
- The user has already chosen PoYo as the execution provider for a music video workflow.

## Model Selection

- `create-music-video`: use for generating a visualized music video from an existing music task and audio identifier.

## Key Inputs

- `task_id` identifies the completed source music generation task.
- `audio_id` identifies the audio track to visualize.
- `author` is optional metadata for the generated music video.
- `domain_name` is optional metadata for the generated music video.
- `callback_url` is required by the documented schema and should point to a server-side webhook.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private prompts, customer task ids, audio identifiers, generated media URLs, callback URLs, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic music video generation unless the user explicitly wants a PoYo Create Music Video API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_create_music_video.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Create Music Video, include:

- chosen model id
- source task and audio identifier summary
- optional author or domain metadata summary
- callback setup summary
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query status or wait for webhook
