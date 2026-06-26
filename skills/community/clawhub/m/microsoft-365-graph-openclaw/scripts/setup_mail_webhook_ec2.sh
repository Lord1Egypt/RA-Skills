#!/usr/bin/env bash
set -eu
set -o pipefail 2>/dev/null || true

# Bootstrap Graph webhook adapter stack on Ubuntu/Debian EC2:
# - Install Caddy
# - Configure reverse proxy for <DOMAIN> -> local adapter
# - Create systemd units for adapter + worker
# - Configure subscription renew timer
#
# Manual prerequisites (not automated):
# - DNS A record pointing DOMAIN to EC2 public IP
# - Inbound 80/443 opened in security group
# - Graph app permissions/consent and OAuth login already completed

usage() {
  cat <<'EOF'
Usage:
  setup_mail_webhook_ec2.sh \
    --domain graphhook.example.com \
    --hook-url http://127.0.0.1:18789/hooks/wake \
    --hook-token SECRET \
    [--session-key hook:graph-mail] \
    --client-state SUPER_SECRET \
    [--repo-root /opt/microsoft-365-graph-openclaw] \
    [--python /usr/bin/python3] \
    [--adapter-port 8789] \
    [--adapter-path /graph/mail] \
    [--renew-minutes 30] \
    [--dry-run]

Notes:
  - Must run as root (or with sudo).
  - Assumes adapter scripts are available under:
      <repo-root>/scripts/
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
warn() { echo "[WARN] $1"; }
run_cmd() {
  if [[ "$DRY_RUN" == "true" ]]; then
    info "[DRY-RUN] $*"
    return 0
  fi
  "$@"
}

DOMAIN=""
HOOK_URL=""
HOOK_TOKEN=""
SESSION_KEY="hook:graph-mail"
CLIENT_STATE=""
REPO_ROOT="$(pwd)"
PYTHON_BIN="/usr/bin/python3"
ADAPTER_PORT="8789"
ADAPTER_PATH="/graph/mail"
RENEW_MINUTES="30"
DRY_RUN="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="$2"; shift 2 ;;
    --hook-url) HOOK_URL="$2"; shift 2 ;;
    --hook-token) HOOK_TOKEN="$2"; shift 2 ;;
    --session-key) SESSION_KEY="$2"; shift 2 ;;
    --client-state) CLIENT_STATE="$2"; shift 2 ;;
    --repo-root) REPO_ROOT="$2"; shift 2 ;;
    --python) PYTHON_BIN="$2"; shift 2 ;;
    --adapter-port) ADAPTER_PORT="$2"; shift 2 ;;
    --adapter-path) ADAPTER_PATH="$2"; shift 2 ;;
    --renew-minutes) RENEW_MINUTES="$2"; shift 2 ;;
    --dry-run) DRY_RUN="true"; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$DOMAIN" || -z "$HOOK_URL" || -z "$HOOK_TOKEN" || -z "$CLIENT_STATE" ]]; then
  echo "Missing required arguments." >&2
  usage
  exit 1
fi

