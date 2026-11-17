---
name: poyo-upload-and-extend-audio
description: Extend uploaded audio on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `upload-and-extend-audio`, audio continuation, uploaded music extension, continuation timing, custom parameters, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/upload-and-extend-audio","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Upload and Extend Audio

## PoYo Links

- Model page: <https://poyo.ai/models/upload-and-extend-audio>
- API docs: <https://docs.poyo.ai/api-manual/music-series/upload-and-extend-audio>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `upload-and-extend-audio` jobs on PoYo. It helps agents prepare uploaded-audio extension payloads, choose simple or custom parameters, submit async tasks, and explain callback or music detail retrieval.

## Use When

- The user explicitly wants to use PoYo with Upload and Extend Audio, `upload-and-extend-audio`, audio continuation, music extension, or extending an uploaded song.
- The user asks for a PoYo Upload and Extend Audio request payload, server-side curl command, integration notes, callback setup, or music result retrieval.
- The user has already chosen PoYo as the execution provider for an uploaded-audio extension workflow.

## Model Selection

- `upload-and-extend-audio`: use for extending an uploaded audio file while preserving the source style.

## Key Inputs

- `upload_url` is required and must point to a publicly accessible audio file.
- `default_param_flag` controls whether the request uses custom parameters.
- `instrumental` controls whether the extension should omit vocals.
- `continue_at` controls where the extension starts.
- `mv` selects the documented music model version.
- `prompt`, `style`, and `title` are used when custom control is needed.
- `negative_tags`, `vocal_gender`, `style_weight`, `weirdness_constraint`, `audio_weight`, and `persona_id` are optional controls when supported by the current PoYo docs.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private audio URLs, private lyrics, generated audio URLs, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic audio editing unless the user explicitly wants a PoYo Upload and Extend Audio API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_upload_and_extend_audio.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Upload and Extend Audio, include:

- chosen model id
- source audio URL handling notes
- simple or custom parameter mode
- continuation timing
- prompt, style, title, and instrumental setting when relevant
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query music detail or wait for webhook
