---
name: email-brand-kit
description: >
  Build an email brand kit from a website: logo, brand colours, fonts and
  tone of voice, so newsletters, campaigns and automated emails match the
  brand. Use for email branding, a brand kit, on-brand email design, brand
  guidelines or brand voice.
---

# Email Brand Kit

Turn the user's website into the Brand Kit every Nitrosend email is designed
from: logo, brand colours, heading and body fonts, company description and
tone of voice.

Guide: [Brand Kit and AI Memory](https://docs.nitrosend.com/integrations/mcp-brand-kit-memory)

1. Ask for the website if you don't have it.
2. Call `nitro_set_brand_kit` with one stable idempotency key to scan and save
   it. With `dry_run: true`, keep the returned `scan_id` and do not claim the
   Brand Kit is saved until the real call succeeds.
3. Show what was captured and ask the user to correct anything that is wrong
   (an old logo, a secondary colour picked as primary, the wrong voice).
4. For manual edits, read `nitro://brand-kit` and change only the fields the
   user named. Upload a local logo through `nitro_ingest` before setting
   `logo_url`.

Without a website, ask for the real business name and one sentence on what it
offers and for whom. Never invent business details or a mailing address.

## Before anything sends

Use the `send-campaign` and `build-flow` skills for review and delivery:
confirm the account and brand with `nitro_get_status`, keep returned IDs and
revisions, check the saved target with `nitro_review_delivery`, send a test
only with `nitro_send_test_message` when asked, and launch or schedule with
`nitro_control_delivery` only after the user explicitly approves the audience.
A saved draft is not a send. Never invent results, metrics or IDs.
