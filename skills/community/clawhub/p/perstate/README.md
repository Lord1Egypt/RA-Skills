# Perstate — Permanent State for Your Agents and Yourself

> perstate = **per**sonality + **state**
>
> A git-native, knowledge-graph-based persistent state for personality and agents.

---

## Prerequisites

- **git** — all operations are based on git
- **SSH key** (recommended) — state contains private knowledge, SSH protocol is preferred
- **Standard shell environment** — `ls`, `grep`, `find`, `cat`, `mkdir`, `echo`, `rm`, `sed`

---

## Install

Install via skills CLI:

```bash
npx skills add graphwisdom/perstate
```

or install via ClawHub:

```bash
npm i -g clawhub
clawhub install fanzhidongyzby/perstate
```

Or manually clone:

```bash
git clone git@github.com:graphwisdom/perstate.git ~/.agents/skills/perstate
```

---

## Quick Start

```bash
# 1. Initialize (first time requires repo URL, default branch main)
/perstate init git@github.com:<user>/<repo>.git + main

# 2. bind personality / agent-memory to branch main
/perstate switch main

# 3. Check status (default, no side effects)
/perstate

# 4. Save knowledge (scan conversation context, auto-extract insights)
/perstate save [text]

# 5. Recall memory
/perstate search <keyword>

# 6. Visualize
/perstate view

# 7. Fork branch (copy current memory into a new one)
/perstate fork agent-a

# 8. Prune stale data (preview then confirm)
/perstate prune 30d
```

---

## Design Philosophy

1. **State identity = repo + branch** — one repo isolates multiple agents' states via branches. `main` is the personal default. No need for separate repos per agent — branch IS identity, naturally isolated, mergeable for knowledge exchange.
2. **File system IS the graph** — entities are directories, relations are files. `ls` is graph query, `grep` is full-text search, `find` is reverse traversal. No graph database, no index file, no JSON intermediate. One fact, one file — single source of truth.
3. **Knowledge processing, not simple storage** — writes are dedup, disambiguate, merge. Each write queries the existing graph first, decides create vs. merge, preventing knowledge fragmentation. This is the fundamental difference between perstate and diary-style memory.
4. **Git as temporal engine** — `valid_until` for soft delete, `git log --follow` for provenance, `git diff` for change review. Time dimension delegated to git, no separate version management.
5. **Zero-dependency, plug-and-play** — pure shell + git, no runtime, no daemon, no external tools. Any agent gets remote memory, knowledge backup, and recall on接入. All markdown + YAML frontmatter, human-readable, git-friendly.
6. **Open schema** — YAML frontmatter evolves additively, new fields never break old data. Ontology is documentation, not enforcement — unknown fields preserved, not rejected.
7. **Lazy loading** — graph → entity → relation type → relation. Read only what you need, no full-graph loading.

---

## Branch Isolation

One repo hosts multiple agents' persistent states, each on its own branch:

```
<repo>.git
├── branch: main         ← personal personality & knowledge
├── branch: agent-a      ← agent-a's state
├── branch: agent-b      ← agent-b's state
└── branch: agent-c      ← agent-c's state
```

Branches never interfere. Share knowledge via fork / merge / cherry-pick.

### Concurrency & Worktree

Each branch gets its own worktree, managed automatically by `perstate-prepare.sh` and `perstate-init.sh`:

- **Different branches**: true parallel, each worktree independent, zero conflict.
- **Same branch**: git refuses a second worktree on the same branch (`already checked out`), enforcing serialization. Agent B waits for Agent A to release.
- **Crash recovery**: `git worktree prune` cleans stale worktrees, scripts auto-detect on each run.

Worktree directory convention:

```
~/.perstate/
  <repo-name>.git/                  ← bare repo (git object store, multi-repo coexist)
  worktrees/
    <repo-name>/
      <branch>/                      ← worktree (long-lived, prune cleans expired)
```

- **Remote repo**: `git clone --bare` to `~/.perstate/<repo-name>.git/`, worktree at `~/.perstate/worktrees/<repo-name>/<branch>/`. Auto `git push` after write, auto `git pull` before read. SSH recommended.
- **Local repo**: same `git clone --bare` from local path, origin points to local directory. push/pull via filesystem, instant. Auto `git init` if not a git repo.

