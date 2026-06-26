---
name: product-recommender
description: >
  Intelligent product recommendation engine for retail digital employees.
  Recommends products based on customer needs, budget, recipient, occasion,
  preferences, and purchase history. Supports gift recommendations, outfit
  pairing, cross-sell, upsell, and "help me decide" flows.
  Use when someone asks: 推荐, 适合, 送礼, 哪个好, 帮我选, 比较一下,
  搭配什么, 有什么好的, recommend, what should I get, best for, gift idea,
  help me pick, what goes with, suitable for, I'm looking for.
metadata:
  openclaw:
    emoji: 🎯
---

# Product Recommender

## Overview

This skill handles all "help me choose" queries. It goes beyond listing products —
it understands the customer's situation, filters intelligently, and presents
a curated shortlist with reasons.

**Depends on:** `products[]` in knowledge base (Step 03).
**Works better with:** inventory data (to exclude out-of-stock items).

---

## Intent Extraction

Before recommending, extract these signals from the conversation:

| Signal | Examples | How to Extract |
|--------|---------|---------------|
| Budget | "500以内", "¥200左右", "不超过1000" | Parse number + direction |
| Recipient | "送妈妈", "给男朋友", "自用" | Named or implied |
| Occasion | "生日", "面试", "日常穿", "夏天用" | Event or context |
| Preferences | "素色", "轻便", "不要太甜", "简约风" | Style/attribute keywords |
| Age/Gender | "30岁女性", "老年人", "男生" | Demographic |
| Constraints | "不含酒精", "纯棉", "防水" | Hard requirements |
| Quantity | "买一套", "各来一个" | Number intent |

If critical signals are missing (especially budget), ask **one** clarifying question.
Never ask for all missing fields at once.

**Reference:** [intent-extraction.md](references/intent-extraction.md)

---

## Filtering Logic

Apply filters in this order (hard → soft):

1. **Hard filters** (eliminate if not met):
   - Budget: `price ≤ budget_max` (or `sale_price` if active)
   - Hard constraints: attribute must match (e.g., "纯棉" → filter by material tag)
   - Stock: exclude if `stock_qty == 0` (when inventory data available)

2. **Soft scoring** (rank what remains):
   - Recipient match: `suitable_for` overlap with recipient description
   - Occasion match: `tags` overlap with occasion keywords
   - Style/preference match: `description` + `tags` keyword overlap
   - Popularity signal: use `sales_rank` if available, else recency

3. **Return top N** (default: 3, configurable via `max_recommendations`)

**Reference:** [filtering-logic.md](references/filtering-logic.md)

---

## Recommendation Presentation

### Standard format (3 recommendations)
```
为您推荐 3 款最适合的选择：

1️⃣ [产品名] ¥[price]
   [1句话说明为什么适合这个场景/人群]
   [关键亮点：1-2个最相关的属性]

2️⃣ [产品名] ¥[price]
   [...]

3️⃣ [产品名] ¥[price]
   [...]

[可选] 您更倾向哪款？我可以帮您查一下库存～
```

### Gift recommendation (add wrapping note)
```
送礼推荐：[产品名] ¥[price]
[为什么适合作为礼物 — 1句话]
[礼盒包装是否可用 if known]
```

### Upsell (when appropriate)
If the customer's budget allows 20% more for a meaningfully better option:
> "还有一款 ¥[price+] 的[产品名]，多了[key upgrade]，性价比也很高，要不要看看？"
Only suggest once per conversation. Never push if customer declines.

---

## Special Flows

### "帮我比较" (Comparison)
When customer names 2+ specific products:
- Fetch both from KB
- Build a comparison table: price / key specs / suitable for / verdict
- Give a clear recommendation, not just data

### "搭配什么" (Outfit/Pairing)
When customer asks what goes with a product:
- Identify the anchor product
- Filter KB for complementary items (matching category tags: "搭配", "配套")
- Present as a complete set with total price

### "再便宜一点" (Price objection)
When customer asks for cheaper options after seeing recommendations:
- Re-filter with lower budget
- If nothing cheaper: explain value at current price, don't apologize for price

### "没有我想要的" (No match)
When no product passes the filters:
1. Tell the customer honestly
2. Suggest the closest available option
3. Offer to notify when matching product arrives (log as feature request)

---

## Script

Use `scripts/recommend.py` for deterministic filtering and scoring.
**Reference:** [filtering-logic.md](references/filtering-logic.md)
