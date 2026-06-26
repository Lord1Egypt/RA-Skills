#!/bin/bash
# ggsql-runner.sh - Execute ggsql SQL and generate chart

set -e

INPUT_SQL="$1"
OUTPUT_FILE="${2:-chart.svg}"
FORMAT="${3:-svg}"

# Check if ggsql-cli is available
if command -v ggsql-cli &> /dev/null; then
    ggsql-cli run -f "$INPUT_SQL" -o "$OUTPUT_FILE" --format "$FORMAT"
    echo "Chart generated: $OUTPUT_FILE"
    exit 0
fi

# Fallback: use WASM playground URL
echo "ggsql-cli not installed. Use WASM playground:"
echo "https://ggsql.org/wasm/"
echo ""
echo "SQL to execute:"
cat "$INPUT_SQL"
echo ""
echo "Save output as: $OUTPUT_FILE"

# Alternative: curl to API (if available in future)
# curl -X POST https://ggsql.org/api/render \
#   -d "sql=$(cat $INPUT_SQL)" \
#   -d "format=$FORMAT" \
#   -o "$OUTPUT_FILE"

exit 1