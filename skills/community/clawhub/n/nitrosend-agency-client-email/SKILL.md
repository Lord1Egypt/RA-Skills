---
name: agency-client-email
description: >
  Run email marketing for agency clients: switch between the client accounts
  and brands this connection can reach, create a new brand with its own
  Brand Kit, build each brand's flows and newsletters, and keep each one's
  sender and contacts separate. Use for marketing agencies and freelancers
  managing several brands.
---

# Agency client email

Run email marketing for several clients or brands.

Guide: [Agency email marketing](https://nitrosend.com/agency-email-marketing)

1. `nitro_get_status` lists the accounts and brands this connection can reach.
   Ask which client to work on, then `nitro_select_account` and
   `nitro_select_brand`. Never infer the target from the last one used.
2. To add a new client brand in the selected account, use
   `nitro_set_brand_kit` with `new_brand`, then build its Brand Kit
   (`email-brand-kit`). New client accounts are created in the Nitrosend app,
   not in chat.
3. Keep each brand's sender, contacts, flows and campaigns separate. Never
   copy contacts between clients.
4. Billing and plans for client accounts are managed in the Nitrosend app.

## Before anything sends

Use the `send-campaign` and `build-flow` skills for review and delivery:
confirm the account and brand with `nitro_get_status`, keep returned IDs and
revisions, check the saved target with `nitro_review_delivery`, send a test
only with `nitro_send_test_message` when asked, and launch or schedule with
`nitro_control_delivery` only after the user explicitly approves the audience.
A saved draft is not a send. Never invent results, metrics or IDs.
