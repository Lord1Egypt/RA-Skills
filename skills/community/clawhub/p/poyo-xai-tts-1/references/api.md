# PoYo xAI TTS 1 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/xai-tts-1>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/music-series/xai-tts-1.json>
- Model page: <https://poyo.ai/models/xai-tts-1>

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

- `xai-tts-1`: text-to-speech generation with expressive delivery controls.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Required `input` fields:

- `text` string, required; length `1-15000` characters

Optional `input` fields:

- `voice` string; supported values include `eve`, `ara`, `rex`, `sal`, and `leo`
- `language_code` string; use `auto` or a supported language code
- `output_format` object
- `output_format.codec` string; supported values include `mp3`, `wav`, `pcm`, `mulaw`, and `alaw`
- `output_format.sample_rate` number; supported values include `8000`, `16000`, `22050`, `24000`, `44100`, and `48000`
- `output_format.bit_rate` number or null; applies to MP3 output

Supported language values include `auto`, `en`, `ar-EG`, `ar-SA`, `ar-AE`, `bn`, `zh`, `fr`, `de`, `hi`, `id`, `it`, `ja`, `ko`, `pt-BR`, `pt-PT`, `ru`, `es-MX`, `es-ES`, `tr`, and `vi`.

Always verify current field support in the PoYo docs before relying on model-specific options.

## Submit Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "xai-tts-1",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "text": "Welcome to the product demo. [pause] <whisper>This line is softer.</whisper> Now back to a clear narration voice.",
      "voice": "eve",
      "language_code": "auto",
      "output_format": {
        "codec": "mp3",
        "sample_rate": 24000,
        "bit_rate": 128000
      }
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
    "created_time": "2026-06-25T10:30:00"
  }
}
```

## Status Query Example

```bash
curl --fail-with-body --request GET \
  --url "https://api.poyo.ai/api/generate/status/task_unified_example" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

## Finished Result Shape

Successful tasks return audio files in the standard PoYo task result shape:

```json
{
  "code": 200,
  "data": {
    "task_id": "task_unified_example",
    "status": "finished",
    "progress": 100,
    "files": [
      {
        "file_url": "https://cdn.poyo.ai/files/task_unified_example/output.mp3",
        "file_type": "audio"
      }
    ],
    "error_message": null
  }
}
```

## Practical Guidance

- Use `auto` for `language_code` unless the user needs an explicit language target.
- Use expressive speech tags only when the requested delivery needs them.
- Choose `mp3` for broad playback compatibility unless the user requests another output codec.
- Save `data.task_id` immediately after submission.
- Use `callback_url` for production queues and longer user workflows.
- Avoid logging API keys, private scripts, callback URLs, or generated audio URLs.
