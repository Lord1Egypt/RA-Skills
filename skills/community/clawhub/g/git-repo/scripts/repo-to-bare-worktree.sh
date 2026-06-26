#!/usr/bin/env bash
# repo-to-bare-worktree: convert an existing regular repo into a bare repo +
# register its working tree as a git worktree at a custom location, preserving
# uncommitted changes. Inverse of repo-to-ghq.sh.
#
# Usage:
#   repo-to-bare-worktree.sh --repo <repo-path> --worktree <target-path> [--name <wt-name>] [--force]
#
#   --repo      Existing regular repo (must contain a real .git directory)
#   --worktree  Target path for the working tree (e.g. ~/.agents/.claude/worktrees/skills)
#   --name      Worktree admin name under <bare>/worktrees/ (default: basename of --worktree)
#   --force     Skip the lock pre-check (NOT recommended)
#
# Result:
#   bare:     <repo>.git              (the moved .git, core.bare=true)
#   worktree: <target-path>           (working tree on its current branch, uncommitted changes intact)
#
# Why the lock pre-check (HARD STOP on Windows):
#   A Windows directory rename of <repo> fails with "Permission denied" while a
#   git GUI (SourceGit) or editor (VS Code) holds an open handle on <repo>/.git.
#   git commands still work (read/write index) — only the filesystem rename is
#   blocked. So we detect holders and abort with guidance instead of failing mid-move.

set -euo pipefail

REPO="" WT="" NAME="" FORCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --worktree) WT="$2"; shift 2 ;;
    --name) NAME="$2"; shift 2 ;;
    --force) FORCE=1; shift ;;
    *) echo "[to-bare] unknown arg: $1" >&2; exit 2 ;;
  esac
done

[ -n "$REPO" ] || { echo "[to-bare] --repo required" >&2; exit 2; }
[ -n "$WT" ]   || { echo "[to-bare] --worktree required" >&2; exit 2; }
[ -d "$REPO/.git" ] || { echo "[to-bare] $REPO has no regular .git directory (already bare/worktree?)" >&2; exit 1; }
[ -e "$WT" ] && { echo "[to-bare] target worktree path already exists: $WT" >&2; exit 1; }

BARE="$REPO.git"
[ -e "$BARE" ] && { echo "[to-bare] bare target already exists: $BARE" >&2; exit 1; }
NAME="${NAME:-$(basename "$WT")}"
BRANCH="$(git -C "$REPO" symbolic-ref --short HEAD 2>/dev/null || echo main)"

# --- Lock pre-check (Windows GUI/editor handle on .git blocks the rename) ---
if [ "$FORCE" != 1 ] && command -v powershell.exe >/dev/null 2>&1; then
  HOLDERS=$(powershell.exe -NoProfile -Command "
    (Get-Process SourceGit,Code,Cursor,Fork,GitKraken,TortoiseGitProc -ErrorAction SilentlyContinue |
      Select-Object -ExpandProperty ProcessName -Unique) -join ','
  " 2>/dev/null | tr -d '\r')
  if [ -n "$HOLDERS" ]; then
    echo "[to-bare] ABORT: a git GUI/editor is running and may hold a handle on $REPO/.git:" >&2
    echo "          $HOLDERS" >&2
    echo "          Close the app(s) with this repo open, then re-run. (override with --force)" >&2
    exit 3
  fi
fi

echo "[to-bare] repo=$REPO  branch=$BRANCH"
echo "[to-bare] bare=$BARE  worktree=$WT  name=$NAME"

# --- (b) move working tree (atomic rename — preserves uncommitted changes) ---
mv "$REPO" "$WT"

# --- (c) extract .git -> bare ---
mv "$WT/.git" "$BARE"

# --- (d) bare config ---
git -C "$BARE" config core.bare true
git -C "$BARE" config --unset core.worktree 2>/dev/null || true

# --- (e) metadata relink (Windows-form abs paths via cygpath -m) ---
to_win() { if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else echo "$1"; fi; }
BARE_W="$(to_win "$BARE")"
WT_W="$(to_win "$WT")"
mkdir -p "$BARE/worktrees/$NAME"
echo "ref: refs/heads/$BRANCH" > "$BARE/worktrees/$NAME/HEAD"
echo "../.."                   > "$BARE/worktrees/$NAME/commondir"
echo "$WT_W/.git"              > "$BARE/worktrees/$NAME/gitdir"
echo "gitdir: $BARE_W/worktrees/$NAME" > "$WT/.git"

# --- (f) rebuild the worktree index from HEAD ---
# Mixed-mode reset: working-tree files are preserved as-is. Any pre-conversion
# staged-but-uncommitted changes are unstaged (re-stage with `git add` after
# conversion if needed) — intentional, so the new worktree starts with a clean
# index aligned to HEAD instead of an index inherited from the pre-move repo.
git -C "$WT" reset HEAD -- . >/dev/null 2>&1 || true

# --- (g) verify ---
echo ""
echo "[to-bare] worktree list:"
git -C "$BARE" worktree list
echo ""
echo "[to-bare] working-tree status (uncommitted changes preserved):"
git -C "$WT" status --short
echo ""
echo "[to-bare] HEAD: $(git -C "$WT" log --oneline -1)"
echo "[to-bare] done. Remember to update SourceGit (old $REPO path is gone)."
