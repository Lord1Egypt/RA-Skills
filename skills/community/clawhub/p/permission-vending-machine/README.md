# Permission Vending Machine (PVM)

<img src="pvm-hero.png" alt="Permission Vending Machine" width="100%">

<a href="https://clawhub.ai/skills/permission-vending-machine"><img src="https://img.shields.io/badge/Clawhub-install-ff6b00?style=flat" alt="Install via Clawhub"></a>
<a href="https://github.com/tylerdotai/permission-vending-machine/blob/main/LICENSE"><img src="https://img.shields.io/github/license/tylerdotai/permission-vending-machine" alt="license"></a>
<a href="https://github.com/tylerdotai/permission-vending-machine"><img src="https://img.shields.io/github/languages/top/tylerdotai/permission-vending-machine" alt="python"></a>

**Local multi-channel approval system for AI agent permissions.** PVM gates sensitive operations behind a human approver — notified via iMessage, Email, Discord, or clickable links — and enforces grants before running dangerous commands.

---

## Overview

When an AI agent wants to run a guarded operation (delete, force-push, etc.), it requests a time-limited grant. PVM notifies all configured channels simultaneously. The approver approves via any channel. Grants are checked before dangerous commands run.

```
Agent                    PVM                       Approver
  |                        |                           |
  |--- pvm request ------->|                           |
  |                        |-- iMessage -------------> |
  |                        |-- Email ----------------> |
  |                        |-- Discord --------------> |
  |                        |                           |
  |                        |<-- APPROVE (any channel) |
  |                        |                           |
  |<-- grant activated ----|                           |
  |                        |                           |
  |--- safe-rm ----------->|                           |
  |<-- GRANTED ------------|                           |
  |                        |                           |
  |--- executes -----------|-------------------------->|
```

---

## Features

- **Grant registry** — SQLite vault with TTL, revocation, and path/repo scope matching
- **Audit log** — every REQUEST/GRANTED/DENIED/EXPIRED/REVOKED event captured
- **5 notification channels** — Sendblue (iMessage), SMTP Email, Discord webhook, Telegram, Slack
- **3 approval detection channels** — Sendblue inbound polling, Email IMAP polling, HTTP clickable links
- **Instant confirmation** — approver gets SMS/email feedback when they approve or deny
- **Safe wrappers** — `safe-rm`, `safe-git-push`, `safe-trash` check grants before executing
- **Persistent daemon** — runs as macOS launchd service (survives reboots)
- **OpenClaw skill** — `pvm_request`, `pvm_status`, `pvm_revoke` for agent integration

---

## Install

## Install

### Interactive Setup Wizard (recommended)

```bash
pip install -e .
pvm init
```

The wizard detects your OS, checks prerequisites, walks through channel configuration, and sets up the service automatically.

### Via Clawhub

```bash
clawhub install permission-vending-machine
```

### Via Git

```bash
git clone https://github.com/tylerdotai/permission-vending-machine.git
cd permission-vending-machine
pip install -e .
```

**Requirements:** Python 3.9+, `sendblue` CLI (for iMessage on macOS), SQLite

---

## Quick Start

### 1. Configure

```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your API keys and approver contacts
```

Key settings:
```yaml
channels:
  sendblue:
    enabled: true
    from_number: "+17862139363"
    approver_numbers:
      - "+1234567890"   # Tyler's number
  email:
    enabled: true
    imap_host: "imap.mail.me.com"
    username: "you@icloud.com"
    password: "app-specific-password"
  discord:
    enabled: true
    webhook_url: "https://discord.com/api/webhooks/..."
    http_approval_base: "http://192.168.0.104:7823"  # your server IP
```

### 2. Start the daemon (runs 24/7)

```bash
# As a macOS launchd service (auto-starts on boot)
launchctl load ~/Library/LaunchAgents/ai.flume.pvm.plist

# Or manually in the foreground
PYTHONPATH=src python3 -m pvm serve --port 7823
```

### 3. Agent requests approval

```bash
pvm request --scope "/tmp/build" --reason "cleaning old artifacts" --duration 5
```

PVM immediately notifies all channels. The approver approves via any channel.

### 4. Approver approves — 4 ways

| Method | How |
|--------|-----|
| **iMessage** | Reply `APPROVE` (no token needed — approves most recent) |
| **Email** | Reply `APPROVE` in the email thread |
| **Discord** | Click "Click to approve" link in the notification |
| **HTTP** | `curl http://localhost:7823/approve/<token>` |

Confirmation SMS is sent back to the approver after every approve/deny.

### 5. Agent executes

```bash
safe-rm -rf /tmp/build
# → grant found, executes
# → grant not found → denied, exit 1
```

---

## CLI Commands

```bash
# Request a permission grant
pvm request --scope <path_or_repo> --reason <reason> --duration <minutes> --block

# Block until approved (agent waits)
pvm request --scope /tmp/data --reason "cleanup" --duration 5 --block --timeout 300

# List active grants
pvm status --agent-id coder

# Revoke a grant early
pvm revoke --grant-id grant_abc123

# View audit log
pvm log --limit 50

# Check if a scope is currently granted
pvm check --scope /tmp/build --agent-id hoss

# Start the HTTP approval server (daemon mode)
pvm serve --port 7823

# Start full daemon (HTTP + email polling + Sendblue polling)
pvm approve-daemon --port 7823
```

---

## Configuration

All settings in `config.yaml`. Environment variables supported via `${VAR}` syntax.

