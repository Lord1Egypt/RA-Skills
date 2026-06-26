---
name: liber-speechapi
description: Use Liber SpeechAPI for three speech workflows: (1) Telegram/openclaw voice-message handling with ASR, concise reply summarization, and Telegram-compatible OGG/Opus TTS, (2) direct text-to-speech generation when the user explicitly asks to synthesize text into audio, and (3) direct speech-to-text transcription when the user explicitly asks to convert audio into text or structured JSON. Support environment-based configuration, optional voice cloning from a reference audio file, and fallback between shared python-env skill and the local Python environment.
---

# Liber SpeechAPI

Use this skill for three related tasks:
- handle Telegram/openclaw voice-message workflows end to end
- convert user-provided text to speech on demand
- convert user-provided audio to text on demand

## Follow this workflow

1. Read `references/config.md` to resolve configuration from `.env` and `config.json`.
2. Read `references/workflow.md` for Telegram/openclaw voice-message handling.
3. Read `references/api.md` when you need endpoint and payload details.
4. Read `references/parameters.md` for detailed ASR/TTS parameter meanings and defaults.
5. Use `scripts/summarize_for_voice.py` only when a reply must be shortened for voice playback.
6. Use `scripts/liber_speech_client.py` for deterministic ASR/TTS calls instead of rewriting HTTP request logic.

## Environment selection

Prefer a shared `python-env` skill if it is available in the current environment.

If `python-env` is not available, use the local Python environment for this skill.

When running local Python commands:
- use Python 3.11 if available
- allow Python 3.10 when 3.11 is unavailable
- install only the minimal dependencies required by the bundled scripts
- do not hardcode secrets; read them from `.env`

## Configuration model

### `.env`

Load core service settings from `.env` in priority order:
1. environment variables (`LIBER_API_BASE_URL` and `LIBER_API_KEY`)
2. `~/.openclaw/.env` file (for global configuration)
3. the skill directory's `.env` file
4. the current working directory's `.env` file

Environment variables take the highest priority, followed by the global config file `~/.openclaw/.env`, then local skill directory, and finally the current working directory.

Required settings:
- `LIBER_API_BASE_URL`
- `LIBER_API_KEY`

### `config.json`

Load detailed defaults from `speechapi_config.json` in `~/.openclaw/workspace/config/` to prevent overwrites during skill updates.
Fallback to local `config.json` if the external config doesn't exist.

Key behavior:
- values of `"default"` or `null` are omitted from API requests
- Telegram-specific voice replies use `global.telegram_tts_format`
- direct text-to-speech uses `tts.format` as its default output format
- direct speech-to-text uses `global.asr_output` as its default output mode

## Direct text-to-speech

When the user explicitly asks to convert text to speech:
1. use `scripts/liber_speech_client.py tts`
2. default to `wav` unless the caller explicitly requests another format
3. include `audio_prompt` only when clone audio is enabled and the file exists
4. return the TTS result URL or saved output path to the caller

## Direct speech-to-text

When the user explicitly asks to convert audio to text:
1. use `scripts/liber_speech_client.py asr`
2. default to structured `json` output
3. return plain text only when the caller explicitly wants transcript text only

## Telegram/openclaw workflow

For incoming Telegram voice/audio:
1. download or access the local audio file
2. send it to ASR and extract the recognized `text`
3. send the transcript to openclaw
4. if the final reply is too long for voice, shorten it to within the configured summary limit
5. synthesize the final spoken reply with Telegram-compatible `ogg_opus`
6. return the resulting audio URL or saved output path to the caller

## Telegram-specific guidance

For Telegram voice replies:
- force `ogg_opus` output
- keep spoken output concise and natural
- if the original answer is verbose, preserve intent and key facts but compress aggressively
- avoid reading markdown, code blocks, tables, or long lists verbatim

## Safety and robustness

- never print or log API keys
- validate input file existence before ASR
- validate text is non-empty before TTS
- use request timeouts
- handle HTTP failures with clear error messages
- if TTS clone audio is configured but missing, continue without cloning instead of failing
- if summarization fails, fall back to conservative truncation rather than blocking the reply
- default direct ASR output to JSON and default direct TTS output to WAV unless the caller requests otherwise

## Expected outputs

Depending on the task, return one of:
- structured ASR JSON
- plain transcript text
- concise voice-ready text
- TTS result URL
- saved audio file path
- a structured JSON object containing transcript, summary, and synthesis result
