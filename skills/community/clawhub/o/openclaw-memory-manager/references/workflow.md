# Memory Manager v2 Workflow

## Intent

This skill extends the existing OpenClaw memory workflow. It does not replace it.

Canonical sources remain:
- `MEMORY.md`
- `memory/YYYY-MM-DD.md`

## Safe operating pattern

### Check
Use `check.ps1` for a quick summary before making changes.

### Snapshot
Use `snapshot.ps1` before risky operations, compaction-sensitive work, or memory/index changes.

### Doctor
Use `doctor.ps1` when semantic memory is unhealthy or unavailable.

### Review
Use `review.ps1` to extract durable learnings from recent daily notes into a review draft. Do not auto-overwrite `MEMORY.md`.

### Archive
Use `archive.ps1` only for older daily notes. Never archive today's daily file.

## Red lines

- Do not overwrite `MEMORY.md`.
- Do not move today's `memory/YYYY-MM-DD.md`.
- Do not silently rewrite memory architecture.
- Do not claim keyword search is semantic search.

## Suggested automation

### Light-touch heartbeat usage
- Run `check.ps1` occasionally.
- Run `doctor.ps1` when memory tooling fails.
- Run `review.ps1 -Days 7` every few days.

### Manual high-value usage
- Run `snapshot.ps1` before large project edits or memory/provider changes.
- Run `archive.ps1 -KeepDays 30` only when the daily-note folder needs cleanup.
