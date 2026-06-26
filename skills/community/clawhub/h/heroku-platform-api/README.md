# 🟣 Heroku Platform API Skill

An [OpenClaw](https://openclaw.ai) skill for managing the full Heroku application lifecycle via the Platform API v3 — zero CLI dependency, pure HTTPS.

[![ClawHub](https://img.shields.io/badge/ClawHub-heroku--platform--api-blueviolet)](https://clawhub.ai/imucyou/heroku-platform-api)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](https://opensource.org/license/mit-0)

## What It Does

This skill teaches your OpenClaw agent to manage Heroku apps using `curl` and `jq` — no Heroku CLI required. Every operation is a plain HTTPS request that can be audited, replayed, and integrated into CI/CD pipelines.

**Covers:** apps, dynos, config vars, releases, rollbacks, builds, add-ons, domains, SSL, logs, pipelines, promotions, Postgres backups, webhooks, review apps, rate limits, error handling, and CI/CD integration.

## Requirements

| Requirement | Detail |
|---|---|
| `HEROKU_API_KEY` | Heroku API token ([generate here](https://dashboard.heroku.com/account)) |
| `HEROKU_PERMISSION` | `readonly` (default) or `full` |
| `curl` | HTTP client |
| `jq` | JSON processor |

All requirements are declared in the SKILL.md frontmatter metadata so ClawHub's security analysis can verify them before install.

## Install

```bash
# Via ClawHub CLI
clawhub install imucyou/heroku-platform-api

# Or via OpenClaw native command
openclaw skills install imucyou/heroku-platform-api
```

## Setup

```bash
# 1. Set your Heroku API token
export HEROKU_API_KEY="your-token-here"

# 2. Choose permission mode (optional — defaults to readonly)
export HEROKU_PERMISSION="readonly"    # read-only, safe for exploration
# export HEROKU_PERMISSION="full"     # enables writes with confirmation prompts
```

**Recommended:** use a scoped OAuth token instead of the global dashboard key.

```bash
# Create a read-only scoped token
heroku authorizations:create --scope read --description "openclaw-heroku-readonly"

# Upgrade to write scope only when needed
heroku authorizations:create --scope read,write --description "openclaw-heroku-full"
```

Never use a `global`-scoped token with this skill.

## Permission System

The skill enforces a two-layer safety model:

**Readonly mode** (default) — all write operations are blocked entirely. No prompts, no execution.

**Full mode** — GET requests run freely; every POST/PATCH/DELETE requires interactive confirmation before execution:

```
🔔 Confirm operation:
   App:      my-app-staging
   Action:   PATCH /apps/my-app-staging/config-vars
   Payload:  {"RAILS_ENV":"production"}
→ Proceed? (yes/no)
```

**Non-interactive environments** (CI, autonomous agents) — write operations fail closed by default. To explicitly opt in:

```bash
export HEROKU_NONINTERACTIVE_WRITES="i-accept-the-risk"
```

## Security

| Property | Value |
|---|---|
| Endpoints contacted | `api.heroku.com`, `postgres-api.heroku.com` only |
| Local files read | None |
| Local files written | `STATUS.md` (only in multi-agent orchestration mode) |
| Install footprint | Instruction-only — no code downloaded or executed at install |
| Credential declared | `HEROKU_API_KEY` as `primaryEnv` in metadata |
| `always` | `false` — skill is not auto-loaded |

**Trust statement:** by using this skill, API requests and their payloads (including config var values) are transmitted to Heroku's API. No data is sent anywhere else.

## Usage Examples

Once installed, just ask your OpenClaw agent in natural language:

- *"List all my Heroku apps"*
- *"Show me the config vars for my-app-staging"*
- *"Scale web dynos to 3 on my-app-production"* (requires `HEROKU_PERMISSION=full`)
- *"Show me the last 5 releases for my-app-staging"*
- *"Read the web logs for my-app-production"*
- *"Create a Postgres backup for my-app-production"*
- *"Rollback my-app-staging to v42"* (requires `HEROKU_PERMISSION=full`)

The agent will select the correct API endpoints, apply permission checks, and ask for confirmation on any write operation.

## Endpoints Reference

| Resource | Method | Endpoint |
|---|---|---|
| App info | GET | `/apps/{app}` |
| Config vars | GET / PATCH | `/apps/{app}/config-vars` |
| Formation | GET / PATCH | `/apps/{app}/formation` |
| Dynos | GET / POST / DELETE | `/apps/{app}/dynos` |
| Releases | GET / POST | `/apps/{app}/releases` |
| Builds | GET / POST | `/apps/{app}/builds` |
| Add-ons | GET / POST / PATCH / DELETE | `/apps/{app}/addons` |
| Domains | GET / POST / DELETE | `/apps/{app}/domains` |
| Log sessions | POST | `/apps/{app}/log-sessions` |
| Webhooks | POST | `/apps/{app}/webhooks` |
| Pipelines | GET / POST | `/pipelines` |
| Promotions | POST | `/pipeline-promotions` |
| SSL/SNI | GET / POST | `/apps/{app}/sni-endpoints` |

## Contributing

1. Fork this repo
2. Create a feature branch
3. Edit `SKILL.md`
4. Test with `clawhub publish --dry-run`
5. Open a Pull Request

## License

[MIT-0](https://opensource.org/license/mit-0) — use freely, no attribution required.
