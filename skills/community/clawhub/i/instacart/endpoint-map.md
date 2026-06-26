# Endpoint Map - Instacart

## Core REST Endpoints

| Endpoint | Method | Main inputs | Main output | Notes |
|----------|--------|-------------|-------------|-------|
| `/idp/v1/products/recipe` | `POST` | title, instructions, ingredients, landing page config | `products_link_url` | creates an Instacart-hosted recipe page |
| `/idp/v1/products/products_link` | `POST` | title, line items, optional instructions, landing page config | `products_link_url` | creates a shopping-list or product-link page |
| `/idp/v1/retailers` | `GET` | `postal_code`, `country_code` | `retailers[]` with `retailer_key` and display fields | use before user-facing link decisions |

## Request Modeling Notes

- `recipe` uses `ingredients[]` with `measurements[]`.
- `products_link` uses `line_items[]` with `line_item_measurements[]`.
- In both endpoints, `product_ids` and `upcs` are mutually exclusive.
- Both write endpoints return a URL, not an order object.

## Nearby Retailers

Retailer lookup returns organization-level retailer metadata:
- `retailer_key`
- `name`
- `retailer_logo_url`

Treat `retailer_key` as a selection hint for downstream page creation logic, not as a store inventory guarantee.

## MCP Coverage

Current official MCP coverage mirrors only two create actions:
- `create-recipe`
- `create-shopping-list`

Use REST for retailer lookup or any unsupported diagnostics.
