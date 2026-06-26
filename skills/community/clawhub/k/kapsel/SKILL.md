---
name: kapsel
description: >
  Project memory capsules — archive completed project knowledge to Google Drive
  and reload it on demand. Use this skill whenever the user mentions "Kapsel",
  "capsule", "project archive", "project memory", or wants to store, recall,
  or manage knowledge from completed projects. Also trigger when the user says
  things like "save this project", "archive this", "I'm done with this project",
  "load the old project", "what did we do on project X?", or "forget this project
  but keep the knowledge". Works with rclone and any cloud remote (Google Drive,
  OneDrive, S3, etc.).
---

# Kapsel — Project Memory Capsules

Kapseln (capsules) let an AI agent archive everything it knows about a completed
project into a structured folder on cloud storage. When the project is needed again,
the agent loads the capsule and has full context — without carrying dead project
knowledge in its permanent memory.

Think of it like moving a finished project from your desk into a labeled filing
cabinet. Your desk stays clean, but you can pull the folder out anytime.

## How it works

Each capsule is a folder on a cloud remote (via rclone) with this structure:

```
<remote>:<base-path>/Kapseln/<project-name>/
├── summary.md    — Short overview (always readable, max 500 words)
├── details.md    — Decisions, timeline, links, background
├── context.md    — Technical details, configs, code snippets
└── files/        — Any associated files (optional)
```

The `summary.md` is deliberately kept short so the agent can scan all capsules
quickly and decide which one to load in full.

## Setup (one-time)

The script needs `rclone` configured with at least one cloud remote.
If the user hasn't set up rclone yet, guide them through it:

```bash
rclone config    # Interactive setup wizard
```

After rclone is configured, the user needs to set two things in the script
or via environment variables:

| Variable | Default | Meaning |
|----------|---------|---------|
| `KAPSEL_REMOTE` | `gdrive:Kapseln` | rclone remote + path for capsule storage |
| `KAPSEL_TMP` | `/tmp/openclaw/kapseln` | Local temp directory for file staging |

Set them as environment variables or edit the top of `kapsel.py`.

```bash
export KAPSEL_REMOTE="gdrive:MyAgent/Kapseln"
export KAPSEL_TMP="/tmp/kapseln"
```

## Commands

Run the script from the workspace scripts directory:

```bash
python3 scripts/kapsel.py list                    # Show all capsules with summaries
python3 scripts/kapsel.py create <name>           # Create new capsule (empty template)
python3 scripts/kapsel.py load <name>             # Load full capsule (all docs)
python3 scripts/kapsel.py summary <name>          # Show only the short summary
python3 scripts/kapsel.py archive <name>          # Mark as completed
python3 scripts/kapsel.py save <name> <file>      # Add a file to the capsule
```

## When to use each command

**Starting a new project** — `create` makes an empty capsule with template files.
Fill in the summary, details, and context as the project progresses.

**Project is done** — `archive` marks the capsule as completed. After archiving,
you can safely forget the project details from your active memory. The capsule
preserves everything.

**Need old project knowledge** — `summary` gives a quick refresher. If you need
the full picture, use `load` to get all details and technical context.

**Want to store a file** — `save` copies any file into the capsule's `files/` folder.
Use this for configs, exports, screenshots, or any artifact worth keeping.

## Workflow for the agent

The recommended pattern for an AI agent using capsules:

1. When a new project begins: `kapsel.py create my-project`
2. As work progresses: update the capsule files with learnings, decisions, configs
3. Project completed: `kapsel.py archive my-project`
4. Remove project details from active memory (e.g. MEMORY.md) — the capsule is the archive
5. Later, if the project comes up again: `kapsel.py load my-project`

The key insight is that capsules free up the agent's working memory. Instead of
accumulating ever-growing context about every project, the agent keeps only active
projects in memory and offloads completed ones to capsules.

## Installation

1. Copy `scripts/kapsel.py` into your agent's workspace scripts directory
2. Make sure `rclone` is installed and configured with a cloud remote
3. Set `KAPSEL_REMOTE` to your preferred storage path
4. Add the commands to your agent's memory/instructions so it knows they exist
