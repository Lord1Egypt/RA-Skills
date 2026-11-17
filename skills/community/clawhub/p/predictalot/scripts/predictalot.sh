#!/usr/bin/env bash
#
# predictalot.sh — POST a univariate zero-shot forecast and pretty-print the
# median + 10/90 quantile band for each horizon step.
#
# Consumer-only: talks to a predictalot instance you already run. Never
# provisions, launches, or reconfigures the container.
#
# Usage:
#   PREDICTALOT_URL=http://localhost:8080 \
#   PREDICTALOT_AUTH_TOKEN=<token> \        # omit for open-auth servers
#     bash predictalot.sh <model> <horizon> <ctx1> <ctx2> ... <ctxN>
#
# Example:
#   bash predictalot.sh chronos-2 5 10 11 12 13 14 15 16 17 18 19 20
#
# Endpoint: POST $PREDICTALOT_URL/v1/timeseries/univariate/forecast
# Requires: curl, jq

set -euo pipefail

PREDICTALOT_URL="${PREDICTALOT_URL:-http://localhost:8080}"

if [[ $# -lt 3 ]]; then
  echo "usage: $0 <model> <horizon> <ctx1> <ctx2> ... <ctxN>" >&2
  echo "  e.g. $0 chronos-2 5 10 11 12 13 14 15 16 17 18 19 20" >&2
  exit 2
fi

model="$1"; shift
horizon="$1"; shift

# Remaining args are the single-series context window.
context_json="$(printf '%s\n' "$@" | jq -R . | jq -s 'map(tonumber)')"

body="$(jq -n \
  --arg model "$model" \
  --argjson horizon "$horizon" \
  --argjson ctx "$context_json" \
  '{model: $model, context: [$ctx], config: {horizon: $horizon, quantileLevels: [0.1, 0.5, 0.9]}}')"

auth=()
if [[ -n "${PREDICTALOT_AUTH_TOKEN:-}" ]]; then
  auth=(-H "Authorization: Bearer ${PREDICTALOT_AUTH_TOKEN}")
fi

resp="$(curl -sS -w $'\n%{http_code}' \
  "${PREDICTALOT_URL}/v1/timeseries/univariate/forecast" \
  "${auth[@]}" \
  -H "Content-Type: application/json" \
  -d "$body")"

code="$(printf '%s' "$resp" | tail -n1)"
payload="$(printf '%s' "$resp" | sed '$d')"

if [[ "$code" != "200" ]]; then
  echo "request failed (HTTP $code):" >&2
  printf '%s\n' "$payload" | jq . >&2 2>/dev/null || printf '%s\n' "$payload" >&2
  exit 1
fi

echo "model=${model} horizon=${horizon}"
echo "step  p10        p50(median)  p90"
printf '%s' "$payload" | jq -r '
  [.quantiles["0.1"][0], .median[0], .quantiles["0.9"][0]] as $q
  | range(0; ($q[1] | length)) as $i
  | "\($i + 1)     \($q[0][$i])       \($q[1][$i])        \($q[2][$i])"
'
