#!/usr/bin/env bash
# Verify every relative Markdown link in a tree resolves.
#
#   scripts/check_doc_links.sh [dir]     (default: repository root)
#
# Exists because the published package is assembled by excluding directories,
# and excluding a directory is exactly what turns a working link into a dead
# one. This repository shipped two dead references/ links to consumers before
# v0.1.4; the check runs in the publish workflow so that cannot recur silently.
set -euo pipefail

root="${1:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)}"
[[ -d "$root" ]] || { printf 'ERROR: not a directory: %s\n' "$root" >&2; exit 2; }

broken=0
checked=0

while IFS= read -r doc; do
  while IFS= read -r link; do
    # Skip absolute URLs, in-page anchors, and empty matches.
    case "$link" in ''|http://*|https://*|mailto:*|'#'*) continue ;; esac
    target="$(dirname "$doc")/${link%%#*}"
    checked=$((checked + 1))
    if [[ ! -e "$target" ]]; then
      printf 'BROKEN: %s -> %s\n' "${doc#"$root"/}" "$link" >&2
      broken=$((broken + 1))
    fi
  done < <(grep -oE '\]\([^)]+\)' "$doc" 2>/dev/null | sed 's/^](//; s/)$//')
done < <(find "$root" -name '*.md' -type f -not -path '*/.git/*')

if (( broken )); then
  printf 'FAIL: %d broken link(s) of %d checked in %s\n' "$broken" "$checked" "$root" >&2
  exit 1
fi
printf 'OK: %d relative link(s) resolve in %s\n' "$checked" "$root"
