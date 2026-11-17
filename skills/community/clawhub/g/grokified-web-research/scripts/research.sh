#!/usr/bin/env bash
# Ask a Grok model a question with live web search, through the Grokified API.
# Usage: research.sh "question" [allowed-domain ...]
#   Up to 5 allowed domains limit the search to those sites (for example docs.example.com).
# Requires: curl, jq, and GROKIFIED_API_KEY in the environment.
# Optional: GROKIFIED_MODEL (default grok-4.7).
set -euo pipefail

BASE_URL="https://api.grokified.com/v1"
MODEL="${GROKIFIED_MODEL:-grok-4.7}"

die() {
  echo "research.sh: $*" >&2
  exit 1
}

[ -n "${GROKIFIED_API_KEY:-}" ] || die "GROKIFIED_API_KEY is not set. Create a key at https://grokified.com/login and export it."
command -v curl >/dev/null || die "curl is not installed."
command -v jq >/dev/null || die "jq is not installed."

[ $# -ge 1 ] || die 'usage: research.sh "question" [allowed-domain ...]'
QUESTION="$1"
shift
[ -n "$QUESTION" ] || die "the question is empty."
[ $# -le 5 ] || die "at most 5 allowed domains are supported."

# Domains are plain host names. Anything else is refused.
for d in "$@"; do
  case "$d" in
    '' | *[!A-Za-z0-9.-]*) die "'$d' is not a plain domain name." ;;
  esac
done

resp_file="$(mktemp)"
trap 'rm -f "$resp_file"' EXIT

read -r -d '' SYSTEM <<'EOF' || true
You are a careful research assistant. Use web search to answer the question.
Prefer primary sources such as official documentation, filings and original announcements.
State dates for time-sensitive facts. If sources disagree, say so and explain how.
Cite sources inline with links. Never invent a URL. If you could not find a reliable answer, say that plainly.
Format: a short answer first, then the key findings as bullet points, then one line giving your confidence and why.
EOF

http_code="$(
  jq -n --arg model "$MODEL" --arg system "$SYSTEM" --arg q "$QUESTION" \
    '$ARGS.positional as $d | {
       model: $model,
       input: [{role: "system", content: $system}, {role: "user", content: $q}],
       tools: [ if ($d | length) > 0
                then {type: "web_search", filters: {allowed_domains: $d}}
                else {type: "web_search"} end ]
     }' --args "$@" |
    curl -sS --max-time 240 -o "$resp_file" -w '%{http_code}' \
      -X POST "$BASE_URL/responses" \
      --config <(printf 'header = "Authorization: Bearer %s"\n' "$GROKIFIED_API_KEY") \
      -H "Content-Type: application/json" \
      --data-binary @-
)"

if [ "$http_code" != "200" ]; then
  echo "research.sh: Grokified returned HTTP $http_code" >&2
  jq -r '.error | "\(.message // "") (\(.code // "no code"))"' "$resp_file" >&2 2>/dev/null || true
  exit 1
fi

answer="$(jq -r '.output_text // ([.output[]? | select(.type == "message") | .content[]? | select(.type == "output_text") | .text] | join("\n")) // empty' "$resp_file")"
[ -n "$answer" ] || die "the response held no answer text."
printf '%s\n' "$answer"

sources="$(jq -r '(.citations // []) | map(if type == "object" then (.url // empty) else . end) | unique[]' "$resp_file" 2>/dev/null || true)"
if [ -n "$sources" ]; then
  printf '\nSources:\n'
  printf '%s\n' "$sources" | sed 's/^/- /'
fi
