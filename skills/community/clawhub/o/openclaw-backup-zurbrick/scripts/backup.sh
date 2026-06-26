#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
BACKUP_DIR="${BACKUP_DIR:-$OPENCLAW_DIR/backups}"
DATE_STAMP="$(date +%Y-%m-%d)"
TIMESTAMP_ISO="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_ID="$(date +%Y-%m-%d_%H%M%S)"
RUN_DIR="$BACKUP_DIR/$RUN_ID"
OP_ARCHIVE="$RUN_DIR/openclaw-backup-$DATE_STAMP.tar.gz"
SECRETS_ARCHIVE="$RUN_DIR/openclaw-secrets-$DATE_STAMP.tar.gz"
SECRETS_ENCRYPTED="$SECRETS_ARCHIVE.age"
MANIFEST_PATH="$RUN_DIR/manifest.json"
INCLUDE_SECRETS=0
AGE_RECIPIENT="${AGE_RECIPIENT:-}"
AGE_PASSPHRASE_FILE="${AGE_PASSPHRASE_FILE:-}"

usage() {
  cat <<'EOF'
Usage: backup.sh [--include-secrets] [--no-secrets] [--output-dir /path/to/backups] [--age-recipient KEY] [--age-passphrase-file FILE]

Create a timestamped OpenClaw backup set.

Default behavior:
  - creates an operational archive only
  - secrets are excluded unless explicitly enabled

Options:
  --include-secrets          Create encrypted secrets archive (.tar.gz.age)
  --no-secrets               Force operational-only backup (default)
  --output-dir <dir>         Override backup root directory
  --age-recipient <key>      age recipient public key for secrets encryption
  --age-passphrase-file <f>  Read age passphrase from file for symmetric encryption
  -h, --help                 Show this help

Env alternatives:
  AGE_RECIPIENT=<age public key>
  AGE_PASSPHRASE_FILE=/path/to/passphrase.txt
EOF
}

warn() { printf 'WARNING: %s\n' "$*" >&2; }
info() { printf '%s\n' "$*"; }
die() { warn "$*"; exit 1; }

while [ "$#" -gt 0 ]; do
  case "$1" in
    --include-secrets)
      INCLUDE_SECRETS=1
      shift
      ;;
    --no-secrets)
      INCLUDE_SECRETS=0
      shift
      ;;
    --output-dir)
      [ "$#" -ge 2 ] || die "--output-dir requires a path"
      BACKUP_DIR="$2"
      RUN_DIR="$BACKUP_DIR/$RUN_ID"
      OP_ARCHIVE="$RUN_DIR/openclaw-backup-$DATE_STAMP.tar.gz"
      SECRETS_ARCHIVE="$RUN_DIR/openclaw-secrets-$DATE_STAMP.tar.gz"
      SECRETS_ENCRYPTED="$SECRETS_ARCHIVE.age"
      MANIFEST_PATH="$RUN_DIR/manifest.json"
      shift 2
      ;;
    --age-recipient)
      [ "$#" -ge 2 ] || die "--age-recipient requires a key"
      AGE_RECIPIENT="$2"
      shift 2
      ;;
    --age-passphrase-file)
      [ "$#" -ge 2 ] || die "--age-passphrase-file requires a path"
      AGE_PASSPHRASE_FILE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "Unknown argument: $1"
      ;;
  esac
done

command -v tar >/dev/null 2>&1 || die "tar is required"
command -v python3 >/dev/null 2>&1 || die "python3 is required"

if [ "$INCLUDE_SECRETS" -eq 1 ]; then
  command -v age >/dev/null 2>&1 || die "age is required for secrets backups. Install with: brew install age (macOS) or apt install age (Linux)"
  if [ -z "$AGE_RECIPIENT" ] && [ -z "$AGE_PASSPHRASE_FILE" ]; then
    die "Secrets backup requested, but no age key/passphrase configured. Set AGE_RECIPIENT, AGE_PASSPHRASE_FILE, or pass --age-recipient/--age-passphrase-file."
  fi
  if [ -n "$AGE_PASSPHRASE_FILE" ] && [ ! -f "$AGE_PASSPHRASE_FILE" ]; then
    die "Passphrase file not found: $AGE_PASSPHRASE_FILE"
  fi
fi

mkdir -p "$RUN_DIR"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/openclaw-backup-stage.XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT

OP_STAGE="$TMP_DIR/openclaw-operational"
SEC_STAGE="$TMP_DIR/openclaw-secrets"
mkdir -p "$OP_STAGE/openclaw/cron" "$SEC_STAGE/openclaw/agents"

FILES_INCLUDED_JSON="$TMP_DIR/files_included.json"
printf '[]' > "$FILES_INCLUDED_JSON"

record_file() {
  python3 - "$FILES_INCLUDED_JSON" "$1" <<'PY'
import json, sys
path, item = sys.argv[1], sys.argv[2]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
if item not in data:
    data.append(item)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f)
PY
}

copy_dir() {
  src="$1"
  dest="$2"
  label="$3"
  if [ -d "$src" ]; then
    mkdir -p "$(dirname "$dest")"
    cp -R "$src" "$dest"
    record_file "$label"
    info "Added: $label"
  else
    warn "Missing directory, skipped: $src"
  fi
}

copy_file() {
  src="$1"
  dest="$2"
  label="$3"
  if [ -f "$src" ]; then
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
    record_file "$label"
    info "Added: $label"
  else
    warn "Missing file, skipped: $src"
  fi
}

