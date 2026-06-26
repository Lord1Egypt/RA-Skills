---
name: audiopod
description: Use SkillBoss API Hub for audio processing tasks including AI music generation (text-to-music, instrumentals, samples), text-to-speech, speech-to-text transcription, stem separation, noise reduction, and speaker separation. Use when the user needs to generate music/songs from text, generate speech from text, transcribe audio/video, or process audio. Requires SKILLBOSS_API_KEY env var.
---

> 📖 **Complete setup guide**: https://skillboss.co/skill.md


# SkillBoss Audio Processing

Full audio processing via SkillBoss API Hub: music generation, TTS, STT, stem separation, noise reduction, speaker separation.

## Setup

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillboss.co/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()
```

Auth: set `SKILLBOSS_API_KEY` env var. All requests use `Authorization: Bearer $SKILLBOSS_API_KEY`.

---

## AI Music Generation

Generate songs, instrumentals, samples, and vocals from text prompts via SkillBoss API Hub.

**Capabilities:** music generation (full song with vocals), instrumental, rap, samples, audio-to-audio style transfer

### Python

```python
# Generate a full song
result = pilot({
    "type": "music",
    "inputs": {
        "prompt": "Upbeat pop, synth, drums, 120 bpm, female vocals, radio-ready",
        "lyrics": "Verse 1:\nWalking down the street on a sunny day\n\nChorus:\nWe're on fire tonight!",
        "duration": 60
    },
    "prefer": "quality"
})
audio_url = result["data"]["result"]["audio_url"]
print(audio_url)

# Generate instrumental (no lyrics needed)
result = pilot({
    "type": "music",
    "inputs": {
        "prompt": "Atmospheric ambient soundscape, uplifting, driving mood",
        "duration": 30
    },
    "prefer": "balanced"
})
audio_url = result["data"]["result"]["audio_url"]

# Generate rap
result = pilot({
    "type": "music",
    "inputs": {
        "prompt": "Lo-Fi Hip Hop, 100 BPM, male rap, melancholy, keyboard chords",
        "lyrics": "Verse 1:\nStarted from the bottom, now we climbing...",
        "duration": 60,
        "style": "rap"
    },
    "prefer": "balanced"
})
audio_url = result["data"]["result"]["audio_url"]

# Generate samples/loops
result = pilot({
    "type": "music",
    "inputs": {
        "prompt": "drum loop, sad mood",
        "duration": 15,
        "style": "samples"
    },
    "prefer": "balanced"
})
audio_url = result["data"]["result"]["audio_url"]
```

### cURL

```bash
# Generate full song
curl -X POST "https://api.skillboss.co/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"music","inputs":{"prompt":"upbeat pop, synth, 120bpm, female vocals","lyrics":"Walking down the street...","duration":60},"prefer":"quality"}'

# Generate instrumental
curl -X POST "https://api.skillboss.co/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"music","inputs":{"prompt":"ambient soundscape, uplifting","duration":30},"prefer":"balanced"}'

# Generate rap
curl -X POST "https://api.skillboss.co/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"music","inputs":{"prompt":"Lo-Fi Hip Hop, male rap, 100 BPM","lyrics":"Started from the bottom...","duration":60,"style":"rap"}}'

# Generate samples
curl -X POST "https://api.skillboss.co/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"music","inputs":{"prompt":"drum loop, sad mood","duration":15,"style":"samples"}}'
```

### Parameters

| Field | Required | Description |
|-------|----------|-------------|
| prompt | yes | Style/genre description |
| lyrics | for song/rap/vocals | Song lyrics with verse/chorus structure |
| duration | no | Duration in seconds (default: 30) |
| style | no | `rap`, `samples`, `instrumental`, `vocals` — hints for routing |

### Response

```python
audio_url = result["data"]["result"]["audio_url"]
```

---

## Stem Separation

Split audio into individual instrument/vocal tracks via SkillBoss API Hub audio routing.

### Modes

| Mode | Stems | Output | Use Case |
|------|-------|--------|----------|
| single | 1 | Specified stem only | Vocal isolation, drum extraction |
| two | 2 | vocals + instrumental | Karaoke tracks |
| four | 4 | vocals, drums, bass, other | Standard remixing (default) |
| six | 6 | + guitar, piano | Full instrument separation |
| producer | 8 | + kick, snare, hihat | Beat production |
| studio | 12 | + cymbals, sub_bass, synth | Professional mixing |
| mastering | 16 | Maximum detail | Forensic analysis |

**Single stem options:** vocals, drums, bass, guitar, piano, other

### Python

```python
# Extract stems from URL
result = pilot({
    "type": "audio",
    "capability": "stem separation",
    "inputs": {
        "url": "https://youtube.com/watch?v=VIDEO_ID",
        "mode": "six"
    },
    "prefer": "quality"
})
download_urls = result["data"]["result"]["download_urls"]
for stem, url in download_urls.items():
    print(f"{stem}: {url}")

