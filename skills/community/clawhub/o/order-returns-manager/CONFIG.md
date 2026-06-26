# Order & Returns Manager — Setup Guide

## Step 1 — Add API scopes to your Shopify app

Go to Shopify Admin → Settings → Apps → your custom app → Configure Admin API scopes.
Add all of the following:

| Scope | Why it's needed |
|-------|----------------|
| `read_orders` | View order data, status, line items |
| `write_orders` | Cancel orders, add notes, update status, update address |
| `write_fulfillments` | Mark orders as dispatched, add tracking |
| `read_fulfillments` | Check fulfilment status |
| `read_customers` | Search orders by customer name/email |
| `write_inventory` | Restock items when returns are processed |
| `read_inventory` | Check current stock levels |
| `read_draft_orders` | Read exchange replacement orders |
| `write_draft_orders` | Create exchange replacement orders |

If you already have the Shopify Product Uploader skill installed, you may already
have some of these. Add any that are missing and reinstall the app.

---

## Step 2 — Configure the skill

Send your OpenClaw bot this message:

```
Set my orders config:
Store: my-store-name
Token: shpat_xxxxxxxxxxxxxxxxxxxx
Return window: 30 days
Auto-restock on return: yes
Require my approval for refunds: yes
Fraud alert above: £150
My return address: [your full return postal address]
```

---

## Step 3 — WooCommerce setup (if applicable)

Generate API keys in WooCommerce → Settings → Advanced → REST API → Add key.
Give it Read/Write permissions.

Then send:
```
Set my WooCommerce config:
Platform: woocommerce
Domain: mystore.co.uk
Consumer key: ck_xxxxxxxxxxxxxxxxxxxx
Consumer secret: cs_xxxxxxxxxxxxxxxxxxxx
```

---

## Step 4 — Test

Try: `check order [any recent order number]`

If you see the order summary, you're set up correctly.

---

## Required Shopify API version

This skill uses Shopify Admin REST API 2025-01.
Your app will use the version specified — default is 2025-01.

---

## Troubleshooting

**"401 Unauthorized"**
→ Token is wrong or expired. Go to Shopify Admin → Apps → your app → API credentials → regenerate.

**"403 Forbidden"**
→ A required scope is missing. Check the table in Step 1 and add the missing scope.

**"Order not found"**
→ Try searching by customer email instead of order number.
→ Ensure you're using the order number without the # symbol, or with it — both work.

**"Refund failed — already refunded"**
→ The order has already been refunded. The skill will show the existing refund details.

**Inventory not restocking**
→ The skill needs your location ID. Send: `what's my Shopify location?` and it will
fetch and store it automatically.

**Tracking not showing live status**
→ Some carrier tracking pages block automated fetches. The skill will always provide
the direct tracking URL as a fallback.

---

## UK Consumer Law quick reference

The skill enforces these automatically, but it's useful to know them:

| Situation | Minimum customer right |
|-----------|----------------------|
| Any online order, any reason | Cancel within 14 days of delivery — full refund |
| Faulty or not as described | Full refund within 30 days, no quibble |
| Fault proven at time of sale | Up to 6 months — repair, replace, or refund |
| Item not delivered | Full refund — carrier risk is merchant's, not customer's |

Source: Consumer Rights Act 2015 · Consumer Contracts Regulations 2013
