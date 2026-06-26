#!/usr/bin/env bash
set -euo pipefail

REPO_PATH="${1:-.}"

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: git is required" >&2
  exit 1
fi

if [ ! -d "$REPO_PATH/.git" ]; then
  echo "ERROR: not a git repository: $REPO_PATH" >&2
  exit 1
fi

echo "== Repo =="
echo "path: $(cd "$REPO_PATH" && pwd)"
echo

echo "== Remotes =="
git -C "$REPO_PATH" remote -v || true
echo

origin_url="$(git -C "$REPO_PATH" remote get-url origin 2>/dev/null || true)"
alias_host=""
if [ -n "$origin_url" ]; then
  case "$origin_url" in
    git@*:* )
      alias_host="$(printf '%s' "$origin_url" | sed -E 's#^git@([^:]+):.*#\1#')"
      ;;
    ssh://git@*/* )
      alias_host="$(printf '%s' "$origin_url" | sed -E 's#^ssh://git@([^/]+)/.*#\1#')"
      ;;
  esac
fi

echo "== SSH files =="
ls -la ~/.ssh 2>/dev/null || echo "~/.ssh not found"
echo

echo "== SSH permissions =="
stat -c '%a %U:%G %n' ~/.ssh ~/.ssh/* 2>/dev/null || true
echo

echo "== SSH config preview =="
sed -n '1,200p' ~/.ssh/config 2>/dev/null || echo "~/.ssh/config not found"
echo

if [ -n "$alias_host" ]; then
  echo "== Alias detected from origin =="
  echo "origin: $origin_url"
  echo "alias:  $alias_host"
  echo

  if command -v ssh >/dev/null 2>&1; then
    echo "== ssh -G summary =="
    ssh -G "$alias_host" 2>/dev/null | awk '
      $1=="user" || $1=="hostname" || $1=="identityfile" || $1=="identitiesonly" || $1=="port" {print}
    ' || true
    echo
  fi
else
  echo "== Alias detection =="
  echo "Could not infer an SSH alias from origin."
  echo "This may be an HTTPS remote, no origin, or a non-standard SSH URL."
  echo
fi

echo "== Read-only checks to run next =="
echo "git -C \"$REPO_PATH\" remote -v"
if [ -n "$alias_host" ]; then
  echo "ssh -T git@$alias_host"
fi
echo "git -C \"$REPO_PATH\" ls-remote origin"
