#!/usr/bin/env bash
set -euo pipefail

if ! command -v vercel >/dev/null 2>&1; then
  echo "vercel not found" >&2
  exit 1
fi

vercel whoami >/dev/null 2>&1 || {
  echo "vercel auth is not ready" >&2
  exit 1
}

exec vercel "$@"
