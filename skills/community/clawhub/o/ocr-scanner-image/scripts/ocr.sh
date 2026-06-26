#!/usr/bin/env bash
set -e

# ------------------------------------------------------------
# OCR‑Wrapper – unterstützt Bilddateien (jpg, png, …) und PDF
# ------------------------------------------------------------

usage() {
  echo "Usage: $0 <file>"
  echo "  <file>  Bild (jpg/png/… ) oder PDF‑Datei"
  exit 1
}

if [ -z "$1" ]; then
  usage
fi

INPUT="$1"
EXTENSION="${INPUT##*.}"   # Dateierweiterung (ohne Pfad)

# ---- Funktion: OCR für ein Bild ----
ocr_image() {
  local img="$1"
  # tesseract –l eng (Englisch).  Entferne "-l eng" für automatische Spracherkennung.
  tesseract "$img" stdout -l eng || true
}

# ---- PDF‑Verarbeitung (falls nötig) ----
if [[ "$EXTENSION" =~ ^[Pp][Dd][Ff]$ ]]; then
  # Konvertiere jede Seite zu einem temporären PNG (300 dpi liefert gute Qualität)
  TMPDIR=$(mktemp -d)
  # pdftoppm erzeugt Dateien: page-1.png, page-2.png, …
  pdftoppm -png -r 300 "$INPUT" "$TMPDIR/page"
  # Schleife über alle erzeugten PNGs und OCR ausführen
  for img in "$TMPDIR"/*.png; do
    echo "--- Seite: $(basename "$img") ---"
    ocr_image "$img"
  done
  rm -rf "$TMPDIR"
else
  # Bilddatei – direkt OCR ausführen
  ocr_image "$INPUT"
fi
