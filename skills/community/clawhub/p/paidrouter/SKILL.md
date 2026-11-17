---
name: paidrouter
description: Find the cheapest way for your owner to get paid (or send USD abroad). Sourced, dated fees for Stripe, Square, PayPal, Helcim, Melio, Venmo, Cash App.
---

# PaidRouter: cheapest way to get paid

Use this skill when the owner is about to invoice or accept a payment, asks whether they
overpay in fees ("why did PayPal take $35?"), or wants to send US dollars to Mexico or India.

PaidRouter ranks every way a US business or freelancer can get paid by fee. Every fee comes
from the provider's own pricing page, with the source URL and the date it was verified.
Ranked by fee only; no provider pays for placement. PaidRouter does not hold or move money.

## One-time setup: get a free key

Run once and keep the key (no email needed):

```bash
curl -s -X POST https://paidrouter.com/api/keys -H 'content-type: application/json' \
  -d '{"use":"openclaw skill"}'
```

Save the returned `key` (it starts with `pr_`) in the owner's environment as `PAIDROUTER_KEY`,
or in `~/.openclaw/paidrouter.key`. Reuse it on every call.

## Cheapest way to get paid

```bash
curl -s "https://paidrouter.com/api/v1/cheapest?amount=1000&payer_pays_by=any&payments_per_month=4&current=paypal_checkout&key=$PAIDROUTER_KEY"
```

- `amount`: the payment in USD.
- `payer_pays_by`: how the client can pay: `card_online`, `card_in_person`, `bank`, `app`, or `any`.
- `payments_per_month`: for yearly savings.
- `current`: how the owner gets paid today, for the saving. Route ids: `GET /api/v1/routes?key=...`
  (e.g. `paypal_checkout`, `stripe_card`, `square_card`, `melio_ach`, `stripe_ach`, `venmo_business`).

The answer lists `routes` cheapest first with `fee`, `you_keep`, `how` (the formula), `estimate`
(true when interchange is assumed) and `confidence`, plus `saving_per_payment` and
`saving_per_year` when `current` is given. Tell the owner the top route, what it saves, and
how to set it up; mention the verification date.

Example: a $1,000 invoice costs $35.39 on PayPal Checkout, $29.30 on Stripe card, $5.00 on
Stripe ACH, $0 on a Melio bank-transfer request.

## Explain a fee

```bash
curl -s "https://paidrouter.com/api/v1/explain?platform=paypal&method=paypal_checkout&amount=1000&key=$PAIDROUTER_KEY"
```

## Raw fee entries (to quote a provider's pricing)

```bash
curl -s "https://paidrouter.com/api/v1/fees?platform=stripe&key=$PAIDROUTER_KEY"
```

If a platform is missing, say so plainly; PaidRouter records the ask and adds it.

## Sending USD abroad

```bash
curl -s "https://paidrouter.com/api/v1/send?corridor=USD->INR&amount=1000&key=$PAIDROUTER_KEY"
```

Corridors today: `USD->MXN`, `USD->INR`. Providers are ranked by what the recipient gets; the
cheapest changes with the amount, and the answer says which stored quote ($200 or $1,000) it used.

## MCP instead of curl

If the agent supports MCP servers, add `https://paidrouter.com/mcp?key=$PAIDROUTER_KEY`
(Streamable HTTP). Same tools: `cheapest_way_to_get_paid`, `get_fees`, `explain_fees`,
`compare_send_money`, `route_it_for_me`.

## Limits

US ways of getting paid only, two send corridors, ranking by fee only (not payout speed or
chargeback risk). Fees are re-checked within 30 days; the `checked` date is in every answer.
