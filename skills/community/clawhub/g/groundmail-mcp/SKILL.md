---
name: groundmail-mcp
description: >-
  Use when installing, configuring or using the Groundmail MCP server in Claude,
  Claude Code, ChatGPT, Cursor or another MCP client: hosted
  https://mcp.groundmail.dev/mcp with OAuth, the groundmail-mcp npm package
  (stdio or --http), GROUNDMAIL_API_KEY / Bearer gm_, and tools such as
  send_email, verify_domain, create_template and get_deliverability.
license: MIT
metadata:
  author: groundmail
  homepage: https://docs.groundmail.dev/ai/agent-skills
  source: https://github.com/Groundmail/groundmail-skills
  documentation: https://docs.groundmail.dev/ai/mcp
  openclaw:
    homepage: https://docs.groundmail.dev/ai/mcp
    primaryEnv: GROUNDMAIL_API_KEY
    envVars:
      - name: GROUNDMAIL_API_KEY
        required: false
        description: Groundmail API key for the local MCP server. Not needed for the hosted server, which signs in with OAuth.
      - name: GROUNDMAIL_API_URL
        required: false
        description: Override the API base URL.
      - name: GROUNDMAIL_BURROWGUARD_SECRET
        required: false
        description: Where to keep a BurrowGuard site secret, if you create a site.
---

# Groundmail MCP

- Hosted: `https://mcp.groundmail.dev/mcp` (Streamable HTTP). OAuth sign-in, or `Authorization: Bearer gm_…`.
- Local: `npx -y groundmail-mcp` (stdio) or `npx -y groundmail-mcp --http` (`http://127.0.0.1:3000/mcp`), with `GROUNDMAIL_API_KEY=gm_…`. Optional `GROUNDMAIL_API_URL`.

Always use the full hosted URL including `/mcp`. For API rules (sandbox, idempotency, error codes) also load the `groundmail` skill.

---

## Install

### Claude Code

```bash
claude mcp add --transport http groundmail https://mcp.groundmail.dev/mcp
```

Then `/mcp` → **groundmail** → **Authenticate**, and sign in to Groundmail in the browser. Headless or CI:

```bash
claude mcp add --transport http groundmail https://mcp.groundmail.dev/mcp \
  --header "Authorization: Bearer $GROUNDMAIL_API_KEY"
# or local stdio
claude mcp add groundmail --env GROUNDMAIL_API_KEY=gm_your_key_here -- npx -y groundmail-mcp
```

### Claude (claude.ai / Desktop)

Settings → Connectors → **Add custom connector** → URL `https://mcp.groundmail.dev/mcp` → Connect → sign in to Groundmail.

### ChatGPT

Developer mode (Settings → Apps & Connectors → Advanced) → **Create** connector → URL `https://mcp.groundmail.dev/mcp`, authentication OAuth → sign in to Groundmail.

### Cursor

`.cursor/mcp.json` or `~/.cursor/mcp.json`, hosted with an API key:

```json
{
  "mcpServers": {
    "groundmail": {
      "url": "https://mcp.groundmail.dev/mcp",
      "headers": { "Authorization": "Bearer gm_your_key_here" }
    }
  }
}
```

Or local stdio:

```json
{
  "mcpServers": {
    "groundmail": {
      "command": "npx",
      "args": ["-y", "groundmail-mcp"],
      "env": { "GROUNDMAIL_API_KEY": "gm_your_key_here" }
    }
  }
}
```

Restart Cursor after editing. The dashboard **Install in Cursor** button writes this with the key filled in. Keep config files with keys out of git.

---

## Tools

