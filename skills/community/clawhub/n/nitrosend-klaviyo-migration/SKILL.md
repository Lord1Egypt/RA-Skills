---
name: klaviyo-migration
description: >
  Migrate from Klaviyo to Nitrosend: import profiles and lists exported from
  Klaviyo as CSV, keep unsubscribes and suppressions, then rebuild flows
  such as welcome series, abandoned cart and post-purchase as Nitrosend
  drafts and connect Shopify for store events. Use when moving email
  marketing from Klaviyo.
---

# Klaviyo migration

Move a user from Klaviyo to Nitrosend.

Guide: [migration FAQ](https://docs.nitrosend.com/faq#contacts-and-migration)

1. Opt-outs first. Ask the user to export Klaviyo's suppressed profiles
   (Audience, Profiles, View suppressed profiles) as CSV. That file mixes
   unsubscribes, bounces and spam complaints, so split it by reason, and
   remove any phone columns.
2. Send the user the import link (`nitro_get_setup_link` with
   `purpose: "migrate"` and `provider: "klaviyo"`) and have them choose Upload
   a CSV for each file: Unsubscribe all from marketing for the unsubscribes,
   Block all email delivery for every other suppressed profile. Don't import
   these files yourself with `nitro_import_contacts`. When they finish,
   spot-check a few addresses from each file with `nitro_query` (`entity:
   "suppressions"`, `filters: { email: <address>, blocking: true }`): every
   address must come back, with `blocks: "all"` for the bounce, complaint and
   other suppression files. If an address is missing, or blocks only marketing
   where it should block all email, stop and tell the user.
3. Then ask for a CSV of the profiles who subscribed to email, one export per
   list or segment (open it in Klaviyo and choose Export to CSV), with phone
   columns removed and the Email Marketing Consent column left in and
   unmapped: the import reads it and keeps anyone marked unsubscribed or never
   subscribed out of marketing. Import each into its list with
   `nitro_import_contacts`: reserve with `upload`, PUT the file to the
   returned URL with its headers, then call it again with the `signed_id`,
   `columns` and `options.list_ids`. The user can upload them from the same
   link instead. Leave out anyone who never subscribed. An import subscribes
   the new contacts it creates, so never import a whole account.
4. Imports don't start flows unless the user turns on Start flows. Confirm
   subscribed, unsubscribed and blocked counts with `nitro_query` before any
   send. While Klaviyo is still in use, have the user import its new opt-outs
   again before every Nitrosend send.
5. Rebuild Klaviyo flows (welcome series, abandoned cart, browse abandonment,
   post-purchase, win-back) with `nitro_compose_flow` as inactive drafts, and
   connect Shopify in Integrations for store events.
