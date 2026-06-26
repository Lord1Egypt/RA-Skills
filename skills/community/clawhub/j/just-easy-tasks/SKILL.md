---
name: just-easy-tasks
description: "Use when an agent needs to work with Just Easy Tasks (JET) via the jet CLI or API: configure API key/context, find, create, update, complete, comment on, link, reference, or inspect tasks and project metadata."
version: 1.0.0
---

# JET

Use `jet` to manage Just Easy Tasks. Prefer CLI commands over raw API calls unless the user asks for API-level work.

## Setup

Install via `npm install -g @just-easy-tasks/jet`.

Configure only once per machine or project:

```sh
jet config set api-key <key>
jet use workspace <workspace-slug>
jet use project <PROJECT>
jet task list
```

`jet` defaults to `https://justeasytasks.com`. Override with `--api-url` or `JET_API_URL`. Settings can also come from `JET_API_KEY`, `JET_WORKSPACE`, `JET_PROJECT`, local `.jet/config.json`, or global config. Pass `--workspace` and `--project` to override implied context for one command.

## Agent Defaults

Use JSON and non-interactive mode:

```sh
jet --json --no-input task list
jet --json --no-input task get JET-123
```

Use `--refresh` when stale cached metadata is possible. Use `--no-cache` to bypass cache. Destructive commands prompt by default; pass `--force` when the user clearly requested deletion/revocation.

Admin mutation commands require `--dangerously-enable-admin-commands`. This flag allows changing shared workspace/project setup, membership/invites, boards, labels, statuses, task types, and priorities. Only use it when the user explicitly asks you to administer those shared settings; do not infer it from ordinary task work.

## Task Targets

Task targets may be:

- `JET-123`
- `acme/JET-123`
- `123` when a default project is set
- a title fragment resolved by the API

If resolution is ambiguous, inspect candidates and ask or use the full ref.

## Common Commands

```sh
jet context
jet workspace list
jet project list
jet task list [query] --status <key> --label <key>
jet task create "Title" --description "Details" --status open --priority high --label bug
jet task get JET-123
jet task update JET-123 --status in-progress --assignee <user-id>
jet task done JET-123
jet comment list JET-123
jet comment add JET-123 "Note"
jet link create JET-123 JET-124 --type blocks
jet reference create JET-123 https://example.com --title "Spec"
jet status list
jet label list
jet type list
jet priority list
```

For scripts, keep `--json --no-input` before the resource command, for example `jet --json --no-input task list --status open`.
