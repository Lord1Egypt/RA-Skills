#!/usr/bin/env bash
# build_pdf.sh — Convert annotated HTML to PDF with WeasyPrint
#
# Usage: ./build_pdf.sh <input.html> <output.pdf>
# Requires: python3 with weasyprint

set -euo pipefail

HTML_FILE="${1:-}"
PDF_FILE="${2:-output.pdf}"

if [ -z "$HTML_FILE" ] || [ ! -f "$HTML_FILE" ]; then
    echo "Usage: $0 <input.html> <output.pdf>"
    exit 1
fi

echo "📄 Building PDF from: $HTML_FILE"
echo "   Output: $PDF_FILE"

# Check WeasyPrint
python3 -c "import weasyprint; print(f'   WeasyPrint {weasyprint.__version__}')" 2>/dev/null || {
    echo "Error: weasyprint not installed. Run: pip3 install weasyprint"
    exit 1
}

# Build PDF
python3 -c "
from weasyprint import HTML
import os

html = HTML(filename='${HTML_FILE}')
html.write_pdf('${PDF_FILE}')
size_kb = os.path.getsize('${PDF_FILE}') / 1024
pages = '?'  # WeasyPrint doesn't easily report page count
print(f'   Size: {size_kb:.0f} KB')
"

echo "✅ PDF generated: $PDF_FILE"
