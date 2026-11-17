---
name: menlo-shopping
description: Use Menlo Shopping MCP to find individual products or build curated shopping lists. Use when a user asks to shop, compare products, find gifts, assemble a setup, or get product recommendations.
---

# Menlo Shopping

Use the configured `menlo-shopping` MCP server for product discovery. Amazon.com is currently supported.

## Choose a tool

- Use `search_products` for a specific item or product category. Add price, rating, and sponsored-result filters when the user gives constraints.
- Use `build_product_kit` for a goal-oriented shopping list, such as a home-office setup, a starter kit, or gift ideas. A product kit is a curated list, not a pre-bundled item.

## Search well

- Keep the query specific: include product type, intended user, style, compatibility, or material when relevant.
- Turn clear budget constraints into `max_price`; use `min_rating` only when the user asks for quality thresholds.
- Start with a small result set and expand only if the user wants more options.

## Present results

- Use returned prices, ratings, and availability facts as-is; do not invent missing details.
- Use each returned `product_url` unchanged when sharing a product.
- Briefly explain why each pick fits the user’s request.
