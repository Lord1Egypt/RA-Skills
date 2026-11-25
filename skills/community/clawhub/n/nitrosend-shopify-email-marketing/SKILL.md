---
name: shopify-email-marketing
description: >
  Run Shopify email marketing: connect a Shopify store, import customers
  with their marketing consent, and use orders, refunds and store activity
  in segments, newsletters and automated emails. Use for Shopify email,
  ecommerce email marketing and online store emails.
---

# Shopify email marketing

Run email marketing for a Shopify store.

Guide: [Shopify email marketing](https://nitrosend.com/shopify-email-marketing)

1. If the store is moving from another email tool, bring that tool's opt-outs
   across before connecting (see `klaviyo-migration` or
   `email-platform-migration`). Shopify then connects from Integrations in the
   Nitrosend app. It imports customers with their Shopify marketing consent
   (others arrive unsubscribed), keeps products and customer details up to
   date, and records checkouts, orders and refunds as events.
2. Build segments from store activity with `nitro_define_segment` (buyers,
   repeat customers, lapsed customers).
3. Build the core flows as drafts: welcome series, abandoned cart, post-purchase
   and win-back (see `abandoned-cart-emails`), then campaigns for launches and
   sales.
4. Don't email customers who didn't opt in to marketing. Consent is read when
   a customer is imported, so before a campaign ask the user whether anyone
   has opted out in Shopify since, and unsubscribe them first with
   `nitro_manage_audience` (`operation: "set_subscription"`, `kind: "email"`,
   `opt_out: true`).
