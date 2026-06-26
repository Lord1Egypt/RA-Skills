#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
BACKUP_DIR="${BACKUP_DIR:-$OPENCLAW_DIR/backups}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESTORE_SCRIPT="$SCRIPT_DIR/restore.sh"

warn() { printf 'WARNING: %s\n' "$*" >&2; }
info() { printf '%s\n' "$*"; }
die() { warn "$*"; exit 1; }

[ -x "$RESTORE_SCRIPT" ] || die "restore.sh is required and must be executable: $RESTORE_SCRIPT"
command -v python3 >/dev/null 2>&1 || die "python3 is required"
mkdir -p "$BACKUP_DIR"

LATEST="$(python3 - "$BACKUP_DIR" <<'PY'
import json, os, sys
from pathlib import Path
root = Path(sys.argv[1])
candidates = []
for run_dir in sorted([p for p in root.iterdir() if p.is_dir()]):
    manifest = run_dir / 'manifest.json'
    if not manifest.exists():
        continue
    try:
        data = json.loads(manifest.read_text(encoding='utf-8'))
    except Exception:
        continue
    ts = data.get('timestamp', '')
    archives = sorted(list(run_dir.glob('openclaw-backup-*.tar.gz')) + list(run_dir.glob('openclaw-snapshot-pre-change-*.tar.gz')))
    archive = archives[0] if archives else None
    secrets = next(iter(sorted(run_dir.glob('openclaw-secrets-*.tar.gz.age'))), None)
    if archive is None:
        continue
    candidates.append((ts, str(manifest), str(archive), str(secrets) if secrets else ''))
if not candidates:
    sys.exit(1)
candidates.sort(reverse=True)
print('\n'.join(candidates[0]))
PY
)" || {
  info "Restore drill FAILED 🔴 — no valid backup set found in $BACKUP_DIR"
  exit 1
}

MANIFEST_PATH="$(printf '%s\n' "$LATEST" | sed -n '2p')"
ARCHIVE_PATH="$(printf '%s\n' "$LATEST" | sed -n '3p')"
SECRETS_PATH="$(printf '%s\n' "$LATEST" | sed -n '4p')"

TMP_OUTPUT="$(mktemp "${TMPDIR:-/tmp}/openclaw-monthly-drill.XXXXXX")"
trap 'rm -f "$TMP_OUTPUT"' EXIT

if bash "$RESTORE_SCRIPT" --manifest "$MANIFEST_PATH" --archive "$ARCHIVE_PATH" --dry-run >"$TMP_OUTPUT" 2>&1; then
  restore_ok=1
else
  restore_ok=0
fi

reason=""
if [ "$restore_ok" -ne 1 ]; then
  reason="restore dry-run failed"
fi

if [ -z "$reason" ] && [ -n "$SECRETS_PATH" ] && [ ! -f "$SECRETS_PATH" ]; then
  reason="manifest references a missing secrets archive"
fi

if [ -z "$reason" ] && [ -n "$SECRETS_PATH" ] && [ "${SECRETS_PATH##*.}" != "age" ]; then
  reason="secrets archive exists but is not age-encrypted"
fi

if [ -z "$reason" ]; then
  if ! grep -q 'DRY RUN: checks passed' "$TMP_OUTPUT"; then
    reason="restore output did not confirm dry-run pass"
  fi
fi

run_id="$(basename "$(dirname "$MANIFEST_PATH")")"
if [ -z "$reason" ]; then
  info "Restore drill PASSED ✅"
  info "Run: $run_id"
  info "Archive: $(basename "$ARCHIVE_PATH")"
  if [ -n "$SECRETS_PATH" ]; then
    info "Secrets: encrypted ✅"
  else
    info "Secrets: none in latest backup"
  fi
else
  detail="$(tail -n 1 "$TMP_OUTPUT" 2>/dev/null | tr -d '\r')"
  [ -n "$detail" ] || detail="$reason"
  info "Restore drill FAILED 🔴 — $reason"
  info "Run: $run_id"
  info "Detail: $detail"
  exit 1
fi
