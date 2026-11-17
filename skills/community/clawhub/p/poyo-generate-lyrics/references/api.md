# PoYo Generate Lyrics API Reference

## Endpoints

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Music detail: `GET https://api.poyo.ai/api/generate/detail/music`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/generate-lyrics>
- Detail docs: <https://docs.poyo.ai/api-manual/music-series/query-music-detail>
- Webhook docs: <https://docs.poyo.ai/api-manual/music-series/music-webhook>

## Authentication

Send `Authorization: Bearer $POYO_API_KEY` and `Content-Type: application/json`. Manage keys at <https://poyo.ai/dashboard/api-key>.

## Request Schema

- `model`: required; use `generate-lyrics`.
- `input.prompt`: required; describe the theme, mood, style, or story in no more than 200 words.
- `callback_url`: optional webhook URL.

## Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer $POYO_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "generate-lyrics",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "An uplifting indie-pop song about rebuilding confidence after moving to a new city, with a concise chorus and vivid nighttime imagery"
    }
  }'
```

## Result Handling

- Save `data.task_id` from the submit response.
- Query the music detail endpoint when polling.
- A completed `generate-lyrics` result can include `title` and `text` fields.
- Use the returned text as input to a later music-generation request when appropriate.
