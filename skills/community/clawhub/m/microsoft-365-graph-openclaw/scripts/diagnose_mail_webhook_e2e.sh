#!/usr/bin/env bash
set -eu
set -o pipefail 2>/dev/null || true

# End-to-end diagnostic for Graph -> Adapter -> Worker -> OpenClaw wake flow.
# Read-only by default, with optional wake probe.

usage() {
  cat <<'EOF'
Usage:
  bash scripts/diagnose_mail_webhook_e2e.sh \
    --domain graphhook.example.com \
    [--repo-root /path/to/microsoft-365-graph-openclaw] \
    [--lookback-minutes 30] \
    [--subscription-id <id>] \
    [--skip-wake-probe]

What it checks:
  1) Env/config values from /etc/default/graph-mail-webhook
  2) Service health (caddy, adapter, worker, renew timer)
  3) Active subscriptions + optional detailed status by id
  4) Queue/dedupe files and webhook ops log snippets
  5) Adapter and worker logs for recent delivery evidence
  6) Optional OpenClaw wake probe (POST /hooks/wake)

Outputs:
  - PASS/WARN/FAIL lines per check
  - Final diagnostic verdict with remediation hints
EOF
}

pass() { echo "[PASS] $1"; }
warn() { echo "[WARN] $1"; }
fail() { echo "[FAIL] $1"; }
info() { echo "[INFO] $1"; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing command: $1" >&2
    exit 1
  }
}

mask_secret() {
  local value="${1:-}"
  local n="${#value}"
  if [[ "$n" -le 8 ]]; then
    printf "<hidden:%d>" "$n"
    return
  fi
  printf "%s...%s" "${value:0:4}" "${value:n-4:4}"
}

DOMAIN=""
REPO_ROOT="$(pwd)"
LOOKBACK_MINUTES="30"
SUBSCRIPTION_ID=""
SKIP_WAKE_PROBE="false"
ENV_FILE="/etc/default/graph-mail-webhook"
STATE_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="$2"; shift 2 ;;
    --repo-root) REPO_ROOT="$2"; shift 2 ;;
    --lookback-minutes) LOOKBACK_MINUTES="$2"; shift 2 ;;
    --subscription-id) SUBSCRIPTION_ID="$2"; shift 2 ;;
    --skip-wake-probe) SKIP_WAKE_PROBE="true"; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$DOMAIN" ]]; then
  echo "Missing required argument: --domain" >&2
  usage
  exit 1
fi

require_cmd python3
require_cmd systemctl
require_cmd curl
require_cmd journalctl
require_cmd ss
require_cmd grep
require_cmd sed

MAIL_SUB_SCRIPT="$REPO_ROOT/scripts/mail_subscriptions.py"
[[ -f "$MAIL_SUB_SCRIPT" ]] || { echo "File not found: $MAIL_SUB_SCRIPT" >&2; exit 1; }

if [[ -f "$REPO_ROOT/state/graph_ops.log" ]]; then
  STATE_DIR="$REPO_ROOT/state"
elif [[ -f "$HOME/.openclaw/workspace/state/graph_ops.log" ]]; then
  STATE_DIR="$HOME/.openclaw/workspace/state"
else
  STATE_DIR="$REPO_ROOT/state"
fi

read_env_value() {
  local key="$1"
  if [[ -r "$ENV_FILE" ]]; then
    grep -E "^${key}=" "$ENV_FILE" | head -n1 | sed -E "s/^${key}=//"
  elif command -v sudo >/dev/null 2>&1; then
    sudo grep -E "^${key}=" "$ENV_FILE" 2>/dev/null | head -n1 | sed -E "s/^${key}=//"
  else
    true
  fi
}

OPENCLAW_HOOK_URL="$(read_env_value OPENCLAW_HOOK_URL || true)"
OPENCLAW_HOOK_TOKEN="$(read_env_value OPENCLAW_HOOK_TOKEN || true)"
OPENCLAW_SESSION_KEY="$(read_env_value OPENCLAW_SESSION_KEY || true)"
GRAPH_WEBHOOK_CLIENT_STATE="$(read_env_value GRAPH_WEBHOOK_CLIENT_STATE || true)"
GRAPH_MAIL_SUBSCRIPTION_ID_ENV="$(read_env_value GRAPH_MAIL_SUBSCRIPTION_ID || true)"
GRAPH_WEBHOOK_ADAPTER_PORT="$(read_env_value GRAPH_WEBHOOK_ADAPTER_PORT || true)"
GRAPH_WEBHOOK_ADAPTER_PATH="$(read_env_value GRAPH_WEBHOOK_ADAPTER_PATH || true)"

