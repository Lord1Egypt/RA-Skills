---
name: linux-security-guardian
description: Autonomous multi-client Linux server security management via SSH MCP. Runs full audit at 1 AM IST nightly via cron. Iterates over all clients and their server fleets. Covers system hardening, CVE scanning (CISA KEV + OSV.dev + NVD API), user auditing, SSH config, firewall rules, running services, file permissions, log analysis, SSL certs, and kernel parameters. Non-breaking actions auto-applied. Critical patches and network/firewall changes require owner confirmation. Report sent per-server and per-client via email plugin/skill (not bundled). All owner-specific config lives in core-extra/config/ — no hardcoded names, domains, or emails.
version: 1.4.2
metadata: {"openclaw": {"emoji": "🛡️", "requires": {"bins": ["bash","python3","ss","iptables","systemctl","grep","awk","sed","find","curl"], "mcp": ["ssh_conn","ssh_exec"]}}}
---

# Linux Security Guardian

## ⚡ SSH MCP — REQUIRED DEPENDENCY

> **SSH MCP is a hard dependency. The agent MUST have SSH MCP tools available to operate.**
> No local/legacy fallback. All operations go through SSH MCP.

### Prerequisite

```yaml
# SSH MCP server must be running and accessible
dependency: ssh_mcp
status: required    # if unavailable → ABORT, alert owner
```

### Server Profile Config

Each target server needs a saved connection in SSH MCP database. Configure in `SERVER_PROFILE.md`:

```yaml
ssh_mcp:
  connection_id: "<id-name-or-alias-from-ssh-conn-list>"   # Saved connection ID, Name, or Alias
  # OR inline config:
  # host: "<server-ip>"
  # port: 22
  # username: "<user>"
  # key_path: "</path/to/key>"
```

### Audit Modules

All 18 modules execute commands via SSH MCP. Each module file lists commands that get wrapped with `ssh_exec(op="run", sessionId, command)`:

```
module command → ssh_exec(op="run", sessionId, command="module command")
              → ssh_exec(op="logs", commandId=cmdId)
              → parse output
```

### CVE Scan

The external CVE scan runs locally (on the guardian host) using curl to CISA KEV, OSV.dev, and NVD API.
Usage requires `--client` and `--server` to write results to per-server paths:

```bash
bash cve/cve-scan.sh --client "client-1" --server "server-01"

# Writes results to:
#   cve/<client>/<server>/scan-results/YYYY-MM-DD.md
#   cve/<client>/<server>/advisories/<CVE-ID>.md
```

Steps:
```bash
# 1. SSH MCP: ssh_exec(op="run", sessionId, command="dpkg-query -W ...") → save locally
# 2. Read from cve/<client>/<server>/scan-results/installed-packages.txt
# 3. curl CISA KEV → filter Linux entries → write advisories
# 4. curl POST OSV.dev batch → match packages → write advisories
# 5. curl NVD API (optional) → cross-check → write advisories
```

---

## Core-Extra Config System

All owner-specific data lives in `core-extra/config/` — **never hardcoded** in hooks or modules.

### Profile
| File | Contains | Fields |
|------|----------|--------|
| `core-extra/config/profile.md` | Owner identity + domain + email | `Owner.name`, `Domain.primary`, `Email.noreply` |

### How Agents Use It
```
At session start → load core-extra/config/profile.md
→ Owner.name  → used in SOUL.md [WORKSPACE OWNER]
→ Email.noreply → used as from: in mail-sender.md
→ Domain.primary → used in config generation

To change: edit core-extra/config/profile.md only.
```

### Rule
- NO hardcoded names, domains, or emails in hooks/, modules/, or root files
- All personal/owner data comes from `core-extra/config/profile.md`
- The core-extra directory is part of the skill (published to ClawHub with placeholders)
- Owner fills profile.md ONCE after install

---

## Multi-Client Architecture

