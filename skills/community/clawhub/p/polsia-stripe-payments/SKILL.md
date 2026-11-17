---
name: stripe-payments
description: "Accept payments on a Polsia-built site via Stripe Connect payment links, then verify them server-side — no Stripe SDK, no webhooks, no STRIPE_SECRET_KEY."
---

# Stripe Payments

Accept card payments through the company's auto-provisioned Stripe Connect account. You create payment links with MCP tools, then verify completed payments server-side. No Stripe SDK, no webhook setup, no STRIPE_SECRET_KEY.

## How the money works

Every company has a Stripe Connect (Express) account. Polsia takes 20% platform fee, company keeps 80% (minus Stripe processing fees). Payouts are daily to their bank.

The account is RESTRICTED until owner finishes Stripe onboarding on the Polsia Payments page. Until then it cannot take payments.

NO bring-your-own-Stripe. Do NOT set STRIPE_SECRET_KEY, do NOT npm install stripe, do NOT build webhooks.

## 1. Create Payment Link

Call the MCP tool with name, amount, and success_url pointing at YOUR app with {CHECKOUT_SESSION_ID} placeholder.

Always pass success_url. Without it, the buyer is redirected to Polsia, not your app.

One-time fixed price: create_payment_link. Recurring: create_subscription_link.

## 2. Success Page — Poll, Don't Verify Once

The payment record is written asynchronously (Stripe to Polsia webhook, ~1s+ after redirect). A single synchronous verify on the success page usually returns verified:false. Render a loading page and poll every 1500ms up to 10 times.

## 3. Verify Server-Side

GET process.env.POLSIA_API_BASE_URL + '/api/company-payments/verify?session_id=' + sessionId
Auth: Authorization: Bearer process.env.POLSIA_API_KEY

Use POLSIA_API_BASE_URL (NOT POLSIA_API_URL which points at AI proxy). Make fulfillment idempotent, keyed on sessionId.

## DO NOT

- Set STRIPE_SECRET_KEY or install Stripe SDK
- Use POLSIA_API_URL for payment endpoints
- Verify only once on success page — poll
- Hardcode buy.stripe.com links
