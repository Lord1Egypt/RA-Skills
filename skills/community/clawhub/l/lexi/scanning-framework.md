# Lexi Scanning Framework

This document is the analytical reference for the Lexi filesystem audit process. It defines how to classify files and directories, what to exclude, how to assess structural health, and how to structure findings.

---

## 1. Exclusion Rules

### Always Excluded (Never Scan, Never Touch)
These paths are excluded from all scanning and modification. Their contents are invisible to the audit.

| Path Pattern | Reason |
|-------------|--------|
| `~/.ssh/` | Security — SSH keys and configs |
| `~/.gnupg/` | Security — GPG keys |
| `~/.secrets/` | Security — credentials, tokens, OAuth files |
| `**/.git/` | Git internals — never modify |
| `**/.env` | Environment secrets |
| `**/auth-profiles.json` | Agent auth credentials |
| `**/credentials.json` | Service credentials |
| `**/node_modules/` | Package dependencies — managed by npm/yarn |
| `**/__pycache__/` | Python bytecode cache — auto-generated |
| `**/.venv/lib/` | Virtual environment packages — managed by pip |
| `**/venv/lib/` | Virtual environment packages — managed by pip |
| `/proc/`, `/sys/`, `/dev/` | System virtual filesystems |

### User-Configurable Exclusions
The user may add paths during Phase 1. Common additions:
- Specific project directories under active development
- Large data directories that shouldn't be moved
- Directories managed by external tools

### Exclusion Behavior
- Excluded paths are **invisible** — they don't appear in the inventory, they aren't classified, and they aren't included in the catalog.
- However, **references to excluded paths** from non-excluded files ARE tracked. If a script in `~/scripts/` references `~/.secrets/api-key`, the script is inventoried and the reference is noted — but the secret file itself is not.
- Exception: `.git/` directories are excluded from scanning, but the *existence* of a `.git/` directory is noted to mark its parent as a git repository.

---

## 2. Directory Classification

Every directory gets assigned a primary type:

| Type | Description | Examples |
|------|-------------|---------|
| **Active Project** | Contains work product being actively developed or maintained | `~/projects/puentelex/`, `~/projects/hcv-procurement-model/` |
| **Paused Project** | Project directory with no significant modifications in 30-90 days | — |
| **Archived Project** | Project directory with no modifications in 90+ days, or explicitly marked archived | — |
| **Agent Workspace** | OpenClaw agent workspace directory | `~/.openclaw/workspace/`, `~/.openclaw/workspace-doc/` |
| **Config/Dotfile** | Application or system configuration | `~/.config/`, `~/.openclaw/agents/` |
| **Data Store** | Structured data (databases, CSV collections, logs) | `~/projects/crm/`, health sentinel data dirs |
| **Tool/Script** | Executable scripts, utilities, CLI tools | `~/scripts/`, `~/.local/bin/` |
| **Documentation** | Reference material, specs, guides | `~/knowledge/`, `~/briefs/` |
| **Media/Assets** | Images, audio, video, fonts | `~/.openclaw/media/` |
| **Temp/Build** | Build artifacts, caches, temporary files | `/tmp/`, `dist/`, `.next/`, `build/` |
| **Archive** | Intentional archive storage | `~/.lexi-archive/` |
| **Unknown** | Purpose unclear — requires human review | — |

### Structural Health Indicators

| Indicator | Healthy | Unhealthy |
|-----------|---------|-----------|
| **Depth** | Key files within 3 levels of home | Important files buried 6+ levels deep |
| **Naming** | Consistent convention within a directory | Mixed kebab-case, snake_case, camelCase, spaces |
| **Single Purpose** | Each directory serves one clear function | Directory contains unrelated file types |
| **Discoverability** | Directory name indicates its contents | Cryptic names (`tmp2/`, `old/`, `stuff/`, `test/`) |
| **Fragmentation** | Related files grouped together | Same project spread across multiple unrelated directories |

---

## 3. File Classification

### Status Labels

