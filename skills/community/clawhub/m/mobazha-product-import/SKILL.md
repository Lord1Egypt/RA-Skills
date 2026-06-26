---
name: product-import
description: Import products from Shopify, Amazon, Etsy, or CSV into a Mobazha store. Use when the user wants to migrate or copy listings from another platform.
---

# Product Import

Import products from Shopify, Amazon, Etsy, and other e-commerce platforms into your Mobazha store.

## Overview

This skill helps you migrate or copy product listings from existing platforms into Mobazha. Two approaches are available:

- **Bulk Import (recommended)** — package products as a ZIP with JSON + images and upload in one call
- **Individual Create** — create listings one at a time via the Admin API

## Bulk Import via MCP Tool

If the store is connected via MCP, use the `listings_import_json` tool for the fastest bulk import:

```json
{
  "import_json": "{\"listings\":[...], \"shippingProfiles\":[...]}",
  "images_base64": "{\"photo1.jpg\":\"<base64>\",\"photo2.jpg\":\"<base64>\"}"
}
```

The tool builds a ZIP archive internally and uploads it to `POST /v1/listings/import/json`.

### import_json Schema

```json
{
  "listings": [
    {
      "slug": "unique-product-slug",
      "title": "Product Name",
      "contractType": "PHYSICAL_GOOD",
      "price": "29.99",
      "pricingCurrency": "USD",
      "description": "Product description",
      "shortDescription": "Brief summary",
      "productType": "Clothing",
      "tags": ["tag1", "tag2"],
      "condition": "NEW",
      "nsfw": false,
      "images": ["photo1.jpg", "photo2.jpg"],
      "introVideo": "demo.mp4",
      "processingTime": "1-3 business days",
      "grams": 500,
      "quantity": "100",
      "shippingProfileId": "Standard Shipping",
      "variants": [
        { "selections": {"Color": "Red", "Size": "S"}, "price": "24.99", "quantity": "50", "productID": "SKU-RED-S" },
        { "selections": {"Color": "Blue", "Size": "S"}, "price": "26.99", "quantity": "30", "productID": "SKU-BLU-S" }
      ]
    }
  ],
  "shippingProfiles": [
    {
      "key": "Standard Shipping",
      "name": "Standard Shipping",
      "isDefault": true,
      "locationGroups": [
        {
          "name": "Worldwide",
          "locations": [{ "country": "ALL" }],
          "shippingOptions": [
            { "name": "Standard", "type": "FIXED_PRICE", "price": "5.00" }
          ]
        }
      ]
    }
  ],
  "collections": [
    {
      "title": "Summer Collection",
      "description": "Best summer products",
      "image": "summer-banner.jpg",
      "products": ["unique-product-slug"]
    }
  ],
  "profile": {
    "name": "Store Name",
    "about": "Store description",
    "shortDescription": "Brief tagline",
    "location": "New York, US"
  }
}
```

### Contract Types

| Type | Notes |
|------|-------|
| `PHYSICAL_GOOD` | Requires `shippingProfileId` matching a profile key/name |
| `DIGITAL_GOOD` | No shipping needed |
| `SERVICE` | No shipping needed |
| `CRYPTOCURRENCY` | Token/coin listings (supports RWA fields) |

### Variants

Each variant uses a `selections` map (not separate name/options fields):

```json
{ "selections": {"Color": "Red", "Size": "M"}, "price": "24.99", "quantity": "50", "productID": "SKU-001" }
```

### Collections

Group products into collections by referencing their slugs:

```json
{ "title": "New Arrivals", "products": ["product-slug-1", "product-slug-2"] }
```

For the complete field reference, see [`references/mapping.md`](references/mapping.md).

### Image Handling

Images referenced in `listings[].images` must be provided as base64-encoded data in the `images_base64` parameter. The filenames must match exactly.

To prepare images:

1. Download product images from the source platform
2. Base64-encode each image file
3. Build the `images_base64` JSON map: `{"filename.jpg": "<base64-data>"}`

## Bulk Import via Direct API

For non-MCP contexts (e.g., shell scripts), build a ZIP file manually:

### ZIP Structure

