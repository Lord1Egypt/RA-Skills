---
name: gladia-audio-intelligence
description: "Configure and use Gladia audio intelligence features: speaker diarization, translation, sentiment analysis, named entity recognition (NER), PII redaction, subtitles (SRT/VTT), summarization, chapterization, custom vocabulary, and audio-to-LLM. Use when the user asks about any audio intelligence feature, enabling features on pre-recorded or live transcription, understanding which features are available in each mode, or combining multiple features. Always prefer the official SDK; fall back to raw REST only when SDK cannot satisfy the requirement."
license: MIT
---

# Audio Intelligence

Gladia's audio intelligence features extract structured data and insights from transcripts. They work on top of the base transcription — most are enabled by adding options to the `transcribe()` call (pre-recorded) or the `startSession()` config (live).

> **SDK-first**: always use the official SDK — see [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md) for policy, setup, and fallback criteria.

## When to Use

- User asks about a specific feature: diarization, translation, PII redaction, sentiment, NER, subtitles, summarization, etc.
- Enabling or configuring one or more audio intelligence features on pre-recorded or live transcription
- Understanding which features are available in live vs pre-recorded mode
- Combining multiple features in a single transcription job

**When NOT to use:** For basic transcription without audio intelligence features, go directly to [gladia-pre-recorded-transcription](../gladia-pre-recorded-transcription/SKILL.md) or [gladia-live-transcription](../gladia-live-transcription/SKILL.md). For gotchas and errors related to specific features, see [gladia-troubleshooting](../gladia-troubleshooting/SKILL.md).

## References

Consult these resources as needed:

- ./references/live-audio-intelligence.md -- Detailed config and WebSocket responses for all live-mode features
- ./references/pre-recorded-audio-intelligence.md -- Detailed config and response structures for all pre-recorded audio intelligence features
- ../gladia-pre-recorded-transcription/SKILL.md -- Pre-recorded transcription workflow and options
- ../gladia-live-transcription/SKILL.md -- Live transcription session config and event handling
- ../gladia-sdk-integration/SKILL.md -- SDK setup, client initialization, and SDK vs raw API decision guide
- ../gladia-troubleshooting/SKILL.md -- Common errors, gotchas, and verification checklist

## Feature Availability

| Feature                  | Pre-recorded | Live | Config key                      |
| ------------------------ | :----------: | :--: | ------------------------------- |
| Speaker diarization      |     Yes      |  No  | `diarization`                   |
| Translation              |     Yes      | Yes  | `translation`                   |
| Sentiment analysis       |     Yes      | Yes  | `sentiment_analysis`            |
| Named entity recognition |     Yes      | Yes  | `named_entity_recognition`      |
| Subtitles (SRT/VTT)      |     Yes      |  No  | `subtitles`                     |
| Custom vocabulary        |     Yes      | Yes  | `custom_vocabulary`             |
| PII redaction            |     Yes      |  No  | `pii_redaction`                 |
| Chapterization           |     Yes      | Yes  | `chapterization` (post-process) |
| Summarization            |     Yes      | Yes  | `summarization` (post-process)  |
| Audio-to-LLM             |     Yes      |  No  | `audio_to_llm`                  |
| Custom spelling          |     Yes      | Yes  | `custom_spelling`               |
| Custom metadata          |     Yes      | Yes  | `custom_metadata`               |

Live features split into two groups: **real-time** (results stream during the session) and **post-processing** (results arrive after `stopRecording()`). See [./references/live-audio-intelligence.md](./references/live-audio-intelligence.md) for details.

## Quick Config Examples

Code examples assume `GladiaClient` is already initialized — see [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md) for setup.

### Speaker Diarization (pre-recorded only)

```typescript
const result = await client.preRecorded().transcribe("audio.mp3", {
  diarization: true,
  diarization_config: { number_of_speakers: 2 },
});
// Each utterance includes a `speaker` field (0-indexed integer)
```

