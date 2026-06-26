#!/usr/bin/env bash
# render_figures.sh — Convert PDF figures to PNG for WeasyPrint embedding
#
# Uses PyMuPDF (fitz) to rasterize vector PDF figures at high DPI.
# Auto-detects raster vs vector PDFs and optimizes output size.
#
# Usage: ./render_figures.sh <figures_dir> <output_dir>

set -euo pipefail

FIGURES_DIR="${1:-}"
OUTPUT_DIR="${2:-/tmp/papyrus_figures}"

if [ -z "$FIGURES_DIR" ] || [ ! -d "$FIGURES_DIR" ]; then
    echo "Usage: $0 <figures_dir> <output_dir>"
    echo "  Converts all PDF figures to PNG for WeasyPrint HTML→PDF pipeline"
    exit 1
fi

# Check PyMuPDF availability
python3 -c "import fitz; print(f'PyMuPDF {fitz.version[0]}')" 2>/dev/null || {
    echo "Error: PyMuPDF not installed. Run: pip3 install PyMuPDF"
    echo "  Without PyMuPDF, vector PDF figures cannot be rasterized."
    exit 1
}

mkdir -p "$OUTPUT_DIR"

TOTAL=0; OK=0; VECTOR=0; RASTER=0

echo "🖼️  Converting PDF figures to PNG (200 DPI)"
echo ""

for pdf_file in "$FIGURES_DIR"/*.pdf; do
    [ -f "$pdf_file" ] || continue
    TOTAL=$((TOTAL + 1))
    base=$(basename "$pdf_file" .pdf)
    out="$OUTPUT_DIR/${base}.png"

    python3 -c "
import fitz, os, sys
from PIL import Image
import io

doc = fitz.open('$pdf_file')
page = doc[0]

# Check if page has embedded raster images (bitmap)
has_embedded = False
for img_info in page.get_images(full=True):
    has_embedded = True
    break

if has_embedded and doc.page_count == 1:
    # Try extract embedded image first (preserves original resolution)
    for img_info in page.get_images(full=True):
        try:
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            img_data = base_image['image']
            pil_img = Image.open(io.BytesIO(img_data)).convert('RGBA')
            # Resize if too large (> 2000px wide)
            if pil_img.width > 2000:
                scale = 2000 / pil_img.width
                pil_img = pil_img.resize(
                    (int(pil_img.width*scale), int(pil_img.height*scale)),
                    Image.LANCZOS)
            pil_img.save('$out')
            print('  $base: {}x{} (embedded bitmap)'.format(pil_img.width, pil_img.height))
            sys.exit(0)
        except: pass

# Vector PDF: rasterize at 200 DPI
mat = fitz.Matrix(200/72, 200/72)
pix = page.get_pixmap(matrix=mat)
pix.save('$out')

# Resize if too wide (> 1400px)
w, h = pix.width, pix.height
if w > 1400:
    img = Image.open('$out').convert('RGBA')
    scale = 1200 / w
    img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
    img.save('$out')
    print('  $base: {}x{} → {}x{} (vector, rasterized)'.format(w, h, img.width, img.height))
else:
    print('  $base: {}x{} (vector, rasterized)'.format(w, h))
" 2>/dev/null

    if [ -f "$out" ]; then
        OK=$((OK + 1))
        sz=$(python3 -c "import os; print(os.path.getsize('$out'))")
        echo "      $sz bytes"
    fi
done

echo ""
echo "═══════════════════════════════════════"
echo "   Total:  $TOTAL"
echo "   OK:     $OK"
echo "   Output: $OUTPUT_DIR"
echo "═══════════════════════════════════════"
