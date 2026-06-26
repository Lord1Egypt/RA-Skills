---
name: memory-manager-v2
description: OpenClaw-native memory maintenance, snapshots, indexing health checks, and review workflows. Use when you need to protect context before risky work, troubleshoot memory_search, create memory snapshots, review recent daily notes for durable learnings, archive old daily notes safely, or inspect memory provider/index health in an OpenClaw workspace.
---

# Memory Manager v2

Maintain OpenClaw memory **without replacing it**.

This skill is for the existing OpenClaw memory model:
- `MEMORY.md` for curated long-term memory
- `memory/YYYY-MM-DD.md` for daily notes
- OpenClaw `memory_search` / `memory_get` for retrieval

Do **not** migrate the workspace into a different memory architecture.
Do **not** move canonical daily memory files by default.
Do **not** present keyword grep as semantic search.

## Use this skill for

- Pre-compaction or pre-risk memory snapshots
- Memory-search troubleshooting and recovery
- Embedding/index health checks
- Reviewing recent daily notes for durable takeaways
- Safe archival of old daily notes
- Quick memory hygiene/status checks

## Resource layout

- `scripts/check.ps1` — quick health/status summary
- `scripts/snapshot.ps1` — create a safe snapshot from current memory files
- `scripts/review.ps1` — generate a review draft from recent daily notes
- `scripts/search.ps1` — wrapper around `openclaw memory search` with keyword fallback
- `scripts/doctor.ps1` — diagnose provider/index readiness and attempt repair
- `scripts/archive.ps1` — archive older daily notes safely
- `references/workflow.md` — operating rules and recommended workflows

## Core rules

1. Preserve `MEMORY.md`.
2. Preserve `memory/YYYY-MM-DD.md` as the canonical daily log format.
3. Never overwrite existing memory files when a safe append or sidecar file is enough.
4. Prefer OpenClaw-native memory commands over homegrown substitutes.
5. Label fallback modes honestly.

## Recommended workflows

### 1) Quick memory health check
Run:

```powershell
pwsh -File scripts/check.ps1
```

Use when you want:
- today file existence
- recent daily note count
- snapshot count
- index/provider health summary

### 2) Troubleshoot memory search
Run:

```powershell
pwsh -File scripts/doctor.ps1
```

Use when:
- `memory_search` is unavailable
- embeddings are failing
- index appears empty
- SQLite lock or provider issues are suspected

To attempt automatic recovery:

```powershell
pwsh -File scripts/doctor.ps1 -Repair
```

### 3) Create snapshot before risky work
Run:

```powershell
pwsh -File scripts/snapshot.ps1
```

Use before:
- large refactors
- config changes
- memory cleanup
- provider/index changes
- long sessions likely to compact

### 4) Review recent memory into durable learnings
Run:

```powershell
pwsh -File scripts/review.ps1 -Days 7
```

Use when:
- promoting facts or preferences into `MEMORY.md`
- summarizing recent activity
- finding repeated themes or decisions

### 5) Search memory
Run:

```powershell
pwsh -File scripts/search.ps1 -Query "jobpulse redesign"
```

Behavior:
- first tries `openclaw memory search`
- falls back to keyword search only if semantic search fails
- reports which mode was used

### 6) Archive older daily notes
Run:

```powershell
pwsh -File scripts/archive.ps1 -KeepDays 30
```

Use when old daily notes should move out of the main `memory/` folder without disturbing recent working memory.

## Portability note

These scripts are PowerShell-first because many OpenClaw workspaces run on Windows. They avoid machine-specific paths where possible and accept `-Workspace` overrides for portability.

## Read next

For workflow guidance and safety boundaries, read `references/workflow.md`.
