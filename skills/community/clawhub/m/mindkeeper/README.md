# Mindkeeper Skill

**Time Machine for Your AI's Brain** — install this skill if you want your AI to inspect history, show diffs, create checkpoints, and guide rollback in natural language.

This skill teaches the AI how to bootstrap and use the `mindkeeper-openclaw` plugin. It is the easiest way to get the OpenClaw Plugin experience without manually setting everything up first.

## Why Use It

- **Guided setup** — the AI checks whether the plugin is available and walks through first-use install
- **Safe permissions model** — plugin install and Gateway restart always require explicit confirmation
- **Natural-language usage** — ask about changes, diffs, rollback, and checkpoints conversationally
- **Rollback guardrails** — preview first, confirm second

## Install

```bash
clawhub install mindkeeper
```

On first use, the AI checks whether `mindkeeper-openclaw` is available. If it is missing, the AI asks for your confirmation before installing the plugin and before restarting Gateway. If automatic restart is unavailable, it tells you to restart Gateway manually.

## What It Enables

- **Browse history** — See what changed in `SOUL.md`, `AGENTS.md`, or any tracked file
- **Compare versions** — Full unified diff between any two commits
- **Rollback** — Restore any file to a previous version with preview + confirmation
- **Named snapshots** — Create checkpoints before risky changes
- **LLM commit messages** — Available in OpenClaw Plugin mode using your existing OpenClaw model and auth settings

## Requirements

- Node.js >= 22
- OpenClaw with Gateway running

The `mindkeeper-openclaw` plugin provides the actual `mind_*` tools and background watcher. This skill provides the guidance and first-use bootstrap behavior.

In OpenClaw Plugin mode, the AI should prefer the `mind_*` tools for history, diff, snapshot, and rollback tasks. CLI commands are mainly for setup, troubleshooting, or manual terminal workflows.

If you prefer to install the plugin yourself first:

```bash
openclaw plugins install mindkeeper-openclaw
# Then restart your Gateway
```

## Permissions & Why They Are Needed

| Action | Purpose |
|--------|---------|
| `openclaw plugins install mindkeeper-openclaw` | Fetches the official plugin and makes the `mind_*` tools available |
| Gateway restart | Loads the newly installed plugin into the running Gateway |

**User consent is required** before either action runs.

## How to Use

1. Install the skill: `clawhub install mindkeeper`
2. Ask your AI in natural language:
   - "What changed in SOUL.md recently?"
   - "Compare my current AGENTS.md to last week's version"
   - "Roll back SOUL.md to yesterday"
   - "Save a checkpoint called 'perfect-personality' before I experiment"

## Examples

| User says | AI action |
|-----------|-----------|
| "What changed in SOUL.md?" | `mind_history` with a file filter |
| "Show me the diff from last week" | `mind_history` → find commit → `mind_diff` |
| "Undo that change" | `mind_rollback` preview first, then execute after confirmation |
| "Save a checkpoint before I experiment" | `mind_snapshot` with a descriptive name |
| "Edit SOUL.md to change my tone" | Edit the file directly; mindkeeper should track the change automatically |

## Troubleshooting

- **History is empty** — Call `mind_status` to check whether mindkeeper is initialized. Make a small edit to a tracked file to trigger the first snapshot.
- **Tools not found** — Ensure the `mindkeeper-openclaw` plugin is installed and Gateway has been restarted.
- **Rollback not applying** — After rollback, run `/new` to reload the session with the restored file.

## Links

- [mindkeeper on GitHub](https://github.com/seekcontext/mindkeeper)
- [mindkeeper-openclaw on npm](https://www.npmjs.com/package/mindkeeper-openclaw)
