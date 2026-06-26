---
name: email-reader
description: Read/search Gmail via gog CLI. Inbox check, email search, content retrieval.
user-invocable: true
tools: Bash
metadata: {"openclaw":{"emoji":"📬","requires":{"bins":["gog"],"env":["GOG_ACCOUNT"]}}}
---

# email-reader

## When to use
User asks to check inbox, search emails, read email content, or summarize recent messages.

## Commands

```bash
# List unread (default action)
gog gmail search 'in:inbox is:unread' --max 5 --format minimal --json

# Search by criteria (use Gmail search syntax)
gog gmail search '<query>' --max 10 --format minimal --json

# Read full email
gog gmail get <message_id> --format full --json

# Get thread
gog gmail thread <thread_id> --format minimal --json
```

## Workflow
1. Verify `gog` on PATH and `GOG_ACCOUNT` set
2. Build Gmail search query from user intent — ask if ambiguous
3. Run `gog gmail search` with `--format minimal --json --max N`
4. Parse JSON → present formatted list (sender, subject, date, snippet, ID)
5. Offer: read full email, refine search, or act on message

## Output format

```
📬 [count] emails:
1. **From:** Name <email> | **Subject:** … | **Date:** YYYY-MM-DD HH:MM
   Preview: … | ID: msg_xxx
```

## Rules
- ALWAYS use `--format minimal --json --max N` (default N=5)
- Never show raw JSON; never fetch full content unless asked
- Preserve message IDs for follow-up actions
- Empty results → confirm criteria, suggest broader terms
- Read-only; send/reply requires email-responder skill
- Never store email content in MEMORY.md unless user requests

## Error handling
- `gog` missing → show install: `npm i -g gogcli` or `brew install gogcli`
- `GOG_ACCOUNT` unset → ask user for Gmail address
- Token expired → `gog auth add <email>`
- API error → show error, suggest fix

## Gmail search operators
`from:` `to:` `subject:` `label:` `is:unread` `is:starred` `has:attachment` `newer_than:Nd` `older_than:Nd` `in:inbox` `in:sent` `filename:ext`
