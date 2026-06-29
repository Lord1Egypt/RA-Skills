---
name: Grocery Price Comparer
slug: grocery-price-comparer
description: Compare fresh grocery prices across Hema, Dingdong, Meituan Maicai & more — find the best deals on your shopping list.
tags: [grocery, price-comparison, shopping, fresh-food, saving, china]
version: 1.0.0
license: MIT-0
---

# Grocery Price Comparer (买菜比价助手)

Compare fresh grocery prices across **Hema (盒马)**, **Dingdong Maicai (叮咚买菜)**, **Meituan Maicai (美团买菜)**, and **Pupu Supermarket (朴朴超市)**. Align different unit standards, find the best total price, and output a ready-to-shop procurement plan.

## Scripts

| Path | Description |
|------|-------------|
| `scripts/compare.py` | Main CLI script — parse list, compare prices, output plan |
| `schemas/input.schema.json` | JSON Schema for workflow input |
| `schemas/output.schema.json` | JSON Schema for workflow output |
| `references/platforms.json` | Platform reference data (coverage, fees, features) |
| `references/categories.json` | Product category keywords and unit standards |

### CLI Usage

```bash
# Compare a shopping list across all 4 platforms
python scripts/compare.py --list "猪肉500g, 西红柿3个, 鸡蛋一盒, 牛奶1L"

# Compare on specific platforms only
python scripts/compare.py --list "牛腩800g, 西兰花2颗, 豆腐1盒" --platforms hema,dingdong

# JSON output for programmatic use
python scripts/compare.py --list "苹果1kg, 大米5kg" --output json

# Validate schemas
python scripts/compare.py --validate-schemas
```

## 🚀 First-Success Path (3 Steps)

1. **Step 1**: Run `python scripts/compare.py --list "鸡蛋, 牛奶, 猪肉" --platforms hema,dingdong`
2. **Step 2**: Review the comparison matrix auto-generated with unit prices
3. **Step 3**: Get the recommendation — see your first price win in <30 seconds

## Core Capabilities

- **Multi-platform query**: Search the same product across 4 major fresh-food delivery platforms simultaneously
- **Unit normalization**: Auto-convert across 500g, 1 份 (serving), 1 斤 (jin), per-piece, and per-pack
- **Total cost calculation**: Factor in product price + delivery fee + platform discounts/coupons
- **Split-order optimization**: Sometimes splitting across 2 platforms saves more than single-platform loyalty
- **Price alert**: Watch a product and notify when it drops below a target price
- **Shopping list parser**: Accept free-text or voice input, parse into structured items (name, spec, quantity)

## Workflow (8 Steps)

### Step 1: Parse Shopping List
**Input**: Free-text shopping list (e.g., "猪肉500g, 西红柿3个, 鸡蛋一盒, 牛奶1L") or uploaded historical order screenshot.
**Output**: Structured item list: `[{name, spec, quantity, category}]`.
**Logic**: Use LLM to extract item name, normalize spec (e.g., "两斤" → 1000g), infer quantity. Flag ambiguous items for user confirmation.

### Step 2: Query All Platforms
**Input**: Structured item list.
**Action**: Search each item on Hema, Dingdong, Meituan Maicai, Pupu (via web fetch or API).
**Output**: Raw search results per platform per item.
**Logic**: Handle platform-specific search APIs. If direct API unavailable, use web scraping fallback. Cache results for 15 minutes.

### Step 3: Unit Normalization
**Input**: Raw search results with varying units (500g, 1份, 1斤, 每袋).
**Output**: All prices normalized to CNY/500g.
**Logic**: 1 斤 = 500g; 1 份 / 1 袋 → estimate from product details, or ask user. Round to 2 decimal places.

### Step 4: Price Matrix Construction
**Input**: Normalized prices per item per platform.
**Output**: Comparison matrix table.

| Item | Spec | Hema | Dingdong | Meituan | Pupu | Best |
|------|------|------|----------|---------|------|------|
| Pork belly | 500g | ¥29.9 | ¥27.8 | ¥31.5 | ¥28.0 | Dingdong |

**Logic**: Highlight the best price per item. Mark N/A when platform doesn't carry the item.

### Step 5: Total Cost Calculation
**Input**: Price matrix + user's quantity per item.
**Output**: Total cost per platform including delivery fees and available coupons.
**Logic**: Base total = sum(unit_price × quantity). Add delivery fee. Subtract available coupons/promotions. Compare single-platform vs split-order scenarios.

### Step 6: Platform-Specific Trade-off Analysis
**Input**: Total cost results.
**Output**: Recommendations with trade-off labels.
**Logic**:
- 🏷 **Cheapest overall**: Single platform with lowest total
- 🔀 **Split optimal**: Cross-platform split saves >10%
- ⭐ **Quality priority**: Rank by freshness rating + price (for users who value quality)

### Step 7: Generate Procurement Plan
**Input**: User's chosen strategy.
**Output**: Ready-to-shop list organized by platform.

```
=== 盒马 (Hema) ===
- 鸡蛋 30枚装 ×1  ¥19.9
- 牛奶 1L ×2       ¥13.8/ea
Subtotal: ¥33.7
```

**Logic**: Group items by platform. Include estimated delivery time window.

### Step 8: Optional — Set Price Alerts
**Input**: Item + target price + platform.
**Output**: Confirmation. Alert fires when condition met.
**Logic**: Store in local state. Poll prices every 4 hours during active hours.

