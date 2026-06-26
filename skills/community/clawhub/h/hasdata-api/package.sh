#!/usr/bin/env bash
# package.sh — pack this openclaw skill into a zip ready for distribution or
# manual upload. README.md is human-facing only and is excluded from the
# bundle. The script itself, OS junk, prior zips, and VCS metadata are also
# excluded.
#
# Usage:
#   ./package.sh                  # writes hasdata-openclaw-skill.zip alongside SKILL.md
#   ./package.sh /tmp/out.zip     # custom output path

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
OUT="${1:-$SCRIPT_DIR/hasdata-openclaw-skill.zip}"

# Resolve OUT to an absolute path so the cd below doesn't break a relative arg.
case "$OUT" in
  /*) ;;
  *) OUT="$(pwd)/$OUT" ;;
esac

cd "$SCRIPT_DIR"
rm -f "$OUT"

zip -r "$OUT" . \
  -x "README.md" \
  -x "$SCRIPT_NAME" \
  -x ".DS_Store" -x "*/.DS_Store" \
  -x ".git/*" \
  -x "*.zip" \
  > /dev/null

echo "wrote: $OUT"
echo "size:  $(du -h "$OUT" | awk '{print $1}')"
echo
echo "contents:"
unzip -l "$OUT" | sed '1,2d;$d'
