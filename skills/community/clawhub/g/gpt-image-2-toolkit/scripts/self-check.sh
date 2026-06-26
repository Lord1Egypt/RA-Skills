#!/usr/bin/env bash
set -euo pipefail

EXPLICIT_DIR="${1:-}"
CONFIG_DIR="${OPENCLAW_CONFIG_DIR:-$HOME/.openclaw}"
CANDIDATES=()

if [ -n "$EXPLICIT_DIR" ]; then
  CANDIDATES+=("$EXPLICIT_DIR")
fi

CANDIDATES+=(
  "$CONFIG_DIR/extensions/hnbc"
  "/usr/lib/node_modules/openclaw/dist/extensions/hnbc"
)

PLUGIN_DIR=""
for dir in "${CANDIDATES[@]}"; do
  if [ -d "$dir" ]; then
    PLUGIN_DIR="$dir"
    break
  fi
done

if [ -z "$PLUGIN_DIR" ]; then
  echo "STATUS=missing"
  echo "CHECKED_DIRS=$(printf '%s,' "${CANDIDATES[@]}" | sed 's/,$//')"
  exit 1
fi

required_files=(
  "index.js"
  "image-generation-provider.js"
  "package.json"
  "openclaw.plugin.json"
)

missing=0
for f in "${required_files[@]}"; do
  if [ ! -f "$PLUGIN_DIR/$f" ]; then
    echo "MISSING_FILE=$f"
    missing=1
  fi
done

if [ "$missing" -ne 0 ]; then
  echo "STATUS=incomplete"
  echo "PLUGIN_DIR=$PLUGIN_DIR"
  exit 2
fi

echo "STATUS=ok"
echo "PLUGIN_DIR=$PLUGIN_DIR"
node - "$PLUGIN_DIR" <<'NODE'
const fs = require('fs');
const path = require('path');
const dir = process.argv[2];
const pkg = JSON.parse(fs.readFileSync(path.join(dir, 'package.json'), 'utf8'));
const manifest = JSON.parse(fs.readFileSync(path.join(dir, 'openclaw.plugin.json'), 'utf8'));
console.log('PACKAGE_NAME=' + (pkg.name || ''));
console.log('PACKAGE_VERSION=' + (pkg.version || ''));
console.log('PLUGIN_ID=' + (manifest.id || ''));
console.log('PROVIDERS=' + ((manifest.providers || []).join(',')));
NODE
