# Recommended Parameters by Use Case

Best parameter configurations for real-time transcription depending on your application type.

## Contents

- Endpointing and VAD Tuning
- Voice Agents (low latency, fast turn detection)
- Meeting Recorders (accuracy, post-processing)
- Call Centers (telephony audio, analytics)
- Live Subtitles / Captions (display-ready text)
- Multi-Language Conversations (code switching)
- Region Selection (eu-west, us-west)

## Endpointing and VAD Tuning

### `endpointing` (seconds)

How long a silence must last before Gladia closes the current utterance and emits a final transcript.

- **Default:** `0.05` — **Range:** `0.01` to `10`

This is the core latency-versus-accuracy tradeoff in live transcription. Lower values produce faster final segments but can split utterances at short pauses. Higher values produce cleaner segments but add latency.

| Use case         | Recommended value | Why                                    |
| ---------------- | ----------------- | -------------------------------------- |
| Voice agent      | `0.05` - `0.1`    | Fast turn detection                    |
| Call center      | `0.1` - `0.3`     | Snappy but tolerates telephony gaps    |
| Live subtitles   | `0.2` - `0.4`     | Readable chunks without too much delay |
| Meeting recorder | `0.3` - `0.5`     | Complete sentences before closing      |

### `maximum_duration_without_endpointing` (seconds)

Hard cap on utterance length when no silence is detected.

- **Default:** `5` — **Range:** `5` to `60`

Use lower values for voice agents (fast turn taking) and higher values for long-form capture (meetings and webinars).

### `speech_threshold` (0.0 - 1.0)

Located in `pre_processing.speech_threshold`. Controls how confident VAD must be before opening an utterance.

- **Default:** `0.5` — **Range:** `0.0` to `1.0`
- Low value (for example `0.3`) increases sensitivity and may trigger on noise
- High value (for example `0.7`) is more conservative and may miss faint speech

Raise `speech_threshold` in noisy environments and lower it only for quiet, low-volume speakers.

## Voice Agents

Optimized for low latency and fast turn detection.

```json
{
  "model": "solaria-1",
  "encoding": "wav/pcm",
  "sample_rate": 16000,
  "bit_depth": 16,
  "channels": 1,
  "language_config": {
    "languages": ["en"]
  },
  "pre_processing": {
    "audio_enhancer": true,
    "speech_threshold": 0.6
  },
  "messages_config": {
    "receive_partial_transcripts": true,
    "receive_speech_events": true
  }
}
```

Key points:

- Enable `receive_partial_transcripts` for lowest latency
- Use `receive_speech_events` to detect turn boundaries
- Higher `speech_threshold` (0.6) reduces false triggers from background noise
- Single language for fastest processing
- Audio enhancer helps with telephony/VoIP audio quality

## Meeting Recorders

Optimized for accuracy and post-processing features.

```json
{
  "model": "solaria-1",
  "encoding": "wav/pcm",
  "sample_rate": 48000,
  "bit_depth": 16,
  "channels": 1,
  "language_config": {
    "languages": ["en", "fr"],
    "code_switching": true
  },
  "messages_config": {
    "receive_partial_transcripts": false
  },
  "post_processing": {
    "summarization": true,
    "summarization_config": { "type": "bullet_points" },
    "chapterization": true
  }
}
```

Key points:

- Higher sample rate (48000) for better accuracy
- Code switching if participants speak multiple languages
- Disable partial transcripts if you only need final results
- Enable post-processing for automatic meeting notes
- Consider multi-channel if each participant is on a separate audio track

## Call Centers

Optimized for telephony audio with analytics.

```json
{
  "model": "solaria-1",
  "encoding": "wav/ulaw",
  "sample_rate": 8000,
  "bit_depth": 8,
  "channels": 1,
  "language_config": {
    "languages": ["en"]
  },
  "pre_processing": {
    "audio_enhancer": true
  },
  "realtime_processing": {
    "sentiment_analysis": true,
    "named_entity_recognition": true
  },
  "messages_config": {
    "receive_partial_transcripts": true
  },
  "post_processing": {
    "summarization": true
  }
}
```

Key points:

- Use `wav/ulaw` or `wav/alaw` encoding for telephony (matches PBX output)
- 8000 Hz sample rate is standard for phone audio
- Audio enhancer compensates for telephony compression
- Real-time sentiment helps detect escalation
- NER extracts customer details (names, account numbers)
- Post-processing summarization for call notes

## Live Subtitles / Captions

Optimized for display-ready text with minimal delay.

```json
{
  "model": "solaria-1",
  "encoding": "wav/pcm",
  "sample_rate": 44100,
  "bit_depth": 16,
  "channels": 1,
  "language_config": {
    "languages": ["en"]
  },
  "realtime_processing": {
    "translation": true,
    "translation_config": { "target_languages": ["fr", "es"] }
  },
  "messages_config": {
    "receive_partial_transcripts": true
  }
}
```

Key points:

- Partial transcripts provide immediate visual feedback
- Translation enables multi-language subtitle streams
- High sample rate from broadcast/streaming sources
- Consider the endpointing configuration for natural subtitle breaks

## Multi-Language Conversations

For conversations where speakers switch between languages.

```json
{
  "model": "solaria-1",
  "encoding": "wav/pcm",
  "sample_rate": 16000,
  "bit_depth": 16,
  "channels": 1,
  "language_config": {
    "languages": ["en", "fr", "es"],
    "code_switching": true
  },
  "realtime_processing": {
    "custom_vocabulary": true,
    "custom_vocabulary_config": {
      "vocabulary": [{ "value": "company-specific-term", "language": "en" }]
    }
  },
  "messages_config": {
    "receive_partial_transcripts": true
  }
}
```

Key points:

- ALWAYS provide 3-5 expected languages when enabling code switching
- Never leave `languages` empty with `code_switching: true` (causes misdetection)
- Per-language custom vocabulary entries improve recognition
- Each utterance in the response includes a `language` field

## Region Selection

Gladia offers two regions for live transcription:

| Region  | Value     | Best for                                     |
| ------- | --------- | -------------------------------------------- |
| EU West | `eu-west` | European users, GDPR compliance              |
| US West | `us-west` | North American users, lowest latency from US |

Set via `GLADIA_REGION` environment variable or client config:

```typescript
const client = new GladiaClient({ apiKey: "...", region: "eu-west" });
```
