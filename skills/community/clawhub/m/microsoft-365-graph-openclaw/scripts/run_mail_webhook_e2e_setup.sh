#!/usr/bin/env bash
set -eu
set -o pipefail 2>/dev/null || true

# One-command setup for steps 2..6:
# 2) Run EC2 bootstrap script
# 3) Validate public HTTPS endpoint handshake
# 4) Create Graph subscription
# 5) Persist subscription id + restart renew services
# 6) Optional real email send test

usage() {
  cat <<'EOF'
Usage:
  sudo bash scripts/run_mail_webhook_e2e_setup.sh \
    --domain graphhook.alitar.one \
    --hook-token "<OPENCLAW_HOOK_TOKEN>" \
    [--configure-openclaw-hooks] \
    [--openclaw-config /path/to/openclaw.json] \
    [--openclaw-service-name auto] \
    [--openclaw-hooks-path /hooks] \
    [--openclaw-allow-request-session-key true] \
    [--hook-url http://127.0.0.1:18789/hooks/wake] \
    [--session-key hook:graph-mail] \
    [--client-state "<GRAPH_WEBHOOK_CLIENT_STATE>"] \
    [--repo-root /path/to/microsoft-365-graph-openclaw] \
    [--minutes 4200] \
    [--test-email tar.alitar@outlook.com] \
    [--dry-run]

Notes:
  - Must run on Linux host where OpenClaw + this repo are installed.
  - Must run as root (or via sudo), because it writes /etc/default and systemd units.
  - If --client-state is omitted, a strong value is auto-generated.
EOF
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing command: $1" >&2
    exit 1
  }
}

ok() { echo "[OK] $1"; }
info() { echo "[INFO] $1"; }
run_cmd() {
  if [[ "$DRY_RUN" == "true" ]]; then
    info "[DRY-RUN] $*"
    return 0
  fi
  "$@"
}

DOMAIN=""
HOOK_URL="http://127.0.0.1:18789/hooks/wake"
HOOK_URL_PROVIDED="false"
HOOK_TOKEN=""
SESSION_KEY="hook:graph-mail"
CLIENT_STATE=""
REPO_ROOT="$(pwd)"
MINUTES="4200"
TEST_EMAIL=""
CONFIGURE_OPENCLAW_HOOKS="false"
OPENCLAW_CONFIG=""
OPENCLAW_SERVICE_NAME="auto"
OPENCLAW_HOOKS_PATH="/hooks"
OPENCLAW_ALLOW_REQUEST_SESSION_KEY="true"
DRY_RUN="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="$2"; shift 2 ;;
    --hook-url) HOOK_URL="$2"; HOOK_URL_PROVIDED="true"; shift 2 ;;
    --hook-token) HOOK_TOKEN="$2"; shift 2 ;;
    --configure-openclaw-hooks) CONFIGURE_OPENCLAW_HOOKS="true"; shift 1 ;;
    --openclaw-config) OPENCLAW_CONFIG="$2"; shift 2 ;;
    --openclaw-service-name) OPENCLAW_SERVICE_NAME="$2"; shift 2 ;;
    --openclaw-hooks-path) OPENCLAW_HOOKS_PATH="$2"; shift 2 ;;
    --openclaw-allow-request-session-key) OPENCLAW_ALLOW_REQUEST_SESSION_KEY="$2"; shift 2 ;;
    --session-key) SESSION_KEY="$2"; shift 2 ;;
    --client-state) CLIENT_STATE="$2"; shift 2 ;;
    --repo-root) REPO_ROOT="$2"; shift 2 ;;
    --minutes) MINUTES="$2"; shift 2 ;;
    --test-email) TEST_EMAIL="$2"; shift 2 ;;
    --dry-run) DRY_RUN="true"; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$DOMAIN" || -z "$HOOK_TOKEN" ]]; then
  echo "Missing required arguments: --domain and --hook-token." >&2
  usage
  exit 1
fi

