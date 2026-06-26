---
name: marketplace-guru
description: Marketplace Guru helps users find and compare products on marketplaces by forcing disciplined purchase intent, clean search briefs, multi-source market mapping, price/risk analysis, and decision-ready recommendations. Use when a user wants to buy, compare, choose, or verify a product on marketplaces or online stores, especially when delivery, price, reviews, seller quality, or alternatives matter.
metadata: {"openclaw":{"requires":{"skills":["win11-visible-browser"]}}}
---

# Marketplace Guru

Marketplace Guru is an OpenClaw read-only purchasing advisor that turns marketplace shopping requests into disciplined, region-aware, multi-source, decision-ready purchase analysis.

## Non-negotiables

Do not skip these. If you cannot satisfy them, say what is missing instead of pretending the search is complete.

| Rule | Requirement |
|---|---|
| Delivery gate | Know delivery city/region before purchase-ready search. |
| Clean brief | Convert conversation into a compact search brief; do not paste user history into search. |
| Clean queries | Use short marketplace queries; apply criteria as filters/checks, not stuffed query text. |
| Source plan | Choose relevant sources before searching; do not default to one marketplace without reason. |
| Multi-source coverage | Use at least 2–3 relevant sources when the user did not name a source. |
| Market map first | Build price ranges and unit economics before final recommendations when comparable tiers exist. |
| No missing-price ranking | Do not rank technical candidates without current price. |
| Audit trail | State where you searched, which filters mattered, and what remains unverified. |
| Read-only | No purchase/cart/login/payment/account actions without explicit confirmation. |

## Workflow

### 1. Build a clean purchase brief

Compress the conversation into a short internal brief before searching.

Include only purchase-relevant fields:

| Field | Examples |
|---|---|
| Product/task | “kids sandals”, “8 TB HDD for photo archive”, “robot vacuum”, “детские сандалии”. |
| Delivery | City/region and deadline. |
| Hard constraints | Size 26, closed toe, 8 TB, leather, compatibility. |
| Soft preferences | Quiet, nicer design, reliable brand, better reviews. |
| Budget / price anchor | “до 3–4k”, “около 20k”, “можно +10–20% for quality”. |
| Allowed breadth | Exact model only vs analogs allowed vs broad discovery. |

Never use the entire chat history as a search query.

### 2. Classify the request

| Mode | Trigger | Behavior |
|---|---|---|
| Specific item | Exact model, SKU, product URL, brand + model, “хочу вот это” | Verify that item first; ask before analog search. |
| Need/task | “подбери”, “что взять”, “нужен…”, broad category | Clarify the real need, then search broadly. |
| Comparison | User gives several items or asks “A vs B” | Compare exact variants, risks, price, and fit. |
| Urgent purchase | “срочно”, deadline, delivery in days | Prioritize available delivery and returns; still keep quality/risk checks. |

Treat a named product as a candidate unless the user clearly says it is mandatory.

### 3. Ask only essential questions

Ask at most 2–3 questions before search unless the user requests a detailed intake.

Required first:

> Куда доставка?

Proceed without delivery only if the user explicitly says delivery does not matter or asks for rough research.

Typical question sets:

| Situation | Ask |
|---|---|
| Specific item | Delivery + “analogs too?” |
| Broad need | Delivery + budget/price anchor + 1 decisive criterion. |
| Urgent purchase | Delivery + deadline + hard constraints. |
| Clothing/shoes | Delivery + size + hard style/material constraints + budget. |
| Tech/storage | Delivery + budget + capacity/compatibility + priority. |

### 4. Create a source plan before searching

Pick sources by both category and purchase mode. State or internally follow the plan.

First classify purchase mode:

| Purchase mode | Signals | Source implication |
|---|---|---|
| Urgent/local | “срочно”, “завтра”, “пару дней”, local delivery matters | Prioritize local marketplaces/retailers; global sources only as price baseline. |
| Cheapest / willing to wait | “дешевле”, “готов ждать”, price dominates | Include global/direct sources and compare local markup. |
| DIY / open / experimental | “сток не важен”, “open-source”, “прошивка”, “для экспериментов”, “своё решение” | Include compatibility docs/source of truth plus global/direct sources; local sources are fast alternatives. |
| Reliability / warranty | “без возни”, “надёжно”, “гарантия”, “официально” | Prioritize official stores, reputable local sellers, major retailers. |
| Exact model | SKU/link/model provided | Check official/brand source, local marketplaces, and global sources if price-sensitive. |

Then choose sources by category and delivery region. Treat named retailers as examples, not universal defaults.

