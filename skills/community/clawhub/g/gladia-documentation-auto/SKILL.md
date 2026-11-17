---
name: gladia-documentation-auto
description: Comprehensive Gladia speech-to-text reference auto-synced from docs.gladia.io. Use as a general-purpose fallback when other specialized skills don't match, or when the user needs a broad overview of Gladia capabilities, endpoints, decision guidance, or workflows. Always prefer the official SDK; fall back to raw REST/WebSocket only when SDK cannot satisfy the requirement.
license: MIT
metadata:
  source: https://docs.gladia.io/.well-known/agent-skills/gladia/skill.md
  digest: sha256:fce0f1bdb678fca35d434a7f9f589187478d079847f0b9fcd6b846c032d1365c
  synced: "2026-10-02"
---

> **SDK-first**: always use the official SDK — see [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md) for policy, setup, and fallback criteria.

## References

Consult these sibling skills as needed:

- ../gladia-sdk-integration/SKILL.md -- SDK setup, client initialization, error handling, and SDK vs raw API decision guide
- ../gladia-sdk-integration/references/sdk-versions.md -- Current SDK versions (auto-synced by CI)
- ../gladia-troubleshooting/SKILL.md -- Common errors, gotchas, and verification checklist
- ../gladia-live-transcription/SKILL.md -- Live streaming transcription
- ../gladia-pre-recorded-transcription/SKILL.md -- Pre-recorded file transcription

---
name: gladia
description: Use when transcribing audio or video to text, building real-time voice applications, extracting insights from speech (diarization, translation, sentiment), or integrating speech-to-text into voice agents, meeting recorders, or multilingual applications. Supports both pre-recorded (async) and live (streaming) transcription with 100+ languages.
metadata:
    mintlify-proj: gladia
    version: "1.0"
---

# Gladia Skill

## Product summary

Gladia is a speech-to-text (STT) API for transcribing audio and video to text. It supports two modes: **pre-recorded** (async file upload) and **live** (real-time WebSocket streaming). The API includes audio intelligence features (diarization, translation, sentiment analysis, PII redaction, summarization) and two models: **Solaria-3** (highest accuracy on European audio, pre-recorded only, 5 languages) and **Solaria-1** (default, 100+ languages, live + async, code switching).

**Key files and endpoints:**
- API key: Get from https://app.gladia.io/apikeys
- Pre-recorded: `POST /v2/pre-recorded` (create job), `GET /v2/pre-recorded/:id` (poll result)
- Live: `POST /v2/live` (init session), WebSocket connection for streaming
- Authentication: Header `x-gladia-key: YOUR_API_KEY`
- SDKs: `@gladiaio/sdk` (JavaScript/TypeScript), `gladiaio-sdk` (Python)
- CLI: `gladia transcribe <file>` for terminal use

**Primary docs:** https://docs.gladia.io

## When to use

Reach for Gladia when:
- Transcribing pre-recorded audio/video files (MP3, WAV, M4A, etc.) asynchronously
- Building real-time voice applications (live captions, voice agents, meeting recorders)
- Extracting structured data from speech (who spoke when, sentiment, entities, translations)
- Handling multilingual audio (100+ languages, code switching)
- Needing high accuracy on European business audio (Solaria-3)
- Integrating with Pipecat, LiveKit, Vapi, Twilio, or other voice platforms
- Running transcription from the terminal (CLI)

Do not use Gladia for:
- Audio longer than 135 minutes in a single pre-recorded request (use enterprise plan for 4h15)
- Live sessions exceeding 3 hours (start a new session before the limit)
- Solaria-3 with code switching or languages outside EN/FR/DE/ES/IT
- Storing audio indefinitely (configure data retention policy)

## Quick reference

### Authentication
```bash
# Set API key in environment
export GLADIA_API_KEY=your_key

# Or pass per request
curl -H "x-gladia-key: your_key" https://api.gladia.io/v2/pre-recorded
```

### Pre-recorded transcription (SDK)
```javascript
const gladia = new GladiaClient({ apiKey: "YOUR_KEY" });
const result = await gladia.preRecorded().transcribe("audio.mp3");
```

```python
gladia = GladiaClient(api_key="YOUR_KEY").prerecorded()
result = gladia.transcribe("audio.mp3")
```

### Live transcription (SDK)
```javascript
const session = gladia.liveV2().startSession({
  encoding: "wav/pcm",
  sample_rate: 16000,
  bit_depth: 16,
  channels: 1,
});
session.on("message", (msg) => {
  if (msg.type === "transcript" && msg.data.is_final) {
    console.log(msg.data.utterance.text);
  }
});
session.sendAudio(audioChunk);
session.stopRecording();
```

### CLI
```bash
gladia auth set your_key
gladia transcribe meeting.wav                    # text output
gladia transcribe podcast.mp3 -o json            # JSON output
gladia transcribe call.wav --diarize -o srt      # subtitles with speakers
gladia transcribe mixed.mp3 --code-switching     # mixed languages
gladia transcribe audio.mp3 --model solaria-3 --language en
```

