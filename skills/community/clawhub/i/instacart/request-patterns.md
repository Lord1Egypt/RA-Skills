# Request Patterns - Instacart

## Recipe Page Pattern

```bash
curl -s "https://connect.dev.instacart.tools/idp/v1/products/recipe" \
  -H "Authorization: Bearer $INSTACART_API_KEY" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weeknight tomato pasta",
    "image_url": "https://example.com/pasta.jpg",
    "instructions": ["Boil pasta", "Simmer sauce", "Combine and serve"],
    "ingredients": [
      {
        "name": "spaghetti",
        "measurements": [{"quantity": 1, "unit": "lb"}]
      },
      {
        "name": "crushed tomatoes",
        "filters": {"brand_filters": ["Muir Glen"]},
        "measurements": [{"quantity": 1, "unit": "can"}]
      }
    ],
    "landing_page_configuration": {
      "partner_linkback_url": "https://example.com/recipes/pasta",
      "enable_pantry_items": true
    }
  }' | jq
```

## Shopping List Pattern

```bash
curl -s "https://connect.dev.instacart.tools/idp/v1/products/products_link" \
  -H "Authorization: Bearer $INSTACART_API_KEY" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sunday staples",
    "line_items": [
      {
        "name": "bananas",
        "quantity": 6,
        "unit": "each"
      },
      {
        "name": "whole milk",
        "line_item_measurements": [{"quantity": 1, "unit": "gallon"}]
      }
    ],
    "landing_page_configuration": {
      "partner_linkback_url": "https://example.com/staples",
      "enable_pantry_items": true
    }
  }' | jq
```

## Canonicalization Rules

- Lowercase unit aliases to a supported form before hashing.
- Keep product names generic; move brand intent to filters.
- Sort filter arrays if order is not semantically meaningful.
- Strip empty optional fields before hashing or caching.
- Hash the normalized request plus environment to build URL-cache keys.

## Measurement Rules

- Prefer `each` for countable products.
- Provide multiple measurements only when truly helpful.
- Put the preferred measurement first.
- Reject zero or negative quantities before sending traffic.

## Identifier Rules

- Use `product_ids` when you already trust Instacart ids.
- Use `upcs` when UPC-priority matching is needed.
- Never send both for the same item.
- Never duplicate the same identifier across multiple items in one payload.
