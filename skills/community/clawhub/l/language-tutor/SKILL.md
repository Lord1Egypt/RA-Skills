---
name: senseaudio-language-tutor
description: Create language learning audio with SenseAudio TTS, including pronunciation drills, bilingual lessons, slowed speech practice, and dialogue exercises. Use when users need language learning materials, pronunciation practice, or vocabulary audio.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - python3
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
    install:
      - kind: uv
        package: requests
      - kind: uv
        package: pydub
    # Optional runtime helper; pydub commonly needs ffmpeg available locally
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
homepage: https://senseaudio.cn
source: https://github.com/anthropics/skills
---

# SenseAudio Language Tutor

Create interactive language-learning audio with official SenseAudio TTS endpoints and parameters.

## What This Skill Does

- Generate pronunciation examples in supported voices
- Create bilingual vocabulary and sentence practice audio
- Produce slowed-speed listening drills for learners
- Build short dialogue exercises with repetition pauses
- Export lesson audio files and companion study notes

## Credential and Dependency Rules

- Read the API key from `SENSEAUDIO_API_KEY`.
- Send auth only as `Authorization: Bearer <API_KEY>`.
- Do not place API keys in query parameters, logs, or saved examples.
- If Python helpers are used, this skill expects `python3`, `requests`, and `pydub`.
- `pydub` may also require a local audio backend such as `ffmpeg`; if unavailable, prefer writing individual audio files instead of merging them.

## Official TTS Constraints

Use the official SenseAudio TTS rules summarized below:

- HTTP endpoint: `POST https://api.senseaudio.cn/v1/t2a_v2`
- Model: `SenseAudio-TTS-1.0`
- Max text length: `10000` characters
- `voice_setting.voice_id` is required
- `voice_setting.speed` range: `0.5-2.0`
- Optional audio format values: `mp3`, `wav`, `pcm`, `flac`
- Optional sample rates: `8000`, `16000`, `22050`, `24000`, `32000`, `44100`
- Optional MP3 bitrates: `32000`, `64000`, `128000`, `256000`
- Optional channels: `1` or `2`

## Recommended Workflow

1. Prepare lesson content:
- Split vocabulary, example sentences, and dialogues into short chunks.
- Keep each API call comfortably below the `10000` character limit.

2. Build minimal TTS requests:
- Send `model`, `text`, `stream`, and `voice_setting.voice_id`.
- Add `speed`, `pitch`, `vol`, and `audio_setting` only when needed.

3. Decode and save audio safely:
- HTTP responses return hex-encoded audio in `data.audio`; decode before saving.
- Keep filenames deterministic and avoid exposing secrets in paths or logs.

4. Compose lessons carefully:
- If `pydub` and an audio backend are available, merge clips and insert silence.
- Otherwise, emit per-word or per-sentence clips and a manifest/Markdown study guide.

5. Handle failures and traceability:
- Check HTTP status and provider error payloads before decoding audio.
- Record `trace_id` only for troubleshooting and avoid showing it unless needed.

## Minimal Helper

```python
import binascii
import os

import requests

API_KEY = os.environ["SENSEAUDIO_API_KEY"]
API_URL = "https://api.senseaudio.cn/v1/t2a_v2"


def generate_tts(text, voice_id="male_0004_a", speed=1.0, stream=False):
    payload = {
        "model": "SenseAudio-TTS-1.0",
        "text": text,
        "stream": stream,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
        },
        "audio_setting": {
            "format": "mp3",
            "sample_rate": 32000,
            "bitrate": 128000,
            "channel": 2,
        },
    }
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    audio_hex = data["data"]["audio"]
    return binascii.unhexlify(audio_hex), data.get("trace_id")
```

## Patterns

### Vocabulary Drill

- Generate one clip for the target word
- Generate one clip for an example sentence
- Optionally generate a slower clip at `speed=0.8`
- Save clips separately or merge with pauses

### Bilingual Lesson

- Alternate source phrase and translated phrase
- Use short pauses (`1000-2000ms`) between clips
- Consider different `voice_id` values for source and translation when helpful

### Dialogue Practice

- Create one clip per line of dialogue
- Insert repetition pauses after each line
- Prefer shorter turns for easier debugging and regeneration

## Output Options

- Individual MP3 clips for words, sentences, or dialogue turns
- Merged lesson audio if local audio tooling is available
- Markdown study guide with transcript, translation, and file manifest

## Safety Notes

- Do not hardcode credentials.
- Do not claim unsupported language-selection parameters for TTS unless the official docs add them.
- Avoid assuming raw bytes can be passed directly to `pydub.AudioSegment`; decode and load through a supported container format.
