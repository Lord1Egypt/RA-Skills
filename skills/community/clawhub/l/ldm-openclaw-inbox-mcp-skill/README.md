# LDM Inbox Check MCP Skill for OpenClaw

An OpenClaw skill for paid, real inbox-placement testing through the `ldm-inbox-check-mcp` server.

It helps outbound agents verify whether a campaign lands in Inbox, Spam, Promotions, or Junk before sending to real prospects.

## What It Does

- Creates paid inbox-placement tests via MCP
- Returns real seed addresses for Gmail, Outlook, Yahoo, Mail.ru, Yandex, and other providers supported by the key
- Reads back provider-level placement
- Checks SPF, DKIM, and DMARC results
- Uses screenshots when enabled
- Stops outbound if the result is risky

## MCP Package

```bash
npx -y ldm-inbox-check-mcp
```

## OpenClaw / MCP Config

```json
{
  "mcpServers": {
    "inbox-check": {
      "command": "npx",
      "args": ["-y", "ldm-inbox-check-mcp"],
      "env": {
        "INBOX_CHECK_API_KEY": "icp_live_xxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

Optional:

```json
{
  "INBOX_CHECK_BASE_URL": "https://check.live-direct-marketing.online"
}
```

## Agent Policy

```text
Before sending bulk outbound, run a paid LDM inbox check through MCP.
If inbox placement is below 70%, or Gmail/Outlook lands in Spam/Junk, pause and report fixes instead of sending.
```

## Example Prompt

```text
Prepare this cold email campaign, then run LDM Inbox Check MCP before sending.
Use Gmail and Outlook for the preflight. If either lands in spam, pause the campaign and tell me what to fix.
```

## Links

- MCP package: https://www.npmjs.com/package/ldm-inbox-check-mcp
- MCP repo: https://github.com/live-direct-marketing/ldm-inbox-check-mcp
- Inbox Check: https://check.live-direct-marketing.online
- API docs: https://check.live-direct-marketing.online/docs/mcp

## Notes

This skill is for paid/quota-backed real inbox tests. For lightweight copy review or a free preflight workflow, use the separate LDM deliverability skill.
