---
name: gmail-no-send
description: Read-only Gmail CLI that cannot send email by design. Search, read, create drafts, update drafts, and archive messages — with zero send capability in the codebase. Use when the agent needs Gmail access for reading email, drafting responses, searching inbox, or archiving messages, but sending must be impossible. Ideal for AI agents that should never autonomously send email. Requires Google Cloud OAuth credentials (user provides their own client_secret.json).
metadata: {"openclaw":{"security":"No send endpoints exist in code. OAuth scope includes compose (Gmail has no drafts-only scope), but send is enforced absent at the application layer. All operations are audit-logged.","author":"Mei Park (@meimakes)","homepage":"https://github.com/meimakes/gmail-no-send"}}
---

# gmail-no-send

Gmail CLI that **cannot send email**. Not "won't" — *can't*. There is no send function in the codebase.

## Install

Requires Python 3.9+.

```bash
cd <skill-dir>/scripts/gmail-no-send
pip install -e .
```

Or install from the GitHub repo:
```bash
pip install git+https://github.com/meimakes/gmail-no-send.git
```

## First-Time Auth

Each user needs their own Google Cloud OAuth credentials:

1. Create a project at console.cloud.google.com
2. Enable the Gmail API
3. Create OAuth 2.0 credentials (Desktop app type)
4. Download `client_secret.json`

Then authenticate:
```bash
gmail-no-send auth --client-secret /path/to/client_secret.json --account myname
```

This opens a browser for Google OAuth consent. Token is saved to `~/.config/gmail-no-send/token.json` and auto-refreshes.

## Commands

All commands require `--account <name>` (matches the name used during auth).

### Search
```bash
gmail-no-send search --account mei --query "from:someone@example.com newer_than:7d" --max 10
```
Returns JSON array of message IDs and thread IDs.

### Read
```bash
gmail-no-send read --account mei --message-id <id>
```
Returns full message payload (headers, body, labels).

### Create Draft
```bash
gmail-no-send draft-create --account mei --to "someone@example.com" --subject "Re: topic" --body "Draft text here"
gmail-no-send draft-create --account mei --to "someone@example.com" --subject "Long draft" --body-file /path/to/body.txt
```

### Update Draft
```bash
gmail-no-send draft-update --account mei --draft-id <id> --to "someone@example.com" --subject "Updated" --body "New body"
```

### Archive
```bash
gmail-no-send archive --account mei --message-id <id>
```
Removes INBOX label (message stays in All Mail).

## Security Model

- **No send command exists.** The CLI has 6 commands: auth, search, read, draft-create, draft-update, archive. None send.
- **OAuth scope caveat:** Gmail API has no "drafts-only" scope. The `compose` scope technically allows send via API. This tool enforces no-send at the application layer — the code simply doesn't call the send endpoint.
- **Audit log:** All operations logged to `~/.config/gmail-no-send/audit.log` with timestamps.
- **Token storage:** `~/.config/gmail-no-send/token.json` — user-local, not shared.

For a deeper security analysis, see [references/threat-model.md](references/threat-model.md).

## Agent Usage Notes

- Search returns message IDs, not content. Call `read` to get the actual message.
- Draft creation returns the draft ID for future updates.
- Use `--body-file` for long draft bodies instead of `--body` to avoid shell escaping issues.
- The tool does NOT support attachments, labels, or filters — intentionally minimal.
