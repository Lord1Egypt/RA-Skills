#!/usr/bin/env bash
set -euo pipefail

# Package indeed-brightdata skill as a ZIP for Claude Desktop distribution.

SCRIPT_DIR=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR

PROJECT_ROOT=""
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly PROJECT_ROOT

readonly PACKAGE_NAME="indeed-brightdata"
readonly OUTPUT_FILE="$PROJECT_ROOT/$PACKAGE_NAME.zip"

TEMP_DIR=""

cleanup() {
  if [[ -n "$TEMP_DIR" && -d "$TEMP_DIR" ]]; then
    rm -rf "$TEMP_DIR"
  fi
}
trap cleanup EXIT

show_help() {
  cat >&2 <<EOF
Usage: $(basename "$0") [OPTIONS]

Package the indeed-brightdata skill into a ZIP file for Claude Desktop.

Options:
  --help    Show this help message and exit

Output:
  Creates $PACKAGE_NAME.zip in the project root directory.
  The ZIP contains all files needed for Claude Desktop installation.
EOF
  exit 0
}

main() {
  if [[ "${1:-}" == "--help" ]]; then
    show_help
  fi

  TEMP_DIR="$(mktemp -d)"

  local staging_dir="$TEMP_DIR/$PACKAGE_NAME"
  mkdir -p "$staging_dir/scripts" "$staging_dir/references"

  # Copy included files
  cp "$PROJECT_ROOT/SKILL.md" "$staging_dir/"

  if [[ -f "$PROJECT_ROOT/LICENSE" ]]; then
    cp "$PROJECT_ROOT/LICENSE" "$staging_dir/"
  fi

  # Copy scripts (excluding package.sh itself)
  find "$PROJECT_ROOT/scripts" -maxdepth 1 -type f ! -name "package.sh" -exec cp {} "$staging_dir/scripts/" \;

  # Copy references
  if [[ -d "$PROJECT_ROOT/references" ]]; then
    cp -r "$PROJECT_ROOT/references/." "$staging_dir/references/"
  fi

  # Remove old output if present
  rm -f "$OUTPUT_FILE"

  # Create ZIP from temp dir so paths are relative
  (cd "$TEMP_DIR" && zip -qr "$OUTPUT_FILE" "$PACKAGE_NAME")

  local size=""
  size="$(du -h "$OUTPUT_FILE" | cut -f1)"

  echo "Created $PACKAGE_NAME.zip ($size)" >&2
}

main "$@"