if [[ "$DRY_RUN" != "true" && "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "Run as root (sudo)." >&2
  exit 1
fi

if [[ "$DRY_RUN" == "true" ]]; then
  info "Dry-run mode enabled: no system changes will be applied."
else
  require_cmd apt-get
  require_cmd systemctl
  require_cmd tee
fi

SCRIPTS_DIR="$REPO_ROOT/scripts"
ADAPTER_SCRIPT="$SCRIPTS_DIR/mail_webhook_adapter.py"
WORKER_SCRIPT="$SCRIPTS_DIR/mail_webhook_worker.py"
SUB_SCRIPT="$SCRIPTS_DIR/mail_subscriptions.py"
ENV_FILE="/etc/default/graph-mail-webhook"

for file in "$ADAPTER_SCRIPT" "$WORKER_SCRIPT" "$SUB_SCRIPT"; do
  [[ -f "$file" ]] || { echo "File not found: $file" >&2; exit 1; }
done

echo "[1/7] Installing dependencies..."
run_cmd apt-get update -y
run_cmd apt-get install -y python3 python3-pip curl gnupg debian-keyring debian-archive-keyring apt-transport-https
ok "Dependencies installed"

if [[ "$DRY_RUN" == "true" ]] || ! command -v caddy >/dev/null 2>&1; then
  echo "[2/7] Installing Caddy..."
  if [[ "$DRY_RUN" == "true" ]]; then
    info "[DRY-RUN] install Caddy and apt repo configuration"
  else
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list >/dev/null
    apt-get update -y
    apt-get install -y caddy
  fi
else
  echo "[2/7] Caddy already installed."
fi
ok "Caddy available"

echo "[3/7] Writing environment file: $ENV_FILE"
if [[ "$DRY_RUN" == "true" ]]; then
  info "[DRY-RUN] write $ENV_FILE"
else
cat > "$ENV_FILE" <<EOF
GRAPH_WEBHOOK_CLIENT_STATE=$CLIENT_STATE
OPENCLAW_HOOK_URL=$HOOK_URL
OPENCLAW_HOOK_TOKEN=$HOOK_TOKEN
OPENCLAW_SESSION_KEY=$SESSION_KEY
GRAPH_WEBHOOK_ADAPTER_PORT=$ADAPTER_PORT
GRAPH_WEBHOOK_ADAPTER_PATH=$ADAPTER_PATH
EOF
chmod 600 "$ENV_FILE"
fi
ok "Environment file written"

echo "[4/7] Configuring Caddy reverse proxy for $DOMAIN"
if [[ "$DRY_RUN" == "true" ]]; then
  info "[DRY-RUN] write /etc/caddy/Caddyfile"
  info "[DRY-RUN] caddy validate --config /etc/caddy/Caddyfile"
  info "[DRY-RUN] systemctl restart caddy"
else
cat > /etc/caddy/Caddyfile <<EOF
https://$DOMAIN {
    reverse_proxy 127.0.0.1:$ADAPTER_PORT
}

http://$DOMAIN {
    redir https://$DOMAIN{uri} 308
}
EOF
  caddy validate --config /etc/caddy/Caddyfile
  systemctl restart caddy
fi
ok "Caddyfile configured for $DOMAIN"

echo "[5/7] Creating systemd service: graph-mail-webhook-adapter"
if [[ "$DRY_RUN" == "true" ]]; then
  info "[DRY-RUN] write /etc/systemd/system/graph-mail-webhook-adapter.service"
else
cat > /etc/systemd/system/graph-mail-webhook-adapter.service <<EOF
[Unit]
Description=Graph Mail Webhook Adapter
After=network.target

[Service]
Type=simple
EnvironmentFile=$ENV_FILE
WorkingDirectory=$REPO_ROOT
ExecStart=$PYTHON_BIN $ADAPTER_SCRIPT serve --host 127.0.0.1 --port \${GRAPH_WEBHOOK_ADAPTER_PORT} --path \${GRAPH_WEBHOOK_ADAPTER_PATH} --client-state \${GRAPH_WEBHOOK_CLIENT_STATE}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
fi
ok "Adapter systemd service created"

echo "[6/7] Creating systemd service: graph-mail-webhook-worker"
if [[ "$DRY_RUN" == "true" ]]; then
  info "[DRY-RUN] write /etc/systemd/system/graph-mail-webhook-worker.service"
else
cat > /etc/systemd/system/graph-mail-webhook-worker.service <<EOF
[Unit]
Description=Graph Mail Webhook Worker
After=network.target

[Service]
Type=simple
EnvironmentFile=$ENV_FILE
WorkingDirectory=$REPO_ROOT
ExecStart=$PYTHON_BIN $WORKER_SCRIPT loop --session-key \${OPENCLAW_SESSION_KEY} --hook-url \${OPENCLAW_HOOK_URL} --hook-token \${OPENCLAW_HOOK_TOKEN}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
fi
ok "Worker systemd service created"

echo "[7/7] Creating renew timer..."
if [[ "$DRY_RUN" == "true" ]]; then
  info "[DRY-RUN] write /etc/systemd/system/graph-mail-subscription-renew.service"
  info "[DRY-RUN] write /etc/systemd/system/graph-mail-subscription-renew.timer"
else
cat > /etc/systemd/system/graph-mail-subscription-renew.service <<EOF
[Unit]
Description=Renew Graph Mail Subscription (manual id required)

