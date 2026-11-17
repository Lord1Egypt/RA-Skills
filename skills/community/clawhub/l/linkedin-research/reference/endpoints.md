# linkedin-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 1 platform group(s).**

## LinkedIn (5)

### `linkedin_company`

- **HTTP:** `GET /linkedin/company/{id}`
- **What:** Get LinkedIn Company info by ID. Returns a LinkedIn company page by its company `id`. The response has the name, headline, about text, industry, company size, employee count on LinkedIn, follower count, founding year, headquarters, locations, specialties, website, logo, Products section cards, affiliated and similar pages, and recent updates with reactions and comment counts.
- **Params:** `id` (string, **required**) — LinkedIn Company ID

### `linkedin_product`

- **HTTP:** `GET /linkedin/product/{id}`
- **What:** Get LinkedIn Product info by ID. Returns a LinkedIn product page by its product `id`. The response has the name, about text, category, owning organization, external link, logo, cover image, media items, featured customers with industry and follower count, and lists of other and similar products.
- **Params:** `id` (string, **required**) — LinkedIn Product ID

### `linkedin_product_categories`

- **HTTP:** `GET /linkedin/product/categories`
- **What:** Discover LinkedIn product categories. Returns the standardized product categories accepted by the products/search endpoint's category_id filter. With a keyword, returns matching categories from LinkedIn's own category search. Without one, returns every known category.
- **Params:** `keyword` (string, optional) — Narrow results to categories matching this term. Omit to return every known category.

### `linkedin_products_search`

- **HTTP:** `GET /linkedin/products/search`
- **What:** Search the LinkedIn product directory. Returns one page of LinkedIn's public product directory search results, optionally scoped to a keyword and/or category. Keyword matching is on word prefixes. start is an upstream card offset advanced by the previous response's next_start; LinkedIn's guest search stops returning results at offset 1200.
- **Params:** `category_id` (string, optional) — Numeric category id from /linkedin/product/categories; `keyword` (string, optional) — Search keyword, matched on word prefixes; `start` (integer, optional) — Upstream card offset, 0 to 1199

### `linkedin_showcase`

- **HTTP:** `GET /linkedin/showcase/{id}`
- **What:** Get Linkedin Showcase Page Info. Returns a LinkedIn showcase page by its showcase page `id`. The response has the name, headline, about text, industry, follower count, employees on LinkedIn, headquarters, locations, specialties, website, logo, Products section cards when present, affiliated and similar pages, and recent updates with reactions and comment counts.
- **Params:** `id` (string, **required**) — LinkedIn Showcase Page ID
