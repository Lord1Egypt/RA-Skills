---
name: poyo-xai-tts-1
description: Generate expressive multilingual speech on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `xai-tts-1`, text-to-speech, voice presets, language code, speech tags, output audio formats, async status polling, callbacks, and server-side integration.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/xai-tts-1","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo xAI TTS 1

## PoYo Links

- Model page: <https://poyo.ai/models/xai-tts-1>
- API docs: <https://docs.poyo.ai/api-manual/music-series/xai-tts-1>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for `xai-tts-1` jobs on PoYo. It helps agents prepare text-to-speech payloads, choose voice and audio output options, submit async tasks, and explain safe server-side integration.

## Use When

- The user explicitly wants to use PoYo with xAI TTS 1, `xai-tts-1`, text-to-speech, expressive speech tags, voice presets, multilingual speech, or the PoYo async audio API.
- The user asks for a PoYo xAI TTS request payload, server-side curl command, integration notes, status polling, webhook setup, or response parsing.
- The user has already chosen PoYo as the execution provider for a text-to-speech workflow.

## Model Selection

- `xai-tts-1`: use for text-to-speech generation with expressive tags, voice presets, language selection, and audio output controls.

## Key Inputs

- `text` is required and supports 1 to 15000 characters.
- `text` can include expressive tags such as `[laugh]`, `[pause]`, `[sigh]`, `<whisper>text</whisper>`, and `<slow>text</slow>`.
- `voice` is optional; supported values include `eve`, `ara`, `rex`, `sal`, and `leo`.
- `language_code` is optional; use `auto` when language detection is preferred.
- `output_format` is optional and can set codec, sample rate, and MP3 bit rate.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private scripts, customer text, generated audio URLs, callback URLs, task ids, or raw authorization headers unless the product policy allows it.
- Do not use this skill for generic speech generation unless the user explicitly wants a PoYo xAI TTS API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, supported language codes, and result retrieval notes.
- Use `scripts/submit_xai_tts_1.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up polling is easy.

## Output Expectations

When helping with PoYo xAI TTS 1, include:

- chosen model id
- voice and language settings
- output audio format settings when relevant
- speech tags used or omitted
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: poll status or wait for webhook