| Status | Symbol | Criteria |
|--------|--------|----------|
| **Active** | 🟢 | Modified within 30 days, OR referenced by active scripts/configs, OR serves a documented purpose |
| **Review** | 🟡 | Purpose unclear, may be stale, needs human context to classify |
| **Orphaned** | 🔴 | Not referenced by any other file, not modified in 90+ days, no clear purpose from name/location |
| **Stale** | ⚪ | Was once active but is now superseded, outdated, or irrelevant (old logs, deprecated configs, dead scripts) |
| **Misplaced** | 🔵 | File serves a clear purpose but is stored in the wrong directory relative to its type and the established hierarchy |
| **Duplicate** | ⚫ | Same or near-identical content exists in another location |

### Classification Decision Tree

```
Is the file in an excluded path?
  → Yes: SKIP (invisible)
  → No: Continue

Is the file referenced by any active config, script, cron, or agent?
  → Yes: 🟢 Active (regardless of modification date)
  → No: Continue

Was the file modified in the last 30 days?
  → Yes: Likely 🟢 Active (verify purpose from name/location)
  → No: Continue

Was the file modified in the last 90 days?
  → Yes: 🟡 Review (may be active but infrequently used)
  → No: Continue

Does the file name/path suggest a clear purpose?
  → Yes: ⚪ Stale (purpose existed but may be outdated)
  → No: 🔴 Orphaned (no purpose identifiable)

Does the same content exist elsewhere?
  → Yes: ⚫ Duplicate (determine which copy is authoritative)

Is the file in the correct directory for its type?
  → No: 🔵 Misplaced (recommend correct location)
```

### Special File Types

| File Pattern | Default Classification | Notes |
|-------------|----------------------|-------|
| `*.log` | ⚪ Stale (unless current) | Logs older than 7 days are almost always stale |
| `*.bak`, `*.backup` | ⚪ Stale | Backups should live in archive, not alongside originals |
| `*.tmp`, `*.temp` | 🔴 Orphaned | Temp files should not persist |
| `*-old.*`, `*-copy.*` | ⚫ Duplicate | Rename patterns suggest duplication |
| `*.md` in workspace root | 🟢 Active | Context files loaded by OpenClaw |
| `SKILL.md` | 🟢 Active | Skill definitions — always active |
| `*.csv`, `*.db`, `*.sqlite` | Check references | Data files — active if referenced |

---

## 4. Reference Integrity

### What Constitutes a Reference

A reference is any hardcoded path in a file that points to another file or directory. References create dependencies — moving the target without updating the reference breaks something.

| Reference Type | Where Found | How to Detect |
|---------------|-------------|---------------|
| **Markdown links** | `.md` files | `[text](path)` or bare paths in prose |
| **Script paths** | `.sh`, `.py`, `.js`, `.ts` | String literals containing `/home/`, `~/`, or relative paths |
| **Config paths** | `.yaml`, `.json`, `.toml` | Path-valued keys |
| **Cron paths** | `crontab -l` | Command strings |
| **PM2 paths** | PM2 ecosystem configs | `script` and `cwd` values |
| **Symlink targets** | Filesystem | `readlink` output |
| **Import statements** | `.py`, `.js`, `.ts` | `import`, `require`, `from` with paths |
| **Source commands** | `.sh`, `.bashrc`, `.profile` | `source`, `.` commands |

### Dependency Graph

The dependency graph maps: **File A references Path B**

Before recommending any move, the Librarian must:
1. Check if the target path appears in the dependency graph
2. Identify ALL files that reference it
3. Include reference updates in the same execution batch as the move
4. Flag references in excluded files (must be updated manually)

### Broken References

A broken reference is a path in a file that points to a location that doesn't exist. These are always findings:
- **Critical** if in a cron job, startup script, or agent config
- **High** if in an active script or frequently-used tool
- **Low** if in documentation or comments

---

## 5. Archive Protocol

### Archive Structure

```
~/.lexi-archive/
├── YYYY-MM-DD/
│   ├── changelog.md          # What was archived and why
│   ├── manifest.json         # Machine-readable: original paths, sizes, dates, reasons
│   └── files/                # Archived files in original directory structure
│       ├── projects/
│       │   └── old-project/
│       └── scripts/
│           └── deprecated-script.sh
```

### Archive Rules

1. **Every deletion is an archive.** No file leaves the filesystem without passing through `~/.lexi-archive/` first.
2. **Manifests are permanent.** Even if archived files are later purged, the manifest stays — it's the record of what existed and where.
3. **Archive retention:** Archives older than 90 days can be flagged for permanent deletion in a future audit, but only with explicit user approval.
4. **Archive is excluded from scans.** Files in `~/.lexi-archive/` are not re-scanned or re-classified. They're done.

