# Audio Intelligence — Live Mode

Detailed configuration reference for audio intelligence features available in live transcription sessions.

## Contents

- Feature Groups (real-time vs post-processing)
- Real-Time Processing Features
  - Translation
  - Sentiment Analysis
  - Named Entity Recognition (NER)
  - Custom Vocabulary
  - Custom Spelling
- Post-Processing Features (after stopRecording)
  - Summarization
  - Chapterization
  - Custom Metadata
- Combining Features
- WebSocket Message Reference
- Features NOT Available in Live Mode

## Feature Groups

Live audio intelligence features split into two groups:

| Group               | When results arrive                                  | Config key            |
| ------------------- | ---------------------------------------------------- | --------------------- |
| **Real-time**       | Stream during the session, alongside transcripts     | `realtime_processing` |
| **Post-processing** | Arrive after `stopRecording()`, before `end_session` | `post_processing`     |

## Real-Time Processing Features

Configure via `realtime_processing` in `startSession()` / `start_session()`.

### Translation

Translates each utterance as it is transcribed. Results arrive as `translation` WebSocket events.

```typescript
const session = client.liveV2().startSession({
  model: "solaria-1",
  encoding: "wav/pcm",
  sample_rate: 16000,
  bit_depth: 16,
  channels: 1,
  realtime_processing: {
    translation: true,
    translation_config: { target_languages: ["fr", "es"] },
  },
});

session.on("message", (msg) => {
  if (msg.type === "translation") {
    console.log(`[${msg.data.utterance.language}] ${msg.data.utterance.text}`);
  }
});
```

```python
from gladiaio_sdk import LiveV2InitRequest, LiveV2RealtimeProcessing, LiveV2WebSocketMessage

session = client.live().start_session(
    LiveV2InitRequest(
        model="solaria-1",
        encoding="wav/pcm",
        sample_rate=16000,
        bit_depth=16,
        channels=1,
        realtime_processing=LiveV2RealtimeProcessing(
            translation=True,
            translation_config={"target_languages": ["fr", "es"]},
        ),
    )
)

@session.on("message")
def on_message(msg: LiveV2WebSocketMessage):
    if msg.type == "translation":
        print(f"[{msg.data.utterance.language}] {msg.data.utterance.text}")
```

WebSocket event:

```json
{
  "type": "translation",
  "data": {
    "utterance": {
      "text": "Bonjour",
      "language": "fr",
      "start": 1.2,
      "end": 1.8
    },
    "source_language": "en"
  }
}
```

### Sentiment Analysis

Per-utterance sentiment polarity. Results arrive as `sentiment_analysis` WebSocket events.

```typescript
const session = client.liveV2().startSession({
  // ... audio format ...
  realtime_processing: { sentiment_analysis: true },
});

session.on("message", (msg) => {
  if (msg.type === "sentiment_analysis") {
    console.log(
      `Sentiment: ${msg.data.sentiment} (${msg.data.sentiment_score})`,
    );
  }
});
```

```python
session = client.live().start_session(
    LiveV2InitRequest(
        # ... audio format ...
        realtime_processing=LiveV2RealtimeProcessing(sentiment_analysis=True),
    )
)

@session.on("message")
def on_message(msg: LiveV2WebSocketMessage):
    if msg.type == "sentiment_analysis":
        print(f"Sentiment: {msg.data.sentiment} ({msg.data.sentiment_score})")
```

WebSocket event:

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

### Named Entity Recognition (NER)

Detects entities (persons, organizations, locations, etc.) in real time.

```typescript
const session = client.liveV2().startSession({
  // ... audio format ...
  realtime_processing: { named_entity_recognition: true },
});

session.on("message", (msg) => {
  if (msg.type === "named_entity_recognition") {
    msg.data.entities.forEach((e) => console.log(`${e.type}: ${e.text}`));
  }
});
```

```python
session = client.live().start_session(
    LiveV2InitRequest(
        # ... audio format ...
        realtime_processing=LiveV2RealtimeProcessing(named_entity_recognition=True),
    )
)
```

WebSocket event:

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

Entity types: `person`, `organization`, `location`, `date`, `time`, `money`, `percentage`, `product`, `event`, `language`, `nationality`.

### Custom Vocabulary

Improves recognition of domain-specific terms in real time.

```typescript
const session = client.liveV2().startSession({
  // ... audio format ...
  realtime_processing: {
    custom_vocabulary: true,
    custom_vocabulary_config: {
      vocabulary: [
        { value: "Gladia", intensity: 0.5 },
        {
          value: "Kubernetes",
          pronunciations: ["koo-ber-net-eez"],
          intensity: 0.5,
        },
      ],
    },
  },
});
```

