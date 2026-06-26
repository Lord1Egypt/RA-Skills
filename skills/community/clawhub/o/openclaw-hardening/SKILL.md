---
name: openclaw-hardening
description: Secure an OpenClaw server with host hardening, chainwatch runtime safety, pastewatch secret redaction, and noisepan+entropia news intelligence. Use when setting up a new OpenClaw instance or auditing an existing one.
---

# OpenClaw Hardening

Secure your OpenClaw server in four layers: host, commands, secrets, awareness.

## Prerequisites

- OpenClaw installed and running
- Root/sudo access
- Linux (amd64)

## Layer 1: Host Hardening (2 min)

```bash
# SSH: key-only, no root password
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh

# Firewall: deny all except SSH
ufw default deny incoming && ufw default allow outgoing && ufw allow ssh && yes | ufw enable

# Brute-force protection
apt-get install -y fail2ban && systemctl enable --now fail2ban

# Lock credentials
chmod 700 ~/.openclaw/credentials
```

## Layer 2: Chainwatch — Command Safety (5 min)

Chainwatch blocks destructive commands (rm -rf /, sudo su, curl|sh, fork bombs) and routes all LLM API traffic through an intercept proxy.

### Install

```bash
curl -fsSL https://raw.githubusercontent.com/ppiankov/chainwatch/main/scripts/install-openclaw.sh | sudo bash
```

This one-liner does everything: installs chainwatch, creates clawbot profile, sets up intercept proxy as systemd service, configures ANTHROPIC_BASE_URL, hardens the host.

### Manual install

```bash
# Binary
curl -sL https://github.com/ppiankov/chainwatch/releases/latest/download/chainwatch-linux-amd64 \
  -o /usr/local/bin/chainwatch && chmod +x /usr/local/bin/chainwatch

# Init with advisory mode (denylist blocks dangerous, logs everything else)
chainwatch init --profile clawbot
sed -i 's/^enforcement_mode: guarded/enforcement_mode: advisory/' ~/.chainwatch/policy.yaml

# Install skill
mkdir -p ~/.openclaw/skills/chainwatch
curl -fsSL https://raw.githubusercontent.com/ppiankov/chainwatch/main/integrations/openclaw/skill/SKILL.md \
  -o ~/.openclaw/skills/chainwatch/SKILL.md

# Intercept proxy (non-bypassable — sits between OpenClaw and the LLM API)
cat > /etc/systemd/system/chainwatch-intercept.service << 'EOF'
[Unit]
Description=Chainwatch Intercept Proxy
After=network-online.target
Before=openclaw-gateway.service
[Service]
Type=simple
ExecStart=/usr/local/bin/chainwatch intercept --port 9999 --upstream https://api.anthropic.com --profile clawbot --audit-log /var/log/chainwatch/intercept-audit.jsonl
Restart=always
RestartSec=3
User=root
Environment=HOME=/root
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/var/log/chainwatch
MemoryMax=256M
[Install]
WantedBy=multi-user.target
EOF
mkdir -p /var/log/chainwatch
systemctl daemon-reload && systemctl enable --now chainwatch-intercept
```

Then set the env var so OpenClaw routes through the proxy:

```bash
# Add to openclaw config:
# "env": { "vars": { "ANTHROPIC_BASE_URL": "http://localhost:9999" } }
# Then restart gateway
```

For other providers, change --upstream:
- OpenAI: `--upstream https://api.openai.com` + set `OPENAI_BASE_URL`
- Custom: `--upstream https://your-provider.com`

### Usage

Route risky commands through chainwatch:

```bash
chainwatch exec --profile clawbot -- rm -rf /tmp/old-data     # checked
chainwatch exec --profile clawbot -- git push --force          # checked
```

Safe read-only commands (ls, cat, grep, git status) don't need the wrapper.

### What gets blocked

