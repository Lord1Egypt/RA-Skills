#!/usr/bin/env bash
set -euo pipefail

if [[ $# -eq 0 ]]; then
  set -- pipe -s 1
fi

if command -v zsh >/dev/null 2>&1; then
  quoted=""
  for arg in "$@"; do
    quoted+=" $(printf '%q' "$arg")"
  done
  exec zsh -lic "macmon${quoted}"
fi

if [[ -x /opt/homebrew/bin/macmon ]]; then
  exec /opt/homebrew/bin/macmon "$@"
fi

exec macmon "$@"
