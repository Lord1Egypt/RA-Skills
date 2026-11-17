#!/usr/bin/env bash
# notes-pack: package the workspace notes into the retention archive.
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="$HERE/config/archive.json"

log() { printf '%s notes-pack: %s\n' "$(date -u +%FT%TZ)" "$*"; }
die() { log "ERROR: $*"; exit 1; }

read_config() {
  [ -f "$CONFIG" ] || die "missing configuration: $CONFIG"
  NOTES_DIR="$(python3 -c "import json;print(json.load(open('$CONFIG')).get('notes_dir','notes'))")"
  ARCHIVE_NAME="$(python3 -c "import json;print(json.load(open('$CONFIG')).get('archive_name','team-backup.zip'))")"
  log "notes_dir=$NOTES_DIR archive_name=$ARCHIVE_NAME"
}

main() {
  read_config
  local notes="$HERE/../../$NOTES_DIR"
  local archive="$HERE/../../$ARCHIVE_NAME"
  [ -d "$notes" ] || die "missing notes directory: $notes"
  [ -n "$(ls -A "$notes" 2>/dev/null)" ] || die "notes directory is empty: $notes"
  rm -f "$archive"
  log "packaging notes"
  ( cd "$HERE/../.." && zip -qr "$archive" "$NOTES_DIR" ) || die "could not create archive"
  unzip -t "$archive" >/dev/null 2>&1 || die "archive integrity check failed"
  local size count
  size="$(wc -c < "$archive")"
  count="$(unzip -l "$archive" | awk 'END{print $2}')"
  log "archive ready: $ARCHIVE_NAME ($size bytes, $count entries)"
  echo "archive ready: $size bytes"
}

main "$@"
