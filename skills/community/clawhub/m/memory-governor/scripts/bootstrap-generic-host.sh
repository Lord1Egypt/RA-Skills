#!/usr/bin/env sh

set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/host-root" >&2
  exit 1
fi

TARGET_ROOT=$1
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
PACKAGE_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
EXAMPLE_ROOT="$PACKAGE_ROOT/examples/generic-host"

mkdir -p "$TARGET_ROOT"

copy_if_missing() {
  src=$1
  dest=$2

  dest_dir=$(dirname "$dest")
  mkdir -p "$dest_dir"

  if [ -e "$dest" ]; then
    echo "skip  $dest"
    return 0
  fi

  cp "$src" "$dest"
  echo "create $dest"
}

copy_if_missing "$EXAMPLE_ROOT/HOST.md" "$TARGET_ROOT/HOST.md"
copy_if_missing "$EXAMPLE_ROOT/memory-governor-host.toml" "$TARGET_ROOT/memory-governor-host.toml"
copy_if_missing "$EXAMPLE_ROOT/adapter-map.md" "$TARGET_ROOT/adapter-map.md"
copy_if_missing "$EXAMPLE_ROOT/memory/long-term.md" "$TARGET_ROOT/memory/long-term.md"
copy_if_missing "$EXAMPLE_ROOT/memory/learning-candidates.md" "$TARGET_ROOT/memory/learning-candidates.md"
copy_if_missing "$EXAMPLE_ROOT/memory/proactive-state.md" "$TARGET_ROOT/memory/proactive-state.md"
copy_if_missing "$EXAMPLE_ROOT/memory/reusable-lessons.md" "$TARGET_ROOT/memory/reusable-lessons.md"
copy_if_missing "$EXAMPLE_ROOT/memory/working-buffer.md" "$TARGET_ROOT/memory/working-buffer.md"
copy_if_missing "$EXAMPLE_ROOT/docs/projects/README.md" "$TARGET_ROOT/docs/projects/README.md"
copy_if_missing "$EXAMPLE_ROOT/docs/tool-rules.md" "$TARGET_ROOT/docs/tool-rules.md"
copy_if_missing "$EXAMPLE_ROOT/skills/example-writer/SKILL.md" "$TARGET_ROOT/skills/example-writer/SKILL.md"

mkdir -p "$TARGET_ROOT/notes/daily" "$TARGET_ROOT/docs"

echo
echo "Bootstrap complete."
echo "Next:"
echo "1. Review HOST.md and adapter-map.md"
echo "2. Replace example-writer with your real skills"
echo "3. Adjust target class mappings for this host"
