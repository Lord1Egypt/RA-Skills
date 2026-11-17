# REST fallback

Without the AppGoat MCP server, call the API directly. Base URL `https://api.appgoat.ai/v1`,
header `x-api-key: $APPGOAT_API_KEY` (create a key at https://dash.appgoat.ai). Responses are
`{ "data": …, "meta": { "credits_used", "credits_remaining", … } }`; errors are
`{ "error": { "code", "message", "hint", "approve_url"? } }` - read `hint`.

| MCP tool | REST call |
|---|---|
| `list_connections` | `GET /connections` (free) |
| `get_app` | `GET /apps/{app}?include=markets` |
| `read_connection` what=listing | `GET /connections/{id}/listings?app={app}&locale=de-DE` |
| `keyword_research` | `GET /keywords?qs=term1,term2&store=apple&country=de&include=related` (5 credits per seed with related) or `&app={app}` (1 per term) |
| `propose_action` | `POST /actions` with `"dry_run": true, "source": "playbook:localization-push"` (free) |
| `apply_action` | `POST /actions/{id}/approve` (1 credit when applied) |
| `reject_action` | `POST /actions/{id}/reject` (free) |

Listing: `{ app, locale, fields: { name, subtitle, description, keywords, promotional_text, whats_new, … }, editable: [...], notes: [...], version, version_state }`
(Play: `title`, `short_description`, `full_description`, `video`).

```bash
CON=con_… APP=1234567890
curl -s -G -H "x-api-key: $APPGOAT_API_KEY" "https://api.appgoat.ai/v1/connections/$CON/listings" \
  -d app=$APP -d locale=de-DE | jq '.data | {fields, editable, notes}'

curl -s -H "x-api-key: $APPGOAT_API_KEY" -H "content-type: application/json" https://api.appgoat.ai/v1/actions \
  -d '{"type":"keywords.set","connection":"'$CON'","dry_run":true,"source":"playbook:localization-push",
       "params":{"app":"'$APP'","locale":"de-DE","mode":"replace","keywords":"gewohnheit,routine,ziel"}}' \
  | jq '.data | {id, diff, guardrail}'
```
