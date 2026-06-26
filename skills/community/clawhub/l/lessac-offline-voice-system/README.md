# Edge TTS Voice Helper Runtime

This skill now exists to restore the **local helper runtime** only.

## Purpose

It reinstalls:
- a local `faster-whisper` transcription wrapper for OpenClaw native inbound audio processing
- local Edge TTS helper/test utilities
- the Python virtualenv and runtime directories in `~/.openclaw/tts`

It does **not** manage Telegram reply delivery.

## Recommended OpenClaw architecture

Keep routing native:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [
          {
            type: "cli",
            command: "/root/.openclaw/tts/transcribe-audio",
            args: ["{{MediaPath}}"],
            timeoutSeconds: 45
          }
        ]
      }
    }
  },
  messages: {
    tts: {
      auto: "inbound",
      provider: "microsoft",
      providers: {
        microsoft: {
          enabled: true,
          voice: "en-IE-ConnorNeural"
        }
      }
    }
  }
}
```

## Install

```bash
./scripts/install.sh
```

## Test

```bash
~/.openclaw/tts/transcribe-audio audio.ogg
~/.openclaw/tts/voice_integration.sh test
```

## Included files

- `scripts/install.sh`
- `scripts/transcribe-audio`
- `scripts/voice_handler.py`
- `scripts/tts_edge_wrapper.py`
- `scripts/voice_integration.sh`
- `scripts/test_skill.py`

## Notes

If OpenClaw is updated and the helper runtime disappears, rerun the installer. Keep live inbound audio handling and outbound voice replies in OpenClaw config, not in custom Telegram wrapper scripts.
