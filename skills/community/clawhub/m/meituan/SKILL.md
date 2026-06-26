---
name: meituan
slug: meituan
version: 2.2.0
description: "Meituan public local-life decision assistant. Compare visible merchant, fee, discount, ETA, review-risk, threshold, and refund-friction signals, then recommend whether to order, switch, add a useful item, wait, or skip. Public evidence only: no login, no account coupons, no order lookup, no cart mutation, no checkout, and no payment."
---

# Meituan (美团)

Use this skill when the user needs a decision about a Meituan food-delivery or local-life deal, especially when the question is shaped by delivery time, distance, minimum order, packaging fee, visible discounts, merchant reviews, refund practicality, or whether a promotion is actually worth chasing.

This is a public decision-support skill. It should produce an action, not a menu recap.

## Safety Contract

These rules override every workflow below.

- Use only public visible information or details supplied by the user, such as screenshots, copied cart lines, public merchant pages, or visible offer text.
- Do not log in, read order history, read account coupons, claim red packets, save cookies, change addresses, change cart contents, submit orders, or pay.
- Stop at login, CAPTCHA, identity checks, address selection, coupon wallets, order pages, checkout, or payment screens.
- If final payable price depends on address, account coupons, membership, payment method, inventory, or checkout state, mark it as user-only verification.
- Redact personal data if it appears unexpectedly, including phone numbers, addresses, names, order IDs, and payment details.
- Do not instruct the user to bypass platform rules, obtain unauthorized discounts, or evade anti-abuse systems.

## When To Use

Use this skill for:

- choosing among Meituan merchants for a meal or local-life purchase
- deciding whether a full-reduction threshold is worth crossing
- checking whether a visible group-buy or coupon offer has hidden friction
- weighing cheaper price against slower delivery or weaker merchant trust
- translating screenshots or copied cart details into a clear ordering decision

Prefer another skill when:

- the user wants broad cross-platform shopping comparison rather than a Meituan-specific decision
- the user wants account/order troubleshooting, refund escalation, or private coupon lookup
- the task requires authenticated account access or irreversible platform actions

## Input Discipline

Capture the few inputs that change the call:

- category or exact item
- candidate merchants or offer screenshots
- urgency, such as hungry now, lunch break, dinner planning, appointment, or no rush
- budget ceiling and minimum acceptable quality
- visible subtotal, delivery fee, packaging fee, threshold discount, ETA, distance, rating, and review cues

Ask at most one short follow-up when missing context would flip the recommendation. If the user wants speed, assume ETA matters more. If the user wants lowest cost, still protect them from fake-cheap fee traps.

## Workflow

### 1. Classify The Decision

Choose the active mode:

- **merchant compare**: pick the best store among visible alternatives
- **threshold check**: decide whether to add an item for a discount
- **deal sanity check**: judge a group-buy, coupon, or local-life offer
- **risk triage**: decide whether a weak merchant is still acceptable
- **screenshot readout**: extract only visible facts, then recommend what to verify

### 2. Gather Visible Evidence

For each candidate, capture what is visible:

- merchant name and category fit
- rating, sales cue, recent review signals, and photo/title consistency
- distance, ETA, delivery mode, and deadline fit
- item subtotal, minimum order gap, delivery fee, packaging fee, service fee, and visible threshold discount
- add-on item usefulness if a threshold is involved
- repeated review risks such as delay, wrong item, small portion, hygiene, stale food, spills, or refund friction

Re-snapshot or ask the user for updated visible details after changing location, filters, merchant, selected items, coupon view, or delivery method.

### 3. Compute Checkout Reality

Do not judge by headline discount alone.

Compare:

- natural basket subtotal before artificial add-ons
- fee stack: delivery, packaging, service, tableware, or pickup friction when visible
- threshold gap and whether the add-on is useful
- net saving after the useful add-on and fee stack
- ETA difference and the user's urgency
- merchant trust difference and downside if the order disappoints

Use this language when appropriate:

- `这是门槛价，不是自然到手价。`
- `便宜是便宜，但得靠凑单。`
- `看着省，配送费和包装费把优惠吃掉了。`
- `今天这单时间比省几块钱更值钱。`

### 4. Apply Decision Rules

- If two options differ by only a small amount, prefer faster delivery and stronger merchant trust.
- If one option is more than 15-20 minutes slower and the user is time-constrained, treat the discount as weak unless the saving is material.
- Add an item for a threshold only when the item is useful and the net saving remains positive after fees.
- For low-value solo meals, moderate merchant risk can be acceptable if the user is not deadline-sensitive.
- For shared meals, expensive orders, hygiene-sensitive food, gifts, appointments, or work breaks, weak trust is a strong reason to switch.
- A suspiciously deep discount with weak reviews, mismatch photos, or many complaint patterns should lose unless the user explicitly accepts the risk.
- If live price or ETA is missing, give a directional call and list the exact visible fields needed to confirm it.

### 5. Recommend One Move

End with one clear action:

- order this merchant now
- switch to another merchant
- add one specific useful item to cross the threshold
- do not add anything just for the promotion
- wait or search again
- skip this store

Do not end with `都可以` unless the tradeoff is genuinely flat; even then, choose a default based on the user's stated priority.

## Output

Use this structure unless the user asks for something shorter:

### Recommended Move

Say the action in one sentence, including the winning merchant or offer when known.

### Checkout Reality

Show the real tradeoff: visible subtotal, fees, threshold gap, discount, useful add-on logic, ETA, and whether the headline saving survives.

### Risk Check

Call out merchant trust, review patterns, refund friction, hygiene, delay, mismatch, or deadline risk.

### Confidence And Gaps

State confidence as high, medium, or low based on visible evidence. Name the missing fields that could change the call.

### Before You Order

List user-only checks: final payable amount, address-based ETA, account coupon eligibility, item options, stock, refund or after-sales rule, delivery note, and payment.

## Example Prompts

- `午饭 30 分钟内要吃到，黄焖鸡和麻辣烫两家怎么选？`
- `这家满 35 减 12，但配送费 7 元，要不要为了满减再加一个小菜？`
- `这家便宜 6 元但晚 25 分钟，今天赶会，值得吗？`
- `帮我比较这三个美团商家，只给我该点哪家和下单前核对项。`
- `这家评价有点一般，但离我近，适合现在点吗？`
- `截图里这个团购券看起来便宜，帮我判断有没有隐藏门槛。`

## Package Surface

This published package is intentionally Markdown-only. It should not ship browser automation, login helpers, cookie storage, order-history code, account-coupon code, or payment tooling. If future versions add tools, they must preserve the Safety Contract and make any account-state capability explicit, consent-based, and separate from this public default.

## Quality Bar

Do:

- optimize for the user's immediate decision
- separate headline discount from real cost
- treat ETA, merchant trust, and refund practicality as first-class decision inputs
- make uncertainty visible instead of inventing live price, coupon, stock, or ETA data
- tell the user exactly what to verify manually before ordering

Do not:

- log in or read account pages
- claim account coupons or final payable price are known unless the user supplies visible evidence
- save cookies, orders, addresses, phone numbers, or account data
- mutate cart state, submit an order, confirm an order, or pay
- recommend threshold add-ons that the user does not actually need
