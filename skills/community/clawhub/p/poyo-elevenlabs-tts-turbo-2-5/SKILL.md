---
name: poyo-elevenlabs-tts-turbo-2-5
description: Generate speech on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `elevenlabs-tts-turbo-2-5`, text-to-speech, voice selection, speech speed, stability, similarity boost, style, timestamps, language code, async task submission, callbacks, and task status retrieval.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/music-series/elevenlabs-tts-turbo-2-5","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo ElevenLabs TTS Turbo 2.5

Use this skill for `elevenlabs-tts-turbo-2-5` jobs on PoYo. It helps agents prepare text-to-speech payloads, tune voice and delivery fields, submit async tasks, and explain result retrieval through PoYo task status.

## Use When

- The user mentions PoYo ElevenLabs TTS Turbo 2.5, `elevenlabs-tts-turbo-2-5`, text-to-speech, voiceover, narration, speech speed, timestamps, or language-code control.
- The workflow needs a PoYo speech payload, async task submission, a callback URL, or task status retrieval guidance.
- The user wants server-side curl or shell examples for PoYo speech generation.

## Model Selection

- `elevenlabs-tts-turbo-2-5`: use for PoYo text-to-speech generation with voice, delivery, context, and timestamp controls.

## Key Inputs

- `text` is required.
- `voice` may be a voice name or compatible voice ID.
- `stability`, `similarity_boost`, `style`, and `speed` tune delivery.
- `timestamps` requests timestamp data when available.
- `previous_text` and `next_text` provide context for long-form narration split across requests.
- `language_code` can steer the target language when supported.
- `apply_text_normalization` can be `auto`, `on`, or `off`.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not log private scripts, customer text, callback URLs, task ids, or generated audio URLs unless the product policy allows it.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_elevenlabs_tts_turbo_2_5.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with ElevenLabs TTS Turbo 2.5, include:

- chosen model id
- voice and language choices
- delivery controls that changed from defaults
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query task status or wait for webhook
