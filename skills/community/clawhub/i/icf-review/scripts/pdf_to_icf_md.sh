#!/bin/bash
# pdf_to_icf_md.sh - Convert PDF ICF files to clean markdown using markitdown
# Usage: ./pdf_to_icf_md.sh <input.pdf> [output.md]

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 <input.pdf> [output.md]"
    echo "  Converts PDF ICF file to markdown, removes form feeds, reports size."
    exit 1
fi

INPUT_PDF="$1"
OUTPUT_MD="${2:-${INPUT_PDF%.pdf}.md}"

if [ ! -f "$INPUT_PDF" ]; then
    echo "Error: File '$INPUT_PDF' not found."
    exit 1
fi

echo "Converting '$INPUT_PDF' to markdown..."
markitdown "$INPUT_PDF" -o "$OUTPUT_MD"

# Remove form feed characters (\f)
sed -i 's/\x0C/ /g' "$OUTPUT_MD"

# Clean up extra blank lines that may result
sed -i '/^[[:space:]]*$/d' "$OUTPUT_MD"

INPUT_SIZE=$(stat -c%s "$INPUT_PDF" 2>/dev/null || stat -f%z "$INPUT_PDF" 2>/dev/null)
OUTPUT_SIZE=$(stat -c%s "$OUTPUT_MD" 2>/dev/null || stat -f%z "$OUTPUT_MD" 2>/dev/null)

echo ""
echo "Conversion complete!"
echo "  Input:  $INPUT_PDF ($INPUT_SIZE bytes)"
echo "  Output: $OUTPUT_MD ($OUTPUT_SIZE bytes)"
