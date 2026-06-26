---
name: glancely
description: >
  Personal tracker framework. Scaffold new habit/workout/mood/reminder
  trackers from natural language. Dashboard, cron, all in one skill.
version: 0.3.0
metadata:
  openclaw:
    requires:
      bins: [python3]
      anyBins: [pip, pip3]
    os: [macos, linux]
    envVars:
      - name: GLANCE_HOME
        required: false
        description: Custom data directory (default ~/.glancely)
---

## What glancely is

A personal tracker framework that puts all your habits in one dashboard.
You describe what you want to track, and glancely scaffolds it — migrations,
cron, dashboard panel — in one command.

## Routing user intent

When a user asks for something, follow this dispatch table:

| User says              | Action |
|------------------------|--------|
| "log mood" / "how I feel" | Check `~/.glancely/components/mood/`. If exists → read SKILL.md → run log.py. If not → read `examples/mood/SKILL.md` for reference → scaffold first, then log. |
| "remind me" / "add reminder" | Check `~/.glancely/components/reminder/`. Same fallback to `examples/reminder/SKILL.md`. |
| "what's my MIT" / "most important task" | Check `~/.glancely/components/mit/`. Fallback to `examples/mit/SKILL.md`. |
| "log diary" / "track time" | Check `~/.glancely/components/diary_logger/`. Fallback to `examples/diary_logger/SKILL.md`. |
| "build dashboard" / "show dashboard" | Run `glancely dashboard build` and open `~/.glancely/dashboard/index.html`. |
| "create tracker" / "track my" / "scaffold a habit" | Read `glancely/skills/scaffold_component/SKILL.md`. Infer fields, cron, notifications from the user's description. Propose a plan. Confirm. Scaffold. |
| "what trackers do I have" | Run `glancely list`. |

## Per-route workflow

1. Check if the user already has a matching component in `~/.glancely/components/`
2. If yes: read its SKILL.md for field docs, then call its scripts/log.py
3. If no: read the matching example in `examples/` for reference, then use the scaffold flow to create it first
4. Report the result

## Setup

If `glancely` CLI is missing or `~/.glancely/` does not exist:
1. Install the package: `pip3 install glancely` (or `pip install glancely` if pip3 isn't available; use `pipx install glancely` on macOS Homebrew/PEP 668 systems)
2. Run `glancely setup` (minimal init — migrations only)
3. If user wants cron, ask for agent_id / session info and write `~/.glancely/openclaw.toml`

## Scaffold flow (via scaffold_component/SKILL.md)

1. **Analyze** the user's goal. Infer tracker name, fields, cron schedule, notification text.
2. **Propose** a plan — list trackers, fields, and cron before touching anything. Ask for confirmation.
3. **Scaffold** each confirmed tracker: `glancely scaffold --name ... --field ... --cron ... --notify ...`
4. Dashboard auto-builds after each scaffold.
