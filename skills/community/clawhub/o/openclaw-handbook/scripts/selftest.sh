#!/usr/bin/env bash
# Self-test: validate every doc path referenced in SKILL.md/EXAMPLES.md still
# resolves on docs.openclaw.ai.
# Run before publishing, or schedule in CI, to catch decision-tree rot.
# Exits non-zero if any path is STALE (3xx → 200, renamed) or MISSING (404/5xx).
#
# Paths are checked in parallel (default 8 workers, override with PARALLEL=N).
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
root="$here/.."
skill="$root/SKILL.md"
examples="$root/EXAMPLES.md"
parallel="${PARALLEL:-8}"
[ -f "$skill" ] || { echo "SKILL.md not found at $skill" >&2; exit 2; }

if [ -f "$examples" ]; then
  stripped=$(cat "$skill" "$examples" | sed 's/`//g')
else
  stripped=$(sed 's/`//g' "$skill")
fi
paths=$( \
  { printf '%s\n' "$stripped" | grep -oE '→ [a-zA-Z0-9/_.-]+\.(md|json)' | sed 's/^→ //'; \
    printf '%s\n' "$stripped" | grep -oE ', [a-zA-Z0-9_-]+/[a-zA-Z0-9/_.-]+\.(md|json)' | sed 's/^, //'; \
  } | sort -u | sed '/^$/d')

# Per-path probe. Emits one line: STATUS<TAB>path[<TAB>extra].
#   OK       — direct 200
#   STALE    — direct 3xx, follows to 200 (rename; tree should be updated)
#   MISSING  — anything else
probe() {
  local p="$1"
  local url="https://docs.openclaw.ai/${p}"
  local direct
  direct=$(curl -sI -o /dev/null -w '%{http_code}' "$url" 2>/dev/null || echo ERR)
  if [ "$direct" = "200" ]; then
    printf 'OK\t%s\n' "$p"
  elif [ "${direct:0:1}" = "3" ]; then
    local final_url final_code
    final_url=$(curl -sIL -o /dev/null -w '%{url_effective}' "$url" 2>/dev/null || echo "")
    final_code=$(curl -sIL -o /dev/null -w '%{http_code}' "$url" 2>/dev/null || echo ERR)
    if [ "$final_code" = "200" ]; then
      printf 'STALE\t%s\t%s → %s\n' "$p" "$direct" "${final_url##https://docs.openclaw.ai/}"
    else
      printf 'MISSING\t%s\t%s, redirect chain ends %s\n' "$p" "$direct" "$final_code"
    fi
  else
    printf 'MISSING\t%s\t%s\n' "$p" "$direct"
  fi
}
export -f probe

results=$(printf '%s\n' "$paths" | xargs -n1 -P "$parallel" -I{} bash -c 'probe "$@"' _ {})

total=$(printf '%s\n' "$results" | wc -l | tr -d ' ')
stale=$(printf '%s\n' "$results" | awk -F'\t' '$1=="STALE"' | wc -l | tr -d ' ')
missing=$(printf '%s\n' "$results" | awk -F'\t' '$1=="MISSING"' | wc -l | tr -d ' ')

printf '%s\n' "$results" | awk -F'\t' '
  $1=="STALE"   { printf "  STALE    %-50s (%s)\n", $2, $3 }
  $1=="MISSING" { printf "  MISSING  %-50s (%s)\n", $2, $3 }
'

printf '\nchecked:    %d\nstale:      %d (3xx renames — update decision tree)\nmissing:    %d (404/5xx — page gone)\n' \
  "$total" "$stale" "$missing"

# Smoke test: fetch.sh must round-trip non-.md paths (.json was a regression).
# Pick one representative non-.md path from the discovered list; if none, skip.
non_md=$(printf '%s\n' "$paths" | grep -v '\.md$' | head -1 || true)
fetch_failed=0
if [ -n "$non_md" ]; then
  if ! "$here/fetch.sh" "$non_md" >/dev/null 2>&1; then
    printf 'fetch:      FAIL  fetch.sh %s (non-.md path)\n' "$non_md"
    fetch_failed=1
  else
    printf 'fetch:      OK    fetch.sh %s\n' "$non_md"
  fi
fi

[ "$missing" -eq 0 ] && [ "$stale" -eq 0 ] && [ "$fetch_failed" -eq 0 ] || exit 1
