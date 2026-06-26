---
name: inbox-manager
version: 1.0.0
description: "Authorize, read, triage, archive, trash, and summarize Gmail inboxes across multiple accounts. Uses Gmail API with OAuth."
allowed-tools: [cron, exec, read, write, edit, web_search]
---

# Inbox Manager

Manage multiple Gmail accounts through a single Google Cloud project. One OAuth client, separate token per account.

## Architecture

```
secrets/inbox/
  client_secret.json            — OAuth 2.0 Desktop client credentials (shared)
  accounts.json                  — {"account@gmail.com": {"label": ..., "token_file": "token-..."}}
  token-account-at-gmail-dot-com.json  — per-account OAuth token

scripts/inbox/
  inbox-auth-final.py           — one-shot OAuth: opens browser, saves token
  inbox-check.py                — read/filter/triage/delete via Gmail API
```

## Adding a new account

1. Run `python3 scripts/inbox-auth-final.py <email>` on machine with browser access
2. Log in to Gmail in the Chromium popup, authorize
3. Token auto-saves to `secrets/inbox/token-<sanitized>.json`
4. `accounts.json` auto-updated

Sanitization: `@` → `-at-`, `.` → `-dot-`

## Gmail API scopes used

- `gmail.readonly` — read messages
- `gmail.modify` — trash, archive, mark read, label

Not used: `gmail.send` / `gmail.compose` (no auto-sending unless explicitly added)

## Operations

### List inbox
```
GET /gmail/v1/users/me/messages?labelIds=INBOX&maxResults=N
GET /gmail/v1/users/me/messages/{id}?format=metadata&metadataHeaders=From,Subject,Date
```

### Search/filter
Use Gmail query syntax via `q` parameter:
- `from:traveloka` — all from sender
- `is:unread` — unread only
- `-from:accounts.google.com` — exclude security alerts
- `after:2026/05/01` — date filter

### Delete/trash
```
POST /gmail/v1/users/me/messages/{id}/trash
```
Batch via `new_batch_http_request()` for bulk operations (100 per batch).

## Cleanup rules (spamforhobo examples)

| Sender | Action | Reason |
|--------|--------|--------|
| Traveloka | Trash | Promo emails |
| Flokk | Trash | Promo emails |
| FossilEra | Trash | Promo emails |
| TIDAL monthly reports | Trash | Old newsletters |
| BloomThis | Trash | Feedback/promo |
| Helpling | Keep | Actual reminders |
| Splitwise | Keep | Balance updates |
| SRX | Keep | Property updates |
| NLB | Keep | Account notifications |

## Security notes

- Tokens contain refresh tokens — treat as sensitive (NEVER commit)
- Google may flag new accounts accessed via CLI-only; use established accounts
- OAuth tokens auto-refresh; no manual reauth needed unless revoked
- 3 security alerts on first auth are normal (Google notifying account owner)
