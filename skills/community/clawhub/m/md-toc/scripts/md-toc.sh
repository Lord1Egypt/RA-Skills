#!/usr/bin/env bash
# md-toc: extract a table of contents from an ATX-markdown file.
set -euo pipefail

usage() {
  echo "usage: md-toc.sh FILE [--max N]" >&2
  exit 2
}

[ $# -ge 1 ] || usage
file="$1"; shift
max=6
while [ $# -gt 0 ]; do
  case "$1" in
    --max) max="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) usage ;;
  esac
done
[ -f "$file" ] || { echo "md-toc: no such file: $file" >&2; exit 1; }

awk -v max="$max" '
BEGIN { in_code = 0 }
/^```/ { in_code = !in_code; next }
in_code { next }
/^#+ / {
  # count leading hashes
  n = 0
  rest = $0
  while (substr(rest, 1, 1) == "#") { n++; rest = substr(rest, 2) }
  if (n > max) next
  # strip leading hashes + whitespace to get title
  title = $0
  sub(/^#+[[:space:]]+/, "", title)
  gsub(/[[:space:]]+$/, "", title)
  # build github-style anchor
  anchor = tolower(title)
  gsub(/[^a-z0-9 -]/, "", anchor)
  gsub(/[[:space:]]+/, "-", anchor)
  pad = ""
  for (i = 1; i < n; i++) pad = pad "  "
  printf "%s- [%s](#%s)\n", pad, title, anchor
}
' "$file"
