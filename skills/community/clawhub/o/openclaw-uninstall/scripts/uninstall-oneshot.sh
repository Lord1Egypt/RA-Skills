#!/usr/bin/env bash
# uninstall-oneshot.sh — Full OpenClaw uninstall. Run by one-shot or manually.
# Usage: uninstall-oneshot.sh [--notify-email EMAIL] [--notify-ntfy TOPIC]

set -e

LOG_FILE="/tmp/openclaw-uninstall.log"
NOTIFY_EMAIL=""
NOTIFY_NTFY=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --notify-email) NOTIFY_EMAIL="$2"; shift 2 ;;
    --notify-ntfy)  NOTIFY_NTFY="$2"; shift 2 ;;
    *) shift ;;
  esac
done

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

log "=== OpenClaw uninstall started ==="

# 1. Stop gateway (if CLI available)
if command -v openclaw &>/dev/null; then
  log "Stopping gateway..."
  openclaw gateway stop 2>/dev/null || true
  log "Uninstalling gateway service..."
  openclaw gateway uninstall 2>/dev/null || true
fi

# 2. Manual service removal (if CLI gone or as backup)
case "$(uname -s)" in
  Darwin)
    launchctl bootout "gui/$UID/ai.openclaw.gateway" 2>/dev/null || true
    rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
    for f in ~/Library/LaunchAgents/com.openclaw.*.plist; do
      [[ -f "$f" ]] && rm -f "$f"
    done
    ;;
  Linux)
    systemctl --user disable --now openclaw-gateway.service 2>/dev/null || true
    rm -f ~/.config/systemd/user/openclaw-gateway.service
    systemctl --user daemon-reload 2>/dev/null || true
    ;;
esac

# 3. Delete state dir
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
if [[ -d "$STATE_DIR" ]]; then
  log "Removing state dir: $STATE_DIR"
  rm -rf "$STATE_DIR"
fi

# 4. Delete profile dirs
for d in "$HOME"/.openclaw-*; do
  [[ -d "$d" ]] || continue
  log "Removing profile dir: $d"
  rm -rf "$d"
done

# 5. Remove CLI
for pm in npm pnpm bun; do
  if command -v "$pm" &>/dev/null; then
    if "$pm" list -g openclaw --depth=0 &>/dev/null 2>&1; then
      log "Removing npm package: $pm remove -g openclaw"
      "$pm" remove -g openclaw 2>/dev/null || true
      break
    fi
  fi
done

# 6. macOS app
if [[ "$(uname -s)" == "Darwin" ]] && [[ -d "/Applications/OpenClaw.app" ]]; then
  log "Removing macOS app"
  rm -rf /Applications/OpenClaw.app
fi

log "=== Uninstall complete ==="

# Notify
if [[ -n "$NOTIFY_EMAIL" ]]; then
  if command -v mail &>/dev/null; then
    echo "OpenClaw uninstalled. Details: $LOG_FILE" | mail -s "OpenClaw Uninstall Complete" "$NOTIFY_EMAIL" 2>/dev/null || log "Email send failed (mail unavailable)"
  else
    log "Email notification skipped (mail command unavailable)"
  fi
fi

if [[ -n "$NOTIFY_NTFY" ]]; then
  if command -v curl &>/dev/null; then
    curl -s -d "OpenClaw uninstalled" "https://ntfy.sh/$NOTIFY_NTFY" &>/dev/null || log "ntfy send failed"
  else
    log "ntfy notification skipped (curl unavailable)"
  fi
fi
