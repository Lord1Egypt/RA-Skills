#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/build"

mkdir -p "$OUT_DIR"

VERSION="$(awk -F': ' '/^version:/ {print $2}' "$ROOT_DIR/SKILL.md" | tr -d '\r')"
NAME="$(awk -F': ' '/^name:/ {print $2}' "$ROOT_DIR/SKILL.md" | tr -d '\r')"

cp "$ROOT_DIR/assets/prompt.txt" "$OUT_DIR/prompt.txt"

cat > "$OUT_DIR/package-info.json" <<JSON
{
  "name": "$NAME",
  "version": "$VERSION",
  "builtAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "includedAssets": [
    "prompt.txt"
  ]
}
JSON

echo "Prepared package metadata at $OUT_DIR/package-info.json"
