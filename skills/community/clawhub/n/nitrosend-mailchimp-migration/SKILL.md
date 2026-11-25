---
name: mailchimp-migration
description: >
  Migrate from Mailchimp to Nitrosend: connect Mailchimp to bring audiences,
  members and merge fields with subscribed, unsubscribed and cleaned status
  preserved, then rebuild the campaigns and customer journeys you still need
  as Nitrosend emails and flows. Use when moving an email list from
  Mailchimp.
---

# Mailchimp migration

Move a user from Mailchimp to Nitrosend without losing consent.

Guides: [Mailchimp integration](https://docs.nitrosend.com/integrations/mailchimp)
and the [migration FAQ](https://docs.nitrosend.com/faq#contacts-and-migration)

1. Bring the opt-outs across before connecting. Ask the user to export
   Mailchimp's unsubscribed contacts, cleaned (bounced) addresses and spam
   complaints as CSV, with any phone columns removed. Send them the import
   link (`nitro_get_setup_link` with `purpose: "migrate"` and
   `provider: "mailchimp"`) and have them choose Upload a CSV for each file:
   Unsubscribe all from marketing for the unsubscribed file, Block all email
   delivery for the cleaned and complaint files. Don't import these files
   yourself with `nitro_import_contacts`.
2. When the user says those imports have finished, spot-check a few addresses
   from each file with `nitro_query` (`entity: "suppressions"`,
   `filters: { email: <address>, blocking: true }`): every address must come
   back, with `blocks: "all"` for the cleaned and complaint files. If an
   address is missing, or blocks only marketing where it should block all
   email, stop and tell the user. A later sync never resubscribes an address
   that is unsubscribed or blocked this way.
3. The Mailchimp connector in Nitrosend Integrations imports audiences as
   lists, members as contacts, names and common merge fields, and source
   metadata. Only `subscribed` members are opted in; no other Mailchimp status
   grants email opt-in.
4. The user connects Mailchimp in the Nitrosend app (OAuth), from the same
   link; don't ask for Mailchimp credentials in chat.
5. Campaign history, templates and reports don't migrate. Rebuild the emails
   and customer journeys the user still needs with `nitro_compose_campaign`
   and `nitro_compose_flow`, saved as drafts.
6. Nothing sends and no flow activates as part of the migration. Confirm
   subscription counts with `nitro_query` before any send. While Mailchimp is
   still in use, have the user import its new unsubscribes, bounces and
   complaints again the same way before every Nitrosend send.
