# Universal Field Mapping: External Platforms → Mobazha

## Import JSON Root Structure

```json
{
  "profile":          { ... },
  "listings":         [ ... ],
  "shippingProfiles": [ ... ],
  "collections":      [ ... ]
}
```

| Root Field | Type | Required | Description |
|------------|------|----------|-------------|
| `listings` | array | **Yes** | Product listings to import |
| `shippingProfiles` | array | No | Shipping profiles (required if any listing is `PHYSICAL_GOOD`) |
| `collections` | array | No | Product collections/categories to create |
| `profile` | object | No | Store profile data to set/update |

## Listing Fields (`listings[]`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `slug` | string | No | Unique URL slug; auto-generated from title if omitted |
| `title` | string | **Yes** | Product name |
| `contractType` | enum | **Yes** | `PHYSICAL_GOOD`, `DIGITAL_GOOD`, `SERVICE`, `CRYPTOCURRENCY` |
| `price` | string | **Yes** | Decimal price (e.g., `"29.99"`) |
| `pricingCurrency` | string | No | ISO 4217 code (default: `USD`) |
| `description` | string | No | Full product description (plain text or Markdown) |
| `shortDescription` | string | No | Brief summary for cards/previews |
| `productType` | string | No | Product category type |
| `tags` | string[] | No | Categorization tags |
| `condition` | enum | No | `NEW`, `USED`, `REFURBISHED` (default: `NEW`) |
| `nsfw` | bool | No | Adult content flag (default: `false`) |
| `images` | string[] | No | Filenames matching entries in the ZIP `images/` dir |
| `introVideo` | string | No | Filename of intro video in ZIP `videos/` dir |
| `processingTime` | string | No | Order processing time (e.g., `"1-3 business days"`) |
| `grams` | uint32 | No | Product weight in grams (physical goods) |
| `quantity` | string | No | Stock quantity (omit for unlimited) |
| `shippingProfileId` | string | Conditional | Required for `PHYSICAL_GOOD`; matches `shippingProfiles[].key` |
| `variants` | object[] | No | Product variants with per-variant pricing |
| `rwaTokenAddress` | string | No | RWA: token contract address |
| `rwaTokenStandard` | string | No | RWA: token standard (e.g., `ERC1155`, `ERC3525`) |
| `rwaTokenId` | string | No | RWA: token ID |
| `rwaSlotId` | string | No | RWA: slot ID (ERC3525 only) |
| `rwaBlockchain` | string | No | RWA: blockchain network |
| `rwaTradeMode` | int | No | RWA: trade mode |
| `rwaEscrowTimeoutSeconds` | uint64 | No | RWA: escrow timeout |
| `rwaAcceptedCurrencies` | string[] | No | RWA: accepted payment currencies |

## Variant Fields (`listings[].variants[]`)

Each variant represents a specific combination (e.g., Red + Large):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `selections` | map[string]string | **Yes** | Option selections, e.g., `{"Color": "Red", "Size": "S"}` |
| `price` | string | No | Variant-specific price (overrides listing price) |
| `quantity` | string | No | Variant-specific stock quantity |
| `productID` | string | No | SKU or product identifier |

Example:

```json
{
  "variants": [
    { "selections": {"Color": "Red", "Size": "S"}, "price": "24.99", "quantity": "50", "productID": "SKU-RED-S" },
    { "selections": {"Color": "Red", "Size": "M"}, "price": "24.99", "quantity": "30", "productID": "SKU-RED-M" },
    { "selections": {"Color": "Blue", "Size": "S"}, "price": "26.99", "quantity": "20", "productID": "SKU-BLU-S" }
  ]
}
```

## Collection Fields (`collections[]`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | **Yes** | Collection name |
| `description` | string | No | Collection description |
| `image` | string | No | Collection cover image filename (from ZIP `images/`) |
| `sortOrder` | string | No | Product sort order within collection |
| `published` | bool | No | Whether collection is visible (default: `true`) |
| `products` | string[] | **Yes** | List of listing slugs belonging to this collection |

Example:

```json
{
  "collections": [
    {
      "title": "Summer Sale",
      "description": "Best deals for summer",
      "image": "summer-banner.jpg",
      "products": ["beach-towel", "sunglasses", "flip-flops"]
    },
    {
      "title": "New Arrivals",
      "products": ["wireless-earbuds", "phone-case-2024"]
    }
  ]
}
```

## Shipping Profile Fields (`shippingProfiles[]`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | **Yes** | Local reference ID (used by `listings[].shippingProfileId`) |
| `name` | string | **Yes** | Display name |
| `isDefault` | bool | No | Set as default shipping profile |
| `locationGroups` | array | **Yes** | Shipping zones with options |

Example:

```json
{
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
            { "name": "Standard", "type": "FIXED_PRICE", "price": "5.00" },
            { "name": "Express", "type": "FIXED_PRICE", "price": "15.00" }
          ]
        }
      ]
    }
  ]
}
```

