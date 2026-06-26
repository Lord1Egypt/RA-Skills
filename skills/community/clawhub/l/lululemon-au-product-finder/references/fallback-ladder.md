# Lululemon AU Fallback Ladder

Use this when anti-bot behavior blocks the normal path.

## Goal

Keep the answer useful while staying anchored to official Lululemon Australia sources.

## Source Tiers

Use the highest available tier for each field.

### Tier 1: Official Product Page

Strongest source.

Examples:

- open product page under `/en-au/p/`
- visible page text such as `Colour :`, `Select US Size (AU Size)`, `A$169`

Allowed for:

- product name
- URL
- color
- sizes
- current price
- original price
- sale flag
- low stock note

### Tier 2: Official Same-Slug Sibling Variant

Use other variant URLs with the same slug to improve color coverage or cross-check sale state.

Allowed for:

- additional colors
- confirmation that the slug maps to the same product family
- approximate variant coverage

Not allowed for:

- copying sizes from one color to another without saying they are variant-specific

### Tier 3: Search Result Snippet For An Official URL

Use when the official URL is known but the page cannot be opened.

Allowed for:

- product name
- official URL
- visible color in snippet
- visible sizes in snippet
- visible price in snippet

Requirements:

- the snippet must point to `lululemon.com.au`
- prefer snippets with the exact product slug or exact product title
- if a snippet is stale-looking or generic, lower confidence

### Tier 4: Official Category Or Collection Page

Use to confirm the product family still exists on the site and to estimate price range when the detail page is blocked.

Allowed for:

- product family existence
- current card price or price range

Not allowed for:

- exact variant sizes
- exact color list unless the color name is explicitly shown

### Tier 5: User-Supplied Official URL, HTML, Or Screenshot

Use only after official-site fallbacks are exhausted.

Allowed for:

- extracting text the user already has access to
- validating blocked variants

## Output Labels

Use these values in `field_sources`:

- `product_page`
- `sibling_variant_page`
- `search_snippet`
- `category_page`
- `user_supplied`

## Coverage Rules

- `all_colors_complete` is `true` only when multiple live variants were checked and the page set looks broad enough to represent the family.
- `sizes_complete` is `true` only for a specific variant page that clearly lists size options.
- If sizes came from a snippet, set `sizes_complete` to `false` unless the snippet obviously shows the full size row.

## Example Partial Output

```json
{
  "query": "define jacket nulu espresso",
  "product_name": "Define Jacket Nulu",
  "product_slug": "define-jacket-nulu",
  "currency": "AUD",
  "all_colors": ["Espresso"],
  "variants": [
    {
      "url": "https://www.lululemon.com.au/en-au/p/define-jacket-nulu/149502666.html",
      "color": "Espresso",
      "price": {
        "current": 169,
        "original": null,
        "sale": null
      },
      "sizes": ["0 (AU 4)", "2 (AU 6)", "4 (AU 8)"],
      "field_sources": {
        "color": "search_snippet",
        "price.current": "search_snippet",
        "sizes": "search_snippet"
      }
    }
  ],
  "confidence": "low",
  "coverage": {
    "variant_count_observed": 1,
    "all_colors_complete": false,
    "sizes_complete": false
  },
  "sources": [
    "https://www.lululemon.com.au/en-au/p/define-jacket-nulu/149502666.html"
  ]
}
```
