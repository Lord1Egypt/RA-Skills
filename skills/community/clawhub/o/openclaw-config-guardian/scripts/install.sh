#!/bin/bash
# config-guardian install.sh
# Installs OpenClaw Config Guardian v3.2
# Usage: bash scripts/install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

GUARDIAN_BIN="/usr/local/bin/openclaw-config-guardian"
SERVICE_FILE="/etc/systemd/system/openclaw-config-guardian.service"
CONFIG_DIR="/root/.openclaw"
BACKUP_DIR="$CONFIG_DIR/backups/config"

echo "[install] Installing OpenClaw Config Guardian v3.2..."

# ── 1. Check dependencies ─────────────────────────────────────────────────────
for dep in inotifywait jq sha256sum; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "[install] ❌ Missing dependency: $dep"
    echo "[install]    Run: apt-get install -y inotify-tools jq coreutils"
    exit 1
  fi
done
echo "[install] ✅ Dependencies OK"

# ── 2. Check openclaw.json exists ────────────────────────────────────────────
if [[ ! -f "$CONFIG_DIR/openclaw.json" ]]; then
  echo "[install] ❌ $CONFIG_DIR/openclaw.json not found. Deploy OpenClaw first."
  exit 1
fi
echo "[install] ✅ openclaw.json found"

# ── 3. Copy guardian script ───────────────────────────────────────────────────
cp "$SKILL_DIR/scripts/openclaw-config-guardian.sh" "$GUARDIAN_BIN"
chmod +x "$GUARDIAN_BIN"
echo "[install] ✅ Guardian script installed: $GUARDIAN_BIN"

# ── 4. Write systemd service ──────────────────────────────────────────────────
cat > "$SERVICE_FILE" <<'SERVICE'
[Unit]
Description=OpenClaw Configuration Guardian
After=network.target
Documentation=file:///root/.openclaw/common_assets/Library/config-guardian/OPERATION.md

[Service]
Type=simple
# Root required: monitors /root/.openclaw/openclaw.json, writes rollback files,
# and sends SIGUSR1 to OpenClaw gateway. No network access. Local-only operation.
User=root
Group=root
ExecStart=/usr/local/bin/openclaw-config-guardian
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw-config-guardian

[Install]
WantedBy=multi-user.target
SERVICE
echo "[install] ✅ systemd service written: $SERVICE_FILE"

# ── 5. Create backup directories ──────────────────────────────────────────────
mkdir -p \
  "$BACKUP_DIR" \
  "$BACKUP_DIR/attempts" \
  "$BACKUP_DIR/baseline_history"
touch "$BACKUP_DIR/guardian_audit.log"
echo "[install] ✅ Backup directories created: $BACKUP_DIR"

# ── 6. Initialize state file if missing ──────────────────────────────────────
if [[ ! -f "$BACKUP_DIR/.guardian_state.json" ]]; then
  cat > "$BACKUP_DIR/.guardian_state.json" <<'JSON'
{
  "attempts": 0,
  "last_error": null,
  "last_backup": null,
  "locked": false,
  "failed_at": null
}
JSON
  echo "[install] ✅ State file initialized"
fi

# ── 7. Generate self-check checksum ───────────────────────────────────────────
sha256sum "$GUARDIAN_BIN" > "$BACKUP_DIR/.guardian_checksum"
echo "[install] ✅ Self-check checksum generated:"
cat "$BACKUP_DIR/.guardian_checksum"

# ── 8. Enable and start service ───────────────────────────────────────────────
systemctl daemon-reload
systemctl enable --now openclaw-config-guardian
echo "[install] ✅ Service enabled and started"

# ── 9. Verify ────────────────────────────────────────────────────────────────
sleep 2
if systemctl is-active --quiet openclaw-config-guardian; then
  echo ""
  echo "[install] ✅ ✅ ✅  OpenClaw Config Guardian v3.2 installed successfully!"
  echo ""
  echo "  Status : $(systemctl is-active openclaw-config-guardian)"
  echo "  Logs   : journalctl -u openclaw-config-guardian -f"
  echo "  Unlock : openclaw-config-guardian unlock"
  echo "  State  : cat $BACKUP_DIR/.guardian_state.json"
else
  echo "[install] ❌ Service failed to start. Check: journalctl -u openclaw-config-guardian -n 30"
  exit 1
fi