### Vault

```yaml
vault:
  db_path: "./grants.db"
  default_ttl_minutes: 30
  max_ttl_minutes: 480
```

### Channels

Each channel is independently enabled. Only enable what you use.

| Channel | Config keys | Notes |
|---------|-------------|-------|
| **Sendblue** | `api_key`, `from_number`, `approver_numbers` | iMessage + SMS. Uses CLI at `/opt/homebrew/bin/sendblue` |
| **Email** | `imap_host`, `imap_port`, `username`, `password`, `smtp_host`, `approver_emails` | IMAP polling + SMTP sending |
| **Discord** | `webhook_url`, `http_approval_base` | Webhook embeds with clickable approve/deny links |
| **Telegram** | `bot_token`, `approver_chat_ids` | Bot API with inline keyboard |
| **Slack** | `webhook_url` | Incoming webhook with Block Kit |

### Permissions

```yaml
permissions:
  guarded_operations:
    - operation: "rm"
      scope_type: "path"
      require_approval: true
    - operation: "git push --force"
      scope_type: "repo"
      require_approval: true
    - operation: "trash"
      scope_type: "path"
      require_approval: false  # auto-approved inside workspace
```

---

## Wrappers

Prepend `safe-` to guarded commands. Each checks the vault before executing.

```bash
safe-rm -rf /tmp/build          # path scope — prefix matching
safe-git-push --force origin    # repo scope — URL or path match
safe-trash ~/Downloads/file     # path scope — prefix matching
```

If no grant exists, the wrapper prints:
```
Permission denied. Request one with: pvm request --scope /tmp/build --reason "..."
```

---

## Daemon (Persistent Service)

The `approve-daemon` runs three things simultaneously:

1. **HTTP server** — listens for `/approve/<token>` and `/deny/<token>` GET/POST requests
2. **Sendblue poller** — checks inbound iMessages every 15s for `APPROVE` or `DENY`
3. **Email poller** — checks IMAP inbox every 30s for approval email replies

### macOS launchd setup

The plist is at `~/Library/LaunchAgents/ai.flume.pvm.plist`:

```bash
launchctl load ~/Library/LaunchAgents/ai.flume.pvm.plist   # start
launchctl unload ~/Library/LaunchAgents/ai.flume.pvm.plist # stop
```

Logs: `~/flume/permission-vending-machine/pvm.log` and `pvm.err.log`

---

## Approval Flow (End-to-End)

```
1. Agent calls: pvm request --scope /tmp/build --reason cleanup --block
2. Vault creates a pending permission_request with a unique token
3. All enabled channels receive notification:
   - Sendblue: iMessage to approver
   - Email: SMTP email to approver
   - Discord: webhook embed with "Click to approve" link
4. Approver responds (any channel):
   - APPROVE → grant created in vault, confirmation SMS sent
   - DENY     → denial logged, confirmation SMS sent
5. Polling thread in agent sees grant → unblocks
6. safe-rm checks vault → grant found → executes
```

---

## Architecture

```
permission-vending-machine/
├── config.example.yaml        # All configuration
├── src/pvm/
│   ├── vault.py               # SQLite registry — grants, requests, audit log
│   ├── models.py              # Grant, PermissionRequest, AuditEntry dataclasses
│   ├── notifier.py            # Multicast dispatcher → all channels
│   ├── channels/
│   │   ├── base.py           # NotificationChannel abstract class
│   │   ├── sendblue.py       # Sendblue iMessage (CLI subprocess)
│   │   ├── email.py          # SMTP email sender
│   │   ├── discord.py        # Discord webhook embeds
│   │   ├── telegram.py       # Telegram bot API
│   │   └── slack.py         # Slack incoming webhooks
│   ├── approval/
│   │   ├── server.py         # Flask HTTP server (/approve, /deny)
│   │   ├── daemon.py          # ApprovalDaemon — starts all pollers + HTTP
│   │   ├── email_poller.py   # IMAP inbox polling for email approvals
│   │   └── sendblue_poller.py # Sendblue CLI polling for iMessage approvals
│   └── cli.py                # pvm CLI entry point
├── wrappers/
│   ├── safe-rm
│   ├── safe-git-push
│   └── safe-trash
└── skills/
    └── permission-guard/
        └── SKILL.md           # OpenClaw skill for agent integration
```

---

## Testing

```bash
pytest tests/ -v
# 35+ tests covering vault, notifier, wrappers
```

---

## Cross-Platform Support

PVM runs on macOS, Linux, and Windows. See [PLATFORMS.md](docs/PLATFORMS.md) for detailed setup guides per platform.

| Feature | macOS | Linux | Windows |
|---------|-------|-------|---------|
| Core vault + wrappers | ✅ | ✅ | ✅ |
| Email (IMAP/SMTP) | ✅ | ✅ | ✅ |
| Discord webhook | ✅ | ✅ | ✅ |
| Telegram bot | ✅ | ✅ | ✅ |
| Slack webhook | ✅ | ✅ | ✅ |
| Sendblue iMessage | ✅ | ❌ | ❌ |
| HTTP approval server | ✅ | ✅ | ✅ |
| Service manager | launchd | systemd | NSSM/Task Scheduler |

**Sendblue iMessage** works only on macOS (uses the local Messages app). For Linux/Windows, Discord webhook + clickable links is the recommended approval path.

---

## License

MIT — see [LICENSE](LICENSE)
