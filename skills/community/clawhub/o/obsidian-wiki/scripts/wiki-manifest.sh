#!/usr/bin/env bash
# wiki-manifest.sh — Delta tracking for incremental wiki compilation
# Usage:
#   bash wiki-manifest.sh <vault-path> status     — accurate counts via hash check
#   bash wiki-manifest.sh <vault-path> diff        — list pending files
#   bash wiki-manifest.sh <vault-path> mark <file> — record a file as ingested
#   bash wiki-manifest.sh --help
set -euo pipefail
export LC_ALL=C

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  echo "Usage: bash wiki-manifest.sh <vault-path> {status|diff|mark <file>}"
  echo "Delta tracking via SHA-256 hashes for incremental wiki compilation."
  exit 0
fi

for arg in "$@"; do
  case "$arg" in --help|-h) ;; --*) echo "Error: unknown option '$arg'" >&2; exit 2 ;; esac
done

command -v python3 >/dev/null 2>&1 || { echo "Error: python3 is required" >&2; exit 1; }

VAULT="${1:?Usage: wiki-manifest.sh <vault-path> <command> [file]}"
VAULT="${VAULT%/}"  # strip trailing slash
CMD="${2:-status}"
ARG="${3:-}"

META_DIR="$VAULT/.wiki-meta"
MANIFEST="$META_DIR/manifest.json"
mkdir -p "$META_DIR"
[ -f "$MANIFEST" ] || echo '{}' > "$MANIFEST"

# Portable SHA-256
file_hash() {
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | cut -d' ' -f1
  elif command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | cut -d' ' -f1
  else
    python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"
  fi
}

# Find all raw sources (grouped correctly for BSD find)
find_raw() {
  [ -d "$VAULT/raw" ] || return 0
  find "$VAULT/raw" -type f \( -iname '*.md' -o -iname '*.pdf' -o -iname '*.txt' -o -iname '*.epub' -o -iname '*.html' \) ! -name '.gitkeep' -print 2>/dev/null | sort
}

# Compute diff: new + changed files (reused by status and diff)
# Single Python call: loads manifest + hashes all raw files → outputs NEW:/CHANGED:/OK: lines
compute_diff() {
  find_raw | python3 -c "
import json, sys, hashlib, os

manifest_path = sys.argv[1]
vault = sys.argv[2]

try:
    with open(manifest_path) as f:
        manifest = json.load(f)
except (json.JSONDecodeError, ValueError):
    print('Error: manifest.json is corrupted (invalid JSON). Fix or delete it.', file=sys.stderr)
    sys.exit(1)
if not isinstance(manifest, dict):
    print('Error: manifest.json has wrong shape (expected object). Fix or delete it.', file=sys.stderr)
    sys.exit(1)

for line in sys.stdin:
    filepath = line.rstrip('\\n')
    if not filepath:
        continue
    relpath = os.path.relpath(filepath, vault)
    try:
        current_hash = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()
    except OSError as e:
        print(f'ERROR:{relpath}\\t{e}', file=sys.stderr)
        continue
    entry = manifest.get(relpath)
    if entry is None:
        print(f'NEW:{relpath}')
    elif not isinstance(entry, dict):
        print(f'NEW:{relpath}')  # malformed entry treated as missing
    elif entry.get('hash', '') != current_hash:
        print(f'CHANGED:{relpath}')
    else:
        print(f'OK:{relpath}')
" "$MANIFEST" "$VAULT" || { echo "Error: compute_diff failed" >&2; exit 1; }
}

