# Marketplace Guru — design notes

Working production design notes for a future OpenClaw skill that helps users buy products on marketplaces.

## Core idea

Marketplace Guru is not just a scraper. It is an **intent interviewer + purchasing advisor**.

The skill must avoid the common agent failure mode:

> user mentions a product → agent immediately searches → agent anchors on the first SKU/brand → real need is lost.

The goal is to understand what the user is actually trying to buy, which constraints matter, and then search with those criteria.

## Non-negotiable first gate: delivery

Before any real marketplace search, determine the delivery market:

- city / region / country;
- delivery deadline, if relevant;
- marketplace region/account context, if known.

Without delivery location, marketplace results are often misleading because price, stock, delivery time, seller availability, and assortment vary by region.

Do not proceed to search unless one of these is true:

1. the user provided the delivery location;
2. the user explicitly says region does not matter;
3. the task is only a rough/global comparison, not a purchase-ready search.

Default short question:

> Куда доставка?

## Do not overwhelm the user

The skill must not ask a long questionnaire.

Use at most **2–3 clarifying questions** before search, unless the user explicitly asks for a detailed requirements intake.

Always ask only the questions that most affect search quality.

## Two intake modes

### 1. Specific model / SKU / link mode

Triggered when the user provides:

- exact model;
- SKU;
- product URL;
- very specific brand + model;
- “хочу вот это”.

Behavior:

1. Respect the provided item first.
2. Ask for delivery location if missing.
3. Check product characteristics, reviews, rating, seller quality, price, availability, delivery.
4. Ask permission before expanding into alternatives.

Do not immediately redirect to analogs. The specific model may be the user’s actual target.

Recommended phrasing:

> Ок, проверю эту модель: характеристики, отзывы, цену, продавцов и доставку. Куда доставка? И можно ли параллельно показать 2–3 аналога, если они новее/лучше по отзывам или характеристикам за близкие деньги?

Alternative shorter phrasing:

> Смотрю строго её. Аналоги тоже проверить?

### Search Permission Gate

Before expanding beyond a user-specified model/brand/link, get permission if the user appears to want that exact item.

Permission is required when:

- the user gave a concrete model;
- the user gave a product link;
- the user said they want this exact item.

Permission is not required when:

- the query is already broad: “подбери”, “что взять”, “лучший”, “аналог”; 
- the provided model is clearly unavailable or incompatible, but explain this before switching.

### 2. Need/task mode

Triggered when the query is broad or task-based:

- “нужен робот-пылесос”;
- “модная футболка”;
- “жёсткий диск для дома”;
- “подарок ребёнку”;
- “что-нибудь для кухни”.

Behavior:

Ask 2–3 questions maximum:

1. Delivery location/deadline — mandatory.
2. One or two category-specific questions that most affect choice.

Examples:

#### Tech

- Budget: strict or flexible for quality?
- Priority: reliability / performance / warranty / quietness / brand / reviews?

#### Clothing

- Size / gender / style.
- Budget and desired positioning: basic / fashionable / branded / “looks more expensive than it is”.

#### Robot vacuum

- Apartment size, pets, carpets.
- Need self-emptying station / wet cleaning.

#### Storage drive

- Internal or external; SSD/HDD; size target.
- Priority: cheapest / reliable / fast / quiet / warranty.

Default broad-query prompt:

> Ок, перед поиском уточню только главное: 1) куда доставка и к какому сроку? 2) бюджет жёсткий или можно расширить ради качества? 3) что важнее: дешевле, надёжнее, быстрее доставка или лучший баланс?

## Interpreting user-mentioned products

If the user names a brand/model, treat it as one of these possibilities, not automatically as a hard requirement:

- exact requirement;
- hypothesis;
- example;
- candidate found by user;
- anchor from previous search.

If unclear, ask whether alternatives are allowed.

Important question:

> Это строго эта модель или можно предложить аналоги лучше по отзывам/характеристикам при близкой цене?

## Decision policy

The final recommendation should not be just “lowest price”.

Return decision-oriented roles:

- 🥇 best overall choice;
- 💸 rational/value choice;
- 🛡️ reliable/premium choice;
- 🚚 fastest delivery, if delivery deadline matters;
- 🚫 avoid / suspicious options, if found.

