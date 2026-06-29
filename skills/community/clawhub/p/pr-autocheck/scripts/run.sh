#!/usr/bin/env bash
# run.sh — Orchestrate PR autocheck: code review -> service health -> Discord sync.
# Produces a combined JSON report (stdout + reports/) and posts it to Discord.
#
# Usage:
#   run.sh [--base REF] [--head REF] [--repo NAME] [--pr LABEL]
# Env:
#   DISCORD_WEBHOOK_URL   Discord webhook for delivery (else payload is saved)
#   HEALTHCHECK_CMD       Override health command (default: skill healthcheck.sh --json)
#   PR_AUTOCHECK_AI       1 (default) allow optional AI deepening, 0 to skip
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="origin/main"; HEAD="HEAD"; REPO="$(basename "$(pwd)")"; PR="local"

while [ $# -gt 0 ]; do
  case "$1" in
    --base) BASE="$2"; shift 2;;
    --head) HEAD="$2"; shift 2;;
    --repo) REPO="$2"; shift 2;;
    --pr) PR="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; shift;;
  esac
done

mkdir -p reports

# 1) Code review
REVIEW=$(bash "$HERE/review.sh" "$BASE" "$HEAD" 2>/dev/null)
[ -z "$REVIEW" ] && REVIEW='{"status":"error","summary":"review produced no output","findings":[]}'

# 2) Service health (reuse healthcheck skill if present)
HC_DEFAULT="$HOME/.openclaw/workspace/skills/healthcheck/healthcheck.sh"
HEALTH_CMD="${HEALTHCHECK_CMD:-}"
if [ -z "$HEALTH_CMD" ] && [ -f "$HC_DEFAULT" ]; then HEALTH_CMD="bash $HC_DEFAULT --json"; fi
HEALTH_RAW=""; HEALTH_OK=0
if [ -n "$HEALTH_CMD" ]; then
  HEALTH_RAW=$($HEALTH_CMD 2>/dev/null)
  if [ -n "$HEALTH_RAW" ] && printf '%s' "$HEALTH_RAW" | jq -e 'type=="object"' >/dev/null 2>&1; then
    HEALTH_OK=1
  fi
fi
if [ "$HEALTH_OK" = "1" ]; then
  HSEV=$(printf '%s' "$HEALTH_RAW" | jq -r '.max_severity // 0')
  case "$HSEV" in 0) HSTAT=ok;; 1) HSTAT=warn;; *) HSTAT=critical;; esac
  HCOUNT=$(printf '%s' "$HEALTH_RAW" | jq -r '(.checks // {}) | length')
  HEALTH=$(jq -nc --arg s "$HSTAT" --arg sum "$HCOUNT service(s) checked (max_severity $HSEV)" \
    --argjson raw "$HEALTH_RAW" '{status:$s, summary:$sum, raw:$raw}')
else
  HEALTH='{"status":"unknown","summary":"healthcheck unavailable in this environment","raw":null}'
fi

# 3) Combine + overall severity
RSTAT=$(printf '%s' "$REVIEW" | jq -r '.status // "unknown"')
HSTAT=$(printf '%s' "$HEALTH" | jq -r '.status // "unknown"')
rank() { case "$1" in critical|error) echo 3;; warn) echo 2;; ok) echo 1;; *) echo 0;; esac; }
OVERALL=ok
[ "$(rank "$RSTAT")" -ge 2 ] || [ "$(rank "$HSTAT")" -ge 2 ] && OVERALL=warn
[ "$(rank "$RSTAT")" -ge 3 ] || [ "$(rank "$HSTAT")" -ge 3 ] && OVERALL=critical

REPORT=$(jq -nc \
  --arg repo "$REPO" --arg pr "$PR" --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg overall "$OVERALL" --argjson review "$REVIEW" --argjson health "$HEALTH" \
  '{repo:$repo, pr:$pr, timestamp:$ts, overall:$overall, review:$review, health:$health}')

OUT="reports/pr-autocheck-${REPO}-$(date +%Y%m%dT%H%M%S).json"
printf '%s\n' "$REPORT" > "$OUT"
printf '%s\n' "$REPORT"

# 4) Discord sync (best-effort; non-zero from notifier is surfaced, not fatal)
set +e
printf '%s' "$REPORT" | bash "$HERE/notify-discord.sh"
DRC=$?
set -e 2>/dev/null || true
echo "report_saved=$OUT discord_exit=$DRC" >&2
exit 0
