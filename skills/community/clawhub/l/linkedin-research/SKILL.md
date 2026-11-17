---
name: linkedin-research
description: Researches public LinkedIn company, product, and showcase pages via the Crawlora API. Look up known IDs or discover and search the public product directory by keyword or category. Does not access personal profiles or private content.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# LinkedIn company research

Look up LinkedIn company, product, and showcase page info by ID — all as
normalized JSON from the Crawlora API, no browser automation or LinkedIn
login required.

## Tool scope and data flow

The optional shell helper is the only command this skill asks to run. It makes
GET requests only to the five documented, allowlisted Crawlora routes. These
include company, product, and showcase lookups by ID, product-category
discovery, and public product-directory search by keyword or category. The
discovery and search routes can access a broader slice of public LinkedIn
product catalog data than an ID-only lookup. When invoked, the helper reads
`CRAWLORA_API_KEY` and sends it as an `x-api-key` header over
HTTPS to `api.crawlora.net`; it does not send the key to LinkedIn. It briefly
writes a mode-600 curl config under `TMPDIR` and removes it when the command
exits. It does not inspect other environment variables, enumerate files, install
software, or run with elevated privileges. Run it only when you want to make a
Crawlora API request; successful requests can consume credits.

## When to use this skill

- "What's <company>'s LinkedIn company info (industry, size, description)?"
- "Pull the LinkedIn product page for <product ID>."
- "Find public LinkedIn products matching <keyword>."
- "List LinkedIn product categories or search categories for <term>."
- "Get details on this LinkedIn showcase page."
- Competitor company profiling or firmographic research using LinkedIn IDs.
- Enriching a company record with its LinkedIn company/product/showcase data.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

Use a known ID for a page lookup, or search the public product directory when
you need to discover products or categories:

1. **Company** — `/linkedin/company/{id}` — detailed company info (industry,
   size, description, and related fields) by LinkedIn Company ID.
2. **Product** — `/linkedin/product/{id}` — detailed product info by LinkedIn
   Product ID.
3. **Showcase page** — `/linkedin/showcase/{id}` — detailed info about a
   LinkedIn showcase page by ID.
4. **Product categories** — `/linkedin/product/categories` — list categories,
   or find matching categories with a keyword.
5. **Product directory search** — `/linkedin/products/search` — find public
   products using a keyword, category, and result offset.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Company info:
scripts/crawlora.sh /linkedin/company/1035

# Product info:
scripts/crawlora.sh /linkedin/product/urn:li:organizationProduct:123456

# Showcase page info:
scripts/crawlora.sh /linkedin/showcase/1234567
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for the complete
LinkedIn endpoint list and parameters this skill uses.

## Examples

- **Company profiling:** `/linkedin/company/{id}` for a target company to
  pull industry, size, and description before an outreach or comparison doc.
- **Product-page audit:** `/linkedin/product/{id}` to check how a competitor
  positions a specific product line on LinkedIn.
- **Showcase-page check:** `/linkedin/showcase/{id}` to see how a company
  segments a sub-brand or business unit on its LinkedIn showcase page.
- **Product discovery:** `/linkedin/products/search` to discover public
  products matching a keyword or category before looking up a product ID.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public company/product/showcase pages; no login, no
  private content. Respect LinkedIn's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Scope: public company/product/showcase data, not personal profiles.** The
  skill includes product category discovery and keyword/category product
  directory search as well as page lookups by ID. It has no personal-profile
  lookup endpoint and does not access private content.
