#!/usr/bin/env bash
# Pre-install checks for inference-optimizer.
# Creates timestamped backups, runs audit, and runs setup preview.
# Optional: pass --apply-setup to run setup --apply after preview.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
WORKSPACE_MAIN="${WORKSPACE_MAIN:-$HOME/clawd}"
WORKSPACE_WHATSAPP="${WORKSPACE_WHATSAPP:-$HOME/.openclaw/workspace-whatsapp}"

BACKUP_BASE="${OPENCLAW_PREFLIGHT_BACKUP_BASE:-$HOME/openclaw-preflight-backup}"
RUN_ID="$(date +%Y-%m-%d-%H%M%S)"
RUN_DIR="$BACKUP_BASE/$RUN_ID"

APPLY_SETUP=false
[[ "${1:-}" = "--apply-setup" ]] && APPLY_SETUP=true

mkdir -p "$RUN_DIR"

backup_dir() {
  local source_dir="$1"
  local archive_name="$2"

  if [[ -d "$source_dir" ]]; then
    tar -czf "$RUN_DIR/$archive_name.tar.gz" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"
    echo "[OK] Backup: $RUN_DIR/$archive_name.tar.gz"
  else
    echo "[SKIP] Missing directory: $source_dir"
  fi
}

echo "=== inference-optimizer preflight ==="
echo "Run directory: $RUN_DIR"
echo ""

echo "=== Backups ==="
backup_dir "$OPENCLAW_DIR" "openclaw-home"
backup_dir "$WORKSPACE_MAIN" "workspace-clawd"
backup_dir "$WORKSPACE_WHATSAPP" "workspace-whatsapp"

echo ""
echo "=== Audit ==="
AUDIT_LOG="$RUN_DIR/audit.txt"
"$SKILL_DIR/scripts/openclaw-audit.sh" | tee "$AUDIT_LOG"
echo "[OK] Audit log: $AUDIT_LOG"

echo ""
echo "=== Setup preview ==="
SETUP_PREVIEW_LOG="$RUN_DIR/setup-preview.txt"
bash "$SKILL_DIR/scripts/setup.sh" | tee "$SETUP_PREVIEW_LOG"
echo "[OK] Setup preview log: $SETUP_PREVIEW_LOG"

if [[ "$APPLY_SETUP" = true ]]; then
  echo ""
  echo "=== Setup apply ==="
  SETUP_APPLY_LOG="$RUN_DIR/setup-apply.txt"
  bash "$SKILL_DIR/scripts/setup.sh" --apply | tee "$SETUP_APPLY_LOG"
  echo "[OK] Setup apply log: $SETUP_APPLY_LOG"
fi

echo ""
echo "=== Verification ==="
VERIFY_LOG="$RUN_DIR/verify.txt"
if bash "$SKILL_DIR/scripts/verify.sh" | tee "$VERIFY_LOG"; then
  echo "[OK] Verify log: $VERIFY_LOG"
else
  echo "[WARN] Verify reported issues: $VERIFY_LOG"
fi

echo ""
echo "=== Next ==="
echo "1) Review backup archives under: $RUN_DIR"
echo "2) Review logs: audit.txt, setup-preview.txt, and verify.txt"
echo "3) If verify reports legacy paths or stale workspace wiring, run setup.sh --apply from the installed skill path"
echo "4) If setup was not applied, run preflight with --apply-setup or run setup.sh --apply after review"
echo "5) For purge, use approval flow and run purge script without --delete unless immediate removal is intended"
