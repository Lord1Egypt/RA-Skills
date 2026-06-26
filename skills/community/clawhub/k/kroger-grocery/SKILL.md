---
name: kroger-grocery
description: "Grocery ordering via Kroger-family stores (Kroger, Fred Meyer, Ralph's, Harris Teeter, King Soopers, Mariano's, QFC, Smith's, etc). Use when: (1) user asks to order groceries or add items to cart, (2) user wants to build a grocery list or meal plan with cart integration, (3) user says 'order the usual' or references a staples list, (4) user asks about product availability or prices at their local store. Requires kroget CLI and a Kroger Developer API app."
---

# Kroger Grocery Ordering

Order groceries via the Kroger API using the [kroget](https://github.com/VargasDevelopment/kroget) CLI. Works with all Kroger-family banners.

## Supported Stores

Kroger, Fred Meyer, Ralph's, Harris Teeter, King Soopers, Mariano's, QFC, Smith's, Fry's, Dillons, Baker's, City Market, Food 4 Less, Foods Co, Jay C, Owen's, Pay Less, Pick 'n Save, Metro Market, Gerbes.

## Setup

See `references/setup.md` for full first-time setup guide.

Quick version:
1. `pipx install kroget`
2. Register app at developer.kroger.com → get client_id + client_secret
3. `kroget setup --client-id ... --client-secret ...`
4. `kroget auth login` → user authorizes in browser
5. Look up store: `kroget products search "test" --location-id <zip>`

## Core Commands

### Search products
```bash
kroget products search "QUERY" --location-id STORE_ID --json
```

### Add to cart
```bash
kroget cart add --location-id STORE_ID --product-id UPC --quantity N --apply --yes
```

### Check auth
```bash
kroget doctor
```

## Workflow

### Ad-Hoc Items
User says "add milk and eggs to the cart":
1. Search each item: `kroget products search "milk" --location-id STORE_ID --json`
2. Pick the best match (or present options if ambiguous)
3. Add to cart: `kroget cart add --location-id STORE_ID --product-id UPC --quantity 1 --apply --yes`
4. Confirm what was added with prices

### Meal Planning
User asks for meal planning with grocery integration:
1. Plan meals based on preferences and dietary restrictions
2. Build ingredient list
3. Search and add each item to cart
4. Report total estimated cost
5. Remind user to open store app to schedule pickup

### Staples / "Order the Usual"
For repeat orders, maintain staples lists in a local file:
1. First time: user provides their regular items
2. Save to a staples file (JSON or markdown)
3. On repeat: search and add all staples to cart
4. Report any items out of stock or price changes

## Important Safety Rules

- **Never attempt checkout** — the API physically cannot do it, and that's a feature
- **Always report prices** before or after adding to cart
- **User must confirm pickup** in their store's app or website
- **Cart add requires `--apply`** — without it, nothing happens
- The API can **add** to cart but **cannot read** cart contents or **place orders**

## Dietary Restrictions

When the user has dietary restrictions, always vet items:
- Check product descriptions for allergens
- Search with restriction-specific terms (e.g., "gluten free pasta")
- Flag items that might contain restricted ingredients
- When in doubt, present options and let the user choose

## Token Refresh

Kroger OAuth tokens expire. kroget handles refresh automatically. If the refresh token expires (extended inactivity), user needs to re-authorize:
```bash
kroget auth login
```
Detect auth failures and prompt for re-auth.

## Notes

- Product IDs are UPCs (e.g., `0001111018221`)
- `--location-id` is required for product search and cart operations
- Each store has unique inventory and pricing
- Use `--json` flag for parseable output
- kroget stores config at `~/.kroget/` (config.json, tokens.json)
