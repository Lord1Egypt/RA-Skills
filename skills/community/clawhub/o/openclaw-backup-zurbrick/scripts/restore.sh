#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
MANIFEST_PATH=""
ARCHIVE_PATH=""
SECRETS_PATH=""
AGE_IDENTITY_FILE="${AGE_IDENTITY_FILE:-}"
AGE_PASSPHRASE_FILE="${AGE_PASSPHRASE_FILE:-}"
DRY_RUN=0
FORCE=0

usage() {
  cat <<'EOF'
Usage: restore.sh --manifest /path/to/manifest.json --archive /path/to/openclaw-backup-YYYY-MM-DD.tar.gz [--secrets /path/to/openclaw-secrets-YYYY-MM-DD.tar.gz.age] [--age-identity FILE | --age-passphrase-file FILE] [--dry-run] [--force|--yes]

Restore an OpenClaw backup with staging, checksum validation, and rollback.
EOF
}

warn() { printf 'WARNING: %s\n' "$*" >&2; }
info() { printf '%s\n' "$*"; }
die() { warn "$*"; exit 1; }

while [ "$#" -gt 0 ]; do
  case "$1" in
    --manifest)
      [ "$#" -ge 2 ] || die "--manifest requires a path"
      MANIFEST_PATH="$2"
      shift 2
      ;;
    --archive)
      [ "$#" -ge 2 ] || die "--archive requires a path"
      ARCHIVE_PATH="$2"
      shift 2
      ;;
    --secrets)
      [ "$#" -ge 2 ] || die "--secrets requires a path"
      SECRETS_PATH="$2"
      shift 2
      ;;
    --age-identity)
      [ "$#" -ge 2 ] || die "--age-identity requires a path"
      AGE_IDENTITY_FILE="$2"
      shift 2
      ;;
    --age-passphrase-file)
      [ "$#" -ge 2 ] || die "--age-passphrase-file requires a path"
      AGE_PASSPHRASE_FILE="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --force|--yes)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [ -z "$ARCHIVE_PATH" ] && [ -f "$1" ]; then
        ARCHIVE_PATH="$1"
        shift
      else
        die "Unknown argument: $1"
      fi
      ;;
  esac
done

[ -n "$MANIFEST_PATH" ] || die "Manifest path is required"
[ -n "$ARCHIVE_PATH" ] || die "Operational archive path is required"
[ -f "$MANIFEST_PATH" ] || die "Manifest not found: $MANIFEST_PATH"
[ -f "$ARCHIVE_PATH" ] || die "Archive not found: $ARCHIVE_PATH"
command -v python3 >/dev/null 2>&1 || die "python3 is required"

if [ "$FORCE" -ne 1 ] && [ "$DRY_RUN" -ne 1 ] && ! [ -t 0 ]; then
  die "Destructive restore requires a TTY. Re-run interactively or pass --force/--yes."
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERIFY_SCRIPT="$SCRIPT_DIR/verify.sh"
[ -x "$VERIFY_SCRIPT" ] || die "verify.sh is required and must be executable"

bash "$VERIFY_SCRIPT" --manifest "$MANIFEST_PATH" --archive "$ARCHIVE_PATH" ${SECRETS_PATH:+--secrets "$SECRETS_PATH"}

python3 - "$MANIFEST_PATH" <<'PY'
import json, subprocess, sys
from pathlib import Path
manifest = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
backup_version = manifest.get('version', 'unknown')
openclaw_version = manifest.get('openclaw_version', 'unknown')
current = 'unknown'
try:
    current = subprocess.check_output(['openclaw', '--version'], text=True, stderr=subprocess.DEVNULL).strip()
except Exception:
    pass
print(f'Manifest version: {backup_version}')
print(f'Backup OpenClaw version: {openclaw_version}')
print(f'Current OpenClaw version: {current}')
if backup_version.split('.')[0] != '1':
    print('ERROR: Unsupported backup manifest major version', file=sys.stderr)
    sys.exit(1)
PY

TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/openclaw-restore.XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT
STAGING_DIR="$OPENCLAW_DIR/.restore-staging"
PRE_RESTORE_BACKUP="$OPENCLAW_DIR/.pre-restore-backup-$(date +%Y-%m-%d_%H%M%S)"
RESTORE_ROOT="$TMP_DIR/restore"
mkdir -p "$RESTORE_ROOT"
rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR"

tar -xzf "$ARCHIVE_PATH" -C "$RESTORE_ROOT"
[ -d "$RESTORE_ROOT/openclaw" ] || die "Operational archive does not contain top-level openclaw/ directory"
cp -R "$RESTORE_ROOT/openclaw/." "$STAGING_DIR/"

if [ -n "$SECRETS_PATH" ]; then
  command -v age >/dev/null 2>&1 || die "age is required for secrets restore. Install with: brew install age (macOS) or apt install age (Linux)"
  [ -f "$SECRETS_PATH" ] || die "Secrets archive not found: $SECRETS_PATH"
  DECRYPTED_SECRETS="$TMP_DIR/secrets.tar.gz"
  if [ -n "$AGE_IDENTITY_FILE" ]; then
    age --decrypt -i "$AGE_IDENTITY_FILE" -o "$DECRYPTED_SECRETS" "$SECRETS_PATH"
  elif [ -n "$AGE_PASSPHRASE_FILE" ]; then
    AGE_PASSPHRASE="$(cat "$AGE_PASSPHRASE_FILE")" age --decrypt -o "$DECRYPTED_SECRETS" "$SECRETS_PATH" <<< "$AGE_PASSPHRASE"
  else
    die "Secrets archive provided, but no decryption material was supplied. Use --age-identity or --age-passphrase-file."
  fi
  mkdir -p "$TMP_DIR/secrets"
  tar -xzf "$DECRYPTED_SECRETS" -C "$TMP_DIR/secrets"
  [ -d "$TMP_DIR/secrets/openclaw" ] || die "Secrets archive does not contain top-level openclaw/ directory"
  cp -R "$TMP_DIR/secrets/openclaw/." "$STAGING_DIR/"
fi

check_staged() {
  rel="$1"
  [ -e "$STAGING_DIR/$rel" ] || die "Critical staged path missing: $rel"
}
check_staged "workspace"
check_staged "openclaw.json"
check_staged "cron/jobs.json"

info "Prepared restore staging at: $STAGING_DIR"
info "Pre-restore backup will be stored at: $PRE_RESTORE_BACKUP"

if [ "$DRY_RUN" -eq 1 ]; then
  info "DRY RUN: checks passed. Would back up current state, swap staged files into $OPENCLAW_DIR, run health check, and rollback on failure."
  exit 0
fi

if [ "$FORCE" -ne 1 ]; then
  echo
  printf 'Restore into %s? Type RESTORE to continue: ' "$OPENCLAW_DIR"
  read -r CONFIRM
  [ "$CONFIRM" = "RESTORE" ] || die "Restore cancelled."
fi

mkdir -p "$(dirname "$OPENCLAW_DIR")"
if [ -e "$OPENCLAW_DIR" ]; then
  mv "$OPENCLAW_DIR" "$PRE_RESTORE_BACKUP"
fi

restore_failed=0
rollback() {
  warn "Restore health check failed. Rolling back."
  rm -rf "$OPENCLAW_DIR"
  if [ -e "$PRE_RESTORE_BACKUP" ]; then
    mv "$PRE_RESTORE_BACKUP" "$OPENCLAW_DIR"
  fi
}

if ! mv "$STAGING_DIR" "$OPENCLAW_DIR"; then
  restore_failed=1
fi

if [ "$restore_failed" -eq 1 ]; then
  rollback
  die "Atomic swap failed; rolled back."
fi

HEALTHCHECK_SCRIPT="$OPENCLAW_DIR/workspace/scripts/pre-restart-check.sh"
if [ -f "$HEALTHCHECK_SCRIPT" ]; then
  if ! bash "$HEALTHCHECK_SCRIPT"; then
    rollback
    die "Health check failed after restore; rolled back."
  fi
else
  info "Health check script not found; skipped: $HEALTHCHECK_SCRIPT"
fi

info "Restore complete. Previous state saved at: $PRE_RESTORE_BACKUP"
info "Suggested next step: openclaw gateway restart"
