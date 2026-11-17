---
name: poyo-add-instrumental
description: Add instrumental accompaniment to uploaded audio on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `add-instrumental`, backing tracks, style tags, negative tags, music model versions, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/add-instrumental","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Add Instrumental

## PoYo Links

- Model page: <https://poyo.ai/models/add-instrumental>
- API docs: <https://docs.poyo.ai/api-manual/music-series/add-instrumental>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `add-instrumental` jobs on PoYo. It helps agents prepare accompaniment-generation payloads for uploaded audio, submit async tasks, and explain callback or music detail retrieval.

## Use When

- The user explicitly wants to use PoYo with Add Instrumental, `add-instrumental`, backing track generation, vocal-to-instrumental accompaniment, melody accompaniment, or music production automation.
- The user asks for a PoYo Add Instrumental request payload, server-side curl command, integration notes, callback setup, or music result retrieval.
- The user has already chosen PoYo as the execution provider for an audio accompaniment workflow.

## Model Selection

- `add-instrumental`: use for generating instrumental accompaniment from an uploaded audio URL.

## Key Inputs

- `upload_url` is required and must point to a publicly accessible audio file.
- `title` is required and should be short enough for the documented title limit.
- `tags` is required and should describe desired genres, moods, or instruments.
- `negative_tags` is required and should describe styles or sounds to avoid.
- `mv` is optional; documented values include `V4_5PLUS`, `V5`, and `V5_5`.
- `vocal_gender`, `style_weight`, `weirdness_constraint`, and `audio_weight` are optional controls when supported by the current PoYo docs.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private audio URLs, private style notes, generated audio URLs, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic music generation unless the user explicitly wants a PoYo Add Instrumental API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_add_instrumental.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Add Instrumental, include:

- chosen model id
- source audio URL handling notes
- title, tags, and negative tags
- optional version and style controls when relevant
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query music detail or wait for webhook
