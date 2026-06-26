---
name: gladia-documentation-auto
description: Comprehensive Gladia speech-to-text reference auto-synced from docs.gladia.io. Use as a general-purpose fallback when other specialized skills don't match, or when the user needs a broad overview of Gladia capabilities, endpoints, decision guidance, or workflows. Always prefer the official SDK; fall back to raw REST/WebSocket only when SDK cannot satisfy the requirement.
license: MIT
metadata:
  source: https://docs.gladia.io/.well-known/agent-skills/gladia/skill.md
  digest: sha256:cae5af7bbe95a1e0c1389bf07116cc038c7ff8f0ee23784588852047eb32be93
  synced: "2026-06-09"
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
name: Gladia
description: Use when building speech transcription features, processing audio/video files, implementing real-time transcription, extracting insights from audio (speaker identification, translation, sentiment), or integrating voice capabilities into applications. Agents should reach for this skill when users request transcription, audio analysis, or voice-driven features.
metadata:
    mintlify-proj: gladia
    version: "1.0"
---

# Gladia Speech-to-Text API

## Product summary

Gladia is a speech-to-text API that transcribes audio and video files in two modes: **pre-recorded** (asynchronous, file-based) and **live** (real-time, WebSocket-based). Beyond transcription, it provides audio intelligence features like speaker diarization, translation, sentiment analysis, PII redaction, and custom vocabulary matching. Agents use Gladia to build transcription workflows, extract structured data from audio, and power voice-driven applications.

**Key files and commands:**
- SDKs: JavaScript (`@gladiaio/sdk`) and Python (`gladiaio-sdk`)
- Authentication: Pass `x-gladia-key` header with your API key
- Pre-recorded endpoint: `POST /v2/pre-recorded` (create job), `GET /v2/pre-recorded/:id` (poll results)
- Live endpoint: `POST /v2/live` (init session), WebSocket connection for streaming audio
- Primary docs: https://docs.gladia.io

## When to use

Reach for this skill when:
- A user wants to transcribe audio or video files (meetings, podcasts, calls, interviews)
- Building real-time transcription (voice agents, live captions, meeting recorders)
- Extracting speaker information (who said what, speaker count, speaker identification)
- Translating transcripts to other languages or generating subtitles
- Detecting sensitive information (PII redaction for GDPR/HIPAA compliance)
- Improving transcription accuracy with domain-specific vocabulary
- Analyzing sentiment or emotions in speech
- Integrating with third-party platforms (Twilio, Vapi, LiveKit, Pipecat, etc.)

## Quick reference

### Authentication
```bash
# All requests require the x-gladia-key header
curl --header 'x-gladia-key: YOUR_API_KEY' https://api.gladia.io/v2/...
```

### Pre-recorded workflow (file-based)
1. **Upload** audio: `POST /v2/upload` → get `audio_url`
2. **Create job**: `POST /v2/pre-recorded` with `audio_url` and options
3. **Poll result**: `GET /v2/pre-recorded/:id` until `status: "done"`

Or use SDK's `transcribe()` method for end-to-end in one call.

### Live workflow (real-time)
1. **Init session**: `POST /v2/live` with audio config (encoding, sample_rate, bit_depth, channels)
2. **Connect WebSocket**: Use returned `url` to open WebSocket connection
3. **Send audio**: Stream audio chunks as binary or base64-encoded JSON
4. **Read messages**: Receive transcript, translation, sentiment, etc. via WebSocket
5. **Stop**: Send `stop_recording` message; WebSocket closes when post-processing done

### Audio formats supported
| Type | Examples |
|------|----------|
| Audio | MP3, WAV, FLAC, AAC, OGG, Opus, M4A |
| Video | MP4, MOV, AVI, WebM, Matroska |
| Online | TikTok, Instagram, Facebook, Vimeo, LinkedIn, YouTube (via URL) |

### File limits
- **Pre-recorded**: Max 135 minutes (2h15m) or 1000 MB; enterprise plans support 4h15m
- **Live**: Max 3 hours per session
- **Recommendation**: Split files >60 minutes for better quality

### Common audio intelligence features

