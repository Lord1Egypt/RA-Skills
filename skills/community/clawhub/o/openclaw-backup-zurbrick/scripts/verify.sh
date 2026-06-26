#!/usr/bin/env bash
set -euo pipefail

MANIFEST_PATH=""
ARCHIVE_PATH=""
SECRETS_PATH=""

usage() {
  cat <<'EOF'
Usage: verify.sh --manifest /path/to/manifest.json --archive /path/to/openclaw-backup-YYYY-MM-DD.tar.gz [--secrets /path/to/openclaw-secrets-YYYY-MM-DD.tar.gz.age]

Validate manifest checksums and verify critical files exist inside the operational archive.
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
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [ -z "$ARCHIVE_PATH" ] && [ -f "$1" ] && [ "${1##*.}" = "gz" ]; then
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

python3 - "$MANIFEST_PATH" "$ARCHIVE_PATH" "$SECRETS_PATH" <<'PY'
import hashlib, json, os, sys
from pathlib import Path
manifest_path, archive_path, secrets_path = sys.argv[1:]
manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
errors = []

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

operational = manifest.get('archives', {}).get('operational', {})
if operational.get('file') != os.path.basename(archive_path):
    errors.append(f"Operational archive filename mismatch: manifest={operational.get('file')} actual={os.path.basename(archive_path)}")
if operational.get('sha256') != sha256(archive_path):
    errors.append('Operational archive checksum mismatch')
if int(operational.get('size') or 0) != os.path.getsize(archive_path):
    errors.append('Operational archive size mismatch')

secrets = manifest.get('archives', {}).get('secrets', {})
if secrets.get('file'):
    if not secrets.get('encrypted'):
        errors.append('Manifest says secrets archive exists but encrypted=false')
    if not secrets_path:
        errors.append('Secrets archive expected by manifest but --secrets was not provided')
    elif not os.path.exists(secrets_path):
        errors.append(f'Secrets archive not found: {secrets_path}')
    else:
        if os.path.basename(secrets_path) != secrets.get('file'):
            errors.append(f"Secrets archive filename mismatch: manifest={secrets.get('file')} actual={os.path.basename(secrets_path)}")
        if not secrets_path.endswith('.age'):
            errors.append('Secrets archive must be encrypted (.age)')
        if sha256(secrets_path) != secrets.get('sha256'):
            errors.append('Secrets archive checksum mismatch')
else:
    if secrets_path:
        errors.append('Secrets archive supplied, but manifest does not expect one')

if errors:
    for err in errors:
        print(f'ERROR: {err}', file=sys.stderr)
    sys.exit(1)
PY

TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/openclaw-verify.XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT

tar -xzf "$ARCHIVE_PATH" -C "$TMP_DIR"
ROOT="$TMP_DIR/openclaw"
[ -d "$ROOT" ] || die "Archive missing openclaw/ root"

STATUS=0
require_path() {
  rel="$1"
  if [ -e "$ROOT/$rel" ]; then
    info "OK: $rel"
  else
    warn "Missing: $rel"
    STATUS=1
  fi
}

require_path "workspace"
require_path "openclaw.json"
require_path "cron/jobs.json"

if [ "$STATUS" -eq 0 ]; then
  echo "VALID"
else
  echo "MISSING"
  exit 1
fi
