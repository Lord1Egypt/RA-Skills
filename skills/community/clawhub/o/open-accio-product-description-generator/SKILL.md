---
name: open-accio-product-description-generator
description: |
  Use when user wants to create product descriptions, SEO copy, Amazon listings, eBay item descriptions, Etsy listing copy, Shopify product pages, or any e‑commerce marketplace copy. Generates conversion‑focused, keyword‑rich copy tailored to the target platform.
version: "1.0.0"
---


# Product Description Generator

## Overview
Generate high‑converting, SEO‑optimized product descriptions for multiple e‑commerce platforms. The skill creates compelling copy that drives sales while improving search visibility.

## Core Workflow
1. **Collect Input** – product name, features, benefits, target audience, tone, and primary keywords.
2. **Select Platform** – Amazon, Shopify, eBay, Etsy, or custom.
3. **Apply Platform Template** – uses platform‑specific structure and length constraints.
4. **Inject SEO** – primary keyword in title and first paragraph, secondary keywords throughout, semantic variations, meta data.
5. **Add Conversion Elements** – hook, problem, solution, benefit‑focused features, social proof, urgency, CTA.
6. **Render Output** – markdown, HTML or CSV as requested.

## Usage Examples

### Amazon Listing
```bash
product-description-generator \
  --product "Wireless Bluetooth Headphones" \
  --features "40hr battery,noise cancelling,Bluetooth 5.3" \
  --benefits "crystal clear audio,comfortable fit,fast charging" \
  --tone professional \
  --platform amazon \
  --output amazon_listing.md
```

### Shopify Product Page
```bash
product-description-generator \
  --product "Ergonomic Office Chair" \
  --features "adjustable lumbar support,360° swivel,breathable mesh" \
  --tone conversational \
  --platform shopify \
  --include-faq \
  --output shopify_description.md
```

### Bulk Generation from CSV
```bash
product-description-generator \
  --csv products.csv \
  --platform ebay \
  --output-dir ./descriptions
```

## Platform Guidelines (see references/platforms.md)
- **Amazon** – Title 150‑200 chars, 5 bullet points, 2000‑3000 char description.
- **Shopify** – Title ≤70 chars, HTML description, SEO meta ≤155 chars.
- **eBay** – Title ≤80 chars, HTML description, detailed item specifics.
- **Etsy** – Title ≤140 chars, story‑driven description, 13 tags of 20 chars.

## Tone Options
- `professional` – data‑driven, authoritative.
- `conversational` – friendly, relatable.
- `playful` – energetic, emoji‑friendly.
- `luxury` – elegant, exclusive.

## Automation
Schedule bulk runs with cron or integrate into product pipelines. See `scripts/` folder for CLI helpers.

---

*Drive sales. Rank higher. Convert visitors.*


---

**Created by [Simon Cai](https://github.com/simoncai519) · More e-commerce skills: [github.com/simoncai519/open-accio-skill](https://github.com/simoncai519/open-accio-skill)**
