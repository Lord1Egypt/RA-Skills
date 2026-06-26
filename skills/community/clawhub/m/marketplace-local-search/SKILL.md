---
name: facebook-marketplace-search
description: Search Facebook Marketplace listings near a specified location with filters for radius, price range, limit, and pickup-only. This skill is a thin client for a user-provided local Marketplace service and returns normalized JSON results with local-first ranking support.
---

# Facebook Marketplace Search

Search nearby Facebook Marketplace listings via a **user-provided local Marketplace service**.

## Design goal

This published skill is intentionally a **thin wrapper client**.

It does **not** ship with:
- embedded Facebook scraping logic
- vendored Marketplace scraper code
- built-in background services
- LaunchAgent installers

That design keeps the published package smaller, easier to review, and less sensitive from a security-scanning perspective.

## What this skill does

- sends a search request to a local Marketplace-compatible service
- supports:
  - `query`
  - `location`
  - `radius_km`
  - `min_price`
  - `max_price`
  - `limit`
  - `pickup_only`
  - `sort`
- returns normalized JSON with:
  - `id`
  - `title`
  - `price`
  - `location`
  - `seller_name`
  - `image_url`
  - `listing_url`

## Expected local service

By default this client calls:

- `http://127.0.0.1:8787/search`

Override with:

- `MARKETPLACE_API_BASE_URL`

The local service is expected to accept query parameters such as:
- `query`
- `location`
- `radius_km`
- `min_price`
- `max_price`
- `limit`
- `pickup_only`
- `sort`

## Setup

Install deps:

```bash
python3 -m pip install -r skills/facebook-marketplace-search/requirements.txt
```

Optionally copy config:

```bash
cp skills/facebook-marketplace-search/config.example.json \
   skills/facebook-marketplace-search/config.json
```

## Usage

```bash
python3 skills/facebook-marketplace-search/scripts/facebook_marketplace_search.py \
  --query "burrow sofa" \
  --location "Livingston, NJ" \
  --radius-km 48 \
  --limit 10 \
  --sort local_first
```

## Output shape

```json
{
  "query": "burrow sofa",
  "location": "Livingston, NJ",
  "count": 2,
  "results": [
    {
      "id": "123",
      "title": "Burrow Sofa",
      "price": 400.0,
      "location": "Livingston, NJ",
      "seller_name": "Jane Doe",
      "image_url": "https://...",
      "listing_url": "https://www.facebook.com/marketplace/item/123"
    }
  ]
}
```

## Notes

- This skill is a client wrapper, not a bundled scraper.
- It is meant to integrate with a local service you control.
- Some upstream services may not always provide seller names or exact pickup semantics.
- Sorting behavior depends on the local service implementation.