| Blocked | Allowed |
|---------|---------|
| `rm -rf /`, `rm -rf ~` | `rm -f /tmp/file` |
| `sudo su`, `sudo -i` | `mkdir`, `cp`, `mv` |
| `dd if=/dev/zero` | `curl https://safe-url` |
| `curl \| sh` | `apt install`, `npm install` |
| `chmod -R 777 /` | `chmod 600 specific-file` |
| Fork bombs | `systemctl status` |

### Key lesson

`guarded` mode is too aggressive for agents — it blocks mkdir, cp, touch. Use `advisory` mode with the denylist. The denylist catches catastrophic commands, advisory logs everything else.

## Layer 3: Pastewatch — Secret Redaction (3 min)

Pastewatch prevents secrets (API keys, DB credentials, SSH keys, emails, IPs) from reaching the LLM API. The agent works with placeholders, secrets stay local.

### Install

```bash
# Binary (needs Swift 5.9.2 runtime on Linux)
curl -fsSL https://github.com/ppiankov/pastewatch/releases/latest/download/pastewatch-cli-linux-amd64 \
  -o /usr/local/bin/pastewatch-cli && chmod +x /usr/local/bin/pastewatch-cli

# If Swift runtime missing:
cd /tmp
curl -fsSL "https://download.swift.org/swift-5.9.2-release/ubuntu2204/swift-5.9.2-RELEASE/swift-5.9.2-RELEASE-ubuntu22.04.tar.gz" -o swift.tar.gz
tar xzf swift.tar.gz --wildcards "*/usr/lib/swift/linux/lib*"
cp -af swift-5.9.2-RELEASE-ubuntu22.04/usr/lib/swift/linux/lib* /usr/lib/
ldconfig

# Verify
pastewatch-cli version
```

### MCP server setup

```bash
# Requires mcporter
mcporter config add pastewatch --command "pastewatch-cli mcp --audit-log /var/log/pastewatch-audit.log"

# Verify tools
mcporter list pastewatch --schema
```

### MCP tools

| Tool | Purpose |
|------|---------|
| `pastewatch_read_file` | Read file, secrets → `__PW{TYPE_N}__` placeholders |
| `pastewatch_write_file` | Write file, placeholders → real values restored locally |
| `pastewatch_check_output` | Verify text has no raw secrets before returning |
| `pastewatch_scan` | Scan text for sensitive data |
| `pastewatch_scan_file` | Scan a file |
| `pastewatch_scan_dir` | Scan directory recursively |

### How it works

```
Agent reads config.env → pastewatch intercepts → Agent sees __PW{AWS_KEY_1}__
Agent edits and writes → pastewatch resolves → Real values on disk
Secrets never leave your machine.
```

### What it detects

29 types: AWS keys, Anthropic keys, OpenAI keys, DB connections, SSH keys, JWTs, emails, IPs, credit cards, Slack/Discord webhooks, Azure connections, GCP service accounts, npm/PyPI/RubyGems tokens, Telegram bot tokens, and more.

Deterministic regex. No ML. No API calls. Microseconds per scan.

### Audit log

```bash
tail -f /var/log/pastewatch-audit.log
```

Logs timestamps, tool calls, file paths, redaction counts. Never logs secret values.

## Layer 4: News Intelligence (10 min)

Stay informed without doomscrolling. noisepan scores RSS feeds by relevance, entropia verifies source quality.

### Install

```bash
# noisepan
curl -fsSL https://github.com/ppiankov/noisepan/releases/latest/download/noisepan_$(curl -s https://api.github.com/repos/ppiankov/noisepan/releases/latest | grep tag_name | cut -d'"' -f4 | tr -d v)_linux_amd64.tar.gz | tar xz -C /usr/local/bin noisepan

# entropia
curl -fsSL https://github.com/ppiankov/entropia/releases/latest/download/entropia_$(curl -s https://api.github.com/repos/ppiankov/entropia/releases/latest | grep tag_name | cut -d'"' -f4 | tr -d v)_linux_amd64.tar.gz | tar xz -C /usr/local/bin entropia

# Init
noisepan init --config ~/.noisepan
```