## Profile Fields (`profile`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | **Yes** | Store name |
| `about` | string | No | Store description |
| `shortDescription` | string | No | Brief store tagline |
| `location` | string | No | Store location |
| `nsfw` | bool | No | Adult content store |
| `vendor` | bool | No | Vendor flag |
| `moderator` | bool | No | Moderator flag |
| `visibility` | string | No | Store visibility setting |
| `colors` | object | No | Theme color overrides |
| `contactInfo` | object | No | Store contact information |

## Cross-Platform Mapping Table

| Concept | Shopify (CSV) | Shopify (API) | Amazon | Etsy | WooCommerce | Mobazha |
|---------|--------------|---------------|--------|------|-------------|---------|
| Name | `Title` | `product.title` | `#productTitle` | `title` | `name` | `title` |
| Description | `Body (HTML)` | `product.body_html` | bullets + `#productDescription` | `description` | `description` | `description` |
| Short Desc | `SEO Description` | `metafields` | — | — | `short_description` | `shortDescription` |
| Price | `Variant Price` | `variants[].price` | `.a-price-whole` | `price` | `regular_price` | `price` |
| Currency | — (store default) | `presentment_prices` | — (page locale) | `currency_code` | `currency` | `pricingCurrency` |
| Images | `Image Src` | `images[].src` | `.a-dynamic-image` | `images[].url_570xN` | `images[].src` | `images[]` |
| Video | — | — | — | `video` | — | `introVideo` |
| SKU | `Variant SKU` | `variants[].sku` | ASIN | `sku` | `sku` | `variants[].productID` |
| Stock | `Variant Inventory Qty` | `variants[].inventory_quantity` | — | `quantity` | `stock_quantity` | `quantity` |
| Category | `Type` | `product_type` | breadcrumbs | `taxonomy_id` | `categories[]` | `productType` / `tags[]` |
| Tags | `Tags` | `tags` | — | `tags` | `tags[]` | `tags[]` |
| Variants | `Option1/2/3` | `options[] + variants[]` | `#twister` | `variations[]` | `attributes[]` | `variants[].selections` |
| Weight | `Variant Grams` | `variants[].grams` | — | `item_weight` | `weight` | `grams` |
| Condition | `Google Shopping / Condition` | — | — | — | `condition` | `condition` |
| Shipping | `Variant Requires Shipping` | `requires_shipping` | — (always physical) | `shipping_template_id` | `shipping_required` | `shippingProfileId` |
| Processing | — | — | — | `processing_min/max` | — | `processingTime` |
| Collections | — | `custom_collections` | — | `shop_sections` | `categories[]` | `collections[]` |
| Status | `Status` | `status` | — | `state` | `status` | — (only import active) |

## Transform Rules

### Description Cleaning

All sources may contain HTML. Clean before import:

1. Strip HTML tags (keep line breaks as `\n`)
2. Decode HTML entities (`&amp;` → `&`)
3. Remove excessive whitespace
4. Truncate to reasonable length (Mobazha allows up to 50,000 characters)

### Price Handling

1. Parse price as decimal number
2. Remove currency symbols and formatting (`,`, spaces)
3. Store as string with 2 decimal places: `"29.99"`
4. Set `pricingCurrency` to the appropriate ISO 4217 code

### Image Processing

1. Download all image URLs to local files
2. Use high-resolution versions where available
3. Supported formats: JPEG, PNG, WebP, GIF
4. Name files consistently: `product-slug-1.jpg`, `product-slug-2.jpg`
5. Reference filenames in `listings[].images` array
6. Provide files in the ZIP `images/` directory (or via `images_base64` for MCP)

### Variant Mapping

Different platforms represent variants differently. Mobazha uses a `selections` map per variant:

| Platform | Structure | Mobazha Equivalent |
|----------|-----------|--------------------|
| Shopify | Multiple rows with `Option1 Name`/`Value` per product | One `variants[]` entry per row with `selections: {"Option1 Name": "Value"}` |
| Shopify API | `options[]` + `variants[]` with `option1/2/3` | Merge option names with values into `selections` map |
| Amazon | Dropdown selectors in `#twister` | Parse selector labels/values into `selections` map |
| Etsy | `variations[]` with `property_id` | Map property names to values in `selections` |
| WooCommerce | `attributes[]` with `options` | Map attribute name to selected option in `selections` |

Example: A Shopify product with Color=Red, Size=S becomes:

```json
{ "selections": { "Color": "Red", "Size": "S" }, "price": "24.99", "productID": "SKU-001" }
```

### Contract Type Detection

| Source Signal | Mobazha contractType |
|---------------|---------------------|
| Requires shipping / has weight | `PHYSICAL_GOOD` |
| Digital download / no shipping | `DIGITAL_GOOD` |
| Service / booking / appointment | `SERVICE` |
| Token / coin / crypto asset | `CRYPTOCURRENCY` |

### Collection Mapping

| Platform | Source | Mobazha `collections[]` |
|----------|--------|------------------------|
| Shopify | Custom Collections API or manual tags | `title` + `products` (slugs) |
| Amazon | — (no direct equivalent) | Create from category groupings |
| Etsy | Shop sections | Map section name → `title`, section listings → `products` |
| WooCommerce | Product categories | Map category name → `title`, assigned products → `products` |
