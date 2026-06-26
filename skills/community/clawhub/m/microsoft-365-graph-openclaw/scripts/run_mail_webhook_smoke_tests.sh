#!/usr/bin/env bash
set -eu
set -o pipefail 2>/dev/null || true

# Minimal-input smoke tests for Graph mail webhook setup.
# Reuses values from /etc/default/graph-mail-webhook when available.

usage() {
  cat <<'EOF'
Usage:
  bash scripts/run_mail_webhook_smoke_tests.sh \
    --domain graphhook.example.com \
    [--test-email tar.alitar@outlook.com] \
    [--client-state "<GRAPH_WEBHOOK_CLIENT_STATE>"] \
    [--adapter-port 8789] \
    [--adapter-path /graph/mail] \
    [--repo-root /path/to/microsoft-365-graph-openclaw] \
    [--create-subscription]

Notes:
  - If /etc/default/graph-mail-webhook exists, values are auto-loaded.
  - --create-subscription enables create/status/renew/delete test cycle.
  - If --test-email is provided, sends a real email and confirms inbox search.
EOF
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing command: $1" >&2
    exit 1
  }
}

DOMAIN=""
TEST_EMAIL=""
CLIENT_STATE=""
ADAPTER_PORT="8789"
ADAPTER_PATH="/graph/mail"
REPO_ROOT="$(pwd)"
CREATE_SUBSCRIPTION="true"
ENV_FILE="/etc/default/graph-mail-webhook"
TMP_SUB_ID=""
OPENCLAW_HOOK_URL="${OPENCLAW_HOOK_URL:-}"
OPENCLAW_HOOK_TOKEN="${OPENCLAW_HOOK_TOKEN:-}"
PASS_COUNT=0
SKIP_COUNT=0

pass() { PASS_COUNT=$((PASS_COUNT + 1)); echo "[PASS] $1"; }
skip() { SKIP_COUNT=$((SKIP_COUNT + 1)); echo "[SKIP] $1"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="$2"; shift 2 ;;
    --test-email) TEST_EMAIL="$2"; shift 2 ;;
    --client-state) CLIENT_STATE="$2"; shift 2 ;;
    --adapter-port) ADAPTER_PORT="$2"; shift 2 ;;
    --adapter-path) ADAPTER_PATH="$2"; shift 2 ;;
    --repo-root) REPO_ROOT="$2"; shift 2 ;;
    --create-subscription) CREATE_SUBSCRIPTION="true"; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  CLIENT_STATE="${CLIENT_STATE:-${GRAPH_WEBHOOK_CLIENT_STATE:-}}"
  if [[ "${ADAPTER_PORT}" == "8789" && -n "${GRAPH_WEBHOOK_ADAPTER_PORT:-}" ]]; then
    ADAPTER_PORT="${GRAPH_WEBHOOK_ADAPTER_PORT}"
  fi
  if [[ "${ADAPTER_PATH}" == "/graph/mail" && -n "${GRAPH_WEBHOOK_ADAPTER_PATH:-}" ]]; then
    ADAPTER_PATH="${GRAPH_WEBHOOK_ADAPTER_PATH}"
  fi
fi

if [[ -z "$DOMAIN" ]]; then
  echo "Missing required argument: --domain" >&2
  usage
  exit 1
fi

if [[ -z "$CLIENT_STATE" ]]; then
  echo "Missing client state. Provide --client-state or set GRAPH_WEBHOOK_CLIENT_STATE in $ENV_FILE." >&2
  exit 1
fi

