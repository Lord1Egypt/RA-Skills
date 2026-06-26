# CSRF and Session Persistence Patterns

Use this reference when a Discord dashboard is moving from local-dev auth toward production safety.

## CSRF Protection

Prefer:
- signed, HTTP-only session cookies
- a separate CSRF token exposed to the frontend
- validation on every mutating route

## Session Persistence

Development starters may use in-memory sessions.
Production should persist session state or refresh metadata in durable storage.

## Refresh Tokens

If the OAuth provider and design require refresh handling:
- store refresh tokens securely server-side
- rotate or update stored credentials carefully
- never expose refresh tokens to the browser
