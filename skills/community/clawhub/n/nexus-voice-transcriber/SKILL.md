---
name: voice-transcriber
description: Voice note transcription and archival for OpenClaw agents. Powered by Deepgram Nova-3 or local Whisper. Transcribes audio messages, saves both audio files and text transcripts.
homepage: https://clawhub.ai/skills/voice-transcriber
metadata: {"openclaw":{"emoji":"🎙️","requires":{"bins":["ffmpeg","python3"]},"os":["linux","darwin","win32"]}}
---

## Setup

On first use, read `references/whisper-models.md` and `references/troubleshooting.md`.  
Ensure dependencies: `ffmpeg`, `python3`, and required Python packages (`openai-whisper`, `deepgram-sdk` optional).

## When to Use

- User sends a voice note / audio file / video file that needs transcription.
- Need to archive both the original audio and the text transcript.
- Want speaker detection (if using Deepgram with diarization).
- Quick local transcription without external APIs (Whisper).

## Architecture

Memory lives in `~/voice-transcriber/`. See below for structure.

```
~/voice-transcriber/
├── memory.md          # Provider preferences, defaults, history
├── transcripts/       # Saved transcripts (txt, json, srt)
├── audio/             # Saved original audio files
└── temp/              # Processing workspace (auto-cleaned)
```

## Quick Reference

| Topic | File |
|-------|------|
| Whisper model guide | `references/whisper-models.md` |
| Troubleshooting | `references/troubleshooting.md` |
| Main script | `scripts/transcribe.py` |

## Core Rules

### 1. Detect Input Type
Before transcription:
- **Local file path** → verify exists, check format (mp3, wav, m4a, mp4, etc.)
- **URL** → download to `temp/`, then process
- **Voice memo** → usually single speaker, short
- **Meeting / interview** → likely multiple speakers, consider diarization

### 2. Choose Provider Based on Context
| Scenario | Best Provider | Why |
|----------|---------------|-----|
| Privacy, no API keys | Local Whisper | Runs on-device, free |
| High accuracy, speed | Deepgram Nova‑3 | Low latency, good accuracy |
| Speaker identification | Deepgram (with diarization) | Native speaker labels |
| No internet | Local Whisper | Offline capable |

### 3. Handle Long Audio
Files >25 MB or >2 hours:
1. Split into chunks with `ffmpeg` (see `scripts/transcribe.py --split`)
2. Process each chunk
3. Merge transcripts with proper timestamps

### 4. Save Artifacts
After successful transcription:
- Save transcript to `~/voice-transcriber/transcripts/` with a meaningful name
- Save original audio to `~/voice-transcriber/audio/` if user wants archival
- Update `memory.md` with date, file, provider, duration

### 5. Output Formats
Default to plain text (`.txt`). Offer alternatives:
- `.txt` — clean text, no timestamps
- `.srt` / `.vtt` — subtitles with timing
- `.json` — structured with word‑level timing (Deepgram) or segment timing (Whisper)

## Common Traps

- **Assuming one provider fits all** → Whisper lacks diarization; Deepgram needs API key.
- **Uploading huge files directly** → Timeouts. Split first.
- **Ignoring audio quality** → Noisy audio may need preprocessing (`ffmpeg` noise reduction).
- **Not checking language** → Whisper auto‑detects but can fail on mixed‑language content.
- **Forgetting to save audio** → User may want the original file archived.

## Requirements

**Required:**
- `ffmpeg` (audio conversion, splitting)
- `python3` + `pip`
- Python packages: `openai-whisper` (local), `requests` (for Deepgram if used)

**Optional API keys (only if using Deepgram):**
- `DEEPGRAM_API_KEY` — for Deepgram Nova‑3 (speaker diarization available)

Local Whisper works without any API keys.

## Provider Quick Reference

### Local Whisper (No API Key)
```bash
# Install
pip install openai-whisper

# Basic transcription (via script)
python3 scripts/transcribe.py --file audio.wav --provider whisper --model base

# Output formats: txt (default), srt, vtt, json
python3 scripts/transcribe.py --file audio.wav --provider whisper --model medium --format srt
```

Models: `tiny` (fastest) → `base` → `small` → `medium` → `large` (most accurate).

### Deepgram Nova‑3 (API Key Required)
```bash
# Set environment variable
export DEEPGRAM_API_KEY="your_key_here"

# Transcribe with speaker diarization
python3 scripts/transcribe.py --file audio.wav --provider deepgram --diarize

# Output JSON with speaker labels
python3 scripts/transcribe.py --file audio.wav --provider deepgram --format json
```

## Audio Preprocessing

### Extract Audio from Video
```bash
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
```

### Reduce Noise
```bash
ffmpeg -i noisy.wav -af "afftdn=nf=-25" clean.wav
```

### Split Long Audio (10‑minute chunks)
```bash
ffmpeg -i long.mp3 -f segment -segment_time 600 -c copy temp/chunk_%03d.mp3
```

## Security & Privacy

**Data that stays local:**
- Transcripts in `~/voice-transcriber/transcripts/`
- Original audio in `~/voice-transcriber/audio/`
- Local Whisper processes entirely on‑device

**Data that leaves your machine (if using Deepgram):**
- Audio file sent to Deepgram API (`api.deepgram.com`)
- Transcript returned and stored locally

**This skill does NOT:**
- Store API keys in plain text (use environment variables)
- Auto‑upload without confirmation
- Retain files on external servers after processing

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `api.deepgram.com/v1/listen` | Audio file | Deepgram transcription |

Only called when user explicitly chooses Deepgram provider. Local Whisper sends nothing.

## Memory Template

Create `~/voice-transcriber/memory.md` with this structure:

```markdown
# Voice Transcriber Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY‑MM‑DD
integration: pending

## Context
<!-- Observations about transcription needs, preferred providers, languages, etc. -->

## Notes
<!-- Provider preferences, format preferences, diarization needs -->

---
*Updated: YYYY‑MM‑DD*
```

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `speech-to-text-transcription` — broader audio/video transcription with more providers
- `ffmpeg` — advanced audio/video processing
- `audio` — general audio manipulation

## Feedback
- If useful: `clawhub star voice-transcriber`
- Stay updated: `clawhub sync`
