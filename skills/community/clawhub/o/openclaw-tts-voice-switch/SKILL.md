---
name: openclaw-tts-voice-switch
version: 1.0.0
description: Switch OpenClaw ElevenLabs TTS voices by updating ~/.openclaw/openclaw.json, keeping Chinese-safe defaults, and restarting the gateway.
metadata: {"openclaw":{"emoji":"🔊","requires":{"bins":["bash","jq","openclaw"]}}}
---

# OpenClaw TTS Voice Switch

Use this skill when you need to change the ElevenLabs voice used by OpenClaw Gateway built-in TTS.

Version scope:

- Verified against `OpenClaw v2026.3.13`
- Newer OpenClaw versions may change config keys, behavior, or restart flow, so this skill may not work without updates

Scope:

- This skill only targets Gateway built-in TTS under `messages.tts`
- It does not target other speech systems, external plugins, call-specific overrides, or unrelated TTS integrations

Read [references/tts-parameters.md](references/tts-parameters.md) when you need parameter meanings, file paths, or language/model guidance.

Use `scripts/list_voices.sh` when you need the actual voices and languages available in the current ElevenLabs account.

It updates:

- `~/.openclaw/openclaw.json`
- `messages.tts.elevenlabs.voiceId`

It keeps these defaults unless the user explicitly wants something else:

- `messages.tts.provider = "elevenlabs"`
- `messages.tts.elevenlabs.modelId = "eleven_multilingual_v2"`
- `messages.tts.elevenlabs.languageCode = "zh"`

## Workflow

1. If the user asks which voices or languages are supported, run:

```bash
bash scripts/list_voices.sh
bash scripts/list_voices.sh zh
```

2. Confirm the target voice name or `voiceId`.
3. If only a voice name is given, resolve it to a `voiceId` from the script output.
4. Run:

```bash
bash scripts/switch_tts_voice.sh "<voiceId>"
bash scripts/switch_tts_voice.sh "<voiceId>" "<languageCode>"
bash scripts/switch_tts_voice.sh "<voiceId>" "<languageCode>" "<modelId>"
bash scripts/switch_tts_voice.sh "<voiceId>" "<languageCode>" "<modelId>" "<apiKey>"
```

5. Tell the user which file and parameter changed.
6. Suggest a quick verification command:

```bash
/tts audio 今天天气不错，我们下午三点开会。
```

## Supported Inputs

- Direct `voiceId`
- Existing known Chinese-capable ElevenLabs `voiceId`
- Optional `languageCode`
- Optional `modelId`
- Optional `apiKey`

If the user only gives a voice name, resolve it to a `voiceId` first.
