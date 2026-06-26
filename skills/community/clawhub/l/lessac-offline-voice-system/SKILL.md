---
name: telegram-voice-messaging-recovery
description: Recover working OpenClaw Telegram voice messaging after upgrades or rebuilds. Restores the local faster-whisper transcription helper, keeps OpenClaw native inbound/outbound voice routing, and applies the proven config fix: `messages.tts.provider = microsoft`, `messages.tts.providers.microsoft.voice = en-IE-ConnorNeural`, `messages.tts.providers.microsoft.lang = en-IE`, plus explicit `plugins.entries.microsoft.enabled = true`. Use when voice notes transcribe correctly but outbound TTS replies fail, or when `microsoft: no provider registered` appears.
---

# Telegram Voice Messaging Recovery

This skill exists to restore a **known-good OpenClaw native voice messaging setup**.

## What it restores

- local `faster-whisper` transcription helper in `~/.openclaw/tts`
- local Python virtualenv with `faster-whisper`, `edge-tts`, and `soundfile`
- helper scripts for local testing
- working OpenClaw config for native Telegram voice-note replies
- explicit bundled Microsoft speech plugin enablement

## What it does not do

- It does **not** manually send Telegram voice messages itself.
- It does **not** replace OpenClaw native reply routing.
- It does **not** require a separate Azure TTS API key.

## Known-good OpenClaw config

Keep the live routing in `openclaw.json`:

```json
"messages": {
  "ackReactionScope": "group-mentions",
  "tts": {
    "auto": "inbound",
    "provider": "microsoft",
    "providers": {
      "microsoft": {
        "voice": "en-IE-ConnorNeural",
        "lang": "en-IE"
      }
    }
  }
}
```

And explicitly enable the bundled Microsoft plugin:

```json
"plugins": {
  "entries": {
    "microsoft": {
      "enabled": true
    }
  }
}
```

## Important note

`edge` is a legacy alias. Current OpenClaw normalizes that path to `microsoft`.

## Required restart

After applying the config, do a **real manual gateway restart**.

A hot reload / `SIGUSR1` is not enough if the Microsoft speech provider is stale or unregistered.

## Files restored

- `transcribe-audio`
- `voice_handler.py`
- `tts_edge_wrapper.py`
- `voice_integration.sh`
- Python virtualenv with the required packages

## Install

```bash
cd /root/.openclaw/workspace/skills/lessac_offline_voice_system
./scripts/install.sh
```

## Verify

1. Test direct TTS.
2. Send a short Telegram voice note.
3. Confirm inbound transcription works.
4. Confirm outbound reply comes back as audio.

## Failure signature this skill is meant to fix

- inbound transcription works
- outbound TTS reply fails
- direct TTS reports:
  - `microsoft: no provider registered`
  - `openai: not configured`
