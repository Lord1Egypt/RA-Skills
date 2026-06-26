#!/usr/bin/env bash
# Locate a local CHANGELOG.md shipped with the installed OpenClaw package.
#
# Strategy: ask the openclaw CLI for its install root via `which`, then
# walk up to the package root and check for CHANGELOG.md. Falls back to
# common install paths on macOS, Linux, and Windows-via-WSL.
#
# Output: prints the absolute path to the changelog on stdout if found.
#         Exits 0 on success, 1 if not found.

set -uo pipefail

candidates=()

# Resolve via the actual openclaw binary (works for npm/pnpm/yarn/global/local).
if command -v openclaw >/dev/null 2>&1; then
  bin="$(command -v openclaw)"
  # Resolve symlinks (`readlink -f` works on Linux; macOS needs `realpath`).
  if command -v realpath >/dev/null 2>&1; then
    bin="$(realpath "$bin" 2>/dev/null || echo "$bin")"
  elif command -v readlink >/dev/null 2>&1; then
    while [ -L "$bin" ]; do
      bin="$(readlink "$bin")"
    done
  fi
  # Walk up looking for package.json + CHANGELOG.md sibling.
  dir="$(dirname "$bin")"
  for _ in 1 2 3 4 5; do
    if [ -f "$dir/CHANGELOG.md" ] && [ -f "$dir/package.json" ]; then
      candidates+=("$dir/CHANGELOG.md")
      break
    fi
    parent="$(dirname "$dir")"
    [ "$parent" = "$dir" ] && break
    dir="$parent"
  done
fi

# Common install roots (npm / pnpm / volta / nvm / fnm / system).
candidates+=(
  # npm global
  "/opt/homebrew/lib/node_modules/openclaw/CHANGELOG.md"
  "/usr/local/lib/node_modules/openclaw/CHANGELOG.md"
  "/usr/lib/node_modules/openclaw/CHANGELOG.md"
  "$HOME/.local/lib/node_modules/openclaw/CHANGELOG.md"
  "$HOME/.npm-global/lib/node_modules/openclaw/CHANGELOG.md"
  # pnpm global (mac + linux)
  "$HOME/Library/pnpm/global/5/node_modules/openclaw/CHANGELOG.md"
  "$HOME/.local/share/pnpm/global/5/node_modules/openclaw/CHANGELOG.md"
  # volta
  "$HOME/.volta/tools/image/packages/openclaw/lib/node_modules/openclaw/CHANGELOG.md"
)

# pnpm / volta / nvm / fnm: glob-resolve since the version segment varies.
if command -v compgen >/dev/null 2>&1 || true; then
  for pat in \
    "$HOME/Library/pnpm/global/"*"/node_modules/openclaw/CHANGELOG.md" \
    "$HOME/.local/share/pnpm/global/"*"/node_modules/openclaw/CHANGELOG.md" \
    "$HOME/.nvm/versions/node/"*"/lib/node_modules/openclaw/CHANGELOG.md" \
    "$HOME/.fnm/node-versions/"*"/installation/lib/node_modules/openclaw/CHANGELOG.md" \
    "/root/.nvm/versions/node/"*"/lib/node_modules/openclaw/CHANGELOG.md" ; do
    # Expand the glob; skip the literal pattern if nothing matched.
    for resolved in $pat; do
      [ -f "$resolved" ] && candidates+=("$resolved")
    done
  done
fi

for c in "${candidates[@]}"; do
  if [ -f "$c" ]; then
    echo "$c"
    exit 0
  fi
done

exit 1
