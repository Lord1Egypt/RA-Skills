---
name: faster-whisper
description: Local speech-to-text with the faster-whisper backend (CTranslate2). Use when transcribing audio locally, setting up the faster-whisper model cache, or replacing a whisper-cli workflow with a faster local engine.
---

# Faster Whisper

## Overview

Use `faster-whisper` for local transcription with low latency and a reusable model cache.

## Rules

- Do not assume `ggml` models work here; `faster-whisper` uses CTranslate2 model folders.
- Prefer CPU `device='cpu'` and `compute_type='int8'` unless the machine is explicitly configured for GPU.
- Keep output plain text unless the user asks for timestamps or captions.

## Setup

1. Confirm `python` and `ffmpeg` are available.
2. Install the Python packages needed for local inference:
   - `faster-whisper`
   - `ctranslate2`
   - `huggingface_hub`
3. Use the project repo `https://github.com/SYSTRAN/faster-whisper` for install/setup guidance.
4. Download `Systran/faster-whisper-small` from `https://huggingface.co/Systran/faster-whisper-small` into a stable local folder such as:
   - `C:\Users\joshu\.openclaw\tools\faster-whisper\models\Systran-faster-whisper-small`
4. Reuse that folder for repeat runs.
5. If the user only has a `ggml-*.bin` file, explain that it belongs to whisper.cpp and is not usable here.

## Transcription

1. Convert Telegram OGG/Opus audio to WAV if needed.
2. Load the local model folder.
3. Transcribe and return the plain-text result.
