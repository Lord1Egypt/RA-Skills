---
name: openclaw-git-manager
description: >
  Use when you want to track, commit, compare, or rollback OpenClaw configuration changes.
  Triggers when the user mentions "commit the config", "save this version",
  "what changed in my config", "restore the previous config", "rollback",
  "config history", or "git manager". Also activates when OpenClaw configuration
  files (openclaw.json, credentials, skills) have been modified and need a
  stable versioned checkpoint before further changes.
license: MIT
metadata:
  version: "1.0"
  category: dev-tools
  author: wangjipeng
---

# OpenClaw Git Manager

Version control for OpenClaw configuration files — commit with diff, compare
history, rollback to any previous version.

## Core Position

Every config change without a git record is a potential data loss event.
This skill turns OpenClaw config management from "hope nothing breaks" into
"I can always go back."

**What it tracks:**
- `~/.openclaw/openclaw.json` — main configuration
- `~/.openclaw/credentials/*.json` — credentials profiles
- `~/.openclaw/agents/` — agent definitions
- `~/.openclaw/flows/` — flow definitions
- `~/.openclaw/skills/` — custom skill configurations

**What it does NOT track:** `memory/`, `logs/`, `media/`, `tmp/`, `trash/`,
`canvas/`, `npm/`, `completions/`, `service-env/`, `tasks/`, `.DS_Store`.

## Repository Setup

On first use, the skill initializes a git repo in `~/.openclaw/` if one does not
exist, configured with a proper `.gitignore` that excludes runtime data.

## Modes

### `/openclaw-git-manager commit`

Stage and commit the current config state with a human-readable message.

Use it when:
- Config was just modified (via wizard, manual edit, or skill)
- Before making risky changes to openclaw.json
- After a successful `doctor` or `config` run that changed state

Execution steps:
1. Inspect which tracked files have changed since last commit (git status)
2. For each changed file, show a concise diff summary (changed keys, not full content)
3. Ask the user to confirm or edit the commit message
4. Stage all changed tracked files
5. Commit with the message, prefixed with `config:`
6. Report the commit hash and number of files changed

Do not:
- Commit raw secrets or real API keys (warn if credentials/ contains real keys)
- Commit binary or cache files
- Make commits without describing what changed

### `/openclaw-git-manager log`

Show the commit history with one-line summaries and diff overviews.

Use it when:
- The user wants to see what changed and when
- Diagnosing a config regression (when did this break?)
- Finding a known-good version to restore

Execution steps:
1. Run `git log --oneline -20` to show recent commits
2. For each commit, show: short hash, relative time, first line of message
3. If the user asks for a specific commit's details, show full diff:
   `git show <hash> --stat` (files) + `git show <hash>` (patch)
4. Present commits newest-first with commit numbers for easy reference

Do not:
- Show full file contents for large files
- Include excluded paths in the diff output

### `/openclaw-git-manager diff`

Show exactly what changed between commits or between the working tree and HEAD.

Use it when:
- Comparing current uncommitted state vs last commit
- Comparing two historical commits
- Verifying what a rollback would change

Execution steps:
1. If no arguments: show diff of all unstaged changes vs HEAD
2. If `--from <commit> --to <commit>`: show diff between two commits
3. Format diffs with file headers and +/- line counts per file
4. For JSON files, optionally render as structured key: value changes
5. Summarize: N files changed, N insertions, N deletions

Do not:
- Show binary diffs (use "file changed, N bytes")
- Show excluded paths (memory/, logs/, etc.)

### `/openclaw-git-manager restore`

Roll back to a previous commit or restore specific files.

Use it when:
- A config change broke something and the user wants to go back
- The user identified a good commit from `log` and wants to restore it
- The user says "undo this" or "go back to before"

Execution steps:
1. If the user names a commit (hash or number from `log`): restore full tree to that commit
2. If the user names a specific file: restore only that file to the commit's version
3. Show a preview diff first: what will change from current state
4. Require user confirmation before overwriting current files
5. After restore, create an automatic recovery commit marking the restore point:
   `config: restore to <hash> (<description>)`
6. Report which files were changed and the new HEAD commit

