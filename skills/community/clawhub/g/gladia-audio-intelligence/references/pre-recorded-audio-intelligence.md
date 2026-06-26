# Audio Intelligence Features (Pre-Recorded)

Detailed configuration reference for all audio intelligence features available on pre-recorded transcriptions.

## Contents

- Feature Availability (pre-recorded vs live matrix)
- Speaker Diarization
- Translation
- Sentiment and Emotion Analysis
- Named Entity Recognition (NER)
- Subtitles (SRT/VTT)
- Custom Vocabulary
- PII Redaction
- Chapterization
- Summarization
- Audio-to-LLM
- Custom Spelling
- Custom Metadata
- Combining Features
- Further Reading

## Feature Availability

| Feature                  | Pre-recorded | Live | Config Key                 |
| ------------------------ | :----------: | :--: | -------------------------- |
| Speaker diarization      |     Yes      |  No  | `diarization`              |
| Translation              |     Yes      | Yes  | `translation`              |
| Sentiment analysis       |     Yes      | Yes  | `sentiment_analysis`       |
| Named entity recognition |     Yes      | Yes  | `named_entity_recognition` |
| Subtitles (SRT/VTT)      |     Yes      |  No  | `subtitles`                |
| Custom vocabulary        |     Yes      | Yes  | `custom_vocabulary`        |
| PII redaction            |     Yes      |  No  | `pii_redaction`            |
| Chapterization           |     Yes      | Yes  | `chapterization`           |
| Summarization            |     Yes      | Yes  | `summarization`            |
| Audio-to-LLM             |     Yes      |  No  | `audio_to_llm`             |
| Custom spelling          |     Yes      | Yes  | `custom_spelling`          |
| Custom metadata          |     Yes      | Yes  | `custom_metadata`          |

## Speaker Diarization

Identifies who said what. Only available for pre-recorded.

```json
{
  "diarization": true,
  "diarization_config": {
    "number_of_speakers": 3,
    "min_speakers": 2,
    "max_speakers": 5
  }
}
```

- `number_of_speakers`: exact count if known (overrides min/max)
- `min_speakers` / `max_speakers`: range when exact count unknown
- Result: each utterance includes a `speaker` field (integer, 0-indexed)

## Translation

Translates the transcript to one or more target languages.

```json
{
  "translation": true,
  "translation_config": {
    "target_languages": ["fr", "es", "de"],
    "model": "base"
  }
}
```

- `target_languages`: array of ISO 639-1 codes
- Result: `result.translation.languages[].full_transcript` and per-utterance translations

## Sentiment and Emotion Analysis

Extracts sentiment polarity and emotions per utterance.

```json
{
  "sentiment_analysis": true
}
```

Result structure:

```json
{
  "sentiment_analysis": {
    "results": [
      {
        "utterance_index": 0,
        "sentiment": "positive",
        "sentiment_score": 0.85,
        "emotions": ["joy", "satisfaction"]
      }
    ]
  }
}
```

## Named Entity Recognition (NER)

Identifies and categorizes entities in the transcript.

```json
{
  "named_entity_recognition": true
}
```

Entity types: `person`, `organization`, `location`, `date`, `time`, `money`, `percentage`, `product`, `event`, `language`, `nationality`.

## Subtitles (SRT/VTT)

Generates subtitle files directly from the transcript.

```json
{
  "subtitles": true,
  "subtitles_config": {
    "formats": ["srt", "vtt"]
  }
}
```

Result: `result.subtitles.srt` and `result.subtitles.vtt` as strings.

## Custom Vocabulary

Improves recognition of domain-specific terms.

```json
{
  "custom_vocabulary": true,
  "custom_vocabulary_config": {
    "vocabulary": [
      { "value": "Gladia" },
      {
        "value": "Kubernetes",
        "pronunciations": ["koo-ber-net-eez"],
        "intensity": 0.5
      },
      { "value": "HIPAA", "language": "en", "intensity": 0.4 }
    ]
  }
}
```

