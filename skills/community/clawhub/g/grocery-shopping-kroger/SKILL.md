---
name: grocery-shopping-kroger
description: "Grocery Shopping - Kroger: Search grocery products with advanced dietary filtering across 2700+ Kroger family stores. Use when an agent needs grocery shopping kroger, grocery shopping kroger, search grocery products by name or brand, filter products by allergens like gluten dairy egg peanut soy, find low calorie or low sugar groceries with nutrition filters, search for high protein or high fiber foods, add to cart, items through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/grocery-shopping-kroger
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/grocery-shopping-kroger"}}
---
# Grocery Shopping - Kroger

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Search products, find stores, and add items to your cart across 2700+ Kroger family stores including Kroger, Ralphs, Fred Meyer, King Soopers, and more. Features batch search (pass an array of items to search all at once), allergen filtering (gluten, dairy, egg, peanut, tree nut, soy, fish, shellfish, sesame, corn, mustard, celery, lupine, sulfite), nutrition filters (max calories, fat, sugar, sodium, cholesterol, carbs; min protein, fiber), SNAP/EBT eligibility filter, and full product details including nutrition panels, allergen data, and ratings.

## Product Instructions
### Kroger Grocery

Search products, find stores, and add items to your cart across 2700+ Kroger-family stores including Kroger, Ralphs, Fred Meyer, King Soopers, Harris Teeter, and more.

#### Overview

This tool connects to the Kroger API to search their product catalog, find nearby stores, get detailed product information with nutrition and allergen data, and add items to a user's Kroger cart. It supports batch product searches (up to 25 items at once), dietary and allergen filtering, nutrition threshold filtering, and SNAP/EBT eligibility filtering. Products are filtered to only show items available both in-store and for delivery.

#### Actions

##### find_stores

Find nearby Kroger-family stores. The user's location (zip code) is injected automatically by the platform.

**Required parameters:** None (zip code is injected automatically)

**Optional parameters:**
- `radius_miles` (integer, 1-100, default 10) -- search radius in miles
- `limit` (integer, 1-50, default 10) -- maximum number of stores to return
- `chain` (string) -- filter by chain name (e.g. `Kroger`, `Ralphs`, `Fred Meyer`, `King Soopers`, `Harris Teeter`)

**Example -- find nearest stores:**
```json
{"action":"find_stores"}
```

**Example -- find Ralphs stores within 25 miles:**
```json
{"action":"find_stores","chain":"Ralphs","radius_miles":25}
```

Returns: `stores[]` (with `location_id`, `chain`, `name`, `phone`, `address` {`line1`, `city`, `state`, `zip_code`}, `latitude`, `longitude`, `open_24h`, `timezone`, `departments[]`), `total`

---

##### search_products

Search the Kroger product catalog. You MUST call `find_stores` first to get a `location_id`, then pass it to every search. Without a `location_id`, products will have no pricing or availability and results will be empty.

**Required parameters:**
- `query` (string) -- search term. For a single item: `"chicken thighs"`. To search multiple items at once, separate with `|` (pipe): `"chicken thighs | olive oil | garlic | spinach"`. Max 25 items per batch.
- `location_id` (string) -- store location ID from `find_stores`

**Optional parameters:**
- `brand` (string) -- filter by brand name
- `limit` (integer, 1-50, default 10) -- results per query
- `start` (integer) -- pagination offset
- `allergen_free` (array of strings) -- filter to products free from specified allergens. Values: `gluten`, `wheat`, `dairy`, `milk`, `lactose`, `egg`, `peanut`, `tree_nut`, `soy`, `fish`, `shellfish`, `sesame`, `corn`, `mustard`, `celery`, `lupine`, `sulfite`
- `max_calories` (number) -- max calories per serving
- `max_total_fat_g` (number) -- max total fat grams per serving
- `max_sugar_g` (number) -- max sugar grams per serving
- `max_sodium_mg` (number) -- max sodium mg per serving
- `max_cholesterol_mg` (number) -- max cholesterol mg per serving
- `max_carbohydrate_g` (number) -- max total carbohydrate grams per serving
- `min_protein_g` (number) -- min protein grams per serving
- `min_fiber_g` (number) -- min dietary fiber grams per serving
- `snap_eligible_only` (boolean) -- only return SNAP/EBT eligible products

