# Shopify Data Export Reference

## Option A: CSV Export (No API Key Required)

1. In Shopify Admin → **Products → All Products**
2. Click **Export** → **All products** → **CSV for Excel/Numbers**
3. Download the CSV file

### CSV Header (Standard Export)

```
Handle,Title,Body (HTML),Vendor,Type,Tags,Published,
Option1 Name,Option1 Value,Option2 Name,Option2 Value,Option3 Name,Option3 Value,
Variant SKU,Variant Grams,Variant Inventory Tracker,Variant Inventory Qty,Variant Inventory Policy,
Variant Fulfillment Service,Variant Price,Variant Compare At Price,Variant Requires Shipping,
Variant Taxable,Variant Barcode,Image Src,Image Position,Image Alt Text,
Gift Card,SEO Title,SEO Description,Google Shopping / Google Product Category,
Google Shopping / Gender,Google Shopping / Age Group,Google Shopping / MPN,
Google Shopping / AdWords Grouping,Google Shopping / AdWords Labels,
Google Shopping / Condition,Google Shopping / Custom Product,Google Shopping / Custom Label 0,
Google Shopping / Custom Label 1,Google Shopping / Custom Label 2,Google Shopping / Custom Label 3,
Google Shopping / Custom Label 4,Variant Image,Variant Weight Unit,Variant Tax Code,Cost per item,Status
```

### Key Mappings (CSV → Mobazha)

| Shopify Field | Mobazha Field | Transform |
|---------------|---------------|-----------|
| `Handle` | — | Used for deduplication only |
| `Title` | `title` | Direct copy |
| `Body (HTML)` | `description` | Strip HTML tags |
| `Vendor` | — | Informational |
| `Type` | `categories[0]` | Map to Mobazha category |
| `Tags` | `tags[]` | Split by comma |
| `Variant Price` | `price` | Parse as decimal |
| `Variant SKU` | `variants[].sku` | Direct copy |
| `Variant Inventory Qty` | `quantity` | Parse as integer |
| `Image Src` | `images[]` | Download and re-upload |
| `Option1 Name` + `Option1 Value` | `variants[].options` | Map to Mobazha variant |
| `Variant Requires Shipping` | `shippingRequired` | `TRUE` → physical item |
| `Google Shopping / Condition` | `condition` | Map: `new`→`NEW`, `used`→`USED` |
| `Status` | — | Only import `active` products |

### Multi-Variant Products

Shopify CSV uses multiple rows per product. The first row has the title and main image; subsequent rows with the same `Handle` contain variant data.

Group rows by `Handle` to reconstruct the full product with all variants.

## Option B: Shopify Admin API

For stores with API access, use the [Products API](https://shopify.dev/docs/api/admin-rest/current/resources/product) for structured data.

### Authentication

Requires a Shopify custom app with `read_products` scope:

```
GET https://{shop}.myshopify.com/admin/api/2024-01/products.json
X-Shopify-Access-Token: {access_token}
```

### API Response → Mobazha Mapping

| Shopify API Field | Mobazha Field | Transform |
|-------------------|---------------|-----------|
| `product.title` | `title` | Direct copy |
| `product.body_html` | `description` | Strip HTML tags |
| `product.product_type` | `tags[]` | Add as tag |
| `product.tags` | `tags[]` | Split by comma |
| `product.images[].src` | `images[]` | Download URL |
| `product.variants[].price` | `price` | Use first variant or lowest |
| `product.variants[].sku` | `variants[].sku` | Direct copy |
| `product.variants[].inventory_quantity` | `quantity` | Sum across locations |
| `product.variants[].option1/2/3` | `variants[].options` | Map to Mobazha variant options |
| `product.variants[].requires_shipping` | contractType | `true` → `PHYSICAL_GOOD` |
| `product.status` | — | Only import `active` |

### Pagination

Shopify API uses cursor-based pagination:

```
GET /admin/api/2024-01/products.json?limit=250
```

Follow the `Link` header `rel="next"` until no more pages.

### Conversion Pseudocode

```python
import requests

def fetch_shopify_products(shop, token):
    url = f"https://{shop}.myshopify.com/admin/api/2024-01/products.json?limit=250&status=active"
    headers = {"X-Shopify-Access-Token": token}
    products = []

    while url:
        resp = requests.get(url, headers=headers)
        data = resp.json()
        products.extend(data["products"])
        # Follow cursor pagination
        link = resp.headers.get("Link", "")
        url = None
        if 'rel="next"' in link:
            for part in link.split(","):
                if 'rel="next"' in part:
                    url = part.split("<")[1].split(">")[0]
    return products
```
