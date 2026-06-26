#!/usr/bin/env bash
# render_formulas.sh — Render LaTeX formulas to PNG with fallback
#
# Fallback chain:
#   1. Local LaTeX engine (pdflatex → PDF → PNG via Python)
#   2. Online API (codecogs.com)
#
# Usage: ./render_formulas.sh <formulas.txt> <output_dir>
# formulas.txt format: one LaTeX formula per line
#   @name=formula_name    — sets output filename
#   LaTeX source line     — the formula to render

set -euo pipefail

FORMULAS_FILE="${1:-}"
OUTPUT_DIR="${2:-/tmp/papyrus_formulas}"

if [ -z "$FORMULAS_FILE" ] || [ ! -f "$FORMULAS_FILE" ]; then
    echo "Usage: $0 <formulas.txt> <output_dir>"
    echo ""
    echo "formulas.txt format:"
    echo "  @name=formula1"
    echo "  \\dpi{150}\\displaystyle \\mathrm{Attention}(Q,K,V)=..."
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# ─────────────────────────────────────────────
#  Stage 1: Check for local LaTeX engine
# ─────────────────────────────────────────────

LOCAL_TEX=""
for engine in pdflatex lualatex xelatex; do
    if command -v "$engine" &>/dev/null; then
        LOCAL_TEX="$engine"
        break
    fi
done

# Also check for pdfcrop (optional, nicer output)
HAS_PDFCROP=false
command -v pdfcrop &>/dev/null && HAS_PDFCROP=true

# Check Python can convert PDF pages to PNG
PYTHON_PDF2PNG=$(python3 -c "
try:
    from pypdf import PdfReader
    from PIL import Image
    print('ok')
except ImportError:
    print('missing')
")

if [ -n "$LOCAL_TEX" ] && [ "$PYTHON_PDF2PNG" = "ok" ]; then
    echo "🔧 Local LaTeX engine found: $LOCAL_TEX"
    echo "   PDF crop: $($HAS_PDFCROP && echo 'yes' || echo 'no')"
    RENDER_MODE="local"
else
    if [ -z "$LOCAL_TEX" ]; then
        echo "⚠️  No local LaTeX engine found (install texlive or basictex)"
    fi
    if [ "$PYTHON_PDF2PNG" != "ok" ]; then
        echo "⚠️  Python pypdf+Pillow not available"
    fi
    echo "🌐 Falling back to online API (codecogs.com)"
    RENDER_MODE="online"
fi

echo ""

# ─────────────────────────────────────────────
#  Stage 2: Render formulas
# ─────────────────────────────────────────────

render_via_local_tex() {
    local tex_formula="$1"
    local output_path="$2"
    local tmpdir
    tmpdir=$(mktemp -d /tmp/papyrus_tex_XXXXXX)

    # Create minimal standalone LaTeX document
    cat > "$tmpdir/formula.tex" << TEXEOF
\\documentclass[preview,border=8pt,varwidth]{standalone}
\\usepackage{amsmath,amssymb}
\\begin{document}
${tex_formula}
\\end{document}
TEXEOF

    # Compile (run twice for cross-references, suppress noisy output)
    (
        cd "$tmpdir"
        "$LOCAL_TEX" -interaction=nonstopmode -halt-on-error formula.tex \
            > /dev/null 2>&1 || true
        "$LOCAL_TEX" -interaction=nonstopmode -halt-on-error formula.tex \
            > /dev/null 2>&1 || true
    )

    if [ ! -f "$tmpdir/formula.pdf" ]; then
        echo "    ✗ pdflatex failed, falling back to online"
        rm -rf "$tmpdir"
        return 1
    fi

    # Crop if available
    if $HAS_PDFCROP; then
        pdfcrop --margins 4 "$tmpdir/formula.pdf" "$tmpdir/formula_crop.pdf" \
            > /dev/null 2>&1 || true
        if [ -f "$tmpdir/formula_crop.pdf" ]; then
            mv "$tmpdir/formula_crop.pdf" "$tmpdir/formula.pdf"
        fi
    fi

    # Convert PDF first page to PNG using Python
    python3 -c "
from pypdf import PdfReader
from PIL import Image
import io, sys

reader = PdfReader('$tmpdir/formula.pdf')
if len(reader.pages) == 0:
    sys.exit(1)

page = reader.pages[0]
# Extract page as image (pypdf 3.x approach)
# For formula PDFs, the page usually contains a single rendered image
for img in page.images:
    data = img.data
    pil_img = Image.open(io.BytesIO(data))
    # Convert to RGBA, preserve transparency
    if pil_img.mode != 'RGBA':
        pil_img = pil_img.convert('RGBA')
    pil_img.save('$output_path')
    print(f'    → {pil_img.size[0]}×{pil_img.size[1]} px (local TeX)')
    break
else:
    # Fallback: render at high DPI using pypdf's page rendering
    sys.exit(1)
" 2>/dev/null

    local status=$?
    rm -rf "$tmpdir"
    return $status
}

render_via_codecogs() {
    local tex_formula="$1"
    local output_path="$2"

    local encoded
    encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${tex_formula}'))")
    local url="https://latex.codecogs.com/png.image?${encoded}"

    python3 -c "
import urllib.request, sys
req = urllib.request.Request('${url}', headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    data = resp.read()
    with open('${output_path}', 'wb') as f:
        f.write(data)
    from PIL import Image
    img = Image.open('${output_path}')
    print(f'    → {img.size[0]}×{img.size[1]} px (online)')
except Exception as e:
    print(f'    ✗ ERROR: {e}', file=sys.stderr)
    sys.exit(1)
"
    return $?
}

# ─────────────────────────────────────────────
#  Main render loop
# ─────────────────────────────────────────────

NAME=""
TOTAL=0
OK=0
FAILED=0

while IFS= read -r line; do
    # Skip comments and empty lines
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$line" ]] && continue

    # Parse @name directive
    if [[ "$line" =~ ^@name=([^[:space:]]+) ]]; then
        NAME="${BASH_REMATCH[1]}"
        continue
    fi

    TOTAL=$((TOTAL + 1))
    SAFE_NAME="${NAME:-formula_${TOTAL}}"
    OUTPUT_FILE="${OUTPUT_DIR}/${SAFE_NAME}.png"

    echo "  [${SAFE_NAME}] ${line:0:70}..."

    RENDERED=false
    if [ "$RENDER_MODE" = "local" ]; then
        if render_via_local_tex "$line" "$OUTPUT_FILE"; then
            RENDERED=true
        fi
    fi

    if ! $RENDERED; then
        if render_via_codecogs "$line" "$OUTPUT_FILE"; then
            RENDERED=true
        fi
    fi

    if $RENDERED; then
        OK=$((OK + 1))
    else
        FAILED=$((FAILED + 1))
        echo "    ✗ All rendering methods failed for: ${SAFE_NAME}"
    fi

    NAME=""  # Reset for next formula
done < "$FORMULAS_FILE"

echo ""
echo "═══════════════════════════════════════"
echo "   Total:  ${TOTAL}"
echo "   OK:     ${OK}"
echo "   Failed: ${FAILED}"
echo "   Mode:   ${RENDER_MODE}"
echo "   Output: ${OUTPUT_DIR}"
echo "═══════════════════════════════════════"