**Example -- basic search:**
```json
{"action":"search_products","query":"organic milk","location_id":"01400441"}
```

**Example -- batch search for multiple items:**
```json
{"action":"search_products","query":"chicken thighs | olive oil | garlic | spinach","location_id":"01400441"}
```

**Example -- filtered search (gluten-free, low calorie):**
```json
{"action":"search_products","query":"crackers","location_id":"01400441","allergen_free":["gluten"],"max_calories":150}
```

**Example -- high protein, low sugar:**
```json
{"action":"search_products","query":"protein bars","location_id":"01400441","min_protein_g":15,"max_sugar_g":5}
```

**Example -- SNAP eligible only:**
```json
{"action":"search_products","query":"fresh bananas","location_id":"01400441","snap_eligible_only":true,"limit":5}
```

**Search tips for fresh produce:** Use specific terms like `"fresh zucchini"`, `"fresh limes"`, `"fresh avocado"` rather than generic single words. Generic terms like `"lime"` may return unrelated products (e.g. "Lemon Lime" soda).

Single-query response: `query`, `products[]`, `total`, `limit`, optional `filter_summary`

Batch response: `batch` (true), `queries_submitted`, `results[]` (each with `query`, `products[]`, `total`), `limit_per_query`

Each product includes: `product_id`, `upc`, `brand`, `description`, `categories[]`, `country_origin`, `snap_eligible`, `organic`, `non_gmo`, `image_url`, `price_regular`, `price_promo`, `size`, `fulfillment` {`delivery`, `pickup`, `in_store`, `ship`}, and optionally `nutrition_summary` {`serving_size`, `calories`, `protein_g`, `total_carbohydrate_g`, `total_fat_g`, `sugar_g`, `dietary_fiber_g`}

When filters are active, a `filter_summary` is included with `products_scanned`, `products_excluded`, and `products_returned` counts.

---

##### get_product_details

Get detailed information for a specific product including full nutrition, allergens, ratings, images, and aisle locations.

**Required parameters:**
- `product_id` (string) -- Kroger product ID

**Optional parameters:**
- `location_id` (string) -- include for local pricing, availability, and aisle information

**Example:**
```json
{"action":"get_product_details","product_id":"0011110838001","location_id":"01400441"}
```

Returns: `product` with `product_id`, `upc`, `brand`, `description`, `categories[]`, `country_origin`, `snap_eligible`, `organic`, `non_gmo`, `temperature`, `allergens[]` (with `name` and `level`), `allergens_description`, `ratings` {`average_rating`, `total_reviews`}, `item_information` {`depth`, `height`, `width`, `gross_weight`, `net_weight`, `average_weight`}, `images[]` (with `perspective`, `size`, `url`), `items[]` (with `item_id`, `size`, `sold_by`, `price_regular`, `price_promo`, `fulfillment`), `aisle_locations[]`, `nutrition` {`ingredient_statement`, `serving_size`, `nutritional_rating`, `nutrients[]` (with `name`, `quantity`, `unit`, `percent_daily_value`)}

If the product is not available for both in-store and delivery at the selected location, an `availability_warning` is included.

---

##### add_to_cart

Add items to the user's Kroger online cart. Requires the user to have a connected Kroger account.