| Feature | Pre-recorded | Live | Use case |
|---------|--------------|------|----------|
| **Diarization** | ✓ | ✓ | Identify speakers, separate voices |
| **Translation** | ✓ | ✓ | Translate to 100+ languages |
| **Subtitles** | ✓ | - | Generate SRT/VTT files |
| **Custom vocabulary** | ✓ | ✓ | Fix domain-specific terms |
| **Custom spelling** | ✓ | ✓ | Normalize misspelled words |
| **Sentiment analysis** | ✓ | ✓ | Detect sentiment & emotions |
| **PII redaction** | ✓ | - | Mask sensitive data (GDPR/HIPAA) |
| **Named entity recognition** | ✓ | ✓ | Extract people, places, dates |
| **Summarization** | ✓ | - | Auto-generate summaries |
| **Chapterization** | ✓ | - | Split into chapters/segments |

## Decision guidance

### When to use pre-recorded vs. live

| Scenario | Use pre-recorded | Use live |
|----------|------------------|----------|
| User uploads a file to transcribe | ✓ | - |
| Real-time transcription (voice agent, meeting) | - | ✓ |
| Post-processing (subtitles, translation, summarization) | ✓ | - |
| Low-latency response needed | - | ✓ |
| Batch processing multiple files | ✓ | - |

### When to use custom vocabulary vs. custom spelling

| Situation | Use custom vocabulary | Use custom spelling |
|-----------|----------------------|---------------------|
| Model outputs garbled/phonetically wrong text | ✓ | - |
| Model outputs recognizable but misspelled word | - | ✓ |
| Domain-specific terms (brand names, jargon) | ✓ | - |
| Normalizing variant spellings | - | ✓ |

### When to use diarization vs. multi-channel audio

| Scenario | Use diarization | Use multi-channel |
|----------|-----------------|-------------------|
| Single audio stream, multiple speakers | ✓ | - |
| Separate audio tracks per speaker | - | ✓ |
| Unknown number of speakers | ✓ | - |
| Known speaker count and channels | - | ✓ |

## Workflow

### Pre-recorded transcription (typical task)

1. **Understand requirements**: Confirm audio format, language, desired features (diarization, translation, subtitles, PII redaction).

2. **Check file constraints**: Verify file is <1000 MB and <135 minutes (or split if needed).

3. **Upload audio** (if local file):
   ```javascript
   const uploadResponse = await gladiaClient.preRecorded().uploadFile("path/to/audio.mp3");
   const audioUrl = uploadResponse.audio_url;
   ```

4. **Create transcription job** with options:
   ```javascript
   const job = await gladiaClient.preRecorded().createUntyped({
     audio_url: audioUrl,
     language_config: { languages: ["en"], code_switching: false },
     diarization: true,
     diarization_config: { min_speakers: 1, max_speakers: 5 },
     custom_vocabulary: true,
     custom_vocabulary_config: { vocabulary: ["Gladia", "Solaria"] },
     translation: true,
     translation_config: { target_languages: ["fr"], model: "base" },
     sentiment_analysis: true,
     pii_redaction: true,
     pii_redaction_config: { entity_types: ["GDPR"] }
   });
   ```

5. **Poll for results** (or use webhooks/callbacks):
   ```javascript
   let result = await gladiaClient.preRecorded().get(job.id);
   while (result.status !== "done") {
     await new Promise(r => setTimeout(r, 2000));
     result = await gladiaClient.preRecorded().get(job.id);
   }
   ```

6. **Extract and validate results**: Check `transcription.utterances`, `translation`, `sentiment_analysis`, `diarization` fields.

7. **Verify output**: Confirm speaker attribution, translation accuracy, PII masking, and custom vocabulary replacements.

### Live transcription (typical task)

1. **Understand audio source**: Confirm encoding (wav/pcm, sample_rate, bit_depth, channels).

2. **Initialize session**:
   ```javascript
   const liveSession = gladiaClient.liveV2().startSession({
     model: "solaria-1",
     encoding: "wav/pcm",
     sample_rate: 16000,
     bit_depth: 16,
     channels: 1,
     language_config: { languages: ["en"], code_switching: false },
     messages_config: { receive_partial_transcripts: true }
   });
   ```