Restore modes:
- **Full tree restore**: `git checkout <commit> -- .` (all tracked files)
- **Single file restore**: `git checkout <commit> -- path/to/file`
- **Hard reset** (destructive): `git reset --hard <commit>` — only if user explicitly says "hard reset"

Do not:
- Perform destructive restores (hard reset, force checkout) without explicit user confirmation
- Restore to a commit that is not an ancestor of HEAD (detached HEAD risk)

### `/openclaw-git-manager status`

Show the current state of the working tree.

Use it when:
- The user asks "what's the current config state?"
- Before committing, to verify which files will be captured
- After a restore, to verify the tree is clean

Execution steps:
1. Run `git status --short` for a concise view
2. Show: number of commits ahead/behind remote (if any), current branch
3. List any uncommitted changes with file names
4. Report whether the tree is "clean" or "N file(s) changed"

Do not:
- Show full diffs in status mode (use `diff` for that)

## Execution Steps

The entry point is always `scripts/git_manager.py`, invoked from `~/.openclaw/`.

```bash
# From ~/.openclaw/ directory
python3 ~/.openclaw/workspace/skills/openclaw-git-manager/scripts/git_manager.py <command> [args]

# Commands: commit, log, diff, restore, status
```

The script resolves its location relative to the installed skill directory,
not the active working directory.

## Config File Locations

| File | Path | Notes |
|------|------|-------|
| Main config | `~/.openclaw/openclaw.json` | Primary tracked file |
| Credentials | `~/.openclaw/credentials/*.json` | Contains real keys — never expose raw |
| Agents | `~/.openclaw/agents/` | Agent definitions |
| Flows | `~/.openclaw/flows/` | Flow definitions |
| Custom skills | `~/.openclaw/workspace/skills/` | Custom skill configs |

## Gitignore Rules (Embedded)

The following are excluded from tracking:

```
# Runtime data (excluded)
memory/
logs/
media/
tmp/
trash/
canvas/
npm/
completions/
service-env/
tasks/
.DS_Store

# Node.js / npm
node_modules/
package-lock.json

# Editor
*.swp
*.swo
.vscode/
.idea/

# OpenClaw internals (not user config)
cron/
devices/
exec-approvals.json
update-check.json
skills-trigger-index.json
subagents/
delivery-queue/
```

## Do Not

- Commit real API keys, bearer tokens, or passwords — redact them first
- Use `git push` — this is a local-only record, not a shared repo
- Merge branches — keep history linear to avoid restore complexity
- Modify `.git/` directory directly — always go through git commands
- Track `memory/` or `logs/` — these are runtime data, not configuration

## Quality Bar

A good commit message should let a future reader answer:
- **What changed?** (a specific config key, file, or group of settings)
- **Why?** (the intent behind the change — "enabled TTS", not "updated json")
- **What was the previous state?** (visible in the diff)

Example commit messages:
- ✅ `config: enable minimax TTS in production profile`
- ✅ `config: add claude-sonnet model to local provider list`
- ✅ `config: rollback agent definitions to pre-migration state`
- ❌ `config: update`
- ❌ `config changes`
- ❌ `stuff`

## Good vs Bad Commit Messages

| Good | Bad |
|------|-----|
| `config: enable minimax TTS in production profile` | `config update` |
| `config: add claude-sonnet to model list` | `model change` |
| `config: restore openclaw.json to pre-wizard state` | `restore` |
| `config: migrate agent definitions to new format` | `migration` |
| `config: disable noisy plugin auto-update` | `changed settings` |

## Log Format

```
commit a1b2c3d  2 hours ago  config: enable minimax TTS
commit b2c3d4e  yesterday   config: add claude-sonnet to providers
commit c3d4e5f  3 days ago   config: initial checkpoint
```

## Rollback Output Contract (MANDATORY)

Every restore use must end with:
1. `Files restored` — list of files changed
2. `New HEAD` — the commit hash the tree now points to
3. `Previous state` — what was the previous commit (for undo purposes)
4. `Next action` — what the user should do next (e.g., "restart gateway")

## Skill Fit

This skill solves one specific problem: **config changes without visibility or reversibility**.

It does NOT replace backup solutions, cloud sync, or team collaboration workflows.