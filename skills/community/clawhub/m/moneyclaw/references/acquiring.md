# Acquiring Reference

Use this reference only when the user explicitly wants merchant-side payment collection rather than buyer-side card spending.

## Table of Contents

1. When To Use Acquiring
2. Merchant Setup
3. Invoice Flow
4. Public Checkout And Widget
5. Webhooks
6. Fees And Lifecycle Notes

## 1. When To Use Acquiring

Switch to acquiring when the user wants to:

- accept USDT from customers
- create hosted invoices
- embed a payment widget on a site
- receive server-side payment notifications

Do not switch to acquiring by default. Buyer-side card purchases remain the primary MoneyClaw use case.

## 2. Merchant Setup

### Enable merchant mode

`POST /api/acquiring/setup`

What it does:

- creates merchant settings for the authenticated user
- generates a webhook secret
- enables merchant mode

Important:

- the `webhookSecret` is shown once
- store it immediately if the user plans to verify webhooks

### Read or update settings

- `GET /api/acquiring/settings`
- `PATCH /api/acquiring/settings`

Settings support:

- `storeName`
- `webhookUrl`
- `enabled`

## 3. Invoice Flow

### Create an invoice

`POST /api/acquiring/invoices`

Useful request fields:

- `amount` - minimum `1`
- `description`
- `reference`
- `callbackUrl`
- `expiresIn` - default `3600`, min `300`, max `86400`

Important response fields:

- `id`
- `amount`
- `fee`
- `netAmount`
- `status`
- `depositAddress`
- `checkoutUrl`
- `expiresAt`

Typical flow:

1. make sure merchant mode is enabled
2. create invoice
3. show the hosted `checkoutUrl` or embed the widget
4. customer pays USDT
5. confirm paid status before fulfilling the order

### List or inspect invoices

- `GET /api/acquiring/invoices`
- `GET /api/acquiring/invoices/{invoiceId}`

Use these to:

- review invoice history
- inspect current invoice state
- reconcile paid vs pending invoices

## 4. Public Checkout And Widget

Public endpoints do not require Bearer auth:

- `GET /api/acquiring/public/invoices/{id}`
- `GET /api/acquiring/public/invoices/{id}/status`

The widget is served from:

- `https://moneyclaw.ai/widget.js`

Core widget usage:

```html
<div id="moneyclaw-pay"></div>
<script src="https://moneyclaw.ai/widget.js"
  data-invoice-id="INVOICE_ID"
  data-theme="dark">
</script>
```

Important widget notes:

- `data-invoice-id` is required
- client-side widget events are for UX only
- confirm payment server-side before fulfilling an order

## 5. Webhooks

If `callbackUrl` is set, MoneyClaw sends a signed POST when an invoice is paid.

Things to verify:

- use the saved `webhookSecret`
- verify `X-Webhook-Signature`
- compute `HMAC-SHA256(requestBody, webhookSecret)` and compare

Do not fulfill orders based only on browser events or optimistic UI state.

## 6. Fees And Lifecycle Notes

- fee: `$0.30 + 3%` per paid invoice
- no fee on unpaid or expired invoices
- invoice expiry is applied lazily on read in the current MVP
- public status polling exists, but should be used conservatively
