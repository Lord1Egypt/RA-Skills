#!/usr/bin/env bash
# Find OpenClaw doc pages matching a keyword (case-insensitive, literal).
# Usage: find.sh <keyword>
# Matches on either the page TITLE or the URL PATH so terms that live only in
# the slug (e.g. "qmd", "honcho") are still discoverable.
# Keyword is matched as a fixed string (grep -F), so regex metacharacters and
# weird chars like '+', '?', '|', '{' are safe.
# Output: one match per line, format "Title<TAB>path.md"
set -euo pipefail
[ $# -lt 1 ] && { echo "usage: $0 <keyword>" >&2; exit 2; }
kw="$1"
curl -sfL https://docs.openclaw.ai/llms.txt \
  | sed -nE 's|^- \[(.*)\]\(https://docs\.openclaw\.ai/(.*)\)$|\1\t\2|p' \
  | grep -iF -- "$kw" || true