case "$CMD" in
  status)
    diff_output=$(compute_diff)
    if [ -z "$diff_output" ]; then
      total_raw=0
    else
      total_raw=$(echo "$diff_output" | wc -l | tr -d ' ')
    fi
    new_count=$(echo "$diff_output" | grep -c '^NEW:' || true)
    changed_count=$(echo "$diff_output" | grep -c '^CHANGED:' || true)
    uptodate_count=$(echo "$diff_output" | grep -c '^OK:' || true)
    pending=$(( new_count + changed_count ))
    echo "=== Manifest Status ==="
    echo "Raw sources:  $total_raw"
    echo "Up to date:   $uptodate_count"
    echo "New:          $new_count"
    echo "Changed:      $changed_count"
    echo "Pending:      $pending"
    ;;

  diff)
    echo "=== Files Needing Ingest ==="
    _diff_out=$(compute_diff)
    if [ -z "$_diff_out" ] || ! echo "$_diff_out" | grep -qE '^(NEW|CHANGED):'; then
      echo "  ✅ All sources up to date"
    else
      echo "$_diff_out" | while IFS= read -r _line; do
        _status="${_line%%:*}"
        _relpath="${_line#*:}"
        case "$_status" in
          NEW)     echo "  📥 NEW:     $_relpath" ;;
          CHANGED) echo "  🔄 CHANGED: $_relpath" ;;
        esac
      done
    fi
    ;;

  mark)
    [ -n "$ARG" ] || { echo "Usage: wiki-manifest.sh <vault> mark <file-path>" >&2; exit 2; }
    # Canonicalize path
    if [ -f "$VAULT/$ARG" ]; then
      abs_file="$VAULT/$ARG"
    elif [ -f "$ARG" ]; then
      # Ensure it's absolute
      case "$ARG" in
        /*) abs_file="$ARG" ;;
        *)  abs_file="$(cd "$(dirname "$ARG")" && pwd)/$(basename "$ARG")" ;;
      esac
    else
      echo "Error: file not found: $ARG" >&2; exit 1
    fi
    # Reject symlinks (find_raw uses -type f which excludes them)
    if [ -L "$abs_file" ]; then
      echo "Error: symlinks are not supported (find_raw excludes them): $ARG" >&2; exit 1
    fi
    relpath="${abs_file#"$VAULT"/}"
    # Enforce that file is under raw/
    case "$relpath" in
      raw/*) ;;
      *) echo "Error: file must be under raw/: $relpath" >&2; exit 1 ;;
    esac
    # Enforce supported file type (case-insensitive, must match find_raw extensions)
    _ext_lower=$(printf '%s' "${relpath##*.}" | tr '[:upper:]' '[:lower:]')
    case "$_ext_lower" in
      md|pdf|txt|epub|html) ;;
      *) echo "Error: unsupported file type .${relpath##*.} (supported: .md, .pdf, .txt, .epub, .html, case-insensitive)" >&2; exit 1 ;;
    esac
    current_hash=$(file_hash "$abs_file")
    file_size=$(wc -c < "$abs_file" | tr -d ' ')
    now=$(python3 -c "from datetime import datetime,timezone;print(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))")
    _tmp_manifest=$(mktemp "$META_DIR/manifest.json.XXXXXX")
    trap 'rm -f "$_tmp_manifest" 2>/dev/null' EXIT
    python3 -c "
import json, sys
manifest_path, relpath, h, ts, sz = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
try:
    with open(manifest_path) as f:
        d = json.load(f)
except (json.JSONDecodeError, ValueError):
    print('Error: .wiki-meta/manifest.json is corrupted (invalid JSON). Fix or delete it.', file=sys.stderr)
    sys.exit(1)
if not isinstance(d, dict):
    print('Error: .wiki-meta/manifest.json has wrong shape (expected object). Fix or delete it.', file=sys.stderr)
    sys.exit(1)
d[relpath] = {'hash': h, 'ingestedAt': ts, 'size': sz}
with open(sys.argv[6], 'w') as f:
    json.dump(d, f, indent=2, sort_keys=True)
print(f'Marked: {relpath} (hash={h})')
" "$MANIFEST" "$relpath" "$current_hash" "$now" "$file_size" "$_tmp_manifest" && mv "$_tmp_manifest" "$MANIFEST" || { rm -f "$_tmp_manifest"; echo "Error: failed to update manifest" >&2; exit 1; }
    ;;

  *)
    echo "Unknown command: $CMD" >&2
    echo "Usage: wiki-manifest.sh <vault-path> {status|diff|mark <file>}" >&2
    exit 2
    ;;
esac
