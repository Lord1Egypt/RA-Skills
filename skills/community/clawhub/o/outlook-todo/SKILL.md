---
name: outlook-todo
license: MIT
description: |
  Read and write Microsoft To Do via its own Microsoft Graph device-code login.
  Enumerate task lists, read/filter tasks, and create, update, complete, or delete tasks
  (writes require --apply plus a typed-YES prompt or an explicit --yes flag).
metadata:
  openclaw:
    emoji: "✅"
    requires:
      bins: ["bash", "jq", "curl", "python3"]
    network:
      allow:
        - "https://login.microsoftonline.com"
        - "https://graph.microsoft.com"
    files:
      write:
        - "~/.outlook-todo/"
---

# Outlook To Do

Use this skill to read and write the signed-in user's Microsoft To Do / Outlook.com task
lists and tasks through Microsoft Graph.

This skill has its own device-code login and token store (`~/.outlook-todo/`).
The consent requests exactly three delegated Microsoft Graph scopes:

- `offline_access`
- `https://graph.microsoft.com/User.Read`
- `https://graph.microsoft.com/Tasks.ReadWrite`

Mail, files, notes, directory, and Teams scopes are never requested.

Read operations may be automatic. Creating, updating, completing, or deleting tasks must require explicit user confirmation.
Non-interactive (agent) use must pass the explicit `--yes` flag — there is no
environment-variable bypass.

## First-time setup

You need a **public client** application registration in Entra ID (Azure AD) with
"Allow public client flows" = **Yes** and device-code flow enabled. This skill uses
the **device code flow** so it works on a headless host.

Azure app registration steps (bring your own — required once):

1. Portal → **Microsoft Entra ID** → **App registrations** → **New registration**.
2. Supported account types: **"Accounts in any organizational directory and personal Microsoft accounts"**.
3. No redirect URI needed. In the app → **Authentication** → set **"Allow public client flows"** = **Yes**.
4. Copy the **Application (client) ID** — that is the `--client-id` below. No client secret is required.

The setup script requests exactly these delegated Microsoft Graph scopes:
`offline_access`, `User.Read`, `Tasks.ReadWrite`.

```bash
cd ~/.openclaw/skills/outlook-todo
./scripts/setup-device-code.sh --client-id 12345678-1234-1234-1234-123456789012
# follow the printed URL, enter the code, finish the browser sign-in
```

The script writes:

| File | Mode | Content |
|---|---|---|
| `~/.outlook-todo/config.json` | 600 | client_id, tenant, authority, scopes, graph_base |
| `~/.outlook-todo/tokens.json` | 600 | access_token, refresh_token, expires_at, scope |

> **Important:** never commit `~/.outlook-todo/` to git. Use `--force` to overwrite.

## Read task lists

```bash
~/.openclaw/skills/outlook-todo/scripts/todo-read.sh lists --format summary
```

## Read tasks

```bash
# Default task list if Microsoft marks one as wellKnownListName=defaultList
~/.openclaw/skills/outlook-todo/scripts/todo-read.sh tasks --format summary

# Specific list by name or id
~/.openclaw/skills/outlook-todo/scripts/todo-read.sh tasks --list-name "Tasks" --format summary
~/.openclaw/skills/outlook-todo/scripts/todo-read.sh tasks --list-id '<LIST_ID>' --format json

# Include completed tasks
~/.openclaw/skills/outlook-todo/scripts/todo-read.sh tasks --status all --format summary
```

Formats: `summary`, `json`, `ids`, `raw`.

## Write tasks (explicit confirmation required)

`todo-write.sh` supports **create / update / complete / delete**. Every write defaults to
**dry-run** (prints the JSON payload; may perform read-only Graph lookups such as
resolving the default list or fetching the task to display — never writes).
Dry-run is not an offline mode. Pass `--apply` to execute.
Interactive runs are prompted to type `YES`; non-interactive runs must pass `--yes`.

```bash
# Create (dry-run preview, then real call)
~/.openclaw/skills/outlook-todo/scripts/todo-write.sh create --title "Buy milk" --due 2026-06-24
~/.openclaw/skills/outlook-todo/scripts/todo-write.sh create --title "Buy milk" --due 2026-06-24 --apply

# Update fields
~/.openclaw/skills/outlook-todo/scripts/todo-write.sh update --task-id '<ID>' --title "New title" --apply --yes

# Mark completed
~/.openclaw/skills/outlook-todo/scripts/todo-write.sh complete --task-id '<ID>' --apply --yes

# Delete (shows the task first)
~/.openclaw/skills/outlook-todo/scripts/todo-write.sh delete --task-id '<ID>' --apply --yes
```

## Token management

```bash
./scripts/token.sh status
./scripts/token.sh refresh
./scripts/token.sh scopes
./scripts/token.sh clear --yes-i-really-mean-it
```

## Files in this skill

| Path | Purpose |
|---|---|
| `SKILL.md` | this file |
| `scripts/setup-device-code.sh` | one-time device-code flow sign-in |
| `scripts/token.sh` | inspect / refresh / clear stored tokens |
| `scripts/_lib.sh` | shared helpers (sourced; not for direct use) |
| `scripts/todo-read.sh` | list task lists and tasks |
| `scripts/todo-write.sh` | create / update / complete / delete tasks |
| `references/graph-todo.md` | Microsoft Graph todo endpoint reference |

## Troubleshooting

- **`token scope does not include Tasks.ReadWrite`** — re-run `./scripts/setup-device-code.sh --force` to re-authenticate.
- **Empty results** — check that tasks exist in Outlook.com / Microsoft To Do.
- **`401 Unauthorized`** — run `scripts/token.sh refresh --force`; if that fails, re-run `scripts/setup-device-code.sh --force`.
