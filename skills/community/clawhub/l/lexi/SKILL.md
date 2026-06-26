---
name: lexi
version: 1.1.0
author: mcroebuck
license: MIT
description: Filesystem librarian for OpenClaw environments. Systematically scans, catalogs, and organizes the entire file structure — identifying orphaned files, misplaced assets, stale artifacts, broken references, and structural inefficiencies. Use when the user says "audit my files", "organize my filesystem", "run lexi", "clean up", "catalog my files", "file audit", "where does this go", or any variation requesting filesystem review, reorganization, or cleanup.
metadata: { "openclaw": { "always": false } }
---

# Lexi — Filesystem Librarian

A structured filesystem audit process organized into six sequential phases. Each phase completes before the next begins. The scanning framework at `{baseDir}/scanning-framework.md` provides classification definitions, exclusion rules, catalog structure, and report templates.

**Safety:** Phases 1–4 are strictly read-only — observation, cataloging, and reporting only. File modifications happen exclusively in Phase 5, and only with explicit user approval for each batch.

---

## Phase 1: Scope & Exclusions

### Steps

1. Confirm the scan root with the user. Default: `~` (full home directory).

2. **Returning User Fast Path:** When `USER.md` contains scan history and known preferences:
   - Present stored exclusions and scope: "Last scan covered [root] with these exclusions: [list]. Still accurate?"
   - If confirmed → proceed to Phase 2.
   - If changes needed → update only what changed.

3. **New Scan Setup:** Confirm exclusion zones per the scanning framework:
   - **Always excluded:** `.ssh/`, `.gnupg/`, `.secrets/`, `.git/` internals, `.env` files, `auth-profiles.json`, `credentials.json`, `node_modules/`, `__pycache__/`, `.venv/` internals
   - **User-configurable exclusions:** Any additional paths the user wants to protect
   - Present the exclusion list and get confirmation before scanning.

4. **Scan mode selection:**
   - **Full audit** — first run or periodic deep scan of everything
   - **Incremental** — only files modified since last audit date
   - **Targeted** — a specific directory tree only

5. Save scope and exclusions for future sessions (update USER.md).

---

## Phase 2: Discovery & Inventory

The raw scan phase — building a complete picture of what exists.

### Steps

1. **Directory tree scan:**
   - For each directory under scan root (respecting exclusions): record path, file count, total size, last modified date
   - Flag: empty directories, deeply nested paths (>5 levels), unusually large directories

2. **File inventory:**
   - For each file (respecting exclusions): record path, size, last modified, file type/extension
   - Flag: files >10MB, files not modified in >90 days, files with no extension

3. **Structural scan:**
   - Identify all git repositories (directories containing `.git/`)
   - Identify all symlinks and their targets (flag broken symlinks)
   - Identify all virtual environments (`.venv/`, `venv/`, `node_modules/`)
   - Map all OpenClaw workspaces and their agent associations
   - Identify duplicate filenames across different directories

4. **Reference scan (critical for safe reorganization):**
   - Grep all `.md` files for path references (absolute and relative)
   - Grep all `.sh`, `.py`, `.js`, `.ts` scripts for hardcoded paths
   - Extract paths from crontab (`crontab -l`)
   - Extract paths from PM2 configs
   - Extract paths from OpenClaw agent configs
   - Map all symlinks with source → target
   - Build the **dependency graph**: which files reference which paths

5. **Output:** A raw inventory file (structured, not prose) — working data for Phase 3, not presented to the user.

### Notes
- This phase can be slow on large filesystems. Provide progress updates.
- For very large directory trees, work in segments (e.g., scan `~/.openclaw/` first, then `~/projects/`, etc.)
- File contents are not read in this phase except during reference scanning. The goal is cataloging structure, not auditing content.

---

## Phase 3: Classification & Analysis

Using the inventory from Phase 2, classify every significant file and directory.

### Steps

1. **Directory classification** — assign each directory a type from the scanning framework:
   - Active project, Archive, Agent workspace, Config/dotfile, Data store, Tool/script, Documentation, Media/assets, Temp/build artifact, Unknown

2. **File classification** — assign each file a status:
   - 🟢 **Active** — recently used, referenced, serves clear purpose
   - 🟡 **Review** — purpose unclear, may be stale, needs human decision
   - 🔴 **Orphaned** — no references, old, no apparent purpose
   - ⚪ **Stale** — was once active, now outdated (old logs, superseded configs, dead scripts)
   - 🔵 **Misplaced** — serves a purpose but lives in the wrong location
   - ⚫ **Duplicate** — same or near-identical content exists elsewhere