The guardian manages **multiple clients**, each with their own server fleet.
SERVER_PROFILE.md defines `## Client:` sections. The audit iterates ALL.

```
SERVER_PROFILE.md
├── ## Client: client-1 (7 servers)
│   ├── server-01
│   ├── server-02
│   └── ... server-07
├── ## Client: client-2 (N servers) ← add as needed
│   └── ...
└── ## Client: [NEXT-CLIENT]
```

All paths use `<client>/<server>/` prefix:
- Findings: `audit/results/<client>/<server>/<severity>/`
- Actions:  `actions/<client>/<server>/auto-done/`
- CVEs:     `cve/<client>/<server>/advisories/`
- Reports:  `reports/<client>/<server>/daily/`

---

## Purpose

Agent manages complete Linux server security autonomously via SSH MCP.
Every night at 1 AM IST:
- Iterates all clients → all servers
- Full security audit runs via SSH MCP
- CVEs scanned against installed packages
- Auto-fixes applied for safe issues
- Critical issues queued for owner confirmation
- Per-server, per-client, and master email reports delivered

---

## Action Decision Matrix

The most important thing — what agent does vs what it asks first:

| Finding Type | CVSS / Severity | Action |
|---|---|---|
| CVE — Critical | ≥ 9.0 | EMAIL ALERT immediately + queue for confirm |
| CVE — High | 7.0–8.9 | Queue for confirm + include in report |
| CVE — Medium | 4.0–6.9 | Include in report + advisory |
| CVE — Low | < 4.0 | Info in report only |
| CVE — KEV (CISA) | any | **Treated as CRITICAL** — immediate alert + confirm within due date |
| CVE — KEV + Ransomware | any | **🔥 HIGHEST PRIORITY** — immediate alert, confirm ASAP |
| Kernel update available | any | Confirm required before patch |
| Security-only pkg update | any | Confirm required |
| SSH: PermitRootLogin yes | critical | Alert + confirm to fix |
| SSH: PasswordAuth yes | high | Alert + confirm to fix |
| SSH: Port 22 | medium | Advisory only |
| Empty password account | critical | AUTO-LOCK immediately |
| Unknown root-uid account | critical | Alert + confirm to lock |
| Inactive account > 90d | medium | Alert + confirm to lock |
| World-writable /tmp | medium | AUTO-FIX chmod |
| World-writable system dir | high | Alert + confirm to fix |
| Unexpected SUID binary | high | Alert only (owner decides) |
| Failed login spike > 20/hr | high | Alert immediately |
| New unknown cron job | high | Alert immediately |
| Firewall rule change needed | any | CONFIRM REQUIRED always |
| Open unexpected port | high | Alert + confirm to close |
| Service: unnecessary running | medium | Alert + confirm to stop |
| SSL cert expiring < 30d | warning | Alert |
| SSL cert expired | critical | Alert immediately |
| Disk > 85% full | warning | Alert |
| Disk > 95% full | critical | Alert immediately |
| Auditd not running | high | AUTO-START + alert |
| fail2ban not running | high | AUTO-START + alert |
| Log file suspicious entry | high | Alert with extract |

---

## Audit Modules

