# PoYo ElevenLabs TTS Turbo 2.5 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Task status: use the standard PoYo task status endpoint documented by PoYo.
- Source docs: <https://docs.poyo.ai/api-manual/music-series/elevenlabs-tts-turbo-2-5>
- Model page: <https://poyo.ai/models/elevenlabs-tts-turbo-2-5>

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

- `elevenlabs-tts-turbo-2-5`: text-to-speech generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `text` string, required
- `voice` string, optional
- `stability` number from `0` to `1`, optional
- `similarity_boost` number from `0` to `1`, optional
- `style` number from `0` to `1`, optional
- `speed` number from `0.7` to `1.2`, optional
- `timestamps` boolean, optional
- `previous_text` string, optional
- `next_text` string, optional
- `language_code` string, optional
- `apply_text_normalization` string, optional: `auto`, `on`, or `off`

Always verify current field support in the PoYo docs before relying on model-specific options.

## Product Voiceover Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "elevenlabs-tts-turbo-2-5",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "text": "Welcome to NovaDesk. Your workspace is ready, your calendar is synced, and your first customer briefing starts in ten minutes.",
      "voice": "Rachel",
      "speed": 1.08,
      "stability": 0.55,
      "similarity_boost": 0.78,
      "style": 0.12,
      "timestamps": false,
      "apply_text_normalization": "auto"
    }
  }'
```

## Localized Notification Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "elevenlabs-tts-turbo-2-5",
    "input": {
      "text": "Bonjour, votre commande est prete. Merci de presenter votre code de retrait a l accueil.",
      "voice": "Aria",
      "language_code": "fr",
      "stability": 0.6,
      "similarity_boost": 0.75,
      "speed": 1,
      "timestamps": true,
      "apply_text_normalization": "auto"
    }
  }'
```

## Long-Form Continuity Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "elevenlabs-tts-turbo-2-5",
    "input": {
      "previous_text": "The city lights faded behind the train.",
      "text": "Mira lowered her voice and said, keep the map close. By sunrise, everyone will be looking for it.",
      "next_text": "The carriage fell silent as the tunnel opened ahead.",
      "voice": "Sarah",
      "stability": 0.42,
      "similarity_boost": 0.82,
      "style": 0.35,
      "speed": 0.94,
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

- Keep the first request simple: `text`, `voice`, and `apply_text_normalization`.
- Add `previous_text` and `next_text` when splitting long-form narration.
- Request `timestamps` only when the product needs alignment metadata.
- Keep private scripts, prompts, callback URLs, task ids, and generated audio URLs out of logs unless explicitly allowed by the product policy.
