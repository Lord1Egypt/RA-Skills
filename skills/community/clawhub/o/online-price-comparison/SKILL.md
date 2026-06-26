---
name: shopgeni
description: >
  AI-powered shopping assistant. Search for products by text or image, and find
  the best prices across Amazon, Google Shopping, and brand stores.
version: 1.0.0
user-invocable: true
tags: [shopping, fashion, price-comparison, recommendations, ai]
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: 🛍️
    os: [darwin, linux]
---

# ShopGeni — AI Shopping Assistant

ShopGeni exposes two AI-powered shopping capabilities:

1. **Item Recommendation** — natural-language and visual product search
2. **Price Comparison** — find the best price for a product across Amazon, Google Shopping, and brand stores

---

## 1. Item Recommendation

Search for products using natural language or a product image.

**Triggers:** "find me a dress", "show sneakers under $100", "recommend a blue denim jacket", "what shoes match this outfit?"

**Text search:**
```bash
python3 $SKILL_PATH/scripts/shopgeni.py \
  --query "blue running shoes under $120"
```

**Visual search (image file):**
```bash
python3 $SKILL_PATH/scripts/shopgeni.py \
  --image "/path/to/photo.jpg" \
  --query "find similar products"
```

---

## 2. Price Comparison

Find the best price for a specific product across multiple stores.

**Triggers:** "find best price for X", "compare prices for X", "where can I buy X cheapest"

**Text query:**
```bash
python3 $SKILL_PATH/scripts/shopgeni.py \
  --query "find best price for Nike Air Force 1 white"
```

**From a product URL:** Extract the product name and brand from the URL yourself, then pass as `--query`. Do not pass URLs to the script — the backend searches by keyword.

**Query construction:** Build the richest possible query from available product attributes — include brand, product name, and any of: style number, color, gender, category. More specific queries yield better results. Examples:
- `"find best price for Reebok Women's Zignition Running Shoes Black/White"`
- `"find best price for Nike Air Force 1 Low Men's Sneaker White style 100074219"`
- `"find best price for Adidas Response Super Women's Running Shoes"`

**With image URL (recommended for better accuracy):** Pass `--image-url` with the product image URL. The backend uses it for visual similarity ranking. If the user searched for products first, use the `image` field from that recommendation:
```bash
python3 $SKILL_PATH/scripts/shopgeni.py \
  --query "find best price for Reebok Women's Zignition Running Shoes Black/White" \
  --image-url "https://example.com/product-image.jpg"
```

**From a local image file:**
```bash
python3 $SKILL_PATH/scripts/shopgeni.py \
  --image "/path/to/product.jpg" \
  --query "find best prices for this product"
```

---

## Follow-up Queries

Pass `--thread-id` to continue a conversation:
```bash
python3 $SKILL_PATH/scripts/shopgeni.py \
  --query "show me similar ones in red" \
  --thread-id "previous-thread-uuid"
```

---

## Response JSON

```json
{
  "intent": "item | price_comparison",
  "content": "assistant response text",
  "thread_id": "uuid",
  "recommendations": [
    {
      "id": "...",
      "name": "Product Name",
      "brand": "Brand",
      "merchant": "Store Name",
      "price": "$99.99",
      "image": "https://...",
      "category": "shoes",
      "product_url": "https://www.beyondstyle.us/prod?id=..."
    }
  ],
  "price_comparison": {
    "candidates": [
      {
        "name": "Product Name",
        "price": "$89.99",
        "source": "Amazon",
        "buy_url": "https://..."
      }
    ]
  }
}
```

---

## Display Guidelines

- **Item recommendations:** Show as a markdown table or bullet list with name, brand, price, and link
- **Price comparison:** Show as a ranked table: `Rank | Store | Price | Link`
- Always show the `content` field as the assistant's main response
- Save `thread_id` from the response if the user may want to follow up
