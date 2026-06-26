#!/bin/bash
# extract_pages.sh — Convert PDF to page images for style analysis
# Usage: bash extract_pages.sh input.pdf output_dir/ [dpi]

set -euo pipefail

PDF="${1:?Usage: extract_pages.sh input.pdf output_dir/ [dpi]}"
OUTDIR="${2:?Usage: extract_pages.sh input.pdf output_dir/ [dpi]}"
DPI="${3:-150}"

if ! command -v pdftoppm &>/dev/null; then
    echo "❌ pdftoppm not found. Install: apt install poppler-utils" >&2
    exit 1
fi

if [ ! -f "$PDF" ]; then
    echo "❌ File not found: $PDF" >&2
    exit 1
fi

mkdir -p "$OUTDIR"

echo "📄 Converting: $PDF → $OUTDIR/ (${DPI} DPI)"

pdftoppm -jpeg -r "$DPI" "$PDF" "${OUTDIR}/page"

COUNT=$(ls -1 "${OUTDIR}"/page-*.jpg 2>/dev/null | wc -l)
echo "✅ Done. $COUNT page(s) extracted."
ls -lh "${OUTDIR}"/page-*.jpg 2>/dev/null | head -5
if [ "$COUNT" -gt 5 ]; then
    echo "   ... and $((COUNT - 5)) more"
fi
