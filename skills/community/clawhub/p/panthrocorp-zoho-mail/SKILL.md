---
name: Zoho Mail
description: Full read/write Zoho Mail access for OpenClaw agents
version: 0.3.0
author: panthrocorp
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - ZOHO_MAIL_TOKEN_KEY
        - ZOHO_CLIENT_ID
        - ZOHO_CLIENT_SECRET
      bins:
        - zoho-mail
    emoji: "📬"
    homepage: https://github.com/PanthroCorp-Limited/openclaw-skills
    os: ["linux"]
---

# Zoho Mail Skill

Full read/write access to a Zoho Mail account (EU data centre).

## Installation

Download the latest release binary for linux/arm64 and install to `~/.openclaw/bin/`:

```bash
TAG=$(curl -fsSL "https://api.github.com/repos/PanthroCorp-Limited/openclaw-skills/releases" \
  | grep -o '"tag_name":"zoho-mail/v[^"]*"' | head -1 | cut -d'"' -f4)
VERSION=${TAG#zoho-mail/v}
curl -fsSL "https://github.com/PanthroCorp-Limited/openclaw-skills/releases/download/${TAG}/zoho-mail_${VERSION}_linux_arm64.tar.gz" \
  | tar -xz -C ~/.openclaw/bin/ zoho-mail
chmod +x ~/.openclaw/bin/zoho-mail
```

## Important

OAuth tokens are encrypted at rest. The operator must run `zoho-mail auth login` once after deployment to complete the OAuth flow.

## Check configuration

```
zoho-mail config show
```

## Mail commands

List messages in a folder (default: INBOX):

```
zoho-mail mail list
zoho-mail mail list --folder INBOX --limit 20 --start 0
```

Read a message by ID:

```
zoho-mail mail read --id MESSAGE_ID
```

Send a new message:

```
zoho-mail mail send --to recipient@example.com --subject "Hello" --body "Message body"
zoho-mail mail send --to recipient@example.com --subject "Hello" --body "<p>HTML body</p>" --html
zoho-mail mail send --to recipient@example.com --cc cc@example.com --subject "Hello" --body "Body"
```

Reply to a message:

```
zoho-mail mail reply --id MESSAGE_ID --body "Reply text"
zoho-mail mail reply --id MESSAGE_ID --body "<p>HTML reply</p>" --html
```

Search messages:

```
zoho-mail mail search --query "from:someone@example.com"
zoho-mail mail search --query "subject:invoice" --limit 20
```

Delete a message:

```
zoho-mail mail delete --id MESSAGE_ID --folder FOLDER_ID
```

Mark messages as read or unread:

```
zoho-mail mail mark --ids id1,id2,id3 --read
zoho-mail mail mark --ids id1 --unread
```

## Folder commands

List all folders:

```
zoho-mail folders list
```

## Authentication commands

Complete the OAuth flow (interactive, run by operator):

```
zoho-mail auth login
```

Check authentication status:

```
zoho-mail auth status
```

Delete the stored token:

```
zoho-mail auth revoke
```

## Output format

All commands output JSON by default.

## Setup (operator, one-time per instance)

1. Set the account email address:
   ```
   zoho-mail config set --email trevor@example.com
   ```
2. Authenticate:
   ```
   zoho-mail auth login
   ```
   Visit the printed URL, authenticate, then paste the full redirect URL back into the terminal.
