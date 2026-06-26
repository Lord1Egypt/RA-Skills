# Dashboard and API Patterns

Use this reference when a Discord bot needs a companion HTTP API, admin dashboard, webhook receiver, or shared backend.

## Default Architecture

Prefer a split like:
- bot runtime handles Discord interactions
- API runtime handles HTTP routes, OAuth, webhooks, and dashboard auth
- shared storage layer holds guild config, tickets, moderation data, and integration state

## Safe Defaults

- keep bot token out of the web client
- separate public routes from admin routes
- authenticate admin routes before exposing guild controls
- validate Discord IDs and user authorization on every mutating route
- log integration-side failures cleanly

## Good First API Endpoints

- `GET /health`
- `GET /guilds/:guildId/settings`
- `PUT /guilds/:guildId/settings`
- `GET /dashboard/guilds/:guildId/settings`
- `PUT /dashboard/guilds/:guildId/settings`
- `POST /webhooks/...` for external integrations

## Auth Guidance

For a real dashboard, prefer Discord OAuth for user identity and session auth.
For starter code, clearly mark any in-memory session storage as development-grade.

## Storage Guidance

Use one shared database when the bot and API need the same state.
Define ownership of writes clearly to avoid race conditions.
Use a shared config accessor layer when both bot and API mutate guild settings.
