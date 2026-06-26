#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-.}"
PORT="${2:-3456}"
CONFIG_PATH="$PROJECT_DIR/config.yaml"
BASE_URL="http://127.0.0.1:$PORT"

ok() {
  printf '[OK] %s\n' "$1"
}

fail() {
  printf '[FAIL] %s\n' "$1" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"
}

need_cmd oa
need_cmd curl

[ -d "$PROJECT_DIR" ] || fail "Project directory not found: $PROJECT_DIR"
[ -f "$CONFIG_PATH" ] || fail "config.yaml not found under: $PROJECT_DIR"

ok "Found OA project at $PROJECT_DIR"

oa collect -c "$CONFIG_PATH" >/tmp/oa-skill-smoke-collect.log 2>&1 || {
  cat /tmp/oa-skill-smoke-collect.log >&2
  fail "oa collect failed"
}
ok "oa collect succeeded"

HEALTH_BODY="$(mktemp)"
GOALS_BODY="$(mktemp)"
TEAM_BODY="$(mktemp)"
trap 'rm -f "$HEALTH_BODY" "$GOALS_BODY" "$TEAM_BODY" /tmp/oa-skill-smoke-collect.log' EXIT

HEALTH_CODE="$(curl -sS -o "$HEALTH_BODY" -w '%{http_code}' "$BASE_URL/api/health" || true)"
[ "$HEALTH_CODE" = "200" ] || fail "/api/health returned $HEALTH_CODE on $BASE_URL"
grep -q '"overall"' "$HEALTH_BODY" || fail "/api/health missing overall field"
ok "/api/health passed"

GOALS_CODE="$(curl -sS -o "$GOALS_BODY" -w '%{http_code}' "$BASE_URL/api/goals" || true)"
[ "$GOALS_CODE" = "200" ] || fail "/api/goals returned $GOALS_CODE on $BASE_URL"
grep -Eq '"id"|cron_reliability|team_health' "$GOALS_BODY" || fail "/api/goals missing expected goal content"
ok "/api/goals passed"

TEAM_CODE="$(curl -sS -o "$TEAM_BODY" -w '%{http_code}' "$BASE_URL/api/team-health?days=30" || true)"
[ "$TEAM_CODE" = "200" ] || fail "/api/team-health returned $TEAM_CODE on $BASE_URL"
grep -q '"agent_id"' "$TEAM_BODY" || fail "/api/team-health missing agent_id content"
ok "/api/team-health passed"

printf '[OK] OA workspace smoke test passed for %s on %s\n' "$PROJECT_DIR" "$BASE_URL"
