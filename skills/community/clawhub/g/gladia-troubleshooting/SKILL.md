---
name: gladia-troubleshooting
description: Diagnose and fix common Gladia API issues. Use when the user encounters errors (401, 403, 429), unexpected behavior, poor transcription quality, billing confusion, audio format problems, WebSocket disconnections, polling failures, or asks about limits and rate limiting. SDK-first diagnostics — many issues are solved by migrating to the official SDK.
license: MIT
---

# Troubleshooting

Common issues, gotchas, and their solutions when working with the Gladia API.

> **SDK-first diagnostics**: first verify the user is on the official SDK — many issues (polling, reconnection, retries) are solved automatically. See [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md) for setup and policy.

## When to Use

- User encounters errors (401, 403, 429, invalid format, timeout) when calling the Gladia API
- Unexpected behavior: poor transcription quality, missing words, wrong language
- WebSocket disconnections, polling failures, or session hangs
- Billing confusion (multi-channel, concurrency limits, plan restrictions)
- Verifying that an integration is correctly configured before going to production

**When NOT to use:** For initial SDK setup and configuration, use [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md). For feature-specific guidance (options, parameters, response structure), use [gladia-pre-recorded-transcription](../gladia-pre-recorded-transcription/SKILL.md) or [gladia-live-transcription](../gladia-live-transcription/SKILL.md).

## References

Consult these resources as needed:

- ../gladia-sdk-integration/SKILL.md -- SDK setup, client config (retry, timeouts), and SDK vs raw API decision guide
- ../gladia-sdk-integration/references/sdk-versions.md -- Current SDK versions (auto-synced by CI)
- ../gladia-pre-recorded-transcription/SKILL.md -- Pre-recorded config options and limits
- ../gladia-live-transcription/SKILL.md -- Live session config and WebSocket event handling
- ../gladia-audio-intelligence/SKILL.md -- Audio intelligence feature configs and availability matrix

## Authentication Errors

### 401 Unauthorized

