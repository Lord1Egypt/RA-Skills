---
name: ponddepth-levels
description: Leveling overlay for OpenClaw Control UI (badge + XP + daily tip + level list + icons).
metadata:
  {
    "openclaw": {
      "emoji": "🦞",
      "requires": {"bins": ["python3"]}
    }
  }
---

# PondDepth Levels (🦞)

A game-like leveling overlay for **OpenClaw Control UI**.

## Quick demo

![PondDepth badge in OpenClaw Control UI](assets/demo.jpg)

## What you get

- **Top-left PondDepth badge** with hover popover
- **XP → Level + progress** (reads `companion-metrics.json`)
- **Daily one-line OpenClaw tip** (reads `openclaw-tip.json`)
- **Level list / XP ranges** (hover `?`) + current XP highlight
- **i18n (zh/en)** + compact skills list layout
- **Level icons** (B/F/S × 1..5)
- **Skills install CTA (B2)** that checks ClawHub auth status and guides users to run `clawhub login`

## Requirements

- `python3`
- OpenClaw installed via Homebrew (default paths below)

## Install

### 1) Install the skill

```bash
clawhub install ponddepth-levels
```

### 2) Apply it to Control UI (copies assets into OpenClaw install)

```bash
bash ~/.openclaw/workspace/skills/ponddepth-levels/scripts/install.sh
```

### 3) Refresh

Open Control UI and **hard refresh**.

## What this modifies (important)

This skill **copies files into your local OpenClaw installation**:

- UI assets directory (default):
  - `/opt/homebrew/lib/node_modules/openclaw/dist/control-ui/assets`
- Files written/updated:
  - `ponddepth-badge.js`
  - `ponddepth-icons/*.png`

A timestamped backup is saved to:

- `~/.openclaw/workspace/_deleted/ponddepth-install-backups/<timestamp>/`

## Scheduled jobs (created on install)

The install script best-effort creates/updates two OpenClaw cron jobs:

1) **PondDepth ClawHub status (10m)**
   - Writes `clawhub-status.json` for the “Install skills” CTA UX

2) **PondDepth companion metrics (hourly)**
   - Generates `companion-metrics.json` (XP/level)

## Configuration (optional)

You can override paths used by the install script:

- `OPENCLAW_WORKSPACE` (default: `~/.openclaw/workspace`)
- `OPENCLAW_UI_ASSETS_DIR` (default: Homebrew OpenClaw Control UI assets dir)

Example:

```bash
export OPENCLAW_UI_ASSETS_DIR="/path/to/openclaw/dist/control-ui/assets"
bash ~/.openclaw/workspace/skills/ponddepth-levels/scripts/install.sh
```

## Uninstall

```bash
bash ~/.openclaw/workspace/skills/ponddepth-levels/scripts/uninstall.sh
```

This removes the injected UI assets and (best-effort) restores the most recent backup from:

- `~/.openclaw/workspace/_deleted/ponddepth-install-backups/`

## Troubleshooting

- **Nothing shows up:** run the install script again, then hard refresh Control UI.
- **Permissions error copying into `/opt/homebrew/...`:** run with a user that has write permission to that Homebrew prefix (or set `OPENCLAW_UI_ASSETS_DIR`).
- **Icons missing:** ensure `ponddepth-icons/` exists under the Control UI assets dir.

---

### Notes for maintainers

- To keep publish size small, this package ships resized PNGs in `assets/icons_bin/` and ignores `assets/icons_b64/` during publish via `.clawhubignore`.