If marketplace recommendations reveal a strong candidate outside the initial query, include it only when analog search is allowed, and explain why it is relevant.

## Risk and quality model

Evaluate:

- exact SKU / variant match;
- new vs used/refurbished;
- seller reputation;
- marketplace fulfillment vs third-party seller;
- warranty and return conditions;
- suspiciously low price;
- hidden conditions: card-only price, wallet discount, coupons, points, subscription;
- reviews quality and common complaints;
- model age and known issues;
- delivery date reliability;
- total price including delivery.

Do not recommend anomalously cheap offers as the best option unless the risk is explicitly acceptable to the user.

## Example: home SSD/HDD search

Bad behavior:

> User says “maybe ADATA” → agent switches fully to ADATA and ignores better recommendations.

Better interpretation:

The real need may be:

> reliable internal storage for a home Windows mini PC / AI machine, with enough capacity, good endurance, acceptable heat, delivery soon, and willingness to pay 10–20% more for quality.

Good search brief:

> Найди внутренний SSD M.2 NVMe для домашнего mini PC. Нужен надёжный диск под Windows/данные/AI-задачи, форм-фактор M.2 2280, PCIe NVMe, желательно TLC, хороший ресурс TBW, нормальный бренд. Рассматривать 1–2 ТБ, но 2 ТБ предпочтительнее, если цена рациональна. Бюджет ориентир 18–22 тыс ₽, можно переплатить до 10–20% за качество и надёжность. Нужна покупка в РФ с доставкой в ближайшие дни. Не гнаться за минимальной ценой; исключать подозрительных продавцов, QLC/слабые модели и нерелевантные SKU. Дай 3–5 вариантов: лучший общий, самый рациональный, премиум/надёжный, и что не брать.

If user provides a specific model:

> Ок, проверю ADATA Legend 960 2TB: характеристики, отзывы, цену и продавцов. Куда доставка? И можно ли показать аналоги вроде Samsung/WD/Kingston, если они лучше по отзывам или надёжности за близкую цену?

## Five brains

1. **Intent Intake** — delivery gate, specific vs broad request, 2–3 questions max, analog permission.
2. **Search Strategy** — web_search → web_fetch → visible browser, no stealth/anti-bot loops.
3. **Offer Normalization** — exact SKU/variant, delivery, discounts, seller/source type, same-item comparison.
4. **Risk & Quality Scoring** — seller, reviews, warranty, suspicious prices, hidden conditions, fit to criteria.
5. **Decision Output** — best overall, value, premium/reliable, fastest delivery, avoid list, short recommendation.

## Found competitor ideas — implementation order

1. **Intent Intake + Delivery Gate** — from our design; base MVP.
2. **Permission Gate for analogs** — from our design; base MVP.
3. **Decision-first output** — from `price-comparison-analyzer`.
4. **L1/L2/L3 answer structure** — from `price-comparison-analyzer`.
5. **Risk-aware recommendation** — from `price-comparison-analyzer`.
6. **Search modes / weighted ranking** — from `shopping-expert`.
7. **Exact SKU + source types + evidence** — from `global-price-comparison`.
8. **Structured output schema** — from `ShopGeni`.
9. **Project structure with references** — from `ecommerce-price-comparison`.
10. **Price watch / coupons** — from `shopping-price-drop-coupon-scout`, later.
11. **Image/photo search** — from `ShopGeni`, major 2.0 feature.

## Production skill requirements

Marketplace Guru should include:

1. Delivery gate before search.
2. Two-mode intake: specific model vs need/task.
3. 2–3 question maximum by default.
4. Permission gate before analog expansion.
5. Decision-first output.
6. Risk labels and “avoid” section.
7. Explicit treatment of discounts and hidden conditions.
8. Evidence: source URL, price, timestamp, delivery region.
9. Read-only safety: no purchases, no cart actions, no login changes without explicit confirmation.
10. Escalation layers: web_search → web_fetch → visible browser when necessary.

## Future files

Potential production structure:

```text
marketplace-guru/
├── SKILL.md
├── README.md
├── references/
│   ├── intake.md
│   ├── risk-model.md
│   ├── output-formats.md
│   └── category-playbooks.md
└── scripts/
    └── optional deterministic helpers
```
