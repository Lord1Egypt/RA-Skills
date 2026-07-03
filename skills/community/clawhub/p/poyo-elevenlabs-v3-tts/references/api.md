# PoYo ElevenLabs V3 TTS API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Task status: use the standard PoYo task status endpoint documented by PoYo.
- Source docs: <https://docs.poyo.ai/api-manual/music-series/elevenlabs-v3-tts>
- Model page: <https://poyo.ai/models/elevenlabs-v3-tts>

## Auth

Send:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Model

- `elevenlabs-v3-tts`: text-to-speech generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `text` string, required
- `voice` string, optional
- `stability` number from `0` to `1`, optional
- `timestamps` boolean, optional
- `language_code` string, optional
- `apply_text_normalization` string, optional: `auto`, `on`, or `off`

Supported voice names documented by PoYo include `Aria`, `Roger`, `Sarah`, `Laura`, `Charlie`, `George`, `Callum`, `River`, `Liam`, `Charlotte`, `Alice`, `Matilda`, `Will`, `Jessica`, `Eric`, `Chris`, `Brian`, `Daniel`, `Lily`, `Bill`, and `Rachel`.

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text To Speech Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "elevenlabs-v3-tts",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "text": "Hello. This is a short test of a production text to speech workflow.",
      "voice": "Rachel",
      "stability": 0.5,
      "timestamps": false,
      "language_code": "en",
      "apply_text_normalization": "auto"
    }
  }'
```

## Timestamp Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "elevenlabs-v3-tts",
    "input": {
      "text": "Every word can include timing data when timestamps are enabled.",
      "voice": "Aria",
      "timestamps": true,
      "apply_text_normalization": "auto"
    }
  }'
```

## Typical Submit Response

```json
{
  "code": 200,
  "data": {
    "task_id": "task_unified_example",
    "status": "not_started",
    "created_time": "2026-06-30T08:00:00"
  }
}
```

## Result Retrieval Notes

- Save `data.task_id` immediately after submission.
- Use the standard PoYo task status endpoint for generated speech results.
- Use `callback_url` for production queues and long-running user workflows.
- Treat `finished` and `failed` as terminal states when receiving callbacks.
- Generated speech is returned in task `files` with an audio file type when the task succeeds.
- If `timestamps` is enabled and returned, timestamp data may be included as a separate file.

## Practical Guidance

- Keep the first request simple: `text`, `voice`, and `apply_text_normalization`.
- Request `timestamps` only when the product needs alignment metadata.
- Keep private scripts, prompts, callback URLs, task ids, timestamp files, and generated audio URLs out of logs unless explicitly allowed by the product policy.
