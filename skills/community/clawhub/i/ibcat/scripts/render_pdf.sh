#!/bin/bash
#
# render_pdf.sh - Phase 3: Generate final bilingual PDF with translations
# Run this AFTER translating segments and merging into translations.json
#
# Usage:
#   bash render_pdf.sh \
#     --input "input.pdf" \
#     --output-dir "/workspace/output" \
#     --work-dir "/data/user/work/translate_work" \
#     --port 8899
#

set -euo pipefail

INPUT=""
OUTPUT_DIR="/workspace/translate_output"
WORK_DIR="/data/user/work/translate_work"
PROXY_PORT=8899
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

while [[ $# -gt 0 ]]; do
    case $1 in
        --input)       INPUT="$2"; shift 2 ;;
        --output-dir)  OUTPUT_DIR="$2"; shift 2 ;;
        --work-dir)    WORK_DIR="$2"; shift 2 ;;
        --port)        PROXY_PORT="$2"; shift 2 ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

TRANSLATIONS_FILE="$WORK_DIR/translations.json"

if [[ ! -f "$TRANSLATIONS_FILE" ]]; then
    echo "ERROR: translations.json not found at $TRANSLATIONS_FILE"
    echo "Please complete Phase 2 (translation) first."
    exit 1
fi

TRANSLATION_COUNT=$(python3 -c "import json; print(len(json.load(open('$TRANSLATIONS_FILE'))))")
echo "============================================"
echo "  Phase 3: Render Bilingual PDF"
echo "============================================"
echo "  Input:        $INPUT"
echo "  Output:       $OUTPUT_DIR"
echo "  Translations: $TRANSLATION_COUNT entries"
echo "  Work dir:     $WORK_DIR"
echo "  Port:         $PROXY_PORT"
echo "============================================"
echo ""

# Step 1: Clear BabelDOC translation cache (CRITICAL!)
echo "[Step 1] Clearing BabelDOC translation cache..."
rm -f /root/.cache/babeldoc/cache.v1.db
echo "  Cache cleared."

# Step 2: Kill any existing proxy
kill $(lsof -ti:$PROXY_PORT 2>/dev/null) 2>/dev/null || true
sleep 1

# Step 3: Start proxy in translate mode
echo "[Step 2] Starting proxy in TRANSLATE mode..."
PROXY_MODE=translate PROXY_PORT=$PROXY_PORT WORK_DIR="$WORK_DIR" \
    python3 "$SCRIPT_DIR/proxy_server.py" > "$WORK_DIR/proxy_translate.log" 2>&1 &
PROXY_PID=$!
sleep 2

# Verify proxy
if ! curl -s "http://127.0.0.1:$PROXY_PORT/v1/models" | grep -q "gpt-4o-mini"; then
    echo "ERROR: Proxy failed to start"
    cat "$WORK_DIR/proxy_translate.log"
    exit 1
fi
echo "  Proxy running (PID: $PROXY_PID)"

# Step 4: Run BabelDOC
echo "[Step 3] Running BabelDOC (render phase)..."
BABELDOC_WORK="$WORK_DIR/babeldoc_render"
rm -rf "$BABELDOC_WORK"
mkdir -p "$BABELDOC_WORK"

babeldoc \
    --files "$INPUT" \
    --lang-in en \
    --lang-out zh-cn \
    --openai \
    --openai-base-url "http://127.0.0.1:$PROXY_PORT/v1" \
    --openai-api-key dummy-key \
    --openai-model gpt-4o-mini \
    --output "$OUTPUT_DIR" \
    --working-dir "$BABELDOC_WORK" \
    --no-auto-extract-glossary \
    --skip-scanned-detection \
    --no-watermark \
    --qps 100 \
    2>&1 | tail -30

# Step 5: Check for unknown segments
UNKNOWN_FILE="$WORK_DIR/unknown_segments.json"
if [[ -f "$UNKNOWN_FILE" ]]; then
    UNKNOWN_COUNT=$(python3 -c "import json; print(len(json.load(open('$UNKNOWN_FILE'))))" 2>/dev/null || echo "0")
    echo ""
    echo "[Step 4] Unknown (untranslated) segments: $UNKNOWN_COUNT"
    if [[ "$UNKNOWN_COUNT" -gt 0 ]]; then
        echo "  WARNING: Some segments were not found in translations.json"
        echo "  These will appear in English in the output PDF."
    fi
else
    echo ""
    echo "[Step 4] All segments translated successfully!"
fi

# Step 6: Stop proxy
kill $PROXY_PID 2>/dev/null || true
echo ""
echo "Proxy stopped."

# Step 7: List output files
echo ""
echo "============================================"
echo "  Output Files"
echo "============================================"
find "$OUTPUT_DIR" -name "*.pdf" -exec ls -lh {} \;

# Step 8: Verify PDF
echo ""
echo "[Step 5] Verifying PDF..."
DUAL_PDF=$(find "$OUTPUT_DIR" -name "*.dual.pdf" | head -1)
if [[ -n "$DUAL_PDF" ]]; then
    python3 "$SCRIPT_DIR/verify_pdf.py" "$DUAL_PDF" --pages 1-10
fi

echo ""
echo "============================================"
echo "  DONE!"
echo "============================================"
