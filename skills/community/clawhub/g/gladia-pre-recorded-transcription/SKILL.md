---
name: gladia-pre-recorded-transcription
description: Transcribe pre-recorded audio files or URLs with Gladia. Use when the user needs batch/async transcription, speaker diarization, subtitles (SRT/VTT), PII redaction, translation, NER, summarization, chapterization, audio-to-LLM, or any audio intelligence on pre-recorded content. Always prefer the official SDK; fall back to raw REST only when SDK cannot satisfy the requirement.
license: MIT
---

# Pre-Recorded Transcription

Gladia's pre-recorded API transcribes audio and video files asynchronously.

> **SDK-first**: always use the official SDK — see [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md) for policy, setup, and fallback criteria.

## When to Use

- Existing audio/video files or URLs (including social/video links)
- Batch or asynchronous transcription workflows
- Pre-recorded-only features: diarization, PII redaction, subtitles

**When NOT to use:** If the user needs real-time / live transcription of a stream, microphone, or ongoing audio feed, use the [gladia-live-transcription skill](../gladia-live-transcription/SKILL.md) instead. Live transcription uses WebSocket sessions, not the pre-recorded API.

## References

Consult these resources as needed:

- ./references/transcription-options.md -- Full options (JS + Python)
- ./references/managing-jobs.md -- `get`, `list`, `getFile`, `delete`
- ./references/delivery-and-response.md -- Response shape and events
- ../gladia-audio-intelligence/SKILL.md -- Feature availability and config
- ../gladia-sdk-integration/SKILL.md -- Setup, config, SDK vs raw API
- ../gladia-sdk-integration/references/sdk-versions.md -- Current SDK versions
- ../gladia-troubleshooting/SKILL.md -- Errors and diagnostics

## API Endpoints (reference — prefer SDK methods instead)

| Endpoint                    | Method | SDK equivalent                          |
| --------------------------- | ------ | --------------------------------------- |
| `/v2/upload`                | POST   | `transcribe()` auto-uploads local files |
| `/v2/pre-recorded`          | POST   | `create()` / `transcribe()`             |
| `/v2/pre-recorded`          | GET    | `list()`                                |
| `/v2/pre-recorded/:id`      | GET    | `get()` / `poll()` / `transcribe()`     |
| `/v2/pre-recorded/:id`      | DELETE | `delete()`                              |
| `/v2/pre-recorded/:id/file` | GET    | `getFile()`                             |

## Workflow

### Recommended (SDK)

The SDK `transcribe()` method handles upload, job creation, and polling in one call. Use this by default.

```typescript
const result = await client.preRecorded().transcribe("./audio.mp3", {
  language_config: { languages: ["en"] },
  diarization: true,
});

console.log(result.result?.transcription?.full_transcript);
```

```python
result = client.prerecorded().transcribe(
    "audio.mp3",
    {"language_config": {"languages": ["en"]}, "diarization": True},
)

print(result.result.transcription.full_transcript)
```

Audio input can be a local file path, HTTP(S) URL, social/video URL, or binary file object. For full input types, see [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md#audio-input-types).

### Fallback (raw REST — only when SDK is not feasible)

Use raw REST only when SDK use is not possible.

1. **Upload** (if local file): `POST /v2/upload` with multipart form data → get `audio_url`
2. **Create job**: `POST /v2/pre-recorded` with `audio_url` and config → get `id`
3. **Poll**: `GET /v2/pre-recorded/:id` until `status: "done"` (or use webhooks/callbacks)
4. **Parse results**: Extract `transcription`, `diarization`, `translation`, etc. from response

## Managing Jobs

Use SDK methods for post-processing operations:

- JavaScript: `client.preRecorded().get(id)`, `.list(filters)`, `.getFile(id)`, `.delete(id)`
- Python: `client.prerecorded().get(id)`, `.list(filters)`, `.get_file(id)`, `.delete(id)`

For full JS/Python examples, pagination filters, and REST equivalents, see [./references/managing-jobs.md](./references/managing-jobs.md).

## Transcription Options

All options are passed as the second argument to `transcribe()`. Key options:

| Option            | Description                                 |
| ----------------- | ------------------------------------------- |
| `language_config` | Expected languages, code switching          |
| `diarization`     | Speaker identification (pre-recorded only)  |
| `translation`     | Translate to target languages               |
| `summarization`   | Generate bullet points or paragraph summary |
| `subtitles`       | Generate SRT/VTT files                      |
| `pii_redaction`   | Redact PII (pre-recorded only)              |
| `audio_to_llm`    | Run custom LLM prompts on transcript        |
| `callback_url`    | Async webhook delivery                      |

For full option details, see [./references/transcription-options.md](./references/transcription-options.md). For audio intelligence config, see [gladia-audio-intelligence](../gladia-audio-intelligence/SKILL.md). For client-level retry/timeouts, see [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md#configuration-options).

## Response and Delivery

For full response JSON and event names, see [./references/delivery-and-response.md](./references/delivery-and-response.md).

## Limits and Specifications

| Constraint              | Value                             |
| ----------------------- | --------------------------------- |
| Max file size           | 1000 MB                           |
| Max duration            | 135 minutes (120 min for YouTube) |
| Enterprise max duration | 4h15                              |
| Concurrency (paid)      | 25 concurrent jobs                |
| Concurrency (free)      | 3 concurrent jobs                 |

## Polling Best Practices

The SDK handles polling automatically — `transcribe()` polls until the job completes with configurable `interval` and `timeout`:

```typescript
const result = await client.preRecorded().transcribe(audio, options, {
  interval: 5000, // Poll every 5s
  timeout: 600000, // Timeout after 10 minutes
});
```

If using raw REST instead of the SDK:

- Use webhooks or callbacks instead of polling when possible
- If polling, implement exponential backoff (start at 3s, max 30s)

## Common Mistakes

- **Code switching without language list**: enabling `code_switching: true` with empty `languages` triggers 100+ language evaluation. Always provide 3-5 expected languages.
- **Polling without backoff**: rapid polling wastes requests and may trigger 429s. The SDK handles this; for raw REST, use webhooks or exponential backoff.
- **Expecting live-only features**: diarization, PII redaction, and subtitles are pre-recorded only — not available in live mode.
- **Wrong audio file path**: the audio download endpoint is `/v2/pre-recorded/:id/file`, not `/v2/pre-recorded/:id/audio`.

For the full list of gotchas and diagnostics, see the [gladia-troubleshooting skill](../gladia-troubleshooting/SKILL.md).

## Further Reading

- [Pre-recorded quickstart](https://docs.gladia.io/chapters/pre-recorded-stt/quickstart)
- [Audio intelligence overview](https://docs.gladia.io/chapters/pre-recorded-stt/audio-intelligence)
- [API reference: init](https://docs.gladia.io/api-reference/v2/pre-recorded/init)
