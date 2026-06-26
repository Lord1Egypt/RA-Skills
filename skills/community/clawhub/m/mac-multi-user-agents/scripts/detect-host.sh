#!/usr/bin/env bash
set -euo pipefail

export PATH=/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

echo "=== host ==="
hostname
sw_vers
echo
echo "=== fast user switching ==="
defaults read /Library/Preferences/.GlobalPreferences MultipleSessionEnabled 2>/dev/null || echo "not set"
echo
echo "=== shared toolchain ==="
for bin in brew node npm openclaw; do
  if command -v "$bin" >/dev/null 2>&1; then
    printf "%-10s %s\n" "$bin" "$(command -v "$bin")"
  else
    printf "%-10s %s\n" "$bin" "missing"
  fi
done
echo
echo "=== local users ==="
dscl . list /Users | egrep '^(agent[0-9]+|[A-Za-z].*)$' | sort
