---
name: memos-cli
description: Use when a user needs to read, search, create, update, delete, comment on, tag, or inspect Memos data through this repository's Go CLI, especially when the agent should prefer real project commands over guessing HTTP API calls.
---

# memos-cli — Repository Memos CLI Skill

**Install:** `go install github.com/rogeecn/memos-cli@latest`  
**Binary form:** `memos-cli`  
**Primary purpose:** Use this repository's Go CLI to perform Memos operations from the terminal.

## Overview

This repository contains a Go CLI named `memos` for common Memos operations.

Agents should prefer this CLI when the user asks to list memos, fetch memo details, search content, apply CEL filters, create or update memos, delete memos, add comments, remove tags, or inspect users. The CLI already handles configuration loading, JSON output, memo formatting, and memo ID normalization behavior implemented in the repo.

## When to Use

Use this skill when:
- The user wants to inspect or modify Memos data from this repository
- The task should use the repo's real command surface instead of handwritten HTTP requests
- The user needs terminal output or structured JSON from Memos commands
- The agent needs a safe preflight check for local config before calling Memos APIs

Do not use this skill when:
- The user is asking to develop the CLI itself rather than use it
- The task is purely about source code changes with no need to run Memos commands

## Setup

Install the CLI first:

```bash
go install github.com/rogeecn/memos-cli@latest
```

Then run it as a normal installed binary:

```bash
memos-cli --help
```

Use `memos-cli` as the canonical entrypoint. Do not use `go run .` in this skill.

## Configuration

**IMPORTANT FOR AGENTS**: Before executing any command that talks to the Memos API, first run:

```bash
memos-cli config check
```

The CLI reads configuration with this precedence:
1. Shell environment variable
2. Current directory `.env`
3. Missing

Expected variables:

```env
MEMOS_URL=http://localhost:5230
MEMOS_API_KEY=your-api-key
MEMOS_ADMIN_API_KEY=your-admin-api-key
DEFAULT_TAG=cli
```

### Preflight Rules

- If `MEMOS_URL` is `missing`, stop and ask the user for the Memos base URL
- If `MEMOS_API_KEY` is `missing`, stop and ask the user to provide or export it
- If the task needs `user list`, also require `MEMOS_ADMIN_API_KEY`
- Do not print secret values back to the user
- Do not suggest editing committed files for secrets; prefer shell env vars or local `.env`

## Output Format

### Default: human-readable text

```bash
memos-cli memo list
memos-cli memo get <memo-id>
```

### Structured output: `--json`

Use `--json` whenever the task needs machine-readable data, IDs for follow-up steps, or filtering with shell tools.

```bash
memos-cli --json memo list
```

## Command Reference

### Configuration

```bash
memos-cli config check
```

### Read Operations

```bash
memos-cli memo list
memos-cli memo list --page-size 20
memos-cli memo list --page-token <token>
memos-cli memo get <memo-id>
memos-cli search "keyword"
memos-cli filter --expr "visibility == 'PRIVATE'"
memos-cli user list
```

### Write Operations

The `content` field supports Markdown. Agents can pass plain text or Markdown content to memo and comment commands.

```bash
memos-cli memo create "# Weekly Note\n\n- shipped feature\n- fixed bug"
memos-cli memo create "memo content" --tag release --tag cli
memos-cli memo create "memo content" --visibility PUBLIC
memos-cli memo update <memo-id> --content "## Updated\n\nThis memo now uses **Markdown**."
memos-cli memo update <memo-id> --visibility PUBLIC
memos-cli memo delete <memo-id> --yes
memos-cli comment create <memo-id> "Looks good.\n\n- reviewed\n- approved"
memos-cli tag remove <memo-id> <tag>
```

## Agent Workflows

### List memos safely

```bash
memos-cli config check
memos-cli memo list
```

Note: `memo list` lists memos using the API default ordering. Treat it as the current list view, not a guaranteed dedicated `recent` command.

### List memos as JSON for follow-up actions

```bash
memos-cli config check
memos-cli --json memo list
```

### Fetch one memo before updating it

```bash
memos-cli memo get <memo-id>
memos-cli memo update <memo-id> --content "new content"
```

### Search then inspect the matching memo

```bash
memos-cli --json search "deploy"
memos-cli memo get <memo-id>
```

### Filter with CEL expression

```bash
memos-cli filter --expr "createTime > timestamp('2026-01-01T00:00:00Z') && visibility == 'PRIVATE'"
```

### Paginate through memo lists

```bash
memos-cli memo list --page-size 20
memos-cli memo list --page-size 20 --page-token <next-token>
```

In text mode, the CLI prints `Next page token: ...` when another page exists. In JSON mode, inspect `nextPageToken`.

### Create a memo with default and explicit tags

```bash
memos-cli memo create "ship checklist ready" --tag release --tag weekly
```

The CLI appends `DEFAULT_TAG` automatically when configured.

### Delete a memo safely

```bash
memos-cli memo delete <memo-id> --yes
```

Deletion requires explicit `--yes`. If the user asks to delete a memo and has not clearly confirmed, ask before running it.

### List users via admin API

```bash
go run . config check
go run . user list
```

If `MEMOS_ADMIN_API_KEY` is missing, stop and ask the user to provide admin credentials.

## ID Rules

- Prefer passing the memo's plain ID, such as `abc123`
- Do not invent `memos://` or other URI forms for CLI commands
- `comment create` and `tag remove` work with memo IDs and rely on the client behavior already implemented in the repo

## Error Reference

| Error or symptom | Likely cause | Agent action |
|---|---|---|
| `MEMOS_URL is required` | Base URL missing | Ask user for `MEMOS_URL` or local `.env` |
| `MEMOS_API_KEY is required` | API key missing | Ask user for `MEMOS_API_KEY` |
| `MEMOS_ADMIN_API_KEY is required` | Admin command without admin key | Ask user for admin key before `user list` |
| `update requires --content or --visibility` | Update called with no changes | Re-run with at least one change flag |
| `delete requires --yes` | Delete missing confirmation flag | Re-run only after explicit confirmation |
| empty or unexpected search results | Filter/query too narrow or API data differs | Try `--json` and inspect returned structure |
| next page not visible | Pagination token not supplied | Re-run with `--page-token` |

## Safety Notes

- Treat API keys as secrets; never echo them back in full
- Prefer `config check` over guessing whether configuration exists
- Prefer `--json` for agent follow-up logic and ID extraction
- Avoid destructive commands unless the user explicitly requested them
- Do not commit `.env` or other local secret material

## Common Mistakes

- Using `go run .` or `go run ./cmd/memos` instead of the installed `memos-cli` binary
- Running API commands before `config check`
- Forgetting `--json` when later steps need a memo ID or token
- Assuming `memo list` is a dedicated `recent` endpoint rather than the default list API
- Forgetting `--yes` for deletions
- Calling `user list` without admin credentials

## Quick Reference

- Install: `go install github.com/rogeecn/memos-cli@latest`
- Preflight: `memos-cli config check`
- List memos: `memos-cli memo list`
- List as JSON: `memos-cli --json memo list`
- Get one memo: `memos-cli memo get <memo-id>`
- Search text: `memos-cli search "keyword"`
- CEL filter: `memos-cli filter --expr "..."`
- Create memo: `memos-cli memo create "content"`
- Update memo: `memos-cli memo update <memo-id> --content "..."`
- Delete memo: `memos-cli memo delete <memo-id> --yes`
- Add comment: `memos-cli comment create <memo-id> "..."`
- Remove tag: `memos-cli tag remove <memo-id> <tag>`
- List users: `memos-cli user list`
