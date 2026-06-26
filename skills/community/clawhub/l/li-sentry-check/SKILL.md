---
name: li_sentry_check
description: "Multi-platform server inspection and health check skill. SSH into remote Linux servers using key-based authentication, run read-only inspection commands (CPU, memory, disk, network, services, security), and generate structured Markdown reports with anomaly highlighting. Use when the user asks to inspect servers, run health checks, check system metrics, perform 巡检/巡查, gather system status, or generate inspection reports. Compatible with nanobot, OpenClaw, and Hermes agent."
---

# li_sentry_check

Multi-platform server inspection and health check via SSH.

## Security Declaration

**This skill is strictly read-only and does NOT:**
- ❌ Modify any server configuration
- ❌ Install or remove software
- ❌ Restart or stop services
- ❌ Write to any file on the remote server
- ❌ Exfiltrate data to external services
- ❌ Access local files other than: `references/targets.yaml`, `references/checks.yaml`, and the SSH private key specified in `keyPath`
- ❌ Make any network connections other than SSH to the target server specified in `targets.yaml`
- ❌ Execute arbitrary commands — only commands from `references/checks.yaml` are allowed

**This skill ONLY:**
- ✅ Reads system information via predefined read-only commands
- ✅ Generates a local Markdown/JSON report
- ✅ Connects to ONE remote server via SSH using the key specified in `targets.yaml`

## Overview

Read-only inspection of remote Linux hosts over SSH using a dedicated key.
Collects system metrics, service status, security events, and generates
a structured Markdown report with anomaly highlighting.

## Platform Support

| Platform  | Script          | Runtime    |
|-----------|-----------------|------------|
| OpenClaw  | `scripts/inspect.mjs` | Node.js 24+ |
| NanoBot   | `scripts/inspect.py`  | Python 3.10+ |
| Hermes    | `scripts/inspect.py`  | Python 3.10+ |

## Safety (Default Deny)

- **Only** run commands defined in `references/checks.yaml`
- **No** state-changing commands (no installs, no config edits, no restarts)
- **Only** SSH key authentication (no passwords)
- **BatchMode=yes** — non-interactive SSH only

## Config

- **Targets**: `references/targets.yaml`
- **Allowed checks**: `references/checks.yaml`

## How To Run

### NanoBot / Hermes (Python)

```bash
python3 scripts/inspect.py --target bogon --checks daily
```

### OpenClaw (Node.js)

```bash
node scripts/inspect.mjs --target bogon --checks daily
```

### Options

| Option     | Description                              | Default |
|------------|------------------------------------------|---------|
| `--target` | Target name from `targets.yaml`          | (required) |
| `--checks` | Check group: `basic`, `services`, `daily`| `basic` |
| `--format` | Output format: `markdown`, `json`        | `markdown` |
| `--output` | Write report to file instead of stdout   | stdout  |

## Check Groups

| Group      | Description                              |
|------------|------------------------------------------|
| `basic`    | Hardware resources: CPU, memory, disk, network |
| `services` | Service status and error logs (from targets.yaml) |
| `daily`    | Full inspection: basic + services + security + logs |

## Extending

1. **Add target**: Edit `references/targets.yaml`
2. **Add checks**: Edit `references/checks.yaml`
3. **Add check group**: Define new group in `checks.yaml`

## SSH Key Setup

```bash
# Generate key pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# Copy to remote server
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<SERVER_IP>

# Test connection
ssh -i ~/.ssh/li_sentry_check inspector@<SERVER_IP>
```

## Security Best Practices

- **Key permissions**: `chmod 600 ~/.ssh/li_sentry_check`
- **Host verification**: For production, pre-populate `known_hosts` instead of `accept-new`
- **Service names**: Only alphanumeric, hyphens, underscores allowed (validated before use)
- **Command allowlist**: Never modify `checks.yaml` with state-changing commands
- **Report handling**: Reports may contain system data — do not share publicly

## Report Output

Reports are generated in Markdown format with:

- **Summary section**: Overall health status, anomaly count
- **Anomaly section**: ⚠️ Highlighted issues requiring attention
- **Normal section**: Collapsible normal check results
- **Details**: Full command output for each check

## Architecture

```
li_sentry_check/
├── SKILL.md                  # This file
├── _meta.json                # Skill metadata
├── references/
│   ├── targets.yaml          # Target server configuration
│   └── checks.yaml           # Command allowlist
└── scripts/
    ├── inspect.mjs           # Node.js implementation (OpenClaw)
    └── inspect.py            # Python implementation (NanoBot/Hermes)
```
