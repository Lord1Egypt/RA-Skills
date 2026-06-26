#!/usr/bin/env bash
# Full-text search across all OpenClaw docs (case-insensitive, literal keyword).
# Usage: search.sh <keyword> [context-lines]
# Caches llms-full.txt for 1 hour at $TMPDIR/openclaw-llms-full.txt to avoid
# re-downloading on every call in a session (file is ~1MB+).
# Returns matching sections with surrounding context, capped at 200 lines.
# Keyword is matched as a fixed string (grep -F), so regex metacharacters and
# weird chars like '+', '?', '|', '{' are safe.
set -euo pipefail
[ $# -lt 1 ] && { echo "usage: $0 <keyword> [context-lines]" >&2; exit 2; }
kw="$1"
ctx="${2:-10}"
cache="${TMPDIR:-/tmp}/openclaw-llms-full.txt"
max_age=3600  # seconds

# Refresh cache if missing or older than max_age.
needs_fetch=1
if [ -f "$cache" ]; then
  if mtime=$(stat -f %m "$cache" 2>/dev/null || stat -c %Y "$cache" 2>/dev/null); then
    age=$(( $(date +%s) - mtime ))
    [ "$age" -lt "$max_age" ] && needs_fetch=0
  fi
fi
if [ "$needs_fetch" -eq 1 ]; then
  curl -sfL https://docs.openclaw.ai/llms-full.txt > "$cache.tmp"
  mv "$cache.tmp" "$cache"
fi

# Tolerate the expected exits: 0=match, 1=no-match, 141=SIGPIPE when head -200
# closes the pipe early. Any other grep error (e.g. unreadable cache) propagates.
set +e
grep -iF -A "$ctx" -B 2 -- "$kw" "$cache" | head -200
rc=$?
set -e
case $rc in 0|1|141) ;; *) exit "$rc" ;; esac