if [[ "$ADAPTER_PATH" != /* ]]; then
  ADAPTER_PATH="/$ADAPTER_PATH"
fi

require_cmd curl
require_cmd python3

SEND_SCRIPT="$REPO_ROOT/scripts/mail_send.py"
FETCH_SCRIPT="$REPO_ROOT/scripts/mail_fetch.py"
SUB_SCRIPT="$REPO_ROOT/scripts/mail_subscriptions.py"

[[ -f "$SUB_SCRIPT" ]] || { echo "File not found: $SUB_SCRIPT" >&2; exit 1; }

cleanup() {
  if [[ -n "$TMP_SUB_ID" ]]; then
    echo "[cleanup] deleting temporary subscription: $TMP_SUB_ID"
    python3 "$SUB_SCRIPT" delete --id "$TMP_SUB_ID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

echo "[1/6] Local adapter handshake..."
LOCAL_TOKEN="local-$(date +%s)"
LOCAL_RESULT="$(curl -fsS "http://127.0.0.1:${ADAPTER_PORT}${ADAPTER_PATH}?validationToken=${LOCAL_TOKEN}")"
[[ "$LOCAL_RESULT" == "$LOCAL_TOKEN" ]] || {
  echo "Local handshake failed. Expected '$LOCAL_TOKEN', got '$LOCAL_RESULT'." >&2
  exit 1
}
pass "Local adapter handshake"

echo "[2/6] Public HTTPS handshake..."
PUBLIC_TOKEN="public-$(date +%s)"
PUBLIC_RESULT="$(curl -fsS "https://${DOMAIN}${ADAPTER_PATH}?validationToken=${PUBLIC_TOKEN}")"
[[ "$PUBLIC_RESULT" == "$PUBLIC_TOKEN" ]] || {
  echo "Public handshake failed. Expected '$PUBLIC_TOKEN', got '$PUBLIC_RESULT'." >&2
  exit 1
}
pass "Public HTTPS handshake"

if [[ -n "$OPENCLAW_HOOK_URL" && -n "$OPENCLAW_HOOK_TOKEN" ]]; then
  echo "[2b] OpenClaw hook auth check..."
  if [[ "$OPENCLAW_HOOK_URL" == *"/wake" ]]; then
    curl -fsS -X POST "$OPENCLAW_HOOK_URL" \
      -H "Authorization: Bearer $OPENCLAW_HOOK_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"text":"Graph webhook smoke auth test","mode":"now"}' >/dev/null
    pass "OpenClaw /hooks/wake authentication"
  else
    curl -fsS -X POST "$OPENCLAW_HOOK_URL" \
      -H "Authorization: Bearer $OPENCLAW_HOOK_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"message":"Graph webhook smoke test","name":"GraphSmoke","wakeMode":"next-heartbeat"}' >/dev/null
    pass "OpenClaw /hooks/agent authentication"
  fi
else
  skip "OpenClaw hook auth check (missing OPENCLAW_HOOK_URL / OPENCLAW_HOOK_TOKEN in env)"
fi

if [[ "$CREATE_SUBSCRIPTION" == "true" ]]; then
  echo "[3/6] Subscription lifecycle test (create/status/renew/delete)..."
  CREATE_JSON="$(
    python3 "$SUB_SCRIPT" create \
      --notification-url "https://${DOMAIN}${ADAPTER_PATH}" \
      --client-state "$CLIENT_STATE" \
      --minutes 180
  )"
  TMP_SUB_ID="$(
    python3 - <<'PY' "$CREATE_JSON"
import json
import sys
body = json.loads(sys.argv[1])
print(body.get("id", ""))
PY
  )"
  if [[ -z "$TMP_SUB_ID" ]]; then
    echo "Failed to parse temporary subscription id." >&2
    echo "$CREATE_JSON"
    exit 1
  fi
  echo "Created: $TMP_SUB_ID"
  python3 "$SUB_SCRIPT" status --id "$TMP_SUB_ID" >/dev/null
  python3 "$SUB_SCRIPT" renew --id "$TMP_SUB_ID" --minutes 180 >/dev/null
  python3 "$SUB_SCRIPT" delete --id "$TMP_SUB_ID" >/dev/null
  TMP_SUB_ID=""
  pass "Subscription lifecycle create/status/renew/delete"
else
  skip "Subscription lifecycle test (run with --create-subscription)"
fi

if [[ -n "$TEST_EMAIL" ]]; then
  [[ -f "$SEND_SCRIPT" ]] || { echo "File not found: $SEND_SCRIPT" >&2; exit 1; }
  [[ -f "$FETCH_SCRIPT" ]] || { echo "File not found: $FETCH_SCRIPT" >&2; exit 1; }
  echo "[4/6] Sending real email..."
  TEST_SUBJECT="Graph Push Smoke $(date +%Y%m%d-%H%M%S)"
  python3 "$SEND_SCRIPT" --to "$TEST_EMAIL" --subject "$TEST_SUBJECT" --body "Graph webhook smoke test."
  echo "Sent subject: $TEST_SUBJECT"

  echo "[5/6] Confirming inbox delivery (poll up to 60s)..."
  FOUND="false"
  LAST_FETCH_ERROR=""
  for _ in $(seq 1 12); do
    FETCH_OUTPUT=""
    if FETCH_OUTPUT="$(python3 "$FETCH_SCRIPT" --folder Inbox --top 10 --subject "$TEST_SUBJECT" 2>&1)"; then
      RESULT="$(python3 - <<'PY' "$FETCH_OUTPUT"
import json
import sys
raw = sys.argv[1]
try:
    data = json.loads(raw)
except Exception:
    print("invalid")
    raise SystemExit(0)
print("ok" if data.get("value") else "no")
PY
)"
      if [[ "$RESULT" == "ok" ]]; then
        FOUND="true"
        break
      fi
      if [[ "$RESULT" == "invalid" ]]; then
        LAST_FETCH_ERROR="mail_fetch returned non-JSON output"
      fi
    else
      LAST_FETCH_ERROR="$FETCH_OUTPUT"
    fi
    if [[ -n "$LAST_FETCH_ERROR" ]]; then
      echo "[INFO] inbox poll retry; last fetch issue: ${LAST_FETCH_ERROR}" >&2
    fi
    sleep 5
  done
  if [[ "$FOUND" != "true" ]]; then
    if [[ -n "$LAST_FETCH_ERROR" ]]; then
      echo "Email not confirmed due fetch errors. Last error:" >&2
      echo "$LAST_FETCH_ERROR" >&2
    fi
    echo "Email not found in Inbox by subject within timeout." >&2
    exit 1
  fi
  pass "Real email send + Inbox confirmation"
else
  skip "Real email send (add --test-email)"
  skip "Inbox confirmation (depends on --test-email)"
fi

echo "[6/6] Final status..."
echo "Smoke tests completed."
echo "- Domain: https://${DOMAIN}${ADAPTER_PATH}"
echo "- Local adapter: http://127.0.0.1:${ADAPTER_PORT}${ADAPTER_PATH}"
echo "- Client state: configured"
echo "- Passed checks: ${PASS_COUNT}"
echo "- Skipped checks: ${SKIP_COUNT}"

if [[ "$CREATE_SUBSCRIPTION" == "true" && -n "$TEST_EMAIL" ]]; then
  echo "READINESS VERDICT: READY_FOR_PUSH (all critical + live email checks passed)"
else
  echo "READINESS VERDICT: PARTIAL_READY"
  echo "To reach full readiness, run with:"
  echo "  --create-subscription --test-email <mailbox>"
fi
