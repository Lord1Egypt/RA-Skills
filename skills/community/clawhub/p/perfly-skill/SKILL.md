---
name: perfly-agent-sync
description: Summarize local coding work and submit selected worklog items to Perfly through the hosted Agent Sync MCP endpoint.
---

# Perfly Agent Sync

Use this skill when the user asks you to send today's work to Perfly, summarize local coding work for Perfly, or update a Perfly worklog.

## Requirements

Perfly Agent Sync requires the Perfly MCP server to be configured in the user's MCP client.

Production MCP endpoint:

```text
https://api.perfly.dev/mcp
```

Prefer MCP OAuth discovery when the client supports browser authorization. The user should only need to add the hosted MCP endpoint.

Use a write-only bearer ingestion token only as a fallback for environments that cannot complete browser OAuth, such as headless CLI, SSH, devcontainer, CI, or remote sandbox workflows.

If token fallback is required, the MCP client sends:

```text
Authorization: Bearer $PERFLY_INGESTION_TOKEN
```

## Workflow

1. Inspect only local context the user approved or clearly expects you to inspect.
2. Prefer metadata such as branch names, recent commit titles, issue keys, task ids, and user-provided notes.
3. Do not read or upload full diffs, source files, issue bodies, pull request bodies, logs, documents, secrets, or customer data.
4. Draft concise worklog items with one clear title per accomplishment.
5. Add a short note only when it improves later recall.
6. Use metadata-only evidence refs such as `git_commit:abc123`, `branch:feature/foo`, or `issue:ABC-123`.
7. Call `perfly_preview_work_items`.
8. Show the preview to the user and ask for confirmation before writing, unless the user explicitly enabled unattended submission.
9. After confirmation, call `perfly_add_work_items`.

## Payload Rules

- `date` must be the user's local work date in `YYYY-MM-DD`.
- `timezone` must be an IANA timezone, such as `Asia/Taipei`.
- `source` should identify the agent, such as `agent:codex`, `agent:claude-code`, `agent:cursor`, or `agent:local-cli`.
- `items` must contain 1 to 50 concise summaries.
- Use stable `idempotencyKey` values when possible, such as `git:<sha>`, `issue:<key>`, or `branch:<name>:<date>:<slug>`.

## Privacy Rules

Never submit:

- source code
- diffs
- full terminal logs
- secrets, tokens, passwords, or API keys
- customer data
- document bodies
- issue or pull request bodies
- attachments

If the user asks to include sensitive material, summarize at a higher level and explain that Perfly Agent Sync accepts summary metadata only.

If MCP is unavailable, explain how to set up Perfly Agent Sync with the hosted MCP endpoint first. Do not ask the user to paste an ingestion token directly into chat; if OAuth cannot work in the user's environment, direct them to create a fallback token in the Perfly app setup page.
