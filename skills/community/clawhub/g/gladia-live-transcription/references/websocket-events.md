# WebSocket Message Types

Complete reference for all WebSocket messages received during a live transcription session.

## Contents

- Message Format
- Lifecycle Events (start_session, start_recording, end_recording, end_session)
- Transcript Events (partial and final transcripts)
- Speech Events (speech_start, speech_end)
- Real-time Intelligence Events (translation, sentiment_analysis, named_entity_recognition)
- Post-Processing Events (post_transcript, post_final_transcript, post_summarization, post_chapterization)
- Acknowledgment Events (audio_chunk, stop_recording)
- SDK Event Mapping
- Error Messages

## Message Format

All messages are JSON with a `type` field:

```json
{
  "type": "transcript",
  "data": { ... }
}
```

## Lifecycle Events

### `start_session`

Sent when the session is initialized (HTTP init complete).

```json
{
  "type": "start_session",
  "data": {
    "id": "session-uuid"
  }
}
```

### `start_recording`

Sent when the WebSocket is connected and ready to receive audio.

```json
{
  "type": "start_recording",
  "data": {}
}
```

### `end_recording`

Sent after `stop_recording` is received and audio processing is finishing.

```json
{
  "type": "end_recording",
  "data": {}
}
```

### `end_session`

Final message before WebSocket closes.

```json
{
  "type": "end_session",
  "data": {}
}
```

## Transcript Events

### `transcript`

The primary message type. Contains partial or final transcripts.

```json
{
  "type": "transcript",
  "data": {
    "is_final": true,
    "utterance": {
      "text": "Hello, how can I help you today?",
      "language": "en",
      "start": 1.2,
      "end": 3.5,
      "words": [
        { "word": "Hello", "start": 1.2, "end": 1.5, "confidence": 0.98 },
        { "word": "how", "start": 1.6, "end": 1.7, "confidence": 0.97 }
      ]
    }
  }
}
```

- `is_final: false` — partial transcript (low-latency, may change)
- `is_final: true` — final transcript (stable, will not change)
- Partial transcripts require `messages_config.receive_partial_transcripts: true`

## Speech Events

### `speech_start`

Voice activity detected — someone started speaking.

```json
{
  "type": "speech_start",
  "data": {
    "time": 1.2
  }
}
```

### `speech_end`

Voice activity ended — silence detected after speech.

```json
{
  "type": "speech_end",
  "data": {
    "time": 3.5
  }
}
```

Requires `messages_config.receive_speech_events: true`.

## Real-time Intelligence Events

### `translation`

Real-time translation of transcripts (if enabled).

```json
{
  "type": "translation",
  "data": {
    "utterance": {
      "text": "Bonjour, comment puis-je vous aider aujourd'hui ?",
      "language": "fr",
      "start": 1.2,
      "end": 3.5
    },
    "source_language": "en"
  }
}
```

### `sentiment_analysis`

Per-utterance sentiment (if enabled).

```json
{
  "type": "sentiment_analysis",
  "data": {
    "utterance_index": 0,
    "sentiment": "positive",
    "sentiment_score": 0.82
  }
}
```

### `named_entity_recognition`

Entities detected in real-time (if enabled).

```json
{
  "type": "named_entity_recognition",
  "data": {
    "entities": [
      { "text": "John Smith", "type": "person", "start": 1.2, "end": 1.8 },
      { "text": "Acme Corp", "type": "organization", "start": 2.1, "end": 2.5 }
    ]
  }
}
```

## Post-Processing Events

These arrive after `stop_recording`, before `end_session`.

### `post_transcript`

Complete transcript assembled from all final utterances.

```json
{
  "type": "post_transcript",
  "data": {
    "transcription": {
      "full_transcript": "...",
      "utterances": [...]
    }
  }
}
```

### `post_final_transcript`

Final polished transcript after post-processing refinements.

```json
{
  "type": "post_final_transcript",
  "data": {
    "transcription": {
      "full_transcript": "...",
      "utterances": [...]
    }
  }
}
```

### `post_summarization`

Summary generated from the complete session (if enabled).

```json
{
  "type": "post_summarization",
  "data": {
    "results": "• Key point 1\n• Key point 2\n• Key point 3"
  }
}
```

### `post_chapterization`

Chapter segmentation of the session (if enabled).

```json
{
  "type": "post_chapterization",
  "data": {
    "results": [
      {
        "headline": "Introduction",
        "summary": "...",
        "start": 0.0,
        "end": 45.2
      },
      {
        "headline": "Main discussion",
        "summary": "...",
        "start": 45.2,
        "end": 180.0
      }
    ]
  }
}
```

## Acknowledgment Events

### `audio_chunk`

Acknowledgment that an audio chunk was received and queued.

```json
{
  "type": "audio_chunk",
  "data": {}
}
```

### `stop_recording`

Acknowledgment that the stop_recording command was received.

```json
{
  "type": "stop_recording",
  "data": {}
}
```

## SDK Event Mapping

The SDK provides a higher-level event API that maps to these WebSocket messages:

| SDK Event    | Fires When                                 |
| ------------ | ------------------------------------------ |
| `started`    | `start_session` received (HTTP init done)  |
| `connecting` | WebSocket reconnect attempt                |
| `connected`  | WebSocket open + `start_recording`         |
| `message`    | Any WebSocket message (all types above)    |
| `ending`     | `stop_recording` sent                      |
| `ended`      | `end_session` received, WebSocket closed   |
| `error`      | Connection error or error message received |

### Filtering messages in the SDK

```typescript
session.on("message", (msg) => {
  switch (msg.type) {
    case "transcript":
      if (msg.data.is_final) handleFinalTranscript(msg.data);
      break;
    case "translation":
      handleTranslation(msg.data);
      break;
    case "post_summarization":
      handleSummary(msg.data);
      break;
  }
});
```

## Error Messages

Errors can arrive as WebSocket messages or trigger the `error` event:

```json
{
  "type": "error",
  "data": {
    "code": "invalid_audio_format",
    "message": "Audio format does not match session configuration"
  }
}
```

Common error codes:

- `invalid_audio_format` — audio doesn't match configured encoding/sample_rate
- `session_timeout` — session exceeded max duration (3 hours)
- `rate_limit_exceeded` — too many concurrent sessions
- `internal_error` — server-side issue (retry with reconnection)
