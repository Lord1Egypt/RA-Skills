# hookpipe-skill

OpenClaw / ClawHub skill for [hookpipe](https://github.com/hookpipe/hookpipe) — reliable webhook infrastructure for AI agents.

## Install

```bash
clawhub install hookpipe/hookpipe-skill
```

## What it does

When your agent needs to receive webhooks from Stripe, GitHub, Slack, or other services, this skill provides hookpipe CLI commands for:

- **One-shot setup** — `hookpipe connect stripe --secret whsec_xxx --to http://localhost:18789/webhook`
- **Local dev tunnel** — `hookpipe dev --port 18789 --provider stripe --secret whsec_xxx`
- **Provider discovery** — `hookpipe providers ls` / `hookpipe providers describe stripe --json`
- **Event streaming** — `hookpipe tail --json`

## Why hookpipe + OpenClaw

OpenClaw's gateway loses webhook events during restarts and downtime. hookpipe sits in front of your gateway — it's always online (Cloudflare Workers), accepts webhooks immediately, and retries delivery until your gateway is back.

```
Stripe → hookpipe (always online) → OpenClaw Gateway (can restart freely)
```

## More info

- [hookpipe GitHub](https://github.com/hookpipe/hookpipe)
- [Provider Design Guide](https://github.com/hookpipe/hookpipe/blob/main/packages/providers/DESIGN.md)
