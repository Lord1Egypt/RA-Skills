# OS Update Checker

[![ClawHub](https://img.shields.io/badge/ClawHub-os--update--checker-blue)](https://clawhub.ai/pfrederiksen/os-update-checker)
[![Version](https://img.shields.io/badge/version-1.2.0-green)]()

An [OpenClaw](https://openclaw.ai) skill that lists available OS and npm package updates, fetches changelogs for each, and classifies risk — so you know exactly what's changing before you approve an upgrade.

Auto-detects the package manager(s). No configuration needed. Runs both an OS package manager **and** `npm` in a single pass if both are available.

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
| Any (global npm packages) | `npm` |
| Node.js (global npm packages) | `npm` |

## Features

- 🌐 **Cross-platform** — auto-detects your package manager(s)
- 📦 **Full upgradable package list** — name, version delta, source repo
- 📋 **Per-package changelogs** — most recent entry where available; npm packages use registry metadata
- 🔴🟡🟢 **Risk classification** — security, moderate (kernel/openssl/openssh/sudo), or low
- 📄 **JSON output** — \`--format json\` for dashboards and cron
- ⚡ **\`--no-changelog\` flag** — fast mode when you just need the count
- 🔀 **Multi-backend** — runs OS + npm in a single pass on mixed environments
- 🔒 **Read-only** — never installs, modifies, or restarts anything

## Installation

\`\`\`bash
clawhub install os-update-checker
\`\`\`

## Usage

\`\`\`bash
# Full summary with changelogs
python3 scripts/check_updates.py

# JSON output
python3 scripts/check_updates.py --format json

# Quick count only
python3 scripts/check_updates.py --no-changelog
\`\`\`

## Security Design

- \`subprocess\` used exclusively with \`shell=False\`
- Package names validated against per-backend allowlist regex before use in commands
- npm registry fetched via \`urllib.request\` (stdlib only, no shell) with 10s timeout
- All exceptions caught by specific type — no bare \`except\`
- No eval, no shell string interpolation, no dynamic code execution

## Requirements

- Python 3.10+
- One supported package manager on PATH (npm optional, always checked independently)

## Changelog

### 1.2.0
- Added \`NpmBackend\` — checks global npm packages via \`npm outdated -g --json\`
- \`detect_backends()\` now runs OS + npm backends in a single pass
- npm registry metadata fetched via stdlib \`urllib.request\` (no new dependencies)

### 1.1.0
- Added brew, zypper, apk, pacman, yum, dnf backends
- Risk classification with moderate-risk package list

### 1.0.0
- Initial release with apt support

## License

MIT

## Links

- [ClawHub](https://clawhub.ai/pfrederiksen/os-update-checker)
- [OpenClaw](https://openclaw.ai)
