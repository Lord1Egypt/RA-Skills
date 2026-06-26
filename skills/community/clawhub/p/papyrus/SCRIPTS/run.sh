#!/usr/bin/env bash
# run.sh — Papyrus main entry point
#
# Usage: ./run.sh --paper <arxiv_url> [options]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_URL=""
LANGUAGE="zh-CN"
OUTPUT_DIR="/tmp/papyrus_run"
FONT_SIZE="10pt"
TITLE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --paper) PAPER_URL="$2"; shift 2 ;;
        --language) LANGUAGE="$2"; shift 2 ;;
        --output) OUTPUT_DIR="$2"; shift 2 ;;
        --title) TITLE="$2"; shift 2 ;;
        --font-size) FONT_SIZE="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -z "$PAPER_URL" ]; then
    echo "Papyrus — Academic Paper Deep-Read Tool"
    echo ""
    echo "Usage: $0 --paper <arxiv_url> [options]"
    echo ""
    echo "Options:"
    echo "  --paper <url>      arXiv paper URL (required)"
    echo "  --language <code>  Target language (default: zh-CN)"
    echo "  --output <dir>     Output directory (default: /tmp/papyrus_run)"
    echo "  --title <text>     Document title override"
    echo "  --font-size <pt>   Body font size (default: 10pt)"
    echo ""
    echo "Example:"
    echo "  $0 --paper https://arxiv.org/abs/1706.03762 \\"
    echo "      --title 'Attention Is All You Need — 逐段精读'"
    exit 0
fi

echo "📜 Papyrus — Paper Deep-Read Pipeline"
echo "   Paper: $PAPER_URL"
echo ""

# Step 1: Fetch source
echo "═══ Step 1/4: Fetch arXiv source ═══"
bash "$SCRIPT_DIR/fetch_arxiv.sh" "$PAPER_URL" "$OUTPUT_DIR"

# Step 2: Identify formulas (manual extraction needed, print template)
echo ""
echo "═══ Step 2/4: Identify formulas ═══"
FORMULAS_FILE="$OUTPUT_DIR/formulas.txt"
cat > "$FORMULAS_FILE" << 'FORMULAS_EOF'
# Papyrus formula definitions
# Add one formula per line. Lines starting with @name= define output filenames.
#
# Example entries:
# @name=formula_attention
# \dpi{150}\displaystyle \mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^{\mathrm{T}}}{\sqrt{d_{k}}}\right)V
#
# @name=formula_multihead
# \dpi{150}\displaystyle \mathrm{MultiHead}(Q,K,V)=\mathrm{Concat}(\mathrm{head}_{1},...,\mathrm{head}_{h})W^{O}
#
# @name=formula_ffn
# \dpi{150}\mathrm{FFN}(x)=\max(0,xW_{1}+b_{1})W_{2}+b_{2}
FORMULAS_EOF

echo "   ⚠️  Formula template written to: $FORMULAS_FILE"
echo "   ⚠️  Edit this file with actual formulas from the paper, then run:"
echo "   bash $SCRIPT_DIR/render_formulas.sh $FORMULAS_FILE $OUTPUT_DIR/formulas"

# Step 3: Render formulas
echo ""
echo "═══ Step 3/4: Render formulas ═══"
if [ -s "$FORMULAS_FILE" ] && grep -q "^[^#@]" "$FORMULAS_FILE" 2>/dev/null; then
    bash "$SCRIPT_DIR/render_formulas.sh" "$FORMULAS_FILE" "$OUTPUT_DIR/formulas"
else
    echo "   ⚠️  No formulas defined. Skipping."
fi

# Step 4: Build HTML and PDF
echo ""
echo "═══ Step 4/4: Build PDF ═══"
echo "   ℹ️  The HTML must be built manually (LLM-assisted step)."
echo "   ℹ️  Use TEMPLATES/paper.html as the base template."
echo "   ℹ️  Follow SOP.md for figure mapping and section structure."
echo "   ℹ️  Once HTML is ready, run:"
echo "   bash $SCRIPT_DIR/build_pdf.sh $OUTPUT_DIR/annotated.html $OUTPUT_DIR/output.pdf"

echo ""
echo "✅ Pipeline setup complete."
echo "   Output directory: $OUTPUT_DIR"
echo ""
echo "Next steps:"
echo "   1. Fill in $OUTPUT_DIR/formulas.txt with paper formulas"
echo "   2. Build annotated HTML following SOP.md"
echo "   3. Run build_pdf.sh to generate final PDF"
