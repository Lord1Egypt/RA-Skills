---
name: gumtree-uk-pets
version: 1.0.0
description: >-
  Search [Gumtree UK](https://www.gumtree.com/) Pets listings with bb-browser—dogs, cats, small furries, reptiles, horses, pet equipment—structured JSON and first-image Markdown for comparing ads. Uses gumtree/search + gumtree/listing adapters with search_category scoped to pets; for UK seasonal pet trade (e.g. June peak) and responsible buy/sell workflows only. Requires bb-browser.
author: SalamankaKit
tags:
  - gumtree
  - uk
  - pets
  - dogs
  - cats
  - classifieds
  - bb-browser
  - animal-welfare
---

# Meet Pets Friends

Use this skill **only** for **UK pet classifieds** on Gumtree: buying or selling **animals**, **pet accessories**, and **equipment**—not property, motors, general for-sale, jobs, or sports.

## Seasonal context (UK)

Demand for puppies, kittens, and rehoming often **peaks around late spring and June**. Help users **compare listings** (price, location, description, photos) and **research sellers**—not to bypass Gumtree messaging, identity checks, or the law.

## Legal and welfare (must follow)

- **UK law**: [Animal Welfare Act 2006](https://www.legislation.gov.uk/ukpga/2006/45/contents), breeding/licensing rules where they apply, and **banned breeds** restrictions—do not advise evading them.
- **Gumtree rules**: follow [Gumtree](https://www.gumtree.com/) pet policies and age/transport requirements; encourage in-person viewing and verifiable documentation (microchip, vet records) where relevant.
- **Read-only CLI**: this skill covers **`gumtree/search`** and **`gumtree/listing`** only. Contacting sellers or posting ads needs the normal site or browser.

## Prerequisites

- [bb-browser](https://www.npmjs.com/package/bb-browser) (`npm i -g bb-browser`).
- This bundle includes [`bb-sites/gumtree/search.js`](bb-sites/gumtree/search.js) and [`bb-sites/gumtree/listing.js`](bb-sites/gumtree/listing.js). Install into bb-browser:

```bash
mkdir -p ~/.bb-browser/sites/gumtree
cp bb-sites/gumtree/search.js ~/.bb-browser/sites/gumtree/search.js
cp bb-sites/gumtree/listing.js ~/.bb-browser/sites/gumtree/listing.js
```

Run the `cp` commands from the directory that contains `bb-sites/` (the unpacked skill bundle root).

---

## Search: keep results inside Pets

**4th positional** on `gumtree/search` is Gumtree `search_category`. For pets, use one of:

| `search_category` | Use for |
|-------------------|---------|
| `pets` | Whole Pets vertical (default starting point) |
| `pets-for-sale` | Animals offered for sale / rehoming |
| `pet-equipment-accessories` | Beds, crates, tanks, filters, etc. |

```bash
bb-browser site gumtree/search "cocker spaniel puppies" "Manchester" 1 pets --json
bb-browser site gumtree/search "indoor rabbit hutch" "Birmingham" 1 pet-equipment-accessories --json
bb-browser site gumtree/search "KC registered labrador" "United Kingdom" 1 pets-for-sale --json
```

**Positional order** (bb-browser): `query`, `location`, `page`, `category`.

- Refine **`query`** with breed, age (“8 weeks”), “rehome”, “rescue”, accessories type, etc.
- **`location`**: city, region, or `United Kingdom`.

Each hit includes `url`, `title`, `price`, `location`, `snippet`, `firstImageUrl`, `firstImageMarkdown`—use **`gumtree/listing`** on any `url` for full description and all images.

```bash
bb-browser site gumtree/listing "https://www.gumtree.com/p/dogs/..." --json
```

---

## When Gumtree markup changes

Update selectors in [`bb-sites/gumtree/search.js`](bb-sites/gumtree/search.js) and [`listing.js`](bb-sites/gumtree/listing.js), then copy the edited files to `~/.bb-browser/sites/gumtree/` again.

## Compliance

Respect [Gumtree](https://www.gumtree.com/) terms, robots.txt, and polite request rates. This skill is **pets-only**; use other skills for non-pet categories.
