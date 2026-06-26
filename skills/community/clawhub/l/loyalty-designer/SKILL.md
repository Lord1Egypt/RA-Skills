---
name: Loyalty Designer
description: Design points-based, tiered, or referral loyalty programs with reward structures calibrated to your margin and customer purchase frequency.
---

# Loyalty Designer

Customer loyalty programs are margin investments — done right they increase purchase frequency and LTV; done wrong they're expensive discount machines that train customers to wait for rewards. Loyalty Designer helps you build a complete loyalty program architecture from scratch: points structures, tier thresholds, reward catalog, referral mechanics, and the financial model that determines whether the program actually improves contribution margin.

---

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Program type for low-AOV repeat buyers | Points-based (frequent earn/burn) | Tiered with low entry threshold | Referral-only (misses existing behavior) |
| Program type for high-AOV infrequent buyers | Tiered VIP (status + perks) | Cash back | Points (too slow to build engagement) |
| Points earn rate | 1-5% of spend as points value | 6-8% of spend | > 10% (margin-destroying) |
| Tier threshold design | Based on actual purchase frequency data | Estimated from AOV × target visits | Arbitrary round numbers |
| Reward breakage estimate | 20-35% expected (industry norm) | 10-20% conservative | 0% (always dangerous assumption) |
| Referral reward structure | Dual-sided (referrer + referee) | Referrer only | No referral mechanic |

---

## Solves

This skill addresses these specific problems:

1. **High one-time buyer rate** — Most customers buy once and never return; no structured incentive exists to reward repeat behavior.
2. **Unsustainable discount programs** — Store-wide discount codes replace loyalty structures, training customers to buy only on sale and crushing margin.
3. **No differentiation between high-LTV and low-LTV customers** — Everyone receives the same treatment regardless of how much they've spent.
4. **Referral programs that don't launch** — Referral mechanics designed as afterthoughts with no realistic incentive calculation or tracking plan.
5. **Loyalty programs that lose money** — Programs launched without a break-even analysis; earn rates set too generously relative to product margin.
6. **Low engagement after enrollment** — Customers sign up for loyalty programs but never redeem, often because reward thresholds are too high or communication is absent.
7. **Fragmented program mechanics** — Points, tiers, and referrals designed as separate features rather than an integrated system reinforcing each other.

---

## Workflow

### Step 1 — Define program type based on business model

Match the program structure to purchase behavior:

**Points-based programs** work best when:
- AOV is under $100 and customers can realistically purchase 3+ times per year
- Product category has natural repurchase cycles (consumables, apparel basics, pet supplies)
- You want to reward every transaction and build a habit of earning

**Tiered programs** work best when:
- You have a meaningful range of customer spend levels ($200 to $2,000+/year)
- You want to create aspiration and status differentiation
- High-tier customers should receive service-level perks (early access, dedicated support) not just discounts

**Referral programs** work best when:
- Customer acquisition cost (CAC) is high relative to LTV
- Your product has strong word-of-mouth potential (new problem solved, visible product, gift-able item)
- Referral mechanic supplements an existing retention program (not a replacement for it)

Many effective programs combine types: a points foundation with tier status overlaid and a referral accelerator.

### Step 2 — Establish the financial model

Before designing any earn/burn rates, calculate what the program can afford:

```
Max Program Cost % = Gross Margin % − Target Contribution Margin %

Example: 45% gross margin, target 38% contribution after loyalty costs
Max Program Cost = 7% of revenue
```

Within that 7%, allocate:
- Points redemption cost: 3-4% (accounting for 25-30% breakage)
- Tier reward costs: 1-2%
- Referral incentive cost: 1-2%

**Breakage** (points earned but never redeemed) is critical to model accurately. Industry average is 25-35%. Program designs that assume 0% breakage consistently lose money.

### Step 3 — Design the points structure

**Earn rate:**
```
Points earned per dollar = Target redemption value / (100 − breakage %)

If 100 points = $1 reward and 30% breakage:
Customer earns $0.70 in real value per 100 points (you owe $0.70 per 100 pts earned)
Effective cost per dollar spent = earn rate × $0.70
```

**Standard earn rates by reward value:**
- 1 point per $1 spent = $0.01 per point if 100 pts = $1 redemption
- Common: 5 points per $1 with 500 pts minimum redemption = ~1% value to customer

**Minimum redemption threshold:** Set high enough to encourage repeat purchases before redeeming. Target: redemption value equal to 1.5-2× AOV spend required to earn it.

**Point expiry:** Add 12-18 month expiry to manage liability and create urgency. Always notify customers 30 days before expiry.

### Step 4 — Design tier thresholds and benefits

Tier thresholds should be based on actual purchase data:

```
Tier 1 threshold = 12-month spend at or above 40th percentile of active customers
Tier 2 threshold = 12-month spend at or above 75th percentile
Tier 3 threshold = 12-month spend at or above 90th percentile
```

If no data is available, use AOV × estimated annual purchases:
- Bronze: 1-2 purchases per year
- Silver: 3-5 purchases per year
- Gold: 6+ purchases per year or total spend > $X

**Tier benefits structure:**

| Tier | Points Multiplier | Discount | Service Perk | Access Perk |
|---|---|---|---|---|
| Bronze | 1× | None needed | Standard | Standard |
| Silver | 1.5× | 5-10% on select | Priority support | Early sale access |
| Gold | 2× | 10-15% on select | Dedicated line | Pre-launch access |

Benefits should include at least one non-discounted perk per tier to avoid pure discount training.

### Step 5 — Design the referral mechanic

**Dual-sided referral (always preferred):**
- Referrer receives: reward triggered when referee makes first purchase
- Referee receives: discount or bonus on first order