if [[ -z "$GRAPH_WEBHOOK_ADAPTER_PORT" ]]; then GRAPH_WEBHOOK_ADAPTER_PORT="8789"; fi
if [[ -z "$GRAPH_WEBHOOK_ADAPTER_PATH" ]]; then GRAPH_WEBHOOK_ADAPTER_PATH="/graph/mail"; fi

echo "==== Graph Webhook E2E Diagnostics ===="
echo "Domain: $DOMAIN"
echo "Repo root: $REPO_ROOT"
echo "State dir: $STATE_DIR"
echo "Lookback: ${LOOKBACK_MINUTES} minutes"
echo

echo "---- 1) Environment ----"
if [[ -n "$OPENCLAW_HOOK_URL" ]]; then pass "OPENCLAW_HOOK_URL=${OPENCLAW_HOOK_URL}"; else fail "OPENCLAW_HOOK_URL missing in $ENV_FILE"; fi
if [[ -n "$OPENCLAW_HOOK_TOKEN" ]]; then pass "OPENCLAW_HOOK_TOKEN=$(mask_secret "$OPENCLAW_HOOK_TOKEN")"; else fail "OPENCLAW_HOOK_TOKEN missing in $ENV_FILE"; fi
if [[ -n "$GRAPH_WEBHOOK_CLIENT_STATE" ]]; then pass "GRAPH_WEBHOOK_CLIENT_STATE=$(mask_secret "$GRAPH_WEBHOOK_CLIENT_STATE")"; else fail "GRAPH_WEBHOOK_CLIENT_STATE missing in $ENV_FILE"; fi
if [[ -n "$OPENCLAW_SESSION_KEY" ]]; then pass "OPENCLAW_SESSION_KEY=${OPENCLAW_SESSION_KEY}"; else warn "OPENCLAW_SESSION_KEY missing in $ENV_FILE"; fi
if [[ -n "$GRAPH_MAIL_SUBSCRIPTION_ID_ENV" ]]; then pass "GRAPH_MAIL_SUBSCRIPTION_ID=${GRAPH_MAIL_SUBSCRIPTION_ID_ENV}"; else warn "GRAPH_MAIL_SUBSCRIPTION_ID not set in $ENV_FILE"; fi
pass "Adapter endpoint: http://127.0.0.1:${GRAPH_WEBHOOK_ADAPTER_PORT}${GRAPH_WEBHOOK_ADAPTER_PATH}"
echo

echo "---- 2) Service health ----"
if systemctl is-active --quiet caddy; then pass "caddy active"; else fail "caddy inactive"; fi
if systemctl is-active --quiet graph-mail-webhook-adapter; then pass "graph-mail-webhook-adapter active"; else fail "graph-mail-webhook-adapter inactive"; fi
if systemctl is-active --quiet graph-mail-webhook-worker; then pass "graph-mail-webhook-worker active"; else fail "graph-mail-webhook-worker inactive"; fi
if systemctl is-active --quiet graph-mail-subscription-renew.timer; then pass "graph-mail-subscription-renew.timer active"; else warn "graph-mail-subscription-renew.timer inactive"; fi
if ss -tln | grep -q ":${GRAPH_WEBHOOK_ADAPTER_PORT}"; then pass "adapter port ${GRAPH_WEBHOOK_ADAPTER_PORT} is listening"; else fail "adapter port ${GRAPH_WEBHOOK_ADAPTER_PORT} is not listening"; fi
if ss -tln | grep -q ":443"; then pass "HTTPS port 443 is listening"; else warn "HTTPS port 443 is not listening"; fi
echo

echo "---- 3) Subscription checks ----"
SUBS_JSON="$(python3 "$MAIL_SUB_SCRIPT" list --top 50 || true)"
if [[ -z "$SUBS_JSON" ]]; then
  fail "Could not retrieve subscriptions list"
else
  SUBS_COUNT="$(python3 - <<'PY' "$SUBS_JSON"
