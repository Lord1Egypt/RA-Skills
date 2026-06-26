---
name: po6-mailbox
description: "Manage PO6 email aliases, mailbox, and landing pages via the PO6 MCP server. Use when the user wants to read, send, search, compose, reply, or forward emails. Use when managing email aliases, forwarding rules, or custom domains. Use when creating, editing, publishing, or viewing analytics for landing pages. Triggers on check email, send email, search inbox, compose message, list aliases, create landing page, check leads, forward email, manage domain."
version: 1.0.0
homepage: https://po6.com
user-invocable: true
metadata: {"clawdbot":{"emoji":"📨","requires":{"env":["PO6_API_KEY"]},"primaryEnv":"PO6_API_KEY","homepage":"https://po6.com/docs/mcp"}}
---

# PO6 Mailbox

Manage your PO6 email aliases, mailbox, and landing pages through natural language.

PO6 gives you short, memorable email addresses like `you@po6.com` or email on your own domain. This skill connects to the PO6 MCP server so you can manage everything conversationally.

## Setup

### 1. Get a PO6 account and API key

1. Sign up at [po6.com](https://po6.com)
2. Go to **Dashboard > Mailbox > API Keys**
3. Create a new API key with the scopes you need
4. Copy the key (starts with `mcp_po6_`)

### 2. Set your API key

```bash
export PO6_API_KEY="mcp_po6_your_key_here"
```

Or add it to your shell profile (`~/.zshrc`, `~/.bashrc`) for persistence.

### 3. Add the MCP server

Add to `~/.openclaw/openclaw.json` under `mcpServers`:

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

Or run the included setup script:

```bash
./scripts/setup.sh
```

### 4. Restart OpenClaw

Restart to pick up the new MCP server.

## Core Tasks

- "Check my inbox for unread emails"
- "Send an email to alice@example.com about the project update"
- "Search my emails for invoices from last month"
- "Reply to the latest email from Bob saying I'll be there at 3pm"
- "Create a draft email to the team about the new schedule"
- "List my aliases and show which ones are active"
- "Create a landing page for our spring sale using the marketing template"

## Available Tools

### Mailbox Management (13 tools)

| Tool | Description |
|------|-------------|
| `list_mailboxes` | List all accessible mailboxes |
| `get_mailbox_stats` | Get mailbox statistics (counts, storage, folders) |
| `list_emails` | List emails with filters (folder, sender, date, unread, starred) |
| `get_email` | Read full email content, headers, and attachments |
| `search_emails` | Search emails by query across sender, subject, and content |
| `mark_email` | Mark emails as read/unread or starred/unstarred |
| `move_email` | Move emails between folders |
| `delete_email` | Permanently delete an email (two-step confirmation) |
| `list_folders` | List all folders in a mailbox |
| `list_email_lists` | List contact/mailing lists |
| `get_email_list_contacts` | Get contacts from a mailing list |
| `list_drafts` | List draft emails pending review |
| `list_sent_emails` | List sent emails with delivery status |

### Email Sending (4 tools)

| Tool | Description |
|------|-------------|
| `compose_email` | Send a new email from your alias (requires paid plan) |
| `reply_email` | Reply to an email |
| `forward_email` | Forward an email to other recipients |
| `create_draft` | Create a draft for your review before sending |

### Templates (2 tools)

| Tool | Description |
|------|-------------|
| `list_templates` | Browse email templates |
| `get_template` | Get template details and variables |

### Aliases & Domains (7 tools)

| Tool | Description |
|------|-------------|
| `list_aliases` | List your @po6.com aliases |
| `get_alias` | Get alias details and forwarding config |
| `update_alias` | Update alias settings (forwarding, active, plus addressing) |
| `list_domains` | List your custom (BYOD) domains |
| `get_domain` | Get domain details (verification, MX, catchall) |
| `update_domain_alias` | Update a domain alias |
| `update_catchall` | Enable/disable catchall forwarding |

### Landing Pages (13 tools)

| Tool | Description |
|------|-------------|
| `list_landing_page_templates` | Browse available page templates |
| `get_landing_page_template` | Get template details |
| `list_landing_pages` | List your pages (draft/published/archived) |
| `get_landing_page` | Get page content, config, and SEO settings |
| `create_landing_page` | Create a new page from a template |
| `update_landing_page` | Update page content, SEO, and settings |
| `publish_landing_page` | Publish a landing page (two-step confirmation) |
| `unpublish_landing_page` | Unpublish a page to draft (two-step confirmation) |
| `archive_landing_page` | Archive a landing page (two-step confirmation) |
| `assign_landing_page_domain` | Assign a custom domain (two-step confirmation) |
| `download_landing_page` | Download page as standalone HTML |
| `get_landing_page_stats` | View analytics (views, visitors, conversions) |
| `list_landing_page_leads` | View form submissions and leads |

## Environment Variable Contract

| Variable | Required | Description |
|----------|----------|-------------|
| `PO6_API_KEY` | Yes | Your PO6 API key (starts with `mcp_po6_`). Get it from [po6.com/dashboard/mailbox](https://po6.com/dashboard/mailbox). |

## API Key Scopes

When creating your API key, select the scopes you need. Start with read-only scopes and add write scopes as needed.

| Scope | Access |
|-------|--------|
| `mailbox:list` | List mailboxes, folders, email summaries |
| `mailbox:read` | Read full email content and attachments |
| `mailbox:search` | Search emails |
| `mailbox:write` | Mark, move emails |
| `mailbox:delete` | Delete emails |
| `mailbox:send` | Send, reply, forward emails |
| `alias:list` | List aliases and domains |
| `alias:read` | Read alias/domain details |
| `alias:write` | Update alias and domain settings |
| `landing_page:list` | List pages and templates |
| `landing_page:read` | Read page content and stats |
| `landing_page:write` | Create, update, archive pages |
| `landing_page:publish` | Publish/unpublish pages |
| `landing_page:leads` | Access lead/form submission data |
| `landing_page:domain` | Manage custom domains on pages |

## Rate Limits

| Limit | Value |
|-------|-------|
| API requests | 60/minute per key (configurable) |
| Email sending (Standard) | 30/hour, 200/day, 3,000/month |
| Email sending (Plus) | 60/hour, 500/day, 10,000/month |
| Email sending (Premium) | 100/hour, 500/day, 15,000/month |
| Brute force protection | 15 failed attempts in 15 min triggers 15 min lockout |

## External Endpoints

This skill communicates only with:

- `https://mcp.po6.com` — PO6 MCP server (all tool calls)

No other external endpoints are contacted.

## Security & Privacy

- **Secrets handling**: Your API key is stored locally in your environment and never logged or sent to third parties. The key is transmitted only in the `Authorization` header over TLS to `mcp.po6.com`.
- **Server-side hashing**: API keys are SHA-256 hashed on the server. PO6 cannot see your key after creation.
- **IP allowlists**: Optionally restrict key usage to specific IP addresses (CIDR notation supported).
- **Key expiration**: Keys can be set to auto-expire on a date you choose.
- **Confirmation for destructive actions**: `delete_email`, `publish_landing_page`, `unpublish_landing_page`, `archive_landing_page`, and `assign_landing_page_domain` all require two-step confirmation before execution.
- **Audit trail**: All API calls are logged and visible in your PO6 dashboard.
- **Scope isolation**: Keys can be restricted to specific mailboxes and specific scopes, following the principle of least privilege.
- **No external storage**: No data is stored outside your PO6 account.

## Troubleshooting

| Error | Fix |
|-------|-----|
| `PO6_API_KEY not set` | Export the variable in the shell that runs OpenClaw. Run `echo $PO6_API_KEY` to verify. |
| `Authentication failed` | Check that your key starts with `mcp_po6_` and hasn't expired. Generate a new key from your dashboard if needed. |
| `Rate limited` (-32002) | Wait a minute and retry. If you need higher limits, upgrade your plan or contact support. |
| `Insufficient scopes` | Your API key lacks permission for that action. Create a new key with the required scopes from your dashboard. |
| `IP not allowed` | Your key has an IP allowlist and your current IP is not on it. Update the allowlist in your dashboard. |

## Support

- Documentation: [po6.com/docs/mcp](https://po6.com/docs/mcp)
- Dashboard: [po6.com/dashboard](https://po6.com/dashboard)
- Contact: [support@po6.com](mailto:support@po6.com)
