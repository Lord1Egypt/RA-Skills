---
name: signup-form-builder
description: >
  Create a website signup form for a mailing list and get the embed snippet
  for Webflow, Squarespace, WordPress, Wix, Shopify or any website. New
  subscribers join the list and can get a welcome email automatically. Use
  for signup forms, subscribe forms, newsletter signups, lead capture and
  growing an email list.
---

# Signup form builder

Give the user a signup form for their website so new subscribers land on a
Nitrosend list.

Guide: [Website signup forms](https://docs.nitrosend.com/guides/website-signup-forms)

1. Resolve or create the destination list (`nitro_query`,
   `nitro_manage_audience` (`operation: "manage_list"`, `action: "create"`)).
2. The embed snippet uses the brand's public website key (`wpkey_live_…`),
   which is safe in website code. Never put a secret key (`nskey_live_…`) in a
   snippet. If you can't read the public key, send the user to Contacts, the
   list, then the Website signup form panel to copy it.
3. Hand over the snippet for their site (Webflow, Squarespace, WordPress, Wix,
   Shopify or plain HTML) and keep the hidden honeypot field.
4. Joining the list fires that list's live `list_add` flows, so pair the form
   with the `welcome-email-series` skill.

See `nitro_search_docs` for "website signup forms" for snippet styles.
