---
name: pipedrive
description: "Pipedrive: Manage Pipedrive sales workflows: discover fields and users, search CRM records, create and update deals, persons, organizations, activities, products, leads, and notes, move records through pipelines and stages. Use when an agent needs pipedrive, capture and convert inbound leads, create and update deals contacts and organizations, move deals through pipeline stages, schedule follow up calls and log notes, convert lead, lead id, data through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/pipedrive
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/pipedrive"}}
---
# Pipedrive

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Put your Pipedrive CRM on autopilot. Connect your account and let your AI assistant turn inbound interest into closed deals — capturing leads, creating contacts and organizations, building deals and advancing them through your pipeline, scheduling follow-up calls, logging notes, and attaching proposals automatically. Ask in plain language to find any record, surface stalled deals, route a lead to the right rep, or trigger downstream automations the moment something changes — and skip the manual data entry that eats your selling time.

## Product Instructions
### Pipedrive

Manage deals, persons, organizations, activities, products, leads, notes, pipelines, stages, and file attachments in Pipedrive.

#### Base rules

- Connection and access checks are handled by the platform.
- Writes require the matching permission scope: `add` for create, `edit` for update, `delete` for delete. Reads are allowed by default.
- `data` is a pass-through JSON body for writes. Convenience fields (`title`, `name`, `value`, `subject`, `content`) are merged underneath `data`; keys in `data` win.
- `options` is a pass-through query-param dict. It can only fill gaps — the dispatcher's params always win. It cannot change the URL or HTTP verb.
- Pagination: v2 actions use `cursor` + `limit` (max 500). v1 actions use `start` + `limit`. Responses expose `additional_data.next_cursor` (v2) or `additional_data.pagination` (v1).
- Every response is wrapped in `{"action": "...", "result": <raw Pipedrive body>}`.

#### Public aliases

- `organization_id` is the public AgentPMT field. The connector maps it to Pipedrive `org_id` for deal, person, activity, notes, and files actions that require `org_id`. Lead and search actions that document `organization_id` keep that spelling.
- `include` is the public AgentPMT field for extra returned fields. The connector maps it to Pipedrive `include_fields`.
- Deal `value` can be sent as a number or as `{ "amount": 5000, "currency": "USD" }`. The object form is accepted for compatibility and normalized to numeric `value` plus `currency` for deal create/update. Lead `value` remains `{ "amount": 5000, "currency": "USD" }`.
- `data` wins over convenience fields. If raw `data` supplies `org_id`, `value`, or `currency`, that raw intent is preserved. Unsupported `organization_id` in a body is normalized to `org_id` only for actions that require `org_id`.

#### Discovery flow

1. `who_am_i` — confirm connection, company, locale.
2. `list_fields` with `module` in `{deals, persons, organizations, activities, products}` — discover field names and hash keys for custom fields.
3. `list_pipelines` + `list_stages` — find `pipeline_id` / `stage_id`.
4. `search_records` or `item_search` — look up records by term.
5. Read → update → verify.

#### Generic CRUD (deal / person / organization / activity / product)

All five core resources share a single set of six verbs and a `resource` parameter.

```json
{"action":"list_records","resource":"deal","limit":50,"pipeline_id":1,"status":"open"}
{"action":"get_record","resource":"deal","deal_id":42,"include":["products_count"]}
{"action":"create_record","resource":"deal","title":"Acme website","value":{"amount":5000,"currency":"USD"},"person_id":10}
{"action":"create_record","resource":"deal","title":"Acme website","value":5000,"data":{"currency":"USD"},"person_id":10,"organization_id":20}
{"action":"update_record","resource":"deal","deal_id":42,"data":{"stage_id":3,"status":"won"}}
{"action":"delete_record","resource":"deal","deal_id":42}
{"action":"search_records","resource":"deal","term":"Acme","fields":["title"],"limit":25}

{"action":"create_record","resource":"person","name":"Jane Doe","data":{"emails":[{"value":"jane@acme.com","primary":true}]}}
{"action":"search_records","resource":"person","term":"jane@acme.com","fields":["email"]}

{"action":"create_record","resource":"organization","name":"Acme Corp","data":{"address":"1 Main St"}}

{"action":"create_record","resource":"activity","subject":"Intro call","data":{"type":"call","due_date":"2026-05-01","due_time":"15:00","deal_id":42}}

{"action":"create_record","resource":"product","name":"Consulting hour","data":{"prices":[{"currency":"USD","price":250}]}}
```

Required primary field for `create_record` by resource:
- `deal` → `title`
- `person` / `organization` / `product` → `name`
- `activity` → `subject`

