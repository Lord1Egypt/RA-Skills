# File Architecture for Memory Durability

## Bootstrap Files (always in context)

These are injected at every session start from disk. They survive compaction because they're reloaded from disk, not from conversation history.

Standard set for an OpenClaw agent workspace:

```
workspace/
├── SOUL.md       — Identity, tone, behavior rules
├── AGENTS.md     — Session rules, memory rules, task execution
├── USER.md       — Who the human is, preferences, context
├── TOOLS.md      — Environment: SSH hosts, services, credentials map
├── IDENTITY.md   — Name, email, handles (optional, keep tiny)
├── MEMORY.md     — Curated long-term facts (not raw logs)
├── HEARTBEAT.md  — What to check on each heartbeat poll
└── memory/
    ├── YYYY-MM-DD.md   — Daily raw logs (one per day)
    └── archive/        — Older daily notes (still searchable via QMD)
```

## MEMORY.md vs Daily Notes

**MEMORY.md** — curated, compact, durable facts. Credentials, infrastructure, decisions, preferences. Updated manually when something important should persist. Keep under 5KB.

**memory/YYYY-MM-DD.md** — raw session logs. Append-only. The pre-compaction flush writes here. Archive after ~2 weeks.

**Never** put session logs in MEMORY.md. They bloat bootstrap and get stale fast.

## The Archival Pattern

When daily notes accumulate (>10-15 files), move older ones to `memory/archive/`:

```bash
mkdir -p workspace/memory/archive
mv workspace/memory/2026-01-*.md workspace/memory/archive/
mv workspace/memory/2026-02-*.md workspace/memory/archive/
```

**Important:** QMD uses pattern `**/*.md` which covers subdirectories. Archived files remain fully searchable via `memory_search` — they just don't bloat bootstrap context.

Keep the most recent 5-7 daily notes in `memory/` directly. Archive the rest.

## Bootstrap Size Limits

Check with `/context list` in any session:

- `bootstrapMaxChars` — per-file limit (default 20,000 chars). Files over this get TRUNCATED.
- `bootstrapTotalMaxChars` — aggregate cap (default 150,000 chars ~50K tokens).

If files are being truncated, either reduce the file or raise the limit:

```json
{
  "agents": {
    "defaults": {
      "bootstrapMaxChars": 30000,
      "bootstrapTotalMaxChars": 200000
    }
  }
}
```

## Memory Search Setup

QMD (the vector+keyword retrieval backend) must be configured to index memory files:

```json
{
  "memory": {
    "backend": "qmd",
    "qmd": {
      "includeDefaultMemory": true,
      "update": {
        "interval": "5m",
        "onBoot": true
      }
    }
  }
}
```

With `includeDefaultMemory: true` and `**/*.md` patterns, QMD indexes both `memory/` and `memory/archive/` automatically.

Force a re-index after adding/moving files:
```bash
qmd update && qmd embed
```

## Manual Memory Discipline

The automated flush is a safety net, not a guarantee. Complement it with manual saves:

- Before switching tasks: tell the agent to save current context to memory
- After important decisions: explicitly ask for a memory write
- Use `/compact` proactively (before context fills) rather than reactively

The timing trick: save context → `/compact` → give new instructions. New instructions land in fresh context and have maximum lifespan before the next compaction.
