# Troubleshooting

## OAuth redirect_uri mismatch

- Ensure `WHOOP_REDIRECT_URI` **exactly** matches the redirect URI configured in the WHOOP developer dashboard.
- If using `http://127.0.0.1:<port>/callback`, the port must match.

## invalid_scope

- Confirm your app has requested and been granted the scope(s).
- Start with: `read:recovery read:sleep read:cycles`.

## 401 Invalid authorization

- Token expired and refresh failed.
- Re-run `scripts/whoop_oauth_login.py` to re-authorize.

## 429 rate limited

- Back off and retry. Honor `Retry-After` when present.

## Wrong “day” because of timezone

- WHOOP timestamps are typically in ISO-8601; convert to the desired timezone.
- Set `WHOOP_TZ` and use it consistently in fetching + normalization.

## Duplicate sends

- If you schedule messages, store a simple state file (e.g. last_sent_date + hash of message content) outside the token file.
