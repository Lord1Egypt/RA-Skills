# Lululemon AU Anti-Bot And Data Source Notes

Validated on `2026-03-21`.

## Verified Findings

- Direct HTTP requests to `https://www.lululemon.com.au/en-au/home` returned Cloudflare `403` in local `curl` tests.
- A fresh automated browser session also hit `Attention Required! | Cloudflare` on the homepage.
- `https://www.lululemon.com.au/robots.txt` was reachable and exposed two useful signals:
  - it disallows query-string search patterns such as `?q=` and `?search=`
  - it points to `https://www.lululemon.com.au/sitemap_index.xml`, but that endpoint was blocked when fetched directly
- Search-indexed product detail pages were still retrievable through the browsing tool and exposed the fields needed for extraction.

## Practical Consequence

The most stable default is:

1. discover product detail URLs through search results
2. open product pages under `/en-au/p/`
3. extract visible text fields
4. merge multiple variant URLs sharing the same product slug

If the normal path breaks, switch to the fallback ladder in [fallback-ladder.md](./fallback-ladder.md) instead of failing immediately.

Do not design the skill around:

- homepage scraping
- onsite search scraping
- direct sitemap crawling
- unauthenticated raw API probing

## Observed Page Patterns

These anchors were observed on AU product pages and are useful for extraction:

- the product heading near the page top
- `Colour :`
- `Select US Size (AU Size)`
- `A$89`, `A$169`, or price ranges
- `Sale Price ... Regular Price ...`
- `Only a few left!`
- `Sold out - notify me`

## Variant Behavior

Different URLs with the same slug can expose different colors and sale states. Treat them as one product family with multiple variants.

Examples observed during validation:

- `define-jacket-nulu/154826268.html`
- `define-jacket-nulu/149502742.html`

One page exposed `Black`, another exposed `Espresso`. This is why `all_colors` should be built from multiple pages when possible.

## Discovery Queries

Preferred search patterns:

- `site:lululemon.com.au/en-au/p "define jacket nulu"`
- `site:lululemon.com.au/en-au/p "swiftly tech long sleeve 2.0"`
- `site:lululemon.com.au/en-au/p "abc trouser warpstreme"`

Tighten the query with:

- gender words: `women`, `men`
- fit words: `cropped`, `hip length`, `regular`
- length markers: `3 inch`, `5 inch`, `25 inch`

## Confidence Guidance

Use `high` confidence when:

- the title matches closely
- at least one product page is open
- color, sizes, and price are all visible

Use `medium` confidence when:

- the title matches and the page is open
- some fields are missing or only one variant page was accessible

Use `low` confidence when:

- the match is based mostly on search-result snippets
- the user description is broad and multiple products remain plausible

## Fallback Observations

- Search snippets for official product URLs often expose usable fields such as color, size rows, and current price, even when the product page itself is not openable.
- Same-slug variant URLs are often enough to recover additional colors when one or more variants are blocked.
- Category pages can confirm that a product family is still active and can expose current card pricing, but they are weaker than detail pages for variant-level data.
