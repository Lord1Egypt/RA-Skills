---
name: email-platform-migration
description: >
  Switch email platforms: connect ActiveCampaign, or import contacts, lists,
  tags and custom fields exported as CSV from MailerLite, Brevo
  (Sendinblue), Kit (ConvertKit), beehiiv, Substack, Constant Contact,
  Omnisend or any other platform, keeping unsubscribes and suppressions,
  then rebuild the emails you need. Use for any email migration.
---

# Email platform migration

Move contacts, lists, tags and custom fields from MailerLite, ActiveCampaign,
HubSpot, Brevo (Sendinblue), Kit (ConvertKit), beehiiv, Substack, Constant
Contact, Omnisend, Drip, Campaign Monitor, AWeber, GetResponse or any CSV
export, then rebuild the templates and automations the user still needs.

Guide: [migration FAQ](https://docs.nitrosend.com/faq#contacts-and-migration)

1. Opt-outs first, from every source. Ask the user to export three files from
   the old platform: people who unsubscribed, addresses that bounced, and
   people who marked email as spam. Split any export that mixes them by reason
   (anything suppressed for another reason goes in with the bounced file), and
   remove any phone columns. Send the user the import link
   (`nitro_get_setup_link` with `purpose: "migrate"`, with `provider` for
   Mailchimp, ActiveCampaign, Klaviyo, MailerLite or Brevo, and without it for
   anything else) and have them choose Upload a CSV (Upload a file when the
   link has no provider) for each file: Unsubscribe all from marketing for the
   unsubscribed file, Block all email delivery for the bounced and complaint
   files. Don't import these files yourself with `nitro_import_contacts`. When
   they finish, spot-check a few addresses from each file with `nitro_query`
   (`entity: "suppressions"`,
   `filters: { email: <address>, blocking: true }`): every address must come
   back, with `blocks: "all"` for the bounced and complaint files. If an
   address is missing, or blocks only marketing where it should block all
   email, stop and tell the user.
2. Then the contacts. Mailchimp, ActiveCampaign and Shopify have native
   connectors in Integrations in the Nitrosend app (see `mailchimp-migration`
   and `shopify-email-marketing`); the user connects them from the link. For
   every other platform, including HubSpot, import a CSV of only the people
   who subscribed to email marketing, one file per list (`options.list_ids`)
   plus one for subscribers on no list, without phone columns but with any
   status or consent column left in and unmapped, since the import reads it
   and keeps opted-out rows out of marketing, with `nitro_import_contacts` or
   from the link without a provider (HubSpot's own link offers only a sync).
   An import subscribes the new contacts it creates, so never import everyone
   in an account or CRM.
3. Confirm subscribed, unsubscribed and blocked counts before any send or flow
   activation. While the old platform is still in use, have the user import
   its new opt-outs again before every Nitrosend send.
4. Recreate the templates and automations the user still needs as drafts.
5. A migration never widens consent: an address being on the old list is not
   proof of permission.
