# MemoryRouter — Installation Guide

## Prerequisites

- OpenClaw installed and running
- Node.js 18+ (built-in `fs` and `path` — no npm packages needed)
- A `MEMORY.md` file in your workspace (can be empty initially)

## Quick Install (1 minute)

```bash
# 1. Create the skill directory
mkdir -p ~/.openclaw/workspace/skills/memory-router

# 2. Copy the skill files
# Place these files from this package into the directory above:
#   - memory-router.js   (core engine)
#   - config.json          (thresholds and options)
#   - SKILL.md             (skill definition)
#   - README.md            (this guide)

# 3. Make executable
chmod +x ~/.openclaw/workspace/skills/memory-router/memory-router.js

# 4. Test it works
node ~/.openclaw/workspace/skills/memory-router/memory-router.js --status
```

Expected output:
```
=== MemoryRouter Status ===

MEMORY.md: X lines, Y KB ✅ OK
memory/: 0 files, 0.0 KB total
self-improving/: 0 files
proactivity/: 0 files
archives: 0 files
manifest: not generated
entity index: 0 entities
WAL: not initialized
```

## Configuration

Edit `config.json` to customize behavior:

```json
{
  "thresholds": {
    "memoryMdMaxLines": 500,
    "memoryMdMaxChars": 25000,
    "tierArchiveMinAgeDays": 3,
    "auditMaxFiles": 50
  },
  "tiering": {
    "archiveDir": "memory/active",
    "retentionDays": 90,
    "keepInMemory": [
      "identity", "preferences", "relationships",
      "projects", "patterns", "boundaries", "key_facts"
    ]
  },
  "manifest": {
    "generateOnTier": true,
    "manifestPath": "memory/memory-manifest.json"
  },
  "audit": {
    "reportPath": "memory/memory-audit-report.md",
    "duplicateThreshold": 0.7,
    "conflictKeywords": [
      "revised", "updated", "changed", "no longer",
      "actually", "correction", "mistake"
    ]
  }
}
```

### Key settings explained

| Setting | Default | What it does |
|---------|---------|-------------|
| `memoryMdMaxLines` | 500 | Auto-tier triggers when MEMORY.md exceeds this line count |
| `memoryMdMaxChars` | 25000 | Same, but by character count (whichever threshold is hit first) |
| `tierArchiveMinAgeDays` | 3 | Sections must be this old before archiving |
| `retentionDays` | 90 | ⚠️ Archived files older than this are **candidates for deletion**. Irreversible. Set to 365+ until confident. |
| `keepInMemory` | see above | Headers/keywords that always stay in the core MEMORY.md |
| `generateOnTier` | true | Auto-generate manifest after tiering |
| `duplicateThreshold` | 0.7 | Similarity score (>70%) to flag as potential duplicate |

## Heartbeat Integration

Add this to your `HEARTBEAT.md` under scheduled tasks:

```markdown
### 🔧 MemoryRouter (SAFE commands only)

- Run `node skills/memory-router/memory-router.js --compact` to update manifest ✅ safe
- Run `node skills/memory-router/memory-router.js --audit` to check for issues ✅ safe
- Run `node skills/memory-router/memory-router.js --status` for health overview ✅ safe
- ⚠️ Do NOT auto-run `--tier` during heartbeats — it permanently rewrites MEMORY.md
- `--tier --dry-run` is side-effect free (no files created or modified)
- For tiering: run `--tier --dry-run` manually, review output, then `--tier --confirm`
- Check `memory/memory-audit-report.md` for any flagged conflicts
```

**Important:** `--tier` permanently rewrites MEMORY.md. Only run it manually with `--confirm` after reviewing `--dry-run` output.

## Agent Memory Loading Protocol

When your agent wakes up, use the manifest instead of loading all memory files:

1. Read `memory/memory-manifest.json`
2. Load all `required: true` files
3. For `required: false` files, use `memory_search` to check relevance
4. Load only the top 3-5 most relevant optional files

This gives you **70-85% context reduction** — load what matters, skip the rest.

## Commands Reference

| Command | What it does |
|---------|-------------|
| `--tier` | Auto-tier MEMORY.md (split core + archive) |
| `--compact` | Generate per-session manifest |
| `--compact --query "text"` | Query-aware manifest with entity boosting |
| `--compact --budget N` | Manifest filtered to N tokens |
| `--audit` | Scan for duplicates/conflicts |
| `--status` | Show memory health overview |
| `--entity add <name> <type> <files...>` | Add entity to index |
| `--entity list` | List all entities |
| `--entity search <query>` | Search entities |
| `--wal init` | Initialize WAL (session state) |
| `--wal get` | Show current WAL state |
| `--wal update <section> --content "<text>"` | Update WAL section |

## Troubleshooting

### "No MEMORY.md found"

Create one:
```bash
echo "# MEMORY.md - Long-Term Memory" > ~/.openclaw/workspace/MEMORY.md
```

### "Memory directory not found"

Create it:
```bash
mkdir -p ~/.openclaw/workspace/memory
```

### Tiering not working

Check your thresholds in `config.json`. If MEMORY.md is under 500 lines and 25KB, nothing happens — that's by design.

### Manifest shows wrong file count

Run `--compact` again. The manifest is regenerated fresh each time.

### Entity search returns nothing

Add entities first:
```bash
node memory-router.js --entity add james person USER.md IDENTITY.md
```

## Custom Workspace Path

If you want to use a different workspace:

```bash
MM_WORKSPACE=/path/to/your/workspace node memory-router.js --status
```
