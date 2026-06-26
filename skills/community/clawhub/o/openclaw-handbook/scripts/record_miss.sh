#!/usr/bin/env bash
# Record a routing miss (or tally recorded misses) for synonym-map promotion.
#
# Record mode:
#   record_miss.sh "<user question>" "<path you ended up fetching>"
#   Appends one line to ~/.openclaw/openclaw-docs/misses.md.
#
# Tally mode:
#   record_miss.sh --tally [N]
#   Groups recorded misses by fetched path and shows counts (top N, default 20).
#   Use this to spot which paths cleared the "3 comparable hits" promotion bar
#   defined in the Evolution Loop section of SKILL.md.
#
# Never auto-edits SKILL.md. Promotion to the Synonym Map is a human decision.
set -eu

dir="$HOME/.openclaw/openclaw-docs"
log="$dir/misses.md"

if [ "${1:-}" = "--tally" ]; then
  top="${2:-20}"
  [ -f "$log" ] || { echo "no misses logged at $log" >&2; exit 0; }
  printf 'count  path\n'
  printf -- '-----  ----\n'
  # Only consider lines starting with an ISO-8601 UTC timestamp (real log rows,
  # not header text). Split on " | " and take field 3 (the path).
  awk -F' \\| ' '/^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z / && NF==3 { print $3 }' "$log" \
    | sort | uniq -c | sort -rn | head -"$top" \
    | awk '{ count=$1; $1=""; sub(/^ +/, ""); printf "%5d  %s\n", count, $0 }'
  exit 0
fi

[ $# -lt 2 ] && {
  cat >&2 <<'USAGE'
usage:
  record_miss.sh "<question>" "<path>"   # record a miss
  record_miss.sh --tally [N]             # summarize top N paths (default 20)
USAGE
  exit 2
}

q="$1"
path="$2"
mkdir -p "$dir"
if [ ! -f "$log" ]; then
  printf '# Routing misses\n\nOne line per miss: timestamp | question | fetched path.\nPromote to SKILL.md Synonym Map only after 3 comparable hits.\nRun `record_miss.sh --tally` to see counts.\n\n' > "$log"
fi
ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
# Flatten newlines in the question so each miss stays on one line.
q_one=$(printf '%s' "$q" | tr '\n' ' ')
printf '%s | %s | %s\n' "$ts" "$q_one" "$path" >> "$log"
printf 'recorded: %s\n' "$log"
