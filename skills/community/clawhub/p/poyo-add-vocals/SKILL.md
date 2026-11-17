---
name: poyo-add-vocals
description: Add AI-generated vocals to uploaded instrumental audio on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `add-vocals`, lyrics or vocal prompts, style controls, vocal gender, callbacks, and music detail retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/add-vocals","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Add Vocals

## PoYo Links

- Model page: <https://poyo.ai/models/add-vocals>
- API docs: <https://docs.poyo.ai/api-manual/music-series/add-vocals>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `add-vocals` jobs on PoYo. It helps agents prepare vocal-generation payloads for uploaded instrumental audio, submit async tasks, and explain callback or music detail retrieval.

## Use When

- The user explicitly wants to use PoYo with Add Vocals, `add-vocals`, AI vocal generation, adding vocals to an instrumental, lyrics-to-vocals, or music production automation.
- The user asks for a PoYo Add Vocals request payload, server-side curl command, integration notes, callback setup, or music result retrieval.
- The user has already chosen PoYo as the execution provider for an instrumental-to-vocal workflow.

## Model Selection

- `add-vocals`: use for generating vocals over an uploaded instrumental audio URL.

## Key Inputs

- `upload_url` is required and must point to a publicly accessible instrumental audio file.
- `prompt` is required and can contain lyrics or a vocal direction.
- `title` is required and should be short enough for the documented title limit.
- `style` is required and should describe genre, mood, or vocal delivery.
- `negative_tags` is required and should describe vocal or music traits to avoid.
- `mv` is optional; documented values include `V4_5PLUS`, `V5`, and `V5_5`.
- `vocal_gender`, `style_weight`, `weirdness_constraint`, and `audio_weight` are optional controls when supported by the current PoYo docs.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private audio URLs, lyrics, vocal prompts, generated audio URLs, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic music generation unless the user explicitly wants a PoYo Add Vocals API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_add_vocals.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Add Vocals, include:

- chosen model id
- source instrumental URL handling notes
- prompt or lyrics summary
- style, negative tags, and optional vocal gender
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query music detail or wait for webhook