| Module | What it checks | SSH MCP Command |
|--------|---------------|-----------------|
| `01-system` | OS, kernel, uptime, last reboot, hardware | `ssh_exec(op="run", sessionId, command="uname -a; cat /etc/*release")` |
| `02-users` | Accounts, root access, sudo, empty passwords, inactive | `ssh_exec(op="run", sessionId, command="cat /etc/passwd; cat /etc/shadow; ...")` |
| `03-ssh` | sshd_config full audit — 20+ checks | `ssh_exec(op="run", sessionId, command="cat /etc/ssh/sshd_config")` |
| `04-auth` | Login history, failed logins, PAM config | `ssh_exec(op="run", sessionId, command="last; cat /var/log/auth.log")` |
| `05-services` | Running services, unnecessary ones, failed units | `ssh_exec(op="run", sessionId, command="systemctl list-units ...")` |
| `06-packages` | Pending updates, security updates count | `ssh_exec(op="run", sessionId, command="apt list --upgradable 2>/dev/null")` |
| `07-cve` | CVE scan — remote via SSH MCP + API-based | `ssh_exec(op="run", sessionId, command="dpkg-query -W ...; curl ...")` |
| `08-network` | Open ports, listening services, active connections | `ssh_exec(op="run", sessionId, command="ss -tulpn; netstat -tulpn")` |
| `09-firewall` | iptables/nftables/ufw rules audit | `ssh_exec(op="run", sessionId, command="iptables-save 2>/dev/null")` |
| `10-filesystem` | SUID/SGID, world-writable, /tmp, sticky bits | `ssh_exec(op="run", sessionId, command="find / -perm -4000 ...")` |
| `11-kernel` | sysctl security params — 15+ checks | `ssh_exec(op="run", sessionId, command="sysctl -a 2>/dev/null")` |
| `12-logs` | auth.log, syslog, kern.log — anomaly scan | `ssh_exec(op="run", sessionId, command="tail -100 /var/log/syslog")` |
| `13-crons` | System + user cron jobs — unknown jobs flagged | `ssh_exec(op="run", sessionId, command="cat /etc/crontab; ls -la /var/spool/cron/")` |
| `14-ssl` | Cert expiry check for all domains/services | `ssh_exec(op="run", sessionId, command="openssl x509 -in ... -noout -dates")` |
| `15-docker` | If running — image vulns, container config | `ssh_exec(op="run", sessionId, command="docker ps; docker images")` |
| `16-disk` | Disk usage, inode usage | `ssh_exec(op="run", sessionId, command="df -h; df -i")` |
| `17-integrity` | AIDE/tripwire check if installed | `ssh_exec(op="run", sessionId, command="aide --check")` |
| `18-rootkit` | rkhunter/chkrootkit if installed | `ssh_exec(op="run", sessionId, command="rkhunter --check --skip-keypress")` |

**Execution rule**: All commands go through `ssh_exec(op="run", sessionId, command="<command>")` → `ssh_exec(op="logs", commandId=cmdId)`. No local execution.

---

## Finding Severity Levels

| Level | Color | Meaning |
|---|---|---|
| `CRITICAL` | 🔴 | Immediate risk, action required now |
| `HIGH` | 🟠 | Significant risk, fix this week |
| `MEDIUM` | 🟡 | Moderate risk, fix this month |
| `LOW` | 🔵 | Minor issue, fix when possible |
| `INFO` | ⚪ | Informational, no action needed |
| `PASS` | 🟢 | Check passed, all good |

---

## Confirmation Flow

When owner confirmation is needed:

```
Finding detected (requires confirm) on <client>/<server>
    ↓
Write to actions/<client>/<server>/pending-confirm/<client>-<server>-<id>-<slug>.md
    ↓
Include in email report under "NEEDS YOUR DECISION" with <client>/<server> context
    ↓
Owner replies with: APPROVE <id> / DENY <id> / SKIP <id>
(Full ID format: <client>-<server>-<type>-<NNN>, e.g. client-1-server-01-ACT-20260529-001)
    ↓
Search all actions/*/*/pending-confirm/ for the ID
    ↓
APPROVE → agent connects to <client>/<server> via SSH MCP → executes action → logs to history/
DENY    → action skipped, noted
SKIP    → deferred to next audit
```

---

## Email Report Structure

Reports are sent per-server, per-client (summary), and master. All via email plugin/skill.