3. **Connect WebSocket and set up handlers**:
   ```javascript
   liveSession.on("message", (message) => {
     if (message.type === "transcript" && message.data.is_final) {
       console.log(message.data.utterance.text);
     }
   });
   ```

4. **Stream audio chunks** as they arrive:
   ```javascript
   liveSession.sendAudio(audioChunk);
   ```

5. **Stop recording** when done:
   ```javascript
   liveSession.stopRecording();
   ```

6. **Retrieve final results** (optional):
   ```javascript
   const result = await fetch(`https://api.gladia.io/v2/live/${sessionId}`, {
     headers: { "x-gladia-key": apiKey }
   });
   ```

## Common gotchas

- **Empty language list with code switching**: Do not set `languages: []` and `code_switching: true` together. The detector will evaluate every utterance against 100+ languages, causing misdetections. Always provide a constrained list (3-5 languages max).

- **Forgetting audio metadata**: For live transcription, `encoding`, `sample_rate`, `bit_depth`, and `channels` must match your actual audio stream. Mismatches cause garbled output.

- **Custom vocabulary intensity too high**: Start at `intensity: 0.4` and raise only if terms are missed. High intensity causes false positives (unrelated words get replaced). Add `pronunciations` variants before raising intensity.

- **Polling without backoff**: Don't hammer the API with rapid polls. Use 2-3 second intervals or webhooks/callbacks instead.

- **Exceeding file limits silently**: Pre-recorded files >135 minutes or >1000 MB will fail. Split large files into ~60-minute chunks before uploading.

- **Not setting language when known**: If you know the language, set `languages: ["en"]` explicitly. Omitting it forces detection, adding latency and risk of misdetection.

- **Diarization without hints**: If you know the speaker count, set `number_of_speakers` or `min_speakers`/`max_speakers`. Hints improve accuracy.

- **PII redaction only for pre-recorded**: PII redaction is not available for live transcription. Plan accordingly for compliance workflows.

- **Webhook/callback URL not reachable**: If using webhooks, ensure your callback URL is publicly accessible and returns 2xx status. Gladia will retry failed deliveries.

- **Multi-channel audio billing**: Transcribing multi-channel audio is billed by total duration × number of channels. A 1-hour 3-channel stream costs 3 hours of transcription.

## Verification checklist

Before submitting transcription work:

- [ ] Audio file is valid format (MP3, WAV, MP4, etc.) and <1000 MB
- [ ] File duration is <135 minutes (or split if longer)
- [ ] API key is valid and has `x-gladia-key` header set
- [ ] Language is set explicitly if known; avoid empty `languages` with `code_switching: true`
- [ ] Custom vocabulary entries are tested; intensity is 0.4-0.6 unless tuned
- [ ] Diarization hints (min/max speakers) are provided if speaker count is known
- [ ] Webhook/callback URL (if used) is publicly accessible and returns 2xx
- [ ] Results include expected fields: `transcription.utterances`, `translation`, `sentiment_analysis`, etc.
- [ ] Speaker attribution is correct (diarization `speaker` field matches expected speakers)
- [ ] PII redaction is applied (if required) and sensitive data is masked
- [ ] Translation accuracy is spot-checked for domain-specific terms
- [ ] Subtitles (if generated) have correct timing and formatting

## Resources

- **Comprehensive page listing**: https://docs.gladia.io/llms.txt
- **Getting started**: https://docs.gladia.io/chapters/introduction/getting-started
- **Pre-recorded quickstart**: https://docs.gladia.io/chapters/pre-recorded-stt/quickstart
- **Live transcription quickstart**: https://docs.gladia.io/chapters/live-stt/quickstart
- **Audio intelligence features**: https://docs.gladia.io/chapters/audio-intelligence/
- **Recommended parameters by use case**: https://docs.gladia.io/chapters/pre-recorded-stt/recommended-parameters
- **API reference**: https://docs.gladia.io/api-reference/
- **SDK documentation**: https://docs.gladia.io/chapters/integrations/sdk

---

> For additional documentation and navigation, see: https://docs.gladia.io/llms.txt
---

> This file is auto-synced from https://docs.gladia.io/.well-known/agent-skills/gladia/skill.md
> Do not edit manually — changes will be overwritten by CI.
> For additional documentation and navigation, see: https://docs.gladia.io/llms.txt
