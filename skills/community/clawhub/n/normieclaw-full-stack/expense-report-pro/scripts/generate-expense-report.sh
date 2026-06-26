#!/bin/bash
# Wrapper script for Playwright PDF generation
# Ensures the Python virtual environment is loaded and Playwright is available
set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <YYYY-MM> <output_pdf_path>"
    exit 1
fi

# Determine script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/generate-expense-report.py"

# Run the Python script
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is required but was not found in PATH."
    exit 1
fi

python3 "$PYTHON_SCRIPT" "$1" "$2"
