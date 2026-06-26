---
name: promotion-engine
description: >
  Retail promotion calculator and discount lookup for digital employees.
  Computes final prices after applying discounts, bundles, thresholds, and
  membership tiers. Answers questions about current promotions and calculates
  how much a customer saves. Use when someone asks about: 优惠, 活动, 折扣,
  满减, 打折, 赠品, 积分抵扣, 会员价, 怎么算, 最便宜怎么买,
  current promotions, any discounts, how much off, coupon, promo code,
  bundle deal, buy one get one.
metadata:
  openclaw:
    emoji: 🏷️
---

# Promotion Engine

## Overview

This skill looks up active promotions and calculates final prices.
It always shows its work (calculation steps) so customers trust the answer.

**Depends on:** `promotions[]` in knowledge base + `membership{}` config.

---

## Query Types

| Query | Example | Action |
|-------|---------|--------|
| "What promotions are active?" | "现在有什么活动？" | List all active promos |
| "How much will I pay?" | "买两件怎么算？" | Calculate total |
| "Is this on sale?" | "这款打折吗？" | Check promo applicability |
| "How do I get the best deal?" | "怎么买最划算？" | Optimize purchase strategy |
| "Can I stack promos?" | "会员折扣和满减可以一起用吗？" | Check stackability |

---

## Calculation Steps

Always show calculation steps. Customers distrust "magic numbers."

### Step 1: Identify applicable promotions
For each item in the cart/query:
1. Check `promotions[]` for active promos (not expired)
2. Filter by `applicable_to` scope (does this product qualify?)
3. Check `excluded` list (is this product excluded?)
4. Check membership tier for additional discounts

### Step 2: Apply promotion rules
**Use `scripts/calculate_promotion.py`** for accurate computation.

Promotion types:
| Type | Rule format | Example |
|------|------------|---------|
| `threshold` | 满X减Y | 满300减50 |
| `discount` | X折 or X% off | 8折, 20% off |
| `bundle` | 买X件享Y价 | 买2件第2件半价 |
| `gift` | 满X赠品 | 满200赠小样 |
| `member_price` | 会员专属价 | VIP价¥199 |

### Step 3: Handle stacking
Check `stackable` field on each promotion.
- `stackable: true` → can combine with others
- `stackable: false` → use highest-value single promo
- When in doubt: use the rule that benefits the customer more

### Step 4: Present result
Show original price → applicable promos → final price → total savings.

---

## Answer Format

### Single item query
```
这款连衣裙 原价：¥399
✨ 夏日大促：满300减50
会员折扣：9折（VIP专享）

最终价格：¥309（节省¥90）
```

### Cart calculation
```
您的购物清单：
  白色连衣裙 ×1   ¥399
  条纹衬衫   ×1   ¥259
  小计：¥658

✨ 满300减50 → -¥50
✨ 满600再减80 → -¥80（两件合计超过600！）

最终合计：¥528（节省¥130 🎉）
```

### No active promotions
```
目前[产品/全场]暂无特别优惠活动。
当前售价：¥[price]
```

---

## Edge Cases

**Conflicting promos:** Always apply the rule that benefits the customer most. State which was applied.

**Expired promo mentioned by customer:** "这个活动已于[date]结束了，目前[有/没有]新的优惠。"

**Promo not in KB but customer claims it exists:** "我目前没有查到这个活动的信息，建议向店员确认一下，以免信息有误。"

**Membership tier unknown:** "您的会员等级我暂时查不到，建议核实后，会员专属折扣会自动应用。"

---

## Script

Use `scripts/calculate_promotion.py` for accurate numeric calculation.
**Reference:** [promo-rules-guide.md](references/promo-rules-guide.md) — detailed rule parsing.
