---
name: oo-salesforce
description: "Salesforce (salesforce.com). Use this skill for ANY Salesforce request — reading, creating, updating, and deleting data. Whenever a task involves Salesforce, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Salesforce"
  author: "OOMOL"
  version: "1.0.2"
  services: ["salesforce"]
  icon: "https://static.oomol.com/logo/third-party/salesforce.svg"
---

# Salesforce

Operate **Salesforce** through your OOMOL-connected account. This skill calls the `salesforce` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Salesforce. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "salesforce" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "salesforce" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_bulk_job` — Abort a Bulk query or ingest job created by the authorized user. [destructive]
- `clone_report` — Clone an accessible report with optional metadata overrides such as name and folderId. [write]
- `convert_leads` — Convert up to 100 Leads using native Salesforce conversion. Query LeadStatus for a valid convertedStatus. Inspect each result for partial failures. Queue-owned leads require an explicit user ownerId. [write]
- `create_chatter_comment` — Reply to a Chatter feed element with structured message segments and optional file, article or shared-feed capabilities. [write]
- `create_chatter_feed_element` — Post a structured Chatter feed item to an explicitly chosen user, group or record. Supports native capabilities and previously uploaded files. [write]
- `create_record` — Create one standard or custom Salesforce record. [write]
- `create_record_tree` — Create parent-child record trees atomically: at most 200 records, five object types and five levels. [write]
- `create_records` — Create up to 200 records, preserving per-record success and errors. [write]
- `create_report` — Create and save a Salesforce report from an explicit report definition. [write]
- `delete_file` — Delete a ContentDocument and its associated versions and links. [destructive]
- `delete_record` — Delete one Salesforce record by object API name and record ID. [destructive]
- `delete_records` — Delete up to 200 Salesforce records, optionally rolling back on any failure. [destructive]
- `describe_invocable_action` — Describe an invocable action's inputs and outputs before calling it.
- `describe_list_view` — Describe a list view including its columns and SOQL query.
- `describe_object` — Describe an sObject, including fields, relationships, permissions and record types.
- `describe_report` — Get report, report-type and extended metadata including available filter fields.
- `download_file` — Download a Salesforce file version to OOMOL file transit; defaults to the latest published version.
- `execute_composite` — Execute up to 25 dependent Salesforce REST subrequests; up to five may be queries or collections. Can delete resources. [destructive]
- `execute_composite_graph` — Execute transactional Salesforce sObject graphs with at most 500 total subrequests and 75 graphs. Can delete resources. [destructive]
- `execute_quick_action` — Execute a global or object-specific quick action with field values and optional record context. [write]
- `get_apex_log` — Read the text of an Apex debug log. Log bodies may contain sensitive application data.
- `get_bulk_ingest_result` — Poll a Bulk ingest job and download successful, failed or unprocessed rows when terminal. JobComplete can still contain failed records.
- `get_bulk_query_result` — Poll a Bulk query; when complete, download one CSV page to file transit. Continue using nextLocator.
- `get_chatter_feed_element` — Get a complete Chatter feed element, preserving capabilities and structured message content.
- `get_current_user` — Retrieve the current authorized Salesforce identity.
- `get_dashboard` — Retrieve dashboard metadata, component data and status with optional filters.
- `get_dashboard_status` — Get refresh status for each dashboard component.
- `get_email_template` — Retrieve an email template's metadata, text body and HTML content.
- `get_file` — Get a Salesforce ContentDocument and its latest version reference.
- `get_knowledge_article` — Get a visible online Knowledge article by article ID or URL name, including custom layout content. Does not retrieve draft versions or custom binary file fields.
- `get_list_view_records` — Execute a list view and retrieve rows and display metadata.
- `get_lookup_suggestions` — Find allowed lookup candidates using the current user's context and dependent field values. Uses UI API POST; this operation only reads suggestions.
- `get_org_limits` — Get organization limits and remaining allocations; requires View Setup and Configuration permission.
- `get_picklist_values` — Get record-type-specific picklist values, including dependencies, through UI API.
- `get_quick_action_defaults` — Get default field values for an object-specific quick action, optionally in a record context.
- `get_record` — Retrieve a Salesforce record by object API name and record ID.
- `get_record_by_external_id` — Retrieve a record by an external ID field and value.
- `get_record_counts` — Get approximate record counts for selected objects or all available objects.
- `get_record_create_defaults` — Get user-specific default values, create layout and object metadata before creating a record. Does not guarantee that validation rules will accept a later write.
- `get_record_layout` — Read the page layout for an object and record type in create, edit or view mode.
- `get_records` — Retrieve up to 2000 records of one object in one request. Missing or inaccessible records return null in place.
- `get_related_records` — Traverse one or more Salesforce relationship API names from a record.
- `get_report_result` — Get the state and results of an asynchronous report. Empty factMap is a valid successful result.
- `get_tooling_record` — Read one Tooling API metadata record without modifying configuration.
- `invoke_action` — Invoke a standard action or custom Flow/Apex action. Dynamic actions may delete data or perform other destructive operations. [destructive]
- `link_file` — Link an existing file to a Salesforce record with an explicit sharing level. [write]
- `list_approval_processes` — List Classic approval process definitions, optionally filtered by object API name.
- `list_chatter_comments` — Read a full page of Chatter comments for a feed element; continue with the page token in nextPageUrl.
- `list_chatter_feed_elements` — Read a Chatter feed with native pagination, search and filters. Feed types support different query options; unsupported combinations are rejected. Embedded comments are previews only.
- `list_dashboards` — List recently viewed dashboards. Query the Dashboard object with SOQL for broader discovery.
- `list_deleted_records` — List deleted records within the retained delete log, at most 15 days; retain returned watermarks.
- `list_email_templates` — List accessible active email templates using SOQL; use query_more for subsequent pages.
- `list_file_shares` — List a file's ContentDocumentLink sharing records; use query_more for later pages.
- `list_invocable_actions` — Discover standard actions, custom action categories, or actions in a custom category.
- `list_knowledge_articles` — Search or browse visible online Knowledge articles by language, channel and categories. Results are summaries; get_knowledge_article retrieves content. Increment pageNumber for subsequent pages.
- `list_list_views` — List the views available for an sObject.
- `list_objects` — List sObjects available to the connected Salesforce user.
- `list_pending_approvals` — List pending Classic approval work items for yourself, yourself and your groups, or an explicit actor. Use query_more with nextRecordsUrl for subsequent pages; group scope does not imply all delegated approvals.
- `list_quick_actions` — List global quick actions or quick actions for a specified object.
- `list_record_files` — List files linked to a Salesforce record, including link IDs needed to unlink; use query_more for later pages.
- `list_reports` — List up to 200 recently viewed reports. For all accessible reports, query the Report object with SOQL.
- `list_updated_records` — List record IDs changed in a replication window within the last 30 days.
- `parameterized_search` — Search Salesforce without composing SOSL; supports all documented parameterized-search options.
- `query` — Execute read-only SOQL and return one page. Use query_more with nextRecordsUrl for subsequent pages.
- `query_more` — Retrieve the next page of a SOQL query using Salesforce's relative nextRecordsUrl.
- `refresh_dashboard` — Request a dashboard refresh; inspect get_dashboard_status before reading refreshed data. [write]
- `review_approval_requests` — Approve or reject Classic approval work items assigned to the current user. Each item can succeed or fail independently. [write]
- `run_report` — Run a report synchronously with optional temporary metadata overrides; does not save changes.
- `save_report` — Save report metadata changes. Salesforce invalidates and deletes running asynchronous jobs for this report when it is saved. [destructive]
- `search_records` — Search across Salesforce objects using SOSL.
- `send_email` — Send email through Salesforce emailSimple and return each action result; inspect isSuccess and errors. [write]
- `send_email_from_template` — Send a Salesforce template email with merge fields; requires a recipient Contact or Lead ID. [write]
- `submit_bulk_ingest` — Create, upload and submit a Bulk API 2.0 CSV job from a public URL. Supports delete and irreversible hardDelete; inspect per-record results. [destructive]
- `submit_bulk_query` — Submit an asynchronous Bulk API 2.0 SOQL query and return a versioned handle. [write]
- `submit_for_approval` — Submit records to Classic approval processes. Inspect each result for partial failures; use invoke_action for Flow approvals. [write]
- `submit_report` — Start an asynchronous report run and return a handle for get_report_result. [write]
- `tooling_query` — Query Salesforce Tooling metadata with SOQL SELECT, such as validation rules, Apex classes and logs. Requires the corresponding administrative permissions.
- `tooling_query_more` — Continue a Tooling SOQL query using its returned nextRecordsUrl.
- `unlink_file` — Delete one ContentDocumentLink without deleting the underlying file. [destructive]
- `update_record` — Update supplied fields on a Salesforce record; omitted fields remain unchanged. [write]
- `update_records` — Update up to 200 records, preserving per-record success and errors. [write]
- `upload_file` — Upload a file URL as a new Salesforce ContentVersion using streaming multipart data (up to 2 GB). Can add a version to an existing file. [write]
- `upsert_record` — Create or update one Salesforce record by an external ID field. Use updateOnly to prevent creation. [write]
- `upsert_records` — Upsert up to 200 records of one object using an external ID field. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Salesforce state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Salesforce is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/salesforce
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Salesforce homepage: https://www.salesforce.com
- API documentation: https://developer.salesforce.com/docs/platform/api-rest/guide/intro-rest.html
