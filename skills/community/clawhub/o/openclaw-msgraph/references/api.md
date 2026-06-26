# Microsoft Graph API Reference

## Auth

| Setting | Value |
|---|---|
| Client ID | YOUR_CLIENT_ID_HERE |
| Tenant | consumers (personal Microsoft accounts) |
| Auth URL | `https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize` |
| Token URL | `https://login.microsoftonline.com/consumers/oauth2/v2.0/token` |
| Redirect URI | `http://localhost:8765/callback` |
| Scopes | `Mail.ReadWrite Calendars.ReadWrite offline_access User.Read` |

## Token File

Stored at `~/.openclaw/msgraph-tokens.json` (mode 0600). Contains:
- `access_token` — Bearer token for API calls
- `refresh_token` — Long-lived token for renewal
- `expires_at` — Unix timestamp of access token expiry
- `expires_in` — Seconds until expiry (from last refresh)

## Key Endpoints

### Mail

| Operation | Endpoint |
|---|---|
| List inbox | `GET /me/mailFolders/inbox/messages` |
| List folder | `GET /me/mailFolders/{folderId}/messages` |
| Get message | `GET /me/messages/{id}` |
| Move message | `POST /me/messages/{id}/move` → `{"destinationId": "..."}` |
| List folders | `GET /me/mailFolders` |
| Search | `GET /me/messages?$search="query"` |
| Mark read | `PATCH /me/messages/{id}` → `{"isRead": true}` |

**Well-known folder names** (usable as IDs directly):
`inbox`, `drafts`, `sentitems`, `deleteditems`, `junk`, `archive`, `outbox`

### Calendar

| Operation | Endpoint |
|---|---|
| List events (view) | `GET /me/calendarView?startDateTime=...&endDateTime=...` |
| Get event | `GET /me/events/{id}` |
| Create event | `POST /me/events` |
| List calendars | `GET /me/calendars` |
| List in calendar | `GET /me/calendars/{id}/calendarView` |

**Event create payload example:**
```json
{
  "subject": "Team Sync",
  "start": {"dateTime": "2026-03-10T10:00:00", "timeZone": "America/New_York"},
  "end":   {"dateTime": "2026-03-10T11:00:00", "timeZone": "America/New_York"},
  "location": {"displayName": "Zoom"},
  "body": {"contentType": "text", "content": "Weekly sync"},
  "attendees": [
    {"emailAddress": {"address": "someone@example.com"}, "type": "required"}
  ]
}
```

## Common Query Parameters

| Param | Purpose | Example |
|---|---|---|
| `$top` | Limit results | `$top=20` |
| `$orderby` | Sort | `$orderby=receivedDateTime desc` |
| `$select` | Fields to return | `$select=id,subject,from` |
| `$search` | OData search | `$search="meeting notes"` |
| `$filter` | OData filter | `$filter=isRead eq false` |

## Error Handling

| HTTP Code | Meaning | Action |
|---|---|---|
| 401 | Unauthorized | Re-run `python auth.py login` |
| 403 | Insufficient scope | Re-auth; check scopes |
| 404 | Resource not found | Check ID |
| 429 | Rate limited | Wait and retry |

On 401, `get_access_token()` will attempt refresh automatically. If refresh also fails, it exits with instructions to re-login.

## PKCE Flow Summary

1. Generate `code_verifier` (random 64-char URL-safe string)
2. `code_challenge = BASE64URL(SHA256(code_verifier))` (no padding)
3. Redirect user to auth URL with `code_challenge_method=S256`
4. After login, Microsoft redirects to `redirect_uri?code=...&state=...`
5. Exchange `code` + `code_verifier` for tokens at token URL
6. Store `access_token`, `refresh_token`, `expires_at`