`search_records` is not supported for `activity` (use `list_records` with filters).

#### Leads

`list_leads`, `get_lead`, `create_lead`, `update_lead`, `delete_lead` run on v1 (UUIDs). `search_leads` and `convert_lead` run on v2.

```json
{"action":"list_leads","limit":50,"owner_id":3}
{"action":"get_lead","lead_id":"a1b2c3d4-..."}
{"action":"create_lead","title":"Acme — inbound","person_id":10,"value":{"amount":1000,"currency":"USD"}}
{"action":"update_lead","lead_id":"a1b2c3d4-...","data":{"label_ids":["hot"]}}
{"action":"delete_lead","lead_id":"a1b2c3d4-..."}
{"action":"search_leads","term":"Acme"}
{"action":"convert_lead","lead_id":"a1b2c3d4-..."}
```

#### Notes

```json
{"action":"list_notes","deal_id":42,"limit":50}
{"action":"get_note","note_id":123}
{"action":"create_note","content":"Called Jane — follow up Tuesday","deal_id":42}
{"action":"update_note","note_id":123,"content":"Updated summary"}
{"action":"delete_note","note_id":123}
```

#### Pipelines & stages (read-only)

```json
{"action":"list_pipelines"}
{"action":"get_pipeline","pipeline_id":1}
{"action":"list_stages","pipeline_id":1}
{"action":"get_stage","stage_id":3}
```

#### Global search & metadata

```json
{"action":"item_search","term":"Acme","item_types":["deal","person","organization"]}
{"action":"list_fields","module":"deals"}
{"action":"list_users"}
{"action":"who_am_i"}
```

#### Files

File actions integrate with the AgentPMT File Manager. Upload bytes to File Manager first (via the file-management tool), then pass the resulting `file_id` here for `upload_file`. For `download_file`, Pipedrive-hosted bytes are pulled from Pipedrive and stored in File Manager under the caller's budget; the response returns the new File Manager `file_id` and a signed URL. Google Drive remote attachments created by `link_remote_file` are not Pipedrive-hosted bytes: use `get_file` or `list_files` to read `remote_id`, then use the Google Drive tool's `download_file_to_storage` action with that file id.

```json
{"action":"list_files","deal_id":42}
{"action":"get_file","pipedrive_file_id":7}
{"action":"download_file","pipedrive_file_id":7}
{"action":"upload_file","file_id":"<file-manager-file-id>","deal_id":42,"file_name_override":"proposal.pdf"}
{"action":"link_remote_file","remote_location":"googledrive","remote_id":"<drive-file-id>","deal_id":42}
{"action":"update_file","pipedrive_file_id":7,"file_name_override":"proposal-v2.pdf","file_description":"Signed version"}
{"action":"delete_file","pipedrive_file_id":7}
```

`upload_file` requires **exactly one** association id: `deal_id`, `person_id`, `organization_id`, `activity_id`, `lead_id`, or `product_id`.

`link_remote_file` uses Pipedrive's remote-file item contract and supports **exactly one** of `deal_id`, `person_id`, or `organization_id`.

#### Webhooks

Subscribe an external `subscription_url` (n8n webhook, Zapier, your own server) to Pipedrive change events. Pipedrive POSTs to that URL when matching records are created, changed, or deleted.

- `event_action`: `create`, `change`, `delete`, or `*` (all).
- `event_object`: `activity`, `deal`, `lead`, `note`, `organization`, `person`, `pipeline`, `product`, `stage`, `user`, or `*`.
- Combine action + object for the event you want (e.g. `create` + `deal` fires on every new deal).
- `webhook_version` is `"2.0"` by default — prefer 2.0 for new subscriptions.

```json
{"action":"list_webhooks"}
{"action":"create_webhook","subscription_url":"<https-webhook-url>","event_action":"change","event_object":"deal","webhook_name":"deal-change-relay"}
{"action":"create_webhook","subscription_url":"<https-webhook-url>","event_action":"*","event_object":"lead"}
{"action":"delete_webhook","webhook_id":123}
```

`create_webhook` requires `add` permission. `delete_webhook` requires `delete` permission. `list_webhooks` is read-only.

#### Response shape

Every call returns:
```json
{"action":"<action>","result":{"success":true,"data":..., "additional_data":...}}
```

`additional_data.next_cursor` (v2) / `additional_data.pagination.next_start` (v1) drive pagination.

