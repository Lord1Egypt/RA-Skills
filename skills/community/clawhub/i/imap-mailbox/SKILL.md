---
name: imap-mailbox
description: "Read and manage emails via IMAP protocol. List, read, search, and download email attachments. Supports digest mode for daily briefings. Triggers: check email, read inbox, new mail, email digest."
---

# IMAP Mailbox

Read and manage emails via the IMAP protocol.

## Use Cases

- User asks to check email, view inbox, or read email content
- User asks to search emails (by sender, subject, etc.)
- User asks to mark emails as read/unread
- Daily email digest / briefing

## Commands

### List Recent Emails

```bash
imap-mailbox list [limit]
```

Lists summaries (sender, subject, date) of the most recent emails. Default: 10.

### Read Email Content

```bash
imap-mailbox read <uid>
```

Read the full content of the email with the specified UID.

### Search Emails

```bash
imap-mailbox search <keyword>
```

Search emails where the subject or sender contains the keyword.

### Email Digest

```bash
imap-mailbox digest
```

Generate a daily email digest summary — categorized and condensed for quick review.

### Download Attachments

```bash
imap-mailbox download <uid> [output-dir]
```

Download attachments from the specified email to the output directory.

## Configuration

Config file located at `~/.config/imap-mailbox/config.json`, containing email address, IMAP server, and authorization token.

```json
{
  "email": "user@example.com",
  "host": "imap.example.com",
  "port": 993,
  "token": "your-authorization-code"
}
```

## Security Notes

- Authorization tokens are stored locally and never uploaded
- Recommend rotating authorization tokens periodically
- To revoke access, regenerate the authorization code in your email provider settings
