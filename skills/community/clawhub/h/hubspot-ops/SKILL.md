---
name: hubspot-ops
description: HubSpot CRM API integration with managed OAuth. Manage contacts, companies, deals, pipelines, tickets, products, line items, marketing emails, and workflows. Use this skill when users want to work with HubSpot CRM data or automate sales and marketing operations.
---

# HubSpot

![HubSpot](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/hubspot.svg)

Access HubSpot CRM via the HubSpot API with managed OAuth authentication. Manage contacts, companies, deals, pipelines, tickets, products, line items, and more.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=hubspot-ops) for hosted connection flows and credentials so you do not need to configure HubSpot API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect HubSpot |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect HubSpot |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│     HubSpot      │
│   (User Chat)   │     │   (OAuth)    │     │   (CRM API)      │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect HubSpot   │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  HubSpot │
   │  File    │           │ Auth     │           │   CRM    │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for HubSpot again."

## Quick Start

```bash
# List contacts
clawlink_call_tool --tool "hubspot_list_contacts" --params '{"limit": 10}'

# Search contacts
clawlink_call_tool --tool "hubspot_search_contacts" --params '{"query": "John Smith"}'

# Get a deal
clawlink_call_tool --tool "hubspot_get_deal" --params '{"deal_id": "YOUR_DEAL_ID"}'
```

## Authentication

All HubSpot tool calls are authenticated automatically by ClawLink using the user's connected HubSpot account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every HubSpot API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=hubspot and connect HubSpot.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `hubspot` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration hubspot
```

**Response:** Returns the live tool catalog for HubSpot.

### Reconnect

If HubSpot tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=hubspot
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration hubspot`

## Security & Permissions

- Access is scoped to CRM data the connected HubSpot user has permission to view and modify.
- **All write operations require explicit user confirmation.** Before executing any create, update, archive, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (archive/delete contacts, deals, companies) are marked as high-impact and must be confirmed.
- Batch operations affect multiple records and should be previewed before execution.

## Tool Reference

### Contacts

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_contacts` | List all contacts with pagination | Read |
| `hubspot_search_contacts` | Search contacts by query or property filters | Read |
| `hubspot_get_contact` | Get a contact by ID | Read |
| `hubspot_create_contact` | Create a new contact | Write |
| `hubspot_update_contact` | Update an existing contact's properties | Write |
| `hubspot_archive_contact` | Archive (soft delete) a contact | Write |
| `hubspot_batch_create_contacts` | Create multiple contacts in one request | Write |
| `hubspot_batch_update_contacts` | Update multiple contacts in one request | Write |
| `hubspot_create_contact_from_nl` | Create a contact from natural language description | Write |

### Companies

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_companies` | List all companies | Read |
| `hubspot_search_companies` | Search companies by query or property filters | Read |
| `hubspot_get_company` | Get a company by ID | Read |
| `hubspot_create_company` | Create a new company | Write |
| `hubspot_update_company` | Update a company's properties | Write |
| `hubspot_archive_company` | Archive a company | Write |
| `hubspot_batch_create_companies` | Create multiple companies in one request | Write |
| `hubspot_batch_update_companies` | Update multiple companies in one request | Write |

### Deals

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_deals` | List all deals with pagination | Read |
| `hubspot_search_deals` | Search deals by query or property filters | Read |
| `hubspot_get_deal` | Get a deal by ID | Read |
| `hubspot_create_deal` | Create a new deal | Write |
| `hubspot_update_deal` | Update a deal's properties | Write |
| `hubspot_archive_deal` | Archive a deal | Write |
| `hubspot_batch_create_deals` | Create multiple deals in one request | Write |
| `hubspot_batch_update_deals` | Update multiple deals in one request | Write |
| `hubspot_create_deal_from_nl` | Create a deal from natural language description | Write |

### Pipelines

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_pipelines` | List all deal pipelines | Read |
| `hubspot_get_pipeline` | Get a specific pipeline's stages | Read |
| `hubspot_create_pipeline` | Create a new deal pipeline | Write |
| `hubspot_update_pipeline` | Update a pipeline's stages or settings | Write |
| `hubspot_delete_pipeline` | Delete a deal pipeline | Write |
| `hubspot_audit_pipeline_changes` | Get audit log of pipeline changes | Read |

