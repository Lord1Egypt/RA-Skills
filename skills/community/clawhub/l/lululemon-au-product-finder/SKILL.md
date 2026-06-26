---
name: Lululemon AU Finder
description: Find a product on the Lululemon Australia site from a natural-language clothing description and return structured details such as product name, variant colors, sizes, prices, URLs, and provenance. Includes fallback handling for anti-bot blocks.
homepage: https://www.lululemon.com.au/en-au/home
read_when:
  - Looking up a Lululemon Australia product from a fuzzy description
  - Extracting colors, sizes, prices, or URLs from lululemon.com.au
  - Recovering partial product data when product pages are blocked by anti-bot checks
metadata: {"clawdbot":{"emoji":"🛍️"}}
---

# Lululemon Au Product Finder

## Overview

This skill finds a Lululemon Australia product from a fuzzy user description and returns structured variant data. It is optimized for live catalog lookups where direct `curl`-style scraping or fresh browser automation may be blocked, and it is expected to degrade gracefully instead of failing hard.

## Core Rules

- Treat all catalog information as live. Verify against current pages before answering.
- Scope the work to `lululemon.com.au`, usually under `/en-au/p/`.
- Prefer search-engine discovery over Lululemon's onsite search.
- Prefer product detail pages over category, sale, or search pages.
- Group variants by product slug, then merge data across multiple variant URLs.
- Report uncertainty explicitly when only one variant page is accessible.
- Preserve per-field provenance when falling back to snippets or indirect evidence.

## Workflow

### 1. Normalize the Request

Extract the strongest product tokens from the user's description:

- product family: `Define Jacket`, `Swiftly Tech`, `ABC Pant`
- fabric or line: `Nulu`, `Luon`, `Warpstreme`
- fit or length: `cropped`, `hip length`, `5 inch`
- audience if present: `women`, `men`

Preserve meaningful qualifiers. Remove filler words.

Build 2-4 search queries, for example:

- `site:lululemon.com.au/en-au/p "define jacket nulu"`
- `site:lululemon.com.au/en-au/p "swiftly tech long sleeve 2.0"`
- `site:lululemon.com.au/en-au/p "abc trouser warpstreme"`

### 2. Discover Candidate Product Pages

Use web search first. Do not start with direct requests to the site's search pages.

Good candidates:

- URLs under `https://www.lululemon.com.au/en-au/p/...`
- search results whose title closely matches the requested product name

Bad candidates unless nothing else exists:

- category pages under `/c/`
- sale landing pages
- URLs that only differ by unrelated campaign parameters

When the search result is close but ambiguous, open the top candidates and compare:

- page title
- main product heading
- fit/fabric text
- price range vs single price

### 3. Select the Product and Collect Variants

Treat the slug after `/p/` as the product family key.

Example:

- `.../p/define-jacket-nulu/154826268.html`
- `.../p/define-jacket-nulu/149502742.html`

These usually represent the same product family with different color variants, and sometimes different sale states.

Rules:

- merge URLs with the same slug into one product record
- keep variant-level prices and sizes separate
- do not assume one page exposes every color name
- do not invent colors from swatch images alone

If needed, read [anti-bot-and-sources.md](./references/anti-bot-and-sources.md) for the validated discovery strategy and known failure modes.

### 3A. Anti-Bot Fallback Ladder

If a product page is blocked or partially readable, do not stop immediately. Fall back in this order:

1. open another search result for the same slug
2. open another variant URL for the same slug
3. use search-result snippets that point to official `lululemon.com.au` product URLs
4. use category or collection pages on `lululemon.com.au` to confirm the product family and current price band
5. reuse an existing real browser session if the environment supports it
6. ask the user for a direct official URL, page HTML, or screenshots only after the official-site fallbacks above are exhausted

What each fallback is allowed to answer:

- product name: product page, snippet, category card
- official URL: product page, search result
- color: product page first, search snippet second, same-slug sibling pages third
- sizes: product page first, snippet second
- current price: product page first, snippet or category card second
- original price or sale state: product page first, snippet second

