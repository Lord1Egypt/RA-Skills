# Letta Memory — Integration Guide

## OpenClaw Integration

### Adding to openclaw.json

```json
{
  "skills": {
    "entries": {
      "letta-memory": {
        "enabled": true
      }
    }
  }
}
```

### Workspace Setup

The skill uses the workspace's `memory/` directory:

```
~/.openclaw/workspace/
├── memory/
│   ├── core.md              # Core memory (always in context)
│   ├── YYYY-MM-DD.md        # Daily notes
│   └── archival/
│       ├── people/
│       ├── projects/
│       ├── decisions/
│       ├── learnings/
│       └── reference/
```

### Heartbeat Integration

Add to HEARTBEAT.md to trigger memory maintenance:

```markdown
# Memory maintenance
- Run letta-memory consolidation if daily notes exist
- Trim core.md if >1000 words
- Review archival for items to promote to core
```

### Cron Job for Auto-Consolidation

```json
{
  "schedule": { "kind": "cron", "expr": "0 */6 * * *", "tz": "America/Santiago" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run letta-memory consolidation: review today's daily notes, extract notable items to archival, trim core if needed."
  }
}
```

## Other Platforms

### Claude Code / Codex

1. Copy `memory/` structure to project root
2. Add to CLAUDE.md or AGENTS.md:
   ```markdown
   ## Memory System (Letta-style)
   - Read memory/core.md at session start
   - Update core when learning new user info
   - Write archival entries for decisions and learnings
   - Run scripts/consolidate.py weekly
   ```

### Generic Agent

1. Initialize: `mkdir -p memory/archival/{people,projects,decisions,learnings,reference}`
2. Create `memory/core.md` with the template from SKILL.md
3. Agent reads core at start, writes to archival as needed
4. Run consolidation periodically

## Migrating Existing Memory

If you already have MEMORY.md (OpenClaw default):

1. Split MEMORY.md into core.md (key facts, <1000 words) and archival entries
2. Keep MEMORY.md as fallback during transition
3. Once stable, remove MEMORY.md dependency

### Migration Script

```bash
# Quick split: first 50 lines → core.md, rest → archival
head -50 MEMORY.md > memory/core.md
# Manually categorize the rest into archival/
```