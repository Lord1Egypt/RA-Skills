---
name: senseaudio-meeting-summarizer
description: Transcribe meetings with SenseAudio ASR speaker diarization, timestamps, and meeting-note extraction workflows. Use when users need meeting transcription, meeting notes, speaker-separated transcripts, or action-item extraction from recordings.
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
        package: websockets
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
homepage: https://senseaudio.cn
---

# SenseAudio Meeting Summarizer

Transform meeting recordings into structured transcripts with speaker identification, timestamps, and local meeting summaries.

## What This Skill Does

- Transcribe recorded meetings with official SenseAudio ASR endpoints
- Separate speakers with diarization on supported models
- Generate word and segment timestamps for navigation
- Produce local summaries and action-item candidates from transcripts
- Support optional realtime transcription for live meetings
- Export transcript and notes in text-friendly formats

## Credential and Dependency Rules

- Read the API key from `SENSEAUDIO_API_KEY`.
- Send auth only as `Authorization: Bearer <API_KEY>`.
- Do not place API keys in query parameters, logs, or saved examples.
- If Python helpers are used, this skill expects `python3`, `requests`, and `websockets`.
- This skill should work without any external LLM credentials.
- If a user explicitly asks for LLM-based summarization, require a separately declared credential for that provider instead of assuming one exists.

## Official ASR Constraints

Use the official SenseAudio ASR rules summarized below:

- HTTP endpoint: `POST https://api.senseaudio.cn/v1/audio/transcriptions`
- WebSocket endpoint: `wss://api.senseaudio.cn/ws/v1/audio/transcriptions`
- File upload limit: `<=10MB` per request
- Meeting-oriented HTTP model: `sense-asr-pro`
- Realtime WebSocket model: `sense-asr-deepthink`
- `enable_speaker_diarization` is supported only on `sense-asr` / `sense-asr-pro`
- `max_speakers` is documented only for `sense-asr-pro`
- `enable_sentiment` and `timestamp_granularities[]` are supported only on `sense-asr` / `sense-asr-pro`
- WebSocket audio must be `pcm`, `16000Hz`, mono

## Recommended Workflow

1. Validate the meeting asset:
- Prefer clear audio with limited background noise.
- Split files larger than `10MB` before upload.

2. Transcribe with the right mode:
- Use HTTP `sense-asr-pro` for recorded meetings needing diarization and timestamps.
- Use WebSocket `sense-asr-deepthink` only for live streaming scenarios.

3. Request only needed features:
- For meeting notes, use `response_format=verbose_json`.
- Enable diarization, timestamps, and sentiment only when the user needs them.
- Provide `max_speakers` only when known and using `sense-asr-pro`.

4. Summarize locally first:
- Build summaries, decisions, and action-item candidates from the transcript itself.
- Keep the no-extra-credentials path as the default behavior.

5. Handle sensitive output carefully:
- Treat returned `session_id`, `trace_id`, and transcript contents as potentially sensitive.
- Do not expose provider identifiers unless needed for debugging.

## Minimal HTTP Transcription Helper

```python
import os

import requests

API_KEY = os.environ["SENSEAUDIO_API_KEY"]
API_URL = "https://api.senseaudio.cn/v1/audio/transcriptions"


def transcribe_meeting(audio_file, max_speakers=None, language=None, target_language=None):
    with open(audio_file, "rb") as handle:
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            files={"file": handle},
            data={
                "model": "sense-asr-pro",
                "response_format": "verbose_json",
                "enable_speaker_diarization": "true",
                "enable_sentiment": "true",
                "enable_punctuation": "true",
                "timestamp_granularities[]": ["word", "segment"],
                **({"max_speakers": max_speakers} if max_speakers else {}),
                **({"language": language} if language else {}),
                **({"target_language": target_language} if target_language else {}),
            },
            timeout=300,
        )
    response.raise_for_status()
    return response.json()
```

## Transcript Processing Pattern

- Read `text` for the full transcript
- Read `segments` for speaker-separated timeline entries
- Use `speaker`, `start`, `end`, `text`, and optional `sentiment` fields when present
- Use `words` only when word timestamps were requested

## Local Summary Pattern

Generate notes from transcript structure without external services:

- `summary`: 3-6 bullets capturing the meeting arc
- `decisions`: statements containing agreements or final choices
- `action_items`: statements with owners, deadlines, or explicit follow-ups
- `participants`: derived from speaker labels
- `timeline`: ordered segments with timestamps

Heuristics that work without an LLM:

- Detect action items from patterns like `will`, `need to`, `follow up`, `by Friday`
- Detect decisions from patterns like `decided`, `agreed`, `we will`, `final choice`
- Aggregate speaker time by summing `end - start`

## Realtime Meeting Pattern

For live meetings, use WebSocket only when streaming audio is actually available.

```python
import asyncio
import json
import os

import websockets

API_KEY = os.environ["SENSEAUDIO_API_KEY"]
WS_URL = "wss://api.senseaudio.cn/ws/v1/audio/transcriptions"


async def transcribe_live_meeting(audio_stream):
    async with websockets.connect(
        WS_URL,
        additional_headers={"Authorization": f"Bearer {API_KEY}"},
    ) as ws:
        await ws.recv()
        await ws.send(json.dumps({
            "event": "task_start",
            "model": "sense-asr-deepthink",
            "audio_setting": {
                "sample_rate": 16000,
                "format": "pcm",
                "channel": 1,
            },
        }))

        async for audio_chunk in audio_stream:
            await ws.send(audio_chunk)

        await ws.send(json.dumps({"event": "task_finish"}))
```

## Output Options

- Full transcript with timestamps in `txt` or `json`
- Meeting notes in `md`
- Action-item list in `json` or `csv`
- Speaker statistics in `json`
- Optional sentiment timeline when requested

## Error Handling

- Poor audio quality: run an audio-quality check first or request a cleaner recording
- Large files: split recordings into chunks under `10MB`
- Wrong language detection: set `language` explicitly on HTTP transcription
- Too many speakers: provide `max_speakers` only with `sense-asr-pro`
- Realtime failures: inspect WebSocket `task_failed` and `base_resp.status_msg`

## Safety Notes

- Do not assume any external summarization provider credential exists.
- Do not add an LLM call unless the user asks for it and the skill metadata is updated to declare that credential.
- Prefer local transcript-based summarization for the default path.
