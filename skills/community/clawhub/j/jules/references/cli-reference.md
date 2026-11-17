# Jules CLI Reference

## Command overview

Jules Tools (`jules`) provides an async interface to Google's cloud coding agent.

### Global flags

- `-h, --help`: Displays help for any command.
- `--theme <dark|light>`: Sets theme for interactive TUI (default: `dark`).

### Commands

#### `jules` (TUI mode)
Launches the full interactive TUI dashboard. Provides:
- Visual session list with execution status.
- Side-by-side patch and diff viewer.
- Session creation wizards.

#### `jules new`
Submits a new coding task to Jules.
- Arguments: Task prompt string or piped stdin.
- Flags:
  - `--repo <owner/repo>`: Target repository (defaults to git remote of current directory).
  - `--parallel <1-5>`: Number of independent parallel attempts to spawn for the task.

#### `jules remote`
Top-level command for managing remote cloud sessions.
- `jules remote list --session`: List all cloud sessions (status, ID, task).
- `jules remote list --repo`: List all repos linked to Jules account.
- `jules remote pull --session <id>`: Fetch generated patch diff.
- `jules remote pull --session <id> --apply`: Fetch and apply patch directly to local working tree.

#### `jules teleport <session_id>`
One-shot bootstrap to synchronize local state with a session.
- Outside a repo: Clones repo from origin, checks out base branch, applies patch.
- Inside matching repo: Applies patch to existing tree.

#### `jules login` / `jules logout`
- `jules login`: Launches browser OAuth flow for Google Account authentication.
- `jules logout`: Purges cached credentials.

#### `jules completion <shell>`
Generates autocompletion script (supports `bash`, `zsh`, `fish`).

## Automation recipes

### 1. Batch issue processing from GitHub CLI

```bash
# Pick first assigned issue and dispatch to Jules
gh issue list --assignee @me --limit 1 --json title,body --jq '.[0] | "\(.title)\n\(.body)"' | jules new
```

### 2. Multi-strategy task exploration

```bash
# Spawn 3 parallel approaches for architectural or tricky refactoring
jules new --parallel 3 "Optimize database query performance in reports/monthly.go"
```

### 3. Pipeline CI or script integration

```bash
# Pull diff and verify before applying
jules remote pull --session "$SESSION_ID" > changes.patch
if git apply --check changes.patch; then
  git apply changes.patch
  npm test
fi
```
