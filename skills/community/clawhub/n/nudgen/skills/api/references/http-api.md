# Nudgen HTTP API Reference

## Contents

- Source Of Truth
- Authentication
- Base URL
- Endpoint Map
- Request Patterns
- Errors
- Practical Tips

## Source Of Truth

- `https://github.com/Nudgen-Marketing/nudgen-cli/internal/api/client.go`
- `https://github.com/Nudgen-Marketing/nudgen-cli/internal/api/models.go`
- `https://docs.nudgen.net/en/api-references`

Use local source as truth when external docs are incomplete.

## Authentication

Every request uses a Personal Access Token (PAT):

```http
Authorization: Bearer <PAT>
Content-Type: application/json
```

Never hardcode PAT values. Keep calls server-side and load secrets from environment or secure secret storage.

## Base URL

```text
https://app.nudgen.net/api/v1
```

## Endpoint Map

The current CLI integration relies on these endpoint families:

- Identity
  - `GET /user/me`
- Contacts
  - `GET /contacts`
  - `POST /contacts/add`
  - `PATCH /contacts/:id`
  - `DELETE /contacts/:id`
- Campaigns
  - `GET /campaigns`
  - `POST /campaigns`
  - `DELETE /campaigns/:id`
- Stats
  - `GET /dashboard/overview`
- Teams
  - `GET /teams`
  - `POST /teams`
  - `POST /teams/switch`
  - `DELETE /teams/:id`
- Brand config
  - `GET /brand`
  - `POST /brand`
  - `PATCH /brand/:id`
  - `DELETE /brand/:id`
- Affiliate/referral
  - `GET /affiliate/me`
  - `GET /affiliate/analytics`
  - `GET /affiliate/payouts`

## Request Patterns

### Identity check

```bash
curl -sS \
  -H "Authorization: Bearer $NUDGEN_PAT" \
  https://app.nudgen.net/api/v1/user/me
```

### Create contact

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $NUDGEN_PAT" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","name":"Alex","tags":["vip"]}' \
  https://app.nudgen.net/api/v1/contacts/add
```

### Switch active team

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $NUDGEN_PAT" \
  -H "Content-Type: application/json" \
  -d '{"teamId":"team_123"}' \
  https://app.nudgen.net/api/v1/teams/switch
```

### Read overview stats

```bash
curl -sS \
  -H "Authorization: Bearer $NUDGEN_PAT" \
  https://app.nudgen.net/api/v1/dashboard/overview
```

## Errors

- Treat non-2xx responses as actionable failures.
- Parse JSON `{ "error": "..." }` when present.
- Handle `401`/`403` as auth or permission issues.
- Handle `429` with retry and backoff.
- For mutating operations, validate team context before write calls.

## Practical Tips

- Start integration tests with `GET /user/me` to validate auth first.
- Keep API usage in backend/server code paths only.
- Make team-scoped behavior explicit in your service logic.
- For automation scripts, couple API verification with a read endpoint after writes.