| Tool | Purpose |
|------|---------|
| `send_email` | `from`, `to`, `subject`, `html`/`text`/`reply_to`, or `template_id`/`template_alias` + `variables` |
| `list_emails` / `get_email` | Recent sends, status of one send |
| `get_batch` / `cancel_batch` | A batch send's status counts; cancel its still-scheduled emails |
| `list_received_emails` | Inbound mail; `in_reply_to_email: "msg_…"` lists the replies to one send |
| `list_domains` / `create_domain` | Sending domains |
| `create_mailbox` / `wait_for_mailbox_message` | An agent's own address, and the next message to it. See the `groundmail-mailboxes` skill |
| `reply_to_mailbox_message` / `send_mailbox_message` | Reply in a thread, or send from a mailbox |
| `apply_domain_dns` / `verify_domain` | Publish DNS (Cloudflare, Vercel, GoDaddy), then verify |
| `list_templates` / `get_template` / `create_template` / `publish_template` | Templates |
| `list_webhooks` / `create_webhook` / `delete_webhook` | Webhook endpoints |
| `list_webhook_deliveries` / `get_webhook_delivery` / `resend_webhook_delivery` | The delivery log: every attempt, the payload and the reply, kept 30 days |
| `send_test_webhook_event` | Simulated event to webhooks; no email sent |
| `list_suppressions` / `add_suppression` / `remove_suppression` | Suppression list |
| `list_category_opt_outs` / `remove_category_opt_out` | One-click unsubscribes from product or newsletter email (per tenant or account-wide) |
| `validate_email` | Check one address: `valid` / `risky` / `invalid`, reasons, typo suggestion. Free; sends nothing |
| `create_burrowguard_site` / `update_burrowguard_site` / `list_burrowguard_sites` / `list_burrowguard_checks` | BurrowGuard: block bots and bad addresses on sign-up forms. Create returns the secret once: put it in the app's env as `GROUNDMAIL_BURROWGUARD_SECRET`, never in code or chat. `watch_only` shows what would be blocked without blocking anyone |
| `get_deliverability` | Best-effort metrics for `7d` or `30d` (not inbox placement guarantees) |
| `enable_dmarc_monitoring` / `get_dmarc_report` | DMARC monitoring: record to publish, then sources, pass rates and enforcement readiness |
| `get_test_inbox_address` / `wait_for_test_email` / `list_test_emails` / `get_test_email` | Email testing: a fresh address on the team's test domain (mail from any provider is caught, never delivered), then wait for the email and read its code and links |
| `list_tenants` / `create_tenant` / `get_tenant` / `update_tenant` / `pause_tenant` / `resume_tenant` / `get_tenant_stats` | Tenants: one per customer you send for (pay as you go and Dedicated) |
| `import_from_provider` / `get_import_report` | Beta. Import from SendGrid, Postmark, Mailgun, Resend, Amazon SES or Azure Communication Services (`dry_run` first), then read the report. Local server only; on the hosted server, send the user to https://app.groundmail.dev/import |

Full list with one line per tool: https://docs.groundmail.dev/ai/mcp

## Rules for agents

1. First send: `from` `noreply@mail.groundmail.dev`, `to` the user's Groundmail account email. Other recipients are refused until a domain is verified and the user has set up billing in the dashboard.
2. Confirm with the user before `send_email` to anyone but them, `create_domain`, `delete_webhook`, `resend_webhook_delivery`, `remove_suppression` or `remove_category_opt_out`.
3. Failed tool calls return the API message, `code: …` with the HTTP status, and a `how to fix` link to https://docs.groundmail.dev/errors#<code>. Follow it instead of retrying blindly.
4. `send_email` does not take an idempotency key. For app code that retries, use the SDK or HTTP with `Idempotency-Key`.
5. Never ask for or accept payment card numbers, passwords, government ID numbers, health information or other sensitive personal data in chat; the user enters billing and account details only in the Groundmail dashboard.

## MCP vs SDK

| Prefer MCP | Prefer SDK / HTTP in app code |
|------------|-------------------------------|
| Interactive setup, DNS, one-off sends, checking status | Production send paths, CI, retries with idempotency |

Never put the API key in client-side code, even when using MCP during development.
