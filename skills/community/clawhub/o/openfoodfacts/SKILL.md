---
name: openfoodfacts
description: Interact with the Open Food Facts API to search for packaged food products by barcode and retrieve nutritional information. Use when the user asks to look up branded packaged foods (soft drinks, snacks, frozen meals, etc.), scan barcodes for nutrition data, or find products sold in stores with packaging. Only contains products with barcodes - does NOT include fresh produce, generic ingredients, or unpackaged foods. No API key required.
metadata: {"openclaw": {"requires": {"bins": ["curl", "jq"]}}}
---

# Open Food Facts API Skill

This skill provides access to the Open Food Facts database - a global, crowd-sourced food products database with strong European coverage.

## Key Features

- **Global coverage**: Products from 150+ countries, with strong European presence
- **No API key required**: Free to use for basic queries
- **Barcode lookup**: Look up products by EAN/UPC barcode
- **Multi-language support**: Product data available in many languages
- **Real-time data**: Community-maintained with frequent updates

## Important Limitations

**Packaged Products Only**: Open Food Facts only contains products with barcodes (EAN/UPC). This means:
- ✅ Packaged foods: soft drinks, chocolate, bread, frozen meals, etc.
- ❌ Fresh produce without packaging: meat from the butcher, loose vegetables, fresh seafood
- ❌ Generic ingredients: "apples", "chicken breast", "rice" (unless packaged by a brand)

**Data Quality**: Since this is crowd-sourced data, accuracy and completeness vary by product. Some products may have incomplete nutritional information.

**Rate Limits**:
- 100 requests/minute for product lookups (by barcode)
- 10 requests/minute for search queries
- No limits on write operations (contributing data)

**Geographic Bias**: While global, coverage is strongest in Europe (especially France, where the project started) and North America.

## API Usage

All API requests are made to `https://world.openfoodfacts.org/api/v2`.

## Commands

### Search Products

Search for food products by name or keyword.

**Usage:**
```bash
./skills/openfoodfacts/scripts/off_search.sh "search query" [page_size]
```

**Parameters:**
- `search query` (required): Keywords to search for (e.g., "chocolate bar")
- `page_size` (optional): Number of results (1-100, default: 10)

**Example:**
```bash
./skills/openfoodfacts/scripts/off_search.sh "chocolate bar"
./skills/openfoodfacts/scripts/off_search.sh "oat milk" 20
```

**Response Format:**
Returns a formatted table with:
- Product name
- Barcode
- Brand

### Get Product by Barcode

Retrieve detailed product information including full nutritional data using a barcode (EAN/UPC).

**Usage:**
```bash
./skills/openfoodfacts/scripts/off_product.sh <barcode>
```

**Parameters:**
- `barcode` (required): The EAN-13 or UPC barcode number (usually 8-13 digits)

**Example:**
```bash
./skills/openfoodfacts/scripts/off_product.sh 5000159325954
./skills/openfoodfacts/scripts/off_product.sh 7622210449283
```

**Response Format:**
Returns formatted output with:
- Product name and brand
- Packaging and quantity
- Nutritional information per 100g
- Ingredients (when available)
- Allergens and labels
- Nutri-Score (if available)
- NOVA group (food processing classification)

## Finding Barcodes

Barcodes (EAN-13, UPC) are typically found:
- On the product packaging, below the barcode lines
- On receipts or invoices
- In grocery store apps after scanning
- On product websites

Barcodes are numeric and usually 8-13 digits long.

## Error Handling

Common errors:
- **Product not found**: Barcode doesn't exist in database
- **Rate limit exceeded**: Too many requests - wait before retrying
- **Malformed barcode**: Barcode format is invalid

## Workflow Examples

### Example 1: Find nutrition for a packaged product

1. Find the barcode on the product packaging (12-13 digit number below the barcode lines)
2. Lookup the product: `./skills/openfoodfacts/scripts/off_product.sh 5000159325954`

### Example 2: Search for a product type

1. Search by name: `./skills/openfoodfacts/scripts/off_search.sh "dark chocolate"`
2. Note the barcode from results
3. Get full details: `./skills/openfoodfacts/scripts/off_product.sh <barcode>`

## Nutri-Score Reference

Products may include a Nutri-Score grade:
- **A** (dark green): Best nutritional quality
- **B** (light green): Good nutritional quality
- **C** (yellow): Average nutritional quality
- **D** (orange): Poor nutritional quality
- **E** (red): Worst nutritional quality

## NOVA Classification

Indicates level of food processing:
- **Group 1**: Unprocessed/minimally processed foods
- **Group 2**: Processed culinary ingredients
- **Group 3**: Processed foods
- **Group 4**: Ultra-processed foods

## Notes

- Results are formatted for readability (no raw JSON dumps)
- Nutritional values are typically per 100g or per serving
- Ingredients may be listed in multiple languages
- Some products have photos available via the website
