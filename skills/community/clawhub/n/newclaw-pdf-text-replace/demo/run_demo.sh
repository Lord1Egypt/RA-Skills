#!/bin/bash
# PDF Text Replace v2.1 - Interactive Demo
#
# Demonstrates all key capabilities:
#   L1 - Equal-length replacement    (2025-01-01 -> 2026-01-01)
#   L2 - Variable-length replacement (500 RMB    -> 1000 RMB)
#   L4 - Color change overlay        (2026-01-01 -> red)
#
# Usage:  bash run_demo.sh
# Prereq: pip3 install reportlab pypdf pdfplumber fonttools

set -e

DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$DEMO_DIR/../scripts/pdf_text_replace.py"

echo "=== PDF Text Replace v2.1 Demo ==="
echo ""

# ── Step 0: Create sample PDF ────────────────────────────────────────────────
echo "Step 0: Generating sample certificate PDF..."
python3 "$DEMO_DIR/create_demo_pdf.py"
echo "  Created: sample_certificate.pdf"
echo ""

# ── Step 1: L1 - Equal-length date replacement ───────────────────────────────
# "2025-01-01" -> "2026-01-01" — same byte length, direct code swap
echo "Step 1: L1 - Equal-length replacement"
python3 "$SCRIPT" \
    "$DEMO_DIR/sample_certificate.pdf" \
    "2025-01-01" "2026-01-01" \
    "$DEMO_DIR/demo_L1.pdf"
echo "  Changed: 2025-01-01 -> 2026-01-01 (equal length, direct byte-swap)"
echo ""

# ── Step 2: L2 - Variable-length amount replacement ─────────────────────────
# "500 RMB" -> "1000 RMB" — different byte length, overlay strategy
echo "Step 2: L2 - Variable-length replacement"
python3 "$SCRIPT" \
    "$DEMO_DIR/demo_L1.pdf" \
    "500 RMB" "1000 RMB" \
    "$DEMO_DIR/demo_L2.pdf"
echo "  Changed: 500 RMB -> 1000 RMB (different length, Tz/reflow strategy)"
echo ""

# ── Step 3: L4 - Color overlay on date ──────────────────────────────────────
# Re-draw the date text in red using a style overlay.
# Note: old_text == new_text here (same string, different color), so the tool
# reports "verification fail" because the text is still present — expected.
# We use "|| true" so set -e does not abort on the false-positive exit code.
echo "Step 3: L4 - Color change"
python3 "$SCRIPT" \
    "$DEMO_DIR/demo_L2.pdf" \
    "2026-01-01" "2026-01-01" \
    "$DEMO_DIR/demo_final.pdf" \
    --color 1,0,0 || true
echo "  Changed: date text color -> red (style overlay)"
echo ""

# ── Summary ──────────────────────────────────────────────────────────────────
echo "=== Results ==="
echo ""
for f in sample_certificate.pdf demo_L1.pdf demo_L2.pdf demo_final.pdf; do
    path="$DEMO_DIR/$f"
    if [ -f "$path" ]; then
        size=$(du -h "$path" | cut -f1)
        echo "  [OK] $f  ($size)"
    else
        echo "  [MISSING] $f"
    fi
done
echo ""
echo "Pipeline complete. Open demo_final.pdf to see all changes applied:"
echo "  - Date:   2025-01-01 -> 2026-01-01"
echo "  - Amount: 500 RMB    -> 1000 RMB"
echo "  - Color:  date text is now red"
echo ""
echo "Files saved in: $DEMO_DIR"
