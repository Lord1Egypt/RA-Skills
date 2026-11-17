---
name: poyo-upload-and-cover-audio
description: Transform uploaded audio into a new music style on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `upload-and-cover-audio`, audio cover generation, style transformation, custom mode, instrumental output, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/upload-and-cover-audio","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Upload and Cover Audio

## PoYo Links

- Model page: <https://poyo.ai/models/upload-and-cover-audio>
- API docs: <https://docs.poyo.ai/api-manual/music-series/upload-and-cover-audio>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `upload-and-cover-audio` jobs on PoYo. It helps agents prepare audio cover payloads, choose simple or custom mode, submit async tasks, and explain callback or music detail retrieval.

## Use When

- The user explicitly wants to use PoYo with Upload and Cover Audio, `upload-and-cover-audio`, audio cover generation, music style transformation, or uploaded-audio remixing.
- The user asks for a PoYo Upload and Cover Audio request payload, server-side curl command, integration notes, callback setup, or music result retrieval.
- The user has already chosen PoYo as the execution provider for an audio cover workflow.

## Model Selection

- `upload-and-cover-audio`: use for transforming an uploaded audio file into a new musical style while preserving the source structure.

## Key Inputs

- `upload_url` is required and must point to a publicly accessible audio file.
- `prompt` is required in simple mode and when custom mode needs vocal content.
- `custom_mode` controls whether the request uses a compact prompt or explicit style and title fields.
- `instrumental` controls whether the output should omit vocals.
- `style` and `title` are required in custom mode.
- `mv`, `negative_tags`, `vocal_gender`, `style_weight`, `weirdness_constraint`, `audio_weight`, and `persona_id` are optional controls when supported by the current PoYo docs.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private audio URLs, private lyrics, generated audio URLs, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic audio editing unless the user explicitly wants a PoYo Upload and Cover Audio API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_upload_and_cover_audio.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Upload and Cover Audio, include:

- chosen model id
- source audio URL handling notes
- simple or custom mode choice
- prompt, style, title, and instrumental setting when relevant
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query music detail or wait for webhook
