---
name: gumtree-uk-football
version: 1.0.0
description: >-
  Search [Gumtree UK](https://www.gumtree.com/) for football-related goods with bb-browser—replica or vintage shirts, boots, memorabilia, trading cards, console/PC football games, and event-style ticket listings—structured JSON and first-image Markdown. Uses gumtree/search + gumtree/listing with search_category tuned to sports/leisure and games; aligned with 2026 World Cup interest. Not for pets, property, or general jobs. Requires bb-browser.
author: SalamankaKit
tags:
  - gumtree
  - uk
  - football
  - soccer
  - world-cup
  - sports
  - memorabilia
  - tickets
  - bb-browser
---

# Gumtree UK football gear & related listings + bb-browser

Use this skill **only** for **football-related buying/selling** on Gumtree UK: **shirts/jerseys**, **boots**, **memorabilia**, **trading/flash cards**, **video games**, and **match or tournament ticket-style listings** (always treat tickets with extra caution—see below). Do **not** use this skill for pets-only, property, motors, or generic jobs.

## Context: 2026 and major tournaments

Users often search for **national team kits**, **club shirts**, **collectibles**, and **games** ahead of big tournaments. Tune **`query`** in natural language (e.g. “England shirt medium”, “Panini stickers”, “FIFA PS5”, “Champions League tickets June”).

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

## Search: categories that match football inventory

Gumtree’s slugs evolve; confirm in the site’s category filters if a search returns wrong verticals. Typical mappings:

| Intent | `search_category` (4th positional) | Example `query` |
|--------|------------------------------------|-------------------|
| Kits, boots, balls, general sports gear | `sports-leisure-travel` | `Manchester United shirt L` |
| Console/PC football games | `cds-dvds-games-books` | `FC 25 PS5` |
| Broader “might be anywhere” hunt | `for-sale` | `signed England shirt framed` |
| Trading cards / stickers (often under general for-sale) | `for-sale` | `Panini Premier League cards` |

**Tickets**: Gumtree mixes **tickets and experiences** inside broader categories; use explicit queries (`World Cup tickets`, `Wembley seats`, club name + `tickets`) and **`sports-leisure-travel`** or **`for-sale`** as needed. **Warn users**: verify seller identity, face-value rules, and fraud risk; never encourage off-platform payment to strangers.

```bash
bb-browser site gumtree/search "England retro shirt 1996" "London" 1 sports-leisure-travel --json
bb-browser site gumtree/search "football boots size 9" "Manchester" 1 sports-leisure-travel --json
bb-browser site gumtree/search "FC 24 Xbox" "United Kingdom" 1 cds-dvds-games-books --json
bb-browser site gumtree/search "Panini stickers album" "Leeds" 1 for-sale --json
```

**Positional order**: `query`, `location`, `page`, `category`.

## Listing detail

```bash
bb-browser site gumtree/listing "https://www.gumtree.com/p/..." --json
```

Use full description and `imageUrls` to check authenticity claims (signatures, tags, receipts)—**do not** present guesses as fact.

---

## When Gumtree markup changes

Edit [`bb-sites/gumtree/search.js`](bb-sites/gumtree/search.js) and [`listing.js`](bb-sites/gumtree/listing.js), then re-copy to `~/.bb-browser/sites/gumtree/`.

## Compliance

Respect [Gumtree](https://www.gumtree.com/) terms, resale rules for tickets where applicable, and polite request rates. **Football/commerce only**—not pets or jobs.
