---
name: plane-cli
version: 0.1.0
description: "Plane.so: Create, update, and manage issues, projects, states, labels, and pages. Use when the user wants to interact with Plane.so — creating issues, listing tasks, updating status, managing labels, or any project-management workflow."
metadata:
  openclaw:
    emoji: "✈️"
    category: "productivity"
    requires:
      bins: ["plane"]
      env: ["PLANE_API_KEY", "PLANE_WORKSPACE_SLUG"]
    cliHelp: "plane --help"
---

# Plane CLI

CLI for [Plane.so](https://plane.so) project management. Output is JSON by default — pipe to `jq` or consume directly.

## Setup

```bash
uv tool install plane-cli   # or: pip install plane-cli
plane config init            # interactive setup wizard
```

Config: `~/.config/plane-cli/config.toml`. All values can be set via env vars (`PLANE_API_KEY`, `PLANE_WORKSPACE_SLUG`, `PLANE_BASE_URL`, `PLANE_PROJECT`) or CLI flags.

## Command Discovery

Do not guess command names or options. Use `--help`:

```bash
plane --help
plane issues --help
plane issues create --help
```

## Quick Reference

| Resource | Key commands |
|----------|-------------|
| `plane projects` | `list`, `get`, `create --name`, `update`, `delete` |
| `plane issues` | `list`, `get`, `create --title`, `update`, `delete` |
| `plane issues comment` | `list <issue-id>`, `add <issue-id> --body` |
| `plane states` | `list`, `get`, `create --name --color`, `update`, `delete` |
| `plane labels` | `list`, `get`, `create --name`, `update`, `delete` |
| `plane pages` | `list`, `get`, `create --name`, `update`, `delete` |

## Common Workflows

**Create an issue:**
```bash
plane issues create --title "Fix login bug" --priority high --state <state-id>
```

**List issues with filters:**
```bash
plane issues list --state <state-id> --assignee <user-id> --all
```

**Update issue state (move to "In Progress"):**
```bash
# First, find the state ID
plane states list --project <pid>
# Then update
plane issues update <issue-id> --state <state-id>
```

**Add a comment (supports stdin with `-`):**
```bash
plane issues comment add <issue-id> --body "Deployed to staging"
git diff HEAD~1 | plane issues comment add <issue-id> --body -
```

## Important Conventions

- `--project` is optional when `defaults.project` is configured
- Destructive commands (`delete`) require `--yes` in non-TTY (agent) contexts
- `--description` and `--body` accept `-` to read from stdin
- `--all` fetches all pages (capped at 1000); default is first 20 results
- `--pretty` renders Rich tables — avoid in scripts, parse JSON instead
- Errors go to stderr as JSON: `{"error": {"type": "...", "message": "...", "status_code": N}}`
- Exit codes: `0` success, `1` error, `2` rate-limited (retry safe)

> [!CAUTION]
> `delete` commands are destructive — always confirm with the user before executing.
