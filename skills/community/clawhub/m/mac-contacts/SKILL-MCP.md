---
name: mac-contacts
description: >
  Read and manage macOS Contacts. Search by name, email, phone, city, or country.
  Show full contact details including list membership. Create, update, or delete
  contacts. Manage group/list membership. Use whenever asked to look up, add,
  edit, remove, or organise contacts, or when you need someone's phone number,
  email, or address.
---

# Mac Contacts

Access macOS Contacts via MCP tools. All reads use unified contact views (iCloud + local merged).

## Available tools

- `mcp__mac-contacts__search_contacts` — Search by name, org, email, phone, city, or country
- `mcp__mac-contacts__show_contact` — Show all fields for a contact including list membership
- `mcp__mac-contacts__create_contact` — Create a new contact
- `mcp__mac-contacts__update_contact` — Update fields (phones/emails are appended, not replaced)
- `mcp__mac-contacts__delete_contact` — Delete a contact
- `mcp__mac-contacts__add_contact_to_list` — Add contact to a named list
- `mcp__mac-contacts__remove_contact_from_list` — Remove contact from a named list
- `mcp__mac-contacts__list_contact_groups` — List all contact groups

## Examples

```
# Find someone
mcp__mac-contacts__search_contacts(query="Jane Doe")
mcp__mac-contacts__search_contacts(phone="4155551234")
mcp__mac-contacts__search_contacts(email="jane@acme.com")

# Full details
mcp__mac-contacts__show_contact(name="Jane Doe")

# Create
mcp__mac-contacts__create_contact(first_name="Jane", last_name="Doe", phones=["415-555-0100"], emails=["jane@acme.com"])

# Update
mcp__mac-contacts__update_contact(name="Jane Doe", phones=["415-555-0199"])

# List management
mcp__mac-contacts__list_contact_groups()
mcp__mac-contacts__add_contact_to_list(name="Jane Doe", list_name="Work")
```