[Service]
Type=oneshot
EnvironmentFile=$ENV_FILE
WorkingDirectory=$REPO_ROOT
ExecStart=/bin/bash -lc 'if [[ -z "\${GRAPH_MAIL_SUBSCRIPTION_ID:-}" ]]; then echo "Set GRAPH_MAIL_SUBSCRIPTION_ID in /etc/default/graph-mail-webhook"; exit 1; fi; $PYTHON_BIN $SUB_SCRIPT renew --id "\${GRAPH_MAIL_SUBSCRIPTION_ID}" --minutes 4200'
EOF

cat > /etc/systemd/system/graph-mail-subscription-renew.timer <<EOF
[Unit]
Description=Run Graph Mail Subscription renew job

[Timer]
OnBootSec=10m
OnUnitActiveSec=${RENEW_MINUTES}m
Unit=graph-mail-subscription-renew.service
Persistent=true

[Install]
WantedBy=timers.target
EOF
fi
ok "Renew timer/service created"

run_cmd systemctl daemon-reload
run_cmd systemctl enable caddy
run_cmd systemctl enable --now graph-mail-webhook-adapter
run_cmd systemctl enable --now graph-mail-webhook-worker
run_cmd systemctl enable --now graph-mail-subscription-renew.timer

echo "[verify] Checking runtime status..."
if [[ "$DRY_RUN" == "true" ]]; then
  info "[DRY-RUN] skip runtime service status checks"
else
  if systemctl is-active --quiet caddy; then
    ok "caddy is active"
  else
    echo "[FAIL] caddy is not active"
    exit 1
  fi
  if ss -ltn '( sport = :443 )' | grep -q ':443'; then
    ok "caddy is listening on :443"
  else
    echo "[FAIL] caddy is not listening on :443"
    exit 1
  fi
  if systemctl is-active --quiet graph-mail-webhook-adapter; then
    ok "graph-mail-webhook-adapter is active"
  else
    echo "[FAIL] graph-mail-webhook-adapter is not active"
    exit 1
  fi
  if systemctl is-active --quiet graph-mail-webhook-worker; then
    ok "graph-mail-webhook-worker is active"
  else
    echo "[FAIL] graph-mail-webhook-worker is not active"
    exit 1
  fi
  if systemctl is-active --quiet graph-mail-subscription-renew.timer; then
    ok "graph-mail-subscription-renew.timer is active"
  else
    echo "[FAIL] graph-mail-subscription-renew.timer is not active"
    exit 1
  fi
fi

if [[ "$DRY_RUN" == "true" ]]; then
  info "[DRY-RUN] skip local adapter probe"
else
  LOCAL_PROBE="$(curl -fsS "http://127.0.0.1:${ADAPTER_PORT}${ADAPTER_PATH}?validationToken=probe-local")"
  if [[ "$LOCAL_PROBE" == "probe-local" ]]; then
    ok "local adapter handshake works"
  else
    echo "[FAIL] local adapter handshake failed"
    exit 1
  fi
fi

echo
echo "Setup completed successfully."
echo
info "Readiness status:"
if [[ "$DRY_RUN" == "true" ]]; then
  warn "dry-run mode: readiness is not evaluated against live system state"
  echo "PUSH_READINESS: DRY_RUN (no system changes applied)"
elif grep -q '^GRAPH_MAIL_SUBSCRIPTION_ID=' "$ENV_FILE"; then
  ok "service stack configured and subscription id present"
  echo "PUSH_READINESS: READY (subscription id set)"
else
  warn "service stack configured, but GRAPH_MAIL_SUBSCRIPTION_ID is not set yet"
  echo "PUSH_READINESS: PARTIAL (create subscription to finish)"
fi
echo
echo "Next steps:"
echo "1) Verify public HTTPS endpoint:"
echo "   curl \"https://$DOMAIN$ADAPTER_PATH?validationToken=abc123\""
echo "2) Create subscription and copy returned id:"
echo "   $PYTHON_BIN $SUB_SCRIPT create --notification-url https://$DOMAIN$ADAPTER_PATH --client-state '$CLIENT_STATE' --minutes 4200"
echo "3) Add GRAPH_MAIL_SUBSCRIPTION_ID=<id> to $ENV_FILE and restart renew service:"
echo "   systemctl restart graph-mail-subscription-renew.service"
