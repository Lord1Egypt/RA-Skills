---
name: oatda-generate-speech
description: Generate speech or audio from text using OATDA's unified audio API. Triggers when the user wants to convert text to speech, create narration, voiceovers, accessibility audio, or use TTS models such as OpenAI tts-1 through OATDA.
homepage: https://oatda.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires": { "bins": ["curl", "jq"], "env": ["OATDA_API_KEY"], "config": ["~/.oatda/credentials.json"] },
        "primaryEnv": "OATDA_API_KEY",
      },
  }
---

# OATDA Speech Generation

Generate spoken audio from text through OATDA's unified audio API.

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
| tts, tts-1, openai tts (default) | openai | tts-1 |
| tts hd, tts-1-hd | openai | tts-1-hd |
| gpt tts, gpt-4o mini tts | openai | gpt-4o-mini-tts |

**Default**: `openai` / `tts-1` if no model specified.

If the user provides `provider/model` format directly (for example `openai/tts-1`), split on `/`.

Common OpenAI voices include `alloy`, `ash`, `ballad`, `coral`, `echo`, `fable`, `nova`, `onyx`, `sage`, and `shimmer`. Use `alloy` if the user does not specify a voice.

> ⚠️ Models change over time. If a model ID fails, query `oatda-list-models` with `?type=audio` first.

## Discovering Audio Model Parameters

Query available audio models and inspect `supported_params` before sending optional fields:

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X GET "https://oatda.com/api/v1/llm/models?type=audio" \
  -H "Authorization: Bearer $OATDA_API_KEY" | jq '.audio_models[] | {id, supported_params}'
```

Look for:
- `audio_modes` containing `tts`
- supported `voice` values
- allowed `response_format` values
- optional fields like `instructions` or `language`

## API Call

The speech endpoint returns **binary audio**, not JSON. Always save the response to a file.

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/speech" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "<PROVIDER>",
    "model": "<MODEL>",
    "input": "<TEXT_TO_SPEAK>",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
  }' \
  --output speech.mp3
```

### Common Parameters

- `input`: Text to convert to speech, max 15000 characters
- `voice`: Voice name, e.g. `alloy`, `nova`, `shimmer`
- `response_format`: `mp3`, `opus`, `aac`, `flac`, `wav`, `pcm`, `mulaw`, or `alaw`
- `speed`: 0.25 to 4.0, default 1.0
- `instructions`: Optional tone/style guidance for supported models
- `language`: Optional language code for supported models

## Success Handling

If the request succeeds, tell the user where the file was saved, for example:

> Speech generated successfully: `speech.mp3`

If headers matter, use `curl -D headers.txt` while still saving the audio body with `--output`.

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid API key | Tell user to check their key |
| 402 | Insufficient credits | Tell user to check balance |
| 400 | Bad request / model not supported | Check model format and query `oatda-list-models` with `type=audio` |
| 429 | Rate limited or monthly cap | Wait briefly and retry once |
| 500 | Provider error | Show the error message if returned |

## Example

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/speech" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "openai",
    "model": "tts-1",
    "input": "Welcome to OATDA, one API to direct all.",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
  }' \
  --output speech.mp3
```

## Notes

- Endpoint: `/api/v1/llm/speech`
- Use `input`, not `prompt`, for TTS requests
- Always save the response with `--output`
- Use `oatda-list-models` to discover available audio models
- Equivalent capability name: `generate_speech`
- Related skills: `oatda-list-models`, `oatda-transcribe-audio`, `oatda-translate-audio`
