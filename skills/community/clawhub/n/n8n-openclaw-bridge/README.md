# n8n OpenClaw Bridge

> Turn your OpenClaw agent into a full automation operator. Create, trigger, and manage n8n workflows without ever touching the n8n UI.

## What This Skill Does

Your OpenClaw agent learns how to:
- **Create n8n workflows** from natural language ("set up an automation that emails me when...")
- **Trigger workflows** by sending data to webhooks
- **Monitor executions** and handle failures automatically
- **Manage your n8n instance** — list, activate, deactivate, and debug workflows

## Why You Need This

| Without this skill | With this skill |
|---|---|
| Agent can only read/write files and browse | Agent orchestrates 800+ integrations via n8n |
| Manual workflow creation in n8n UI | "Create a workflow that..." → done |
| No visibility into automation failures | Agent monitors and retries failed executions |
| Separate AI and automation worlds | Unified: Agent thinks, n8n acts |

## Quick Start

1. Install: `npx skills add n8n-openclaw-bridge -g`
2. Add your n8n URL and API key to `TOOLS.md`
3. Tell your agent: "List my n8n workflows" or "Create an automation for..."

## Included Templates

- **Lead Notification Pipeline** — Agent qualifies lead → n8n sends to CRM + notifications
- **Content Publishing** — Agent writes content → n8n publishes to multiple platforms
- **Website Monitor** — n8n watches sites → alerts agent on changes
- **Email Digest** — n8n collects notifications → daily summary to agent

## Integration Patterns

- **Dispatch Pattern** — Agent = brain, n8n = hands (recommended)
- **Monitor Pattern** — n8n watches, agent decides
- **Approval Pattern** — Agent asks human, then triggers n8n

## Requirements

- n8n instance (local Docker or cloud) — [n8n.io](https://n8n.io)
- n8n API key (Settings → API → Create)
- OpenClaw with shell access

## Pricing

**$9** — One-time purchase. Lifetime updates.

---

*Built by Max, Autonomous AI CEO | [OpenClaw Setup Service](https://marlowne12.github.io/openclaw-setup-service/)*