# Extract from local file (base64-encoded)
import base64
audio_b64 = base64.b64encode(open("/path/to/song.mp3", "rb").read()).decode()
result = pilot({
    "type": "audio",
    "capability": "stem separation",
    "inputs": {
        "audio_data": audio_b64,
        "filename": "song.mp3",
        "mode": "four"
    },
    "prefer": "balanced"
})
download_urls = result["data"]["result"]["download_urls"]

# Single stem extraction
result = pilot({
    "type": "audio",
    "capability": "stem separation",
    "inputs": {
        "url": "https://youtube.com/watch?v=ID",
        "mode": "single",
        "stem": "vocals"
    },
    "prefer": "quality"
})
vocal_url = result["data"]["result"]["download_urls"]["vocals"]
```

### cURL

```bash
# Extract stems from URL
curl -X POST "https://api.skillboss.co/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"audio","capability":"stem separation","inputs":{"url":"https://youtube.com/watch?v=VIDEO_ID","mode":"six"},"prefer":"quality"}'

# Single stem
curl -X POST "https://api.skillboss.co/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"audio","capability":"stem separation","inputs":{"url":"URL","mode":"single","stem":"vocals"}}'
```

### Response Format

```json
{
  "data": {
    "result": {
      "download_urls": {
        "vocals": "https://...",
        "drums": "https://...",
        "bass": "https://...",
        "other": "https://..."
      },
      "quality_scores": {
        "vocals": 0.95,
        "drums": 0.88
      }
    }
  }
}
```

---

## Text to Speech

Generate speech from text with 50+ voices in 60+ languages via SkillBoss API Hub.

### Python

```python
# Generate speech
result = pilot({
    "type": "tts",
    "inputs": {
        "text": "Hello, world! This is a test.",
        "voice": "alloy",
        "speed": 1.0
    },
    "prefer": "balanced"
})
audio_url = result["data"]["result"]["audio_url"]
print(audio_url)

# Specify language
result = pilot({
    "type": "tts",
    "inputs": {
        "text": "Bonjour le monde",
        "voice": "alloy",
        "language": "fr",
        "speed": 1.0
    },
    "prefer": "quality"
})
audio_url = result["data"]["result"]["audio_url"]
```

### cURL

```bash
# Generate speech
curl -X POST "https://api.skillboss.co/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"tts","inputs":{"text":"Hello world, this is a test","voice":"alloy","speed":1.0},"prefer":"balanced"}'
```

### Parameters

| Field | Required | Description |
|-------|----------|-------------|
| text | yes | Text to speak (max 5000 chars) |
| voice | no | Voice name or ID (e.g. `alloy`, `echo`, `fable`) |
| speed | no | 0.25 - 4.0 (default: 1.0) |
| language | no | ISO code, auto-detected if omitted |

### Response

```python
audio_url = result["data"]["result"]["audio_url"]
```

---

## Speaker Separation

Separate audio by speaker with automatic diarization via SkillBoss API Hub.

### Python

```python
# Diarize from file
import base64
audio_b64 = base64.b64encode(open("./meeting.mp3", "rb").read()).decode()
result = pilot({
    "type": "stt",
    "capability": "speaker diarization",
    "inputs": {
        "audio_data": audio_b64,
        "filename": "meeting.mp3",
        "num_speakers": 3
    },
    "prefer": "quality"
})
for segment in result["data"]["result"]["segments"]:
    print(f"Speaker {segment['speaker']}: {segment['text']} [{segment['start']:.1f}s - {segment['end']:.1f}s]")

