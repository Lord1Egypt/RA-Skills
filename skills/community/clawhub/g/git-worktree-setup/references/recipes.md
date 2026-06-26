# Stack-Specific Recipes

Drop the relevant block(s) into the "Resource declarations" section of `setup-worktree.sh`. Helpers used: `link_resource`, `link_glob`, `copy_resource`, `hash_port` (defined in template).

---

## npm workspaces / pnpm / yarn (Node monorepo)

```bash
# Root hoisted deps + every workspace's local node_modules.
# CRITICAL: bundlers (vite/webpack/rollup) resolve from apps/web/, walking
# up one parent. Subpath exports (zod/v3, zod/v4) only exist in the workspace
# install — root may have a deduped older copy.
link_resource "node_modules"
link_glob    "apps/*/node_modules"
link_glob    "packages/*/node_modules"
link_glob    "libs/*/node_modules"   # if present

# pnpm: also link the content-addressed store metadata
# link_resource "node_modules/.pnpm"   # already inside node_modules above
```

If the team forbids sharing `node_modules` (rare; usually for native-binary deps that bake absolute paths), do `npm install` per-worktree instead — but accept the cost.

---

## Yarn Berry / PnP

```bash
link_resource ".yarn/cache"        # offline mirror — safe to share
link_resource ".yarn/unplugged"    # native deps unpacked here
link_resource ".pnp.cjs"           # generated; share or per-worktree both ok
link_resource ".pnp.loader.mjs"
copy_resource ".yarnrc.yml"        # per-worktree may diverge if you tweak
```

---

## Python — poetry / uv / pip-venv

```bash
# Share the resolved virtualenv (same machine, identical interpreter path).
link_resource ".venv"

# poetry: share lockfile resolution cache
link_resource ".cache/poetry"

# uv: share global cache (already in ~/.cache/uv, no per-repo state)

# Editable installs may bake worktree-absolute paths; verify after first
# `python -c "import yourpkg"` whether it resolves to main or worktree.
# If broken, re-run `pip install -e .` per-worktree.
```

---

## Cargo (Rust)

```bash
# target/ is per-build; sharing usually causes lock contention on debug builds.
# Share only the registry cache (rarely worth it — cargo handles that globally).
# Most Rust projects need: nothing here. Cold builds are the norm per worktree.

# If you really want to share build artifacts, set CARGO_TARGET_DIR globally
# instead of symlinking — sccache is also a saner solution.
```

---

## Go modules

```bash
# Go has a global module cache (~/go/pkg/mod) shared across all checkouts —
# nothing per-repo needs symlinking. vendor/ if present can be shared:
link_resource "vendor"
```

---

## Cloudflare Workers / Wrangler

```bash
# Local D1/R2/KV state — share so all worktrees see same dev data,
# OR per-worktree-copy if branches diverge schemas.
link_resource "apps/api/.wrangler/state"      # shared
# copy_resource "apps/api/.wrangler/state"     # isolated alternative

# Secrets (.dev.vars) MUST be copy not link — secrets per worktree may differ
copy_resource "apps/api/.dev.vars"
```

---

## Docker Compose

```bash
BRANCH=$(git -C "$CURRENT_DIR" branch --show-current)
PROJECT=$(clean_branch_name "$BRANCH")

# Per-worktree compose project name — avoids container/volume name collisions
upsert_env "$CURRENT_DIR/.env.local" COMPOSE_PROJECT_NAME "$PROJECT"

# CRITICAL: COMPOSE_PROJECT_NAME alone does NOT prevent host-port collisions.
# Two stacks both binding 0.0.0.0:5432 will fail with "address already in use".
# Solution: hash a host-port per service and reference it in compose.yml as
# ${POSTGRES_HOST_PORT:-5432}:5432, ${REDIS_HOST_PORT:-6379}:6379, etc.
upsert_env "$CURRENT_DIR/.env.local" POSTGRES_HOST_PORT "$(hash_port "${BRANCH}-pg")"
upsert_env "$CURRENT_DIR/.env.local" REDIS_HOST_PORT    "$(hash_port "${BRANCH}-redis")"

# If you share volumes intentionally (read warning under "Database" below):
# link_resource "docker/postgres-data"
```

---

## Per-worktree dev port (avoid collisions across parallel sessions)

