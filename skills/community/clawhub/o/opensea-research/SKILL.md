---
name: opensea-research
description: Researches OpenSea NFT collections, items, marketplace activity, listings, offers, traits, categories, chains, and creator profiles via the Crawlora API, returning clean JSON. Use when the user wants to inspect an NFT collection, compare marketplace activity, find items, or analyze OpenSea sales and listings without scraping pages.
---

# OpenSea research

Inspect public OpenSea marketplace data as normalized JSON: collections,
items, traits, listings, offers, sales activity, categories, chains, and
creator profiles.

## When to use this skill

- Search or browse NFT collections and items.
- Inspect collection stats, traits, best deals, or related collections.
- Compare sales, listings, offers, and marketplace activity.
- Resolve accepted chain/category values before making a filtered request.
- Research a collection or creator's public marketplace footprint.

## Setup

- Get a Crawlora API key at [crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`.

## How it works

Start with `/opensea/categories` and `/opensea/chains` when a filter needs a
closed value set. Use collection/item search and detail endpoints next, then
the collection/item activity, listings, offers, sales, and trait endpoints for
market analysis. Keep cursors returned by paginated activity/listing calls.

Full endpoint list: [`reference/endpoints.md`](reference/endpoints.md).

## Example

```sh
scripts/crawlora.sh /opensea/collections slugs="example-collection" | jq '.'
scripts/crawlora.sh /opensea/collection/example-collection | jq '.'
scripts/crawlora.sh /opensea/collection/example-collection/activity | jq '.'
```
