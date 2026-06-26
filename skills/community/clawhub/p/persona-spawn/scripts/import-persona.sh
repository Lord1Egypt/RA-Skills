#!/usr/bin/env bash
# Import one or more personas from the Emblem marketplace into a local personas directory.
#
# Usage:
#   import-persona.sh [--no-index] <handle> <personas_dir>
#   import-persona.sh [--no-index] --all <personas_dir>

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
NO_INDEX=0
IMPORT_ALL=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-index)
      NO_INDEX=1
      shift
      ;;
    --all)
      IMPORT_ALL=1
      shift
      ;;
    *)
      break
      ;;
  esac
done

import_one() {
  local HANDLE="$1"
  local DEST_ROOT="$2"
  local DEST="$DEST_ROOT/$HANDLE"
  local BASE="https://raw.githubusercontent.com/decentraliser/personas/main/personas/$HANDLE"

  local HTTP_CODE
  HTTP_CODE=$(curl -sf -o /dev/null -w '%{http_code}' "$BASE/persona.json" 2>/dev/null || echo "000")
  if [[ "$HTTP_CODE" != "200" ]]; then
    echo "Error: persona '$HANDLE' not found in marketplace (HTTP $HTTP_CODE)" >&2
    return 1
  fi

  mkdir -p "$DEST"
  echo "Importing $HANDLE..."
  curl -sf "$BASE/persona.json"  > "$DEST/persona.json"  && echo "  ✓ persona.json"
  curl -sf "$BASE/SOUL.md"       > "$DEST/SOUL.md"       && echo "  ✓ SOUL.md"
  curl -sf "$BASE/IDENTITY.md"   > "$DEST/IDENTITY.md"   2>/dev/null && echo "  ✓ IDENTITY.md" || echo "  - IDENTITY.md (not found, optional)"
  curl -sf "$BASE/avatar.png"    > "$DEST/avatar.png"    2>/dev/null && echo "  ✓ avatar.png" || true
}

import_all() {
  local DEST_ROOT="$1"
  local TMPDIR
  TMPDIR="$(mktemp -d)"

  echo "Downloading persona archive..."
  curl -Lsf "https://github.com/decentraliser/personas/archive/refs/heads/main.tar.gz" -o "$TMPDIR/personas.tar.gz"
  tar xzf "$TMPDIR/personas.tar.gz" -C "$TMPDIR"

  local SRC_DIR="$TMPDIR/personas-main/personas"
  if [[ ! -d "$SRC_DIR" ]]; then
    echo "Archive did not contain personas directory" >&2
    rm -rf "$TMPDIR"
    return 1
  fi

  mkdir -p "$DEST_ROOT"
  cp -r "$SRC_DIR"/* "$DEST_ROOT"/
  rm -rf "$TMPDIR"
  echo "Imported all personas into: $DEST_ROOT"
}

if [[ "$IMPORT_ALL" == "1" ]]; then
  DEST_ROOT="${1:?Usage: import-persona.sh --all <personas_dir>}"
  import_all "$DEST_ROOT"
else
  HANDLE="${1:?Usage: import-persona.sh [--no-index] <handle> <personas_dir>}"
  DEST_ROOT="${2:?Usage: import-persona.sh [--no-index] <handle> <personas_dir>}"
  import_one "$HANDLE" "$DEST_ROOT"
fi

if [[ "$NO_INDEX" != "1" ]]; then
  python3 "$SCRIPT_DIR/rebuild-index.py" "$DEST_ROOT" >/dev/null
  echo "Index rebuilt: $DEST_ROOT/index.json"
else
  echo "Skipped index rebuild (--no-index)"
fi

echo "Done."
