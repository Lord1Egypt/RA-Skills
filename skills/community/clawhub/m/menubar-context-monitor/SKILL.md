---
name: context-monitor
description: 「macOS」常驻菜单栏的上下文显示器 · Menu bar context monitor for OpenClaw agents.
---

# MenuBar Context Monitor

macOS 菜单栏实时显示 OpenClaw agent 的上下文用量、模型和运行状态。基于 [SwiftBar](https://github.com/swiftbar/SwiftBar)。

Real-time OpenClaw agent observability in your macOS menu bar, powered by [SwiftBar](https://github.com/swiftbar/SwiftBar).

**Version:** 1.1.0
**Platform:** macOS only
**Author:** [@hjklasdfg](https://github.com/hjklasdfg)
**Source:** [GitHub](https://github.com/hjklasdfg/context-monitor)

## Features

- 🔧 Menu bar shows the most recently active agent's emoji + context usage (e.g. `🔧 140k`)
- 📊 Dropdown lists all agents with context tokens, model alias, and last active time
- 🫠 Warning indicator when context exceeds 100k tokens
- ▶ / — / ✖ Running, idle, and failed state indicators
- 🏠 Works locally or over SSH to a remote OpenClaw host

## Screenshots

```
🔧 98k                          ← menu bar
───────────────────────────────
🦞 OpenClaw Agents (6)
───────────────────────────────
▶ 🔧 tech    98k/1000k (9%)  │ opus   │ 26s ago
— 🎮 main    50k/1000k (5%)  │ opus   │ 2m ago
— 🎯 career  52k/1000k (5%)  │ opus   │ 1m ago
— ✍️ content 40k/1000k (4%)  │ opus   │ 20h ago
— 💰 finance 52k/200k (26%)  │ haiku  │ 1h ago
✖ 🧠 phil    26k/1000k (2%)  │ opus   │ 3d ago
───────────────────────────────
Refresh
```

## Install

Choose the scenario that matches your setup:

### Scenario A: OpenClaw runs on this Mac (local mode)

Everything on one machine — OpenClaw and the menu bar monitor.

```bash
# 1. Install the skill via OpenClaw CLI
openclaw skills install menubar-context-monitor

# 2. Run the installer
bash ~/.openclaw/skills/context-monitor/scripts/install.sh
```

### Scenario B: OpenClaw runs on another machine (remote mode)

Most common setup — OpenClaw runs on a server / Raspberry Pi / Mac Mini, and you want the menu bar on your MacBook. **No OpenClaw installation needed on the MacBook.**

```bash
# 1. Clone the repo
git clone https://github.com/hjklasdfg/openclaw-context-monitor.git
cd openclaw-context-monitor

# 2. Run the installer with your OpenClaw host's SSH address
bash scripts/install.sh --remote user@host
```

> **Example:** `bash scripts/install.sh --remote linyili@192.168.1.100`
>
> SSH key auth is required. If not set up yet, the installer will guide you.

### Alternative: Ask your agent

If you have OpenClaw running locally, you can also just tell your agent:

> "Help me set up agent menu bar monitoring"

The agent will read this skill and walk you through it.

## SwiftBar First Launch

When SwiftBar opens for the first time, it asks you to choose a **plugin folder**. Press `Cmd+Shift+G` and paste:

```
~/Library/Application Support/SwiftBar/Plugins
```

The installer places the plugin script in this directory. You only need to do this once.

## Requirements

- macOS (SwiftBar is macOS-only)
- Python 3
- [SwiftBar](https://github.com/swiftbar/SwiftBar) — installer will offer to install via Homebrew
- SSH key auth (remote mode only)

## How it works

```
SwiftBar plugin (your Mac)  →  SSH  →  status collector (OpenClaw host)  →  sessions.json
                            or locally ↗
```

Two components:
1. **`openclaw-status.py`** — Reads agent session data on the OpenClaw host
2. **`swiftbar-plugin.sh`** — Renders the menu bar on your Mac

## Customization

| Setting | How to change |
|---|---|
| Refresh interval | Rename plugin: `30s` → `10s`, `1m`, `5m` |
| Warning threshold | Edit `WARN = 100000` in the plugin |
| SSH target | Edit `MINI=` in plugin or set `OPENCLAW_SSH_TARGET` env var |

## Agent emoji

Reads from each agent's `IDENTITY.md`:

```markdown
- **Emoji:** 🔧
```

Falls back to agent name if not set.

## Model display

Shows short aliases: opus, sonnet, haiku, flash, pro. User-configured `modelAliases` in `openclaw.json` take priority.

## Troubleshooting

| Menu bar | Meaning | Fix |
|---|---|---|
| `🦞 ❌` | Connection failed | Check SSH / network |
| `🦞 ⚠️` | Data parse error | Run `python3 ~/.openclaw/openclaw-status.py` on host |
| Agent missing | No session data yet | Use the agent once to generate a session |

## License

MIT

---

<!-- Agent instructions below — not displayed on ClawHub -->

## Agent Setup Guide

When a user asks to set up context monitoring, follow this flow:

**Before starting:** This skill requires running commands on a Mac. If the user might be on a mobile device:
> "This needs to run on a Mac. Are you at your Mac now? If you're on another device, I'll send you the commands to run later."

**Step 1:** Ask the user:
> "Does OpenClaw run on this Mac, or on a remote machine? If remote, what's the SSH address? (e.g. `user@hostname`)"

**Step 2 (local mode):** Run the installer directly:
```bash
bash scripts/install.sh --yes
```

**Step 2 (remote mode):** The agent cannot install SwiftBar on the user's Mac remotely. Instead:
1. Deploy the status collector to the OpenClaw host:
   ```bash
   scp scripts/openclaw-status.py <user>@<host>:~/.openclaw/openclaw-status.py
   ```
2. Generate copy-paste instructions for the user with the full install command, including the correct SSH target baked in.

**SwiftBar installation:** If SwiftBar needs to be installed, ask the user for permission first:
> "This requires installing SwiftBar (a macOS menu bar tool). OK to install?"

After confirmation, pass `--yes` to skip the script's interactive prompt.

## Triggers

menu bar, SwiftBar, agent status, agent monitor, observability, dashboard mac, agent context, context monitor, 菜单栏, 上下文显示, agent 监控
