# Distribution

## Repos

- Lightweight policy skill: https://github.com/live-direct-marketing/ldm-openclaw-skill
- Paid MCP inbox-check skill: https://github.com/live-direct-marketing/ldm-openclaw-inbox-mcp-skill

## ClawHub Publish

Install CLI:

```bash
npx -y clawhub login
npx -y clawhub whoami
```

Publish:

```bash
npx -y clawhub skill publish /root/ldm-openclaw-skill --version 1.0.0 --clawscan-note "This skill provides outbound deliverability preflight instructions and may call the user-configured LDM API only when the user configures LDM_API_KEY."
npx -y clawhub skill publish /root/ldm-openclaw-inbox-mcp-skill --version 1.0.0 --clawscan-note "This skill uses the ldm-inbox-check-mcp MCP server via npx and requires INBOX_CHECK_API_KEY. It creates paid/quota-backed inbox placement tests only for user-approved outbound preflight workflows."
```

## Community Post

```text
I built two OpenClaw skills for outbound agents:

1. LDM Deliverability Check
A lightweight pre-send policy skill that stops bulk outbound if deliverability risk is high.

2. LDM Inbox Check MCP
A paid MCP-backed workflow that creates real seed-mailbox tests and checks Gmail/Outlook/Yahoo/Mail.ru/Yandex inbox placement before sending.

Useful for cold email, recruiting, investor updates, deal-flow, and sales agents.

Repos:
https://github.com/live-direct-marketing/ldm-openclaw-skill
https://github.com/live-direct-marketing/ldm-openclaw-inbox-mcp-skill
```

## Short Version

```text
Built two OpenClaw skills that add deliverability safety rails to outbound agents.

One is a lightweight pre-send policy skill.
The other uses LDM Inbox Check MCP for real paid seed-mailbox tests before sending.

https://github.com/live-direct-marketing/ldm-openclaw-skill
https://github.com/live-direct-marketing/ldm-openclaw-inbox-mcp-skill
```
