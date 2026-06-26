---
name: Gmail Integration
description: Gmail integration - Send emails, manage labels, and automate Gmail workflows with full OAuth2 support
homepage: https://github.com/lukaizj/gmail-integration-skill
tags:
  - productivity
  - email
  - gmail
  - google
  - automation
requires:
  env:
    - GMAIL_CLIENT_ID
    - GMAIL_CLIENT_SECRET
files:
  - gmail.py
---

# Gmail Integration

Gmail integration skill for OpenClaw. Send emails, manage labels, and automate Gmail workflows.

## Capabilities

- Send emails via Gmail API
- List recent emails from inbox
- Create and manage custom labels
- Full OAuth2 support for secure authentication

## Setup

1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API from API Library
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Download the JSON and get client_id and client_secret
5. Configure environment variables

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GMAIL_CLIENT_ID` | Yes | OAuth Client ID from Google Cloud |
| `GMAIL_CLIENT_SECRET` | Yes | OAuth Client Secret |

## Usage Examples

```
Send an email to boss@example.com with subject "Project Update" and body "The project is complete"

List my recent emails from Gmail

Create a new label named "Projects/OpenClaw"
```

## Message Types

- Plain text emails
- HTML emails (coming soon)
- Emails with attachments (coming soon)

## Rate Limits

Google Gmail API has rate limits:
- 100:00 requests per day
- 100 requests per second

## Troubleshooting

- "Invalid credentials": Re-check your OAuth credentials
- "Rate limit exceeded": Wait before making more requests
- "Account not verified": Your app needs to go through Google's verification for sensitive scopes