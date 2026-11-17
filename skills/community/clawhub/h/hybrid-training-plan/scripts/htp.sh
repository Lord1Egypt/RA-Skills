#!/usr/bin/env bash
# htp.sh — CLI adapter for the hybridtrainingplan.app API
# Requires: curl (7.76+), jq
# Env: HYBRID_API_KEY (required), HYBRID_API_URL (optional, must be https)

set -euo pipefail

API_URL="${HYBRID_API_URL:-https://api.hybridtrainingplan.app}"
API_KEY="${HYBRID_API_KEY:?HYBRID_API_KEY must be set}"

# The key goes wherever API_URL points, so refuse anything but https.
[[ "$API_URL" == https://* ]] || { echo "HYBRID_API_URL must start with https://" >&2; exit 2; }
[[ "$API_KEY" =~ ^htp_[0-9a-f]{64}$ ]] || { echo "HYBRID_API_KEY does not look like an htp_ key" >&2; exit 2; }

uuid() { [[ "${1:-}" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]] || { echo "not a UUID: ${1:-}" >&2; exit 2; }; echo "$1"; }
day()  { [[ "${1:-}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || { echo "not a date (YYYY-MM-DD): ${1:-}" >&2; exit 2; }; echo "$1"; }

# Header via stdin so the key never shows up in `ps`.
req() {
  local method="$1" path="$2" body="${3:-}"
  local args=(-sS --fail-with-body --max-time 30 --proto '=https' -X "$method" -H @-)
  [[ -n "$body" ]] && args+=(-H "Content-Type: application/json" --data-binary "$body")
  printf 'Authorization: Bearer %s\n' "$API_KEY" | curl "${args[@]}" "$API_URL$path"
}

# Compact view of /api/watch/sessions: what to do, with the ids needed to log it.
SLIM_SESSIONS='[.sessions[] | {
  dayDate, planId, sessionId, kind, sessionType, title, durationMinutes, done, description,
  exercises: (if .strength then (.strength as $s | $s.exercises | to_entries | map(
    .key as $i | [$s.sets[] | select(.exerciseIdx == $i and .warmupPercent == null)] as $w
    | {name: .value.name, exerciseKey: .value.key, prescription: .value.label, loadGuidance: .value.loadGuidance,
       workSets: ($w | length), suggestedKg: ($w[0].weightKg)})) else null end),
  runSteps, workout
} | with_entries(select(.value != null))]'

cmd="${1:-}"
shift || true

case "$cmd" in
  today)
    today=$(date +%F)
    req GET /api/watch/sessions | jq --arg d "$today" "{state, distanceUnit, sessions: ($SLIM_SESSIONS | map(select(.dayDate == \$d)))}"
    ;;

  upcoming)
    req GET /api/watch/sessions | jq "{state, distanceUnit, sessions: $SLIM_SESSIONS}"
    ;;

  dashboard)
    req GET /api/users/me/dashboard | jq '{
      currentPlanId: .user.currentPlanId, distanceUnit, totalCompletedSessions,
      plans: [.plans[] | {id, title, status, startsAt, endsAt, isAdaptive}],
      today: (.todaySession | if . then {planId, planTitle, date: .day.date, status: .day.status, isRestDay: .day.isRestDay,
        sessions: [.day.sessions[] | {id, title, sessionType, durationMinutes}]} else null end)
    }'
    ;;

  day)
    d=$(day "${1:-}"); p=$(uuid "${2:-}")
    req GET "/api/plans/$p" | jq --arg d "$d" '[.content.weeks[].days[] | select(.date == $d)][0]'
    ;;

  complete|skip)
    d=$(day "${1:-}"); p=$(uuid "${2:-}")
    status=$([[ "$cmd" == complete ]] && echo completed || echo skipped)
    req PATCH "/api/plans/$p/days/$d" "{\"status\":\"$status\"}" | jq .
    ;;

  log-session)
    body="${1:?JSON body required}"
    jq -e 'type == "object" and .planId and .sessionId and .dayDate and .sessionType' <<<"$body" >/dev/null \
      || { echo "body must be a JSON object with planId, sessionId, dayDate, sessionType" >&2; exit 2; }
    req PUT /api/session-logs "$body" | jq .
    ;;

  session-logs)
    p=$(uuid "${1:-}"); d=$(day "${2:-}")
    req GET "/api/session-logs?planId=$p&dayDate=$d" | jq .
    ;;

  maxes)
    req GET /api/exercise-maxes | jq '[.maxes[] | {displayName, exerciseKey, oneRepMaxKg, source, updatedAt}] | sort_by(.displayName)'
    ;;

  set-max)
    name="${1:?exercise name required}"; kg="${2:?weight in kg required}"
    body=$(jq -n --arg n "$name" --argjson kg "$kg" '{exerciseName: $n, oneRepMaxKg: $kg}')
    req PUT /api/exercise-maxes "$body" | jq .
    ;;

  *)
    cat >&2 <<'EOF'
Usage: htp.sh <command> [args]
Sends authenticated HTTPS requests to $HYBRID_API_URL (default api.hybridtrainingplan.app).

Read-only:
  today                          today's sessions, with ids and suggested weights
  upcoming                       the coming days' sessions
  dashboard                      current plan id, plans, today's day status
  day <date> <planId>            one day in full from the plan
  session-logs <planId> <date>   logs recorded for a day
  maxes                          stored 1RMs

Write (changes your live account immediately):
  log-session '<json>'           save or replace a session log; completes the day
  complete <date> <planId>       mark a day completed
  skip <date> <planId>           mark a day skipped
  set-max "<exercise>" <kg>      overwrite a 1RM
EOF
    exit 1
    ;;
esac
