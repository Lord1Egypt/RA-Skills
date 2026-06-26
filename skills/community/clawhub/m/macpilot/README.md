# MacPilot Skills

Agent skills for [MacPilot](https://github.com/adhikjoshi/macpilot) — a CLI tool for macOS automation via Accessibility APIs.

These skills teach AI coding agents (Claude Code, Cursor, Codex, etc.) how to use MacPilot to automate macOS tasks: clicking buttons, typing text, managing windows, handling file dialogs, taking screenshots, and more.

## Install

```bash
npx skills add adhikjoshi/macpilot-skills
```

This uses the [skills](https://github.com/vercel-labs/skills) CLI to install skills into your agent of choice.

## Available Skills

| Skill | Description |
|-------|-------------|
| **macpilot-automation** | Core macOS automation — mouse, keyboard, apps, menus, clipboard (with history & search), notifications, shell, system controls |
| **macpilot-ui-inspector** | Inspect and interact with UI elements via accessibility APIs — find, click, read, and modify controls |
| **macpilot-dialog-handler** | Handle native file dialogs (Open, Save, Print) — navigate folders, select files, dismiss alerts, wait-for & click-primary |
| **macpilot-screenshot-ocr** | Capture screenshots, OCR click (find & click text on screen), screen recording with pause/resume |
| **macpilot-window-manager** | Manage windows — list, move, resize, snap, fullscreen, Spaces, save/restore layouts |

## Prerequisites

1. **MacPilot installed** — Build from source or download from [releases](https://github.com/adhikjoshi/macpilot/releases)
2. **Accessibility permission** — Grant MacPilot.app access in System Settings > Privacy & Security > Accessibility
3. **Screen Recording permission** (for screenshot/OCR skills) — Grant in System Settings > Privacy & Security > Screen Recording

## Quick Start

```bash
# Install MacPilot skills into Claude Code
npx skills add adhikjoshi/macpilot-skills

# Now ask Claude Code to automate macOS:
# "Open Safari and navigate to example.com"
# "Take a screenshot of the Finder window"
# "Snap VS Code to the left half and Terminal to the right"
# "Save this file to my Desktop"
```

## Manual Install

If you prefer not to use `npx skills`, copy any `SKILL.md` file to your agent's skills directory:

```bash
# Claude Code (project scope)
mkdir -p .claude/skills/macpilot-automation
cp skills/macpilot-automation/SKILL.md .claude/skills/macpilot-automation/

# Claude Code (global scope)
mkdir -p ~/.claude/skills/macpilot-automation
cp skills/macpilot-automation/SKILL.md ~/.claude/skills/macpilot-automation/
```

## License

MIT