```bash
BRANCH=$(git -C "$CURRENT_DIR" branch --show-current)
DEV_PORT=$(hash_port "$BRANCH")          # e.g. 4837 for branch "feat-auth"
API_PORT=$(hash_port "${BRANCH}-api")    # salt for second service

# WHICH .env file? Depends on the framework:
#   - Vite (apps/web)     → apps/web/.env.local           (reads VITE_PORT, PORT)
#   - Next.js (apps/web)  → apps/web/.env.local           (reads PORT)
#   - Compose vars        → root .env or .env.local       (interpolated by docker-compose)
#   - Bare Node script    → wherever your dev script reads
# Use upsert_env so re-running updates in place instead of duplicating lines.
upsert_env "$CURRENT_DIR/apps/web/.env.local" PORT     "$DEV_PORT"
upsert_env "$CURRENT_DIR/apps/web/.env.local" VITE_PORT "$DEV_PORT"
upsert_env "$CURRENT_DIR/apps/api/.env"       PORT     "$API_PORT"
```

---

## Database (Postgres / SQLite / Redis local data)

```bash
# Postgres dev volume — share by default for "agent sees same data" workflow.
#
# WARNING: Postgres assumes ONE postmaster per PGDATA. If you `docker compose up`
# in two worktrees concurrently, the second one's container will fail to start
# (postmaster.pid lock) OR — if the lock check is bypassed — corrupt WAL just
# like SQLite. Sharing pgdata is safe for SEQUENTIAL dev across worktrees but
# NOT for parallel `docker compose up`. For parallel dev, either copy_resource
# (each worktree gets its own pgdata) or use a single shared compose stack
# outside any worktree.
link_resource "docker/pgdata"

# SQLite — shared file means concurrent writes from two `dev` instances
# WILL corrupt the WAL. If parallel dev is plausible, COPY:
copy_resource "data/local.db"

# Redis dump — single-writer constraint identical to Postgres. Share for
# sequential, copy or use a single shared instance for parallel.
link_resource "data/redis-dump.rdb"
```

---

## Editor / IDE state (optional UX nicety)

```bash
# Open the worktree in your editor at the end of the script:
# (skip if already open to avoid focus-stealing)

# WebStorm
if pgrep -qf "WebStorm" && \
   osascript -e 'tell application "System Events" to get name of every window of (processes whose name contains "WebStorm")' 2>/dev/null \
   | grep -q "$(basename "$CURRENT_DIR")"; then
  : # already open
else
  open -a "WebStorm" "$CURRENT_DIR"
fi

# VS Code
# code "$CURRENT_DIR"

# Cursor
# cursor "$CURRENT_DIR"
```

---

## WorktreeCreate-hook variant (strict stdout)

If wired to `WorktreeCreate` instead of `SessionStart`, the script must:
1. Read JSON from stdin once into a variable.
2. Send all progress to `/dev/tty`, never stdout.
3. Print **only** the absolute worktree path on stdout at the end.
4. Suppress `git worktree add`'s own stdout (`>/dev/null 2>&1`).

```bash
#!/usr/bin/env bash
set -euo pipefail

INPUT=$(cat)                                            # stdin readable once
NAME=$(echo "$INPUT" | jq -r '.name')
REPO="${CLAUDE_PROJECT_DIR:?missing}"
WT="${REPO}/.claude/worktrees/${NAME}"
BRANCH="claude/${NAME}"

log() { echo "$*" > /dev/tty 2>/dev/null || true; }

log "Creating worktree on $BRANCH..."
mkdir -p "$(dirname "$WT")"
git worktree add -b "$BRANCH" "$WT" HEAD >/dev/null 2>&1

log "Bootstrapping resources..."
( cd "$WT" && bash "${REPO}/scripts/setup-worktree.sh" > /dev/tty 2>&1 ) || true

echo "$WT"   # ONLY the path on stdout
```

Pair with `worktree-remove.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
INPUT=$(cat)
WT=$(echo "$INPUT" | jq -r '.worktree_path')
[ -d "$WT" ] || exit 0

# Tear down docker stack first so containers release ports before we kill.
# Omit --volumes if pgdata etc was a SHARED symlink (don't nuke main repo's data).
( cd "$WT" && docker compose down 2>/dev/null ) || true

# Kill any dev server holding ports we generated for this worktree.
# Loops ALL hashed *_PORT keys, not just DEV_PORT.
if [ -f "$WT/.env.local" ]; then
  for port in $(grep -E '^[A-Z_]+_PORT=' "$WT/.env.local" | cut -d= -f2); do
    [ -n "$port" ] && lsof -ti :"$port" 2>/dev/null | xargs kill 2>/dev/null || true
  done
fi

BRANCH=$(git -C "$WT" branch --show-current 2>/dev/null || true)
git worktree remove "$WT" --force 2>/dev/null || true
[ -n "$BRANCH" ] && git branch -D "$BRANCH" 2>/dev/null || true
```