---

## 6. Catalog Structure

The catalog (`~/CATALOG.md`) is the living index of the filesystem. It is the primary deliverable of every audit.

### Required Sections

```markdown
# Filesystem Catalog
*Last updated: YYYY-MM-DD by Lexi*
*Last full audit: YYYY-MM-DD*

## Directory Map
| Path | Type | Purpose | Owner/Agent | Status |
|------|------|---------|-------------|--------|

## Agent Workspaces
| Agent | Workspace | Key Files |
|-------|-----------|-----------|

## Active Projects
| Project | Path | Last Modified | Status |
|---------|------|---------------|--------|

## Scripts & Tools
| Tool | Path | Purpose | Referenced By |
|------|------|---------|---------------|

## Data Stores
| Store | Path | Format | Size | Last Updated |
|-------|------|--------|------|-------------|

## Conventions
- New projects go in: ~/projects/<name>/
- Scripts go in: ~/scripts/ (system) or ~/.local/bin/ (user CLIs)
- Agent workspaces: ~/.openclaw/workspace-<agent>/
- Skills: <workspace>/skills/<name>/
- Documentation: ~/knowledge/ (reference) or ~/briefs/ (generated)
- Media: project-local or ~/.openclaw/media/

## Exclusions (Not Cataloged)
[List of excluded paths and reasons]

## Archive History
| Date | Files Archived | Reason |
|------|---------------|--------|
```

### Catalog Rules

1. **The catalog is authoritative.** If it says a file goes in `~/projects/`, that's where it goes.
2. **New files should follow conventions.** Any agent creating files should check the catalog conventions section first.
3. **Lexi owns the catalog.** Other agents may read it but should not edit it directly. Propose changes through Lexi.
4. **The catalog is regenerated on every full audit** and incrementally updated on every targeted or incremental scan.

---

## 7. Report Structure

### Executive Summary
- Scan scope and date
- Total files and directories scanned
- Classification breakdown (counts and percentages by status)
- Top findings by priority
- Estimated recoverable space (from duplicates, stale files, orphans)

### Directory Health Map
For each top-level directory:
- Purpose assessment
- Health indicators (naming, depth, fragmentation)
- Recommended changes (if any)

### Findings (by priority)
Each finding includes:
- File/directory path
- Classification and reasoning
- Size and last modified date
- Dependency graph impact (who references this?)
- Recommendation: keep / move / archive / merge
- If move: proposed new location + required reference updates

### Reference Integrity Report
- Broken references found
- High-risk references (would break if files are moved)
- Circular references or redundant symlinks

### Structural Recommendations
- Directory consolidation opportunities
- Naming convention standardization
- Depth optimization
- New directories that should be created

### Proposed Catalog
- The draft catalog that will become `~/CATALOG.md` after approval

---

## 8. Incremental Scan Protocol

For periodic (weekly cron) or on-demand quick scans:

1. **Load last audit date** from catalog
2. **Find modified files:** `find ~ -newer <last-audit-timestamp> -not -path <exclusions>`
3. **Find new files:** Files not in current catalog
4. **Find missing files:** Catalog entries whose paths no longer exist
5. **Check references:** Any new broken references?
6. **Generate diff report:**
   - New files needing classification
   - Missing files needing catalog cleanup
   - Modified files needing re-classification
   - New broken references
7. **Update catalog** with confirmed changes

---

## 9. Safety Principles

1. **Read before write. Always.** Phases 1-4 are information gathering. Phase 5 is action. Never mix them.
2. **Archive before delete. Always.** The `~/.lexi-archive/` is the safety net. No exceptions.
3. **Batch and confirm.** Never execute more than one batch of changes without user confirmation.
4. **Reference-aware moves.** A file move without updating all references is worse than not moving it.
5. **Excluded means invisible.** If a path is excluded, Lexi does not read it, classify it, recommend changes to it, or modify it. Period.
6. **When in doubt, flag for review.** A 🟡 Review classification that gets human input is always better than a 🔴 Orphaned classification that deletes something important.
7. **Respect "that's there on purpose."** If the user says a file belongs where it is, catalog it as intentional and don't re-flag it in future scans.