import json, sys
try:
    data=json.loads(sys.argv[1])
    print(len(data.get("value",[])))
except Exception:
    print("0")
PY
)"
  if [[ "${SUBS_COUNT}" == "0" ]]; then
    fail "No active subscriptions"
  else
    pass "Active subscriptions: ${SUBS_COUNT}"
  fi
  python3 - <<'PY' "$SUBS_JSON"
import json, sys
try:
    data=json.loads(sys.argv[1])
except Exception:
    print("[WARN] Could not parse subscriptions payload")
    raise SystemExit(0)
for s in data.get("value",[]):
    print(f"[INFO] sub={s.get('id')} resource={s.get('resource')} changeType={s.get('changeType')} expires={s.get('expirationDateTime')} clientState={'set' if s.get('clientState') else 'null'}")
PY
fi

if [[ -z "$SUBSCRIPTION_ID" && -n "$GRAPH_MAIL_SUBSCRIPTION_ID_ENV" ]]; then
  SUBSCRIPTION_ID="$GRAPH_MAIL_SUBSCRIPTION_ID_ENV"
fi
if [[ -z "$SUBSCRIPTION_ID" && -n "$SUBS_JSON" ]]; then
  SUBSCRIPTION_ID="$(python3 - <<'PY' "$SUBS_JSON"
import json, sys
try:
    data=json.loads(sys.argv[1])
    vals=data.get("value",[])
    print(vals[0].get("id","") if vals else "")
except Exception:
    print("")
PY
)"
fi

if [[ -n "$SUBSCRIPTION_ID" ]]; then
  SUB_STATUS="$(python3 "$MAIL_SUB_SCRIPT" status --id "$SUBSCRIPTION_ID" || true)"
  if [[ -n "$SUB_STATUS" ]]; then
    python3 - <<'PY' "$SUB_STATUS" "$GRAPH_WEBHOOK_CLIENT_STATE"
import json, sys
data=json.loads(sys.argv[1])
expected=sys.argv[2]
cid=data.get("clientState")
if cid:
    print(f"[PASS] subscription({data.get('id')}) clientState present")
    if expected and cid != expected:
        print("[WARN] subscription clientState differs from env GRAPH_WEBHOOK_CLIENT_STATE")
else:
    print(f"[WARN] subscription({data.get('id')}) clientState is null")
PY
  else
    warn "Could not retrieve status for subscription id: $SUBSCRIPTION_ID"
  fi
else
  warn "No subscription id available for detailed status check"
fi
echo

echo "---- 4) Queue / state files ----"
QUEUE_FILE="$STATE_DIR/mail_webhook_queue.jsonl"
DEDUPE_FILE="$STATE_DIR/mail_webhook_dedupe.json"
OPS_FILE="$STATE_DIR/graph_ops.log"
if [[ -f "$QUEUE_FILE" ]]; then
  QUEUE_LINES="$(wc -l < "$QUEUE_FILE" | tr -d ' ')"
  pass "Queue file exists ($QUEUE_FILE), lines=$QUEUE_LINES"
else
  warn "Queue file missing: $QUEUE_FILE"
fi
if [[ -f "$DEDUPE_FILE" ]]; then
  pass "Dedupe file exists: $DEDUPE_FILE"
else
  warn "Dedupe file missing: $DEDUPE_FILE"
fi
if [[ -f "$OPS_FILE" ]]; then
  info "Recent webhook ops (with UTC timestamp when available):"
  python3 - <<'PY' "$OPS_FILE"
import json
import sys
from datetime import datetime, timezone

path = sys.argv[1]
try:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
except Exception:
    print("[WARN] Could not read ops file")
    raise SystemExit(0)

filtered = [ln for ln in lines if ("mail_webhook_" in ln or "mail_subscription_" in ln)]
for line in filtered[-20:]:
    rendered = line
    try:
        obj = json.loads(line)
        ts = obj.get("timestamp")
        if isinstance(ts, (int, float)):
            obj["timestampUtc"] = datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        rendered = json.dumps(obj, ensure_ascii=False)
    except Exception:
        pass
    print(rendered)
PY
else
  warn "Ops log missing: $OPS_FILE"
fi
echo