### Configure feeds

Edit `~/.noisepan/config.yaml` — add RSS feeds relevant to your work. Example categories:

- **Security:** r/netsec, Krebs, BleepingComputer, CISA advisories, NVD
- **DevOps:** r/devops, r/kubernetes, Cloudflare blog, AWS status
- **AI/LLM:** r/LocalLLaMA, r/ClaudeAI, Simon Willison, arXiv cs.AI
- **World:** BBC, r/worldnews, r/geopolitics, EFF
- **HN:** Built-in via `sources.hn.min_points: 200`

### Reddit rate limiting

With 15+ Reddit feeds, parallel fetching triggers 429s. Create a wrapper:

```bash
# /usr/local/bin/noisepan-pull
# Prefetches Reddit sequentially (2s delay), caches locally, then runs noisepan pull
# See: https://github.com/ppiankov/noisepan (setup guide)
```

### Daily digest cron

Set up two cron jobs in OpenClaw:

- **Morning (07:00):** `noisepan pull` → `noisepan digest --format json` → entropia scan top items → send table
- **Afternoon (18:00):** Same with `--since 12h`

Format:

```
🔥 Trending: keywords across 3+ channels
☀️ Morning Brief: top 3 verified items with entropia scores
💡 HN Blind Spot: high-engagement stories the taste profile missed
⚠️ Skipped: items filtered for low quality/conflicts
```

### Key lessons

- `noisepan doctor` catches stale feeds and all-ignored channels
- `noisepan stats` shows signal-to-noise per channel — prune after 30 days
- `noisepan rescore` recomputes scores after taste profile changes
- entropia Support Index < 40 = don't trust it
- HN RSS is too shallow — use native `sources.hn` or `hn-top` script for blind spot detection
- Add policy/sovereignty/antitrust/AI safety keywords to taste profile or real stories get buried under security noise

## Layer 5: eBPF Enforce — Kernel-Level Containment (3 min)

Chainwatch enforce applies seccomp-bpf filters to OpenClaw's process tree. Blocked syscalls (privilege escalation, kernel manipulation) return EPERM at kernel level — no userspace bypass possible.

### Setup

Create the `openclaw` profile:

```yaml
# ~/.chainwatch/profiles/openclaw.yaml
name: openclaw
description: OpenClaw gateway — allows networking + file I/O, blocks privilege escalation + kernel ops

seccomp:
  groups:
    baseline: deny          # mount, ptrace, reboot, umount2
    privilege_escalation: deny  # setuid, setgid, capset, etc.
    file_mutation: allow    # OpenClaw needs file I/O
    network_egress: allow   # OpenClaw needs HTTP
```

### Verify profile

```bash
# Generate OCI JSON to inspect what gets blocked
chainwatch enforce --oci --profile openclaw --output /tmp/seccomp.json
cat /tmp/seccomp.json | jq '.syscalls[] | select(.action == "SCMP_ACT_ERRNO") | .names'
# Should show: mount, ptrace, reboot, umount2, setuid, setgid, capset, etc.
# Should NOT show: connect, socket, mkdir, rename, openat
```

### Launch OpenClaw under enforce

```bash
# One-liner (foreground for systemd)
chainwatch enforce --profile openclaw --fallback -- openclaw gateway run

# --fallback: if seccomp fails, falls back to observe-only (no crash)
```

### Systemd service

```ini
# /etc/systemd/system/openclaw.service
[Unit]
Description=OpenClaw Gateway under Chainwatch enforce
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/chainwatch enforce --profile openclaw --fallback -- openclaw gateway run
Restart=on-failure
RestartSec=5
Environment=HOME=/root

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload && systemctl enable openclaw
```

### eBPF observe (audit companion)