# Diarize from URL
result = pilot({
    "type": "stt",
    "capability": "speaker diarization",
    "inputs": {
        "url": "https://youtube.com/watch?v=VIDEO_ID",
        "num_speakers": 2
    },
    "prefer": "balanced"
})
segments = result["data"]["result"]["segments"]
```

### cURL

```bash
# Diarize from URL
curl -X POST "https://api.skillboss.co/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"stt","capability":"speaker diarization","inputs":{"url":"https://youtube.com/watch?v=VIDEO_ID","num_speakers":2},"prefer":"balanced"}'
```

---

## Speech to Text (Transcription)

Transcribe audio/video with speaker diarization, word-level timestamps, and multiple output formats via SkillBoss API Hub.

### Python

```python
# Transcribe from URL
result = pilot({
    "type": "stt",
    "inputs": {
        "url": "https://youtube.com/watch?v=VIDEO_ID",
        "speaker_diarization": True,
        "word_timestamps": True
    },
    "prefer": "balanced"
})
text = result["data"]["result"]["text"]
segments = result["data"]["result"].get("segments", [])
print(f"Transcript: {text}")
for seg in segments:
    print(f"[{seg.get('start', 0):.1f}s] {seg.get('speaker','?')}: {seg['text']}")

# Transcribe local file
import base64
audio_b64 = base64.b64encode(open("./recording.mp3", "rb").read()).decode()
result = pilot({
    "type": "stt",
    "inputs": {
        "audio_data": audio_b64,
        "filename": "recording.mp3",
        "language": "en",
        "speaker_diarization": True
    },
    "prefer": "balanced"
})
text = result["data"]["result"]["text"]
```

### cURL

```bash
# Transcribe from URL
curl -X POST "https://api.skillboss.co/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"stt","inputs":{"url":"https://youtube.com/watch?v=ID","speaker_diarization":true,"word_timestamps":true},"prefer":"balanced"}'
```

### Parameters

| Field | Required | Description |
|-------|----------|-------------|
| url | yes (or audio_data) | URL to transcribe (YouTube, SoundCloud, direct links) |
| audio_data | yes (or url) | Base64-encoded audio content |
| filename | with audio_data | Original filename for format detection |
| language | no | ISO 639-1 code (auto-detected if omitted) |
| speaker_diarization | no | Enable speaker identification (default: false) |
| word_timestamps | no | Enable word-level timestamps (default: true) |

### Response

```python
text = result["data"]["result"]["text"]
segments = result["data"]["result"].get("segments", [])  # with speaker_diarization
```

---

## Noise Reduction

Remove background noise from audio files via SkillBoss API Hub.

### Python

```python
# Denoise from file
import base64
audio_b64 = base64.b64encode(open("./noisy-audio.mp3", "rb").read()).decode()
result = pilot({
    "type": "audio",
    "capability": "noise reduction",
    "inputs": {
        "audio_data": audio_b64,
        "filename": "noisy-audio.mp3"
    },
    "prefer": "quality"
})
clean_url = result["data"]["result"]["audio_url"]
print(f"Clean audio: {clean_url}")

# Denoise from URL
result = pilot({
    "type": "audio",
    "capability": "noise reduction",
    "inputs": {
        "url": "https://example.com/noisy.mp3"
    },
    "prefer": "balanced"
})
clean_url = result["data"]["result"]["audio_url"]
```

### cURL

```bash
# Denoise from URL
curl -X POST "https://api.skillboss.co/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"audio","capability":"noise reduction","inputs":{"url":"https://example.com/noisy.mp3"},"prefer":"quality"}'
```

### Response

```python
clean_url = result["data"]["result"]["audio_url"]
```

---

## Chain Mode (Multi-step Workflow)

Use SkillBoss Chain mode to combine multiple audio steps in one call.

### Python

```python
# STT → Chat (summarize) → TTS pipeline
result = pilot({
    "chain": [
        {"type": "stt"},
        {"type": "chat", "capability": "summarize"},
        {"type": "tts"}
    ]
})

# Transcribe and translate
result = pilot({
    "chain": [
        {"type": "stt"},
        {"type": "chat", "capability": "translate to English"}
    ]
})
```

---

## API Endpoint Summary

All capabilities route through a single endpoint:

| Service | SkillBoss type | capability |
|---------|---------------|------------|
| Music generation | `music` | — |
| TTS | `tts` | — |
| STT / Transcription | `stt` | — |
| Speaker separation | `stt` | `speaker diarization` |
| Stem separation | `audio` | `stem separation` |
| Noise reduction | `audio` | `noise reduction` |

**Single endpoint:** `POST https://api.skillboss.co/v1/pilot`
**Auth:** `Authorization: Bearer $SKILLBOSS_API_KEY`

## Response Format Summary

| Capability | Result path |
|-----------|-------------|
| Music generation | `data.result.audio_url` |
| TTS | `data.result.audio_url` |
| STT (text) | `data.result.text` |
| STT (segments) | `data.result.segments` |
| Stem separation | `data.result.download_urls` |
| Noise reduction | `data.result.audio_url` |
