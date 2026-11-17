# GoDaddy API Skill

An agent skill for GoDaddy's current developer platform, built around the official `gddy` CLI for dynamic REST and GraphQL discovery, domains, registration, nameservers, DNS, authentication, and account operations.

Version 2.0.0 also documents the public Domains MCP, official agent integrations, beta Hosting and Email, experimental Platform apps/actions/webhooks/extensions, and Agent Name Service. Verified against gddy v0.2.12 on September 5, 2026. See [coverage and setup](references/agent-platform.md), including current availability limits. The skill supplies instructions; CLI installation and MCP connection setup are separate host operations.

## ClawHub

[View GoDaddy API on ClawHub](https://clawhub.ai/solarx56/skills/godaddy-api)

```bash
openclaw skills install @solarx56/godaddy-api
```

The skill's executable instructions are in [`SKILL.md`](SKILL.md). Detailed API discovery, safety, and retry guidance lives under [`references/`](references/).