**Required parameters:**
- `items` (array of objects) -- items to add, each with:
  - `upc` (string, required) -- product UPC code from search or product detail results
  - `quantity` (integer, required, minimum 1) -- quantity to add
  - `modality` (string, optional) -- `PICKUP` or `DELIVERY` (defaults to user's Kroger account preference)

**Example:**
```json
{"action":"add_to_cart","items":[{"upc":"0011110838001","quantity":2},{"upc":"0001111042010","quantity":1}]}
```

**Example -- specify fulfillment method:**
```json
{"action":"add_to_cart","items":[{"upc":"0011110838001","quantity":1,"modality":"PICKUP"}]}
```

Returns: `success` (boolean), `items_added` (count), `items[]`

---

#### Workflows

##### Grocery Shopping Workflow

1. **Always start with `find_stores`** to get a `location_id` (user location is detected automatically)
2. `search_products` with `query` + `location_id` -- location_id is required for every search
3. Optionally use `get_product_details` for full info on specific products (nutrition, allergens, aisle location)
4. `add_to_cart` with UPCs and quantities (requires user Kroger account connection)

##### Dietary-Restricted Shopping

1. `find_stores` to get a `location_id`
2. `search_products` with allergen and/or nutrition filters (e.g. `allergen_free: ["gluten", "dairy"]`, `max_calories: 200`)
3. Review `filter_summary` to see how many products were scanned vs. excluded
4. `get_product_details` to verify allergen labels and full ingredient statements
5. `add_to_cart` with confirmed products

##### Meal Prep Batch Search

1. `find_stores` to get a `location_id`
2. `search_products` with pipe-separated ingredients: `"chicken breast | brown rice | broccoli | olive oil | garlic"`
3. Results are grouped by query with concurrent API calls for faster results
4. `add_to_cart` with selected items from each result group

#### Notes

- Only products available for both in-store shopping and delivery are returned in search results
- Allergen filtering uses Kroger's allergen labels with an ingredient-statement fallback for products that lack allergen declarations
- Fresh whole foods (produce, raw meat, seafood) without allergen labels are allowed through the filter unless the product itself IS the allergen (e.g. fresh walnuts filtered for tree nuts)
- Nutrition filtering excludes products that lack the relevant nutrient data (to be safe)
- Batch searches run with limited concurrency (2 concurrent queries) with automatic retry on API errors
- The `query` parameter accepts both a plain string and a pipe-delimited multi-query string; both formats are supported
- `add_to_cart` requires the user to have connected their Kroger account through the platform

## When To Use
- Use this skill for `Grocery Shopping - Kroger` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: grocery shopping   kroger, grocery shopping kroger, search grocery products by name or brand, filter products by allergens like gluten dairy egg peanut soy, find low calorie or low sugar groceries with nutrition filters, search for high protein or high fiber foods, add to cart, items.
- Supported action names: `add_to_cart`, `find_stores`, `get_product_details`, `search_products`.

## Use Cases
- Search grocery products by name or brand
- Filter products by allergens like gluten dairy egg peanut soy
- Find low-calorie or low-sugar groceries with nutrition filters
- Search for high-protein or high-fiber foods
- Find SNAP/EBT eligible grocery items
- Get full nutrition facts and ingredients for any product
- Find nearby Kroger family stores by zip code
- Check product pricing and availability at specific stores
- Add items to Kroger cart for pickup or delivery
- Compare prices across store locations
- Plan meals with dietary restriction support
- Build grocery lists for specialized diets

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `4`.
x402 availability: not enabled for this product.

- `add_to_cart` (action slug: `add-to-cart`): Add items to the user's Kroger online cart. Requires user Kroger account connection. Price: `5` credits. Parameters: `items`.
- `find_stores` (action slug: `find-stores`): Find nearby Kroger-family stores. User location (zip code) is injected automatically. Price: `5` credits. Parameters: `chain`, `limit`, `radius_miles`.
- `get_product_details` (action slug: `get-product-details`): Get detailed product information including full nutrition, allergens, ratings, images, and aisle locations. Price: `5` credits. Parameters: `location_id`, `product_id`.
- `search_products` (action slug: `search-products`): Search the Kroger product catalog. You MUST call find_stores first to get a location_id. Supports batch search with pipe-separated queries, allergen filtering, nutrition filters, and SNAP eligibility. Price: `5` credits. Parameters: `allergen_free`, `brand`, `limit`, `location_id`, `max_calories`, `max_carbohydrate_g`, `max_cholesterol_mg`, `max_sodium_mg`, plus 7 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "grocery-shopping-kroger"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "grocery-shopping-kroger"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "grocery-shopping-kroger"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "grocery-shopping-kroger"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "grocery-shopping-kroger"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "grocery-shopping-kroger"
  }
}
```

## Call This Tool
Product slug: `grocery-shopping-kroger`

Marketplace page: https://www.agentpmt.com/marketplace/grocery-shopping-kroger

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Grocery-Shopping---Kroger",
    "arguments": {
      "action": "add_to_cart",
      "items": [
        {
          "modality": "PICKUP",
          "quantity": 1,
          "upc": "example upc"
        }
      ]
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "grocery-shopping-kroger",
  "parameters": {
    "action": "add_to_cart",
    "items": [
      {
        "modality": "PICKUP",
        "quantity": 1,
        "upc": "example upc"
      }
    ]
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `add_to_cart` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/grocery-shopping-kroger
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