| Category | Default sources |
|---|---|
| General marketplaces | Local dominant marketplaces for the delivery region + global options when price/waiting matters. Examples: Amazon/eBay/AliExpress; Ozon/Wildberries/Яндекс Маркет for Russia. |
| Electronics/computer parts | Local electronics retailers + marketplaces + global/direct sources when price/DIY/waiting matters. Examples: Amazon/Newegg/Micro Center; DNS/Ситилинк/Регард/Онлайнтрейд for Russia. |
| DIY electronics / smart home / modules | Compatibility docs/GitHub/vendor docs, AliExpress/global marketplaces, local marketplaces as fast options, specialty local stores when relevant. |
| Kids clothing/shoes | Local fashion/kids retailers, regional marketplaces, brand stores when relevant. Examples: Amazon/Zalando/Target; WB/Ozon/Яндекс/Детский мир for Russia. |
| Appliances/home | Local major retailers, brand stores, regional marketplaces. Examples: Amazon/Best Buy/MediaMarkt; Яндекс Маркет/Ozon/DNS/М.Видео/Эльдорадо for Russia. |
| Exact brand item | Brand/official store + 2 relevant marketplaces + major retailer when relevant. |

Minimum coverage when the user did not name a source:

- Search at least 2 sources for quick/urgent tasks.
- Search at least 3 sources for non-trivial purchases.
- If the user signals cheapest/DIY/willing-to-wait, include at least one global/direct source unless explicitly excluded.
- Explain if a source is blocked, not checked, or only used as a price baseline.

Do not start and finish on one marketplace unless the user named it or time constraints force a quick partial result.

### 5. Use clean queries and filters

Use short base queries. Put constraints into filters or later verification.

Bad:

```text
сандали кожаные детские для девочки 26 закрытый нос кожа срочно доставка Москва до 4000
```

Good:

```text
сандалии детские
```

Then filter/check:

- size: 26;
- gender/style: girl if available;
- closed toe;
- material: leather/natural leather if available;
- delivery: today/tomorrow/2–3 days;
- price: up to budget;
- seller/rating/returns.

For exact models, query the model name only; do not append every criterion.

### 6. Search using the lightest reliable layer

| Layer | Use for | Stop/escalate when |
|---|---|---|
| `web_search` | Source discovery, broad candidate discovery, retailer pages. | Bot challenge, stale snippets, missing price/delivery. |
| `web_fetch` | Readable product pages and specs. | Captcha, JS-only, blocked, no price/delivery. |
| Browser | Marketplace filters, exact availability, recommendations, delivery, seller checks. | Captcha/login wall/manual intervention appears; do not loop. |

Use visible browser only when it materially improves accuracy. Prefer one reusable tab per source.

Do not use stealth/anti-bot bypasses.

### 7. Inspect marketplace recommendations and special offers

For each marketplace source that is opened, inspect beyond the initial search result:

- filters and sorted results;
- similar/recommended products;
- other sellers for the same item;
- alternative sizes/configurations/bundles;
- delivery badges and urgent delivery options;
- sponsored/special offers, but treat them as candidates, not truth.

Normalize and risk-check recommended items before suggesting them.

### 8. Build a market map before recommendations

Before naming winners, map the relevant market. Do not anchor on one listing or one expensive source.

For comparable products, estimate:

| Field | Requirement |
|---|---|
| Segments | Sizes, capacities, classes, brands, internal/external, material tiers, etc. |
| Price range | Low/normal/high range per segment. |
| Unit economics | ₽/TB, ₽/piece, ₽/kg, ₽/m², ₽/month, or category-appropriate unit. |
| User price anchor | Whether offers are inside, below, or above the user's corridor. |
| Outliers | Suspiciously cheap, overpriced, or unusually good. |
| Availability | Delivery deadline and stock scarcity when urgent. |

If the user gave a price anchor:

- search inside it first;
- label far-above-budget options as premium/overpriced;
- justify any over-budget recommendation;
- do not make a much more expensive offer the main pick unless clearly worth it.

If data is incomplete, call it partial and say what remains unverified.

### 9. Normalize offers before comparing

Compare only compatible offers.

| Field | Check |
|---|---|
| Exact item/variant | Same model/SKU/size/material/configuration. |
| Condition | New vs used/refurb/open-box. |
| Seller/source type | Official, marketplace fulfilled, third-party, unknown. |
| Delivery | Region, date, courier/PVZ, urgent availability. |
| Price basis | Normal price vs card/wallet/coupon/points/subscription. |
| Returns/warranty | Especially for shoes/clothing and electronics. |
| Reviews | Rating count, recurring complaints, not just star average. |

For clothing/shoes, verify size availability and return/try-on conditions before ranking when possible.

