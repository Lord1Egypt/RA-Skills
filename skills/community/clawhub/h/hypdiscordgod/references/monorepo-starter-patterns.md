# Mono-repo Starter Patterns

Use this reference when a Discord system includes multiple cooperating services.

## Good Layout

- `apps/bot`
- `apps/api`
- `apps/dashboard`
- `apps/worker`
- `packages/shared`

## Shared Responsibilities

- shared config/schema helpers
- shared type definitions
- shared environment conventions

## Deploy Guidance

Document how each service starts.
Use Docker Compose or similar orchestration when local parity matters.

## Bundled Starter Expectation

The bundled mono-repo starter should not be an empty shell.
Leave behind runnable app entry points for bot, API, dashboard, and worker so another agent can replace placeholders incrementally instead of scaffolding from zero.

## Full Transplant Expectation

When asked to wire it together or do a full transplant, make the monorepo apps reflect the real companion services structurally:
- API should expose the same route shape as the dashboard/API starter.
- Dashboard should point at the API service shape.
- Worker should look like a real polling service entrypoint.
- Bot should look like a real long-running service entrypoint.