if [[ "$DRY_RUN" != "true" && "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "Run as root (sudo)." >&2
  exit 1
fi

require_cmd curl
require_cmd systemctl
require_cmd python3
require_cmd sed
require_cmd grep
require_cmd cp
if [[ "$DRY_RUN" == "true" ]]; then
  info "Dry-run mode enabled: no system changes or API writes will be applied."
fi

SETUP_SCRIPT="$REPO_ROOT/scripts/setup_mail_webhook_ec2.sh"
SUB_SCRIPT="$REPO_ROOT/scripts/mail_subscriptions.py"
SEND_SCRIPT="$REPO_ROOT/scripts/mail_send.py"
ENV_FILE="/etc/default/graph-mail-webhook"
ADAPTER_PATH="/graph/mail"

[[ -f "$SETUP_SCRIPT" ]] || { echo "File not found: $SETUP_SCRIPT" >&2; exit 1; }
[[ -f "$SUB_SCRIPT" ]] || { echo "File not found: $SUB_SCRIPT" >&2; exit 1; }

if [[ -z "$CLIENT_STATE" ]]; then
  CLIENT_STATE="$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
)"
fi

if [[ "$OPENCLAW_HOOKS_PATH" != /* ]]; then
  OPENCLAW_HOOKS_PATH="/$OPENCLAW_HOOKS_PATH"
fi

if [[ "$CONFIGURE_OPENCLAW_HOOKS" == "true" ]]; then
  ACTING_USER="${SUDO_USER:-$USER}"
  ACTING_HOME="$(eval echo "~$ACTING_USER")"

  if [[ -z "$OPENCLAW_CONFIG" ]]; then
    CANDIDATES=(
      "/etc/openclaw/config.json5"
      "/etc/openclaw/config.json"
      "/opt/openclaw/config.json5"
      "/opt/openclaw/openclaw.json"
      "$HOME/.openclaw/config.json5"
      "$HOME/.openclaw/config.json"
      "$HOME/.openclaw/openclaw.json"
      "$HOME/.config/openclaw/config.json5"
      "$HOME/.config/openclaw/config.json"
      "$ACTING_HOME/.openclaw/config.json5"
      "$ACTING_HOME/.openclaw/config.json"
      "$ACTING_HOME/.openclaw/openclaw.json"
      "$ACTING_HOME/.config/openclaw/config.json5"
      "$ACTING_HOME/.config/openclaw/config.json"
    )
    for cand in "${CANDIDATES[@]}"; do
      if [[ -f "$cand" ]]; then
        OPENCLAW_CONFIG="$cand"
        break
      fi
    done
  fi

  if [[ -z "$OPENCLAW_CONFIG" ]]; then
    echo "OpenClaw config not found automatically." >&2
    echo "Provide --openclaw-config with the correct path." >&2
    echo "Try discovery on host:" >&2
    echo "  sudo sh -lc 'ls -la /etc/openclaw /opt/openclaw ~/.openclaw ~/.config/openclaw 2>/dev/null'" >&2
    exit 1
  fi
  [[ -f "$OPENCLAW_CONFIG" ]] || { echo "OpenClaw config not found: $OPENCLAW_CONFIG" >&2; exit 1; }

  if [[ "$HOOK_URL_PROVIDED" == "false" ]]; then
    HOOK_URL="http://127.0.0.1:18789${OPENCLAW_HOOKS_PATH}/wake"
  fi

  BACKUP_PATH="${OPENCLAW_CONFIG}.bak.$(date +%Y%m%d-%H%M%S)"
  if [[ "$DRY_RUN" == "true" ]]; then
    info "[DRY-RUN] backup OpenClaw config: $OPENCLAW_CONFIG -> $BACKUP_PATH"
  else
    cp "$OPENCLAW_CONFIG" "$BACKUP_PATH"
    ok "OpenClaw config backup created: $BACKUP_PATH"
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    info "[DRY-RUN] patch OpenClaw hooks block in $OPENCLAW_CONFIG"
  else
  python3 - "$OPENCLAW_CONFIG" "$HOOK_TOKEN" "$OPENCLAW_HOOKS_PATH" "$OPENCLAW_ALLOW_REQUEST_SESSION_KEY" <<'PY'
import sys
from pathlib import Path

cfg_path = Path(sys.argv[1])
token = sys.argv[2]
hooks_path = sys.argv[3]
allow_req = sys.argv[4].lower() == "true"

new_hooks = (
    "hooks: {\n"
    "    enabled: true,\n"
    f"    token: \"{token}\",\n"
    f"    path: \"{hooks_path}\",\n"
    "    defaultSessionKey: \"hook:ingress\",\n"
    f"    allowRequestSessionKey: {'true' if allow_req else 'false'},\n"
    "    allowedSessionKeyPrefixes: [\"hook:\"],\n"
    "  }"
)

text = cfg_path.read_text(encoding="utf-8")

def skip_ws(i):
    while i < len(text) and text[i].isspace():
        i += 1
    return i

def skip_str(i):
    quote = text[i]
    i += 1
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == quote:
            return i + 1
        i += 1
    return i

def skip_line_comment(i):
    while i < len(text) and text[i] != "\n":
        i += 1
    return i

def skip_block_comment(i):
    i += 2
    while i + 1 < len(text):
        if text[i] == "*" and text[i + 1] == "/":
            return i + 2
        i += 1
    return i

def skip_value(i):
    i = skip_ws(i)
    if i >= len(text):
        return i
    if text[i] in ("'", '"'):
        return skip_str(i)
    if text[i] in "{[":
        open_c, close_c = text[i], ("}" if text[i] == "{" else "]")
        depth = 0
        while i < len(text):
            c = text[i]
            if c in ("'", '"'):
                i = skip_str(i)
                continue
            if c == "/" and i + 1 < len(text) and text[i + 1] == "/":
                i = skip_line_comment(i + 2)
                continue
            if c == "/" and i + 1 < len(text) and text[i + 1] == "*":
                i = skip_block_comment(i)
                continue
            if c == open_c:
                depth += 1
            elif c == close_c:
                depth -= 1
                if depth == 0:
                    return i + 1
            i += 1
        return i
    while i < len(text) and text[i] not in ",}\n":
        i += 1
    return i

def find_hooks_property():
    i = 0
    depth = 0
    while i < len(text):
        c = text[i]
        if c in ("'", '"'):
            i = skip_str(i)
            continue
        if c == "/" and i + 1 < len(text) and text[i + 1] == "/":
            i = skip_line_comment(i + 2)
            continue
        if c == "/" and i + 1 < len(text) and text[i + 1] == "*":
            i = skip_block_comment(i)
            continue
        if c == "{":
            depth += 1
            i += 1
            continue
        if c == "}":
            depth -= 1
            i += 1
            continue
        if depth == 1:
            j = skip_ws(i)
            if j < len(text) and text.startswith("hooks", j):
                k = j + 5
                k = skip_ws(k)
                if k < len(text) and text[k] == ":":
                    value_start = k + 1
                    value_end = skip_value(value_start)
                    end = value_end
                    end_ws = skip_ws(end)
                    if end_ws < len(text) and text[end_ws] == ",":
                        end = end_ws + 1
                    return j, end
        i += 1
    return None

span = find_hooks_property()
if span:
    start, end = span
    updated = text[:start] + new_hooks + "\n" + text[end:]
else:
    close_idx = text.rfind("}")
    if close_idx == -1:
        raise SystemExit("Could not find root object in OpenClaw config.")
    prefix = text[:close_idx].rstrip()
    if not prefix.endswith("{"):
        prefix += ",\n"
    updated = prefix + "  " + new_hooks + "\n}\n"

cfg_path.write_text(updated, encoding="utf-8")
print("OpenClaw hooks block updated.")
PY
  fi

  info "Restarting OpenClaw service: $OPENCLAW_SERVICE_NAME"
  if [[ "$OPENCLAW_SERVICE_NAME" == "auto" ]]; then
    if command -v openclaw >/dev/null 2>&1; then
      if [[ -n "${SUDO_USER:-}" ]]; then
        if [[ "$DRY_RUN" == "true" ]]; then
          info "[DRY-RUN] sudo -u $ACTING_USER openclaw gateway restart"
        else
          sudo -u "$ACTING_USER" openclaw gateway restart || true
        fi
      else
        run_cmd openclaw gateway restart || true
      fi
    fi
    if [[ -n "${SUDO_USER:-}" ]]; then
      if [[ "$DRY_RUN" == "true" ]]; then
        info "[DRY-RUN] sudo -u $ACTING_USER systemctl --user restart openclaw-gateway.service"
      else
        sudo -u "$ACTING_USER" systemctl --user restart openclaw-gateway.service || true
      fi
    else
      run_cmd systemctl --user restart openclaw-gateway.service || true
    fi
  else
    run_cmd systemctl restart "$OPENCLAW_SERVICE_NAME" || true
    if [[ -n "${SUDO_USER:-}" ]]; then
      if [[ "$DRY_RUN" == "true" ]]; then
        info "[DRY-RUN] sudo -u $ACTING_USER systemctl --user restart $OPENCLAW_SERVICE_NAME"
      else
        sudo -u "$ACTING_USER" systemctl --user restart "$OPENCLAW_SERVICE_NAME" || true
      fi
    else
      run_cmd systemctl --user restart "$OPENCLAW_SERVICE_NAME" || true
    fi
  fi
  if [[ "$DRY_RUN" != "true" ]]; then
    sleep 2
  fi
  if [[ "$OPENCLAW_SERVICE_NAME" == "auto" ]]; then
    if command -v openclaw >/dev/null 2>&1; then
      if [[ -n "${SUDO_USER:-}" ]]; then
        if [[ "$DRY_RUN" == "true" ]]; then
          info "[DRY-RUN] sudo -u $ACTING_USER openclaw gateway status --no-probe"
        else
          sudo -u "$ACTING_USER" openclaw gateway status --no-probe >/dev/null || true
        fi
      else
        run_cmd openclaw gateway status --no-probe >/dev/null || true
      fi
    fi
  else
    run_cmd systemctl status "$OPENCLAW_SERVICE_NAME" --no-pager >/dev/null || true
  fi

  info "Running OpenClaw hook smoke tests..."
  if [[ "$DRY_RUN" == "true" ]]; then
    info "[DRY-RUN] POST http://127.0.0.1:18789${OPENCLAW_HOOKS_PATH}/wake"
  else
    curl -fsS -X POST "http://127.0.0.1:18789${OPENCLAW_HOOKS_PATH}/wake" \
      -H "Authorization: Bearer $HOOK_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"text":"Graph webhook setup smoke test","mode":"now"}' >/dev/null
    ok "OpenClaw /hooks/wake check passed"
  fi
fi

echo "[Step 2] Running bootstrap script..."
DRY_RUN_ARG=()
if [[ "$DRY_RUN" == "true" ]]; then
  DRY_RUN_ARG+=(--dry-run)
fi
bash "$SETUP_SCRIPT" \
  --domain "$DOMAIN" \
  --hook-url "$HOOK_URL" \
  --hook-token "$HOOK_TOKEN" \
  --session-key "$SESSION_KEY" \
  --client-state "$CLIENT_STATE" \
  --repo-root "$REPO_ROOT" \
  "${DRY_RUN_ARG[@]}"

echo "[Step 3] Validating public HTTPS endpoint..."
VALIDATION_TOKEN="probe-$(date +%s)"
if [[ "$DRY_RUN" == "true" ]]; then
  info "[DRY-RUN] GET https://$DOMAIN$ADAPTER_PATH?validationToken=$VALIDATION_TOKEN"
else
  VALIDATION_URL="https://$DOMAIN$ADAPTER_PATH?validationToken=$VALIDATION_TOKEN"
  MAX_VALIDATION_ATTEMPTS=12
  VALIDATION_SLEEP_SECONDS=5
  VALIDATION_OK="false"
  CURL_ERR_FILE="$(mktemp)"

  for attempt in $(seq 1 "$MAX_VALIDATION_ATTEMPTS"); do
    if VALIDATION_RESULT="$(curl -fsS "$VALIDATION_URL" 2>"$CURL_ERR_FILE")"; then
      if [[ "$VALIDATION_RESULT" == "$VALIDATION_TOKEN" ]]; then
        VALIDATION_OK="true"
        break
      fi
      echo "[WARN] HTTPS validation attempt $attempt/$MAX_VALIDATION_ATTEMPTS returned unexpected body."
    else
      CURL_CODE="$?"
      CURL_ERR_MSG="$(tr '\n' ' ' <"$CURL_ERR_FILE")"
      echo "[WARN] HTTPS validation attempt $attempt/$MAX_VALIDATION_ATTEMPTS failed (curl=$CURL_CODE): $CURL_ERR_MSG"
    fi

    if [[ "$attempt" -lt "$MAX_VALIDATION_ATTEMPTS" ]]; then
      sleep "$VALIDATION_SLEEP_SECONDS"
    fi
  done

  rm -f "$CURL_ERR_FILE"

  if [[ "$VALIDATION_OK" != "true" ]]; then
    echo "[FAIL] HTTPS endpoint validation failed after $MAX_VALIDATION_ATTEMPTS attempts." >&2
    echo "[diag] systemctl status caddy --no-pager" >&2
    systemctl status caddy --no-pager || true
    if command -v ss >/dev/null 2>&1; then
      echo "[diag] ss -ltnp '( sport = :80 or sport = :443 )'" >&2
      ss -ltnp '( sport = :80 or sport = :443 )' || true
    fi
    echo "[diag] journalctl -u caddy -n 80 -l --no-pager" >&2
    journalctl -u caddy -n 80 -l --no-pager || true
    exit 1
  fi
fi
echo "Endpoint validation OK."

echo "[Step 4] Creating Graph subscription..."
if [[ "$DRY_RUN" == "true" ]]; then
  CREATE_JSON='{"id":"dry-run-subscription-id","dryRun":true}'
  SUBSCRIPTION_ID="dry-run-subscription-id"
  info "[DRY-RUN] python3 $SUB_SCRIPT create --notification-url https://$DOMAIN$ADAPTER_PATH --client-state <hidden> --minutes $MINUTES"
else
  CREATE_JSON="$(
    python3 "$SUB_SCRIPT" create \
      --notification-url "https://$DOMAIN$ADAPTER_PATH" \
      --client-state "$CLIENT_STATE" \
      --minutes "$MINUTES"
  )"
  echo "$CREATE_JSON"
  SUBSCRIPTION_ID="$(
    python3 - <<'PY' "$CREATE_JSON"
import json
import sys
body = json.loads(sys.argv[1])
print(body.get("id", ""))
PY
)"
fi

if [[ -z "$SUBSCRIPTION_ID" ]]; then
  echo "Could not parse subscription id from create response." >&2
  exit 1
fi
echo "Subscription created: $SUBSCRIPTION_ID"

echo "[Step 5] Persisting subscription id in $ENV_FILE..."
if [[ "$DRY_RUN" == "true" ]]; then
  info "[DRY-RUN] update GRAPH_MAIL_SUBSCRIPTION_ID in $ENV_FILE"
else
  if grep -q '^GRAPH_MAIL_SUBSCRIPTION_ID=' "$ENV_FILE"; then
    sed -i "s|^GRAPH_MAIL_SUBSCRIPTION_ID=.*$|GRAPH_MAIL_SUBSCRIPTION_ID=$SUBSCRIPTION_ID|" "$ENV_FILE"
  else
    printf "\nGRAPH_MAIL_SUBSCRIPTION_ID=%s\n" "$SUBSCRIPTION_ID" >> "$ENV_FILE"
  fi
fi

run_cmd systemctl daemon-reload
run_cmd systemctl restart graph-mail-webhook-adapter
run_cmd systemctl restart graph-mail-webhook-worker
run_cmd systemctl restart graph-mail-subscription-renew.service
run_cmd systemctl restart graph-mail-subscription-renew.timer

echo "Services restarted."

echo "[Step 6] Optional real email test..."
if [[ -n "$TEST_EMAIL" ]]; then
  TEST_SUBJECT="Graph Push E2E $(date +%Y%m%d-%H%M%S)"
  if [[ "$DRY_RUN" == "true" ]]; then
    info "[DRY-RUN] python3 $SEND_SCRIPT --to $TEST_EMAIL --subject \"$TEST_SUBJECT\" --body \"Graph webhook push end-to-end test.\""
  else
    python3 "$SEND_SCRIPT" --to "$TEST_EMAIL" --subject "$TEST_SUBJECT" --body "Graph webhook push end-to-end test."
    echo "Sent test email to: $TEST_EMAIL"
    echo "Subject: $TEST_SUBJECT"
  fi
else
  echo "Skipped (no --test-email provided)."
fi

echo
echo "Setup and validation completed. Summary:"
echo "- Domain: https://$DOMAIN$ADAPTER_PATH"
echo "- Client state: $CLIENT_STATE"
echo "- Subscription ID: $SUBSCRIPTION_ID"
echo "- Env file: $ENV_FILE"
if [[ "$CONFIGURE_OPENCLAW_HOOKS" == "true" ]]; then
  echo "- OpenClaw config: $OPENCLAW_CONFIG"
  echo "- OpenClaw service: $OPENCLAW_SERVICE_NAME"
fi
echo
echo "Useful checks:"
echo "  systemctl status graph-mail-webhook-adapter --no-pager"
echo "  systemctl status graph-mail-webhook-worker --no-pager"
echo "  systemctl status graph-mail-subscription-renew.timer --no-pager"
echo "  python3 \"$SUB_SCRIPT\" status --id \"$SUBSCRIPTION_ID\""
echo
echo "READINESS VERDICT:"
if [[ "$DRY_RUN" == "true" ]]; then
  echo "READY_FOR_PUSH: DRY_RUN (no live mutations or external API writes executed)"
elif [[ -n "$TEST_EMAIL" ]]; then
  echo "READY_FOR_PUSH: YES (public endpoint, subscription, services, and real email send tested)"
else
  echo "READY_FOR_PUSH: YES (public endpoint, subscription, and services validated)"
  echo "NOTE: add --test-email for full live delivery check."
fi
