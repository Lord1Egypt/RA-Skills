---
name: gumtree-uk-jobs
version: 1.0.0
description: >-
  Search [Gumtree UK](https://www.gumtree.com/) jobs and part-time listings with bb-browser from the user’s role, location, and hours—structured JSON plus first-image Markdown for scanning vacancies. Uses gumtree/search + gumtree/listing with search_category jobs (and optional job subcategory slugs). Not for pets, property sales, motors, or football collectibles. Requires bb-browser.
author: SalamankaKit
tags:
  - gumtree
  - uk
  - jobs
  - part-time
  - recruitment
  - classifieds
  - bb-browser
---

# Gumtree UK jobs & part-time

Use this skill **only** for **UK employment** listings on Gumtree: **full-time**, **part-time**, **temporary**, and **casual** roles the user describes in natural language. Do **not** use it for pets, football merchandise, property to buy/rent as housing, or motors.

## Prerequisites

- [bb-browser](https://www.npmjs.com/package/bb-browser) (`npm i -g bb-browser`).
- This bundle includes [`bb-sites/gumtree/search.js`](bb-sites/gumtree/search.js) and [`bb-sites/gumtree/listing.js`](bb-sites/gumtree/listing.js). Install:

```bash
mkdir -p ~/.bb-browser/sites/gumtree
cp bb-sites/gumtree/search.js ~/.bb-browser/sites/gumtree/search.js
cp bb-sites/gumtree/listing.js ~/.bb-browser/sites/gumtree/listing.js
```

Run `cp` from the unpacked bundle root (the folder that contains `bb-sites/`).

---

## How to turn user input into a search

1. **`query`**: combine role + contract hint + optional sector, e.g. `evening cleaner Bristol`, `weekend retail assistant`, `remote admin part time`, `warehouse operative night shift`.
2. **`location`**: city, region, postcode area, or `United Kingdom` for national scan.
3. **`page`**: `1`, `2`, … for pagination.
4. **`category`**: use **`jobs`** to stay inside the Jobs vertical. Gumtree exposes **subcategories** as their own `search_category` slugs (examples below)—pick one when the user’s sector is clear.

### Example job subcategory slugs (confirm on site if results look wrong)

| User intent | Example `search_category` |
|-------------|---------------------------|
| General / mixed | `jobs` |
| Retail, shop floor | `retail-jobs` |
| Hospitality, bar, kitchen | `hospitality-catering-jobs` |
| Office, admin, PA | `secretary-pa-jobs` or `office-jobs` |
| Customer service, call centre | `customer-service-call-center-jobs` |
| Driving, warehouse | `driving-warehouse-jobs` |

Subcategory slugs **change** over time—if Gumtree returns unrelated ads, fall back to `jobs` and a sharper **`query`**.

```bash
bb-browser site gumtree/search "part time barista" "Edinburgh" 1 jobs --json
bb-browser site gumtree/search "weekend warehouse" "Birmingham" 1 driving-warehouse-jobs --json
bb-browser site gumtree/search "remote data entry" "United Kingdom" 1 jobs --json
bb-browser site gumtree/search "summer festival steward" "Manchester" 1 hospitality-catering-jobs --json
```

**Positional order**: `query`, `location`, `page`, `category`.

## Listing detail (full advert text)

```bash
bb-browser site gumtree/listing "https://www.gumtree.com/p/retail-jobs/..." --json
```

Encourage users to verify **employer identity**, **right to work**, and **pay** on official channels; the CLI is read-only.

---

## When Gumtree markup changes

Edit [`bb-sites/gumtree/search.js`](bb-sites/gumtree/search.js) and [`listing.js`](bb-sites/gumtree/listing.js), then re-copy to `~/.bb-browser/sites/gumtree/`.

## Compliance

Respect [Gumtree](https://www.gumtree.com/) terms, robots.txt, and polite request rates. **Jobs-only** skill.