3. **Structural analysis:**
   - Identify directories serving the same purpose (fragmentation)
   - Identify naming inconsistencies (kebab-case vs. snake_case vs. mixed)
   - Identify depth violations (files buried too deep or too shallow for their type)
   - Identify orphaned project directories (no git activity, no recent modifications, not referenced)

4. **Placement analysis** — for every 🔵 Misplaced file:
   - Current location
   - Recommended location (with reasoning)
   - Reference impact (what would break if moved without updating references)

5. **Deduplication analysis** — for every ⚫ Duplicate:
   - All locations where the content exists
   - Which copy is authoritative (most recent, most referenced, in the "right" place)
   - Recommendation: which to keep, which to remove

---

## Phase 4: Report & Collaborative Review

### Steps

1. **Generate the audit report** following the structure in the scanning framework:
   - Executive Summary (total files, directories, classifications breakdown)
   - Directory Map (purpose of each top-level and second-level directory)
   - High-Priority Findings (orphaned, misplaced, duplicated — sorted by impact)
   - Structural Recommendations (directory consolidation, naming, hierarchy changes)
   - Reference Impact Assessment (what would break with proposed changes)
   - Proposed Catalog (the living index document)

2. **Present the Executive Summary first:**
   - "Here's what I found across [N] files in [M] directories: [breakdown]. Ready to go through the findings?"

3. **Collaborative review mode** — work through findings by priority:
   - Present the finding with specific paths
   - Explain the reasoning
   - Show reference impact if applicable
   - Wait for user decision: approve, reject, defer, or discuss
   - Track all decisions

4. **Build the action plan** from approved changes:
   - Group actions into safe batches (moves that don't depend on each other)
   - Order batches to minimize intermediate breakage
   - Include reference updates in same batch as the move they depend on

### Notes
- The user may have context about why a file exists where it does. When the user says "that's there on purpose," accept it and record it in the catalog so future scans don't re-flag it.
- Present file sizes and dates — they help the user make decisions about stale files.

---

## Phase 5: Execution (Requires Explicit Approval)

### Steps

1. **Pre-flight safety check:**
   - Confirm the archive directory exists: `~/.lexi-archive/YYYY-MM-DD/`
   - Confirm no active processes are using files in the current batch
   - Confirm git repos in the affected area have clean working trees

2. **Execute approved changes one batch at a time:**
   - **Moves:** `mv` with archive backup of original location manifest
   - **Deletions:** Always archive first — move to `~/.lexi-archive/YYYY-MM-DD/` with a manifest entry recording original path, size, date, and reason for removal
   - **Reference updates:** Update all files that referenced the old path
   - **Symlink cleanup:** Remove broken symlinks, update targets for moved files

3. **After each batch:**
   - Verify the moves completed correctly
   - Run a quick reference check — grep for any remaining old-path references
   - Report results to user before proceeding to next batch

4. **Post-execution:**
   - Generate a changelog: what moved, what was archived, what references were updated
   - Update the catalog with new locations
   - Save the changelog to `~/.lexi-archive/YYYY-MM-DD/changelog.md`

### Notes
- The archive is sacred — files are always archived before removal.
- If a reference update would modify a file in an excluded zone (e.g., `.secrets/`), flag it for manual update instead.
- If anything unexpected occurs during execution, stop and report rather than attempting silent recovery.

---

## Phase 6: Catalog Generation

### Steps

1. **Generate or update the living catalog** at `~/CATALOG.md`:
   - Top-level directory map with purposes
   - Key file locations (configs, scripts, data stores)
   - Agent workspace index
   - Project directory index with status (active/archived/paused)
   - Conventions (naming, depth, where new files of each type should go)
   - Last audit date and summary

2. **The catalog is the primary deliverable.** Other agents reference it when deciding where to store a file. It should be:
   - Scannable (table format where possible)
   - Authoritative (single source of truth for "where does X go?")
   - Maintainable (updated by Lexi on each audit, not manually)

3. **Save the full audit report** to the Lexi workspace:
   `<lexi_workspace>/audits/audit-YYYY-MM-DD.md`

---

## Incremental Mode (Weekly Cron / On-Demand)

For scans after the initial full audit:

1. Scan only files modified since last audit date
2. Check for new files not in the catalog
3. Check for deleted files still in the catalog
4. Check for broken references (files moved without updating refs)
5. Generate a diff report: what changed, what needs attention
6. Update the catalog with any confirmed changes

---

## Slash Command

This skill responds to `/lexi` as a slash command trigger. Also invoked by "audit my files", "organize", "run lexi", "clean up my files", "file audit", "catalog", or similar.