### 10. Evaluate risk and quality

Do not rank by lowest price alone.

Assess:

- seller reputation and fulfillment;
- reviews and review count;
- return/warranty clarity;
- suspiciously low price;
- hidden conditions or “price from” traps;
- delivery reliability;
- fit to hard constraints;
- whether paying more buys meaningful quality or convenience.

Mark risky/mismatched candidates as avoid instead of recommending them.

### 11. Give a decision-first answer

Default output order:

1. **Search audit** — sources checked, filters/criteria used, any blockers.
2. **Market map** — price ranges and unit prices/segments when applicable.
3. **Takeaway** — value zone, premium zone, avoid zone.
4. **Recommendations** — concrete picks with price, delivery, seller/source, risk, and link when available.
5. **Unverified / next check** — what still needs browser/detail verification.

Do not output technical links without prices when price is important.

Use roles:

| Role | Meaning |
|---|---|
| 🥇 Best overall | Best balance of price, quality, risk, and delivery. |
| 💸 Value choice | Cheaper acceptable option. |
| 🛡️ Reliable/premium | Better brand, seller, warranty, reviews, or lower risk. |
| 🚚 Fastest | Best when deadline dominates. |
| 🚫 Avoid | Suspicious, mismatched, missing-price, late delivery, or poor value. |

For each candidate include: price, delivery date/region, source/seller, key reason, risk/compromise, link if available, and timestamp if relevant.

Keep the visible answer compact. Provide deeper analysis only if asked.

### 12. Run a compliance checkpoint before final answer

Before responding, verify:

- Delivery region known or explicitly not needed.
- Clean brief used; no stuffed query from conversation history.
- Source plan followed or exceptions stated.
- At least minimum source coverage attempted.
- Price anchor respected.
- Market map created when comparable segments exist.
- Candidates have prices and delivery data, or are marked unverified.
- Marketplace recommendations/special offers were considered when marketplace pages were used.
- No state-changing actions performed.

If any item fails, either fix it or explicitly label the result as partial.

### 13. Stay read-only

Do not purchase, add to cart, change account settings, log in, save payment details, send messages to sellers, or perform other state-changing actions unless the user explicitly requests and confirms that specific action.

For any state-changing step, summarize what will change, where, risk, rollback if possible, and wait for explicit confirmation.

## Error handling

| Problem | Response |
|---|---|
| No delivery region | Ask for delivery location and pause purchase-ready search. |
| Too many missing criteria | Ask only the top 2–3 clarifying questions. |
| Bot challenge / captcha / login wall | Stop or switch source; report blocker; do not loop. |
| One source dominates results | Search another source or label result low-confidence/partial. |
| Query is getting long | Reset to a clean base query and use filters/checks. |
| Product has specs but no price | Do not rank it; mark “technical candidate, price not verified”. |
| Conflicting prices | Show range, source, timestamp, and confidence. |
| User price anchor known | Keep recommendations near it; label large over-budget options premium/overpriced. |
| Similar but not identical products | Separate them; do not compare as the same item. |
| Suspiciously cheap offer | Put it in risks/avoid unless user explicitly accepts risk. |
| Exact item requested | Do not suggest analogs unless asked or permitted. |

## Examples

| User says | First response | Correct behavior |
|---|---|---|
| “Find the best price for this product link.” | “Where do you need delivery? Exact item only or are alternatives allowed?” | Same-SKU comparison across relevant local/global sources, risk notes, best link. |
| “I need a Zigbee USB coordinator; cheapest is fine, I can wait.” | “Where is delivery? Home Assistant/Zigbee2MQTT/ZHA, or should I compare broadly?” | Use compatibility docs plus AliExpress/global sources and local fast alternatives; compare price, chip, firmware, delivery. |
| “Compare robot vacuums under $400 with fast delivery to Berlin.” | “Any must-have features: self-emptying, mopping, pet hair, or mapping?” | Region-aware EU/local sources, clean queries, market map, priced recommendations. |
| “Посмотри Samsung 990 Pro 2TB” | “Куда доставка? Аналоги тоже проверить, если найдутся лучше по отзывам/цене?” | Verify Samsung first; analogs only if allowed. |
| “Сандалии кожаные детские для девочки, 26, срочно” | “Куда доставка? Бюджет? Закрытый нос/примерка важны?” | Clean query “сандалии детские”; filters: 26, delivery, budget, material, closed toe; use region-relevant stores. |

## Notes for future versions

Implement later, not required for MVP 1.0.0:

- category playbooks;
- structured JSON output schema;
- price watch and coupons;
- deterministic extraction scripts;
- image/photo search, reserved for a major 2.0 release.
