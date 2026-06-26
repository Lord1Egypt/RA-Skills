# API Contract Snapshot (Ops-Focused)

## Envelope
Success:
```json
{ "success": true, "data": {} }
```
Error:
```json
{ "success": false, "error": { "code": "...", "message": "...", "details": {} } }
```

## Auth and Registration
- `POST /api/v1/auth/permit/challenge`
- `POST /api/v1/auth/permit/solve`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/verify`
- `POST /api/v1/auth/admin/login`

## Messaging
- `POST /api/v1/messages/send`
- `GET /api/v1/messages/inbox`
- `GET /api/v1/messages/sent`
- `GET /api/v1/messages/:id`
- `POST /api/v1/messages/:id/ack`

## Admin
- `GET /api/v1/admin/stats`
- `GET /api/v1/admin/accounts`
- `GET /api/v1/admin/messages`
- `POST /api/v1/admin/registration/override-permit`
- `GET /api/v1/admin/registration/events`

## Auth Header Options
- `Authorization: Bearer <jwt>`
- `Authorization: ApiKey <lm_...>`
