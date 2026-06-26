#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <repo-name> [--private|--public]" >&2
  exit 1
fi

repo="$1"
visibility="${2:---private}"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh not found" >&2
  exit 1
fi

gh auth status >/dev/null 2>&1 || {
  echo "gh auth is not ready" >&2
  exit 1
}

if [ ! -d .git ]; then
  git init
fi

gh repo create "$repo" "$visibility" --source=. --remote=origin --push