## Sample Prompts

### Prompt 1: Basic Comparison
**User**: "帮我比价：猪肉一斤，鸡蛋一盒，青菜500g，在盒马和叮咚买菜"
**Expected Output**: Comparison matrix for 3 items across 2 platforms, with total cost.

### Prompt 2: Full List
**User**: "这周买菜清单：牛腩800g、西兰花2颗、豆腐1盒、酸奶6杯、苹果1kg、大米5kg。帮我看看哪个平台最便宜"
**Expected Output**: Full comparison across all 4 platforms, split-order suggestion if applicable.

### Prompt 3: Quality Priority
**User**: "我想买品质好的海鲜：三文鱼200g和基围虾500g，哪个平台新鲜度口碑好？价差多大？"
**Expected Output**: Quality-first ranking with price comparison for seafood items.

### Prompt 4: Budget Constraint
**User**: "预算100块，要买够3天的菜（2人份）：肉、蛋、3种蔬菜、水果。推荐最优组合"
**Expected Output**: Budget-optimized shopping list with per-platform allocation.

### Prompt 5: Price Alert
**User**: "帮我盯着盒马的澳洲肥牛卷，降到25块以下通知我"
**Expected Output**: Alert set confirmation. Later: notification when condition triggers.

### Prompt 6: Screenshot Upload
**User**: [uploads Dingdong order screenshot] "上次在叮咚买的这些，这次想对比下盒马和朴朴"
**Expected Output**: Parsed list from screenshot, comparison across 3 platforms.

## Real Task Examples

### Example 1: Weekly Grocery Run
**Scenario**: Family of 3, weekly grocery shopping, budget-conscious.
**Input**: "本周买菜：五花肉1000g、鸡胸肉500g、西红柿6个、黄瓜3根、白菜1颗、鸡蛋30枚、牛奶2L、苹果1kg、香蕉1把、大米10kg"
**Steps**:
1. Parse → 10 items structured
2. Query 4 platforms → results
3. Normalize units (meat by 500g, veg by piece/bunch, staples by pack)
4. Build matrix → identify best per item
5. Calculate totals → Dingdong ¥187.3, Hema ¥203.5, Meituan ¥192.1, Pupu ¥198.8
6. Split analysis → Hema+Dingdong split = ¥176.5 (save ¥10.8)
7. Output split-order plan
**Output**: Two-platform procurement plan, total ¥176.5, saves 6% vs single best.

### Example 2: Party Shopping
**Scenario**: Hotpot party for 8 people, bulk purchase.
**Input**: "火锅食材：肥牛2kg、肥羊1.5kg、虾滑500g、丸子1kg、豆腐2盒、蘸料8份、饮料2大瓶"
**Steps**:
1. Parse → 7 items, large quantities
2. Query → Hema and Meituan have bulk discounts
3. Unit normalize → bulk pricing differs from retail
4. Matrix → Hema bulk cheapest for meat, Dingdong for sides
5. Recommend split: meat from Hema (bulk discount), sides from Dingdong
**Output**: Split plan, total ¥352.0, saves ¥41 vs single-platform.

### Example 3: New City Explorer
**Scenario**: Just moved, unfamiliar with local platforms. Want to know which platform is most reliable.
**Input**: "我刚搬到深圳，平时买菜哪个平台性价比最高？帮我比价5样日常菜"
**Steps**:
1. Auto-generate 5 common items: eggs, milk, pork, greens, rice
2. Query all 4 platforms
3. Matrix + consistency check (historical reliability)
4. Recommend based on price + delivery quality + coverage area
**Output**: Platform recommendation with sample price comparison.

## Boundary Conditions

| Condition | Behavior |
|-----------|----------|
| Item not found on any platform | Report "未找到", suggest similar item |
| Platform API rate-limited | Graceful fallback: estimate from cached data, flag as "estimated" |
| Quantity too small (e.g., 10g) | Warn user, suggest minimum purchase unit |
| Ambiguous item name (e.g., "白菜" could be napa or bok choy) | Show both options, ask to clarify |
| Price mismatch with user screenshot | Flag discrepancy, suggest re-check |
| User in unsupported city | Check coverage map; recommend available platforms |
| All platforms have same price | Report tie, recommend by delivery speed |
| Multi-currency or non-CNY request | Only support CNY; inform user |
| Screenshot OCR fails | Ask user to type items manually |

## Error Handling

| Error Code | Scenario | Handling |
|-----------|----------|----------|
| E-PLATFORM-DOWN | Platform unavailable (maintenance/outage) | Skip platform, flag in matrix as "不可用" |
| E-PARSE-FAIL | Shopping list parsing failed | Show what was parsed, ask user to correct |
| E-RATE-LIMIT | Too many queries in short time | Wait and retry with exponential backoff (max 3) |
| E-CACHE-STALE | Cached price > 30 min old | Show with "可能已过期" warning, offer refresh |
| E-OCR-FAIL | Screenshot text extraction failed | Prompt user for manual input |
| E-NO-COVERAGE | User location not served by any platform | Show coverage map, suggest alternatives |

## Security Requirements

- **No credential storage**: Never store platform login credentials
- **Price data only**: Only scrape public-facing price and product data
- **No transaction execution**: This skill compares prices; it does NOT place orders
- **Screenshot sanitization**: Strip EXIF/metadata from uploaded screenshots before processing
- **User location privacy**: City-level location OK; never store precise coordinates
