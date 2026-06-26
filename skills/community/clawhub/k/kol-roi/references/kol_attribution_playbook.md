# KOL attribution, refunds, and traffic quality playbook

Load when `kol-roi` needs depth. Use by section.

---

## 1. Joining orders to creators

| Signal | Strength | Pitfall |
|--------|----------|---------|
| Unique discount code | High if exclusive | Code sharing on deal sites |
| UTM `utm_campaign` or `utm_content` | High if enforced | Stripped in apps / iOS |
| Affiliate network click ID | High for network orders | Cross-device loss |
| Link-in-bio aggregator | Medium | Multi-brand dilution |

Pick **one primary rule** per report; if hybrid, show **overlap** and **dedupe** logic.

---

## 2. Refunds and chargebacks

- Match **refund date** to reporting window policy (refund in month T vs order in month T−1).  
- **Partial refunds**: reduce net revenue; note if commission platform claws back **pro-rata**.  
- **Chargebacks**: treat like refunds for "true" contribution unless user says otherwise.

---

## 3. Fake or junk traffic (heuristics, not legal proof)

- Session **duration** and **engaged sessions** by `source/campaign` vs creator.  
- **Conversion rate** vs brand baseline; sudden **0% purchase** with huge clicks.  
- **Geo** and **device** concentration; **new customer %** collapse.  
- **Single-use codes** appearing on **public coupon aggregators**.

Recommend **verification** (cap payout, delayed commission, code rotation)—do not accuse publicly without evidence.

---

## 4. True ROI formulas (pick and label)

**A. Payout-as-cost (no COGS):**  
\(\text{ROI} = (\text{Net revenue} - \text{Commissions} - \text{Fees}) / (\text{Fixed fees} + \text{Commissions})\)

**B. Contribution margin (with margin %):**  
\(\text{Contribution} = \text{Net revenue} \times m - \text{Creator costs}\)  
then ROI vs creator spend as user prefers.

Always show **denominator** (what "cost" includes).

---

## 5. Renewal rubric (quick)

| Signal | Lean toward |
|--------|-------------|
| Net revenue ↑, refund % stable, ROI > hurdle | **Renew** |
| Revenue OK but refund ↑ or code leakage | **Renegotiate** (cap, exclusivity, new code) |
| Spend ↑, net flat, junk traffic flags | **Pause** or **test** smaller cap |
| Sample &lt; N orders | **Test extension**, wider window |

---

## 6. Exports checklist (minimum columns)

- Order ID, date, gross, refunded amount, net paid  
- Discount codes / UTM fields  
- Customer new vs returning (if available)  
- SKU or category (for margin if needed)  
- Affiliate payout row: creator ID, commission, flat fee period
