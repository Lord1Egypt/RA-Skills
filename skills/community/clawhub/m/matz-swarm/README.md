# Agent Swarm Orchestrator

Multi-project coding automation: task intake → AI coding → AI review → MR/PR → merge.

## Quick Start

### 1. Install

```bash
mkdir -p ~/agent-swarm/{scripts,logs,projects}
cp scripts/*.sh ~/agent-swarm/scripts/
chmod +x ~/agent-swarm/scripts/*.sh
```

### 2. Configure

Create `~/agent-swarm/registry.json`:

```json
{
  "config": {
    "gitProvider": "gitlab",
    "gitUser": "YourUsername",
    "codingAgent": "claude",
    "reviewAgent": "codex",
    "notifyMethod": "openclaw",
    "notifyTarget": "your-chat-id",
    "notifyChannel": "telegram",
    "obsidianDir": "~/Documents/Obsidian Vault/agent-swarm",
    "worktreeBase": "~/GitLab/worktrees",
    "repoBase": "~/GitLab/repos"
  },
  "projects": {}
}
```

**Config options:**

| Key | Values | Description |
|-----|--------|-------------|
| `gitProvider` | `gitlab` \| `github` | Git hosting provider |
| `gitUser` | string | Your username on the provider |
| `codingAgent` | `claude` \| `codex` \| `aider` | AI agent for coding tasks |
| `reviewAgent` | `codex` \| `claude` \| `none` | AI agent for code review |
| `notifyMethod` | `openclaw` \| `webhook` \| `none` | Notification delivery |
| `notifyTarget` | string | Chat ID (openclaw) or webhook URL |
| `notifyChannel` | string | Channel for openclaw (e.g. `telegram`) |
| `obsidianDir` | path \| `""` | Obsidian vault path, empty to disable |
| `worktreeBase` | path | Where git worktrees are created |
| `repoBase` | path | Where project repos live |

All config values can also be overridden via environment variables with `SWARM_` prefix (e.g. `SWARM_GIT_PROVIDER=github`).

### 3. Initialize tasks file

```bash
echo '{"tasks":[]}' > ~/agent-swarm/tasks.json
```

### 4. Add a project

```bash
~/agent-swarm/scripts/new-project.sh my-project
```

Or manually add to `registry.json`:

```json
{
  "projects": {
    "my-project": {
      "repo": "git@gitlab.com:You/my-project.git",
      "base_branch": "main",
      "worktree_base": "~/GitLab/worktrees",
      "local_repo": "~/GitLab/repos/my-project",
      "context_path": "context.md"
    }
  }
}
```

### 5. Set up cron

```bash
crontab -e
```

```
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
*/3 * * * * ~/agent-swarm/scripts/check-agents.sh
*/5 * * * * ~/agent-swarm/scripts/scan-obsidian.sh
0 3 * * * ~/agent-swarm/scripts/cleanup.sh
```

### 6. Prerequisites

| Tool | Required for | Install |
|------|-------------|---------|
| `claude` | Coding (default) | `npm i -g @anthropic-ai/claude-code` |
| `codex` | Review (default) | `npm i -g @openai/codex` |
| `glab` | GitLab MR ops | `brew install glab` |
| `gh` | GitHub PR ops | `brew install gh` |
| `jq` | JSON parsing | `brew install jq` |
| `tmux` | Agent sessions | `brew install tmux` |
| `python3` | Task management | (usually pre-installed) |

Only install the tools for your chosen providers.

**Claude Code setup** (if using `claude` as coding agent):
```bash
# Authenticate
claude login

# Skip permission prompts (required for automation)
# In ~/.claude/settings.json:
{ "skipDangerousModePermissionPrompt": true }

# Trust worktree directories (avoids trust dialog per worktree)
# Run once in each base directory:
cd ~/GitLab/worktrees && claude   # accept trust dialog
cd ~/GitLab/repos && claude       # accept trust dialog
```

## Usage

### Spawn a task
```bash
~/agent-swarm/scripts/spawn-agent.sh <project> "<task description>"
```

### Monitor
```bash
tmux attach -t agent-<task-id>
tail -f ~/agent-swarm/logs/<task-id>.log
```

### Merge a completed MR
```bash
~/agent-swarm/scripts/merge-and-sync.sh <project> <mr-number>
```

### Sync local repo to latest main
```bash
~/agent-swarm/scripts/sync-project-main.sh <project>
```

## How It Works

```
spawn-agent.sh
  ├── Creates git worktree + feature branch
  ├── Builds prompt (task + project context)
  └── Launches tmux → run-agent.sh
                         ├── Runs coding agent (claude -p)
                         └── Triggers review-and-push.sh
                               ├── Runs review agent
                               ├── CRITICAL/HIGH → auto-fix retry (max 2)
                               ├── MEDIUM → auto-fix (non-blocking)
                               ├── LOW → notes in MR only
                               ├── Push + create MR/PR
                               └── Notify → ready_to_merge

check-agents.sh (cron every 3min)
  ├── Dead agent + commits → trigger review
  ├── Running >60min → timeout alert
  └── MR merged → mark done + sync main

scan-obsidian.sh (cron every 5min)
  └── Obsidian note status: ready → auto-spawn

cleanup.sh (daily 3am)
  └── Archive old tasks, remove worktrees, clean logs
```

## Obsidian Integration (Optional)

Create notes in your configured `obsidianDir`:

```markdown
---
project: my-project
status: active
---

## Tasks

### Add user auth
status: ready
priority: high
> Implement JWT authentication for the /api/login endpoint

### Fix homepage layout
status: draft
> Adjust the grid spacing on mobile
```

- `status: ready` → auto-spawned within 15 minutes
- `status: draft` → ignored until you change it
- Frontmatter `status: stop` → skip entire project

## File Structure

```
~/agent-swarm/
├── registry.json          # Project configs + global settings
├── tasks.json             # Task state machine
├── scripts/
│   ├── config.sh          # Shared config (all scripts source this)
│   ├── spawn-agent.sh
│   ├── run-agent.sh
│   ├── review-and-push.sh
│   ├── check-agents.sh
│   ├── scan-obsidian.sh
│   ├── send-notifications.sh
│   ├── merge-and-sync.sh
│   ├── sync-project-main.sh
│   ├── new-project.sh
│   └── cleanup.sh
├── logs/                  # Task logs + notifications
└── projects/              # Per-project overrides (context.md lives in project repo)
```

## License

MIT
