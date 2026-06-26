---
name: permission-vending-machine
description: "Multi-channel approval system for AI agent permissions. GATES sensitive operations (file deletion, git force-push) behind human approval. Notifies via iMessage, Email, Discord, Telegram, Slack — and enforces time-limited grants before dangerous commands run. Use when an agent needs permission to delete files, force-push, or perform destructive operations."
---

# Permission Vending Machine (PVM)

**Multi-channel approval system for AI agent permissions.**

Gates sensitive operations (file deletion, git force-push, etc.) behind a human approver. Notifies via iMessage/SMS, Email, Discord, Telegram, or Slack — and enforces grants before running dangerous commands.

## When to use

Use when an AI agent needs to perform an operation that could be destructive:
- Deleting files or directories
- Force-pushing to git repositories
- Moving files to trash outside the agent's workspace

## Quick Setup

```bash
# 1. Install
git clone https://github.com/tylerdotai/permission-vending-machine.git
cd permission-vending-machine
pip install -e .

# 2. Configure
cp config.example.yaml config.yaml
# Edit config.yaml with your API keys

# 3. Start the daemon (macOS)
launchctl load ~/Library/LaunchAgents/ai.flume.pvm.plist

# 4. Agent requests permission
pvm request --scope "/tmp/build" --reason "cleaning artifacts" --duration 5

# 5. Approver approves via iMessage, email, or Discord link

# 6. Agent runs guarded command
safe-rm -rf /tmp/build
```

## How it works

```
Agent → pvm request → Vault (pending) → Notify all channels
                                                ↓
                 Approver approves via any channel
                                                ↓
                 Grant created → Agent unblocks → safe-* command executes
```

## Approval Methods

| Method | How to approve |
|--------|---------------|
| **iMessage** | Reply `APPROVE` (no token needed) |
| **Email** | Reply `APPROVE` in the approval email |
| **Discord** | Click "Click to approve" link |
| **HTTP** | `curl http://host:7823/approve/<token>` |

## Configuration

Key settings in `config.yaml`:

```yaml
channels:
  sendblue:        # macOS only — iMessage via CLI
    enabled: true
    from_number: "+1..."
    approver_numbers: ["+1..."]
  email:           # cross-platform
    enabled: true
    imap_host: "imap.example.com"
    username: "user"
    password: "pass"
  discord:         # cross-platform
    enabled: true
    webhook_url: "https://discord.com/api/webhooks/..."
    http_approval_base: "http://your-server:7823"
```

## CLI Commands

```bash
pvm request --scope <path> --reason <text> --duration <min>  # Request approval
pvm status --agent-id <id>                                    # List active grants
pvm revoke --grant-id <id>                                    # Revoke early
pvm log --limit 50                                           # Audit log
pvm serve --port 7823                                         # HTTP server
pvm approve-daemon --port 7823                               # Full daemon
```

## Wrappers

Prepend `safe-` to guarded commands:

- `safe-rm -rf /path` — checks path scope grant
- `safe-git-push --force` — checks repo scope grant
- `safe-trash /path` — checks path scope grant

## Platforms

- **macOS**: launchd service, Sendblue iMessage works
- **Linux**: systemd service, use Discord/email/Telegram for approvals
- **Windows**: NSSM/Task Scheduler, use Discord/email/Telegram

See [docs/PLATFORMS.md](docs/PLATFORMS.md) for detailed setup per platform.

## Links

- Repo: https://github.com/tylerdotai/permission-vending-machine
- Docs: [PLATFORMS.md](docs/PLATFORMS.md) · [ARCHITECTURE.md](docs/ARCHITECTURE.md)
