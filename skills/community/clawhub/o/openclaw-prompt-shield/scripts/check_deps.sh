#!/usr/bin/env bash
# Verify dependencies for openclaw-prompt-shield.
# Exits 0 if all are available, 1 if any are missing.

set -u

missing=0

if command -v python3 >/dev/null 2>&1; then
  printf "  ok   %-9s %s\n" "python3" "$(python3 --version 2>&1)"
else
  printf "  miss %-9s not found in PATH\n" "python3"
  missing=1
fi

# Verify standard library only (no third-party deps required)
if python3 -c "import re, json, base64, argparse, pathlib, sys" >/dev/null 2>&1; then
  printf "  ok   %-9s standard library OK\n" "stdlib"
else
  printf "  miss %-9s standard library check failed\n" "stdlib"
  missing=1
fi

if [ "$missing" -eq 1 ]; then
  echo
  echo "Dependencies missing. Install python3 via your package manager." >&2
  exit 1
fi

echo
echo "All dependencies satisfied."
exit 0
