# Email & Messaging

## Email

### Available Tools
- **gog** — Google Workspace (Gmail, full suite)
- **himalaya** — IMAP/SMTP email CLI
- Web-based email via browser

### Email Operations
- List, read, search, compose, reply, forward
- Attachments (send and receive)
- Labels/folders management
- Filters and rules

### Email Workflows
1. **Daily digest** — Fetch → summarize → notify
2. **Auto-reply** — Match criteria → template response
3. **Newsletter processing** — Extract links → summarize
4. **Invoice tracking** — Parse → categorize → log

## Messaging Platforms

### Available
- **discord** — Discord operations (send, poll, reactions, threads)
- **slack** — Slack control (messages, reactions, pins)
- **bluebubbles** — iMessage via BlueBubbles server
- **imsg** — iMessage/SMS via macOS Messages.app
- **wacli** — WhatsApp messaging
- **xurl** — X (Twitter) DMs and posts

### Cross-Platform Patterns
- Use `message` tool for unified sending
- Route by channel parameter
- Format per platform (no markdown tables on WhatsApp, etc.)

## SMS & Voice
- **voice-call** — OpenClaw voice calls
- **imsg** — SMS via Messages.app

## Notification Strategies
- Urgent: Direct message to primary channel
- Info: Batched daily summary
- FYI: Logged to notes, no notification
- Use `silent` flag for non-urgent sends

## Email Best Practices
- Clear subject lines
- Concise body — respect the reader's time
- Call to action when needed
- Professional tone by default
- Proofread before sending (especially external)
