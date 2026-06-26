# PO6 Mailbox — OpenClaw Skill

Manage your [PO6](https://po6.com) email aliases, mailbox, and landing pages from any OpenClaw-connected chat app (WhatsApp, Telegram, Discord, Signal, Slack, and more).

**39 tools** across email, aliases, domains, and landing pages — all accessible via natural language.

## Quick Start

### Install from ClawHub

```
/install po6-mailbox
```

### Manual Install

1. **Get your API key** from [po6.com/dashboard/mailbox](https://po6.com/dashboard/mailbox) (starts with `mcp_po6_`)

2. **Set the environment variable:**
   ```bash
   echo 'export PO6_API_KEY="mcp_po6_your_key_here"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Add the MCP server.** Run the included setup script:
   ```bash
   cd ~/.openclaw/skills/po6-mailbox
   ./scripts/setup.sh
   ```

   Or manually add to `~/.openclaw/openclaw.json`:
   ```json
   {
     "mcpServers": {
       "po6-mailbox": {
         "type": "streamable-http",
         "url": "https://mcp.po6.com",
         "headers": {
           "Authorization": "Bearer ${PO6_API_KEY}"
         }
       }
     }
   }
   ```

4. **Restart OpenClaw** and you're ready to go.

## What Can It Do?

**Email Management (19 tools)** — Read, send, search, reply, forward, and organize emails from your PO6 aliases. Create drafts for review before sending. Browse and use email templates. Manage contact lists.

**Alias & Domain Management (7 tools)** — List and configure your @po6.com aliases and custom domain (BYOD) email addresses. Update forwarding rules and catchall settings.

**Landing Pages (13 tools)** — Create, edit, publish, and track landing pages. View analytics, manage leads, assign custom domains, and download pages as standalone HTML.

## Example Conversations

> "Check my inbox"

Lists your recent emails with sender, subject, and preview.

> "Send an email to alice@example.com from my w@ alias about tomorrow's meeting"

Composes and sends the email from your PO6 alias.

> "Search for emails about invoices from the last 2 weeks"

Searches across your mailbox and returns matching emails.

> "How many leads did my landing page get this week?"

Shows conversion stats and recent form submissions.

> "Create a landing page for our new product launch"

Walks you through template selection and page creation.

> "Star all unread emails from my boss"

Searches and bulk-marks emails.

> "Forward the email from Sarah to my work address"

Finds the email and forwards it.

## Scopes & Permissions

When creating your API key, you choose exactly what the skill can access:

| What you want to do | Scopes needed |
|---------------------|--------------|
| Read emails only | `mailbox:list`, `mailbox:read` |
| Read + send emails | `mailbox:list`, `mailbox:read`, `mailbox:send` |
| Full email management | `mailbox:list`, `mailbox:read`, `mailbox:write`, `mailbox:send`, `mailbox:search`, `mailbox:delete` |
| Manage aliases | `alias:list`, `alias:read`, `alias:write` |
| Manage landing pages | `landing_page:list`, `landing_page:read`, `landing_page:write`, `landing_page:publish` |
| View landing page leads | `landing_page:list`, `landing_page:read`, `landing_page:leads` |
| Everything | All scopes |

**Tip:** Start with read-only scopes and add write scopes as needed. You can always create a new key with broader access later.

## Security

- API key stays on your machine — only sent in the `Authorization` header over TLS to `mcp.po6.com`
- All traffic goes directly to `https://mcp.po6.com` — no other external endpoints
- Keys are SHA-256 hashed server-side (PO6 can't see your key after creation)
- Optional IP allowlists (CIDR) and key expiration for extra security
- Keys can be scoped to specific mailboxes
- Destructive actions (`delete_email`, `publish_landing_page`, `unpublish_landing_page`, `archive_landing_page`, `assign_landing_page_domain`) require two-step confirmation
- Full audit trail in your PO6 dashboard

## Rate Limits

| Limit | Value |
|-------|-------|
| API requests | 60/minute per key (configurable) |
| Email sending (Standard) | 30/hour, 200/day, 3,000/month |
| Email sending (Plus) | 60/hour, 500/day, 10,000/month |
| Email sending (Premium) | 100/hour, 500/day, 15,000/month |
| Brute force protection | 15 failed attempts in 15 min → 15 min lockout |

Free plan users cannot send email via the API.

## Troubleshooting

| Error | Fix |
|-------|-----|
| `PO6_API_KEY not set` | Export the variable in the shell that runs OpenClaw. Run `echo $PO6_API_KEY` to verify. |
| `Authentication failed` | Check that your key starts with `mcp_po6_` and hasn't expired. Generate a new key from your dashboard. |
| `Rate limited` (-32002) | Wait a minute and retry. Upgrade your plan for higher limits. |
| `Insufficient scopes` | Your API key lacks the permission for that action. Create a new key with the required scopes. |
| `IP not allowed` | Your key has an IP allowlist and your current IP isn't on it. Update it in your dashboard. |

## Links

- [PO6 Website](https://po6.com)
- [PO6 Dashboard](https://po6.com/dashboard)
- [MCP Documentation](https://po6.com/docs/mcp)
- [Support](mailto:support@po6.com)
