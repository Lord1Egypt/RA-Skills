---
name: ecommerce-listing-generator
slug: ecommerce-listing-generator
version: 1.0.0
description: Generate production-ready Amazon and AliExpress listings from a product image or parameters. Outputs title, bullet points, description, and SEO keywords in one shot.
author: ""
homepage: ""
tags:
  - ecommerce
  - amazon
  - aliexpress
  - seo
  - listing
  - cross-border
  - marketing
metadata:
  openclaw:
    emoji: "🛒"
    category: Marketing
    requires:
      env: []
      bins: []
    os:
      - linux
      - darwin
      - win32
---

# 🛒 Cross-Border E-Commerce Listing Generator

Generate production-ready multi-platform listings for Amazon and AliExpress from a product image or text parameters — including title, bullet points, description, and SEO keywords.

## Trigger Conditions

Activate this skill when the user:
- Sends a message starting with `/listing`
- Mentions "generate listing", "write listing", "Amazon listing", "AliExpress listing"
- Sends a product image along with keywords like "Amazon", "AliExpress", "listing", "cross-border"

## Information Collection

Before generating, verify the following are present:

| Field | Priority | Notes |
|-------|----------|-------|
| Product name / category | **Required** | |
| Core features / selling points | **Required** | |
| Target market | **Required** | e.g. Amazon US / AliExpress Global |
| Material / specs | Important | |
| Target audience | Important | |
| Price range | Optional | Affects positioning words |

If fields 1–3 are missing, ask before generating. Do not guess.

## Output Format

### Amazon Listing (English)

```
【Amazon Listing】

Title:
[≤200 chars | Brand + Core Keyword + Spec/Material + Use Case + Benefit]
Rules: Title case. No ALL CAPS. No: Best / Top / Sale / Free / ! @ # $

Bullet Points:
• [KEYWORD] - [Feature description, ≤255 chars]
• [KEYWORD] - [Material / build quality]
• [KEYWORD] - [Use case / target audience]
• [KEYWORD] - [Specs / compatibility]
• [KEYWORD] - [Warranty / after-sales]
Each bullet starts with an ALL-CAPS keyword phrase followed by " - "

Product Description:
[3–5 sentences. May use <b> and <br> HTML tags.]

Backend Search Terms (hidden keywords):
[15–20 unique keywords, comma-separated, no repetition from title]
```

### AliExpress Listing (English)

```
【AliExpress Listing】

Title:
[≤128 chars | Attribute + Core Keyword + Modifier + Use Case]
Style: Higher keyword density than Amazon. Natural stacking.

Search Keywords:
- Core (3): [high-volume root terms]
- Long-tail (8): [specific feature + product phrases]
- Scenario (4): [use case / occasion phrases]

Product Tags:
[10 tags, comma-separated]
```

## Quality Checklist

Auto-verify before output:
- [ ] Amazon title ≤200 chars, no banned words (Best/Top/Sale/Free/Special/!)
- [ ] AliExpress title ≤128 chars
- [ ] Each bullet point starts with ALL-CAPS keyword phrase
- [ ] No false claims or unverifiable superlatives
- [ ] Keywords flow naturally — no obvious stuffing

## Sub-Commands

| Command | Output |
|---------|--------|
| `/listing amazon [desc]` | Amazon only |
| `/listing aliexpress [desc]` | AliExpress only |
| `/listing keywords [desc]` | Keyword analysis only |
| `/listing rewrite [old title]` | Optimise an existing title |
| `/listing translate` | Generate DE / FR / ES / JP versions |

## Upsell Prompt

After completing the base output, always append:

> ✅ Listing generated! Need anything else?
> 1️⃣ Multi-language versions (DE / FR / ES / JP)
> 2️⃣ Competitor gap analysis
> 3️⃣ A+ Content copy
> 4️⃣ PPC keyword grouping suggestions

## Example Input

```
/listing
Product: Active Noise Cancelling Wireless Headphones
Features: ANC, 30H battery, Bluetooth 5.3, fast charge, foldable
Material: Protein leather ear cushions, matte ABS
Target market: Amazon US
Target audience: commuters, students, WFH workers
Price range: $35–$50
```
