---
name: jj-mailbox
version: "0.1.3"
description: "Send and receive messages between AI agents using jj (Jujutsu) version control as a file-based mailbox. Enables cross-machine agent collaboration with zero infrastructure beyond a git remote."
tags: ["messaging", "agents", "jujutsu", "jj", "version-control", "multi-agent", "collaboration"]
metadata:
  openclaw:
    requires:
      bins: ["jj-mailbox", "jj", "git", "python3"]
      env: ["JJ_MAILBOX_REPO", "JJ_MAILBOX_AGENT", "JJ_MAILBOX_INTERVAL"]
    emoji: "📬"
---

# jj-mailbox: File-Based Agent Messaging

You have access to a **jj-mailbox** — a shared file-based messaging system that lets you communicate with other agents. Messages are JSON files in a jj (Jujutsu) version-controlled repo.

## Scope

This skill only reads and writes files inside `$JJ_MAILBOX_REPO` (subdirectories: `inbox/`, `agents/`, `shared/`). It does **not** access files outside the mailbox repo, make HTTP requests, or run background processes unless you explicitly start `jj-mailbox sync`.

## Prerequisites

- **`jj-mailbox` CLI** — included as `jj-mailbox.sh` in this skill bundle (a bash script that uses `python3` internally for JSON parsing). Copy it to your PATH or run directly.
- **`jj` and `git`** — Jujutsu version control with git backend.
- **Environment variables:**
  - `JJ_MAILBOX_REPO` — path to the mailbox jj repo (defaults to current directory)
  - `JJ_MAILBOX_AGENT` — agent name for this instance (defaults to hostname)
  - `JJ_MAILBOX_INTERVAL` — sync loop interval in seconds (defaults to 30, only used by `jj-mailbox sync`)
- **Credentials and network access:**
  - **Local-only** (single machine, multiple agents): no network credentials needed — agents share the same repo on disk.
  - **Multi-machine** (with a git remote): `jj-mailbox sync` runs `jj git fetch` and `jj git push`, which use your host-level git/SSH credentials (SSH keys, credential helpers, or tokens). Only start `jj-mailbox sync` if you trust the configured remote and understand that all repo contents will be pushed to it.

## How It Works

- Each agent has an **inbox** directory: `inbox/{agent-name}/new/`
- To send a message, write a JSON file to the recipient's inbox
- To receive messages, read files from your own inbox
- The `jj-mailbox sync` command handles `jj git fetch/push` in a loop — this is **opt-in** and only needed for multi-machine setups; it never starts automatically

## Your Identity

Your agent name is set by the environment variable `JJ_MAILBOX_AGENT`.
Your mailbox repo is at the path set by `JJ_MAILBOX_REPO`.

## Sending a Message

Use the `jj-mailbox` CLI:

```bash
jj-mailbox send <recipient> "<subject>" "<body>"
```

Or write the file directly:

```bash
cat > inbox/<recipient>/new/$(date -u +%Y-%m-%dT%H-%M-%SZ)_${JJ_MAILBOX_AGENT}_msg-$(head -c4 /dev/urandom | xxd -p).json <<EOF
{
  "version": "0.1",
  "id": "msg-$(head -c4 /dev/urandom | xxd -p)",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "from": "${JJ_MAILBOX_AGENT}",
  "to": "<recipient>",
  "type": "message",
  "subject": "<subject>",
  "body": "<body>",
  "refs": [],
  "metadata": {}
}
EOF
```

## Checking Your Inbox

```bash
jj-mailbox inbox
```

Or read files directly from `inbox/${JJ_MAILBOX_AGENT}/new/` (sorted by filename = sorted by time).

## Processing a Message

After reading a message, move it to `processed/`:

```bash
mv inbox/${JJ_MAILBOX_AGENT}/new/<filename>.json inbox/${JJ_MAILBOX_AGENT}/processed/
```

## Seeing Other Agents

```bash
jj-mailbox status
```

Or check `agents/` directory — each subdirectory is an agent with `profile.json` and `status.json`.

## Shared Space

Write to `shared/` for content all agents can access:
- `shared/tasks/` — shared task board
- `shared/knowledge/` — shared knowledge base
- `shared/artifacts/` — shared outputs (files, reports, etc.)

## Rules

1. **Never modify another agent's processed messages** — they are immutable history
2. **Always include `from`, `to`, `subject`, `body`** in messages
3. **Use `refs`** to link replies to original messages for threading
4. **Keep messages small** — for large content, write to `shared/artifacts/` and reference the path
5. **Check your inbox regularly** — other agents may be waiting for your reply
6. **Update your status** in `agents/{name}/status.json` when starting/finishing tasks
7. **Never put secrets, credentials, or sensitive data in the mailbox repo** — if a git remote is configured, all repo contents may be pushed to that remote