### Tickets

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_tickets` | List all tickets | Read |
| `hubspot_search_tickets` | Search tickets by query or property filters | Read |
| `hubspot_get_ticket` | Get a ticket by ID | Read |
| `hubspot_create_ticket` | Create a new ticket | Write |
| `hubspot_update_ticket` | Update a ticket's properties | Write |
| `hubspot_archive_ticket` | Archive a ticket | Write |
| `hubspot_batch_create_tickets` | Create multiple tickets in one request | Write |

### Products & Line Items

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_products` | List all products | Read |
| `hubspot_get_product` | Get a product by ID | Read |
| `hubspot_create_product` | Create a new product | Write |
| `hubspot_update_product` | Update a product's properties | Write |
| `hubspot_archive_product` | Archive a product | Write |
| `hubspot_list_line_items` | List all line items | Read |
| `hubspot_get_line_item` | Get a line item by ID | Read |
| `hubspot_create_line_item` | Create a new line item | Write |
| `hubspot_update_line_item` | Update a line item's properties | Write |
| `hubspot_archive_line_item` | Archive a line item | Write |

### Associations

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_create_association` | Create a labeled association between two CRM records | Write |
| `hubspot_list_associations` | List all associations for a record | Read |
| `hubspot_delete_association` | Remove an association between two records | Write |

### Properties

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_contact_properties` | List all contact properties | Read |
| `hubspot_list_company_properties` | List all company properties | Read |
| `hubspot_list_deal_properties` | List all deal properties | Read |
| `hubspot_create_property` | Create a new custom property | Write |
| `hubspot_update_property` | Update a custom property | Write |
| `hubspot_archive_property` | Archive a custom property | Write |
| `hubspot_create_property_group` | Create a new property group | Write |
| `hubspot_update_property_group` | Update a property group | Write |
| `hubspot_archive_property_group` | Archive a property group | Write |

### Quotes

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_quotes` | List all quotes | Read |
| `hubspot_get_quote` | Get a quote by ID | Read |
| `hubspot_create_quote` | Create a new quote | Write |
| `hubspot_update_quote` | Update a quote | Write |
| `hubspot_archive_quote` | Archive a quote | Write |
| `hubspot_batch_create_quotes` | Create multiple quotes in one request | Write |
| `hubspot_batch_update_quotes` | Update multiple quotes in one request | Write |

### Marketing Emails

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_marketing_emails` | List all marketing emails | Read |
| `hubspot_get_marketing_email` | Get a marketing email by ID | Read |
| `hubspot_create_marketing_email` | Create a new marketing email | Write |
| `hubspot_update_marketing_email` | Update a marketing email | Write |
| `hubspot_clone_marketing_email` | Clone an existing marketing email | Write |
| `hubspot_delete_marketing_email` | Permanently delete a marketing email | Write |
| `hubspot_create_draft_version` | Create or update a draft version of a marketing email | Write |
| `hubspot_get_ab_variation` | Get A/B test variation for a marketing email | Read |
| `hubspot_create_ab_variation` | Create an A/B test variation | Write |

### Campaigns

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_campaigns` | List all marketing campaigns | Read |
| `hubspot_get_campaign` | Get a campaign by ID | Read |
| `hubspot_create_campaign` | Create a new marketing campaign | Write |
| `hubspot_update_campaign` | Update a campaign | Write |
| `hubspot_delete_campaign` | Delete a campaign | Write |

### Workflows

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_workflows` | List all workflows | Read |
| `hubspot_get_workflow` | Get a workflow by ID | Read |
| `hubspot_create_workflow` | Create a new workflow | Write |
| `hubspot_update_workflow` | Update a workflow's settings or actions | Write |
| `hubspot_delete_workflow` | Delete a workflow | Write |
| `hubspot_enroll_in_workflow` | Enroll a contact in a workflow | Write |

### Tasks & Notes

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_tasks` | List all tasks | Read |
| `hubspot_get_task` | Get a task by ID | Read |
| `hubspot_create_task` | Create a new task | Write |
| `hubspot_update_task` | Update a task | Write |
| `hubspot_archive_task` | Archive a task | Write |
| `hubspot_create_note` | Create a note on a CRM record | Write |

### Engagement (Emails, Calls, Meetings)

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_engagements` | List all engagements (emails, calls, meetings) | Read |
| `hubspot_create_engagement` | Create an engagement record | Write |
| `hubspot_get_engagement` | Get an engagement by ID | Read |

