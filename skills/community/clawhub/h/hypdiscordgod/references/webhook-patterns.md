# Webhook Integration Patterns

Use this reference when a Discord bot project needs inbound webhooks from external services.

## Safe Defaults

- authenticate every webhook route
- verify signatures when the provider supports it
- make handlers idempotent when duplicate delivery is possible
- log failures with enough context to debug retries
- avoid blocking long work in the HTTP request path

## Common Uses

- GitHub/GitLab event notifications
- Stripe/payment updates
- CI/CD deploy notifications
- internal service triggers for bot actions

## Architecture

Prefer:
- API route receives webhook
- validate auth/signature
- normalize payload
- persist or queue event if needed
- bot or worker performs Discord-side action
