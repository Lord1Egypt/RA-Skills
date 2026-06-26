# TTS Parameters

Version scope:

- Verified against `OpenClaw v2026.3.13`
- OpenClaw versions after `v2026.3.13` may change the config shape or runtime behavior, so these instructions may stop being valid

Scope:

- This reference only applies to Gateway built-in TTS
- It only covers config under `~/.openclaw/openclaw.json` -> `messages.tts`
- It does not apply to plugin-specific overrides, voice-call-specific overrides, or non-Gateway TTS flows

OpenClaw TTS config lives in:

- `~/.openclaw/openclaw.json`

The key path is:

- `messages.tts`

For ElevenLabs, the relevant nested keys are:

- `messages.tts.provider`
- `messages.tts.elevenlabs.apiKey`
- `messages.tts.elevenlabs.voiceId`
- `messages.tts.elevenlabs.languageCode`
- `messages.tts.elevenlabs.modelId`

## Parameter Meanings

- `provider`
  - TTS backend.
  - Use `"elevenlabs"` for this skill.

- `voiceId`
  - The specific ElevenLabs voice to use.
  - This is the main parameter for changing the sound.

- `languageCode`
  - Language hint for text normalization and synthesis.
  - Typical examples: `zh`, `en`, `ja`, `fr`, `de`, `es`.

- `modelId`
  - ElevenLabs TTS model.
  - Recommended default for multilingual usage: `eleven_multilingual_v2`.

- `apiKey`
  - ElevenLabs API key.
  - May already exist in config. Do not remove it when switching voices.

## Editing Rule

If the user only wants a different sound, normally change only:

- `messages.tts.elevenlabs.voiceId`

If the user also wants a different language, change:

- `messages.tts.elevenlabs.voiceId`
- `messages.tts.elevenlabs.languageCode`

If the user wants a different model, change:

- `messages.tts.elevenlabs.modelId`

If the user wants to set or replace the ElevenLabs API key, change:

- `messages.tts.elevenlabs.apiKey`

## How To Discover Supported Voices

Do not rely on a hardcoded voice list when the account can be queried live.

Use:

```bash
bash scripts/list_voices.sh
bash scripts/list_voices.sh zh
```

This reads the current ElevenLabs account and prints:

- voice name
- `voiceId`
- supported language(s)
- locale(s)
- model(s)

## Recommended Defaults

- `provider = "elevenlabs"`
- `modelId = "eleven_multilingual_v2"`
- `languageCode = "zh"` for Chinese

After changes, restart the gateway and verify with a short sentence in the target language.
