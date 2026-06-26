#!/bin/bash
# Wrapper for PDF generation
set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Usage: ./generate-invoice-pdf.sh <input.html> <output.pdf>"
    exit 1
fi

python3 "$(dirname "$0")/generate-invoice-pdf.py" "$1" "$2"
