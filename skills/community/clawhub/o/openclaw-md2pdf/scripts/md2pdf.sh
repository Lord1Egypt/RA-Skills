#!/usr/bin/env bash
# md2pdf.sh — Markdown to PDF converter
# Usage: md2pdf.sh input.md
# Output: PDF wird im gleichen Ordner wie das MD abgelegt
set -euo pipefail

if [[ $# -lt 1 || "$1" == "--help" || "$1" == "-h" ]]; then
  echo "Usage: md2pdf.sh <input.md>"
  echo "  PDF wird im gleichen Ordner wie das MD abgelegt."
  exit 0
fi

INPUT="$1"

if [[ ! -f "$INPUT" ]]; then
  echo "ERROR: Datei nicht gefunden: $INPUT"
  exit 1
fi

# Output: gleicher Ordner, gleicher Name, .pdf statt .md
INPUT_DIR="$(cd "$(dirname "$INPUT")" && pwd)"
BASENAME="$(basename "$INPUT" .md)"
OUTPUT="$INPUT_DIR/${BASENAME}.pdf"
TYPST_TMP="$INPUT_DIR/.${BASENAME}.typ"

# Pandoc: MD → Typst (intermediate)
pandoc "$INPUT" \
  --from markdown \
  --to typst \
  --output "$TYPST_TMP" \
  --wrap=none

# Typst template: wrap pandoc output with styling
TYPST_STYLED="$INPUT_DIR/.${BASENAME}_styled.typ"
cat > "$TYPST_STYLED" <<'TYPST_HEADER'
#set page(margin: 2cm)
#set text(font: ("Helvetica Neue", "Helvetica", "Arial"), size: 11pt, lang: "de")
#set par(leading: 0.8em, spacing: 1.2em)
#show heading.where(level: 1): it => {
  set text(size: 20pt, weight: "bold")
  v(0.5em)
  it
  v(0.2em)
  line(length: 100%, stroke: 0.5pt + luma(180))
  v(0.3em)
}
#show heading.where(level: 2): it => {
  set text(size: 15pt, weight: "bold")
  v(0.4em)
  it
  v(0.1em)
}
#show heading.where(level: 3): it => {
  set text(size: 12pt, weight: "bold")
  v(0.3em)
  it
}
#show raw.where(block: true): it => {
  set text(font: ("Menlo", "Courier New"), size: 9pt)
  block(fill: luma(245), inset: 10pt, radius: 4pt, width: 100%, it)
}
#show raw.where(block: false): it => {
  set text(font: ("Menlo", "Courier New"), size: 9.5pt)
  box(fill: luma(240), inset: (x: 3pt, y: 1.5pt), radius: 2pt, it)
}
#show link: it => {
  set text(fill: rgb("#0969da"))
  underline(it)
}
TYPST_HEADER

# Replace invalid #horizontalrule with proper Typst syntax
cat "$TYPST_TMP" | sed 's/#horizontalrule/line(length: 100%, stroke: 0.5pt + luma(180))/g' >> "$TYPST_STYLED"


# Typst: styled → PDF
typst compile "$TYPST_STYLED" "$OUTPUT" --root "$INPUT_DIR"

# Cleanup temp files
rm -f "$TYPST_TMP" "$TYPST_STYLED"

echo "OK: $OUTPUT"
