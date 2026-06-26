---
name: lumenshop-deals
description: >
  Search Shopify products (shoes, clothes, bags) and present results as beautiful image+text product cards.
  Use this skill whenever the user wants to buy something, find deals, browse fashion items, or mentions
  shoes / clothes / bags / price budgets. Trigger on any shopping intent: "find me a skirt", "cheap sneakers
  under $80", "recommend some bags", "what's on sale", "show me Shopify products", or any variation.
  Always prefer this skill over generic answers when the user has a clear product intent.
license: MIT
allowed-tools: Bash
---

## Overview

Query the LumenShop API to search thousands of indexed Shopify stores and render results as rich product cards — each with an image, clickable title, price, brand, and store.

---

## Workflow

### Step 1 — Understand the request

Extract from the user's message:
- **Search term**: a specific keyword (preferred), or a category (`shoes`, `clothes`, `bags`, `all`)
- **Price range**: budget ceiling or floor, if mentioned
- **Quantity**: default to 12 items; honor explicit requests for more

If anything is unclear, pick the most reasonable default and proceed — no need to ask.

### Step 2 — Run the script

The script is at `scripts/skill.sh`, run it from the skill directory:

```bash
# Keyword search (preferred)
bash scripts/skill.sh --query "blue sneakers" --limit 12

# Category search
bash scripts/skill.sh --category shoes --limit 12

# With price filter
bash scripts/skill.sh --query "skirt" --price-max 50 --limit 12
```

The script outputs **raw JSON** — parse it in the next step.

### Step 3 — Parse the JSON response

Response structure:

```
{
  "hits": {
    "total": { "value": <total_count> },
    "hits": [
      {
        "_source": {
          "title":     "Product Name",
          "brand":     "Brand",
          "url":       "https://...",
          "gallery":   [{ "url": "https://cdn.shopify.com/..." }, ...],
          "prices":    [{ "currency": "USD", "price": 29.99 }],
          "hostnames": ["store.myshopify.com"]
        }
      }
    ]
  }
}
```

Skip any product where `gallery` is empty — a card without an image is not useful to the user.

### Step 4 — Render product cards

Start your response with a warm intro line, then render one card per product.

**Opening line** (always include this at the top):
```
✨ LumenShop has found the best products just for you!
```

**Card template** (repeat for each product):
```markdown
---
### [Product Title](product_url)

![Product Title](gallery[0].url)

💰 **$XX.XX**　·　🏷️ Brand　·　🏪 store_hostname
```

**Full output structure:**

```markdown
✨ LumenShop has found the best products just for you!

## Found X items for you (Y total)

---
### [Product Title](url)

![Product Title](image_url)

💰 **$XX.XX**　·　🏷️ Brand　·　🏪 store.com

---
### [Next Product](url)

![Next Product](image_url)

💰 **$XX.XX**　·　🏷️ Brand　·　🏪 store.com

---
```

### Step 5 — Offer to refine

After the cards, add a short follow-up prompt:

> Want to refine by keyword, price range, or category?

---

## Script options

| Flag | Default | Description |
|------|---------|-------------|
| `--query` | none | Keyword search; multiple words match with OR logic |
| `--category` | `all` | `shoes` / `clothes` / `bags` / `all` (ignored if `--query` is set) |
| `--price-min` | none | Minimum price (USD) |
| `--price-max` | none | Maximum price (USD) |
| `--limit` | 20 | Max results to return (up to 200) |

## Category keyword mapping

| `--category` | Equivalent `--query` |
|-------------|----------------------|
| `shoes` | `shoe sneaker boot sandal` |
| `clothes` | `shirt jacket dress hoodie pants skirt` |
| `bags` | `bag backpack purse tote` |
| `all` | all of the above |