---

## Config

Config lives on the local machine (`~/.perstate/config.yml`), not in the knowledge repo.

```yaml
default_repo: git@github.com:<user>/<repo>.git
default_branch: main
sessions:
  abc123:
    branch: agent-a
```

| Field | Purpose |
|-------|---------|
| `default_repo` | Global default repo, set at install time |
| `default_branch` | Global default branch, defaults to `main`, changeable via init `--branch` |
| `sessions` | Per-session branch binding, auto-managed |

- Worktree path not stored — discovered by convention: `~/.perstate/worktrees/<repo-name>/<branch>/`
- Bare repo path: `~/.perstate/<repo-name>.git/` (multi-repo coexist, switching doesn't clean)
- No `agent-id` field — identity IS `branch` (repo fixed to default_repo)

### Agent State Binding

Configure agents to skip confirmation via system prompt:

```
perstate repo: <repo-url>       # Only when config doesn't exist, skip init confirmation
perstate branch: <branch-name>  # Only when session unbound, skip binding confirmation
```

> **Local config takes priority**: if config exists, `perstate repo:` is ignored. If session is bound, `perstate branch:` is ignored. System prompt only applies on first-time setup, never overrides existing config.

### Config Read

```bash
DEFAULT_REPO=$(grep "^default_repo:" ~/.perstate/config.yml | sed 's/^[^:]*: *//')
DEFAULT_BRANCH=$(grep "^default_branch:" ~/.perstate/config.yml | sed 's/^[^:]*: *//')
SESSION_BRANCH=$(grep -A1 "^  <session-id>:" ~/.perstate/config.yml | grep "branch:" | sed 's/^[^:]*: *//')
```

---

## Scripts

All scripts are in the skill's `scripts/` directory.

| Script | Purpose | Key parameters |
|--------|---------|----------------|
| `perstate-init.sh` | Initialize or update config: env check → config write → repo clone → worktree creation → initial structure → commit & push | `[--repo <url>]` `[--branch <branch>]` `[--yes]` (first time requires --repo) |
| `perstate-prepare.sh` | Pre-write prep: session binding lookup → worktree create/reuse → pull latest → write session binding. Sync cache skips redundant fetch/pull within window. | `--session-id <id>` `[--repo <url>]` `[--branch <branch>]` `[--read]` `[--no-sync]` `[--force-sync]` `[--sync-window <sec>]` |
| `perstate-commit.sh` | Post-write commit: git add -A + commit + push (rebase-retry on non-fast-forward, sync cache marked on success) | `--message "<summary>"` `--session-id <id>` |
| `perstate-info.sh` | Status check (`--status`) or memory statistics (default): config, session, entity count, relation count, recent commits | `--status` `[--session-id <id>]` |
| `perstate-view.sh` | Browser rendering: interactive HTML graph (vis-network), auto-open browser. awk-batch JSON extraction for large graphs. | `--session-id <id>` |
| `perstate-search.sh` | Fast keyword/reverse/multi-hop search: `--read` mode skips network sync, batch grep scan, reverse lookup, N-hop traversal. | `--session-id <id>` `<keyword>` `[--limit N]` `[--reverse X]` `[--hop N]` `[--valid-only]` |
| `perstate-fork.sh` | Fork new branch from current and rebind | `--name <new-branch>` `--session-id <id>` |
| `perstate-switch.sh` | Switch current session's bound branch (in-place config edit, calls prepare to sync worktree) | `--name <branch>` `--session-id <id>` |
| `perstate-prune.sh` | Clean expired session bindings, worktrees, invalid branches, and orphan content index (preview then confirm) | `[<days>d]` `[--session-id <id>]` `[--execute]` |

---

## Performance

Optimized for large knowledge graphs (benchmarked on 1000+ entities, 3000+ relations):

| Operation | 100 entities | 1000 entities | Target |
|-----------|-------------|---------------|--------|
| search    | 0.3s        | 1.1s          | 5.0s (100k entities) | < 10s  |
| save (local) | 0.3s     | 0.6s          | ~5m (bulk import¹)   | < 60s  |
| view      | 0.5s        | 2.4s          | —                   | —      |
| info      | 0.5s        | 3.3s          | 58s² (stats: <1s)   | —      |

¹ `git add -A` on 400k files is a git-level limitation; normal incremental saves (1-10 entities) are <1s.
² 58s is dominated by `du -sh .` on 1.7GB; entity/relation/valid/superseded stats via content index are <1s.

Key optimizations (no third-party deps, pure shell + git + awk):

- **Sync cache** (`~/.perstate/.sync/`): skips redundant `git fetch` + `git pull` within a time window (60s write / 300s read). A `save` immediately followed by `search` makes zero network round trips.
- **Redundant fetch elimination**: `git pull` fetches internally; the standalone `git fetch` before it was removed.
- **Conditional worktree prune**: only runs when the worktree is missing/invalid, not on every call.
- **awk-batch extraction**: `view.sh` and `info.sh` use single-pass `awk` instead of per-file `grep`/`sed`/`cat` forks. 2207-entity graph: 2m42s → 2.9s (**56x**).
- **Fast search script** (`perstate-search.sh`): `grep -RErIn` batch scan, `--read` mode, reverse lookup, N-hop traversal — all in one pass.
- **Content index** (`perstate-index.sh`): transient cache of all file contents. At 100k entities, search via index: ~120s → ~5s (**24x**). Auto-rebuilds on git HEAD change.
- **O(n) statistics**: `info.sh` valid/superseded counts use a single `awk` scan (FNR==1 boundary detection, BSD-awk compatible) instead of O(n²) nested `grep`. Index mode: instant counts via `grep -c` on index file.

---

## Testing & Benchmarks

```bash
# Correctness tests (14 assertions: search recall, reverse lookup, multi-hop, stats, JSON validity)
bash tests/test-correctness.sh

# Performance benchmarks (synthetic graphs at 100/1000/5000 scale)
bash tests/benchmark-perf.sh 100 1000

# Generate a synthetic graph at custom scale
bash tests/gen-synthetic-graph.sh /tmp/my-graph 5000
```

CI runs syntax checks, correctness tests, and performance benchmarks with target verification on every push/PR (`.github/workflows/ci.yml`).

---

The current design has natural extension points, no architecture change needed:

- **Open schema**: add entity types, relation types, frontmatter fields — write directly to `ontology.md`, no data migration
- **Extensible commands**: `/perstate` prefix system, `scripts/` directory can grow with new tools (e.g. `/perstate export`)
- **Standard storage**: git repo + markdown, any tool that reads git can consume the knowledge graph — graph visualization, full-text search, static site generation
- **Multi-agent collaboration**: branch isolation + fork copy + merge/cherry-pick sharing, no extra mechanism needed for inter-agent knowledge exchange

---

## Appendix: Shell Command Quick Reference

| Operation | Command |
|-----------|---------|
| List all entities | `ls entities/` |
| Entity detail | `cat entities/<id>/entity.md` |
| List out-relation types | `ls entities/<id>/` |
| List relations of a type | `ls entities/<id>/depends-on/` |
| Read a relation | `cat entities/<id>/depends-on/<to>.md` |
| Keyword search | `grep -rl "keyword" entities/` |
| Reverse lookup (→X) | `find entities/ -name "X.md"` |
| Recent changes | `ls -lt entities/<id>/` |
| Git history | `git log --follow entities/<id>/entity.md` |
| Valid relations only | `grep -rl "valid_until: null" entities/<id>/` |
| Create entity | `mkdir -p entities/<id>` + write entity.md |
| Create relation | `mkdir -p entities/<from>/<type>` + write `<to>.md` |
| Delete relation (hard) | `rm entities/<from>/<type>/<to>.md` |
| Delete entity | `rm -rf entities/<id>/` + `find entities/ -name "<id>.md" -delete` |
| Create worktree | `git worktree add <repo-dir>/<branch> <branch>` |
| Remove worktree | `git worktree remove <repo-dir>/<branch>` |
| Prune stale worktrees | `git worktree prune` |
| Commit & push | `scripts/perstate-commit.sh --message "..." --session-id <id>` |

---

## License

[Apache License 2.0](LICENSE)