```python
result = client.prerecorded().transcribe("audio.mp3", {
    "diarization": True,
    "diarization_config": {"number_of_speakers": 2},
})
```

### Translation (pre-recorded and live)

**Pre-recorded:**

```typescript
const result = await client.preRecorded().transcribe("audio.mp3", {
  translation: true,
  translation_config: { target_languages: ["fr", "es"] },
});
```

```python
result = client.prerecorded().transcribe("audio.mp3", {
    "translation": True,
    "translation_config": {"target_languages": ["fr", "es"]},
})
```

**Live** (result streams as `translation` WebSocket events — see [live-audio-intelligence.md](./references/live-audio-intelligence.md)):

```typescript
const session = client.liveV2().startSession({
  // ... audio format options ...
  realtime_processing: {
    translation: true,
    translation_config: { target_languages: ["fr"] },
  },
});
```

```python
from gladiaio_sdk import LiveV2InitRequest, LiveV2RealtimeProcessing

session = client.live().start_session(
    LiveV2InitRequest(
        # ... audio format options ...
        realtime_processing=LiveV2RealtimeProcessing(
            translation=True,
            translation_config={"target_languages": ["fr"]},
        ),
    )
)
```

### Summarization (pre-recorded and live)

**Pre-recorded:**

```typescript
const result = await client.preRecorded().transcribe("audio.mp3", {
  summarization: true,
  summarization_config: { type: "bullet_points" },
});
```

**Live** (arrives after `stopRecording()` as `post_summarization` event):

```typescript
const session = client.liveV2().startSession({
  // ... audio format options ...
  post_processing: {
    summarization: true,
    summarization_config: { type: "bullet_points" },
  },
});
session.on("message", (msg) => {
  if (msg.type === "post_summarization") console.log(msg.data.results);
});
```

For full per-feature config options and response structures, see:

- Pre-recorded: [./references/pre-recorded-audio-intelligence.md](./references/pre-recorded-audio-intelligence.md)
- Live: [./references/live-audio-intelligence.md](./references/live-audio-intelligence.md)

## Common Mistakes

- **`code_switching: true` with empty `languages`**: triggers evaluation across 100+ languages and causes frequent misdetections. Always provide 3-5 expected languages.
- **Custom vocabulary `intensity` above 0.6**: values over 0.6 cause false positives where unrelated words get replaced. Keep at 0.4-0.6 and use `pronunciations` for better results.
- **Expecting diarization, PII redaction, subtitles, or audio-to-LLM in live mode**: these four features are pre-recorded only.
- **Enabling many features simultaneously without considering cost/latency**: each enabled feature adds processing time. Enable only what you need; combine `diarization + summarization + translation` only when all are required.

For the full gotcha list, see [gladia-troubleshooting](../gladia-troubleshooting/SKILL.md).

## Further Reading

- [Audio intelligence overview](https://docs.gladia.io/chapters/pre-recorded-stt/audio-intelligence)
- [Speaker diarization](https://docs.gladia.io/chapters/audio-intelligence/speaker-diarization)
- [Translation](https://docs.gladia.io/chapters/audio-intelligence/translation)
- [Sentiment analysis](https://docs.gladia.io/chapters/audio-intelligence/sentiment-analysis)
- [Named entity recognition](https://docs.gladia.io/chapters/audio-intelligence/named-entity-recognition)
- [PII redaction](https://docs.gladia.io/chapters/audio-intelligence/pii-redaction)
- [Custom vocabulary](https://docs.gladia.io/chapters/audio-intelligence/custom-vocabulary)
- [Summarization](https://docs.gladia.io/chapters/audio-intelligence/summarization)
- [Chapterization](https://docs.gladia.io/chapters/audio-intelligence/chapterization)
- [Audio-to-LLM](https://docs.gladia.io/chapters/audio-intelligence/audio-to-llm)
- [Live audio intelligence](https://docs.gladia.io/chapters/live-stt/audio-intelligence)
