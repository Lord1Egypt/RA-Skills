#!/bin/bash
# Open Food Facts API - Product Lookup by Barcode
# Usage: off_product.sh <barcode>

# Configuration
API_BASE="https://world.openfoodfacts.org/api/v2/product"

# Parse arguments
BARCODE="$1"

if [ -z "$BARCODE" ]; then
    echo "Usage: off_product.sh <barcode>"
    echo "  barcode: EAN-13 or UPC barcode (8-13 digits)"
    echo ""
    echo "Examples:"
    echo "  off_product.sh 7310100027933"
    echo "  off_product.sh 5000159325954"
    echo ""
    echo "Tip: Find the barcode below the barcode lines on product packaging"
    exit 1
fi

# Validate barcode (should be numeric)
if ! echo "$BARCODE" | grep -qE '^[0-9]{8,13}$'; then
    echo "❌ Error: Invalid barcode format."
    echo "Barcode should be 8-13 digits (numeric only)."
    exit 1
fi

# Make API request
URL="${API_BASE}/${BARCODE}"
RESPONSE=$(curl -s -w "\n%{http_code}" \
    -H "User-Agent: OpenClawBot/1.0" \
    "$URL")

# Separate body and status code
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check for errors
case "$HTTP_CODE" in
    200)
        # Success - check if product exists
        STATUS=$(echo "$BODY" | jq -r '.status // 0')
        if [ "$STATUS" != "1" ]; then
            echo "❌ Product not found"
            echo ""
            echo "The barcode '$BARCODE' does not exist in the Open Food Facts database."
            echo ""
            echo "This could mean:"
            echo "- The product is not yet in the database"
            echo "- The barcode might be incorrect"
            echo ""
            echo "You can add it at: https://world.openfoodfacts.org"
            exit 1
        fi
        ;;
    429)
        echo "❌ Error: Rate limit exceeded."
        echo "Product lookups are limited to 100 requests per minute."
        echo "Please wait a moment before trying again."
        exit 1
        ;;
    *)
        echo "❌ Error: Unexpected HTTP status code: $HTTP_CODE"
        exit 1
        ;;
esac

# Parse product data
PRODUCT=$(echo "$BODY" | jq '.product')

PRODUCT_NAME=$(echo "$PRODUCT" | jq -r '.product_name // .product_name_en // "Unknown"')
BRANDS=$(echo "$PRODUCT" | jq -r '.brands // "N/A"')
QUANTITY=$(echo "$PRODUCT" | jq -r '.quantity // "N/A"')
CODE=$(echo "$PRODUCT" | jq -r '.code // "N/A"')
NUTRISCORE=$(echo "$PRODUCT" | jq -r '.nutriscore_grade // "N/A"' | tr '[:lower:]' '[:upper:]')
NOVA_GROUP=$(echo "$PRODUCT" | jq -r '.nova_group // "N/A"')

# Display product info
echo "# $PRODUCT_NAME"
echo ""
echo "**Barcode:** $CODE"
if [ "$BRANDS" != "N/A" ]; then
    echo "**Brand:** $BRANDS"
fi
if [ "$QUANTITY" != "N/A" ]; then
    echo "**Quantity:** $QUANTITY"
fi

# Display Nutri-Score
if [ "$NUTRISCORE" != "N/A" ] && [ "$NUTRISCORE" != "null" ]; then
    echo "**Nutri-Score:** $NUTRISCORE"
fi

# Display NOVA group
if [ "$NOVA_GROUP" != "N/A" ] && [ "$NOVA_GROUP" != "null" ]; then
    echo "**NOVA Group:** $NOVA_GROUP"
fi

echo ""

# Display ingredients
echo "## Ingredients"
echo ""
INGREDIENTS=$(echo "$PRODUCT" | jq -r '.ingredients_text // .ingredients_text_en // ""')
if [ -n "$INGREDIENTS" ] && [ "$INGREDIENTS" != "null" ]; then
    echo "$INGREDIENTS"
else
    echo "*No ingredient information available*"
fi
echo ""

# Display allergens
ALLERGENS=$(echo "$PRODUCT" | jq -r '.allergens // ""')
if [ -n "$ALLERGENS" ] && [ "$ALLERGENS" != "null" ] && [ "$ALLERGENS" != "" ]; then
    echo "**Allergens:** $ALLERGENS"
    echo ""
fi

# Display nutritional information
echo "## Nutritional Information (per 100g)"
echo ""

NUTRIMENTS=$(echo "$PRODUCT" | jq '.nutriments')

if [ "$NUTRIMENTS" = "null" ] || [ -z "$NUTRIMENTS" ]; then
    echo "*No nutritional information available*"
else
    echo "| Nutrient | Amount | Unit |"
    echo "|----------|--------|------|"
    
    # Extract common nutrients
    ENERGY_KCAL=$(echo "$NUTRIMENTS" | jq -r '.["energy-kcal"] // .energy_kcal // empty')
    if [ -n "$ENERGY_KCAL" ]; then
        echo "| Energy | $ENERGY_KCAL | kcal |"
    fi
    
    PROTEIN=$(echo "$NUTRIMENTS" | jq -r '.proteins // .protein // empty')
    if [ -n "$PROTEIN" ]; then
        echo "| Protein | $PROTEIN | g |"
    fi
    
    CARBS=$(echo "$NUTRIMENTS" | jq -r '.carbohydrates // .carbs // empty')
    if [ -n "$CARBS" ]; then
        echo "| Carbohydrates | $CARBS | g |"
    fi
    
    SUGARS=$(echo "$NUTRIMENTS" | jq -r '.sugars // empty')
    if [ -n "$SUGARS" ]; then
        echo "| - of which sugars | $SUGARS | g |"
    fi
    
    FAT=$(echo "$NUTRIMENTS" | jq -r '.fat // empty')
    if [ -n "$FAT" ]; then
        echo "| Fat | $FAT | g |"
    fi
    
    SATURATED=$(echo "$NUTRIMENTS" | jq -r '."saturated-fat" // .saturated_fat // empty')
    if [ -n "$SATURATED" ]; then
        echo "| - of which saturates | $SATURATED | g |"
    fi
    
    FIBER=$(echo "$NUTRIMENTS" | jq -r '.fiber // .fibers // empty')
    if [ -n "$FIBER" ]; then
        echo "| Fiber | $FIBER | g |"
    fi
    
    SALT=$(echo "$NUTRIMENTS" | jq -r '.salt // empty')
    if [ -n "$SALT" ]; then
        echo "| Salt | $SALT | g |"
    fi
    
    SODIUM=$(echo "$NUTRIMENTS" | jq -r '.sodium // empty')
    if [ -n "$SODIUM" ]; then
        echo "| Sodium | $SODIUM | g |"
    fi
fi

echo ""
echo "---"
echo "More info: https://world.openfoodfacts.org/product/$CODE"
