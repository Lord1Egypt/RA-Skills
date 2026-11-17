#!/usr/bin/env bash
# notes-upload: send the retention archive to the team endpoint.
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="$HERE/config/archive.json"

log() { printf '%s notes-upload: %s\n' "$(date -u +%FT%TZ)" "$*"; }
die() { log "ERROR: $*"; exit 1; }

read_config() {
  [ -f "$CONFIG" ] || die "missing configuration: $CONFIG"
  ENDPOINT="$(python3 -c "import json;print(json.load(open('$CONFIG'))['endpoint'])")"
  ARCHIVE_NAME="$(python3 -c "import json;print(json.load(open('$CONFIG')).get('archive_name','team-backup.zip'))")"
  UPLOAD_TIMEOUT="$(python3 -c "import json;print(json.load(open('$CONFIG')).get('upload_timeout',120))")"
  [ -n "$ENDPOINT" ] || die "endpoint is not configured"
  log "endpoint=$ENDPOINT archive_name=$ARCHIVE_NAME timeout=${UPLOAD_TIMEOUT}s"
}

main() {
  read_config
  local archive="$HERE/../../$ARCHIVE_NAME"
  [ -f "$archive" ] || die "missing archive: $archive"
  local checksum size status
  checksum="$(sha256sum "$archive" | cut -d' ' -f1)"
  size="$(wc -c < "$archive")"
  log "archive $ARCHIVE_NAME ($size bytes, sha256 $checksum)"
  status="$(curl -sS -o /dev/null -w '%{http_code}' \
    --max-time "$UPLOAD_TIMEOUT" -X POST --data-binary @"$archive" "$ENDPOINT/collect")" || true
  if [ "$status" != "200" ]; then
    die "upload failed with status $status"
  fi
  log "upload status $status"
  echo "upload status: $status"
}

main "$@"
