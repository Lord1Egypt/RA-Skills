# Grocery Shopping - Kroger Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `grocery-shopping-kroger`

x402 availability: not enabled for this product.

## `add_to_cart`

Action slug: `add-to-cart`

Price: `5` credits

Add items to the user's Kroger online cart. Requires user Kroger account connection.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `items` | `array` | yes | Items to add to cart |

Sample parameters:

```json
{
  "items": [
    {
      "modality": "PICKUP",
      "quantity": 1,
      "upc": "example upc"
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "items": {
    "description": "Items to add to cart",
    "items": {
      "properties": {
        "modality": {
          "description": "Fulfillment method (defaults to user's Kroger account preference)",
          "enum": [
            "PICKUP",
            "DELIVERY"
          ],
          "required": false,
          "type": "string"
        },
        "quantity": {
          "description": "Quantity to add",
          "minimum": 1,
          "required": true,
          "type": "integer"
        },
        "upc": {
          "description": "Product UPC code from search or product detail results",
          "required": true,
          "type": "string"
        }
      },
      "type": "object"
    },
    "required": true,
    "type": "array"
  }
}
```

## `find_stores`

Action slug: `find-stores`

Price: `5` credits

Find nearby Kroger-family stores. User location (zip code) is injected automatically.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chain` | `string` | no | Filter by chain name (Kroger, Ralphs, Fred Meyer, King Soopers, Harris Teeter, etc.) |
| `limit` | `integer` | no | Maximum number of stores to return (default 10, max 50) |
| `radius_miles` | `integer` | no | Search radius in miles (default 10) |

Sample parameters:

```json
{
  "chain": "example chain",
  "limit": 1,
  "radius_miles": 1
}
```

Generated JSON parameter schema:

```json
{
  "chain": {
    "description": "Filter by chain name (Kroger, Ralphs, Fred Meyer, King Soopers, Harris Teeter, etc.)",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Maximum number of stores to return (default 10, max 50)",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "radius_miles": {
    "description": "Search radius in miles (default 10)",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `get_product_details`

Action slug: `get-product-details`

Price: `5` credits

Get detailed product information including full nutrition, allergens, ratings, images, and aisle locations.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `location_id` | `string` | no | Store location ID for local pricing and aisle info |
| `product_id` | `string` | yes | Kroger product ID |

Sample parameters:

```json
{
  "location_id": "example location id",
  "product_id": "example product id"
}
```

Generated JSON parameter schema:

```json
{
  "location_id": {
    "description": "Store location ID for local pricing and aisle info",
    "required": false,
    "type": "string"
  },
  "product_id": {
    "description": "Kroger product ID",
    "required": true,
    "type": "string"
  }
}
```

## `search_products`

Action slug: `search-products`

Price: `5` credits

Search the Kroger product catalog. You MUST call find_stores first to get a location_id. Supports batch search with pipe-separated queries, allergen filtering, nutrition filters, and SNAP eligibility.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `allergen_free` | `array` | no | Filter to products free from these allergens |
| `brand` | `string` | no | Filter by brand name |
| `limit` | `integer` | no | Results per page (default 10, max 50) |
| `location_id` | `string` | yes | Store location ID from find_stores. REQUIRED for pricing and availability. |
| `max_calories` | `number` | no | Max calories per serving |
| `max_carbohydrate_g` | `number` | no | Max total carbohydrate grams per serving |
| `max_cholesterol_mg` | `number` | no | Max cholesterol mg per serving |
| `max_sodium_mg` | `number` | no | Max sodium mg per serving |
| `max_sugar_g` | `number` | no | Max sugar grams per serving |
| `max_total_fat_g` | `number` | no | Max total fat grams per serving |
| `min_fiber_g` | `number` | no | Min dietary fiber grams per serving |
| `min_protein_g` | `number` | no | Min protein grams per serving |
| `query` | `string` | yes | Product search term. For a single item: "chicken thighs". For multiple items, separate with \| (pipe): "chicken thighs \| olive oil \| garlic". Max 25 items per batch. |
| `snap_eligible_only` | `boolean` | no | Only return SNAP/EBT eligible products |
| `start` | `integer` | no | Pagination offset |

Sample parameters:

```json
{
  "allergen_free": [
    "gluten"
  ],
  "brand": "example brand",
  "limit": 1,
  "location_id": "example location id",
  "max_calories": 0,
  "max_carbohydrate_g": 0,
  "max_cholesterol_mg": 0,
  "max_sodium_mg": 0
}
```

Generated JSON parameter schema:

```json
{
  "allergen_free": {
    "description": "Filter to products free from these allergens",
    "items": {
      "enum": [
        "gluten",
        "wheat",
        "dairy",
        "milk",
        "lactose",
        "egg",
        "peanut",
        "tree_nut",
        "soy",
        "fish",
        "shellfish",
        "sesame",
        "corn",
        "mustard",
        "celery",
        "lupine",
        "sulfite"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "brand": {
    "description": "Filter by brand name",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Results per page (default 10, max 50)",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "location_id": {
    "description": "Store location ID from find_stores. REQUIRED for pricing and availability.",
    "required": true,
    "type": "string"
  },
  "max_calories": {
    "description": "Max calories per serving",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "max_carbohydrate_g": {
    "description": "Max total carbohydrate grams per serving",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "max_cholesterol_mg": {
    "description": "Max cholesterol mg per serving",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "max_sodium_mg": {
    "description": "Max sodium mg per serving",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "max_sugar_g": {
    "description": "Max sugar grams per serving",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "max_total_fat_g": {
    "description": "Max total fat grams per serving",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "min_fiber_g": {
    "description": "Min dietary fiber grams per serving",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "min_protein_g": {
    "description": "Min protein grams per serving",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "query": {
    "description": "Product search term. For a single item: \"chicken thighs\". For multiple items, separate with | (pipe): \"chicken thighs | olive oil | garlic\". Max 25 items per batch.",
    "required": true,
    "type": "string"
  },
  "snap_eligible_only": {
    "description": "Only return SNAP/EBT eligible products",
    "required": false,
    "type": "boolean"
  },
  "start": {
    "description": "Pagination offset",
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```
