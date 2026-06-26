# Positioning & Use-Case Mapping

## Core Positioning

**Golgent Lifestyle Discovery** helps AI agents turn everyday user intent into actionable lifestyle recommendations — across shopping, dining, local services, travel, and everyday decisions.

---

## Supported Categories

| Category | Status | Data Sources | Location Required |
|----------|--------|-------------|-------------------|
| `ecommerce` | ✅ Active | Taobao, Tmall | No |
| `food_delivery` | ✅ Active | Meituan, Ele.me | Yes (precise address/coordinates) |
| *(omit)* | ✅ Active | Queries all sources | Depends on context |

> **Planned categories:** local services, travel, activities — coming soon.

---

## Scene → Category Mapping

### Shopping Decisions → `ecommerce`

User wants to buy products, find deals, or compare prices.

**Example intents:**
- 预算 500 元以内的通勤跑鞋
- 给经常出差的人推荐降噪耳机
- 帮我找一台编程用的笔记本电脑
- 天猫上有什么好的包邮咖啡机

**Keyword extraction examples:**

| User Input | `search_keywords` | `filters` |
|------------|-------------------|-----------|
| "预算500以内的通勤跑鞋" | `["跑鞋", "通勤", "轻便"]` | `{ "price_max": 500 }` |
| "帮我找5000-15000的编程笔记本" | `["笔记本电脑", "编程"]` | `{ "price_min": 5000, "price_max": 15000 }` |
| "天猫上包邮的咖啡机" | `["咖啡机"]` | `{ "platform": "tmall", "free_shipping": true }` |

### Dining & Food Delivery → `food_delivery`

User wants to order food, find restaurants, or discover dining options nearby.

**Example intents:**
- 今晚附近适合两个人吃的川菜
- 帮我找个附近的火锅店
- 推荐北京国贸附近适合工作日晚餐的餐厅

**Keyword extraction examples:**

| User Input | `search_keywords` | `filters` |
|------------|-------------------|-----------|
| "附近适合两人的川菜" | `["川菜"]` | `{ "sort_by": "nearest", "latitude": ..., "longitude": ... }` |
| "帮我找个火锅店" | `["火锅"]` | → ask for user location first |

### Everyday Choices → omit category or pick best fit

User has a broad lifestyle question that may span multiple categories.

**Example intents:**
- 给经常出差的人推荐降噪耳机和酒店选择
- 周末在上海适合带娃去的活动或服务
- 帮我选一个性价比高的上门保洁方案

**Handling:** Break into sub-queries if needed, or omit `category` to query all sources.

---

## Keyword Extraction Rules

When converting user intent to structured API parameters:

1. `search_keywords` — extract 1–3 **Chinese** keywords that capture the core need
2. `filters.price_min` / `price_max` — extract from budget mentions
3. `filters.sort_by` — infer from preference:
   - "最畅销" → `sales`
   - "最便宜" → `price_asc`
   - "最贵" → `price_desc`
   - "最近的" → `nearest`
4. `filters.platform` — "天猫" → `tmall`, "淘宝" → `taobao`
5. `filters.free_shipping` — "包邮" → `true`
6. `filters.latitude` / `filters.longitude` — for `food_delivery`, actively ask for coordinates
7. `filters.location` — city name for general use; detailed address for `food_delivery`

**When the user's need is vague**, ask a clarifying question before calling the API — e.g. "你主要是通勤用还是运动用？预算大概多少？"

---

## Sample Prompts

These prompts demonstrate the range of scenarios this skill handles:

- 今晚附近适合两个人吃的川菜
- 预算 500 元以内的通勤跑鞋
- 周末在上海适合带娃去的活动或服务
- 给经常出差的人推荐降噪耳机和酒店选择
- 帮我选一个性价比高的上门保洁方案
- Recommend a good dinner place near Sanlitun for two people tonight
- Find me commuter running shoes under 500 RMB
- Suggest family-friendly weekend activities in Shanghai
- Help me compare local cleaning service options
- Recommend products and services that fit a frequent traveler

---

## Marketplace Listing Copy

### Title

golgent-lifestyle-discovery

### Short Description

Lifestyle discovery for AI agents across shopping, dining, local services, travel, and everyday decisions.

### Long Description

Golgent Lifestyle Discovery helps AI agents turn everyday user intent into actionable recommendations. Use it for shopping decisions, dining and takeout, local services, travel ideas, and other lifestyle choices that depend on budget, preference, and location. The skill is designed for agents that need structured recommendation flows, privacy-aware data handling, and ready-to-use commercial or local-life discovery experiences.

### Tags

- lifestyle
- local-services
- shopping
- dining
- travel
- recommendations
- commerce
- discovery

### One-line Taglines

- **A:** Lifestyle discovery for AI agents.
- **B:** Help AI agents turn everyday intent into actionable lifestyle recommendations.
- **C:** Personalized shopping, dining, local services, and lifestyle discovery for AI agents.
