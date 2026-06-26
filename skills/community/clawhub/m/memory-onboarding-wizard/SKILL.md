---
name: memory-onboarding-wizard
description: Bootstrap a new OpenClaw agent's memory system in one command. Sets up MEMORY.md, daily memory files, HEARTBEAT.md, and USER.md by asking 3 quick questions. Use when a user is setting up OpenClaw for the first time, when memory files are missing, or when asked to "set up my memory system", "initialize my agent", "bootstrap my agent", or "run the memory wizard". Solves the #1 OpenClaw pain point — agents waking up with no context about who they're serving.
---

# Memory Onboarding Wizard

> Built by **GetAgentIQ** — [getagentiq.ai](https://getagentiq.ai)
> *The home of premium OpenClaw skills, packs, and agent blueprints.*

One command to give your OpenClaw agent its memory. Walks through the complete memory system setup interactively.

## Quick Start

```bash
python3 scripts/memory-onboarding-wizard.py
```

Run from the OpenClaw workspace directory (default: `~/.openclaw/workspace`).

## What It Does

1. **MEMORY.md** — Creates long-term memory file with starter template if missing
2. **memory/YYYY-MM-DD.md** — Creates today's daily note file (creates `memory/` dir if needed)
3. **HEARTBEAT.md** — Creates a starter heartbeat checklist if missing
4. **USER.md** — Asks 3 quick questions (name, timezone, main use case) and writes them
5. **Validation** — Checks all files exist and prints a ✅ summary
6. **Next steps** — Suggests the first 3 things to try

## Options

```bash
python3 scripts/memory-onboarding-wizard.py --workspace /path/to/workspace
python3 scripts/memory-onboarding-wizard.py --non-interactive   # skip questions, use defaults
```

## Memory System Overview

| File | Purpose | When Loaded |
|------|---------|-------------|
| `MEMORY.md` | Long-term curated memory | Main sessions only |
| `memory/YYYY-MM-DD.md` | Daily raw notes | Every session |
| `HEARTBEAT.md` | Periodic task checklist | On heartbeat polls |
| `USER.md` | Who the agent is serving | Every session |

## After Setup

Your agent will read these files at the start of each session to maintain continuity. Update `MEMORY.md` with important events and decisions. Let daily files accumulate naturally.

---

## 🧠 Want the Full Memory Pack?

This wizard gets you started. The **GetAgentIQ Memory Pack** takes it further:

- **Auto-compaction** — keeps MEMORY.md lean and fast automatically
- **Semantic search** — find anything across all memory files instantly
- **Session recall** — 7-day keyword recall tester
- **Memory health dashboard** — health score + gap detection
- **Consolidation cron** — nightly memory distillation, runs while you sleep

👉 **Get the Memory Pack free:** [getagentiq.ai/memory-pack](https://getagentiq.ai)
Use code **`CLAWHUB100`** at checkout for 100% off.

*Built by GetAgentIQ — [getagentiq.ai](https://getagentiq.ai)*