### Per-Server Report
```
Subject: [Linux Guardian] <client>/<server> — YYYY-MM-DD | Score: N/100 | CRITICAL:N HIGH:N

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINUX SECURITY GUARDIAN — NIGHTLY REPORT
Client: <client> | Server: <server> | <IP> | YYYY-MM-DD 01:00 IST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY
Security Score: N/100 | Grade: X
Critical: N | High: N | Medium: N | Low: N
Auto-fixed: N | Pending confirm: N | Passed: N

━━ 🔴 CRITICAL (immediate action needed)
[Finding details]

━━ 🟠 HIGH
[Finding details]

━━ ⚡ AUTO-ACTIONS TAKEN (safe, non-breaking)
[What was auto-fixed]

━━ 🔑 NEEDS YOUR DECISION (reply APPROVE/DENY/SKIP <id>)
[Pending confirmations with IDs — includes <client>/<server> prefix]

━━ 📦 CVE REPORT
[CVEs found by severity]

━━ 🌐 NETWORK & FIREWALL
[Port/firewall status]

━━ 🟡 MEDIUM / LOW
[Less urgent findings]

━━ 🟢 ALL PASSING
[Checks that passed]

━━ NEXT AUDIT: Tomorrow 01:00 IST
```

### Per-Client Summary Report
```
Subject: [Linux Guardian] <client> Summary — YYYY-MM-DD | Servers: N/N | CRITICAL:N HIGH:N

Client: <client>
Servers audited: N of N total
Average score: N/100

| Server | Score | Critical | High | Score Grade |
|--------|-------|----------|------|-------------|
| ...    | ...   | ...      | ...  | ...         |

Cross-server patterns: [same vuln found on multiple servers]
```


---

## Security Score Formula

```
score = 100
score -= (critical_count × 20)
score -= (high_count × 10)
score -= (medium_count × 3)
score -= (low_count × 1)
score = max(0, score)

Grade: 90-100 = A | 75-89 = B | 60-74 = C | < 60 = F
```

---

## Folder Structure

```
linux-security-guardian/
  audit/
    modules/                     ← 01-system.md ... 18-rootkit.md
    results/
      <client>/<server>/
        critical/  high/  warning/  info/  pass/
          YYYY-MM-DD-<check>.md  ← per-client/per-server findings

  actions/
    <client>/<server>/
      auto-done/                 ← auto-fixed actions (logged)
        YYYY-MM-DD-<slug>.md
      pending-confirm/           ← waiting for owner
        <id>-<slug>.md
      history/                   ← all approved/denied actions

  cve/
    cve-scan.sh                  ← external CVE scanner (takes --client --server)
    external-sources.md          ← all API URLs, query params, working examples
    .cache/                      ← shared cached API responses (6h TTL)
    <client>/<server>/
      scan-results/              ← YYYY-MM-DD.md
      advisories/                ← <cve-id>.md

  reports/
    <client>/<server>/
      daily/YYYY-MM-DD.md
      weekly/YYYY-WNN.md

  network/
    <client>/<server>/
      firewall-snapshots/        ← YYYY-MM-DD-rules.txt
      port-scans/                ← YYYY-MM-DD.md
      proposed-changes/          ← <id>-<change>.md

  hooks/
    audit-runner.md              ← main 1 AM audit orchestrator (multi-client loop)
    on-critical.md               ← fires on any critical finding (with client/server)
    on-confirm-reply.md          ← processes owner APPROVE/DENY/SKIP
    pre-action.md                ← safety check before any action
    post-action.md               ← verify action succeeded
    mail-sender.md               ← uses email plugin/skill to send report

  crons/
    active/
      nightly-audit.md           ← 1 AM IST permanent
    completed/

  core-extra/
    config/
      profile.md                 ← owner name, domain, email (fill ONCE, no hardcode)
    hooks/                       ← shared hooks (mirrors hooks/ structure)
    templates/                   ← shared templates

  errors/
    raw/                         ← raw error logs

  memory/
    schema.json
    index.json

  SOUL.md                        ← soul context (multi-client aware)
  AGENT.md                       ← behavioral rules (multi-client, SSH MCP hard dep)
  SERVER_PROFILE.md               ← multi-client server details
  AUDIT_LOG.md                    ← append-only master log
  BASELINE.md                     ← expected state snapshot
  STATS.md
```
