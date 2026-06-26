#!/usr/bin/env bash
set -euo pipefail

# Render a note into multiple PNG pages.
# Usage:
#   ./render_note_pages.sh input.md out_dir "Title" [/usr/bin/brave-browser]

IN="${1:-}"
OUTDIR="${2:-}"
TITLE="${3:-Note}"
BRAVE="${4:-/usr/bin/brave-browser}"

if [[ -z "$IN" || -z "$OUTDIR" ]]; then
  echo "Usage: $0 input.md out_dir \"Title\" [/path/to/brave]" >&2
  exit 2
fi

mkdir -p "$OUTDIR/pages"
mkdir -p "$OUTDIR"

# Split
node skills/math-notes-katex/scripts/split_note_md.js "$IN" "$OUTDIR/pages" --max-lines=55 >/dev/null

# Render each page
shopt -s nullglob
for p in "$OUTDIR"/pages/page-*.md; do
  base=$(basename "$p" .md)
  out_png="$OUTDIR/${base}.png"
  node skills/math-notes-katex/scripts/render_note_png.js "$p" "$out_png" --title="$TITLE" --brave="$BRAVE"
  echo "rendered: $out_png" >&2
done
