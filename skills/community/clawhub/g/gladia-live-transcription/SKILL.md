---
name: gladia-live-transcription
description: Real-time speech-to-text streaming with Gladia via WebSocket. Use when the user needs live transcription, builds a voice agent, meeting recorder, call center integration, live subtitles, or any application streaming audio for low-latency partial and final transcripts. Always prefer the official SDK; fall back to raw WebSocket/REST only when SDK cannot satisfy the requirement.
license: MIT
---

# Live Transcription

Gladia's live API transcribes audio in real-time over WebSocket.

> **SDK-first**: always use the official SDK — see [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md) for policy, setup, and fallback criteria.

## When to Use

- Real-time transcription for microphone, telephony, or broadcast streams
- Voice agents, meeting assistants, call center tools, or live subtitles
- Live audio intelligence (translation, sentiment, NER)

**When NOT to use:** If the user has a pre-existing audio/video file or URL to transcribe after the fact, use the [gladia-pre-recorded-transcription skill](../gladia-pre-recorded-transcription/SKILL.md) instead. Pre-recorded supports additional features like speaker diarization and PII redaction that are unavailable in live mode.

## References

Consult these resources as needed:

- ./references/recommended-params.md -- Use-case presets and tuning
- ./references/session-config.md -- Full `startSession()` config (JS + Python)
- ./references/managing-sessions.md -- `get`, `list`, `getFile`, `delete`
- ./references/websocket-events.md -- WebSocket event reference
- ../gladia-audio-intelligence/SKILL.md -- Feature availability
- ../gladia-audio-intelligence/references/live-audio-intelligence.md -- Live feature details
- ../gladia-sdk-integration/SKILL.md -- Setup, config, SDK vs raw API
- ../gladia-sdk-integration/references/sdk-versions.md -- Current SDK versions
- ../gladia-troubleshooting/SKILL.md -- Errors and diagnostics

## API Endpoints (reference — prefer SDK methods)

| Endpoint                | Method | SDK equivalent                |
| ----------------------- | ------ | ----------------------------- |
| `/v2/live`              | POST   | `startSession()`              |
| `/v2/live`              | GET    | `list()`                      |
| `/v2/live/:id`          | GET    | `get(id)`                     |
| `/v2/live/:id`          | DELETE | `delete(id)`                  |
| `/v2/live/:id/file`     | GET    | `getFile(id)`                 |
| WebSocket URL from init | —      | `sendAudio()` / `session.on()` |

## Session Lifecycle

SDK flow: `startSession()` -> `sendAudio()` -> receive transcript events -> `stopRecording()` -> `get(id)` for final result.

## Quick Start

For SDK installation and client initialization, see the [gladia-sdk-integration skill](../gladia-sdk-integration/SKILL.md).

### JavaScript/TypeScript

```typescript
const session = client.liveV2().startSession({
  model: "solaria-1",
  encoding: "wav/pcm",
  sample_rate: 16000,
  bit_depth: 16,
  channels: 1,
  language_config: { languages: ["en"] },
  messages_config: { receive_partial_transcripts: true },
});

session.on("message", (msg) => {
  if (msg.type === "transcript") console.log(msg.data.utterance.text);
});
session.sendAudio(audioBuffer);
session.stopRecording();
```

### Python (sync)

```python
from gladiaio_sdk import (
    LiveV2InitRequest,
    LiveV2LanguageConfig,
    LiveV2MessagesConfig,
    LiveV2WebSocketMessage,
)

live_client = client.live()

session = live_client.start_session(
    LiveV2InitRequest(
        model="solaria-1",
        encoding="wav/pcm",
        sample_rate=16000,
        bit_depth=16,
        channels=1,
        language_config=LiveV2LanguageConfig(languages=["en"]),
        messages_config=LiveV2MessagesConfig(receive_partial_transcripts=True),
    )
)

@session.on("message")
def on_message(message: LiveV2WebSocketMessage):
    if message.type == "transcript":
        print(message.data.utterance.text.strip())

session.send_audio(audio_bytes)
session.stop_recording()
```

## Session Configuration

Core fields to set on every session:

- Audio format: `encoding`, `sample_rate`, `bit_depth`, `channels` (must exactly match the stream)
- Language: `language_config.languages` and optional `code_switching`
- Message behavior: `messages_config.receive_partial_transcripts` and speech events
- Optional processing: `pre_processing`, `realtime_processing`, `post_processing`

See [./references/session-config.md](./references/session-config.md) for full examples and [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md#configuration-options) for client retry/timeout settings.

## Key Tuning Parameters

`endpointing` is the primary latency-versus-completeness control for final transcripts.

| Use case         | Recommended value |
| ---------------- | ----------------- |
| Voice agent      | `0.05` - `0.1`    |
| Call center      | `0.1` - `0.3`     |
| Live subtitles   | `0.2` - `0.4`     |
| Meeting recorder | `0.3` - `0.5`     |

For `maximum_duration_without_endpointing`, `speech_threshold`, and full tuning guidance, see [./references/recommended-params.md](./references/recommended-params.md#endpointing-and-vad-tuning).

## Audio Streaming

Use `session.sendAudio(chunk)` (JS) / `session.send_audio(chunk)` (Python) to stream audio data. The SDK sends each chunk as a binary WebSocket frame.

- Chunk size: 100ms of audio per frame (recommended)
- Send continuously — do not batch large chunks
- Audio format MUST match the `encoding`, `sample_rate`, `bit_depth`, and `channels` in session config

## Stopping and Reconnection

### Normal stop

```typescript
session.stopRecording(); // Triggers post-processing, then session ends
```

```python
session.stop_recording()  # Triggers post-processing, then session ends
```

### Force end (skip post-processing)

```typescript
session.endSession(); // Immediately closes, no post-processing
```

```python
session.end_session()  # Immediately closes, no post-processing
```

### Reconnection

SDK reconnection is automatic (`wsRetry`). For raw WebSocket fallback, reconnect to the same URL.

## Limits

| Constraint           | Value                        |
| -------------------- | ---------------------------- |
| Max session duration | 3 hours                      |
| Supported encodings  | wav/pcm, wav/alaw, wav/ulaw  |
| Concurrency (paid)   | 30 concurrent sessions       |
| Concurrency (free)   | 1 concurrent session         |
| Billing              | Per-second of streamed audio |
| Multi-channel        | Billed as N x duration       |

## Managing Sessions

Use SDK methods for post-capture operations:

- JavaScript: `client.liveV2().get(id)`, `.list(filters)`, `.getFile(id)`, `.delete(id)`
- Python: `client.live().get(id)`, `.list(filters)`, `.get_file(id)`, `.delete(id)`

For full examples and pagination filters, see [./references/managing-sessions.md](./references/managing-sessions.md).

## Common Mistakes

- **Audio format mismatch**: the `encoding`, `sample_rate`, `bit_depth`, and `channels` in session config MUST match the actual audio stream exactly.
- **Forgetting to stop recording**: leaving a session open without `stopRecording()` keeps it hanging.
- **Wrong audio file path**: the audio download endpoint is `/v2/live/:id/file`, not `/v2/live/:id/audio`.

For the full list of gotchas and diagnostics, see the [gladia-troubleshooting skill](../gladia-troubleshooting/SKILL.md).

## Further Reading

- [Live quickstart](https://docs.gladia.io/chapters/live-stt/quickstart)
- [Partial transcripts](https://docs.gladia.io/chapters/live-stt/features/partial-transcripts)
- [Endpointing](https://docs.gladia.io/chapters/live-stt/features/endpointing)
- [API reference: init](https://docs.gladia.io/api-reference/v2/live/init)
