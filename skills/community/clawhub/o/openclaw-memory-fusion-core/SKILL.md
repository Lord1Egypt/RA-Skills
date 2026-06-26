---
name: openclaw-memory-fusion
description: Build and operate a unified OpenClaw memory system that combines native Markdown memory, project memory, structured event memory, migration from older PROJECTS.md/improvements.md layouts, memorySearch configuration, and upgrade-safe maintenance workflows.
---

# OpenClaw Memory Fusion

Use this skill when the user wants to:
- unify OpenClaw memory into one system
- preserve or migrate older `PROJECTS.md` / `memory/*.md` / improvements data
- add structured event memory on top of native Markdown memory
- enable `memorySearch` safely for long-term and project retrieval
- audit, repair, or upgrade-check the memory setup after OpenClaw changes

This skill is designed to stay compatible with OpenClaw upgrades:
- it uses workspace Markdown files as the source of truth
- it only touches documented `memorySearch` config fields
- it keeps checkpoints, manifests, and rollback data for every mutating command
- it does not patch OpenClaw internals

## Architecture

`openclaw-memory-fusion` keeps memory in five layers:
- native memory: `MEMORY.md`, `PROJECTS.md`, `memory/YYYY-MM-DD.md`
- project memory: `projects/<slug>/overview.md`, `timeline.md`, `decisions.md`, `artifacts.md`
- project aliases: `memory_fusion/project_aliases.md` (`projects/ALIASES.md` is treated as a legacy location and migrated away from retrieval)
- ops memory: `ops/*.md` for system improvements and upgrade notes
- event memory: `memory_fusion/events/*.jsonl`
- semantic retrieval layer: `memory_fusion/semantic/*.md`

## Primary Commands

Check the current setup:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py doctor
```

Preview installation without changing anything:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py install
```

Apply installation and configure memory search:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py install --apply --provider local
```

Preview migration of legacy project memory:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py migrate
```

Apply migration:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py migrate --apply
```

Record a structured memory event:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py capture \
  --kind project_update \
  --scope project \
  --project sample-project \
  --summary "Deployment checklist moved into final validation"
```

Rebuild semantic digests:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py sync-semantic --apply
```

Generate or refresh the editable project alias registry:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py sync-aliases --apply
```

Auto-capture recent working memory into structured events:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py auto-capture --days 7 --apply
```

Check project-memory drift:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py drift-check --days 30
```

Run a reflective dream pass with safe repairs:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py dream --days 7 --apply --repair-placeholders
```

Check upgrade safety:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py upgrade-check
```

Rollback the latest mutating command:
```bash
python3 ~/.agents/skills/openclaw-memory-fusion/scripts/openclaw_memory_fusion.py rollback --latest
```

## Safety Defaults

- `install` and `migrate` are dry-run by default
- `auto-capture`, `drift-check`, and `dream` are also dry-run by default
- `sync-aliases` is also dry-run by default
- mutating commands write manifests under `workspace/memory_fusion/manifests/`
- backups go under `workspace/memory_fusion/checkpoints/`
- existing Markdown files are not overwritten unless the command is explicitly applying changes

## Reflective Features

- `auto-capture` extracts structured events from recent `memory/YYYY-MM-DD.md` and ops notes
- `sync-aliases` maintains a human-editable alias table with `Force aliases` and `Suggested aliases`
- `drift-check` compares project overview snapshot fields with more recent structured events
- `dream` chains auto-capture, drift analysis, semantic refresh, and optional placeholder repair
- placeholder repair only fills obviously incomplete `Status` / `Next step` fields; conflicting non-placeholder content is reported, not silently rewritten

## When To Avoid This Skill

Do not use this skill if the user only wants to remember a single durable preference. In that case, update the relevant Markdown memory file directly.