```python
session = client.live().start_session(
    LiveV2InitRequest(
        # ... audio format ...
        realtime_processing=LiveV2RealtimeProcessing(
            custom_vocabulary=True,
            custom_vocabulary_config={
                "vocabulary": [
                    {"value": "Gladia", "intensity": 0.5},
                    {"value": "Kubernetes", "pronunciations": ["koo-ber-net-eez"], "intensity": 0.5},
                ]
            },
        ),
    )
)
```

Keep `intensity` at 0.4-0.6. Values above 0.6 cause false positives. See [gladia-troubleshooting](../../gladia-troubleshooting/SKILL.md) for the intensity gotcha.

### Custom Spelling

Normalizes spelling variants to a preferred form.

```typescript
const session = client.liveV2().startSession({
  // ... audio format ...
  realtime_processing: {
    custom_spelling: true,
    custom_spelling_config: {
      spelling: [{ from: ["gladya", "gladia.io"], to: "Gladia" }],
    },
  },
});
```

---

## Post-Processing Features

Configure via `post_processing` in `startSession()`. Results arrive after `stopRecording()` as WebSocket events, before `end_session`.

### Summarization

Generates a summary of the entire session.

```typescript
const session = client.liveV2().startSession({
  // ... audio format ...
  post_processing: {
    summarization: true,
    summarization_config: { type: "bullet_points" }, // or "paragraph"
  },
});

session.on("message", (msg) => {
  if (msg.type === "post_summarization") console.log(msg.data.results);
});
```

```python
from gladiaio_sdk import LiveV2InitRequest, LiveV2PostProcessing

session = client.live().start_session(
    LiveV2InitRequest(
        # ... audio format ...
        post_processing=LiveV2PostProcessing(
            summarization=True,
            summarization_config={"type": "bullet_points"},
        ),
    )
)
```

WebSocket event:

```json
{
  "type": "post_summarization",
  "data": { "results": "• Key point 1\n• Key point 2" }
}
```

### Chapterization

Segments the session into chapters with headlines and summaries.

```typescript
const session = client.liveV2().startSession({
  // ... audio format ...
  post_processing: { chapterization: true },
});

session.on("message", (msg) => {
  if (msg.type === "post_chapterization") console.log(msg.data.results);
});
```

```python
session = client.live().start_session(
    LiveV2InitRequest(
        # ... audio format ...
        post_processing=LiveV2PostProcessing(chapterization=True),
    )
)
```

WebSocket event:

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
      }
    ]
  }
}
```

### Custom Metadata

Attach arbitrary key-value metadata to the session for filtering and retrieval.

```typescript
const session = client.liveV2().startSession({
  // ... audio format ...
  custom_metadata: { call_id: "call-123", agent: "support-bot" },
});
```

---

## Combining Features

Real-time and post-processing features can be combined freely:

```typescript
const session = client.liveV2().startSession({
  model: "solaria-1",
  encoding: "wav/pcm",
  sample_rate: 16000,
  bit_depth: 16,
  channels: 1,
  realtime_processing: {
    translation: true,
    translation_config: { target_languages: ["fr"] },
    sentiment_analysis: true,
    named_entity_recognition: true,
  },
  post_processing: {
    summarization: true,
    summarization_config: { type: "bullet_points" },
    chapterization: true,
  },
});
```

Enable only what you need — each feature adds processing overhead.

---

## WebSocket Message Reference

For the full list of all WebSocket message types (including lifecycle events and acknowledgments), see [../../gladia-live-transcription/references/websocket-events.md](../../gladia-live-transcription/references/websocket-events.md).

Intelligence-related message types:

| Message type               | Group        | Trigger                                        |
| -------------------------- | ------------ | ---------------------------------------------- |
| `translation`              | Real-time    | `realtime_processing.translation`              |
| `sentiment_analysis`       | Real-time    | `realtime_processing.sentiment_analysis`       |
| `named_entity_recognition` | Real-time    | `realtime_processing.named_entity_recognition` |
| `post_summarization`       | Post-process | `post_processing.summarization`                |
| `post_chapterization`      | Post-process | `post_processing.chapterization`               |

---

## Features NOT Available in Live Mode

These features are pre-recorded only and are silently ignored if configured in a live session:

| Feature             | Pre-recorded alternative                                            |
| ------------------- | ------------------------------------------------------------------- |
| Speaker diarization | Use multi-channel audio (one speaker per channel)                   |
| PII redaction       | Implement client-side redaction on transcript text                  |
| Subtitles (SRT/VTT) | Generate from the final transcript after session ends               |
| Audio-to-LLM        | Use `GET /v2/live/:id` after session ends, then call LLM separately |

For full pre-recorded feature config, see [./pre-recorded-audio-intelligence.md](./pre-recorded-audio-intelligence.md).