## When To Use
- Use this skill for `Pipedrive` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: pipedrive, capture and convert inbound leads, create and update deals contacts and organizations, move deals through pipeline stages, schedule follow up calls and log notes, convert lead, lead id, data.
- Supported action names: `convert_lead`, `create_lead`, `create_note`, `create_record`, `create_webhook`, `delete_file`, `delete_lead`, `delete_note`, `delete_record`, `delete_webhook`, `download_file`, `get_file`, `get_lead`, `get_note`, `get_pipeline`, `get_record`, `get_stage`, `item_search`, `link_remote_file`, `list_fields`, `list_files`, `list_leads`, `list_notes`, `list_pipelines`, `list_records`, `list_stages`, `list_users`, `list_webhooks`, `search_leads`, `search_records`, `update_file`, `update_lead`, `update_note`, `update_record`, `upload_file`, `who_am_i`.

## Use Cases
- Capture and convert inbound leads
- Create and update deals contacts and organizations
- Move deals through pipeline stages
- Schedule follow-up calls and log notes
- Search any deal contact or lead
- Attach proposals and contracts from File Manager
- Generate pipeline hygiene and stalled-deal reports
- Trigger automations when CRM records change
- Read and write custom fields
- Forecast open pipeline value

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `36`.
x402 availability: not enabled for this product.

