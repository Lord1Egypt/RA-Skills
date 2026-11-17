---
name: poyo-video-translator
description: Video Translator on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `poyo-ai/video-translator`, translating video speech, `video_urls`, `source_language`, `target_language`, async status polling, callbacks, subtitle outputs, and server-side integration.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/video-translator","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Video Translator
## PoYo Links

- Model page: <https://poyo.ai/models/video-translator>
- API key page: <https://poyo.ai/dashboard/api-key>


Use this skill for Video Translator jobs on PoYo. It helps agents prepare video translation payloads, submit async tasks, and explain server-side polling or webhook handling.

## Use When

- The user explicitly wants to use PoYo Video Translator, `video-translator`, or `poyo-ai/video-translator`.
- The user asks for a PoYo video translation payload, server-side curl command, integration notes, status polling, webhook setup, subtitle output handling, or response parsing.
- The user has already chosen PoYo as the execution provider for translating video speech or captions.

## Model Selection

- `poyo-ai/video-translator`: translate source video speech and return translated media outputs through PoYo's async task flow.

## Key Inputs

- `video_urls` is required inside `input` and should contain one public media URL.
- `source_language` is required and should be an explicit source language code.
- `target_language` is required and sets the translated output language.
- `callback_url` is optional and useful for production queues.
- Save the returned `task_id` immediately for status checks.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private video URLs, source media, translated outputs, subtitle files, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic translation, dubbing, or subtitle tasks unless the user explicitly wants a PoYo Video Translator API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_video_translator.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Video Translator, include:

- chosen model id
- media URL input summary
- source and target language choices
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query task status or wait for webhook
