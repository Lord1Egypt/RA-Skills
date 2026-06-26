# Advanced Setup

Use this page only when the default wizard flow is not enough.

Default path:

1. Install with `npx -y clawhub install openclaw-growth-engineer`
2. Bootstrap once with `bash skills/openclaw-growth-engineer/scripts/bootstrap-openclaw-workspace.sh`
3. Run `npx -y @analyticscli/growth-engineer wizard --connectors`
4. For connector setup, run `npx -y @analyticscli/growth-engineer wizard --connectors github,revenuecat,paddle,seo,sentry,asc`
5. Run `node scripts/openclaw-growth-start.mjs --config data/openclaw-growth-engineer/config.json`

## Secrets

- Keep secrets out of repo files and out of `config.json`.
- Prefer the OpenClaw runtime or secret store for secret injection.
- Use raw env vars only when your OpenClaw setup does not already manage them for you.
- The exact env names live in `config.secrets` and in [Required Secrets](required-secrets.md).

## Connector Overrides

- Built-in source keys are `analytics`, `revenuecat`, `paddle`, `seo`, `sentry`, `coolify`, and `feedback`; `feedback` is part of the AnalyticsCLI/custom feedback source, not a separate primary setup connector.
- Extra mobile connectors go into `sources.extra[]`.
- Prefer `mode=file` for maximum stability.
- Use `mode=command` when the command deterministically returns JSON.
- Put Sentry Cloud and self-hosted GlitchTip accounts under `sources.sentry.accounts[]` when they expose the Sentry-compatible API. Treat ASC CLI as the ASC / App Store Connect connector, not as a generic extra.

Useful extras:

- `app-store-reviews`
- `play-console`
- `firebase-crashlytics`

## Delivery Modes

- `actions.mode = "issue"` creates implementation-ready GitHub issues.
- `actions.mode = "pull_request"` creates draft PRs plus `.openclaw/proposals/...` files.

## Scheduling

- One-shot run: `node scripts/openclaw-growth-runner.mjs --config data/openclaw-growth-engineer/config.json`
- Continuous loop: `node scripts/openclaw-growth-runner.mjs --config data/openclaw-growth-engineer/config.json --loop`
- Preflight only: `node scripts/openclaw-growth-preflight.mjs --config data/openclaw-growth-engineer/config.json --test-connections`

## Schema And Examples

- [Setup And Scheduling](setup-and-scheduling.md)
- [Required Secrets](required-secrets.md)
- [Input Schema](input-schema.md)