### Model selection
| Model | Best for | Modes | Languages | Code switching |
|-------|----------|-------|-----------|---|
| **Solaria-3** | European real-world audio, highest accuracy | Pre-recorded only | EN, FR, DE, ES, IT | No |
| **Solaria-1** | Default, global coverage, live streaming | Pre-recorded + live | 100+ | Yes |

### Audio Intelligence features
- **Diarization**: Identify speakers (`diarization: true`)
- **Translation**: Translate to 100+ languages (`translation: true`, set `target_languages`)
- **Sentiment analysis**: Extract emotion and tone (`sentiment_analysis: true`)
- **PII redaction**: Anonymize sensitive data (`pii_redaction: true`)
- **Summarization**: Generate summaries (`summarization: true`, set `type: "general" | "bullet_points" | "concise"`)
- **Named Entity Recognition**: Extract entities (`named_entity_recognition: true`)
- **Custom vocabulary**: Boost accuracy for domain terms (`custom_vocabulary: true`, provide `vocabulary` list)
- **Subtitles**: Generate SRT/VTT (`subtitles: true`, set `formats`)

### Limits
| Limit | Value |
|-------|-------|
| Pre-recorded max duration | 135 minutes (enterprise: 4h15) |
| Live session max duration | 3 hours |
| Pre-recorded concurrency | 25 parallel + 300 queued (paid) |
| Live concurrency | 30 concurrent sessions |
| File size | 1000 MB max |
| Channels (pre-recorded) | 2 (mono/stereo) |
| Channels (live) | 8 |

## Decision guidance

### When to use Solaria-3 vs Solaria-1

| Condition | Use Solaria-3 | Use Solaria-1 |
|-----------|---|---|
| Pre-recorded audio | ✓ | ✓ |
| Live/streaming | ✗ | ✓ |
| European business audio (calls, meetings) | ✓ | — |
| 100+ languages needed | ✗ | ✓ |
| Code switching (mixed languages) | ✗ | ✓ |
| EN, FR, DE, ES, IT only | ✓ | ✓ |
| Clean, formal speech | — | ✓ |

### When to use pre-recorded vs live

| Scenario | Pre-recorded | Live |
|----------|---|---|
| Transcribe uploaded file | ✓ | ✗ |
| Real-time captions | ✗ | ✓ |
| Voice agent / IVR | ✗ | ✓ |
| Meeting recording | ✓ | ✓ (stream during call) |
| Batch processing | ✓ | ✗ |
| Async job with polling | ✓ | ✗ |
| WebSocket streaming | ✗ | ✓ |

### When to use SDK vs API vs CLI

| Tool | Best for | Complexity |
|------|----------|---|
| **SDK** (JavaScript/Python) | Application integration, error handling, retries | Low |
| **API** (REST/WebSocket) | Custom workflows, non-SDK languages | Medium |
| **CLI** | Terminal, scripts, CI/CD, one-off transcriptions | Very low |

### Result retrieval: polling vs webhooks vs callbacks

| Method | Use when | Trade-off |
|--------|----------|-----------|
| **Polling** (SDK `.poll()`) | Simple, synchronous flow | Blocks, wastes requests |
| **Webhooks** | Server-to-server, configured in dashboard | Setup required, less flexible |
| **Callbacks** | Per-job notification, no polling | Must expose HTTP endpoint |

## Workflow

### Pre-recorded transcription (typical flow)

1. **Get API key** from https://app.gladia.io/apikeys and set `GLADIA_API_KEY` environment variable.

2. **Choose model and features**: Decide between Solaria-3 (accuracy, 5 languages) or Solaria-1 (coverage, 100+ languages). List required audio intelligence features (diarization, translation, etc.).

3. **Prepare audio**: Ensure file is under 135 minutes, under 1000 MB, and in a supported format (MP3, WAV, M4A, FLAC, OGG, etc.).

4. **Upload and transcribe** (SDK):
   ```javascript
   const result = await gladia.preRecorded().transcribe("audio.mp3", {
     model: "solaria-3",
     language_config: { languages: ["en"] },
     diarization: true,
   });
   ```

5. **Poll or wait for callback**: SDK `.transcribe()` polls automatically. For raw API, use `.poll()` or configure a callback URL.

6. **Extract results**: Access `result.transcription.full_transcript`, `result.transcription.utterances`, `result.diarization`, `result.translation`, etc.

7. **Handle errors**: Check `result.status` for "done" or "error". Inspect error details before retrying (transient vs. input issues).

### Live transcription (typical flow)

1. **Initialize session** (backend):
   ```javascript
   const response = await fetch("https://api.gladia.io/v2/live", {
     method: "POST",
     headers: { "x-gladia-key": "YOUR_KEY", "Content-Type": "application/json" },
     body: JSON.stringify({
       encoding: "wav/pcm",
       sample_rate: 16000,
       bit_depth: 16,
       channels: 1,
       language_config: { languages: ["en"] },
     }),
   });
   const { id, url } = await response.json();
   ```