Do not use unofficial reseller pages to fill official catalog fields.

### 4. Extract Fields From Each Variant Page

From each accessible variant page, extract:

- `product_name`
- `url`
- `color`
- `price.current`
- `price.original` when a regular price is shown
- `price.sale`
- `sizes`
- optional flags such as `low_stock`, `notify_only`, `online_only`

Common page anchors:

- the main heading near the top of the page
- `Colour :`
- `Select US Size (AU Size)`
- `A$...`
- `Sale Price ... Regular Price ...`

Normalization rules:

- currency is always `AUD` unless the page clearly shows otherwise
- convert price strings like `A$169` to numeric `169`
- preserve the site's size labels, for example `0 (AU 4)`
- if the product name is split across lines, join it into one string

### 5. Merge and Return Structured Output

Return one product object with:

- canonical product name
- product slug
- currency
- `all_colors` as the union of observed variant colors
- `variants` as an array of per-URL observations
- `confidence`
- `field_sources`
- `coverage`
- `sources`

Use this JSON shape by default:

```json
{
  "query": "define jacket nulu",
  "product_name": "Define Jacket Nulu",
  "product_slug": "define-jacket-nulu",
  "currency": "AUD",
  "all_colors": ["Black", "Espresso"],
  "variants": [
    {
      "url": "https://www.lululemon.com.au/en-au/p/define-jacket-nulu/154826268.html",
      "color": "Black",
      "price": {
        "current": 169,
        "original": 169,
        "sale": false
      },
      "sizes": ["0 (AU 4)", "2 (AU 6)", "4 (AU 8)"],
      "field_sources": {
        "color": "product_page",
        "price.current": "product_page",
        "sizes": "product_page"
      }
    }
  ],
  "confidence": "medium",
  "coverage": {
    "variant_count_observed": 1,
    "all_colors_complete": false,
    "sizes_complete": true
  },
  "sources": [
    "https://www.lululemon.com.au/en-au/p/define-jacket-nulu/154826268.html"
  ]
}
```

## Anti-Bot Policy

Default order of attack:

1. Use web search to discover product URLs.
2. Open product detail pages and extract visible structured text.
3. Merge multiple variant URLs for the same slug.
4. If product pages are blocked, fall back to official-site search snippets and related official pages.
5. If the environment supports a real browser session, prefer session reuse over a fresh automated browser.
6. Only then ask the user for a direct product URL, page HTML, or screenshots.

Avoid these as the primary path:

- raw `curl` or `requests` against the homepage or product pages
- fresh headless browser sessions with default automation fingerprints
- onsite search pages using `?q=` or `?search=`

If a user explicitly wants a scriptable crawler, explain that the stable default is not a raw HTTP scraper. It is a discovery-and-extraction workflow built around search indexing plus product detail pages, with optional browser-state reuse only when the environment supports a real user session.

If you have to answer from fallbacks, downgrade confidence and mark each fallback-derived field in `field_sources`.

## Failure Handling

- If multiple products fit the description, return the top matches and note why the match is ambiguous.
- If only one variant page is accessible, say that `all_colors` may be incomplete.
- If a page exposes images but not machine-readable color names, do not infer names from pixels.
- If the page is blocked, say so plainly and keep working through the fallback ladder.
- If all official pages are blocked but official search snippets are available, return a partial answer instead of a hard failure.
- If the answer is partial, say exactly which fields were verified from product pages and which came from snippets or sibling variants.

## When To Return Partial Results

Return partial structured output when at least one of these is known from official sources:

- an official product URL
- a reliable product name match
- at least one of color, sizes, or current price

For partial output:

- keep unknown fields as `null` or empty arrays
- set `confidence` to `low` or `medium`
- set `coverage.all_colors_complete` to `false` unless multiple live variants were verified
- include a short note describing the blocking point
