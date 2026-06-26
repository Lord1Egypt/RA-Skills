---
name: mlx-whisper
description: >
  Set up mlx-whisper as the local audio transcription engine for OpenClaw on Apple Silicon Macs
  (M1/M2/M3/M4). Automatically transcribes voice notes sent via Telegram or WhatsApp before the
  agent processes them. Use when the user wants to enable voice message transcription locally
  without any API key, or asks to set up Whisper, mlx-whisper, or local speech-to-text in OpenClaw.
  Apple Silicon only (macOS darwin).
  Note: Requires internet for initial model download (~465MB), but runs inference locally.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "os": ["darwin"],
        "requires": { "bins": ["python3", "pip3"] },
        "install":
          [
            {
              "id": "pip-mlx-whisper",
              "kind": "exec",
              "command": "pip3",
              "args": ["install", "mlx-whisper"],
              "label": "Install mlx-whisper (Apple Silicon)",
            },
          ],
      },
  }
---

# mlx-whisper — Local Voice Transcription for Apple Silicon

Enables automatic transcription of voice notes in OpenClaw using Apple's MLX framework.
No API key required. Works fully offline. ~60× faster than standard Whisper on M1/M2/M3/M4.

## How it works

1. User sends a voice note (Telegram `.ogg` / WhatsApp `.opus`)
2. OpenClaw downloads the audio file
3. Passes it to `mlx-whisper-transcribe.sh` via `{{MediaPath}}`
4. Transcript is injected as the message body
5. Agent replies to the text content

## Setup

### Step 1 — Install mlx-whisper

```bash
pip3 install mlx-whisper
```

Verify:
```bash
python3 -c "import mlx_whisper; print('OK')"
```

### Step 2 — Install the wrapper script

Find the Python bin path:
```bash
python3 -m site --user-base
# e.g. /Users/<you>/Library/Python/3.9
```

Copy `bin/mlx-whisper-transcribe.sh` from this skill to `<user-base>/bin/mlx-whisper-transcribe.sh`, then make it executable:

```bash
PYBIN=$(python3 -m site --user-base)/bin
cp {baseDir}/bin/mlx-whisper-transcribe.sh "$PYBIN/mlx-whisper-transcribe.sh"
chmod +x "$PYBIN/mlx-whisper-transcribe.sh"
```

Test it:
```bash
"$PYBIN/mlx-whisper-transcribe.sh" /path/to/audio.ogg
# First run downloads the model (~465MB). Subsequent runs are instant.
```

### Step 3 — Configure OpenClaw

Add to `~/.openclaw/openclaw.json` under `tools.media.audio`:

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "models": [
          {
            "type": "cli",
            "command": "<user-base>/bin/mlx-whisper-transcribe.sh",
            "args": ["{{MediaPath}}"],
            "timeoutSeconds": 60
          }
        ]
      }
    }
  }
}
```

Replace `<user-base>` with the output of `python3 -m site --user-base`.

### Step 4 — Restart OpenClaw

```bash
openclaw gateway restart
```

Or restart the OpenClaw app from the menu bar.

## Models

The wrapper uses `whisper-small-mlx` by default (465MB, good balance of speed and accuracy).
To change, edit `bin/mlx-whisper-transcribe.sh` and update `path_or_hf_repo`:

| Model | Size | Use case |
|-------|------|----------|
| `mlx-community/whisper-tiny-mlx` | 75MB | Fastest, basic accuracy |
| `mlx-community/whisper-small-mlx` | 465MB | **Recommended** |
| `mlx-community/whisper-medium-mlx` | 1.5GB | Higher accuracy |
| `mlx-community/whisper-large-v3-mlx` | 3GB | Best accuracy |

## Language hint (optional)

Pass a language code as the second argument to skip auto-detection (faster):

```bash
mlx-whisper-transcribe.sh audio.ogg zh   # Chinese
mlx-whisper-transcribe.sh audio.ogg en   # English
```

In `openclaw.json`, add the language to args:
```json
"args": ["{{MediaPath}}", "zh"]
```

## Performance (M3 MacBook Pro, 8GB)

| Audio length | Transcription time |
|-------------|-------------------|
| 10 sec | ~1 sec |
| 1 min | ~7 sec |
| 30 min | ~3.5 min |

## Troubleshooting

- **`mlx_whisper not found`**: Run `pip3 install mlx-whisper` again
- **Empty transcript**: Audio may be silent or music-only (Whisper transcribes speech only)
- **Timeout**: Increase `timeoutSeconds` for long audio files
- **Wrong language**: Add `"language": "zh"` or the target language code to args
- **Model download fails**: Check internet connection; models are cached after first run in `~/.cache/huggingface`