**Referral economics:**
```
Max referral reward = Gross Margin on first referee order − New customer CAC avoided
```

If CAC is $40 and gross margin on first order is $25 → referral reward should not exceed $25 (to avoid spending more than CAC already costs).

**Referral tracking requirements:**
- Unique referral codes or links per customer
- Attribution window: typically 30 days from link share to first purchase
- Fraud protection: limit referrals per account, restrict same-address referrals

### Step 6 — Build the reward catalog

Reward options by cost effectiveness:

| Reward Type | Margin Impact | Customer Perceived Value | Recommended |
|---|---|---|---|
| Discount on future order | High (direct margin cost) | Medium | Limit to % of catalog |
| Free product (own product) | Medium (COGS only) | High | Strong option |
| Free shipping threshold removal | Low (variable) | High for frequent buyers | Yes |
| Early access / experiences | Very low | High for top tier | Yes for Gold tier |
| Third-party gift cards | Fixed cost | Medium | Use sparingly |

### Step 7 — Define the communication and engagement calendar

Loyalty programs fail without ongoing engagement communication:

- **Enrollment confirmation:** Points balance, how to earn, redemption instructions
- **Points milestone emails:** Triggered at 25%, 50%, 75%, and 100% of redemption threshold
- **Expiry warnings:** 30 days, 7 days before point expiry
- **Tier upgrade notification:** Celebrate achievement, show next tier benefits
- **Tier downgrade warning:** 30 days before end of qualifying period
- **Referral nudge:** After 2nd purchase, remind customer of referral program

---

## Worked Examples

### Example 1 — Skincare Brand (High-Repeat, Low-AOV)

**Inputs:**
- Category: Skincare (moisturizers, serums, cleansers)
- AOV: $45
- Purchase frequency: ~4x/year for active customers
- Gross margin: 62%
- Current one-time buyer rate: 68%
- Goal: Increase repeat purchase rate to 45%

**Program design:**

Points structure:
- 5 points per $1 spent
- 500 points = $5 reward (1% effective return to customer)
- Minimum redemption: 500 points ($100 spend required → 2.2 orders to first reward)
- 18-month expiry

Tiers:
- Bronze (default): 0–$149/year spend
- Silver: $150–$299/year (3–4 orders) → 1.5× points, birthday gift
- Gold: $300+/year (6+ orders) → 2× points, free shipping always, early access

Referral:
- Referrer: 250 bonus points (~$2.50 value) on referee's first order
- Referee: $5 off first order
- Max referral reward: $7.50 total (vs. $22 blended CAC)

Financial model:
- Points earn cost: 1% × (1 − 30% breakage) = 0.7% of revenue
- Tier perks: 1.2% of revenue estimated
- Referral cost: 0.8% of revenue at projected referral volume
- **Total loyalty cost: 2.7% of revenue** (well within 7% max)

---

### Example 2 — Home Goods Brand (Low-Frequency, High-AOV)

**Inputs:**
- Category: Furniture and home décor
- AOV: $320
- Purchase frequency: 1-2×/year max for most customers
- Gross margin: 48%
- Goal: Increase referrals and encourage upsell categories

**Program design:**

Tier structure (points too slow for annual buyers):
- Member: 0–$499/year → Free returns, style consultation access
- Insider: $500–$999/year → 5% back on next purchase, priority delivery, early sale
- Elite: $1,000+/year → Personal stylist, white-glove delivery, exclusive catalog access

No standard points: Replace with "purchase credit" — 3% of every order credited to account, redeemable on orders $200+. This avoids the "points feel cheap" problem for luxury positioning.

Referral:
- Referrer: $30 account credit when referee spends $200+
- Referee: 10% off first order
- Financial check: Referee first order $320 → 10% discount = $32 cost. Plus $30 referral credit = $62 total. Gross margin on $320 = $153. Net margin on referred order: $153 - $62 = $91. Positive even on first order.

**Program positioning:** Not called a "loyalty program" — positioned as a "Home Collective membership" to match premium brand positioning.

---

## Common Mistakes

1. **Setting earn rates before calculating margin math** — Many programs launch at 2-5% customer value before checking whether that's sustainable at scale.

2. **Zero breakage assumption** — Assuming all points will be redeemed. Industry data shows 25-35% of points are never redeemed. Building this into financials reduces required earn rates.

3. **Tier thresholds too easy to reach** — If 70% of customers immediately qualify for Silver, Silver has no aspirational value and you're giving Silver perks to everyone.

4. **Discount-only reward catalogs** — Training every customer to seek discounts. Mix discount rewards with experience and access rewards to protect margin and increase perceived program value.

5. **No engagement communication plan** — Launching a program without points milestone emails means most enrolled customers forget they're in it.

6. **Single-sided referral programs** — Referral programs that only reward the referrer (and not the new customer) consistently underperform because the referee has no incentive to act.

7. **Points expiry that's too short** — 6-month expiry feels punitive and drives disengagement. 12-18 months is standard; expire too fast and customers opt out entirely.

8. **Program design doesn't match brand positioning** — A luxury brand calling it a "points program" with a leaderboard cheapens perception. Program design must match brand voice.

9. **No fraud prevention** — Referral programs without same-address restrictions or account limits quickly attract abuse from customers self-referring or creating duplicate accounts.

10. **Launching without a sunset plan** — If the program doesn't achieve retention goals after 12 months, you need a way to end or restructure it without alienating enrolled customers.

---

## Resources

- `references/output-template.md` — Full loyalty program design output format
- `references/program-economics-guide.md` — Financial modeling for points, tiers, and referrals
- `references/tier-design-benchmarks.md` — Industry benchmarks for thresholds and benefit structures
- `assets/loyalty-design-checklist.md` — Pre-launch and quarterly program health checklist
