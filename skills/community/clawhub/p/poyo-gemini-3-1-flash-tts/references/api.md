# PoYo Gemini 3.1 Flash TTS API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Task status: use the standard PoYo task status endpoint documented by PoYo.
- Source docs: <https://docs.poyo.ai/api-manual/music-series/gemini-3-1-flash-tts>
- Model page: <https://poyo.ai/models/gemini-3-1-flash-tts>

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

- `gemini-3-1-flash-tts`: text-to-speech generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `text` string, required
- `style_instructions` string, optional
- `voice` string, optional for single-speaker synthesis
- `language_code` string, optional
- `speakers` array, optional, exactly two speaker objects when used
- `temperature` number from `0` to `2`, optional
- `output_format` string, optional: `mp3`, `wav`, or `ogg_opus`

When using `speakers`:

- Provide exactly two speaker objects.
- Each speaker object includes `speaker_id` and `voice`.
- Each `speaker_id` should contain only letters, numbers, and underscores.
- Prefix dialogue lines in `text` with matching speaker ids.
- Top-level `voice` is ignored when `speakers` is set.

Always verify current field support in the PoYo docs before relying on model-specific options.

## Single Speaker Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gemini-3-1-flash-tts",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "text": "Good morning, team. [short pause] The release is ready, and the customer demo starts in ten minutes.",
      "style_instructions": "Warm product narrator with clear pacing.",
      "voice": "Kore",
      "temperature": 1,
      "output_format": "mp3"
    }
  }'
```

## Multilingual Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gemini-3-1-flash-tts",
    "input": {
      "text": "English: Your order is ready for pickup. Spanish: Su pedido esta listo para recoger. French: Votre commande est prete a etre retiree.",
      "style_instructions": "Friendly store assistant voice, natural and concise.",
      "voice": "Zephyr",
      "language_code": "English (US)",
      "temperature": 1,
      "output_format": "wav"
    }
  }'
```

## Two Speaker Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gemini-3-1-flash-tts",
    "input": {
      "text": "Host: Welcome back to Launch Notes. [laughing] Today the build passed. Guest: Great news. Let us keep the update clear and calm for users.",
      "style_instructions": "Conversational podcast tone with distinct speaker energy.",
      "speakers": [
        {
          "speaker_id": "Host",
          "voice": "Charon"
        },
        {
          "speaker_id": "Guest",
          "voice": "Kore"
        }
      ],
      "temperature": 1,
      "output_format": "ogg_opus"
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
    "created_time": "2026-06-29T08:00:00"
  }
}
```

## Result Retrieval Notes

- Save `data.task_id` immediately after submission.
- Use the standard PoYo task status endpoint for generated speech results.
- Use `callback_url` for production queues and long-running user workflows.
- Treat `finished` and `failed` as terminal states when receiving callbacks.
- Generated speech is returned in task `files` with an audio file type when the task succeeds.

## Practical Guidance

- Use top-level `voice` for single-speaker output.
- Use `speakers` only when the user needs two distinct voices.
- Match `speaker_id` values exactly to dialogue prefixes in `text`.
- Keep private scripts, prompts, callback URLs, task ids, and generated audio URLs out of logs unless explicitly allowed by the product policy.
