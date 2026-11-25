---
name: contacts-and-segments
description: >
  Manage contacts, email lists, segments, tags and subscribers: import
  contacts by CSV, sync HubSpot or Attio, search a contact's history, build
  segments from data and engagement, and verify email addresses to clean the
  list. Use for audience management and email list hygiene.
---

# Contacts and segments

Manage contacts, lists, tags, segments and email list hygiene.

Guides: [Managing contacts](https://docs.nitrosend.com/guides/managing-contacts) and
[segments](https://docs.nitrosend.com/concepts/segments)

- Find people with `nitro_search_contacts`; list and count with `nitro_query`.
- Create or update contacts (`nitro_manage_audience` (`operation: "create_contact"`), `nitro_manage_audience` (`operation: "update_contact"`)),
  manage lists (`nitro_manage_audience` (`operation: "manage_list"`, `action: "create"`), `nitro_manage_audience` (`operation: "manage_list"`, `action: "add_contacts"`)) and
  tags (`nitro_manage_audience` (`operation: "bulk_tag"`)). List additions can trigger live flows.
- Build dynamic audiences with `nitro_define_segment` from attributes, tags,
  lists, events and engagement.
- Clean a list with `nitro_manage_audience` (`operation: "validate"`, `dry_run: true`), show the quote, then
  the same operation with its `quote_digest` after the user
  agrees.
- Deleting contacts or lists needs a preview and the user's confirmation.

Import only contacts the user is authorised to email.
