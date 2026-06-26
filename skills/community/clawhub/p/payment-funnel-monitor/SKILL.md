---
name: payment-funnel-monitor
description: Monitor the payment last mile — initiate → success reconciliation → local method gaps — to recover conversion lost to failed checkouts. Use when payment success rate is below ~95%, specific countries (e.g. Brazil, Germany) underperform vs baseline, support tickets spike for payment timeouts or declines, gateway errors after Shopify/Woo/Stripe updates, or the user asks to fix checkout payment failures. Deliver failure error-code analysis and a prioritized list of local payment methods to add. Also trigger on 3DS/SCA friction, wallet coverage, or "orders drop at pay button." Do NOT use for non-payment checkout fields only (shipping form) with no pay-step failure signal, or pure accounting payout reconciliation with no authorization success rate.
compatibility:
  required: []
---

# Payment funnel monitor

You own **pay step → authorization outcome**: metrics, **error code interpretation**, and **payment-method completion** so fewer sessions die at the last click.

## When to lean in

- **Success rate &lt; ~95%** (define: successful charges / payment attempts or sessions reaching pay — align with merchant).
- **Country anomalies** (BR, DE, IN, etc.) vs global baseline.
- **Timeout / decline** ticket volume high.

## Core workflow

1. **Reconcile funnel** — Initiated payment → submitted → succeeded vs failed vs abandoned (if data exists).
2. **Error code analysis** — Group by gateway code / decline reason; map to action (retry, 3DS, enable local rail, fraud rule).
3. **Local method strategy** — Per underperforming country, recommend **wallets, bank transfer, installments, local cards** as appropriate.

## Gather context

1. Platform + gateways (Stripe, Adyen, PayPal, Shopify Payments, etc.).
2. Date range; overall and **by country** success rate.
3. Sample error codes or ticket themes.
4. Current payment methods enabled per market.

Read `references/payment_codes_and_methods.md` for code families and country method hints.

## Mandatory success outputs (every full run)

### 1) Failure error code analysis

Structured block — table or bullet groups:

| Error / decline family | Example codes (illustrative) | Likely cause | Action |
|-------------------------|------------------------------|--------------|--------|
| Insufficient funds | issuer codes | Customer | Messaging; retry |
| 3DS / SCA failed | authentication_required | Bank / UX | 3DS flow, fallback |
| Timeout | gateway timeout | Latency / mobile | Timeout config, alternate method |
| Blocked / fraud | do_not_honor, risk | Rules / issuer | Review rules; local method |
| … | … | … | … |

Use **merchant’s actual codes** when provided; otherwise use gateway-typical families and label as examples.

### 2) Recommended local payment methods (checklist)

Per **priority country** (or globally), output a **checklist** table:

| Market | Recommended method | Role | Enable via (typical) |
|--------|-------------------|------|----------------------|
| Brazil | Pix | Instant, high success | Stripe Pix, PSP |
| Brazil | Boleto (if applicable) | Unbanked | Local PSP |
| Germany | PayPal, SEPA, Klarna | Trust + bank debit | Gateway settings |
| … | … | … | … |

At least **three rows** when multi-country; tie rows to **observed** underperformance or generic BR/DE if user named them.

## KPI snapshot (include when possible)

| Metric | Value | Target |
|--------|-------|--------|
| Payment success rate | … | ≥95% |
| Success by country (worst 3) | … | vs global |
| Timeout / unknown fail share | … | minimize |

## When NOT to use

- Shipping-only abandonment with no payment attempt data.
- Merchant payout settlement with no authorization funnel ask.

## Split with other skills

- **Abandoned checkout (full funnel)** — use when drop is before pay; this skill is **pay-step deep**.
- **Promo traffic stress** — use when whole-site CVR drops under load.
