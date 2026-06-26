# Transcription Options Reference

Complete configuration reference for all pre-recorded transcription options passed as the second argument to `transcribe()`.

## Contents

- Language Configuration
- Audio Intelligence Options (full example)
- Delivery (callbacks)

For client-level config (retry, timeouts, HTTP headers), see [gladia-sdk-integration](../../gladia-sdk-integration/SKILL.md#configuration-options). For detailed audio intelligence feature docs, see [gladia-audio-intelligence](../../gladia-audio-intelligence/SKILL.md).

## Full Options Example (JavaScript/TypeScript)

```typescript
const result = await client.preRecorded().transcribe(audioInput, {
  // Language
  language_config: {
    languages: ["en", "fr"], // Expected languages (ISO 639-1)
    code_switching: true, // Detect language changes mid-speech
  },

  // Audio Intelligence
  diarization: true, // Speaker identification
  diarization_config: { number_of_speakers: 3 },
  translation: true,
  translation_config: { target_languages: ["fr", "es"] },
  summarization: true,
  summarization_config: { type: "bullet_points" },
  sentiment_analysis: true,
  named_entity_recognition: true,
  chapterization: true,
  subtitles: true,
  subtitles_config: { formats: ["srt", "vtt"] },
  pii_redaction: true,
  pii_redaction_config: {
    policy: "mask",
    entities: ["person", "location", "phone_number"],
  },
  audio_to_llm: true,
  audio_to_llm_config: { prompts: ["Summarize the key decisions made"] },
  custom_vocabulary: true,
  custom_vocabulary_config: {
    vocabulary: [
      { value: "Gladia", intensity: 0.5 },
      { value: "Kubernetes", pronunciations: ["koo-ber-net-eez"] },
    ],
  },

  // Delivery
  callback_url: "https://your-server.com/webhook",
});
```

## Full Options Example (Python)

```python
result = client.prerecorded().transcribe("audio.mp3", {
    "language_config": {"languages": ["en", "fr"], "code_switching": True},
    "diarization": True,
    "diarization_config": {"number_of_speakers": 3},
    "translation": True,
    "translation_config": {"target_languages": ["fr", "es"]},
    "summarization": True,
    "summarization_config": {"type": "bullet_points"},
    "sentiment_analysis": True,
    "named_entity_recognition": True,
    "chapterization": True,
    "subtitles": True,
    "subtitles_config": {"formats": ["srt", "vtt"]},
    "pii_redaction": True,
    "pii_redaction_config": {"policy": "mask", "entities": ["person", "location", "phone_number"]},
    "audio_to_llm": True,
    "audio_to_llm_config": {"prompts": ["Summarize the key decisions made"]},
    "custom_vocabulary": True,
    "custom_vocabulary_config": {
        "vocabulary": [
            {"value": "Gladia", "intensity": 0.5},
            {"value": "Kubernetes", "pronunciations": ["koo-ber-net-eez"]},
        ],
    },
    "callback_url": "https://your-server.com/webhook",
})
```

## Options Quick Reference

| Option                                  | Type       | Description                             |
| --------------------------------------- | ---------- | --------------------------------------- |
| `language_config.languages`             | `string[]` | Expected languages (ISO 639-1)          |
| `language_config.code_switching`        | `bool`     | Detect language changes mid-speech      |
| `diarization`                           | `bool`     | Speaker identification                  |
| `diarization_config.number_of_speakers` | `int`      | Exact speaker count (overrides min/max) |
| `translation`                           | `bool`     | Translate transcript                    |
| `translation_config.target_languages`   | `string[]` | Target language codes                   |
| `summarization`                         | `bool`     | Generate summary                        |
| `summarization_config.type`             | `string`   | `bullet_points` or `paragraph`          |
| `sentiment_analysis`                    | `bool`     | Per-utterance sentiment                 |
| `named_entity_recognition`              | `bool`     | Entity extraction                       |
| `chapterization`                        | `bool`     | Chapter segmentation                    |
| `subtitles`                             | `bool`     | Generate subtitle files                 |
| `subtitles_config.formats`              | `string[]` | `srt`, `vtt`                            |
| `pii_redaction`                         | `bool`     | Redact PII                              |
| `pii_redaction_config.policy`           | `string`   | `mask` or `tag`                         |
| `audio_to_llm`                          | `bool`     | Run LLM prompts on transcript           |
| `custom_vocabulary`                     | `bool`     | Domain-specific terms                   |
| `callback_url`                          | `string`   | Webhook URL for async delivery          |
