---
name: pet-services-research
description: Researches public Rover sitter and trainer profiles through the Crawlora API, returning clean JSON. Use when the user wants to discover pet sitters, dog walkers, trainers, or inspect a public provider profile without scraping Rover pages.
---

# Pet services research

Search Rover's public sitter and trainer marketplace as normalized JSON for
provider discovery and profile research.

## When to use this skill

- Find sitters near a location.
- Find trainers by service area.
- Inspect a public sitter or trainer profile.

## Setup

- Get a Crawlora API key at [crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`.

## How it works

Use `/rover/search` for sitter discovery and `/rover/trainer-search` for
trainer discovery. Follow a result's slug into `/rover/sitter/{slug}` or
`/rover/trainer/{slug}` for the public profile.

Full endpoint list: [`reference/endpoints.md`](reference/endpoints.md).

## Example

```sh
scripts/crawlora.sh /rover/search location="Austin, TX" service_type=dog-walking | jq '.'
scripts/crawlora.sh /rover/sitter/example-sitter | jq '.'
```
