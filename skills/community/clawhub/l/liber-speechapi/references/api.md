# Liber SpeechAPI Reference

## Base URL

Default example:

```text
http://localhost:5555/api/v1
```

Set the actual base URL through `.env`:

- `LIBER_API_BASE_URL`

## Authentication

Use bearer token authentication:

```http
Authorization: Bearer YOUR_API_KEY
```

Read the token from:

- `LIBER_API_KEY`

Do not hardcode tokens in scripts.

---

## Health check

```http
GET /health
```

Use this to verify service availability before ASR/TTS when needed.

---

## ASR

### Endpoint

```http
POST /asr/transcribe
```

### Form fields

- `file`: local audio file upload
- `url`: remote audio URL, optional alternative to file
- `language`: e.g. `zh`, `en`
- `task`: `transcribe` or `translate`
- `timestamps`: `chunk` or `word`
- other optional backend parameters from `config.json`

### Expected response fields

- `text`: recognized text
- `chunks`: optional segment information
- `meta`: metadata

### Output modes in this skill

- direct ASR default: return full JSON
- explicit text-only mode: return `text` only
- Telegram/openclaw mode: extract `text` and pass it into the chatbot workflow

### Notes

- Prefer file upload for Telegram voice processing.
- Validate that the input file exists and is readable.
- Fail clearly if no `text` is returned.

---

## TTS

### Endpoint

```http
POST /tts/synthesize
```

### Form fields

- `text`: text to synthesize
- `model`: `multilingual`, `turbo`, or `standard`
- `language`: e.g. `zh`, `en`
- `format`: `wav`, `mp4`, or `ogg_opus`
- `audio_prompt`: optional reference audio file for voice cloning
- other optional backend parameters from `config.json`

### Expected response fields

- `audio_url`: generated audio file URL
- `meta.format`
- `meta.sample_rate`

### Output format rules in this skill

- direct TTS default: `wav`
- Telegram voice reply: force `ogg_opus`
- explicit caller override: honor the requested format when it is valid

### Notes

- For Telegram voice notes, use `format=ogg_opus`.
- Only send `audio_prompt` when clone audio is enabled and the file exists.
- If `audio_prompt` is disabled or missing, send a normal TTS request.

---

## Telegram compatibility

The upstream project explicitly recommends `OGG/Opus` for Telegram voice-note delivery.

Use:
- `format=ogg_opus`

---

## Error handling guidance

Handle these cases explicitly:
- network timeout
- 401/403 authentication failure
- 404 wrong base URL or endpoint
- 422 invalid form fields
- empty ASR text
- empty TTS audio_url

Return actionable messages so the calling workflow can decide whether to retry, downgrade, or fall back to plain text.
