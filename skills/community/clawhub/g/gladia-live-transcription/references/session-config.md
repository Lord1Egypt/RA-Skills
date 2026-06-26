# Session Configuration Reference

Complete configuration reference for options passed to `startSession()` (JS) / `start_session()` (Python).

## Contents

- JavaScript/TypeScript Full Configuration Example
- Python Typed Request Example
- Related References

## JavaScript/TypeScript Full Configuration Example

```typescript
const session = client.liveV2().startSession({
  // Model
  model: "solaria-1",

  // Audio format (MUST match your audio stream exactly)
  encoding: "wav/pcm", // wav/pcm | wav/alaw | wav/ulaw
  sample_rate: 16000, // Hz (8000, 16000, 44100, 48000)
  bit_depth: 16, // 8 or 16
  channels: 1, // 1 (mono) or 2 (stereo; billed as 2x duration)

  // Language
  language_config: {
    languages: ["en"], // 1-5 expected languages
    code_switching: false, // Detect language changes mid-speech
  },

  // Pre-processing
  pre_processing: {
    audio_enhancer: true, // Noise reduction
    speech_threshold: 0.5, // VAD threshold (0.0-1.0)
  },

  // Real-time features
  realtime_processing: {
    custom_vocabulary: true,
    custom_vocabulary_config: { vocabulary: [...] },
    translation: true,
    translation_config: { target_languages: ["fr"] },
    named_entity_recognition: true,
    sentiment_analysis: true,
  },

  // Post-processing (runs after stop_recording)
  post_processing: {
    summarization: true,
    summarization_config: { type: "bullet_points" },
    chapterization: true,
  },

  // Message filtering
  messages_config: {
    receive_partial_transcripts: true, // Low-latency partial results
    receive_speech_events: true, // speech_start / speech_end
    receive_pre_processing_events: false,
  },

  // Callbacks
  callback_url: "https://your-server.com/live-events",
});
```

## Python Typed Request Example

```python
from gladiaio_sdk import (
    LiveV2InitRequest,
    LiveV2LanguageConfig,
    LiveV2MessagesConfig,
    LiveV2PreProcessing,
    LiveV2RealtimeProcessing,
    LiveV2PostProcessing,
)

session = live_client.start_session(
    LiveV2InitRequest(
        model="solaria-1",
        encoding="wav/pcm",
        sample_rate=16000,
        bit_depth=16,
        channels=1,
        language_config=LiveV2LanguageConfig(languages=["en"], code_switching=False),
        pre_processing=LiveV2PreProcessing(audio_enhancer=True, speech_threshold=0.5),
        realtime_processing=LiveV2RealtimeProcessing(
            custom_vocabulary=True,
            translation=True,
            sentiment_analysis=True,
        ),
        post_processing=LiveV2PostProcessing(summarization=True, chapterization=True),
        messages_config=LiveV2MessagesConfig(
            receive_partial_transcripts=True,
            receive_speech_events=True,
        ),
    )
)
```

## Related References

- For client-level settings (retry, timeouts, WebSocket behavior), see [gladia-sdk-integration](../../gladia-sdk-integration/SKILL.md#configuration-options).
- For complete live audio intelligence config behavior, see [live-audio-intelligence](../../gladia-audio-intelligence/references/live-audio-intelligence.md).
