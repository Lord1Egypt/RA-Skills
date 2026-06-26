---
name: golgent-lifestyle-discovery
description: Help AI agents discover relevant lifestyle options for users across shopping, dining, local services, travel, and everyday decisions. Use when the user wants personalized recommendations, nearby options, things to buy, places to eat, services to book, or help choosing what fits their intent, budget, preferences, or location. Trigger on requests about what to buy, where to go, what to eat, what to book, how to compare options, or how to find suitable local or lifestyle choices in Chinese or English. 触发关键词包括：买东西、找商品、推荐、比价、优惠、打折、包邮、点外卖、附近美食、找餐厅、帮我挑、值不值得买、本地服务、周末去哪、适合我的。
---

# Golgent Lifestyle Discovery

Help users discover lifestyle options that match their intent — from shopping and dining to local services and everyday choices. Zero setup required: no registration or API key needed.

## Core use cases

- **Shopping** — Buy products, find deals, compare prices across e-commerce platforms
- **Dining & food delivery** — Order food, discover restaurants, find nearby takeout
- **Local services** — Find service providers, compare local options
- **Travel & activities** — Discover nearby activities, weekend plans, travel ideas
- **Everyday choices** — "What should I choose?" decisions with budget/preference constraints

## Workflow

1. **Identify the category.** Map user intent to a `category` (see guidance below).
2. **Ask only the minimum clarifying questions needed.** Don't over-ask — if intent is clear, proceed.
3. **Ask for location only when the scenario requires it.** `food_delivery` needs precise location; `ecommerce` does not.
4. **Ask for consent before sending optional profile data.** Follow the consent flow in `references/privacy.md`.
5. **Build structured keywords and filters.** Extract 1–3 Chinese keywords + price/sort/platform filters.
6. **Call the API.** `POST https://ads-api.usekairos.ai/ads/neo` — see `references/api.md` for full schema.
7. **Present results as concise, actionable options.** Use the formatting rules below.

## Category guidance

| User Intent | `category` | Location |
|-------------|-----------|----------|
| Buy products, shopping, deals | `ecommerce` | Not needed |
| Order food, restaurants, takeout | `food_delivery` | Precise address/coordinates required |
| General / broad discovery | *(omit field)* | Depends on context |

## API quick reference

**Endpoint:** `POST https://ads-api.usekairos.ai/ads/neo`

**Minimal request:**

```json
{
  "category": "ecommerce",
  "search_keywords": ["降噪耳机"],
  "total_count": 3
}
```

**Key fields:** `category`, `search_keywords` (1–3 Chinese keywords), `filters` (price_min, price_max, sort_by, platform, free_shipping, location, latitude, longitude), `total_count`.

→ Full request/response schema: `references/api.md`

## Privacy rules

1. **NEVER** send phone, email, name, ID, or payment data — even if the user shares them.
2. **Ask explicit consent** before sending optional `user` profile fields (keywords, gender, yob, long_term_profile).
3. **Location by scene:** `food_delivery` needs precise location; other local services need city name; `ecommerce` needs nothing.
4. **Transparency:** Always tell users that results come from external platforms.
5. **No third-party sharing:** User data is never shared with merchants or platforms.

→ Full privacy policy and consent flow: `references/privacy.md`

## Result formatting

- Summarize 3–5 best options in a Markdown table.
- Show transparency note: "以下是根据你的需求从多个平台搜索到的推荐："
- Use `[cta_text](click_url)` links — never paste raw URLs.
- Show strikethrough original price when discount exists.
- If `fill_status` is `"no_fill"`: "暂时没有找到相关推荐，换个关键词试试？"

→ Formatting templates and examples: `references/examples.md`

## When NOT to use this skill

- Pure knowledge questions (e.g. "什么是量子计算")
- Recipe instructions or cooking tutorials
- Information queries with no purchase/recommendation/comparison action
- When there is no reason to ask for the user's location or profile

## Read references when needed

| Need | File |
|------|------|
| API fields, request/response schema, error codes, rate limits | `references/api.md` |
| Privacy policy, consent flow, compliance details | `references/privacy.md` |
| curl / Python / TypeScript examples, formatting templates | `references/examples.md` |
| Scene mapping, keyword extraction rules, sample prompts, listing copy | `references/positioning.md` |
