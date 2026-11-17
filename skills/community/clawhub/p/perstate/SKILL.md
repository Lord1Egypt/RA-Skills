---
name: perstate
description: >-
  A git-native remote knowledge graph that provides persistent state for agents and individuals.
  /perstate checks status, /perstate save writes insights, /perstate search recalls, /perstate fork copies branches, /perstate switch changes branches, /perstate info shows stats, /perstate view visualizes, /perstate prune cleans up.
  Trigger: user says "persist" "remember" "recall" "memory" "save insight" or types /perstate.
  Auto-extracts insights, deduplicates and merges, multi-hop queries, graph visualization.
---

## Commands

All operations use the `/perstate` prefix. Scripts are in the skill's `scripts/` directory.

> Agent receives skill content + args, maps args to the corresponding command below.

| Command | Purpose | Script |
|---------|---------|--------|
| `/perstate` | Status check (no side effects, shows config completeness and session binding, guides init) | `scripts/perstate-info.sh --status --session-id <id>` |
| `/perstate init` | Initialize config (Agent guides user to provide repo URL and branch name) | `scripts/perstate-init.sh [--repo <url>] [--branch <branch>]` |
| `/perstate save [content]` | Write memory (scan context or write specified content. Create/update/delete determined by Agent from semantics) | `scripts/perstate-prepare.sh --session-id <id>` → knowledge processing → `scripts/perstate-commit.sh --session-id <id>` |
| `/perstate search <keyword>` | Recall memory (single-point, multi-hop, subgraph, natural language) | `scripts/perstate-search.sh --session-id <id> <keyword>` (fast path: `--read` mode skips sync, grep -RErIn batch scan) |
| `/perstate info` | Memory statistics (entity count, relation count, recent commits) | `scripts/perstate-info.sh --session-id <id>` |
| `/perstate view` | Render memory graph in browser | `scripts/perstate-view.sh --session-id <id>` |
| `/perstate fork <name>` | Fork new branch from current and rebind | `scripts/perstate-fork.sh --name <name> --session-id <id>` |
| `/perstate switch <branch>` | Switch current session's bound branch | `scripts/perstate-switch.sh --name <branch> --session-id <id>` |
| `/perstate prune [Nd]` | Clean expired session bindings, worktrees, and invalid branches (preview then confirm) | `scripts/perstate-prune.sh <days>d [--session-id <id>] [--execute]` |

> Agent must always pass `--session-id <id>` when calling scripts, **do not use `--worktree` to bypass session binding**. Unbound sessions must go through the session binding flow first. Session ID source: CC uses session UUID, Kimi Code uses session path ID, other platforms use session identifier or `date +%s`. Do not use `$$` or `basename "$PWD"`.

---

## Initialization (`/perstate init`)

Flow when user runs `/perstate init`:

1. **Agent collects repo + branch** (cannot skip):
   - If config exists → read `default_repo` and `default_branch`, use structured interaction to confirm or modify
   - If config doesn't exist → use AskUserQuestion (one call, two questions):
     - **Repo address**: options SSH remote (recommended) / local path / HTTPS remote (not recommended) + Other for custom input
     - **Branch name**: options `main` (default) / custom + Other for custom input
