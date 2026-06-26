---
name: workspace-audit
description: Nightly workspace audit — auto-discover file dependencies by scanning all workspace files for cross-references, manage HOT/WARM/COLD memory tiers, detect orphaned files, sync inconsistencies, and report workspace health. Works out of the box on any OpenClaw workspace. Supports optional local-overrides.md for custom dependency rules. Use when triggered by a nightly cron job, or when the user asks to audit, clean up, or check workspace health.
---

# Workspace Audit

Auto-discover, clean, tier, sync, and report on an OpenClaw workspace.

## Memory Tiers

- **HOT** — auto-loaded every session: root `.md` files (`MEMORY.md`, `TODO.md`, `USER.md`, etc.)
- **WARM** — on disk, loaded on demand: `memory/*.md`, `projects/*/` files
- **COLD** — archived, rarely touched: `memory/archive/`

## Procedure

### 1. Dependency Discovery

Scan every `.md` and `.json` file in `workspace/` (skip `skills/`, `.git/`, `archive/`).

**For each file, extract:**
- File paths (relative or absolute) mentioned in content
- Section headings that appear in multiple files (shared topics)
- Lists that substantially overlap across files (potential duplicates)

**Then cross-reference against:**
- Cron job prompts: `cron list` → extract all file paths from every job's `message` field → verify each file exists
- Index files: any file named `README.md` or containing a Markdown table with path-like entries → verify linked targets exist
- Tree diagrams: code blocks containing directory trees → verify paths match actual filesystem

Build a dependency graph: `{file → [files it references]}`.

Flag:
- **Broken links**: referenced file doesn't exist
- **Orphaned files**: files referenced by nothing (not in any cron, not linked from any index, not a root auto-loaded file)
- **Content drift**: two files that reference the same data but have diverged (e.g., a list appears in both MEMORY.md and another file but they differ)

### 2. Memory Hygiene

Read all files in `memory/` (skip `archive/`).

- **Merge**: Combine related entries across files (same topic split across daily files)
- **Deduplicate**: Remove identical content that exists in multiple places
- **Prune**: Delete entries confirmed no longer useful (completed one-off tasks, expired temporary notes)
- **Archive**: Move daily files older than 7 days to `memory/archive/`
- **Rename**: Fix inconsistent naming if found

After changes, update the workspace structure tree in `MEMORY.md` if one exists.

### 3. Auto-promote / Demote

Apply tier rules. See [tier-rules.md](references/tier-rules.md) for thresholds and exceptions.

- **Promote WARM → HOT**: Add a summary line to `MEMORY.md`
- **Demote HOT → WARM**: Remove from `MEMORY.md`, ensure info exists in a WARM file
- **Demote WARM → COLD**: Move file to `memory/archive/`

**Every promotion or demotion must be listed in the report.**

### 4. Local Overrides (optional)

If [local-overrides.md](references/local-overrides.md) exists, run those additional checks. These are user-specific dependency pairs that can't be auto-discovered (e.g., content-level sync between specific sections).

Skip this step if the file doesn't exist.

### 5. Report

Send a concise message to the user:

```
🔍 Workspace Audit — {date}

**Dependencies**
- {broken links found and fixed/flagged}
- {orphaned files found}
- {content drift detected}
- {or "All dependencies healthy"}

**Cleaned**
- {what was merged/deleted/archived, or "Nothing — all clean"}

**Tier changes**
- ⬆️ Promoted: {item} (WARM → HOT) — reason
- ⬇️ Demoted: {item} (HOT → WARM) — reason
- {or "No tier changes"}

**Sync issues**
- {local override mismatches, or "All in sync"}

**Health**
- {file count} workspace files, {cron count} cron jobs, {error count} cron errors
- {any expiring items}
```
