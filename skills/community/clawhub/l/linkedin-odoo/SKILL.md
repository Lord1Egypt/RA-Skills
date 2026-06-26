---
name: linkedin-odoo
description: Finds a LinkedIn profile URL for an Odoo contact using their name and company, then saves it to the x_linkedin_url field in Odoo. Trigger when a user asks to find the LinkedIn profile for an Odoo contact or update their LinkedIn URL.
---

# LinkedIn to Odoo Contact Updater

This skill automatically searches for a contact's LinkedIn profile using their name and company name (if available) in Odoo, and updates their `x_linkedin_url` field.

## Setup
The skill uses Odoo credentials via environment variables, same as the `odoo-manager` skill:
- `ODOO_URL`
- `ODOO_DB`
- `ODOO_USERNAME`
- `ODOO_PASSWORD` or `ODOO_API_KEY`

## How to use

Run the Python script located in `scripts/update_linkedin.py` with the Odoo Contact ID as the only argument. 

```bash
python3 scripts/update_linkedin.py <odoo_contact_id>
```

### Process Overview:
1. When asked to find a LinkedIn URL for a specific contact (by name or ID), use the `odoo-manager` skill or script to find the contact's ID.
2. Run `scripts/update_linkedin.py <ID>`.
3. The script will fetch the contact's name and company, run a web search for their LinkedIn profile (`site:linkedin.com/in <Name> <Company>`), and write the URL back to `res_partner.x_linkedin_url`.

### Notes
- The script uses the `html.duckduckgo.com` search to find the LinkedIn profile natively in Python. 
- It requires no additional API keys for the search.
- It targets the specific custom field `x_linkedin_url` provided by the user.