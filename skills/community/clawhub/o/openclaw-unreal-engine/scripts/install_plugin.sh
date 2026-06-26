#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 /path/to/UnrealProject" >&2
  exit 1
fi

PROJECT_DIR="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGIN_SRC="$SKILL_DIR/assets/OpenClawUnrealPlugin"
PLUGIN_DST="$PROJECT_DIR/Plugins/OpenClawUnrealPlugin"

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "Project directory not found: $PROJECT_DIR" >&2
  exit 1
fi

mkdir -p "$PROJECT_DIR/Plugins"
rm -rf "$PLUGIN_DST"
cp -R "$PLUGIN_SRC" "$PLUGIN_DST"

echo "Installed plugin to: $PLUGIN_DST"
echo "Next: regenerate project files if needed, then build the project/plugin in Unreal Editor or your IDE."
