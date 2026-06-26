# Whisper Models Guide

Whisper is OpenAI’s open‑source speech‑recognition model. It runs **locally** (no API key) and supports 90+ languages.

## Available Models

| Model | Size | Speed | Accuracy | Recommended For |
|-------|------|-------|----------|-----------------|
| `tiny` | 39 MB | Fastest | Lowest | Quick drafts, short voice notes |
| `base` | 74 MB | Fast | Medium | Everyday transcription (default) |
| `small` | 244 MB | Medium | Good | Longer recordings, decent accuracy |
| `medium` | 769 MB | Slow | High | Interviews, meetings, important content |
| `large` | 1550 MB | Slowest | Highest | Final transcripts, professional use |

> **Rule of thumb:** `base` for speed, `medium` for quality. `large` is overkill unless you need maximum accuracy.

## Installation

```bash
pip install openai-whisper
```

On first use, Whisper will download the chosen model automatically (cached in `~/.cache/whisper/`).

## Language Support

Whisper auto‑detects language. To force a specific language:

```bash
python3 scripts/transcribe.py --file audio.wav --provider whisper --language en
```

Common language codes:
- `en` — English
- `es` — Spanish
- `fr` — French
- `de` — German
- `it` — Italian
- `pt` — Portuguese
- `zh` — Chinese
- `ja` — Japanese
- `ar` — Arabic

## Performance Tips

1. **GPU acceleration** (optional):  
   Install `torch` with CUDA support for faster transcription.
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```
2. **Reduce noise first** with ffmpeg:
   ```bash
   ffmpeg -i noisy.wav -af "afftdn=nf=-25" clean.wav
   ```
3. **Split very long files** (>2 hours) before processing to avoid memory issues.

## When to Use Whisper

✅ No API keys needed  
✅ Works offline  
✅ Private — audio never leaves your machine  
✅ Good accuracy for most use cases  

❌ No built‑in speaker diarization (can’t tell speakers apart)  
❌ Slower than cloud APIs on CPU  
❌ Large models consume significant RAM/disk
