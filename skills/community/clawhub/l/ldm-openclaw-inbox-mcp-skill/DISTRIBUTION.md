# Distribution

Main paired skills:

- https://github.com/live-direct-marketing/ldm-openclaw-skill
- https://github.com/live-direct-marketing/ldm-openclaw-inbox-mcp-skill

## ClawHub Publish

```bash
npx -y clawhub login
npx -y clawhub skill publish /root/ldm-openclaw-inbox-mcp-skill --version 1.0.0 --clawscan-note "This skill uses the ldm-inbox-check-mcp MCP server via npx and requires INBOX_CHECK_API_KEY. It creates paid/quota-backed inbox placement tests only for user-approved outbound preflight workflows."
```

## Community Post

```text
I built an OpenClaw skill for paid inbox-placement checks through MCP.

It creates a real LDM Inbox Check test, returns seed addresses, waits for the outbound system to send the exact campaign draft, then reads back Gmail/Outlook/Yahoo/Mail.ru/Yandex placement, SPF/DKIM/DMARC, and screenshots when enabled.

Policy:
If inbox placement is below 70%, or Gmail/Outlook lands in Spam/Junk, the agent pauses and reports fixes instead of sending.

Repo:
https://github.com/live-direct-marketing/ldm-openclaw-inbox-mcp-skill

MCP package:
https://www.npmjs.com/package/ldm-inbox-check-mcp
```
