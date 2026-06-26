---
name: oatda-translate-audio
description: Translate foreign-language audio into English text using OATDA's unified audio API. Triggers when the user wants audio translation, spoken-language translation, Whisper-style translation, or English output from uploaded recordings through OATDA.
homepage: https://oatda.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🌍",
        "requires": { "bins": ["curl", "jq"], "env": ["OATDA_API_KEY"], "config": ["~/.oatda/credentials.json"] },
        "primaryEnv": "OATDA_API_KEY",
      },
  }
---

# OATDA Audio Translation

Translate foreign-language audio into English text through OATDA's unified audio API.

## API Key Resolution

All commands need the OATDA API key. Resolve it inline for each `exec` call:

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}"
```

If the key is empty or `null`, tell the user to get one at https://oatda.com and configure it.

**Security**: Never print the full API key. Only verify existence or show first 8 chars.

## Model Mapping

| User says | Provider | Model |
|-----------|----------|-------|
| whisper, whisper-1, openai whisper (default) | openai | whisper-1 |
| translate audio, audio translation | openai | whisper-1 |

**Default**: `openai` / `whisper-1` if no model specified.

If the user provides `provider/model` format directly (for example `openai/whisper-1`), split on `/`.

> ⚠️ Models change over time. If a model ID fails, query `oatda-list-models` with `?type=audio` first.

## Input Preparation

The translation endpoint supports:
- `multipart/form-data` with a local file upload
- JSON with a base64 data URL in `file`

Maximum audio file size is 25MB.

For local files, prefer multipart upload because it is simpler and avoids large JSON bodies.

## Discovering Audio Model Parameters

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X GET "https://oatda.com/api/v1/llm/models?type=audio" \
  -H "Authorization: Bearer $OATDA_API_KEY" | jq '.audio_models[] | {id, supported_params}'
```

Look for:
- `audio_modes` containing `translation`
- supported `response_format` values
- optional prompt or filename support

## API Call (multipart)

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/translations" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -F "provider=<PROVIDER>" \
  -F "model=<MODEL>" \
  -F "file=@<AUDIO_FILE>" \
  -F "response_format=json"
```

## Alternative API Call (base64 JSON)

```bash
AUDIO_DATA_URL="data:audio/mpeg;base64,$(base64 -w 0 audio.mp3)"

export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/translations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d "$(jq -n \
    --arg provider \"<PROVIDER>\" \
    --arg model \"<MODEL>\" \
    --arg file \"$AUDIO_DATA_URL\" \
    '{provider: $provider, model: $model, file: $file, response_format: \"json\"}')"
```

## Common Parameters

- `prompt`: Optional hint for terminology, names, or translation style
- `response_format`: `json`, `text`, `srt`, `verbose_json`, or `vtt`
- `temperature`: 0 to 1
- `filename`: Optional filename for JSON uploads

## Response Format

The API returns JSON like:

```json
{
  "text": "The English translation...",
  "language": "fr",
  "duration": 42.5,
  "costs": {
    "inputCost": 0,
    "outputCost": 0.0001,
    "totalCost": 0.0001,
    "currency": "USD"
  }
}
```

Present the `text` field to the user and mention that the output is English.

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid API key | Tell user to check their key |
| 402 | Insufficient credits | Tell user to check balance |
| 400 | Bad request / model not supported | Check model or file format and query `oatda-list-models` with `type=audio` |
| 413 | File too large | Keep audio under 25MB or split it |
| 429 | Rate limited or monthly cap | Wait briefly and retry once |

## Example

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/translations" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -F "provider=openai" \
  -F "model=whisper-1" \
  -F "file=@french-audio.mp3" \
  -F "response_format=json"
```

## Notes

- Endpoint: `/api/v1/llm/translations`
- Translation output is English text
- Prefer multipart upload for local files
- Use `prompt` for names, acronyms, or domain-specific terminology
- Equivalent capability name: `translate_audio`
- Related skills: `oatda-transcribe-audio`, `oatda-generate-speech`, `oatda-list-models`
