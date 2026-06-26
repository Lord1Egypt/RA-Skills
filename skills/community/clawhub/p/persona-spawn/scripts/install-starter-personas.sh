#!/usr/bin/env bash
set -euo pipefail

DEST_ROOT="${1:?Usage: install-starter-personas.sh <personas_dir>}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
ASSET_DIR="$SKILL_DIR/assets/personas"

if [[ ! -d "$ASSET_DIR" ]]; then
  echo "Bundled personas not found: $ASSET_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_ROOT"
cp -r "$ASSET_DIR"/* "$DEST_ROOT"/
if [[ ! -f "$DEST_ROOT/config.json" ]]; then
  cat > "$DEST_ROOT/config.json" <<'JSON'
{
  "context_files": []
}
JSON
fi
python3 "$SCRIPT_DIR/rebuild-index.py" "$DEST_ROOT" >/dev/null

echo "Installed starter personas to: $DEST_ROOT"
echo "Rebuilt index: $DEST_ROOT/index.json"
