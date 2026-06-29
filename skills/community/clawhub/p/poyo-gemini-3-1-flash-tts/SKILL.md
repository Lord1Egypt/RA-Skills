---
name: poyo-gemini-3-1-flash-tts
description: Generate speech on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `gemini-3-1-flash-tts`, Gemini text-to-speech, style instructions, voice presets, language code, two-speaker dialogue, output formats, async task submission, callbacks, and task status retrieval.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/music-series/gemini-3-1-flash-tts","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Gemini 3.1 Flash TTS

Use this skill for `gemini-3-1-flash-tts` jobs on PoYo. It helps agents prepare text-to-speech payloads, choose single-speaker or two-speaker mode, submit async tasks, and explain result retrieval through PoYo task status.

## Use When

- The user mentions PoYo Gemini 3.1 Flash TTS, `gemini-3-1-flash-tts`, text-to-speech, style instructions, voice presets, audio tags, multilingual speech, or two-speaker dialogue.
- The workflow needs a PoYo speech payload, async task submission, a callback URL, or task status retrieval guidance.
- The user wants server-side curl or shell examples for PoYo speech generation.

## Model Selection

- `gemini-3-1-flash-tts`: use for PoYo text-to-speech generation with style instructions, voice presets, and optional two-speaker dialogue.

## Key Inputs

- `text` is required.
- `style_instructions` can guide delivery, pace, accent, tone, or emotion.
- `voice` selects a preset for single-speaker synthesis.
- `language_code` can steer multilingual synthesis when supported.
- `speakers` enables exactly two speakers; each `speaker_id` must match prefixes in `text`.
- `temperature` controls delivery variation.
- `output_format` can be `mp3`, `wav`, or `ogg_opus`.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not log private scripts, customer text, callback URLs, task ids, or generated audio URLs unless the product policy allows it.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_gemini_3_1_flash_tts.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with Gemini 3.1 Flash TTS, include:

- chosen model id
- single-speaker or two-speaker mode
- voice presets and style instructions
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query task status or wait for webhook
