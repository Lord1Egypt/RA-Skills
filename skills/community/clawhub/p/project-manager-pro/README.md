# Project Manager Pro

**Conversational task & project management for OpenClaw agents.**

Your AI agent becomes your project manager. Tell it what you need to do in plain language — it creates tasks, breaks down projects, tracks dependencies, and follows up proactively. No app to open. No UI to click. Just talk.

## What It Does

- **Conversational task creation** — "I need to launch the website by March 20" → structured project with subtasks, deadlines, and dependencies
- **Smart decomposition** — Break big goals into actionable task trees with time estimates
- **Proactive check-ins** — Morning priorities, evening review, weekly progress summary
- **Context-aware prioritization** — Eisenhower matrix by default, auto-escalates as deadlines approach
- **Cross-tool integration** — Auto-generates tasks from other NormieClaw tools (expenses, meal prep, fitness, content)
- **Natural language everything** — Add, edit, complete, filter, and view tasks through conversation

## What It Replaces

| Tool | Annual Cost | What PM Pro Does Instead |
|------|-------------|--------------------------|
| Todoist Pro | $48/yr | Full task management with AI prioritization |
| Asana (Starter) | $132/yr | Project breakdown, dependencies, progress tracking |
| Motion | $348/yr | AI-driven prioritization and proactive follow-ups |

**Project Manager Pro: $49 one-time.**

## Quick Start

### 1. Install

Copy the `project-manager-pro/` folder into your OpenClaw agent's skills directory:

```bash
cp -r project-manager-pro/ ~/.openclaw/skills/project-manager-pro/
```

### 2. Setup

Run the setup script to create the data directory:

```bash
chmod 700 ~/.openclaw/skills/project-manager-pro/scripts/*.sh
~/.openclaw/skills/project-manager-pro/scripts/setup.sh
```

### 3. Configure

Start a conversation with your agent. It will walk you through setup using `SETUP-PROMPT.md`:
- Set your active projects
- Choose a priority framework
- Configure check-in times
- Enable cross-tool integrations

### 4. Use

Just talk to your agent:
- "Add a task to review the contract by Thursday"
- "Break down the apartment move into subtasks"
- "What's on my plate today?"
- "Mark the dentist appointment as done"
- "Show me everything that's overdue"

## File Structure

```
project-manager-pro/
├── SKILL.md              # Agent instructions (the brain)
├── SETUP-PROMPT.md       # First-run configuration conversation
├── README.md             # This file
├── SECURITY.md           # Security considerations
├── config/
│   └── settings.json     # User preferences and defaults
├── scripts/
│   ├── setup.sh          # Initialize data directory
│   ├── export-tasks.sh   # Export as markdown/CSV/JSON
│   └── weekly-review.sh  # Generate weekly progress summary
├── examples/
│   ├── example-project-breakdown.md
│   ├── example-daily-checkin.md
│   └── example-cross-tool-tasks.md
└── dashboard-kit/
    ├── manifest.json
    └── DASHBOARD-SPEC.md
```

## Data Storage

Tasks and projects are stored as JSON files in `~/.openclaw/workspace/pm-pro/`. No external database. No cloud sync. No account required.

## Export

Export your tasks anytime:

```bash
./scripts/export-tasks.sh markdown   # Readable markdown report
./scripts/export-tasks.sh csv        # Spreadsheet-compatible CSV
./scripts/export-tasks.sh json       # Raw JSON dump
```

## Dashboard

If you're using the NormieClaw dashboard system, Project Manager Pro includes widgets for:
- Today's task list
- Overdue alerts
- Weekly progress bar
- Per-project completion status
- Completion trend charts

See `dashboard-kit/DASHBOARD-SPEC.md` for integration details.

## Requirements

- OpenClaw agent with skill loading support
- Bash shell (macOS, Linux, or WSL)
- `jq` (installed automatically by setup.sh if missing)

## Support

Questions or issues? Reach out at [normieclaw.ai](https://normieclaw.ai).

---

*Built by NormieClaw — AI tools for the rest of us.*
