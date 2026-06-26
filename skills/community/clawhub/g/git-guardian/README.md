# Git Guardian

An [OpenClaw](https://openclaw.ai) skill that enforces transparent, git-tracked workflows for AI agent file operations.

## The Problem

AI agents create and modify files constantly — scripts, configs, documents — but users often have no visibility into what changed, when, or why. Changes happen silently, making it hard to review, audit, or roll back agent work.

## The Solution

Git Guardian enforces a simple rule: **show the diff before you apply it.**

Every file operation the agent performs is:
1. **Branched** — changes happen on feature branches, never directly on main
2. **Diffed** — the user sees exactly what changed before it's finalized
3. **Committed** — every change gets a clear commit message
4. **Pushed** — work is pushed to remote for review and history

## Quick Start

Install the skill:
```bash
openclaw skills install git-guardian
```

The skill activates automatically when the agent creates or modifies files. It will:
- Create a feature branch for the work
- Show you a `git diff` before committing
- Wait for your approval before finalizing
- Push and provide a review link

## Helper Script

Includes `git-guardian.sh` for common operations:

```bash
# Start tracked work (creates a branch)
git-guardian.sh start "add new integration"

# See what changed
git-guardian.sh diff

# Commit approved changes
git-guardian.sh commit "added PostHog MCP config"

# Push and get review link
git-guardian.sh finish

# Quick status check
git-guardian.sh status
```

## When It Kicks In

- **Branch + full diff:** Multi-file changes, new features, config modifications
- **Inline diff:** Single-line fixes, typo corrections (still committed, just less ceremony)

## What's NOT Tracked

- Ephemeral files (`/tmp/`, session state, working buffers)
- Secrets (API keys, tokens, credentials)
- Large binaries (referenced, not committed)

## Why This Matters

Trust is built on transparency. When an AI agent modifies your files, you should be able to:
- **See** exactly what changed (diff)
- **Understand** why it changed (commit message)
- **Approve** before it takes effect (review step)
- **Revert** if something goes wrong (git history)

## License

MIT
