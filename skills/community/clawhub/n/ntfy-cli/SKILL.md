---
name: ntfy-cli
description: Send push notifications via ntfy.sh or self-hosted ntfy server. Supports priorities, titles, tags, icons, and attachments.
metadata:
  openclaw:
    emoji: "🔔"
    requires:
      bins:
        - ntfy
---

# ntfy CLI Skill

Send push notifications using the `ntfy` command-line tool. Agents can use this to alert Genor on his devices.

## Installation

Ensure `ntfy` is installed on the system:

```bash
# On Debian/Ubuntu
sudo apt install ntfy

# Or download binary from https://ntfy.sh/
```

Verify with `ntfy --version`.

## Basic Usage

The simplest form: push a message to a topic (which is just a URL endpoint).

```bash
ntfy send <topic_url> "<message>"
```

Example (as tested by Genor):
```bash
ntfy send http://genorbox1:9101/email-notification "HEJ"
```

## Advanced Options

### Title
```bash
ntfy send --title "Alert from Email Emily" <topic_url> "message"
```

### Priority
Priorities: `max`, `high`, `default`, `low`, `min`

```bash
ntfy send --priority high <topic_url> "Important message"
```

### Tags (emojis)
```bash
ntfy send --tags warning,skull <topic_url> "Something went wrong"
```

### Markdown formatting
```bash
ntfy send --markdown <topic_url> "**Bold** and *italic* text"
```

### Click action (open URL when tapped)
```bash
ntfy send --click "https://example.com" <topic_url> "Open dashboard"
```

### Attachments (from URL)
```bash
ntfy send --attach "https://example.com/image.png" <topic_url> "See attached"
```

### Combining options
```bash
ntfy send \
  --title "Server down" \
  --priority max \
  --tags warning,skull \
  --click "https://statuspage.example.com" \
  <topic_url> "Server xy01 is unreachable"
```

## Topic URL Format

- Self-hosted: `http://your-server:port/topic-name` or `https://your-server/topic-name`
- ntfy.sh cloud: `https://ntfy.sh/topic-name`

Topics are essentially passwords; choose something not easily guessable.

## When to Use

- Urgent alerts that need immediate attention (use `--priority max` or `high`)
- Informational notifications (use `low` or `min`)
- Email notifications (Email Emily)
- System health warnings
- Monitoring alerts

## Best Practices

- Always include a clear, concise message
- Use priority appropriately to avoid alert fatigue
- Tag messages with relevant emojis for quick visual scanning
- For critical alerts, consider adding a click action to open a dashboard or runbook
- Keep topic names secret if you want to restrict who can send notifications

## Agent Integration

When an agent needs to notify Genor via ntfy:

1. Build the message content
2. Use `ntfy send` with appropriate flags
3. Choose priority based on urgency
4. Add tags for context (e.g., `email-emily`, `health-check`)

Example from Email Emily:
```bash
ntfy send \
  --title "New important email" \
  --priority high \
  --tags email,important \
  http://genorbox1:9101/email-notification "From: john@example.com\nSubject: Project update..."
```

## Security Note

The ntfy topic URL is effectively a shared secret. Do not expose it in logs or public channels. Only use it within secure environments.

---

*ntfy-cli skill for OpenClaw agents - Updated 2026-04-02*