- `value`: the target spelling
- `pronunciations`: optional array of phonetic hints
- `intensity`: 0.0-1.0, recommended 0.4-0.6 (higher causes false positives)
- `language`: ISO 639-1 code if specific to one language

## PII Redaction

Automatically detects and redacts personally identifiable information. Pre-recorded only.

```json
{
  "pii_redaction": true,
  "pii_redaction_config": {
    "policy": "mask",
    "entities": [
      "person",
      "location",
      "phone_number",
      "email",
      "credit_card",
      "date_of_birth"
    ]
  }
}
```

- `policy`: `mask` (replace with `[REDACTED]`) or `tag` (wrap with entity type markers)
- `entities`: which PII types to redact

## Chapterization

Segments audio into chapters with headlines and summaries.

```json
{
  "chapterization": true
}
```

Result:

```json
{
  "chapterization": {
    "results": [
      {
        "headline": "Project status update",
        "summary": "Team discussed progress on Q2 deliverables...",
        "start": 0.0,
        "end": 120.5
      }
    ]
  }
}
```

## Summarization

Generates concise summaries of the audio content.

```json
{
  "summarization": true,
  "summarization_config": {
    "type": "bullet_points"
  }
}
```

- `type`: `bullet_points` (default) or `paragraph`
- Result: `result.summarization.results` string

## Audio-to-LLM

Run custom LLM prompts against the transcript. Pre-recorded only.

```json
{
  "audio_to_llm": true,
  "audio_to_llm_config": {
    "prompts": [
      "Summarize the key action items",
      "Extract all mentioned deadlines",
      "What questions were left unanswered?"
    ]
  }
}
```

Result: `result.audio_to_llm.results[]` — one response per prompt.

## Custom Spelling

Normalize spelling variants to preferred forms (e.g., brand names).

```json
{
  "custom_spelling": true,
  "custom_spelling_config": {
    "spelling": [
      { "from": ["gladya", "gladia.io"], "to": "Gladia" },
      { "from": ["k8s", "kubernetes"], "to": "Kubernetes" }
    ]
  }
}
```

## Custom Metadata

Attach arbitrary metadata to a job for filtering and retrieval.

```json
{
  "custom_metadata": {
    "customer_id": "cust-123",
    "project": "onboarding-calls",
    "batch": "2026-05"
  }
}
```

Metadata is stored with the job and returned in list/get responses. Use for organizing and filtering transcriptions.

## Combining Features

All features can be enabled simultaneously. Enable only what you need to minimize latency and cost:

```json
{
  "language_config": { "languages": ["en"], "code_switching": false },
  "diarization": true,
  "diarization_config": { "number_of_speakers": 2 },
  "translation": true,
  "translation_config": { "target_languages": ["fr"] },
  "summarization": true,
  "summarization_config": { "type": "bullet_points" },
  "sentiment_analysis": true,
  "subtitles": true,
  "subtitles_config": { "formats": ["srt"] }
}
```

## Further Reading

- [Audio-to-LLM](https://docs.gladia.io/chapters/audio-intelligence/audio-to-llm)
- [Speaker Diarization](https://docs.gladia.io/chapters/audio-intelligence/speaker-diarization)
- [PII Redaction](https://docs.gladia.io/chapters/audio-intelligence/pii-redaction)
- [Translation](https://docs.gladia.io/chapters/audio-intelligence/translation)
- [Custom Vocabulary](https://docs.gladia.io/chapters/audio-intelligence/custom-vocabulary)
- [Summarization](https://docs.gladia.io/chapters/audio-intelligence/summarization)
- [Chapterization](https://docs.gladia.io/chapters/audio-intelligence/chapterization)
- [Sentiment Analysis](https://docs.gladia.io/chapters/audio-intelligence/sentiment-analysis)
- [NER](https://docs.gladia.io/chapters/audio-intelligence/named-entity-recognition)
- [Subtitles](https://docs.gladia.io/chapters/audio-intelligence/subtitles)
