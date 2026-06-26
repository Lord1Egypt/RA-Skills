# WHOOP API (quick reference)

This skill uses WHOOP’s **official** OAuth + API.

## OpenAPI spec

The public OpenAPI spec is downloadable from the WHOOP API docs.

## Base URLs

- API server (from OpenAPI `servers[0].url`):
  - `https://api.prod.whoop.com/developer`

## OAuth (Authorization Code)

From OpenAPI `components.securitySchemes.OAuth.flows.authorizationCode`:

- Authorization URL:
  - `https://api.prod.whoop.com/oauth/oauth2/auth`
- Token URL:
  - `https://api.prod.whoop.com/oauth/oauth2/token`

### Scopes (common)

Typical read scopes:

- `read:recovery`
- `read:sleep`
- `read:cycles`
- `read:workout`
- `read:profile`
- `read:body_measurement`

Request the minimum necessary, but most “daily summary” use cases want at least recovery + sleep + cycles.

## Common endpoints (v2)

See the live API docs for complete details. Common calls used by the scripts:

- Recovery collection: `GET /v2/recovery`
- Sleep collection: `GET /v2/activity/sleep`
- Cycle collection: `GET /v2/cycle`
- Workout collection: `GET /v2/activity/workout`
- Basic profile: `GET /v2/user/profile/basic`
- Body measurements: `GET /v2/user/measurement/body`
- Revoke access: `DELETE /v2/user/access`

## Pagination

WHOOP collection endpoints are paginated. Prefer:

- fetch “recent N days” by query parameters (when supported)
- otherwise page until you cover the requested date range

## Rate limiting

Handle HTTP 429 by backing off (sleep + retry). If `Retry-After` exists, honor it.
