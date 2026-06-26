# Discord OAuth Dashboard Patterns

Use this reference when building a real dashboard login flow for Discord bot administration.

## Core Model

Prefer:
- Discord OAuth for identity
- server-side session storage or signed cookies
- guild-level authorization checks on every privileged route

## Required OAuth Pieces

- `DISCORD_CLIENT_ID`
- `DISCORD_CLIENT_SECRET`
- `DISCORD_REDIRECT_URI`
- scopes such as `identify` and `guilds`

## Safe Rules

- never expose the client secret to the frontend
- verify the OAuth callback state value
- map authenticated users to guild admin/manage permissions before allowing config writes
- keep session expiration and logout behavior explicit

## Production Expectations

Production should use durable sessions, HTTPS, secure cookies, CSRF protection, and stricter permission checks.
Prefer fetching the user's guild list and verifying they have sufficient rights in the target guild before allowing dashboard access.
