---
name: matter-cli
description: Interact with a user's Matter reading library using the Matter CLI. Use when asked to: browse inbox or reading queue, search articles by topic, get highlights or annotations, tag or archive articles, save new URLs, summarize articles, compile highlights into a digest, check reading progress, or manage the Matter library in any way. Triggers on: "my Matter library", "reading list", "inbox", "highlights", "queue", "saved articles", "reading queue", "Matter", "archive article", "tag article".
---

# Matter CLI Skill

## Setup (first time)
```bash
# Install (downloads binary directly from official GitHub releases)
# macOS arm64:
curl -fsSL https://github.com/getmatterapp/matter-cli/releases/latest/download/matter-darwin-arm64 -o ~/.matter/bin/matter && chmod +x ~/.matter/bin/matter

# macOS x86:
curl -fsSL https://github.com/getmatterapp/matter-cli/releases/latest/download/matter-darwin-x64 -o ~/.matter/bin/matter && chmod +x ~/.matter/bin/matter

# Linux arm64:
curl -fsSL https://github.com/getmatterapp/matter-cli/releases/latest/download/matter-linux-arm64 -o ~/.matter/bin/matter && chmod +x ~/.matter/bin/matter

# Linux x86:
curl -fsSL https://github.com/getmatterapp/matter-cli/releases/latest/download/matter-linux-x64 -o ~/.matter/bin/matter && chmod +x ~/.matter/bin/matter

# Add to PATH if needed
export PATH="$HOME/.matter/bin:$PATH"

# Authenticate
matter login
```
Source: <https://github.com/getmatterapp/matter-cli>
Requires a **Matter Pro** subscription. Get one at <https://web.getmatter.com/settings>.

CLI binary: `matter` (added to PATH after install)
Auth: Stored locally after `matter login`.
Full command reference: See [references/commands.md](references/commands.md)

## Core Workflows

### Browse Inbox
```bash
matter items list --status inbox --order inbox_position --limit 10
```

### Browse Reading Queue
```bash
matter items list --status queue --order library_position --limit 10
```

### Read / Summarize an Article
```bash
matter items get <id> --include markdown
```
Fetch markdown content, then summarize or analyze it.

### Search by Topic
```bash
matter search "<topic>" --type items --limit 10
```

### Get Highlights for an Article
```bash
matter annotations list --item <item_id> --all
```

### Tag an Article
```bash
matter tags list   # find or confirm tag id/name first
matter tags add --item <item_id> --name "<tag_name>"
```

### Archive an Article
```bash
matter items update <id> --status archive
```

### Save a New URL
```bash
matter items save --url "<url>" --status queue
```

### Compile Highlights Digest
1. Search or list items by topic/tag
2. For each item: `matter annotations list --item <id> --all`
3. Compile highlights into structured output

## Output Format
All commands return JSON by default. Use `--plain` for human-readable output.

**⚠️ Do NOT use `--all` for large libraries.** It streams all pages in one call and will hit rate limits mid-stream, corrupting the JSON response. Instead, paginate manually:
```bash
# First page
matter items list --status queue --order updated --limit 50 --plain

# Next page (use cursor from previous response)
matter items list --status queue --order updated --limit 50 --plain --cursor <cursor>
```
Repeat with each returned cursor until no cursor is shown. Add `sleep 5` between pages to stay within rate limits.

## Rate Limits

| Operation | Limit |
|-----------|-------|
| Read (list, get) | 120/min |
| Search | 30/min |
| Markdown (full text) | 20/min |
| Write (update, tag, archive) | 30/min |
| Save (new URLs) | 10/min |
| Burst | 5/min |

**Rules for bulk operations:**
- Fetching full markdown for multiple articles: `sleep 4` between each call (stays under 20/min)
- Running multiple searches back-to-back: `sleep 3` between each (stays under 30/min)
- Never fire more than 5 requests in rapid succession (burst limit)
- If you receive a `Rate limit exceeded. Retry after N seconds` error: stop immediately, wait the stated seconds + 5, then resume
- For research tasks across 5+ articles: fetch markdown sequentially with delays, not in parallel
