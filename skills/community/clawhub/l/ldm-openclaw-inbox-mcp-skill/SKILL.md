---
name: ldm-inbox-check-mcp
description: Use the paid LDM Inbox Check MCP server to run real inbox-placement tests before OpenClaw agents send cold email or bulk outbound.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - INBOX_CHECK_API_KEY
      bins:
        - npx
    primaryEnv: INBOX_CHECK_API_KEY
    envVars:
      - name: INBOX_CHECK_API_KEY
        required: true
        description: Bearer API key for Inbox Check service. Starts with icp_live_.
      - name: INBOX_CHECK_BASE_URL
        required: false
        description: Optional base URL override. Defaults to https://check.live-direct-marketing.online.
    install:
      - kind: node
        package: ldm-inbox-check-mcp
        bins: [ldm-inbox-check-mcp]
    emoji: "\U0001F4EC"
    homepage: https://github.com/live-direct-marketing/ldm-openclaw-inbox-mcp-skill
---

# LDM Inbox Check MCP

Use this skill when an OpenClaw agent needs a real paid inbox-placement test, not just a lightweight content review.

This skill uses the `ldm-inbox-check-mcp` MCP server. It creates an inbox test, returns real seed mailboxes, requires the outbound system to send the exact draft to those seed addresses, then reads back placement, authentication, screenshots, and provider-level results.

## MCP Server

Configure the MCP server:

```json
{
  "mcpServers": {
    "inbox-check": {
      "command": "npx",
      "args": ["-y", "ldm-inbox-check-mcp"],
      "env": {
        "INBOX_CHECK_API_KEY": "icp_live_xxxxxxxxxxxxxxxxxxxxxxxx",
        "INBOX_CHECK_BASE_URL": "https://check.live-direct-marketing.online"
      }
    }
  }
}
```

`INBOX_CHECK_API_KEY` is required and starts with `icp_live_`.

Each successful `inbox_check_create` consumes paid/quota-backed usage. Do not create tests casually.

## Available Tools

Use these MCP tools when available:

- `inbox_check_me` - inspect API key tier, features, allowed providers, and quota usage
- `inbox_check_create` - create a paid inbox-placement test and return seed addresses
- `inbox_check_status` - fetch placement, SPF/DKIM/DMARC, summary stats, screenshots
- `inbox_check_list` - list previous tests
- `inbox_check_delete` - delete a test and screenshots; irreversible

Domain monitoring tools may also be available:

- `monitor_list_domains`
- `monitor_add_domain`
- `monitor_run_check`
- `monitor_get_latest_check`
- `monitor_list_checks`
- `monitor_get_settings`
- `monitor_update_settings`

## When To Use

Run a paid inbox check before:

- sending a cold email campaign
- sending more than 5 similar outbound emails
- changing sender domain, mailbox, template, links, or tracking setup
- launching recruiting, investor-update, deal-flow, sales, or partnership outreach
- diagnosing sudden spam placement
- validating a new email infrastructure setup

For a casual one-off message, ask the user before consuming a paid/quota-backed test.

## Workflow

1. Call `inbox_check_me` to confirm the key works and inspect allowed providers/quota.
2. Choose the smallest provider set that answers the user question. Prefer Gmail and Outlook for a fast preflight; add Yahoo, Mail.ru, or Yandex when relevant.
3. Call `inbox_check_create` with selected providers and useful metadata.
4. Send the exact final email draft to every returned seed address using the same sender, subject, body, links, headers, and tracking settings planned for the campaign.
5. Wait 60-120 seconds, then call `inbox_check_status`.
6. If the test is still waiting/checking, poll again after a short delay.
7. Decide whether to send, revise, or pause.

## Pass / Fail Policy

Default pass criteria:

- Inbox placement is at least 70%.
- Gmail and Outlook do not land in Spam/Junk.
- SPF passes.
- DKIM passes.
- DMARC passes or is aligned enough for the campaign risk.
- No critical blocklist, unsafe-link, or broken-link issue appears.

Fail the preflight and pause sending if:

- inbox placement is below 70%
- Gmail or Outlook lands in Spam/Junk
- SPF, DKIM, or DMARC fails
- seed messages are not received after the normal wait window
- screenshots or headers show obvious spam-folder placement
- the API reports quota/tier limits that make the test incomplete

Only continue after a failed preflight if the user explicitly overrides the risk.

## Reporting Format

Report results like this:

```text
LDM paid inbox check: PASS/FAIL
Test token: ...
Providers tested: Gmail, Outlook, ...
Inbox placement: N%
Spam/Junk: ...
Not received: ...
Authentication: SPF ..., DKIM ..., DMARC ...
Screenshots: available/not available
Quota: used ... / limit ...
Decision: send / revise / pause
Fixes: ...
```

## Cost And Quota Discipline

Because this is a paid/quota-backed MCP workflow:

- Call `inbox_check_me` before creating tests when quota is unknown.
- Reuse recent relevant tests from `inbox_check_list` when the sender, subject, body, links, and providers are unchanged.
- Do not run repeated tests while editing copy unless the user is ready for final approval.
- Prefer one final paid test over many speculative tests.

## Safety

Never print, log, commit, or expose `INBOX_CHECK_API_KEY`.

Never send campaign emails before the paid inbox check completes unless the user explicitly asks to bypass deliverability preflight.

Never delete tests unless the user asks or retention policy requires it.
