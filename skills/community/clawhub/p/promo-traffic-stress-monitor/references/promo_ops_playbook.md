# Promo ops & traffic stress playbook

For `promo-traffic-stress-monitor` when you need extra detail.

---

## 1. Metrics (define in every answer)

| Metric | Role |
|--------|------|
| Sessions / clicks | Load |
| Orders | Output |
| CVR | sessions→orders or clicks→orders (state which) |
| Spend | Ads cash out |
| ROAS or MER | revenue / ad spend (or total revenue / total paid) |
| Breakeven ROAS | 1 / (margin after variable costs) — merchant must confirm margin |

---

## 2. First 4 hours — what “good” looks like (illustrative)

- CVR **not below** pre-promo same weekday band by more than ~20–30% without reason (landing change, OOS).
- ROAS **at or above** breakeven if goal is volume; above target if goal is profit.
- No spike in **checkout error** or **bounce on checkout** vs cart.

---

## 3. Scale vs hold (decision)

| Condition | Suggested ad action |
|-----------|---------------------|
| ROAS > target, CVR stable, stock OK | Increase budget on winning ad sets; duplicate angle |
| ROAS between breakeven and target | Hold; optimize creative/placement |
| ROAS < breakeven | Cut or pause; fix lander/checkout first |
| Hero SKU OOS | Pause SKU-specific ads; redirect to in-stock alternates |

---

## 4. Restock + comms

- PDP banner: **Back soon — notify me** or **Similar in stock**
- Email/SMS to waitlist if SKU returns mid-promo
- Don’t raise bid on OOS URLs

---

## 5. Traffic allocation (budget split)

- **Winner**: last 4h ROAS rank + volume
- **Laggard**: high spend, low CVR → reduce or swap creative
- **Test bucket**: small % on new angle only after base stable
