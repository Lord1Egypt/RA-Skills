# Ecommerce Growth — Contribution Margin, Repeat Rate, and the Second Order

Transactional retail is the one model where growth can be perfectly measured and still be fatal: revenue is real, margin is thin, and the business lives or dies on whether the second order happens. Everything here is computed on **contribution margin**, never on revenue.

**Contents:** [Contribution Margin First](#contribution-margin-first) · [The Order Equation](#the-order-equation) · [Repeat Purchase Is the Business](#repeat-purchase-is-the-business) · [AOV Levers](#aov-levers) · [Cart and Checkout Abandonment](#cart-and-checkout-abandonment) · [Product Page and Merchandising](#product-page-and-merchandising) · [Email and SMS](#email-and-sms) · [Returns, Discounts, and the Margin Leaks](#returns-discounts-and-the-margin-leaks) · [Traps](#traps)

**Before any spend or promotion decision**, read `## Funnel` (conversion and AOV with as-of dates), `## Retention` (repeat-rate cohorts) and `## Channels` in `~/Clawic/data/growth/memory.md`. A promotion planned without the repeat-rate cohort in front of you is a decision about revenue made in ignorance of profit.

## Contribution Margin First

```
contribution_per_order = AOV − COGS − payment_fees − shipping_cost − pick/pack − expected_return_cost
CAC_ceiling_first_order = contribution_per_order            (break even on order 1)
CAC_ceiling_with_repeat = contribution_per_order × expected_orders_per_customer
```

Worked: AOV 68 USD, COGS 27 USD, fees 2.10 USD, shipping 6.50 USD, pick/pack 2 USD, returns allowance 3.40 USD → contribution 27 USD per order. At 1.0 orders per customer, no paid channel above 27 USD CAC works. At 2.4 expected orders, the ceiling rises to ~65 USD — the entire business case is that multiplier, and it is measured, not assumed.

Three disciplines: recompute contribution when any input moves (shipping rates and COGS move more often than teams update the model), express **ROAS as a contribution-margin ROAS** rather than a revenue one, and state the currency in every figure.

## The Order Equation

```
revenue = sessions × conversion_rate × AOV
profit  = orders × contribution_per_order − marketing − fixed
```

Diagnose in this order, since each is cheaper to move than the next: conversion rate (page and checkout), AOV (merchandising and bundles), repeat rate (lifecycle and product), sessions (channels). Sessions last, because buying more of a funnel that leaks is the most expensive fix available (`diagnosis.md`).

Segment every rate by **new versus returning**: returning customers convert several times better and carry no acquisition cost, so a blended conversion rate moves with traffic mix rather than with anything you did (`plateaus.md`).

## Repeat Purchase Is the Business

- **Cohort by first-order month**, and track orders per customer and cumulative contribution at 30/90/180/365 days. That curve is the asset; the first order is the cost of acquiring it.
- The **second-order rate** is the single most predictive number: the share of first-time buyers who order again within a window set by the category's replenishment cycle. It is the gate on every CAC decision.
- Derive the **replenishment interval** from the observed distribution of gaps between orders, then time the lifecycle message to just before it — not to a round number of days (`lifecycle.md`).
- **Subscription or replenishment programs** convert a repeat-rate problem into a retention problem with a churn curve, which is a better problem to have (`retention.md`, `monetization.md`).
- Report **new versus returning revenue split** every period. A business whose growth is entirely new customers is buying its revenue every month.

## AOV Levers

| Lever | Mechanism | Watch |
|---|---|---|
| Free-shipping threshold | Set just above current AOV so it pulls a real basket up | Set too high it suppresses orders; the threshold is a price change |
| Bundles and sets | Raises AOV and often margin | Discounting the bundle below the sum of margins destroys the point |
| Cross-sell at cart | Relevant complements at the decision moment | Irrelevant recommendations lower checkout conversion |
| Volume/tier pricing | Multi-buy incentives | Pulls forward demand; watch the following period |
| Post-purchase upsell | Offer after payment, no checkout risk | Must be one click and genuinely relevant |
| Premium tier of the same product | Choice architecture makes the middle option normal | Only with a real difference |

Every AOV lever must be judged on **contribution per session**, not AOV alone: a bundle that raises AOV 15% while cutting margin 20% is a loss dressed as a win.

## Cart and Checkout Abandonment

Abandonment is high everywhere and much of it is browsing, not intent. Work the causes that are yours:

| Cause | Fix |
|---|---|
| Unexpected costs at the last step | Show shipping and taxes early, or include them in price |
| Forced account creation | Guest checkout, account offered after purchase |
| Long or multi-page forms | Address autocomplete, one page, minimal fields (`activation.md` on step count) |
| Missing payment method | Add the methods your geography expects — this is regional, and a missing local method is a hard stop |
| Slow or broken mobile checkout | Test on real devices; most sessions are mobile |
| Trust gap | Return policy, security signals, real reviews near the button |

Recovery: an abandoned-cart sequence is standard and effective, triggered within hours and stopping instantly on purchase, with a discount only in the final message if at all — discounting the first message teaches customers to abandon carts deliberately (`lifecycle.md`).

## Product Page and Merchandising

- The product page is the conversion surface; images, the buy box, and price clarity outrank copy. Page-level testing craft: `cro`.
- **Reviews** are the highest-leverage social proof in retail and a supply problem: solicit them post-delivery, at the moment the product has been used.
- **Search and filters** on a catalogue site are a growth surface: measure zero-result searches — they are a demand signal for products you do not stock and a conversion leak for products you do but cannot be found.
- **Stock-outs** are silent conversion killers with a second-order cost: a customer who arrives for a stocked-out item and leaves may not return. Track lost sessions on out-of-stock pages and route them to alternatives.
- **Page speed** correlates with conversion on mobile retail; treat a slow page as a funnel defect, not an engineering preference.

## Email and SMS

The highest-margin channel in ecommerce, because the list is owned and the marginal cost is near zero.

- Flows before campaigns: welcome, abandoned browse, abandoned cart, post-purchase, replenishment, win-back. Flows are triggered and always-on; campaigns are broadcasts and burn the list (`lifecycle.md`).
- **Segment by purchase behaviour** — first-time versus repeat, category affinity, recency — because the same message to the whole list is what drives unsubscribes.
- **SMS is high-consent, high-cost, high-intrusion**: reserve it for time-sensitive transactional and a small number of genuinely valuable moments, and follow the local consent regime strictly.
- Deliverability rules apply in full (`lifecycle.md`); a retail list burnt by daily promotions is expensive to rebuild.

## Returns, Discounts, and the Margin Leaks

- **Returns are a category-level number**, not a company one; apparel and footwear return at rates that make blended figures useless. Model the return rate per category into contribution, and treat a rising rate as a sizing, description, or photography defect.
- **Discount depth trains the customer.** A brand on permanent promotion has repriced itself and lost the ability to run a real promotion.
- **Promotion cannibalisation**: measure incremental orders against a hold-out or a comparable period, not total orders during the promotion. Most promotions move demand in time rather than creating it (`experiments.md`).
- **Marketplace channels** (Amazon and equivalents) buy volume at the cost of margin, the customer relationship, and the email address. That is a strategic trade, not a channel test: model contribution after all fees before treating it as growth (`acquisition.md`).
- **Payment fees, shipping surcharges, and packaging** drift upward quietly. Re-derive contribution quarterly.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Optimising ROAS on revenue | 3× ROAS at 30% margin loses money on every order | Contribution-margin ROAS |
| Assuming repeat purchase | The whole CAC ceiling rests on a number nobody measured | Second-order rate by cohort |
| Free shipping without modelling it | Shipping cost is often the whole contribution | Threshold set above AOV, modelled |
| Discount in the first abandoned-cart email | Teaches deliberate abandonment | Reminder first; discount last, if at all |
| Judging a promotion on total orders | Pulls demand forward and calls it growth | Incremental orders versus hold-out |
| Blended new/returning conversion | Moves with traffic mix, not with your work | Segment always |
| Ignoring zero-result searches | A demand signal and a conversion leak, both invisible | Report and act on them weekly |
| Marketplace channels counted as growth | Trades margin and the customer relationship for volume | Model post-fee contribution and the lost relationship |

**After any margin, cohort, or promotion analysis**, write it back in the same turn: contribution per order with its component costs and currency into `## Pricing`, conversion and AOV with as-of dates into `## Funnel`, second-order rate and orders-per-customer by cohort into `## Retention`, all in `~/Clawic/data/growth/memory.md` (`memory-template.md`). A promotion post-mortem with its incrementality read goes to `experiments/<year>.md`; the contribution model itself, once it has been derived properly, is `artifacts/contribution-model.md` with its `## Boxes` line — it is re-derived from scratch every quarter otherwise, usually with different numbers.