2. **Return secure URL to client**: Pass `url` (contains temporary token) to frontend/mobile app. Keep API key on backend.

3. **Client connects to WebSocket** and sends audio chunks as they arrive.

4. **Listen for messages**: Handle `transcript` (partial/final), `speech_start`, `speech_end`, `sentiment_analysis`, etc.

5. **Stop recording**: Send `stop_recording` message or close WebSocket with code 1000. Server processes remaining audio and post-processing.

6. **Retrieve final results**: Call `GET /v2/live/:id` to fetch complete transcript, diarization, translation, etc.

## Common gotchas

- **Solaria-3 with multiple languages**: Solaria-3 does not support code switching. Pass exactly one language in `language_config.languages` (e.g., `["fr"]`), not multiple. Use Solaria-1 for mixed-language audio.

- **Live session timeout**: A single WebSocket session cannot exceed 3 hours. For longer events, start a new session before reaching the limit. Track session duration and reconnect proactively.

- **Resubmitting the same audio**: If a POST already returned 200 or you received a `transcription.created` webhook, do not resubmit the same audio. Wait on that job ID. Resubmitting creates a new billable job.

- **Polling without backoff**: Polling too aggressively wastes API quota. Use exponential backoff (start at 1s, cap at 10s) or switch to callbacks/webhooks.

- **Audio format mismatch**: Ensure `encoding`, `sample_rate`, `bit_depth`, and `channels` match your actual audio. Mismatches cause silent failures or garbled output.

- **Missing language specification**: If you know the language, set `language_config.languages` to skip auto-detection and reduce latency. Auto-detection adds 1–2 seconds.

- **Callback URL not reachable**: If using callbacks, ensure your endpoint is publicly accessible and returns 2xx within a reasonable timeout. Gladia retries failed callbacks.

- **Concurrency limits**: Free tier: 3 pre-recorded concurrent, 1 live. Paid: 25 pre-recorded concurrent, 30 live. Requests beyond the limit queue. Monitor queue time during high load.

- **Data retention**: By default, audio and transcripts are retained. If GDPR/privacy is a concern, enable Zero Data Retention (results delivered only via callbacks, no retrieval).

- **Partial transcripts accuracy**: Partial transcripts use a faster, smaller model than finals. Accuracy degrades with multiple languages or code switching. Use for UX only, not for final output.

## Verification checklist

Before submitting work:

- [ ] API key is set in environment or passed securely (never hardcoded in client code).
- [ ] Model choice matches use case (Solaria-3 for European accuracy, Solaria-1 for live or 100+ languages).
- [ ] Language configuration is correct: single language for Solaria-3, multiple allowed for Solaria-1 with code switching.
- [ ] Audio file is under 135 minutes and 1000 MB (or enterprise plan for longer).
- [ ] Audio format, encoding, sample rate, and channels are specified correctly.
- [ ] Audio Intelligence features are enabled only if needed (diarization, translation, etc.).
- [ ] Callback or webhook URL is configured if using async notification (not polling).
- [ ] Error handling is in place: check job status, inspect error details, retry only on transient failures.
- [ ] Live session duration is monitored; new session started before 3-hour limit.
- [ ] Results are extracted from the correct fields: `transcription.full_transcript`, `transcription.utterances`, `diarization.speakers`, `translation.results`, etc.
- [ ] Concurrency limits are respected; requests queue gracefully when limits are hit.
- [ ] Data retention policy is configured (default: stored; set to zero-retention if required).

## Resources

**Comprehensive page-by-page navigation:**
https://docs.gladia.io/llms.txt

**Critical documentation pages:**
1. [Pre-recorded STT Quickstart](https://docs.gladia.io/chapters/pre-recorded-stt/quickstart) — Upload, create job, poll results, configure features
2. [Live STT Quickstart](https://docs.gladia.io/chapters/live-stt/quickstart) — WebSocket init, streaming, message handling
3. [Models](https://docs.gladia.io/chapters/introduction/models) — Solaria-3 vs Solaria-1 comparison and selection guide
4. [Audio Intelligence](https://docs.gladia.io/chapters/audio-intelligence/) — Diarization, translation, sentiment, PII redaction, summarization
5. [Limits & Specifications](https://docs.gladia.io/chapters/limits-and-specifications/concurrency) — Concurrency, duration, file size, rate limits
6. [CLI](https://docs.gladia.io/chapters/developer-tools/gladia-cli) — Terminal transcription without code
7. [API Reference](https://docs.gladia.io/api-reference/) — Full endpoint documentation, request/response schemas

---

> For additional documentation and navigation, see: https://docs.gladia.io/llms.txt
---

> This file is auto-synced from https://docs.gladia.io/.well-known/agent-skills/gladia/skill.md
> Do not edit manually — changes will be overwritten by CI.
> For additional documentation and navigation, see: https://docs.gladia.io/llms.txt
