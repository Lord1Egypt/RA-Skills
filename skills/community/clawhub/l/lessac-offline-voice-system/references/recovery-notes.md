# Recovery Notes

## Confirmed working fix (2026-04-05)

The working state required **all** of the following:

1. `messages.tts.provider = "microsoft"`
2. `messages.tts.providers.microsoft.voice = "en-IE-ConnorNeural"`
3. `messages.tts.providers.microsoft.lang = "en-IE"`
4. `plugins.entries.microsoft.enabled = true`
5. a **real manual gateway restart** after the config change

## Why this mattered

OpenClaw v2026.4.2 includes a bundled Microsoft speech extension that uses `node-edge-tts`.
The extension and dependency can both exist on disk while the live runtime still fails with:

- `microsoft: no provider registered`
- `openai: not configured`

In this case, the fix was not more config-shape changes. The fix was explicit plugin enablement plus a real restart.

## Useful facts

- `edge` is a legacy alias and normalizes to `microsoft`
- direct provider blocks are migrated to `messages.tts.providers.*`
- do not start by deleting `~/.openclaw/tts`
- test direct TTS before blaming Telegram delivery

## Local runtime helper path

The local transcription helper remains useful and should stay in place:

- `/root/.openclaw/tts/transcribe-audio`

The local Python venv at `/root/.openclaw/tts/venv` was able to synthesize Edge-backed speech successfully in standalone testing.
