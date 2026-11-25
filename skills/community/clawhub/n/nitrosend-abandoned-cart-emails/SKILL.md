---
name: abandoned-cart-emails
description: >
  Build abandoned cart, abandoned checkout and browse abandonment reminder
  emails for an online store, plus post-purchase and win-back emails, using
  Shopify store activity or events an online store sends through the Events
  API. Use for ecommerce email marketing and cart recovery.
---

# Abandoned cart emails

Recover lost sales for an online store with abandoned cart, abandoned checkout
and browse abandonment reminders, plus post-purchase and win-back emails.

Examples: [Abandoned cart emails](https://nitrosend.com/email-examples/abandoned-cart)

1. Check the store connection in `nitro_get_status`. Shopify connects from
   Integrations in the Nitrosend app; other stores send events through the
   Events API. Don't promise a trigger the account doesn't receive.
2. Use the store events available to the account as the flow trigger, with a
   wait (often one to four hours) before the first reminder and a condition
   that exits anyone who has since ordered.
3. Compose with `nitro_compose_flow` in intent mode; include the cart or
   product details the trigger provides rather than invented products.
4. Offer a discount only if the user asks for one.

## Before anything sends

Use the `send-campaign` and `build-flow` skills for review and delivery:
confirm the account and brand with `nitro_get_status`, keep returned IDs and
revisions, check the saved target with `nitro_review_delivery`, send a test
only with `nitro_send_test_message` when asked, and launch or schedule with
`nitro_control_delivery` only after the user explicitly approves the audience.
A saved draft is not a send. Never invent results, metrics or IDs.