### Owners & Teams

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_owners` | List all HubSpot owners | Read |
| `hubspot_get_owner` | Get a specific owner by ID | Read |
| `hubspot_list_teams` | List all teams | Read |
| `hubspot_get_team` | Get a team by ID | Read |
| `hubspot_create_team` | Create a new team | Write |
| `hubspot_update_team` | Update a team | Write |
| `hubspot_delete_team` | Delete a team | Write |

### Import & Export

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_list_imports` | List all import jobs | Read |
| `hubspot_get_import` | Get status and details of an import | Read |
| `hubspot_create_import` | Create a new CRM import job | Write |
| `hubspot_cancel_import` | Cancel an active import | Write |
| `hubspot_fetch_import_errors` | Get error details for a failed import | Read |

### GDPR

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_delete_contact_gdpr` | Permanently delete a contact and associated data | Write |
| `hubspot_delete_company_gdpr` | Permanently delete a company and associated data | Write |
| `hubspot_delete_deal_gdpr` | Archive a deal (GDPR permanent delete not supported for deals) | Write |

### Account & Configuration

| Tool | Description | Mode |
|------|-------------|------|
| `hubspot_get_account_info` | Get current account info (email, hub ID, user details) | Read |
| `hubspot_list_owners` | List all owners | Read |

## Code Examples

### List recent contacts

```bash
clawlink_call_tool --tool "hubspot_list_contacts" \
  --params '{
    "limit": 20,
    "properties": ["firstname", "lastname", "email", "phone"]
  }'
```

### Search contacts by email

```bash
clawlink_call_tool --tool "hubspot_search_contacts" \
  --params '{
    "query": "john.smith@example.com"
  }'
```

### Create a new deal

```bash
clawlink_call_tool --tool "hubspot_create_deal" \
  --params '{
    "properties": {
      "dealname": "Enterprise Contract",
      "amount": "50000",
      "dealstage": "qualifiedtobuy",
      "pipeline": "default"
    }
  }'
```

### Create a contact from natural language

```bash
clawlink_call_tool --tool "hubspot_create_contact_from_nl" \
  --params '{
    "description": "John Smith works as CTO at Acme Corp, his email is john@acme.com and phone is 555-0100"
  }'
```

### Create a note on a contact

```bash
clawlink_call_tool --tool "hubspot_create_note" \
  --params '{
    "engagement": {
      "active": true,
      "type": "NOTE"
    },
    "metadata": {
      "body": "Discussed Q4 renewal. Customer interested in upgrading to enterprise plan."
    },
    "associations": {
      "contact_ids": ["CONTACT_ID"]
    }
  }'
```

### Archive a contact

```bash
clawlink_call_tool --tool "hubspot_archive_contact" \
  --params '{
    "contact_id": "YOUR_CONTACT_ID"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm HubSpot is connected.
2. Call `clawlink_list_tools --integration hubspot` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `hubspot`.
5. If no HubSpot tools appear, direct the user to https://claw-link.dev/dashboard?add=hubspot.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → search → get → call                                 │
│                                                             │
│  Example: List contacts → Search → Get details → Show        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview → User approves            │
│           → Execute create/update/archive                    │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Contact, company, deal, and ticket IDs are stable HubSpot internal IDs — use them directly in API calls.
- Properties use internal names (e.g., `dealname`, `amount`, `closedate`) not display labels.
- Dates must be in ISO 8601 format (e.g., `2024-03-15`).
- Batch operations support up to 100 records per request.
- `create_X_from_nl` tools use an LLM to parse natural language into the correct property payload.
- Archiving is a soft delete — records move to the recycling bin and can often be restored.
- GDPR permanent deletion erases contact data per compliance requirements.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration hubspot`. |
| Missing connection | HubSpot is not connected. Direct the user to https://claw-link.dev/dashboard?add=hubspot. |
| `RESOURCE_NOT_FOUND` | Record does not exist. Check the ID. |
| `INVALID_PROPERTY_VALUE` | Property value doesn't match expected format. Check property definitions. |
| `INVALID_ARGUMENT` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `hubspot`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [HubSpot API Documentation](https://developers.hubspot.com/docs/overview)
- [CRM API Reference](https://developers.hubspot.com/docs/api/crm/contacts)
- [Deals API Reference](https://developers.hubspot.com/docs/api/crm/deals)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=hubspot-ops
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=hubspot-ops)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)