- **Cause**: Invalid or missing API key
- **Fix (SDK)**: Verify the key is passed via the `apiKey` (JS) / `api_key` (Python) constructor option, or set the `GLADIA_API_KEY` environment variable
- **Fix (raw REST)**: Verify the key is passed in the `x-gladia-key` header
- **Check**: Go to [app.gladia.io](https://app.gladia.io) → API keys → verify the key is active

### 403 Forbidden

- **Cause**: Key doesn't have access to the requested feature or region
- **Fix**: Check your plan tier; some features are plan-restricted

## Rate Limiting and Concurrency

### 429 Too Many Requests

Concurrency limits by plan:

| Plan       | Pre-recorded |   Live    | Notes              |
| ---------- | :----------: | :-------: | ------------------ |
| Free       |      3       |     1     | 10 hrs/month total |
| Starter    |      25      |    30     | —                  |
| Growth     |      25      |    30     | —                  |
| Enterprise |  Unlimited   | Unlimited | —                  |

**Fix**: Wait for in-progress jobs to complete before starting new ones, or upgrade your plan.

## Common Gotchas

### 1. Code switching without language list

**Problem**: Enabling `code_switching: true` with an empty `languages` array causes evaluation across 100+ languages and frequent misdetections.

**Fix**: Always provide 3-5 expected languages:

```json
{
  "language_config": {
    "languages": ["en", "fr", "es"],
    "code_switching": true
  }
}
```

### 2. Custom vocabulary intensity too high

**Problem**: `intensity` values above 0.6 cause false positives where unrelated words get replaced by vocabulary entries.

**Fix**: Keep intensity at 0.4-0.6. Use `pronunciations` for better recognition instead of raising intensity:

```json
{
  "vocabulary": [
    { "value": "Gladia", "pronunciations": ["gla-dee-ah"], "intensity": 0.5 }
  ]
}
```

### 3. Audio exceeding duration limits silently

**Problem**: Pre-recorded files over 135 minutes may fail without a clear error message.

**Fix**: Split long audio into chunks of ~60 minutes before uploading. For enterprise (4h15 limit), contact support.

### 4. Multi-channel billing surprise

**Problem**: Sending 2-channel (stereo) audio is billed as 2x the duration.

**Fix**: Merge to mono if you don't need per-channel speaker identification. Only use multi-channel intentionally for distinct audio sources.

### 5. WebSocket disconnection without recovery

**Problem**: If the WebSocket drops, creating a new session loses context.

**Fix (SDK — recommended)**: The SDK handles reconnection automatically with configurable `wsRetry`. No action needed if using the SDK.

**Fix (raw WebSocket)**: Reconnect to the **same WebSocket URL** to resume the session. Do NOT call `/v2/live` again.

### 6. Polling without backoff

**Problem**: Rapidly polling `/v2/pre-recorded/:id` wastes requests and may trigger rate limits.

**Fix (SDK — recommended)**: The SDK handles polling automatically. Use `transcribe()` which includes built-in backoff, or configure `poll()` directly:

```typescript
const result = await client.preRecorded().transcribe(audio, options, {
  interval: 5000, // 5 seconds between polls
});
```

```python
result = client.prerecorded().transcribe(
    "audio.mp3",
    options,
    {"interval": 5000},  # 5 seconds between polls
)
```

**Fix (raw REST)**: Implement exponential backoff (start at 3s, max 30s), or use webhooks/callbacks instead.

### 7. Forgetting to stop recording

**Problem**: Leaving a WebSocket open without sending `stop_recording` keeps the session hanging until the 3-hour timeout.

**Fix**: Always explicitly call `session.stopRecording()` (or `session.stop_recording()` in Python) when done. Implement cleanup in error handlers.

### 8. Partial transcripts not appearing

**Problem**: Real-time results come only as final transcripts by default.

**Fix**: Enable partial transcripts in session config:

```json
{
  "messages_config": {
    "receive_partial_transcripts": true
  }
}
```

### 9. Expecting diarization in live mode

**Problem**: Speaker diarization is only available for pre-recorded transcription.

**Fix**: For live multi-speaker scenarios, use multi-channel audio with one speaker per channel and track by channel number.

### 10. PII redaction in live mode

**Problem**: `pii_redaction: true` is silently ignored in live transcription.

**Fix**: PII redaction only works for pre-recorded. For live compliance needs, implement client-side redaction on the transcript text.

## Audio Format Issues

### "Invalid audio format" error

- Verify `encoding`, `sample_rate`, `bit_depth`, `channels` match your actual audio stream
- For pre-recorded: format is auto-detected from the file; this error is live-specific
- For supported formats and size limits, see [gladia-pre-recorded-transcription](../gladia-pre-recorded-transcription/SKILL.md#limits-and-specifications) and [gladia-live-transcription](../gladia-live-transcription/SKILL.md#limits)

## Transcription Quality Issues

### Poor accuracy

1. **Check audio quality**: Background noise, low volume, or heavy compression degrades results
2. **Enable audio enhancer**: `pre_processing.audio_enhancer: true` (live)
3. **Specify languages**: Always provide expected languages rather than relying on auto-detection
4. **Use custom vocabulary**: For domain-specific terms (medical, legal, technical)
5. **Check sample rate**: Higher sample rates (16kHz+) give better results than 8kHz

### Wrong language detected

1. Provide explicit `languages` list
2. If multi-language, enable `code_switching` with 3-5 expected languages
3. For single-language content, specify exactly one language and disable code switching

### Missing words or gaps

1. Check for silence or very low volume sections
2. Verify audio isn't corrupted (try playing it back)
3. For live: ensure chunks are sent continuously without large gaps

## Webhook/Callback Issues

### Callbacks not received

1. Verify `callback_url` is publicly reachable (not localhost)
2. Check your server returns 2xx within timeout
3. Verify no firewall/WAF blocking incoming requests
4. Test with a service like webhook.site first

### Webhook signature verification

Webhooks are powered by Svix. Verify using the Svix libraries:

```typescript
import { Webhook } from "svix";
const wh = new Webhook(webhookSecret);
wh.verify(payload, headers);
```

## Verification Checklist

Before submitting transcription work:

- [ ] Using the official Gladia SDK (if not, confirm there is a valid reason for raw API calls)
- [ ] API key is valid and passed correctly (SDK constructor or `GLADIA_API_KEY` env var)
- [ ] Audio file is under 1000 MB and within duration limits
- [ ] Audio format is supported
- [ ] If using code switching, `languages` list has 3-5 entries
- [ ] If using custom vocabulary, intensity is 0.4-0.6
- [ ] For live: session properly closed with `stopRecording()` / `stop_recording()`
- [ ] For live: audio format config matches actual stream
- [ ] Callbacks/webhooks are reachable if configured
- [ ] Multi-channel audio is intentional
- [ ] Error responses are handled (SDK throws typed errors; raw API returns `status`, `error_message`)

## Further Reading

- [Authentication](https://docs.gladia.io/chapters/api/authentication)
- [Rate limits and concurrency](https://docs.gladia.io/chapters/limits-and-specifications/rate-limits)
- [Supported formats and limits](https://docs.gladia.io/chapters/limits-and-specifications/supported-formats)
- [Webhooks](https://docs.gladia.io/chapters/pre-recorded-stt/webhooks)
- [API reference (error codes)](https://docs.gladia.io/api-reference)

## Support Resources

- [Gladia Documentation](https://docs.gladia.io)
- [Support Center](https://support.gladia.io)
- [API Status](https://status.gladia.io)
- [Dashboard](https://app.gladia.io)
