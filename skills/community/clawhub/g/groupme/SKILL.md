---
name: groupme
description: "Bridge OpenClaw to GroupMe for team communication. Send scheduled messages, broadcast announcements, run shift reminders, and automate group messaging via cron jobs. Use when: you want to send messages to a GroupMe group on a schedule or on-demand, automate team announcements, or create notification workflows."
metadata:
  openclaw:
    requires:
      env:
        - GROUPME_ACCESS_TOKEN
        - GROUPME_BOT_ID
        # GROUPME_GROUP_ID is optional — only needed for group discovery, not for sending
      bins:
        - curl
        - python3  # Used for safe JSON serialization in send-message.sh
    primaryEnv: GROUPME_ACCESS_TOKEN
  license: MIT-0
  version: 1.0.4
  tags: [groupme, messaging, automation, cron, announcements]
---

# GroupMe Skill — OpenClaw × GroupMe Integration

Connect OpenClaw to any GroupMe group for automated messaging, announcements, and team communication workflows.

## What This Skill Does

- **Send messages** to a GroupMe group on-demand or on a schedule
- **Automate recurring messages** via cron (shift reminders, daily briefings, weekly announcements)
- **Broadcast urgent alerts** instantly with one command
- **Enable team workflows** — kudos, polls, coverage requests, etc.

## API Overview

**Base URL:** `https://api.groupme.com/v3`

**Authentication:** Token passed as query parameter `?token=ACCESS_TOKEN`

**Key Endpoints:**

| Endpoint | Purpose |
|----------|---------|
| `POST /bots/post` | Send a message |
| `GET /groups` | List your groups |
| `GET /groups/:id/messages` | Get group messages |

## Configuration

Before using this skill, you need:

1. **GroupMe Access Token** — get it at https://dev.groupme.com/bots (top of page)
2. **Group ID** — the ID of your GroupMe group (fetch via API)
3. **Bot ID** — create a bot at https://dev.groupme.com/bots/new

### Save Your Tokens

Create a file at `~/.openclaw/secrets/groupme.env`:

```bash
GROUPME_ACCESS_TOKEN="your_access_token_here"
GROUPME_BOT_ID="your_bot_id_here"
GROUPME_GROUP_ID="your_group_id_here"  # Optional — only needed to discover group IDs, not required for sending
```

**Never commit this file to git.**

### Finding Your Group ID

Run this command (replace with your token):

```bash
curl -s "https://api.groupme.com/v3/groups?token=YOUR_TOKEN&per_page=10"
```

Look for your group in the response — the `id` field is your Group ID.

## Quick Reference

### Send a Message

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"bot_id": "YOUR_BOT_ID", "text": "Your message here"}' \
  "https://api.groupme.com/v3/bots/post?token=YOUR_ACCESS_TOKEN"
```

### Send with Line Breaks

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"bot_id": "YOUR_BOT_ID", "text": "Line one\nLine two\nLine three"}' \
  "https://api.groupme.com/v3/bots/post?token=YOUR_ACCESS_TOKEN"
```

## Usage Patterns

### One-Time Messages

Tell OpenClaw to send a message:

> "Send a message to the group: Don't forget, team meeting at 3pm today"

> "Post this to the group: Great job everyone on a successful week!"

### Scheduled Messages via Cron

**Daily shift reminder (Mon-Fri at 8am):**

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * 1-5",
    "tz": "America/New_York"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Send daily shift reminder to GroupMe"
  },
  "sessionTarget": "isolated"
}
```

**Weekly team announcement (Monday at 9am):**

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1",
    "tz": "America/New_York"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Send weekly team announcement to GroupMe"
  },
  "sessionTarget": "isolated"
}
```

### Workflow Ideas

| Workflow | Description |
|----------|-------------|
| **Shift Reminders** | Fire 1hr before each shift |
| **Team Announcements** | Weekly goals, meeting changes |
| **Emergency Alerts** | One-command urgent broadcast |
| **Recognition Posts** | Kudos for good work |
| **Coverage Requests** | "Need someone to cover 3-5pm" |
| **Daily Briefs** | Industry news, daily stats |
| **Polling** | "Thumbs up if you can work Saturday" |

## Message Types

### Plain Text
```json
{
  "bot_id": "BOT_ID",
  "text": "Your message here"
}
```

### With Image
Images must first be uploaded to GroupMe's image service. See https://dev.groupme.com/docs/image_service

```json
{
  "bot_id": "BOT_ID",
  "text": "Check out the new schedule!",
  "attachments": [{
    "type": "image",
    "url": "https://i.groupme.com/xxxxx.large"
  }]
}
```

### With Location
```json
{
  "bot_id": "BOT_ID",
  "text": "Heading to the location",
  "attachments": [{
    "type": "location",
    "lat": "40.738206",
    "lng": "-73.993285",
    "name": "Location Name"
  }]
}
```

## Limitations

- **Outbound only** — Bots can send messages but cannot receive and respond. For two-way conversation, a callback URL server is required.
- **1,000 character limit** per message
- **Images** must be uploaded to GroupMe's image service first
- **No bot personality** — GroupMe bots are announcement channels, not conversational agents

## Files

```
~/.openclaw/skills/groupme/
├── SKILL.md              ← this file
├── scripts/
│   └── send-message.sh   ← optional shell helper
```

## Setup Checklist

- [ ] Get access token: https://dev.groupme.com/bots
- [ ] Create bot: https://dev.groupme.com/bots/new
- [ ] Find Group ID via API
- [ ] Save tokens to `~/.openclaw/secrets/groupme.env`
- [ ] Test: send a message manually
- [ ] Set up first cron job

## Skill Metadata

- **Version:** 1.0.0
- **License:** MIT-0
- **Token storage:** `~/.openclaw/secrets/groupme.env`
- **Runtime:** isolated agent session for cron-driven messages