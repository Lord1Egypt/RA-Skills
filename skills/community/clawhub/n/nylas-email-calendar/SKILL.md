---
name: nylas-email-calendar
description: Email, calendar & contacts via Nylas API — 14 typed tools across Gmail, Outlook, Exchange, Yahoo, iCloud, and IMAP.
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["NYLAS_API_KEY"]},"primaryEnv":"NYLAS_API_KEY","emoji":"📧"}}
---

# Nylas Email, Calendar & Contacts

Unified access to email, calendar, and contacts across Gmail, Outlook, Exchange, Yahoo, iCloud, and IMAP — powered by the Nylas API.

## Setup

Install the plugin (one command, no restart needed):

```bash
openclaw plugins install @nylas/openclaw-nylas-plugin
```

Configure your API key:

```bash
openclaw config set nylas.apiKey "YOUR_NYLAS_API_KEY"
```

Get your API key from [Nylas Dashboard](https://dashboard-v3.nylas.com).

Verify setup:

```bash
openclaw nylas status
openclaw nylas discover
```

## Tools

### Email (7 tools)

- **nylas_list_messages** — List recent messages with optional filters (unread, limit)
- **nylas_search_messages** — Search messages by keyword (e.g., `from:sarah Q4 budget`)
- **nylas_read_message** — Read a specific message by ID (full content)
- **nylas_send_message** — Send an email (to, subject, body)
- **nylas_create_draft** — Create a draft for review before sending
- **nylas_list_threads** — List email threads grouped by conversation
- **nylas_list_folders** — List mailbox folders and labels

### Calendar (5 tools)

- **nylas_list_events** — List calendar events for a date range
- **nylas_create_event** — Create a new event with title, time, and participants
- **nylas_update_event** — Update an existing event (reschedule, add attendees)
- **nylas_delete_event** — Delete a calendar event
- **nylas_get_availability** — Check free/busy availability for scheduling

### Contacts (2 tools)

- **nylas_search_contacts** — Search contacts by name or email
- **nylas_get_contact** — Get full contact details by ID

## Multi-Account Support

The plugin auto-discovers all connected accounts from your API key. Use named grants to reference accounts:

- "Check my **work** email" — resolves to your work grant
- "What's on my **personal** calendar?" — resolves to your personal grant

## Examples

- "Show me unread emails from this week"
- "Send a reply to Sarah's last message"
- "What meetings do I have tomorrow?"
- "Schedule a 30-min call with the team on Thursday at 2pm"
- "Find Sarah Chen's email address"
- "Am I free Friday afternoon?"
- "Create a draft response to the budget proposal"

## Links

- [Installation Guide](https://cli.nylas.com/guides/install-openclaw-nylas-plugin)
- [npm Package](https://www.npmjs.com/package/@nylas/openclaw-nylas-plugin)
- [Nylas CLI](https://cli.nylas.com)
