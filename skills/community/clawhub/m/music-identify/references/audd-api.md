# AudD API Reference (Summary)

## Endpoint
- POST https://api.audd.io/

## Parameters (multipart/form-data)
- `file`: Audio file to identify (OGG/Opus accepted)
- `api_token`: AudD API key
- `return`: Optional; set to `spotify` to include Spotify metadata

## Response Format (JSON)
- Success with match:
  - `status`: "success"
  - `result`: object with fields such as `title`, `artist`, `album`, and `spotify`
  - `result.spotify.external_urls.spotify`: Spotify URL
- Success with no match:
  - `status`: "success"
  - `result`: null
- Error:
  - `status`: "error"
  - `error`: object with `error_message` (and optionally `error_code`)