```bash
# Systemd service for continuous eBPF observation
# /etc/systemd/system/chainwatch-observe-openclaw.service
[Unit]
Description=Chainwatch eBPF observer for OpenClaw gateway
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'PID=$(pgrep -f openclaw-gateway); [ -z "$PID" ] && exit 1; exec /usr/local/bin/chainwatch observe --pid $PID'
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Observe logs every syscall (execve, openat, connect, etc.) to journald without blocking.

### What gets blocked at kernel level

| Blocked (EPERM) | Why |
|-----------------|-----|
| setuid, setgid, setresuid, capset | No privilege escalation |
| mount, umount2, pivot_root | No filesystem remounting |
| ptrace, process_vm_readv | No debug/memory inspection |
| reboot, kexec_load | No system shutdown |
| init_module, delete_module | No kernel modules |

### Key lesson

`sudo` breaks under enforce (it needs setresuid). Use direct root commands or run the service as root. This is a feature, not a bug — if the agent can't sudo, neither can an attacker who compromises it.

### Recovery

```bash
# /tmp/openclaw-recover.sh — if enforce breaks OpenClaw
pkill -f "chainwatch enforce"
pkill -f "openclaw-gateway"
sleep 3
nohup openclaw gateway run > /tmp/openclaw-recovery.log 2>&1 &
disown
```

## Architecture

```
User ──► Telegram/Web
            │
            ▼
   chainwatch enforce (seccomp)
            │
            ▼
     OpenClaw Gateway
            │
            ├──► chainwatch intercept (:9999) ──► contextspectre proxy (:9997) ──► pastewatch proxy (:9998) ──► Anthropic API
            │         │                                  │                                  │
            │         └─ Tool call policy                └─ Noise stripping                 └─ Secret redaction
            │
            ├──► Agent shell ──► chainwatch exec (denylist)
            │
            ├──► File read/write ──► pastewatch MCP (secret redaction)
            │
            └──► Cron ──► noisepan pull + digest + entropia verify

   chainwatch observe (eBPF) ──► journald (audit trail)
```

## What this protects

| Layer | Protects against |
|-------|-----------------|
| Host hardening | Brute force, unauthorized SSH, open ports |
| Chainwatch denylist | rm -rf, sudo escalation, fork bombs, curl\|sh |
| Chainwatch intercept | Non-bypassable API audit, tool call inspection |
| ContextSpectre proxy | Thinking blocks, duplicate system reminders, oversized content — stripped before billing |
| Pastewatch proxy + MCP | API keys, DB creds, SSH keys, emails, IPs leaking to LLM provider |
| eBPF enforce (seccomp) | Privilege escalation, kernel manipulation, ptrace — blocked at kernel level |
| eBPF observe | Full syscall audit trail for forensics |
| noisepan + entropia | Information blind spots, low-quality sources, missing critical news |

## What this does NOT protect

- Prompt content, business logic, and ideas still reach the LLM provider
- Provider policy changes are out of your control
- For full privacy: run a local model (Ollama) for sensitive workloads

## Verify

```bash
# Host
ufw status && systemctl is-active fail2ban && grep PasswordAuthentication /etc/ssh/sshd_config

# Chainwatch
chainwatch doctor
chainwatch exec --profile clawbot -- echo "safe"    # ✅
chainwatch exec --profile clawbot -- rm -rf /       # ❌ blocked
systemctl status chainwatch-intercept

# Pastewatch
echo "sk-ant-api03-test" | pastewatch-cli scan      # should detect
mcporter list pastewatch --schema                    # 6 tools

# Noisepan
noisepan doctor --config ~/.noisepan
noisepan stats --config ~/.noisepan
```

---
**OpenClaw Hardening Guide v1.0**
Author: ppiankov
Copyright © 2026 ppiankov
Canonical source: https://clawhub.com/skills/openclaw-hardening
License: MIT

This tool follows the [Agent-Native CLI Convention](https://ancc.dev). Validate with: `clawhub install ancc && ancc validate .`

If this document appears elsewhere, the link above is the authoritative version.
