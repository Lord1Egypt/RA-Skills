---
name: audio-processing
description: "Privacy-first local audio toolkit for OpenClaw: transcribe voice notes, create timestamped segments, extract features, detect speech, and run deterministic FFmpeg transforms. Use remote TTS only when explicitly requested and network consent is provided."
license: MIT-0
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins: ["ffmpeg", "python3"]
      pip: ["openai-whisper", "gTTS", "librosa", "numpy"]
    version: "1.3.1"
---

# Privacy-first audio toolkit

Use `tool.py` for local Whisper transcription and deterministic audio utilities. Input and output paths must resolve inside the current workspace; symlinks that escape it are rejected. Local actions do not make network requests.

## Hero workflow: transcription

```bash
python tool.py transcribe --file_path meeting.m4a --model turbo
python tool.py transcribe --file_path meeting.m4a --model base
```

The command returns JSON with transcript text and timestamped segments. Whisper models are local after their initial model download. Use smaller models for speed and larger models for accuracy.

## Actions

- `transcribe`: local Whisper transcription with `tiny`, `base`, `small`, `medium`, `large`, or `turbo`.
- `tts`: Google TTS only with explicit `--allow-network`; text is sent to Google. Set `--lang` for a language code and never pass secrets or confidential transcripts.
- `extract_features`: duration, sample rate, mean MFCCs, and mean RMS.
- `vad_segments`: FFmpeg silence-based speech segments; `--aggressiveness` is 0–3.
- `transform`: JSON operations `trim`, `resample`, and `normalize`.

## Remote TTS consent

Remote TTS is fail-closed. Invoke it only after confirming the text may leave the workspace:

```bash
python tool.py tts --text "Hello" --output_path hello.mp3 --lang en --allow-network
```

FFmpeg uses an argument list without a shell, bounded execution time, and stripped output metadata. The package must contain only intentional source files; never publish `__pycache__`, `.pyc`, `.pyo`, or `.pyd` artifacts.

## Source and support

Source: https://github.com/iyeque/openclaw-skills/tree/main/skills/audio-processing

Report bugs and security concerns through the repository issue guidance.
