---
name: poyo-elevenlabs-v3-tts
description: Generate speech on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `elevenlabs-v3-tts`, text-to-speech, voice selection, stability, timestamps, language code, text normalization, async task submission, callbacks, and task status retrieval.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/elevenlabs-v3-tts","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo ElevenLabs V3 TTS
## PoYo Links

- Model page: <https://poyo.ai/models/elevenlabs-v3-tts>
- API docs: <https://docs.poyo.ai/api-manual/music-series/elevenlabs-v3-tts>
- API key page: <https://poyo.ai/dashboard/api-key>


Use this skill for `elevenlabs-v3-tts` jobs on PoYo. It helps agents prepare text-to-speech payloads, choose voice and delivery fields, submit async tasks, and explain result retrieval through PoYo task status.

## Use When

- The user mentions PoYo ElevenLabs V3 TTS, `elevenlabs-v3-tts`, text-to-speech, voiceover, narration, timestamps, language code, or text normalization.
- The workflow needs a PoYo speech payload, async task submission, a callback URL, or task status retrieval guidance.
- The user wants server-side curl or shell examples for PoYo speech generation.

## Model Selection

- `elevenlabs-v3-tts`: use for PoYo text-to-speech generation with voice, stability, language, normalization, and optional timestamp controls.

## Key Inputs

- `text` is required.
- `voice` selects a supported voice name.
- `stability` tunes voice stability.
- `timestamps` requests timing data when available.
- `language_code` can enforce a target language when supported.
- `apply_text_normalization` can be `auto`, `on`, or `off`.
- `callback_url` is optional and useful for production queues.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not log private scripts, customer text, callback URLs, task ids, timestamps files, or generated audio URLs unless the product policy allows it.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and result retrieval notes.
- Use `scripts/submit_elevenlabs_v3_tts.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- After submission, report the returned `task_id` clearly so follow-up retrieval is easy.

## Output Expectations

When helping with ElevenLabs V3 TTS, include:

- chosen model id
- voice and language choices
- timestamp and normalization choices
- final payload or concise parameter summary
- returned `task_id` if a request was actually submitted
- next step: query task status or wait for webhook
