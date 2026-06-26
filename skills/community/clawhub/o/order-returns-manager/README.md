# 📦 Order & Returns Manager — OpenClaw Skill

Manage Shopify and WooCommerce orders and returns end-to-end from WhatsApp or Telegram.
Check order status with live tracking, process returns, approve refunds, restock inventory,
flag fraud, and get a morning summary — all from a single message.

UK-focused: Consumer Rights Act compliance built in so you never accidentally break the law.

## What it does

- **Order lookup** — find any order by number, email, or customer name. Includes live carrier tracking for Royal Mail, DPD, Evri, DHL, and Parcelforce
- **Returns & refunds** — full approval workflow, auto-restock, return instruction emails to customers, partial refunds
- **UK law guard** — blocks illegal return denials and warns you before you expose the store to chargebacks or Trading Standards complaints
- **Fulfilment** — mark orders as dispatched, add tracking numbers, notify customers
- **Cancellations** — cancel unfulfilled orders with automatic refund and restock
- **Fraud detection** — scores new orders against 8 risk signals including freight forwarder addresses and disposable email domains
- **Lost parcel handling** — separate workflow for "not received" claims distinct from returns
- **Reports** — morning orders summary, weekly/monthly returns report with return rate by product

## Example usage

```
You:  check order 1234
Bot:  📦 Order #1234 — James Thornton · Fulfilled ✅ · £67.98
      Royal Mail TT123456785GB · In transit · est. delivery 11 Apr
      Actions: return / cancel / resend tracking / note

You:  customer wants to return it, changed his mind
Bot:  ↩️ Return request — 12 days, within window ✅ · £34.99 · customer pays return ship
      YES / DENY / PARTIAL?

You:  yes
Bot:  ✅ Refund issued · Restocked · Return email sent
```

## Setup

1. Add `read_orders`, `write_orders`, `write_fulfillments`, `read_customers`, `write_inventory` scopes to your Shopify custom app
2. Tell your bot: `Set my store: my-store-handle, token: shpat_xxx`
3. Optionally set your return address: `My return address is: [address]`

Full setup guide: see `CONFIG.md`

## Platforms

- Shopify (all plans) — full support
- WooCommerce (REST API v3) — full support

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full skill — 9 workflows, UK law reference, fraud detection |
| `EXAMPLES.md` | 7 real-world examples showing expected behaviour |
| `CONFIG.md` | Setup guide, required API scopes, troubleshooting |

## Notes

- Returns are checked against UK Consumer Rights Act 2015 before any denial is allowed
- Fraud detection includes UK-specific freight forwarder postcodes
- Dates always in UK format (DD MMM YYYY)
- Currency always GBP (£)
- Works alongside the Shopify Product Uploader skill
