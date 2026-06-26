# Channel Adapters Reference

Per-channel message formatting rules and send mechanics.

## Email (Gmail via `gog` CLI)

### Prerequisites
- `gog` CLI installed and an authorized account (run `gog auth list -j` to verify)
- All commands below accept `-a <email>` to target a specific account; omit when only one account is authorized

### Format Rules
- Subject line: max 60 characters, no clickbait, specific to recipient
- Body: 4-6 sentences for cold open, 2-4 for follow-ups
- Max 120 words for cold open, 80 words for follow-up
- Plain text preferred (no HTML formatting unless user style dictates)
- Include signature block from user's Gmail settings

### Send Mechanics
1. Write the composed body to a temp file (avoids shell-escaping multi-line text):
   `printf '%s' "$body" > /tmp/outclaw_msg.txt`
2. Draft (non-trust mode): `gog gmail drafts create --to "<to>" --subject "<subj>" --body-file /tmp/outclaw_msg.txt -j`
3. Send (trust mode): `gog gmail send --to "<to>" --subject "<subj>" --body-file /tmp/outclaw_msg.txt -j`
4. Capture `id` and `threadId` from the JSON response for response detection

### Threading
- Follow-ups use `--reply-to-message-id=<id>` and/or `--thread-id=<threadId>` on `gog gmail send`
- `gog` sets `In-Reply-To`/`References` headers automatically and keeps the conversation in the same Gmail thread

## Slack

### Format Rules
- Max 3-4 sentences for DMs
- Use Slack formatting: `*bold*`, `_italic_`, no markdown headers
- No @mentions in first message to avoid notification spam
- Include brief context if messaging in a channel vs DM

### Send Mechanics
1. `slack_send_message` to user or channel
2. Track message timestamp for threading
3. Follow-ups in same thread via `thread_ts`

## WhatsApp

### Format Rules
- Max 2-3 sentences per message
- Conversational, casual tone (even more than Slack)
- No formatting (WhatsApp formatting is limited)
- Emojis acceptable if user style includes them
- No links in first message (spam filter risk)

### Send Mechanics
1. WhatsApp MCP `send_message` with recipient number
2. Track message ID for read receipts and responses
3. Respect WhatsApp Business API rate limits

## LinkedIn

### Format Rules
- Connection request note: max 300 characters
- InMail: max 200 words, subject line required
- More formal than Slack/WhatsApp, less than email
- Always reference a shared connection or interest
- No links in connection request notes

### Send Mechanics (via [linkedin-cli plugin](https://clawhub.ai/arun-8687/linkedin-cli))
1. `linkedin_cli.send_connection_request` with profile URL and note
2. `linkedin_cli.send_message` for InMails and DMs to existing connections
3. `linkedin_cli.get_profile` for pre-send research and verification
4. Rate limit: max 5 LinkedIn actions per hour

### Fallback: Browser Automation
If the linkedin-cli plugin is not installed, fall back to browser automation:
navigate to profile, click Connect, add note. Screenshot confirmation for audit trail.
This fallback is less reliable and should not be the primary path.

## Calendly

### Format Rules
- Include Calendly link naturally in message body
- Frame as "pick a time that works" not "book a meeting"
- Only include in touchpoints where a meeting CTA is appropriate

### Send Mechanics
1. `calendly.get_scheduling_link` for user's default event type
2. Embed link in message draft for the appropriate channel

## Channel Selection Matrix

| Scenario | Primary | Secondary | Notes |
|----------|---------|-----------|-------|
| Enterprise prospect | Email | LinkedIn | Formal channels first |
| Startup / tech | Email | Slack/LinkedIn | More casual acceptable |
| Existing Slack workspace | Slack DM | Email | Direct channel preferred |
| WhatsApp Business listed | Email | WhatsApp | After email intro |
| Warm intro available | LinkedIn | Email | Leverage connection |
