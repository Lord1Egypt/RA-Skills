#!/bin/bash
#
# translate_pdf.sh - One-shot PDF bilingual translation using BabelDOC
#
# Usage:
#   bash translate_pdf.sh \
#     --input "input.pdf" \
#     --output-dir "/workspace/output" \
#     --lang-in en \
#     --lang-out zh-cn \
#     --work-dir "/data/user/work/translate_work"
#
# This script automates Phase 1 (extract) and Phase 3 (render) of the
# BabelDOC translation pipeline. Phase 2 (translation) must be done
# separately using LLM sub-agents (see SKILL.md for details).
#

set -euo pipefail

# Default values
INPUT=""
OUTPUT_DIR="/workspace/translate_output"
LANG_IN="en"
LANG_OUT="zh-cn"
WORK_DIR="/data/user/work/translate_work"
PROXY_PORT=8899
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --input)       INPUT="$2"; shift 2 ;;
        --output-dir)  OUTPUT_DIR="$2"; shift 2 ;;
        --lang-in)     LANG_IN="$2"; shift 2 ;;
        --lang-out)    LANG_OUT="$2"; shift 2 ;;
        --work-dir)    WORK_DIR="$2"; shift 2 ;;
        --port)        PROXY_PORT="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: bash translate_pdf.sh --input <pdf> [options]"
            echo "  --input       Path to input PDF (required)"
            echo "  --output-dir  Output directory (default: /workspace/translate_output)"
            echo "  --lang-in     Source language (default: en)"
            echo "  --lang-out    Target language (default: zh-cn)"
            echo "  --work-dir    Working directory (default: /data/user/work/translate_work)"
            echo "  --port        Proxy port (default: 8899)"
            exit 0 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [[ -z "$INPUT" ]]; then
    echo "ERROR: --input is required"
    exit 1
fi

if [[ ! -f "$INPUT" ]]; then
    echo "ERROR: Input file not found: $INPUT"
    exit 1
fi

echo "============================================"
echo "  BabelDOC PDF Bilingual Translation"
echo "============================================"
echo "  Input:     $INPUT"
echo "  Output:    $OUTPUT_DIR"
echo "  Language:  $LANG_IN -> $LANG_OUT"
echo "  Work dir:  $WORK_DIR"
echo "  Port:      $PROXY_PORT"
echo "============================================"
echo ""

# Step 0: Ensure BabelDOC is installed
if ! command -v babeldoc &> /dev/null; then
    echo "[Step 0] Installing BabelDOC..."
    pip install babeldoc --break-system-packages -q
fi

# Step 1: Apply font patches
echo "[Step 1] Applying font patches..."
python3 "$SCRIPT_DIR/setup_fonts.py"

# Step 2: Clear old caches
echo "[Step 2] Clearing old caches..."
rm -f /root/.cache/babeldoc/cache.v1.db
mkdir -p "$WORK_DIR"
rm -f "$WORK_DIR/segments.json" "$WORK_DIR/translations.json" "$WORK_DIR/unknown_segments.json"

# Step 3: Kill any existing proxy on the port
kill $(lsof -ti:$PROXY_PORT 2>/dev/null) 2>/dev/null || true
sleep 1

# Step 4: Start proxy in extract mode
echo "[Step 3] Starting proxy in EXTRACT mode..."
PROXY_MODE=extract PROXY_PORT=$PROXY_PORT WORK_DIR="$WORK_DIR" \
    python3 "$SCRIPT_DIR/proxy_server.py" > "$WORK_DIR/proxy_extract.log" 2>&1 &
PROXY_PID=$!
sleep 2

# Verify proxy is running
if ! curl -s "http://127.0.0.1:$PROXY_PORT/v1/models" | grep -q "gpt-4o-mini"; then
    echo "ERROR: Proxy server failed to start"
    cat "$WORK_DIR/proxy_extract.log"
    exit 1
fi
echo "  Proxy running (PID: $PROXY_PID)"

# Step 5: Run BabelDOC in extract mode
echo "[Step 4] Running BabelDOC (extract phase)..."
BABELDOC_WORK="$WORK_DIR/babeldoc_extract"
mkdir -p "$BABELDOC_WORK"
rm -rf "$BABELDOC_WORK"

babeldoc \
    --files "$INPUT" \
    --lang-in "$LANG_IN" \
    --lang-out "$LANG_OUT" \
    --openai \
    --openai-base-url "http://127.0.0.1:$PROXY_PORT/v1" \
    --openai-api-key dummy-key \
    --openai-model gpt-4o-mini \
    --output "$OUTPUT_DIR/extract" \
    --working-dir "$BABELDOC_WORK" \
    --no-auto-extract-glossary \
    --skip-scanned-detection \
    --no-watermark \
    --qps 100 \
    2>&1 | tail -20

# Step 6: Check extracted segments
SEGMENT_COUNT=$(python3 -c "import json; d=json.load(open('$WORK_DIR/segments.json')); print(len(d))" 2>/dev/null || echo "0")
echo ""
echo "[Step 5] Extracted $SEGMENT_COUNT text segments"
echo ""
echo "============================================"
echo "  PHASE 1 COMPLETE: Text segments extracted"
echo "============================================"
echo ""
echo "Segments file: $WORK_DIR/segments.json"
echo ""
echo "NEXT STEPS:"
echo "  1. Split segments into batches (max 260 per batch, 3 batches max):"
echo "     python3 $SCRIPT_DIR/split_segments.py $WORK_DIR/segments.json $WORK_DIR"
echo ""
echo "  2. Translate each batch using LLM sub-agents"
echo "     -> Output: $WORK_DIR/translations_batch_1.json, _2.json, _3.json"
echo ""
echo "  3. Merge translations:"
echo "     python3 -c \"import json; t={}; [t.update(json.load(open(f'$WORK_DIR/translations_batch_{i}.json'))) for i in range(1,4)]; json.dump(t, open(f'$WORK_DIR/translations.json','w'), ensure_ascii=False, indent=2)\""
echo ""
echo "  4. Run render phase:"
echo "     bash $SCRIPT_DIR/translate_pdf.sh --render-only \\"
echo "       --input \"$INPUT\" --output-dir \"$OUTPUT_DIR\" \\"
echo "       --work-dir \"$WORK_DIR\" --port $PROXY_PORT"
echo ""

# Kill extract proxy
kill $PROXY_PID 2>/dev/null || true
echo "Extract proxy stopped."
echo ""
echo "Run '--render-only' after completing translation to generate final PDF."
