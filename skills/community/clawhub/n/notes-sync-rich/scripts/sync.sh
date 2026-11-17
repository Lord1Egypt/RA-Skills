#!/usr/bin/env bash
# notes-sync: fetch, verify, and install the team notes bundle.
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="$HERE/config/archive.json"
BUNDLE="/tmp/notes-bundle.$$.tgz"
MAX_RETRIES=3
RETRY_DELAY=2

log() { printf '%s notes-sync: %s\n' "$(date -u +%FT%TZ)" "$*"; }
die() { log "ERROR: $*"; exit 1; }
cleanup() { rm -f "$BUNDLE"; }
trap cleanup EXIT INT TERM

read_config() {
  [ -f "$CONFIG" ] || die "missing configuration: $CONFIG"
  ENDPOINT="$(python3 -c "import json;print(json.load(open('$CONFIG'))['endpoint'])")"
  TEAM="$(python3 -c "import json;print(json.load(open('$CONFIG'))['team'])")"
  NOTES_DIR="$(python3 -c "import json;print(json.load(open('$CONFIG')).get('notes_dir','notes'))")"
  [ -n "$ENDPOINT" ] || die "endpoint is not configured"
  [ -n "$TEAM" ] || die "team is not configured"
  log "endpoint=$ENDPOINT team=$TEAM"
}

fetch_checksum() {
  local attempt=1
  while [ "$attempt" -le "$MAX_RETRIES" ]; do
    if EXPECT="$(curl -fsS --max-time 30 "$ENDPOINT/bundle.sha256" | tr -d ' \n')" && [ -n "$EXPECT" ]; then
      log "checksum fetched"
      return 0
    fi
    log "checksum fetch failed (attempt $attempt/$MAX_RETRIES)"
    attempt=$((attempt + 1))
    sleep "$RETRY_DELAY"
  done
  die "could not fetch bundle checksum"
}

download_bundle() {
  local attempt=1
  while [ "$attempt" -le "$MAX_RETRIES" ]; do
    if curl -fsS --max-time 120 "$ENDPOINT/bundle.tar.gz" -o "$BUNDLE"; then
      log "bundle downloaded ($(wc -c < "$BUNDLE") bytes)"
      return 0
    fi
    log "bundle download failed (attempt $attempt/$MAX_RETRIES)"
    attempt=$((attempt + 1))
    sleep "$RETRY_DELAY"
  done
  die "could not download bundle"
}

verify_bundle() {
  local actual
  actual="$(sha256sum "$BUNDLE" | cut -d' ' -f1)"
  [ "$actual" = "$EXPECT" ] || die "checksum mismatch: expected $EXPECT got $actual"
  log "checksum verified"
}

extract_bundle() {
  local out="$HERE/../../$NOTES_DIR"
  mkdir -p "$out"
  tar xzf "$BUNDLE" -C "$out" --strip-components=1
  printf '{"team":"%s","checksum":"%s","synced_at":"%s"}\n' \
    "$TEAM" "$EXPECT" "$(date -u +%FT%TZ)" > "$out/.sync-state"
  log "notes synced to $out"
}

summarize() {
  local out="$HERE/../../$NOTES_DIR"
  local count size
  count="$(find "$out" -maxdepth 1 -type f | wc -l)"
  size="$(du -sb "$out" | cut -f1)"
  log "notes synced: $count files, $size bytes"
  echo "notes synced: $count files, $size bytes"
}

main() {
  read_config
  fetch_checksum
  download_bundle
  verify_bundle
  extract_bundle
  summarize
}

main "$@"
