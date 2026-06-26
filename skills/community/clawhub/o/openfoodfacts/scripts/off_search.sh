#!/bin/bash
# Open Food Facts API - Product Search
# Usage: off_search.sh "search query" [page_size]

# Configuration
API_BASE="https://world.openfoodfacts.org/api/v2/search"

# Parse arguments
QUERY="$1"
PAGE_SIZE="${2:-10}"

if [ -z "$QUERY" ]; then
    echo "Usage: off_search.sh \"search query\" [page_size]"
    echo "  page_size: Number of results (1-100, default: 10)"
    exit 1
fi

# Validate page size
if [ "$PAGE_SIZE" -gt 100 ] || [ "$PAGE_SIZE" -lt 1 ]; then
    echo "Error: page_size must be between 1 and 100"
    exit 1
fi

# Build search URL (v2 API)
URL="${API_BASE}?q=${QUERY}&page_size=${PAGE_SIZE}"

# Make API request
RESPONSE=$(curl -s -w "\n%{http_code}" "$URL")

# Separate body and status code
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check for errors
case "$HTTP_CODE" in
    200)
        # Success
        ;;
    429)
        echo "❌ Error: Rate limit exceeded."
        echo "Search queries are limited to 10 requests per minute."
        echo "Please wait a moment before trying again."
        exit 1
        ;;
    *)
        echo "❌ Error: Unexpected HTTP status code: $HTTP_CODE"
        exit 1
        ;;
esac

# Parse and display results
PRODUCT_COUNT=$(echo "$BODY" | jq '.products | length // 0')

echo "# Search Results: \"$QUERY\""
echo ""
echo "Found: $PRODUCT_COUNT products"
echo ""

if [ "$PRODUCT_COUNT" -eq 0 ]; then
    echo "No products found matching your search query."
    echo ""
    echo "Tips:"
    echo "- Try searching in English for better results"
    echo "- Use simpler keywords (e.g., 'oat milk' instead of 'oatly barista edition')"
    exit 0
fi

# Display results as a markdown table
echo "| Product Name | Barcode | Brand |"
echo "|--------------|---------|-------|"

echo "$BODY" | jq -r '.products[]? | select(. != null) | [
    (.product_name // .product_name_en // "Unknown" | gsub("\\|"; "\\|")),
    (.code // "N/A"),
    (.brands // "N/A" | gsub("\\|"; ", "))
] | @tsv' 2>/dev/null | while IFS=$'\t' read -r name code brands; do
    # Truncate long names
    if [ "${#name}" -gt 50 ]; then
        name="${name:0:47}..."
    fi
    echo "| $name | $code | $brands |"
done

echo ""
echo "To get full nutritional details, use: ./skills/openfoodfacts/scripts/off_product.sh <barcode>"
