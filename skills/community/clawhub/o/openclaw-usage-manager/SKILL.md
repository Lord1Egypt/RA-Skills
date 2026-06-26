---
name: openclaw-usage-manager
description: Real-time usage dashboard and auto-switcher for dual Claude Max accounts. Use when: (1) checking C1/C2 utilization, (2) switching between accounts, (3) monitoring 5h/7d rate limits. Launches a browser dashboard showing both accounts side-by-side. Auto-switches when either 5h or 7d utilization exceeds 80%.
---

# OpenClaw Usage Manager

Monitor and auto-switch between two Claude Max accounts (C1/C2) based on 5-hour and 7-day utilization rates.

## What This Does

- **Usage Dashboard**: Browser UI showing C1/C2 utilization in real time
- **Auto-Switcher**: Checks rates every 3h (via cron), switches when either 5h OR 7d hits 80%
- **Security-audited**: Reviewed by Claude Code + Codex before release

## Setup

See full setup guide: https://github.com/Takao-Mochizuki/openclaw-usage-manager

### Quick Start

```bash
# 1. Clone and install
git clone https://github.com/Takao-Mochizuki/openclaw-usage-manager.git
mkdir -p ~/.openclaw/workspace/tools/usage-dashboard
mkdir -p ~/.openclaw/workspace/tools/usage-switch
cp usage-dashboard/server.mjs ~/.openclaw/workspace/tools/usage-dashboard/
cp usage-switch/check.mjs ~/.openclaw/workspace/tools/usage-switch/
cp usage-switch/setup-tokens.sh ~/.openclaw/workspace/tools/usage-switch/

# 2. Configure 1Password item IDs in setup-tokens.sh and server.mjs
# Replace "your-c1-item-id" and "your-c2-item-id" with your actual 1Password item IDs

# 3. Run one-time token setup (requires TouchID)
chmod +x ~/.openclaw/workspace/tools/usage-switch/setup-tokens.sh
~/.openclaw/workspace/tools/usage-switch/setup-tokens.sh

# 4. Add usage alias to ~/.zshrc
alias usage='lsof -ti:18800 | xargs kill -9 2>/dev/null; sleep 0.5; node ~/.openclaw/workspace/tools/usage-dashboard/server.mjs & sleep 1 && open http://localhost:18800'
```

## Usage

```bash
# Launch dashboard
usage

# Check utilization (JSON output)
node ~/.openclaw/workspace/tools/usage-switch/check.mjs

# Output example:
# {"c1":{"5h":7,"7d":43,"over":false},"c2":{"5h":4,"7d":69,"over":false},"current":"C2","needSwitch":false}
```

## OpenClaw Cron (Auto-Switch every 3h)

Set up a cron job in OpenClaw with schedule `0 */3 * * *`:

```
Run: node ~/.openclaw/workspace/tools/usage-switch/check.mjs
If needSwitch is true → run openclaw gateway restart and notify your channel.
If bothOver is true → post manual intervention request.
Otherwise → silent.
```

## Requirements

- OpenClaw installed
- Claude Max × 2 accounts
- Node.js >= 18
- 1Password CLI (`op`) recommended for secure token storage

## Security

- tokens.json: chmod 600, excluded from git
- Atomic writes: tmp file + renameSync
- Dashboard: localhost-only, CSRF tokens, POST-only API
- Audited by Claude Code + Codex

## Links

- GitHub: https://github.com/Takao-Mochizuki/openclaw-usage-manager
- Author: @5dmgmt (五次元経営株式会社)
