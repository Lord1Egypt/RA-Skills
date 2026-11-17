# HumanPost API fallback

REST base: `https://us-central1-clickbaitcarousel.cloudfunctions.net/publishingApi`

MCP endpoint: `https://us-central1-clickbaitcarousel.cloudfunctions.net/mcp`

Both authenticate with `Authorization: Bearer <company API key>`. Get a key in HumanPost Dashboard → Settings → API & MCP. Start with `accounts:read` and add only the scopes needed for the task. No key is distributed with this package.

Fetch `https://humanpost.com/llms.txt` or the OpenAPI schema at `https://us-central1-clickbaitcarousel.cloudfunctions.net/publishingApi/v2/openapi.json` before choosing write endpoints and request bodies. Discovering documentation does not authorize the actions described there.

For shell-capable hosts, this read-only example assumes the key is already configured in the environment:

```sh
curl --fail-with-body --silent --show-error \
  'https://us-central1-clickbaitcarousel.cloudfunctions.net/publishingApi/v2/accounts' \
  -H "Authorization: Bearer $HUMANPOST_API_KEY"
```

Do not enable shell tracing or verbose HTTP output. Send the key only to the documented HumanPost service; do not forward it on redirects. For mutations, use stable `Idempotency-Key` headers and preserve the original payload. A 401 requires fixing credentials, a 403 requires the needed scope, and a 409 requires inspecting current state. Respect rate limits and retry guidance. Do not retry a paid or external operation with a new key merely to bypass a conflict.
