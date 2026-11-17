# PoYo Add Vocals API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Music detail: `GET https://api.poyo.ai/api/generate/detail/music`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/add-vocals>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/music-series/add-vocals.json>
- Music detail docs: <https://docs.poyo.ai/api-manual/music-series/query-music-detail>
- Music webhook docs: <https://docs.poyo.ai/api-manual/music-series/music-webhook>
- Model page: <https://poyo.ai/models/add-vocals>

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

- `add-vocals`: generates vocals over uploaded instrumental audio.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Required `input` fields:

- `upload_url` string URI; public instrumental audio URL
- `prompt` string; lyrics or vocal direction
- `title` string; documented maximum is 100 characters
- `style` string; desired vocal or music style
- `negative_tags` string; unwanted styles or vocal traits

Optional `input` fields:

- `mv` string; supported values include `V4_5PLUS`, `V5`, and `V5_5`
- `vocal_gender` string; supported values include `m` and `f`
- `style_weight` number from `0` to `1`
- `weirdness_constraint` number from `0` to `1`
- `audio_weight` number from `0` to `1`

Always verify current field support in the PoYo docs before relying on model-specific options.

## Submit Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "add-vocals",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "upload_url": "https://example.com/audio/instrumental.mp3",
      "prompt": "A bright chorus about starting again after a long night",
      "title": "Morning Light",
      "style": "pop, clean vocal, upbeat",
      "negative_tags": "harsh shouting, distorted vocal",
      "mv": "V4_5PLUS",
      "vocal_gender": "f",
      "style_weight": 0.7
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
    "created_time": "2026-07-06T08:00:00"
  }
}
```

## Result Retrieval Notes

- Save `data.task_id` immediately after submission.
- Use the music detail endpoint for generated music task results.
- Use `callback_url` for production queues and long-running user workflows.
- Treat `finished` and `failed` as terminal states when receiving callbacks.
- Download returned audio and cover image files before relying on them long term.

## Practical Guidance

- Use a public instrumental audio URL; upload local files to trusted storage before submitting.
- Keep the vocal prompt clear enough to guide lyrics, delivery, or intended scene.
- Use negative tags to avoid unwanted styles, vocal texture, or pacing.
- Keep private recordings, lyrics, customer names, callback URLs, and generated audio URLs out of logs.