echo "---- 5) Recent adapter/worker evidence (${LOOKBACK_MINUTES}m) ----"
ADAPTER_LOG="$(sudo journalctl -u graph-mail-webhook-adapter --since "${LOOKBACK_MINUTES} minutes ago" --no-pager || true)"
WORKER_LOG="$(sudo journalctl -u graph-mail-webhook-worker --since "${LOOKBACK_MINUTES} minutes ago" --no-pager || true)"

REAL_POST_COUNT="$(printf "%s\n" "$ADAPTER_LOG" | grep -c 'POST /graph/mail HTTP/1.1" 202' || true)"
VALIDATION_COUNT="$(printf "%s\n" "$ADAPTER_LOG" | grep -c 'validationToken' || true)"
if [[ "${REAL_POST_COUNT}" -gt 0 ]]; then
  pass "Graph delivery observed: ${REAL_POST_COUNT} real POST(s) to /graph/mail"
else
  warn "No real /graph/mail 202 deliveries observed in last ${LOOKBACK_MINUTES} minutes"
fi
if [[ "${VALIDATION_COUNT}" -gt 0 ]]; then
  info "Validation handshake events observed: ${VALIDATION_COUNT}"
fi

QUEUE_EMPTY_COUNT="$(printf "%s\n" "$WORKER_LOG" | grep -c 'Queue is empty' || true)"
if [[ "${QUEUE_EMPTY_COUNT}" -gt 0 ]]; then
  info "Worker reported empty queue ${QUEUE_EMPTY_COUNT} time(s)"
fi
if printf "%s\n" "$WORKER_LOG" | grep -qi 'error\|traceback\|failed'; then
  warn "Worker logs contain error/failure indicators"
else
  pass "No explicit worker errors found in recent logs"
fi
echo

echo "---- 6) Optional wake probe ----"
WAKE_HTTP_CODE="SKIPPED"
if [[ "$SKIP_WAKE_PROBE" == "true" ]]; then
  info "Wake probe skipped by flag"
elif [[ -n "$OPENCLAW_HOOK_URL" && -n "$OPENCLAW_HOOK_TOKEN" ]]; then
  WAKE_HTTP_CODE="$(curl -s -o /tmp/diag_wake_body.json -w "%{http_code}" -X POST "$OPENCLAW_HOOK_URL" \
    -H "Authorization: Bearer $OPENCLAW_HOOK_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"text":"diagnostic wake probe","mode":"now"}' || true)"
  if [[ "$WAKE_HTTP_CODE" == "200" ]]; then
    pass "Wake probe returned HTTP 200"
  else
    warn "Wake probe HTTP code: $WAKE_HTTP_CODE"
  fi
else
  warn "Wake probe skipped (missing OPENCLAW_HOOK_URL or OPENCLAW_HOOK_TOKEN)"
fi
echo

echo "==== Diagnostic verdict ===="
HARD_FAIL=0
[[ -n "$OPENCLAW_HOOK_URL" ]] || HARD_FAIL=1
[[ -n "$OPENCLAW_HOOK_TOKEN" ]] || HARD_FAIL=1
[[ -n "$GRAPH_WEBHOOK_CLIENT_STATE" ]] || HARD_FAIL=1
systemctl is-active --quiet caddy || HARD_FAIL=1
systemctl is-active --quiet graph-mail-webhook-adapter || HARD_FAIL=1
systemctl is-active --quiet graph-mail-webhook-worker || HARD_FAIL=1

if [[ "$HARD_FAIL" -eq 1 ]]; then
  echo "VERDICT: NOT_READY (base configuration/services issue)"
  echo "Action: fix FAIL items above first."
  exit 2
fi

if [[ "${REAL_POST_COUNT}" -gt 0 && ( "$WAKE_HTTP_CODE" == "200" || "$WAKE_HTTP_CODE" == "SKIPPED" ) ]]; then
  echo "VERDICT: READY_PIPELINE (delivery evidence + healthy services)"
else
  echo "VERDICT: PARTIAL_READY"
  echo "Action hints:"
  echo "- If no real POST deliveries: re-send external test mail and monitor adapter with --follow"
  echo "- If wake probe not 200: verify OpenClaw hook token/path"
  echo "- If queue remains empty with real POST deliveries: inspect adapter parsing for messageId fallback"
fi
