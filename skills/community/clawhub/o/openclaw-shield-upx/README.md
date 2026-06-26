# OpenClaw Shield

Security monitoring skill for the OpenClaw Shield plugin by [UPX](https://www.upx.com).

## What it does

Teaches your agent to use the Shield plugin — check health, query events, inspect the redaction vault, and manage security cases.

- Run `openclaw shield status`, `logs`, `flush`, `vault show`, and `cases` commands
- Call RPCs for programmatic access (`shield.events_recent`, `shield.events_summary`, `shield.cases_list`, etc.)
- Triage and resolve cases with categorized resolution and root cause
- Set up automated case monitoring via `openclaw shield monitor --on`
- Quick case check with `/shieldcases` (no agent tokens used)
- Answer questions about Shield's privacy model and subscription status

## Requirements

- [OpenClaw Shield plugin](https://www.npmjs.com/package/@upx-us/shield) installed and activated
- Active Shield subscription from [UPX](https://upx.com) — [start a free 30-day trial](https://www.upx.com/en/lp/openclaw-shield-upx)

## Install

This skill is bundled with the Shield plugin. Install the plugin and the skill is available automatically:

```bash
openclaw plugins install @upx-us/shield
openclaw shield activate <YOUR_KEY>
openclaw gateway restart
```

## Links

- **Plugin (npm)**: [@upx-us/shield](https://www.npmjs.com/package/@upx-us/shield)
- **Skill (ClawHub)**: [openclaw-shield-upx](https://clawhub.ai/brunopradof/openclaw-shield-upx)
- **Dashboard**: [uss.upx.com](https://uss.upx.com)

## About

Made by [UPX](https://upx.com) — cybersecurity engineering for critical environments.
