# PoYo Boost Music Style API Reference

## Endpoints

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Music detail: `GET https://api.poyo.ai/api/generate/detail/music`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/boost-music-style>
- Detail docs: <https://docs.poyo.ai/api-manual/music-series/query-music-detail>
- Webhook docs: <https://docs.poyo.ai/api-manual/music-series/music-webhook>

## Authentication

Send `Authorization: Bearer $POYO_API_KEY` and `Content-Type: application/json`. Manage keys at <https://poyo.ai/dashboard/api-key>.

## Request Schema

- `model`: required; use `boost-music-style`.
- `input.content`: required; use concise genre, mood, instrument, tempo, or production descriptors.
- `callback_url`: optional webhook URL.

## Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer $POYO_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "boost-music-style",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "content": "Cinematic, hopeful, orchestral, restrained percussion"
    }
  }'
```

## Result Handling

- Save `data.task_id` from the submit response.
- Query music detail for polling or wait for the callback.
- Review the enhanced description and pass it to Generate Music only when it preserves the intended genre, mood, and instrumentation.
