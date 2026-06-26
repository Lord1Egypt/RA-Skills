---
name: speech-to-text
description: Transcribe or translate audio files to text using a public Hugging Face Whisper Space over Gradio. Use when the user sends voice notes, audio attachments, meeting clips, podcasts, interviews, or any local audio file (.ogg, .mp3, .wav, .m4a, etc.) and wants a transcript, rough captions, or an English translation without relying on paid APIs first.
---

# Speech to Text

Use this skill to turn local audio files into text with a public Whisper-based endpoint.

## Quick start

Run:

```bash
python3 scripts/transcribe.py /path/to/file.ogg
```

Return the transcript as plain text. By default, the script also applies lightweight Chinese punctuation and sentence-breaking cleanup.

For machine-readable output:

```bash
python3 scripts/transcribe.py /path/to/file.ogg --json
```

To disable cleanup and keep the raw model text:

```bash
python3 scripts/transcribe.py /path/to/file.ogg --format raw
```

To force Chinese punctuation cleanup:

```bash
python3 scripts/transcribe.py /path/to/file.ogg --format zh
```

For English translation instead of same-language transcription:

```bash
python3 scripts/transcribe.py /path/to/file.ogg --task translate
```

## Workflow

1. Confirm the input is a local audio file.
2. Run `scripts/transcribe.py` on it.
3. If the transcript looks imperfect, tell the user it came from a public Whisper endpoint and may need cleanup.
4. If helpful, post-process into:
   - cleaned transcript
   - summary
   - action items
   - bilingual output

## What the script does

The script:

- uploads the local file to a public Gradio-backed Hugging Face Space
- submits a Whisper transcription job
- waits for completion via the Gradio event stream
- prints the resulting text

Default endpoint:

- `https://hf-audio-whisper-large-v3-turbo.hf.space`

Override it with:

```bash
python3 scripts/transcribe.py input.ogg --space https://your-space.hf.space
```

or set:

```bash
export HF_WHISPER_SPACE=https://your-space.hf.space
```

## Guardrails

- Treat this as a best-effort public/free path, not a privacy-grade path.
- Do not use for highly sensitive audio unless the user explicitly accepts public third-party processing.
- Expect rate limits, queueing, and occasional outages.
- If the public endpoint fails, explain that the free backend is unavailable and offer alternatives.

## Output handling

Prefer to return:

- the raw transcript when the user asked to "转文字/听写"
- a cleaned version when punctuation is poor
- a short note about uncertainty if names, numbers, or jargon may be wrong

## Script

- `scripts/transcribe.py` — public Whisper transcription helper