```
my-import/
├── listings.json          # Required: product data + shipping profiles
├── profile.json           # Optional: store profile data
├── images/                # Product images referenced in listings.json
│   ├── photo1.jpg
│   ├── photo2.png
│   └── ...
└── videos/                # Optional: intro videos
    └── demo.mp4
```

### Upload

```bash
curl -X POST "https://your-store.example.com/v1/listings/import/json" \
  -H "Authorization: Bearer <token>" \
  -F "file=@my-import.zip"
```

### Response

```json
{
  "data": {
    "total": 10,
    "created": 8,
    "updated": 2,
    "failed": 0,
    "createdItems": [{ "slug": "product-1", "title": "Product 1" }],
    "updatedItems": [{ "slug": "product-2", "title": "Product 2" }],
    "errors": []
  }
}
```

## References

Detailed per-platform extraction guides and field mappings are in the `references/` directory:

| File | Description |
|------|-------------|
| [`references/shopify-api.md`](references/shopify-api.md) | Shopify CSV export and Admin API data extraction |
| [`references/amazon-scrape.md`](references/amazon-scrape.md) | Amazon product page scraping with BeautifulSoup |
| [`references/mapping.md`](references/mapping.md) | Universal field mapping table (all platforms → Mobazha) |

## Supported Sources

| Source | Method | Notes |
|--------|--------|-------|
| Shopify | CSV export or API | See [`references/shopify-api.md`](references/shopify-api.md) |
| Amazon | Web scraping | See [`references/amazon-scrape.md`](references/amazon-scrape.md) |
| Etsy | CSV export or API | Export from Etsy Shop Manager |
| WooCommerce | CSV/JSON export | Export from WooCommerce admin |
| Generic CSV | Manual | Any CSV with title, description, price, images |

## Method 1: Shopify Import

1. Export products via CSV or API — see [`references/shopify-api.md`](references/shopify-api.md) for details
2. Transform to Mobazha format — see [`references/mapping.md`](references/mapping.md) for field mapping
3. Download all product images locally
4. Build the `listings.json` (include `shippingProfiles` for physical goods)
5. Upload via `listings_import_json` MCP tool or direct ZIP API

## Method 2: Amazon Product Import

1. Collect product URLs or ASINs to import
2. Extract product data — see [`references/amazon-scrape.md`](references/amazon-scrape.md) for scraping code and DOM selectors
3. Transform to Mobazha JSON format — see [`references/mapping.md`](references/mapping.md)
4. Download images locally (use high-res URLs: replace `_AC_US40_` with `_AC_SL1500_`)
5. Upload via `listings_import_json` MCP tool or direct ZIP API

**Important**: Respect robots.txt and rate limits; use 3-5 second delays between requests; verify pricing before import

## Method 3: Individual Listing Create

For small imports (< 10 products), create listings one at a time via the `listings_create` MCP tool:

```json
{
  "listing_json": "{\"slug\":\"my-product\",\"metadata\":{\"contractType\":\"DIGITAL_GOOD\",...},\"item\":{\"title\":\"...\",\"price\":\"9.99\",...}}"
}
```

Or via the Admin API:

```
POST /v1/listings
Content-Type: application/json
Authorization: Bearer <token>
```

Images must be uploaded first via `POST /v1/media` to obtain content hashes.

## Authentication

### MCP Connection

If the store is connected via MCP (recommended), authentication is handled automatically through the MCP session token.

### Direct API Access

For direct API calls, authenticate via OAuth to obtain a Bearer token, then include it in the `Authorization` header.

## Rate Considerations

- Bulk import handles rate management internally — one ZIP upload imports all products
- For individual creates, process one at a time and wait for each to succeed
- Report progress to the user (e.g., "Created 15/50 listings...")
- Large ZIP files (100+ products with images) may take 30-60 seconds to process

## Credential Handling

- Never store, log, or display API keys or passwords after use
- For Shopify/Etsy API access, the user should provide their own API keys
- MCP tokens are session-scoped and managed by the platform

## Limitations

- Product reviews cannot be imported (they are store-specific)
- Physical goods require shipping profiles — include them in the import JSON
- Payment options are set at the store level, not per-product
- Digital product files must be re-uploaded to Mobazha
- Maximum ZIP size: 300 MB (configurable)
- Maximum video size per listing: 15 MB
