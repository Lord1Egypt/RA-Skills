# Meo Mai Moi API Reference

## Authentication

Use Sanctum personal access tokens for programmatic access.

To start using Meo Mai Moi through an agent, the user must manually sign in or register at https://meo-mai-moi.com, create a personal API key/token at https://meo-mai-moi.com/developer, and provide it to the agent securely, preferably through a local env file or secret manager. Do not ask users to paste API keys into public chats, shared prompts, GitHub issues, logs, or committed files.

Official docs:

- User/developer docs: https://meo-mai-moi.com/docs
- API integration guide: https://meo-mai-moi.com/docs/api-integration.html
- Project page: https://project.meo-mai-moi.com

Required headers:

- `Authorization: Bearer <token>`
- `Accept: application/json`

Practical env pattern:

```bash
set -a
source /path/to/meo-mai-moi.env
set +a
```

Example env file:

```env
API_KEY=...
```

Minimal identity/auth check:

```bash
curl -sS \
  -H "Authorization: Bearer $API_KEY" \
  -H "Accept: application/json" \
  https://meo-mai-moi.com/api/users/me
```

## Stable contract assumptions

Treat `/api/*` as the active v1 contract.

Documented pet-management contract:

- `GET /api/my-pets`
- `GET /api/my-pets/sections`
- `POST /api/pets`
- `GET /api/pets/{pet}`
- `PUT /api/pets/{pet}`
- `PUT /api/pets/{pet}/status`
- `DELETE /api/pets/{pet}`
- `POST /api/pets/{pet}/weights`
- `PUT /api/pets/{pet}/weights/{weight}`
- `DELETE /api/pets/{pet}/weights/{weight}`
- `POST /api/pets/{pet}/medical-records`
- `PUT /api/pets/{pet}/medical-records/{record}`
- `DELETE /api/pets/{pet}/medical-records/{record}`
- `POST /api/pets/{pet}/vaccinations`
- `PUT /api/pets/{pet}/vaccinations/{record}`
- `POST /api/pets/{pet}/vaccinations/{record}/renew`
- `DELETE /api/pets/{pet}/vaccinations/{record}`
- `POST /api/pets/{pet}/microchips`
- `PUT /api/pets/{pet}/microchips/{microchip}`
- `DELETE /api/pets/{pet}/microchips/{microchip}`

Do not assume `PATCH /api/pets/{pet}` is supported.

## Abilities

Current PAT ability enforcement:

- `read` for `GET /api/users/me`, `GET /api/my-pets`, `GET /api/my-pets/sections`
- `create` for pet creation and nested record creation
- `update` for pet updates, status updates, and nested record updates
- `delete` for pet deletion and nested record deletion

Session-authenticated browser requests are broader than PAT-backed requests. Do not assume a browser capability is a stable PAT contract.

## Response conventions

Success usually looks like:

```json
{
  "success": true,
  "data": {},
  "message": "Optional human message"
}
```

Error usually looks like:

```json
{
  "success": false,
  "data": null,
  "message": "Human-readable summary",
  "error": "Optional machine-ish code",
  "errors": {
    "field": ["Validation message"]
  }
}
```

Exception:

- `204 No Content` intentionally has an empty body.

## Useful known details

- `POST /api/pets` requires `country` as ISO 3166-1 alpha-2, for example `VN`.
- `GET /api/my-pets` and `GET /api/my-pets/sections` include compact `health_summary` data for list views.
- Some pet-health read endpoints are public or optional-auth. That does not make write operations public.

## Rate limits and quotas

Expect both minute throttles and a daily quota.

- Authenticated API group: production default is `60/min`
- Public API group: production default is `30/min`
- Regular users: `1000 requests/day` by default
- Premium users: unlimited
- Daily quota window resets at UTC day boundary

Over-quota responses use `429` and the error code `API_DAILY_QUOTA_EXCEEDED`.

## Safe usage pattern

1. Read first.
2. Confirm identifiers and current state.
3. Write the smallest change needed.
4. Re-read to verify the result.
5. If a route or payload is undocumented, say it is undocumented before using it.

## Handy examples

List my pets:

```bash
curl -sS \
  -H "Authorization: Bearer $API_KEY" \
  -H "Accept: application/json" \
  https://meo-mai-moi.com/api/my-pets
```

Get one pet:

```bash
curl -sS \
  -H "Authorization: Bearer $API_KEY" \
  -H "Accept: application/json" \
  https://meo-mai-moi.com/api/pets/123
```

Create a weight record:

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"weight_kg":4.2,"record_date":"2026-04-26"}' \
  https://meo-mai-moi.com/api/pets/123/weights
```

The live API currently validates `weight_kg` and `record_date` for weight writes. Do not send `weight` or `recorded_at` unless the server contract changes and you re-verify it.
