#!/bin/bash
# generate-pdf.sh
# Usage: ./generate-pdf.sh input.html output.pdf
# A simple wrapper for generate-pdf.py

set -euo pipefail
IFS=$'\n\t'

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input.html> <output.pdf>"
    exit 1
fi

INPUT_HTML=$1
OUTPUT_PDF=$2

case "$INPUT_HTML" in
    *.html) ;;
    *)
        echo "Error: Input file must end with .html"
        exit 1
        ;;
esac

case "$OUTPUT_PDF" in
    *.pdf) ;;
    *)
        echo "Error: Output file must end with .pdf"
        exit 1
        ;;
esac

# Ensure playwright and dependencies are available
if ! command -v playwright &> /dev/null; then
    echo "Playwright not found. Please run 'pip install playwright' and 'playwright install chromium'."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "python3 not found."
    exit 1
fi

python3 "$(dirname "$0")/generate-pdf.py" "$INPUT_HTML" "$OUTPUT_PDF"
