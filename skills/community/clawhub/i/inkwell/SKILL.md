---
name: mindkeeper
description: "Bootstrap a complete 3-layer memory system for any OpenClaw agent. PARA knowledge structure, QMD search integration, daily consolidation cron, transcript verification, and end-of-day sign-off routine — all in one install. Use when: setting up memory, initializing a knowledge base, bootstrapping memory, configuring PARA structure, setting up QMD, creating a second brain, organizing agent knowledge, enabling daily consolidation, or configuring sign-off routines."
---

# Mindkeeper — Complete Agent Memory System

Mindkeeper bootstraps a production-grade, 3-layer memory system for OpenClaw agents. It turns a fresh agent into one that remembers, learns, and organizes knowledge automatically.

## Architecture Overview

Three layers, each serving a distinct purpose:

```
Layer 1: MEMORY.md          — Tacit knowledge (preferences, lessons, patterns)
Layer 2: memory/*.md        — Daily notes (raw capture of what happened)
Layer 3: /life/ (PARA)      — Structured knowledge repo, QMD-indexed
         ├── projects/      — Active endeavors with goals and deadlines
         ├── areas/         — Ongoing responsibilities (no end date)
         ├── resources/     — Reference material, how-tos, patterns
         └── archive/       — Completed or inactive items
```

Supporting systems:
- **QMD** — Local semantic search across all layers (BM25 + vectors + reranking)
- **Daily consolidation** — Cron job extracts knowledge from sessions automatically
- **Transcript verification** — Echo and store voice transcripts for accuracy
- **Sign-off routine** — End-of-day consolidation, memory update, and shutdown

## Setup

### 1. Run the bootstrap script

The setup script creates the directory structure and starter files. It never overwrites existing files.

**Windows (PowerShell):**
```powershell
pwsh -File "<skill_dir>/scripts/setup.ps1" -Workspace "<workspace_path>"
```

**Linux/Mac (Bash):**
```bash
bash "<skill_dir>/scripts/setup.sh" "<workspace_path>"
```

Where `<workspace_path>` is the OpenClaw workspace root (typically `~/.openclaw/workspace`).

### 2. Configure QMD (recommended)

QMD provides semantic search across all your knowledge files and session transcripts. See [references/qmd-setup.md](references/qmd-setup.md) for the complete setup guide including Windows workarounds.

### 3. Set up daily consolidation

A cron job reviews all sessions and extracts knowledge into your PARA structure. See [references/consolidation.md](references/consolidation.md) for the exact cron command, prompt, and configuration options.

### 4. Enable transcript verification (optional)

For voice-heavy workflows, add inline transcript echo and local storage. See [references/transcripts.md](references/transcripts.md) for the two-layer approach.

### 5. Configure sign-off routine (optional)

End-of-day routine: consolidation → memory update → status report → optional gateway stop. See [references/sign-off.md](references/sign-off.md) for the complete workflow.

## Working with the Memory System

### Writing to memory

- **Quick capture** → Append to today's daily note (`memory/YYYY-MM-DD.md`)
- **Lesson learned** → Update `MEMORY.md` with the distilled insight
- **Project update** → Update the relevant file in `life/projects/`
- **New reference** → Create a file in `life/resources/`
- **Decision record** → Use the ADR template in `life/resources/decisions/`

### Searching memory

Use `memory_search` to find information across all indexed files. QMD searches MEMORY.md, daily notes, and the entire `/life/` tree.

### Maintaining memory

- During heartbeats: review recent daily notes, promote insights to MEMORY.md
- During consolidation: cron job handles session → knowledge extraction
- Periodically: move completed projects to `life/archive/`, prune stale content

## Templates

Starter templates are in the `templates/` directory:

| Template | Purpose |
|----------|---------|
| `templates/project.md` | New project file for `life/projects/` |
| `templates/area.md` | New area of responsibility for `life/areas/` |
| `templates/resource.md` | Reference material for `life/resources/` |
| `templates/decision.md` | Lightweight ADR for `life/resources/decisions/` |
| `templates/daily-note.md` | Daily note for `memory/` |
| `templates/memory.md` | MEMORY.md starter with recommended sections |

Copy and customize as needed. The setup script uses these templates for initial file creation.

## Reference Docs

| Document | Read when... |
|----------|-------------|
| [references/qmd-setup.md](references/qmd-setup.md) | Setting up QMD search backend |
| [references/consolidation.md](references/consolidation.md) | Configuring daily consolidation cron |
| [references/transcripts.md](references/transcripts.md) | Setting up voice transcript verification |
| [references/sign-off.md](references/sign-off.md) | Configuring end-of-day routine |

## Tips

- **MEMORY.md is your soul** — Keep it curated. It's the first thing loaded each session.
- **Daily notes are disposable** — Raw capture, not polished writing. Speed > quality.
- **PARA is flexible** — Don't overthink categories. Move things as understanding evolves.
- **Templates are starting points** — Customize them to match your human's workflow.
- **QMD fallback is automatic** — If QMD goes down, builtin search takes over seamlessly.
