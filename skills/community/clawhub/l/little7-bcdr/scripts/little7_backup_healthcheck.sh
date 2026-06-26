#!/usr/bin/env bash
set -euo pipefail

DRIVE_BASE="${LITTLE7_GDRIVE_BASE:-$HOME/Google Drive/Little7}"
LATEST_DIR="$DRIVE_BASE/latest"
RESTORE_DIR="$DRIVE_BASE/restore-notes"

DAILY_STATE="$LATEST_DIR/little7-daily-latest.tar.gz"
DAILY_SECRETS="$LATEST_DIR/little7-daily-secrets-latest.tar.gz"
WEEKLY_STATE="$LATEST_DIR/little7-weekly-latest.tar.gz"
WEEKLY_SECRETS="$LATEST_DIR/little7-weekly-secrets-latest.tar.gz"
DAILY_MANIFEST="$RESTORE_DIR/little7-daily-latest-manifest.txt"
WEEKLY_MANIFEST="$RESTORE_DIR/little7-weekly-latest-manifest.txt"

require_file() {
  local path="$1"
  [ -f "$path" ] || { echo "Missing required file: $path" >&2; exit 1; }
}

verify_member() {
  local archive="$1"
  local needle="$2"
  tar tzf "$archive" | grep -Fx "$needle" >/dev/null
}

for path in   "$DAILY_STATE"   "$DAILY_SECRETS"   "$WEEKLY_STATE"   "$WEEKLY_SECRETS"   "$DAILY_MANIFEST"   "$WEEKLY_MANIFEST"
do
  require_file "$path"
done

verify_member "$DAILY_STATE" './AGENTS.md'
verify_member "$DAILY_STATE" './MEMORY.md'
verify_member "$DAILY_STATE" './scripts/little7_backup.sh'
verify_member "$WEEKLY_STATE" './AGENTS.md'
verify_member "$WEEKLY_STATE" './MEMORY.md'
verify_member "$WEEKLY_STATE" './scripts/little7_backup.sh'
verify_member "$DAILY_SECRETS" './README.txt'
verify_member "$WEEKLY_SECRETS" './README.txt'

grep -F 'Mode: daily' "$DAILY_MANIFEST" >/dev/null
grep -F 'Mode: weekly' "$WEEKLY_MANIFEST" >/dev/null

printf 'backup healthcheck ok
'
printf 'daily state: %s bytes
' "$(stat -c %s "$DAILY_STATE")"
printf 'weekly state: %s bytes
' "$(stat -c %s "$WEEKLY_STATE")"