- `convert_lead` (action slug: `convert-lead`): Convert a lead by UUID. Price: `5` credits. Parameters: `data`, `lead_id`, `options`.
- `create_lead` (action slug: `create-lead`): Create a lead. Requires add permission and title plus person_id or organization_id. Price: `5` credits. Parameters: `data`, `options`, `organization_id`, `owner_id`, `person_id`, `title`, `value`.
- `create_note` (action slug: `create-note`): Create a note linked to one record. Requires add permission. Price: `5` credits. Parameters: `content`, `data`, `deal_id`, `lead_id`, `options`, `organization_id`, `person_id`.
- `create_record` (action slug: `create-record`): Create one core resource record. Requires add permission. Price: `5` credits. Parameters: `data`, `deal_id`, `name`, `options`, `organization_id`, `owner_id`, `person_id`, `pipeline_id`, plus 5 more.
- `create_webhook` (action slug: `create-webhook`): Subscribe an HTTPS URL to Pipedrive change events. Requires add permission. Price: `5` credits. Parameters: `event_action`, `event_object`, `options`, `subscription_url`, `user_id`, `webhook_name`, `webhook_version`.
- `delete_file` (action slug: `delete-file`): Delete a Pipedrive file. Requires delete permission. Price: `5` credits. Parameters: `pipedrive_file_id`.
- `delete_lead` (action slug: `delete-lead`): Delete a lead by UUID. Requires delete permission. Price: `5` credits. Parameters: `lead_id`, `options`.
- `delete_note` (action slug: `delete-note`): Delete a note by id. Requires delete permission. Price: `5` credits. Parameters: `note_id`, `options`.
- `delete_record` (action slug: `delete-record`): Delete one core resource record. Requires delete permission. Price: `5` credits. Parameters: `activity_id`, `deal_id`, `options`, `organization_id`, `person_id`, `product_id`, `resource`.
- `delete_webhook` (action slug: `delete-webhook`): Delete a Pipedrive webhook subscription. Requires delete permission. Price: `5` credits. Parameters: `options`, `webhook_id`.
- `download_file` (action slug: `download-file`): Download a Pipedrive file into AgentPMT File Manager. Price: `5` credits. Parameters: `attachment_expiration_minutes`, `ingest_expiration_days`, `pipedrive_file_id`.
- `get_file` (action slug: `get-file`): Fetch Pipedrive file metadata by id. Price: `5` credits. Parameters: `options`, `pipedrive_file_id`.
- `get_lead` (action slug: `get-lead`): Fetch one lead by UUID. Price: `5` credits. Parameters: `lead_id`, `options`.
- `get_note` (action slug: `get-note`): Fetch one note by id. Price: `5` credits. Parameters: `note_id`, `options`.
- `get_pipeline` (action slug: `get-pipeline`): Fetch one pipeline by id. Price: `5` credits. Parameters: `options`, `pipeline_id`.
- `get_record` (action slug: `get-record`): Fetch one core resource record by id. Price: `5` credits. Parameters: `activity_id`, `custom_fields`, `deal_id`, `include`, `options`, `organization_id`, `person_id`, `product_id`, plus 1 more.
- `get_stage` (action slug: `get-stage`): Fetch one stage by id. Price: `5` credits. Parameters: `options`, `stage_id`.
- `item_search` (action slug: `item-search`): Search across Pipedrive item types by term. Price: `5` credits. Parameters: `cursor`, `exact_match`, `fields`, `item_types`, `limit`, `options`, `search_for_related_items`, `term`.
- `link_remote_file` (action slug: `link-remote-file`): Link a Google Drive file to a Pipedrive deal, person, or organization. Requires add permission plus an active Google Drive integration in Pipedrive. Price: `5` credits. Parameters: `deal_id`, `file_name_override`, `organization_id`, `person_id`, `remote_id`, `remote_location`.
- `list_fields` (action slug: `list-fields`): List field metadata for deals, persons, organizations, activities, or products. Price: `5` credits. Parameters: `cursor`, `limit`, `module`, `options`.
- `list_files` (action slug: `list-files`): List files with optional record filters. Price: `5` credits. Parameters: `activity_id`, `deal_id`, `lead_id`, `limit`, `options`, `organization_id`, `person_id`, `product_id`, plus 3 more.
- `list_leads` (action slug: `list-leads`): List leads with filters and pagination. Price: `5` credits. Parameters: `filter_id`, `limit`, `options`, `organization_id`, `owner_id`, `person_id`, `sort_by`, `sort_direction`, plus 1 more.
- `list_notes` (action slug: `list-notes`): List notes with optional record filters. Price: `5` credits. Parameters: `deal_id`, `lead_id`, `limit`, `options`, `organization_id`, `person_id`, `sort_by`, `sort_direction`, plus 2 more.
- `list_pipelines` (action slug: `list-pipelines`): List pipelines. Price: `5` credits. Parameters: `cursor`, `limit`, `options`.
- `list_records` (action slug: `list-records`): List one core resource: deal, person, organization, activity, or product. Price: `5` credits. Parameters: `cursor`, `custom_fields`, `deal_id`, `filter_id`, `include`, `limit`, `options`, `organization_id`, plus 9 more.
- `list_stages` (action slug: `list-stages`): List stages, optionally filtered by pipeline_id. Price: `5` credits. Parameters: `cursor`, `limit`, `options`, `pipeline_id`.
- `list_users` (action slug: `list-users`): List Pipedrive users. Price: `5` credits. Parameters: `options`.
- `list_webhooks` (action slug: `list-webhooks`): List Pipedrive webhook subscriptions. Price: `5` credits. Parameters: `options`, `user_id`.
- `search_leads` (action slug: `search-leads`): Search leads by term. Price: `5` credits. Parameters: `cursor`, `exact_match`, `fields`, `include`, `limit`, `options`, `term`.
- `search_records` (action slug: `search-records`): Search deal, person, organization, or product records by term. Activity is not searchable. Price: `5` credits. Parameters: `cursor`, `exact_match`, `fields`, `include`, `limit`, `options`, `organization_id`, `person_id`, plus 3 more.
- `update_file` (action slug: `update-file`): Rename or update a Pipedrive file description. Requires edit permission. Price: `5` credits. Parameters: `file_description`, `file_name_override`, `pipedrive_file_id`.
- `update_lead` (action slug: `update-lead`): Update a lead by UUID. Requires edit permission. Price: `5` credits. Parameters: `data`, `lead_id`, `options`, `title`, `value`.
- `update_note` (action slug: `update-note`): Update a note by id. Requires edit permission. Price: `5` credits. Parameters: `content`, `data`, `note_id`, `options`.
- `update_record` (action slug: `update-record`): Update one core resource record. Requires edit permission. Price: `5` credits. Parameters: `activity_id`, `data`, `deal_id`, `name`, `options`, `organization_id`, `person_id`, `product_id`, plus 4 more.
- `upload_file` (action slug: `upload-file`): Upload an AgentPMT File Manager file to Pipedrive as an attachment. Requires add permission. Price: `5` credits. Parameters: `activity_id`, `deal_id`, `file_id`, `file_name_override`, `lead_id`, `organization_id`, `person_id`, `product_id`.
- `who_am_i` (action slug: `who-am-i`): Return the connected Pipedrive user and company details. Price: `5` credits. Parameters: `options`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "pipedrive"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "pipedrive"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "pipedrive"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "pipedrive"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "pipedrive"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "pipedrive"
  }
}
```

## Call This Tool
Product slug: `pipedrive`

Marketplace page: https://www.agentpmt.com/marketplace/pipedrive

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Pipedrive",
    "arguments": {
      "action": "convert_lead",
      "data": {},
      "lead_id": "example lead id",
      "options": {}
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "pipedrive",
  "parameters": {
    "action": "convert_lead",
    "data": {},
    "lead_id": "example lead id",
    "options": {}
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `convert_lead` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/pipedrive
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
