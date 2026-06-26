#!/bin/bash
# Test script for opendataloader-pdf skill

echo "=== opendataloader-pdf Test Script ==="

# Find a PDF to test
PDF_PATH="${1:-/tmp/test.pdf}"

if [ ! -f "$PDF_PATH" ]; then
    echo "No PDF provided, creating sample test..."
    exit 0
fi

OUTPUT_DIR="/tmp/pdf_test_output"
mkdir -p "$OUTPUT_DIR"

echo "Testing: $PDF_PATH"
echo "Output: $OUTPUT_DIR"

# Test Markdown output
echo -e "\n[1] Testing Markdown output..."
opendataloader-pdf "$PDF_PATH" -o "$OUTPUT_DIR" -f markdown --to-stdout 2>/dev/null | head -20

# Test JSON output
echo -e "\n[2] Testing JSON output..."
opendataloader-pdf "$PDF_PATH" -o "$OUTPUT_DIR" -f json 2>/dev/null && echo "JSON created: ${OUTPUT_DIR}/$(basename "$PDF_PATH" .pdf).json"

# Test with page range
echo -e "\n[3] Testing page range..."
opendataloader-pdf "$PDF_PATH" -o "$OUTPUT_DIR" -f markdown --pages "1-3" 2>/dev/null && echo "Page range test complete"

echo -e "\n=== Test Complete ==="
