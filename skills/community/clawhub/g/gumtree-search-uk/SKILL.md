---
name: gumtree-bb-browser
version: 1.0.0
description: >-
  Search [Gumtree UK](https://www.gumtree.com/) from the terminal with bb-browser: property and flats to buy or rent, general second-hand deals, pets, used cars, and more local classifieds—structured JSON plus first-image Markdown for assistants. Includes gumtree/search and gumtree/listing adapters; requires bb-browser.
author: SalamankaKit
tags:
  - gumtree
  - uk
  - classifieds
  - property
  - rent
  - flatshare
  - motors
  - pets
  - second-hand
  - bb-browser
  - local-ads
---

# Gumtree UK + bb-browser

Use this skill when you need **UK local classifieds** as data an agent can reason over: **homes for sale**, **rentals and flatshares**, **second-hand goods**, **pets**, **used cars**, and other Gumtree categories—without manual copy-paste from the site.

## What this helps with

- **Property (buy)**: search sale listings; open a listing for full text, price, location, and all photos.
- **Renting / flatshare**: same flow for rental and shared-accommodation style listings on Gumtree.
- **Second-hand & general trade**: furniture, phones, bikes, and other “for sale” items—compare results using titles, prices, snippets, and thumbnails.
- **Pets**: find or inspect pet listings (always follow platform rules and local animal-welfare laws).
- **Used cars & motors**: browse motors listings; pull detail pages for specs in the description and image sets.

All of the above use the same two commands: **`gumtree/search`** then **`gumtree/listing`** for any result URL.

## Prerequisites

- [bb-browser](https://www.npmjs.com/package/bb-browser) installed globally (`npm i -g bb-browser`).
- Adapter files: `bb-sites/gumtree/search.js` and `bb-sites/gumtree/listing.js`.

Install adapters (private site overrides the community bundle):

```bash
mkdir -p ~/.bb-browser/sites/gumtree
cp bb-sites/gumtree/search.js ~/.bb-browser/sites/gumtree/search.js
cp bb-sites/gumtree/listing.js ~/.bb-browser/sites/gumtree/listing.js
```

After you change adapter files, copy again or use symlinks.

---

## 1) Search: `gumtree/search`

Each hit includes:

- `firstImageUrl` — absolute URL for the lead image (same role as `image` when present)
- `firstImageMarkdown` — ready-to-paste Markdown image line for chat UIs that render Markdown
- `url`, `title`, `price`, `location`, `snippet`

```bash
bb-browser site gumtree/search "2 bed flat Manchester" --json
bb-browser site gumtree/search "VW Golf" --json
bb-browser site gumtree/search "sofa" --json
```

**Comparing multiple results in chat**: paste `firstImageMarkdown` per row (or `![title](firstImageUrl)`). If remote images are blocked, fall back to showing `firstImageUrl` as a link.

**Positional arguments** (order follows bb-browser field order):

1. `query` (required)
2. `location` — default `United Kingdom`
3. `page` — default `1`
4. `category` — Gumtree `search_category`, default `all` (e.g. `cars-vans-motorbikes`; for property, pets, or other verticals use the slug from Gumtree’s category URLs / filters)

```bash
bb-browser site gumtree/search sofa Manchester --json
bb-browser site info gumtree/search
```

Note: unknown `--flags` are dropped by bb-browser’s global parser—use **positionals**, not `--page 2`.

---

## 2) Listing detail: `gumtree/listing`

Fetches the listing page: full **`description`** (JSON-LD `Product` when available, else `og:description`), plus **all image URLs** and a **lead image**.

```bash
bb-browser site gumtree/listing "https://www.gumtree.com/p/..."
# Path-only input is OK (domain is filled in):
bb-browser site gumtree/listing /p/coffee-table/some-slug/1512630746
```

Typical JSON fields:

- `description` — body text
- `title`, `price`, `location`
- `firstImageUrl`, `imageUrls`, `firstImageMarkdown`
- Removed listings return `error` and `hint`

```bash
bb-browser site info gumtree/listing
```

---

## When Gumtree HTML / JSON-LD changes

- **Search**: update selectors in `bb-sites/gumtree/search.js` (e.g. `article[data-q="search-result"]`).
- **Listing**: keep JSON-LD `Product` parsing first; fall back to `og:description` / `og:image`.

## Logged-in-only flows

Contacting sellers or posting ads still requires `bb-browser open` and normal browser interaction.

## Contributing upstream

Follow the [bb-sites](https://github.com/epiral/bb-sites) pattern: one JS file per command with `/* @meta */`.

## Compliance

Respect [Gumtree](https://www.gumtree.com/) terms, robots.txt, and polite request rates.
