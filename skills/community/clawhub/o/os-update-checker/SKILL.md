---
name: os-update-checker
version: 1.2.0
description: "Check for available OS package updates with per-package changelog summaries and risk classification. Supports apt (Debian/Ubuntu), dnf (Fedora/RHEL), yum (CentOS 7), pacman (Arch), zypper (openSUSE), apk (Alpine), brew (macOS), and npm (global packages). Use when: checking system update status, before approving upgrades, or in heartbeats/cron for periodic OS health monitoring. Read-only — does not install or modify anything."
---

# OS Update Checker

Read-only, cross-platform package update checker. Auto-detects the available package manager, lists upgradable packages, fetches changelogs, and classifies risk (security, moderate, low). Designed to give enough context to approve or defer an upgrade confidently.

## Supported Package Managers

| OS / Runtime | Package Manager |
|---|---|
| Debian / Ubuntu / Mint | `apt` |
| Fedora / RHEL 8+ / Rocky / Alma | `dnf` |
| CentOS 7 / RHEL 7 | `yum` |
| Arch / Manjaro / EndeavourOS | `pacman` / `checkupdates` |
| openSUSE Leap / Tumbleweed / SLES | `zypper` |
| Alpine Linux | `apk` |
| macOS / Linux (Homebrew) | `brew` |
| Node.js (global npm packages) | `npm` |

## Usage

```bash
# Human-readable summary with changelogs (auto-detects OS)
python3 scripts/check_updates.py

# JSON output (for dashboards, cron, integrations)
python3 scripts/check_updates.py --format json

# Skip changelogs for a quick count
python3 scripts/check_updates.py --no-changelog
```

## Risk Classification

- 🔴 **security** — source repo contains a security indicator
- 🟡 **moderate** — critical package (kernel, openssh, openssl, sudo, curl, bash, etc.)
- 🟢 **low** — standard maintenance update

## How It Works

1. **Detects** available package manager from PATH (`apt` → `dnf` → `yum` → `pacman` → `zypper` → `apk` → `brew`)
2. **Lists** upgradable packages using the appropriate read-only command
3. **Validates** each package name against a per-backend allowlist regex before any further use
4. **Fetches** the most recent changelog entry per package (apt: `apt changelog`; dnf/yum: `rpm --changelog`; others: package info)
5. **Reports** in text or JSON format

## Security Design

- `subprocess` is used exclusively with `shell=False` — arguments are passed as a list, never interpolated into a shell string
- Package names are validated against per-backend allowlist patterns before use in commands
- All exceptions are caught by specific type — no bare `except`
- Read-only commands only — no installs, no writes, no service restarts

## System Access

- **Commands (read-only):** `apt list`, `apt changelog`, `dnf check-update`, `rpm -q --changelog`, `yum check-update`, `pacman -Qu`, `pacman -Si`, `zypper list-updates`, `zypper info`, `apk list`, `apk info`, `brew outdated`, `brew info`, `npm outdated -g --json`
- **Network:** Outbound HTTPS to distribution changelog servers (apt); outbound HTTPS to `registry.npmjs.org` (npm); others use local package metadata
- **No file writes**

## Requirements

- Python 3.10+
- One supported package manager available on PATH
