#!/usr/bin/env bash
# review.sh — Deterministic PR code review with optional AI deepening.
# Emits JSON to stdout: {status, base, head, files_changed, findings:[...], summary}
# Never hard-depends on `gh`; falls back to git diff. Safe to run in any git repo.
set -uo pipefail

BASE="${1:-origin/main}"
HEAD="${2:-HEAD}"

emit_json() { jq -nc "$@"; }

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  emit_json --arg s "error" --arg m "not a git repository" \
    '{status:$s, summary:$m, findings:[]}'
  exit 2
fi

# Resolve base ref; fall back gracefully so review never aborts the pipeline.
if ! git rev-parse --verify --quiet "$BASE" >/dev/null; then
  for cand in origin/main origin/master main master HEAD~1; do
    if git rev-parse --verify --quiet "$cand" >/dev/null; then BASE="$cand"; break; fi
  done
fi

DIFF_RANGE="${BASE}...${HEAD}"
FILES=$(git diff --name-only "$DIFF_RANGE" 2>/dev/null)
[ -z "$FILES" ] && FILES=$(git diff --name-only "$BASE" "$HEAD" 2>/dev/null)
NUM_FILES=$(printf '%s\n' "$FILES" | grep -c . || true)

# --- Deterministic heuristic findings (no LLM required) ---
findings_file=$(mktemp)
add_finding() { # severity title detail
  jq -nc --arg sev "$1" --arg t "$2" --arg d "$3" \
    '{severity:$sev,title:$t,detail:$d}' >> "$findings_file"
}

DIFF=$(git diff "$DIFF_RANGE" 2>/dev/null || git diff "$BASE" "$HEAD" 2>/dev/null)

# Secret-ish patterns in added lines
ADDED=$(printf '%s\n' "$DIFF" | grep -E '^\+' | grep -vE '^\+\+\+')
if printf '%s\n' "$ADDED" | grep -qiE '(api[_-]?key|secret|password|token)\s*[:=]\s*["'\''][^"'\'' ]{8,}'; then
  add_finding "critical" "Possible hardcoded credential" "An added line looks like a hardcoded secret/API key. Move it to env/secret storage."
fi
if printf '%s\n' "$ADDED" | grep -qE '(TODO|FIXME|XXX)'; then
  add_finding "warning" "Unresolved TODO/FIXME in diff" "Added lines contain TODO/FIXME markers; confirm they are tracked."
fi
if printf '%s\n' "$ADDED" | grep -qiE 'console\.log|println!|System\.out\.print|fmt\.Println\(|print\('; then
  add_finding "suggestion" "Debug print statements" "Added lines include debug prints; consider a logger or removing before merge."
fi
if printf '%s\n' "$ADDED" | grep -qiE '(eval\(|exec\(|os\.system|subprocess\.[a-z]+\([^)]*shell=True)'; then
  add_finding "critical" "Dynamic code/shell execution" "Added lines use eval/exec/shell=True; validate inputs to avoid injection."
fi
LARGE=$(printf '%s\n' "$FILES" | while read -r f; do
  [ -f "$f" ] || continue
  n=$(git diff "$DIFF_RANGE" -- "$f" 2>/dev/null | grep -cE '^\+' || true)
  [ "${n:-0}" -gt 400 ] && echo "$f ($n added lines)"
done)
[ -n "$LARGE" ] && add_finding "warning" "Large file change" "Big diffs are hard to review: $(echo "$LARGE" | tr '\n' '; ')"

# --- Optional AI deepening if a coding agent is available (best-effort) ---
AI_NOTE=""
if [ "${PR_AUTOCHECK_AI:-1}" = "1" ] && [ -n "$DIFF" ]; then
  if command -v codex >/dev/null 2>&1; then AI_NOTE="codex available (set PR_AUTOCHECK_AI=0 to skip)"; fi
fi

FINDINGS_JSON=$(jq -sc '.' "$findings_file" 2>/dev/null || echo '[]')
rm -f "$findings_file"
CRIT=$(printf '%s' "$FINDINGS_JSON" | jq '[.[]|select(.severity=="critical")]|length')
WARN=$(printf '%s' "$FINDINGS_JSON" | jq '[.[]|select(.severity=="warning")]|length')

STATUS="ok"
[ "${WARN:-0}" -gt 0 ] && STATUS="warn"
[ "${CRIT:-0}" -gt 0 ] && STATUS="critical"

SUMMARY="$NUM_FILES file(s) changed; ${CRIT} critical, ${WARN} warning finding(s)"

emit_json \
  --arg s "$STATUS" --arg b "$BASE" --arg h "$HEAD" \
  --argjson nf "${NUM_FILES:-0}" --argjson f "$FINDINGS_JSON" \
  --arg sum "$SUMMARY" --arg ai "$AI_NOTE" \
  '{status:$s, base:$b, head:$h, files_changed:$nf, findings:$f, summary:$sum, ai_note:$ai}'
