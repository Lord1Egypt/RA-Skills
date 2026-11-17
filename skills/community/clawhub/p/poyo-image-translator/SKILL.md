---
name: poyo-image-translator
description: Image Translator on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `poyo-ai/image-translator`, translating text inside images, `image_urls`, `source_language`, `target_language`, async status polling, callbacks, and server-side integration.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/image-translator","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Image Translator
## PoYo Links

- Model page: <https://poyo.ai/models/image-translator>
- API key page: <https://poyo.ai/dashboard/api-key>


Use this skill for Image Translator jobs on PoYo. It helps agents prepare image translation payloads, submit async tasks, and explain server-side polling or webhook handling.

## Use When

- The user explicitly wants to use PoYo Image Translator, `image-translator`, or `poyo-ai/image-translator`.
- The user asks for a PoYo image translation payload, server-side curl command, integration notes, status polling, webhook setup, or response parsing.
- The user has already chosen PoYo as the execution provider for translating text inside images.

## Model Selection

- `poyo-ai/image-translator`: translate text inside one source image and return translated image output through PoYo's async task flow.

## Key Inputs

- `image_urls` is required inside `input` and should contain one public image URL.
- `source_language` may be `auto` or an explicit source language code.
- `target_language` is required and sets the output language.
- `callback_url` is optional and useful for production queues.
- Save the returned `task_id` immediately for status checks.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private image URLs, source images, translated outputs, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic translation or image editing unless the user explicitly wants a PoYo Image Translator API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_image_translator.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Image Translator, include:

- chosen model id
- image URL input summary
- source and target language choices
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query task status or wait for webhook
