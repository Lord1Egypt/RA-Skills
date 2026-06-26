#!/usr/bin/env bash
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

extract_doc_tsv | awk -F '\t' '
function section(url, rest, parts, n) {
  sub(/^https:\/\/docs.openclaw.ai\//, "", url)
  rest = url
  sub(/\.md$/, "", rest)
  n = split(rest, parts, "/")
  if (n == 1) return "root"
  return parts[1]
}
{
  sec = section($2)
  docs[sec] = docs[sec] sprintf("- %s\n  %s\n", $1, $2)
  counts[sec]++
}
END {
  for (sec in counts) keys[++n] = sec
  asort(keys)
  for (i = 1; i <= n; i++) {
    sec = keys[i]
    printf "## %s (%d)\n%s\n", sec, counts[sec], docs[sec]
  }
}'
