#!/bin/bash

# OCR Tool for Unix/Linux/macOS
# Usage: ./ocr.sh [image_path] [options]

set -e

IMAGE="$1"
if [ -z "$IMAGE" ]; then
    echo "Usage: $0 <image_path> [options]"
    echo "Options:"
    echo "  --lang chi_sim+eng    Language for OCR (default: chi_sim+eng)"
    echo "  --output file.txt     Output file for extracted text"
    echo "  --detailed            Show detailed analysis"
    echo "  --extract-only        Only extract text, no analysis"
    exit 1
fi

# Parse arguments
LANG="chi_sim+eng"
OUTPUT=""
DETAILED=false
EXTRACT_ONLY=false

shift
while [[ $# -gt 0 ]]; do
    case $1 in
        --lang)
            LANG="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --detailed)
            DETAILED=true
            shift
            ;;
        --extract-only)
            EXTRACT_ONLY=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

echo "OCR Tool - Processing: $IMAGE"
echo "Language: $LANG"

if [ ! -f "$IMAGE" ]; then
    echo "Error: Image file not found: $IMAGE"
    exit 1
fi

# Check if Tesseract is installed
if ! command -v tesseract &> /dev/null; then
    echo "Error: Tesseract not found. Please install Tesseract OCR."
    echo "Install via:"
    echo "  macOS: brew install tesseract"
    echo "  Ubuntu/Debian: sudo apt install tesseract-ocr"
    echo "  Fedora: sudo dnf install tesseract"
    exit 1
fi

if [ "$EXTRACT_ONLY" = true ]; then
    if [ -z "$OUTPUT" ]; then
        # Output to console
        tesseract "$IMAGE" stdout -l "$LANG"
    else
        # Output to file
        tesseract "$IMAGE" "$OUTPUT" -l "$LANG"
        echo "Text extracted to: ${OUTPUT}.txt"
    fi
    exit 0
fi

# Full analysis
echo ""
echo "=================================================="
echo "OCR ANALYSIS REPORT"
echo "=================================================="
echo ""

# Extract text to temporary file
TEMP_FILE=$(mktemp)
tesseract "$IMAGE" "$TEMP_FILE" -l "$LANG" > /dev/null 2>&1
TEXT_FILE="${TEMP_FILE}.txt"

if [ ! -f "$TEXT_FILE" ]; then
    echo "Error: OCR failed to extract text"
    exit 1
fi

# Analyze text
TEXT=$(cat "$TEXT_FILE")
LINE_COUNT=$(wc -l < "$TEXT_FILE")

# Extract company names
COMPANIES=$(echo "$TEXT" | grep -oE '#[^ ]+' | sed 's/#//g' | sort -u)
COMPANY_COUNT=$(echo "$COMPANIES" | wc -w)

# Extract stock codes
STOCKS=$(echo "$TEXT" | grep -oE '[0-9]{6}\.[A-Z]{2,4}' | sort -u)
STOCK_COUNT=$(echo "$STOCKS" | wc -w)

# Extract financial metrics
METRICS=$(echo "$TEXT" | grep -oE '同比增长[0-9.]+%|利润[0-9.]+亿元|增长[0-9.]+%' | sort -u)
METRIC_COUNT=$(echo "$METRICS" | wc -w)

# Extract keywords
KEYWORDS="公告 知道 商业航天 智能电网 机器人 绿色电力 电气 设备 应用 领域 电力设施"
FOUND_KEYWORDS=""
for keyword in $KEYWORDS; do
    if echo "$TEXT" | grep -q "$keyword"; then
        FOUND_KEYWORDS="$FOUND_KEYWORDS $keyword"
    fi
done
KEYWORD_COUNT=$(echo "$FOUND_KEYWORDS" | wc -w)

# Display results
echo "📊 Summary:"
echo "  Total lines: $LINE_COUNT"
echo "  Companies found: $COMPANY_COUNT"
echo "  Stock codes: $STOCK_COUNT"
echo "  Financial metrics: $METRIC_COUNT"
echo "  Keywords found: $KEYWORD_COUNT"
echo ""

if [ $COMPANY_COUNT -gt 0 ]; then
    echo "🏢 Companies:"
    echo "$COMPANIES" | while read -r company; do
        [ -n "$company" ] && echo "  • $company"
    done
    echo ""
fi

if [ $STOCK_COUNT -gt 0 ]; then
    echo "📈 Stock Codes:"
    echo "$STOCKS" | while read -r stock; do
        [ -n "$stock" ] && echo "  • $stock"
    done
    echo ""
fi

if [ $METRIC_COUNT -gt 0 ]; then
    echo "💰 Financial Metrics:"
    echo "$METRICS" | while read -r metric; do
        [ -n "$metric" ] && echo "  • $metric"
    done
    echo ""
fi

if [ $KEYWORD_COUNT -gt 0 ]; then
    echo "🔑 Keywords:"
    for keyword in $FOUND_KEYWORDS; do
        echo "  • $keyword"
    done
    echo ""
fi

if [ "$DETAILED" = true ]; then
    echo "📝 Full Text (first 30 lines):"
    echo "=================================================="
    head -30 "$TEXT_FILE"
    echo "=================================================="
    echo ""
fi

# Clean up
rm -f "$TEXT_FILE"

echo "=================================================="
echo "Analysis complete"
echo "=================================================="