2. **Agent executes script** (pass `--yes` to skip script's interactive confirmation, since Agent already confirmed in step 1):
   ```bash
   scripts/perstate-init.sh --repo <url> --branch <branch> --yes
   ```
3. Script auto-completes: check git → check repo protocol (non-SSH gives security warning) → write config → clone repo → create worktree → create initial structure → commit & push

> **Remote vs Local** (unified architecture):
> - bare clone to `~/.perstate/<repo-name>.git/`, worktree at `~/.perstate/worktrees/<repo-name>/<branch>/`
> - **Remote git URL** (`git@...` recommended / `https://...`): push/pull over network
> - **Local path**: push/pull over filesystem (instant). Auto `git init` if not a git repo
> - Multi-repo coexist, switching doesn't clean old repos (local cache)

---

## Session Binding (entry point for `save`/`search`/`info`/`view`/`fork`/`switch`)

**Before executing `/perstate save`, `/perstate search`, `/perstate info`, `/perstate view`, `/perstate fork`, `/perstate switch`, go through the session binding flow to determine branch.**

> `/perstate` (no args, status check) and `/perstate prune` don't need session binding.

### Scenario 1: First install (config doesn't exist)

Check if system prompt specifies `perstate repo: <url>`:
- **Specified** → run `scripts/perstate-init.sh --repo <url> --branch <perstate branch or main> --yes`, continue with original command after init
- **Not specified** → collect repo+branch in current interaction (same as "Initialization" step 1), run init, continue with original command

### Scenario 2: First binding (config exists, session unbound)

Check if system prompt specifies branch (see scenario 3). If not → use structured interaction to confirm:
"Default is personal memory (`<default_branch>` branch). Confirm? Or enter a new branch name:"
- Confirm → bind `default_branch`; enter new name → bind that branch (auto-create if doesn't exist)

Write to config:
```bash
grep -q "^sessions:" ~/.perstate/config.yml || echo "sessions:" >> ~/.perstate/config.yml
cat >> ~/.perstate/config.yml << EOF
  <session-id>:
    branch: <branch>
EOF
```

### Scenario 3: System prompt specified (no confirmation needed)

System prompt can contain:
```
perstate repo: <repo-url>       # Only when config doesn't exist, skip init confirmation
perstate branch: <branch-name>  # Only when session unbound, skip binding confirmation
```
> **Local config takes priority**: if config exists, `perstate repo:` is ignored. If session bound, `perstate branch:` is ignored. System prompt only applies on first-time setup, never overrides existing config.

### Scenario 4: Already bound

Session has binding → **use directly**, no prompt:
```bash
grep -q "^  <session-id>:" ~/.perstate/config.yml && echo "bound" || echo "unbound"
SESSION_BRANCH=$(grep -A1 "^  <session-id>:" ~/.perstate/config.yml | grep "branch:" | sed 's/^[^:]*: *//')
```

### After all scenarios: prepare worktree + sync

Once branch is determined:
- **save/search**: Agent manually runs prepare → `cd "$(scripts/perstate-prepare.sh --session-id <id>)"`
- **info/view/fork/switch**: scripts internally call prepare.sh, just call the script directly
- **search (fast path)**: `scripts/perstate-search.sh --session-id <id> <keyword>` — internally calls prepare with `--read` mode, uses grep batch scan + reverse/multi-hop traversal

`perstate-prepare.sh` auto-completes: worktree create/reuse + `git fetch origin` + `git pull --ff-only`, ensuring local branch is in sync with remote.

> **Sync cache (performance)**: `prepare.sh` caches the last sync timestamp per `<repo>__<branch>` in `~/.perstate/.sync/`. Within the cache window (60s for writes, 300s for reads), `git fetch` + `git pull` are skipped entirely — a single `save` followed by `search` makes zero network round trips. Flags: `--read` (read mode, longer window), `--no-sync` (skip network entirely), `--force-sync` (ignore cache), `--sync-window <sec>` (custom window).

> **Content index (large-scale search)**: `perstate-index.sh` builds a transient content index at `~/.perstate/.index/<repo>__<branch>.content` — all entity/relation file contents concatenated into a single stream. `search` and `info` use this index when fresh (auto-detected via git HEAD) instead of scanning 400k+ files with `grep -r`. At 100k entities / 300k relations: search drops from ~120s (`grep -r`) to ~5s (index awk scan), a 24x improvement. The index is a transient cache, not the knowledge graph data source — falls back to `grep -r` only if rebuild fails. **Auto-refresh**: `search`/`info` rebuild the index automatically when absent or stale (HEAD mismatch) — users never need to maintain it manually. Rebuild explicitly with `scripts/perstate-index.sh --worktree <path> --rebuild`.

---

## Repository Structure

```
entities/
  <entity-id>/
    entity.md                   # Entity metadata + free-form knowledge
    <relation-type>/            # Out-relation directory (e.g. depends-on/, enables/)
      <target-id>.md            # One relation: this entity --type--> target
schema/
  ontology.md                   # Entity types, relation types definition
```

File system IS the index: `ls entities/` lists all entities, `ls entities/<id>/` lists out-relation types.

### entity-id naming convention

kebab-case, English preferred (e.g. `llm-evaluation`), must be valid as directory/file name.

---

## File Formats

### entity.md

```markdown
---
id: llm-evaluation
label: LLM Evaluation
type: domain
aliases: [LLM evaluation, model benchmarking]
created_at: 2026-07-14
updated_at: 2026-07-15
sources: ["arxiv:2505.20416", "github:user/repo"]
---

## Overview

LLM evaluation is the systematic measurement of LLM capabilities...

## Key Insights

(Knowledge about this entity itself, not about specific relations)

## Sources

- arxiv:2505.20416 — paper PDF (§4 Method, §5.3 Scaling)
- github:user/repo — README + source code (background_review.py#L1-L25)
```

### relation file (`entities/<from>/<type>/<to>.md`)

```markdown
---
from: llm-evaluation
to: harness
type: depends-on
created_at: 2026-07-14
updated_at: 2026-07-15
valid_until: null
sources: ["arxiv:2505.20416 §4", "chat:2026-07-14"]
---

## Insight

LLM evaluation fundamentally depends on harness's engineering capabilities...
```

### Temporal fields

| Field | Meaning |
|-------|---------|
| `created_at` | First recorded date |
| `updated_at` | Last modified date |
| `valid_until` | `null` = still valid; a date = superseded (soft delete) |
| git history | Full provenance (`git log --follow <file>`) |

---

## Write Flow (`/perstate save`)

### 1. Extract entities and relations

From conversation insights (or user-specified info), identify:
- **Entities** (concepts, domains, technologies)
- **Relations** (depends-on, enables, contradicts, etc.)
- **Relation content** (the crystallized insight on each relation)

### 2. Dedup, disambiguate, merge

For each entity:
```bash
ls entities/ | grep -i "<entity-id>"           # by id
grep -rl "label:.*<label>" entities/            # by label
grep -rl "<alias>" entities/*/entity.md          # by alias
```
- No match → create new; one match → merge (update frontmatter, append body); multiple matches → disambiguate using context

For each relation:
```bash
ls entities/<from>/<type>/ | grep "<target>"
```
- No match → create new; match → merge (append insight)

### 3. Write files

Follow templates in "File Formats" section, replacing `<placeholders>` with actual values.

**Create entity:** `mkdir -p entities/<id>` → write entity.md from template

**Merge entity:** read existing → update frontmatter `updated_at` + `aliases` union + `sources` append → append `###` subsection (with date) → use Edit tool

**Create relation:** `mkdir -p entities/<from>/<type>` → write `<to>.md` from template

**Merge relation:** read existing → update frontmatter `updated_at` + `sources` append → append `###` subsection → use Edit tool

**Delete:** locate target → soft delete (set `valid_until`) or hard delete (`rm` + clean empty dirs)

### 4. Commit

```bash
scripts/perstate-commit.sh --message "perstate: <summary>" --session-id <session-id>
```

**All steps must complete synchronously within one turn. Never split prepare and commit across turns.**

---

## Query Patterns (`/perstate search`)

> Prefer the dedicated `scripts/perstate-search.sh` for fast keyword/reverse/multi-hop queries. It uses `--read` mode (skips network sync) and batch `grep -RErIn` scan. For ad-hoc shell queries, prepare the worktree first then use the commands below.

**Basic queries:**
```bash
cat entities/<id>/entity.md                    # single entity
ls entities/                                     # full overview
ls entities/<id>/                                # list out-relation types
ls entities/<id>/depends-on/                    # specific relation type
cat entities/<id>/depends-on/<target>.md         # read one relation
grep -rl "keyword" entities/ | head -5             # keyword search
```

**Advanced queries:**
```bash
# Multi-hop traversal
FIRST_HOP=$(ls entities/X/depends-on/ | sed 's/\.md$//')
for target in $FIRST_HOP; do echo "=== $target ==="; ls entities/$target/depends-on/ 2>/dev/null; done

# Reverse lookup (who points to X?)
find entities/ -name "X.md" -type f
grep -rl "to: X" entities/

# Temporal query
ls -lt entities/X/depends-on/
git log --oneline -10

# Subgraph extraction (2-hop)
find entities/X/ -name "*.md" -not -name "entity.md"
find entities/ -path "*/X.md"

# Valid relations only
grep -rl "valid_until: null" entities/X/depends-on/
```

**Natural language query**: extract keywords → `grep -rl` to locate → read matching files → synthesize summary
**Result aggregation**: after multi-hop/multi-file queries → merge → dedup → sort by relevance or time → summarize

---

## Additional Commands

**info**: outputs repo, branch, path, size, entity count, relation count (valid/superseded/undeclared), recent commits. Script internally calls prepare.sh.

**view**: generates interactive HTML graph (vis-network), auto-opens browser. Nodes colored by entity type, edges labeled with relation type. Script internally calls prepare.sh.

**fork `<name>`**: forks new branch from current and rebinds. Script auto-completes: read current binding → create new branch → create worktree → update session binding → push to remote. After fork, subsequent writes go to the new branch; original branch memory is fully preserved.

**switch `<branch>`**: switches to an **existing** branch (vs fork: fork copies into a new branch, switch changes to an existing one). Script auto-completes: validate branch exists → in-place rewrite config binding → call prepare to create worktree and pull. Common usage: after fork experiment, `/perstate switch main` to go back.

**prune `[Nd]`**: two-step flow (preview → confirm → execute, see command table). Cleans: expired session bindings (worktree mtime > N days), expired worktrees (first `git worktree prune`, then remove), invalid branches (local exists but remote deleted, `git branch -d` safe delete), orphan content index (index files whose branch no longer exists in the bare repo).

---

## Trigger Timing

### When to search (recall)
- Before answering a question that might relate to accumulated knowledge
- At conversation start if the topic is within the agent's expertise domains
- When user says "recall" / "remember" / "memory" / "before" / "you mentioned earlier"

### When to save (persist)
- After producing high-dimensional insights (high-dimensional = non-trivial analysis, pattern recognition, causal reasoning, experience synthesis; NOT data statistics or fact listing)
- When user says "persist" / "remember" / "save" / "save insight"
- Do NOT trigger: on every message, on conversations without substantive insight, on pure execution tasks
