---
name: openclaw-whisper-voice
description: Local Whisper speech-to-text for audio files and inbound voice notes on the OpenClaw Gateway host. Use when setting up local transcription for WhatsApp, Telegram, or other audio attachments; when configuring tools.media.audio with a CLI fallback instead of a cloud API; or when you need a reusable shell entrypoint that makes Whisper + ffmpeg work reliably on Linux.
metadata:
  {
    "openclaw": {
      "emoji": "🎙️",
      "requires": { "bins": ["whisper", "ffmpeg"] },
      "install": [
        {
          "id": "local-whisper-user-install",
          "kind": "manual",
          "label": "Run scripts/install_local_whisper.sh on the Gateway host"
        }
      ]
    }
  }
---

# OpenClaw Whisper Voice

Use this skill to make local Whisper transcription dependable on the OpenClaw Gateway host.

## Install on the host

Run:

```bash
{baseDir}/scripts/install_local_whisper.sh
```

The installer:

- installs Python packages into `~/.local`
- installs a CPU-safe PyTorch build
- installs `openai-whisper`
- installs `imageio-ffmpeg`
- creates stable `~/.local/bin/whisper` and `~/.local/bin/ffmpeg` launchers

## Transcribe a file manually

Use the wrapper instead of raw `whisper` when reliability matters:

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --model tiny --stdout-only
{baseDir}/scripts/transcribe.sh /path/to/audio.mp3 --task translate --format srt
```

## Configure inbound WhatsApp and Telegram voice notes

Patch OpenClaw config so inbound audio uses the wrapper:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        timeoutSeconds: 120,
        models: [
          {
            type: "cli",
            command: "{baseDir}/scripts/transcribe.sh",
            args: ["{{MediaPath}}", "--model", "base", "--stdout-only"],
            timeoutSeconds: 120
          }
        ]
      }
    }
  }
}
```

## Model choices

- `tiny`: fastest, weakest accuracy
- `base`: best default for chat voice notes
- `small` or larger: better accuracy, heavier CPU and RAM use

## Output rules

- Use `--stdout-only` for `tools.media.audio` so stdout is only transcript text.
- Use `--format txt|srt|vtt|json` for standalone file transcription.
- First model download goes into `~/.cache/whisper`.