redact_openclaw_json() {
  src="$1"
  dest="$2"
  python3 - "$src" "$dest" <<'PY'
import json, sys
from pathlib import Path
src, dest = Path(sys.argv[1]), Path(sys.argv[2])
secret_words = ('token', 'secret', 'password', 'key', 'auth', 'cookie', 'session', 'credential', 'bearer')

def redact(value, key_name=''):
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            lowered = k.lower()
            if any(word in lowered for word in secret_words):
                out[k] = '[REDACTED]'
            else:
                out[k] = redact(v, k)
        return out
    if isinstance(value, list):
        return [redact(v, key_name) for v in value]
    if isinstance(value, str) and any(word in key_name.lower() for word in secret_words):
        return '[REDACTED]'
    return value

data = json.loads(src.read_text(encoding='utf-8'))
dest.write_text(json.dumps(redact(data), indent=2, sort_keys=True) + '\n', encoding='utf-8')
PY
}

copy_dir "$OPENCLAW_DIR/workspace" "$OP_STAGE/openclaw/workspace" "workspace/"
if [ -f "$OPENCLAW_DIR/openclaw.json" ]; then
  mkdir -p "$OP_STAGE/openclaw"
  redact_openclaw_json "$OPENCLAW_DIR/openclaw.json" "$OP_STAGE/openclaw/openclaw.json"
  record_file "openclaw.json (redacted)"
  info "Added: openclaw.json (redacted)"
else
  warn "Missing file, skipped: $OPENCLAW_DIR/openclaw.json"
fi
copy_file "$OPENCLAW_DIR/cron/jobs.json" "$OP_STAGE/openclaw/cron/jobs.json" "cron/jobs.json"

if [ "$INCLUDE_SECRETS" -eq 1 ]; then
  copy_file "$OPENCLAW_DIR/.env" "$SEC_STAGE/openclaw/.env" ".env"
  copy_dir "$OPENCLAW_DIR/agents" "$SEC_STAGE/openclaw/agents" "agents/"
fi

[ -d "$OP_STAGE/openclaw/workspace" ] || [ -f "$OP_STAGE/openclaw/openclaw.json" ] || [ -f "$OP_STAGE/openclaw/cron/jobs.json" ] || die "Nothing was staged for operational backup."

(
  cd "$OP_STAGE"
  tar -czf "$OP_ARCHIVE" openclaw
)

if [ "$INCLUDE_SECRETS" -eq 1 ]; then
  if [ ! -f "$SEC_STAGE/openclaw/.env" ] && [ ! -d "$SEC_STAGE/openclaw/agents" ]; then
    warn "Secrets backup requested but no secrets files were found; skipping secrets archive."
    INCLUDE_SECRETS=0
  else
    (
      cd "$SEC_STAGE"
      tar -czf "$SECRETS_ARCHIVE" openclaw
    )

    if [ -n "$AGE_RECIPIENT" ]; then
      age -r "$AGE_RECIPIENT" -o "$SECRETS_ENCRYPTED" "$SECRETS_ARCHIVE"
    else
      AGE_PASSPHRASE="$(cat "$AGE_PASSPHRASE_FILE")" age -p -o "$SECRETS_ENCRYPTED" "$SECRETS_ARCHIVE" <<< "$AGE_PASSPHRASE"
    fi
    rm -f "$SECRETS_ARCHIVE"
    info "Created encrypted secrets archive: $SECRETS_ENCRYPTED"
  fi
fi

OPENCLAW_VERSION="$(openclaw --version 2>/dev/null || echo 'unknown')"
NODE_VERSION="$(node --version 2>/dev/null || echo 'unknown')"
OS_NAME="$(uname -srm)"

python3 - "$MANIFEST_PATH" "$OP_ARCHIVE" "$SECRETS_ENCRYPTED" "$FILES_INCLUDED_JSON" "$TIMESTAMP_ISO" "$OPENCLAW_VERSION" "$NODE_VERSION" "$OS_NAME" "$INCLUDE_SECRETS" <<'PY'
import hashlib, json, os, sys
from pathlib import Path
manifest, op_archive, sec_archive, files_json, timestamp, openclaw_version, node_version, os_name, include_secrets = sys.argv[1:]
include_secrets = int(include_secrets)
files_included = json.loads(Path(files_json).read_text(encoding='utf-8'))

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

payload = {
    'version': '1.1.0',
    'openclaw_version': openclaw_version.strip(),
    'timestamp': timestamp,
    'archives': {
        'operational': {
            'file': os.path.basename(op_archive),
            'sha256': sha256(op_archive),
            'size': os.path.getsize(op_archive),
        },
        'secrets': {
            'file': os.path.basename(sec_archive) if include_secrets and os.path.exists(sec_archive) else None,
            'sha256': sha256(sec_archive) if include_secrets and os.path.exists(sec_archive) else None,
            'size': os.path.getsize(sec_archive) if include_secrets and os.path.exists(sec_archive) else 0,
            'encrypted': bool(include_secrets and os.path.exists(sec_archive)),
        },
    },
    'files_included': files_included,
    'node_version': node_version.strip(),
    'os': os_name.strip(),
}
Path(manifest).write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8')
PY

info "Created operational archive: $OP_ARCHIVE"
info "Created manifest: $MANIFEST_PATH"
if [ "$INCLUDE_SECRETS" -eq 0 ]; then
  info "Secrets archive: not created (default operational-only mode)"
fi
info "Next step: bash scripts/verify.sh --manifest '$MANIFEST_PATH' --archive '$OP_ARCHIVE'"
