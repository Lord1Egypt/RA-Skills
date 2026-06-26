---
name: openclaw-harness
description: "Cross-session context manager for AI agents with checkpoint/snapshot, Build-Verify-Fix closure, and entropy management (GC). Use when: (1) creating a task checkpoint before risky work, (2) verifying task completion via harness verify, (3) cleaning up stale checkpoints with harness gc, (4) restoring a previous checkpoint, (5) tracking cross-session progress, or (6) linting agent configuration files (SOUL.md/IDENTITY.md/AGENTS.md)."
---

# openclaw-harness

> Cross-session context tracking, entropy management, and verification closure for AI agents.

## Quick Reference

| Command | Description |
|---------|-------------|
| `harness init [--force]` | Initialize Harness in current workspace |
| `harness status [-v\|-j\|-s]` | Show Harness status |
| `harness checkpoint create <label> [--tag <tag>]` | Create a checkpoint snapshot |
| `harness checkpoint list` | List all checkpoints |
| `harness checkpoint restore <cp-id> [--force]` | Restore to a checkpoint |
| `harness checkpoint delete <cp-id>` | Delete a checkpoint |
| `harness verify [--rule '<json>'] [--exit-code]` | Run verification checks |
| `harness gc [--dry-run] [--max-cp N] [--max-age N] [--aggressive]` | Entropy cleanup |
| `harness progress show` | Show cross-session progress |
| `harness linter [--fix] [--strict]` | Lint SOUL/IDENTITY/AGENTS files |
| `harness fix [placeholders\|whitespace\|trailing\|all]` | Auto-fix linter issues |

## Core Workflow

```bash
# 1. Initialize (once per workspace)
harness init

# 2. Create checkpoint before risky work
harness checkpoint create "before-refactor"

# 3. Do work, verify
harness verify

# 4. Create another checkpoint when milestone reached
harness checkpoint create "feature-done" --tag "feature"

# 5. Preview cleanup
harness gc --dry-run

# 6. Restore if needed
harness checkpoint restore <cp-id> --force
```

## Safety Rules

- **Never deleted**: SOUL.md, IDENTITY.md, USER.md, MEMORY.md, AGENTS.md, TOOLS.md, TASKS.md, .harness/
- All deletions logged to `.harness/gc.log`
- Deleted files archived to `.harness/.trash/` before removal

## Directory Structure

```
.harness/                   # Harness state root (created by init)
├── .initialized            # Init marker (version + timestamp)
├── config.json             # Config: max_checkpoints, max_age_days, etc.
├── gc.log                  # Deletion audit log
├── checkpoints/<cp-id>/    # Checkpoint snapshots
│   ├── manifest.json       # Snapshot manifest
│   └── files/              # Snapshot copies
├── reports/                # Verification reports
├── tasks/                  # Task metadata
├── tmp/                    # Temp files (GC target)
└── .agent-progress.json    # Cross-session progress state
```

## Advanced Usage

**Custom verification rules:**
```bash
harness verify --rule '[{"name":"Build OK","type":"command","path":"npm run build"}]'
```

**Checkpoint management:**
```bash
harness checkpoint create "label" --tag "v1" --tag "stable"
harness checkpoint show <cp-id>
```

**GC with limits:**
```bash
harness gc --max-cp 5        # Max 5 checkpoints per task
harness gc --max-age 7      # Delete checkpoints older than 7 days
harness gc --aggressive     # Also clean tmp/ directory
```

**Progress tracking:**
```bash
harness progress show
harness progress set-phase "Phase 2"
harness progress add-blocker "Waiting for API key"
```

**Linter and fix:**
```bash
harness linter --strict     # Fail on warnings too
harness linter --fix        # Auto-fix issues (creates .orig backups)
harness fix all --dry-run   # Preview all auto-fixes
```

## Detailed Reference

For complete documentation, load the relevant reference:
- **Architecture & design**: See [references/architecture.md](references/architecture.md)
- **Requirements & acceptance criteria**: See [references/requirement.md](references/requirement.md)
- **Technical knowledge package**: See [references/knowledge-package.md](references/knowledge-package.md)
- **Maintenance guide**: See [references/maintenance.md](references/maintenance.md)

## Scripts

This skill includes helper scripts for skill developers:

- `scripts/init_skill.py` — Initialize a new skill from template
- `scripts/package_skill.py` — Package and validate a skill into .skill file

```bash
# Create a new skill
python scripts/init_skill.py my-new-skill --path /path/to/output

# Package a skill
python scripts/package_skill.py /path/to/skill-folder
```
