---
name: oo-cloudflare
description: "Cloudflare (cloudflare.com). Use this skill for ANY Cloudflare request — reading, creating, updating, and deleting data. Whenever a task involves Cloudflare, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cloudflare"
  author: "OOMOL"
  version: "1.0.0"
  services: ["cloudflare"]
  icon: "https://static.oomol.com/logo/third-party/cloudflare.svg"
---

# Cloudflare

Operate **Cloudflare** through your OOMOL-connected account. This skill calls the `cloudflare` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cloudflare. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cloudflare" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cloudflare" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_custom_domain` — Attach a custom domain from a Cloudflare zone to an R2 bucket. [write]
- `attach_worker_domain` — Attach a custom domain to a Worker service. [write]
- `cancel_build` — Cancel a queued or running Workers Builds job. [destructive]
- `create_bucket` — Create an R2 bucket in a Cloudflare account. [write]
- `create_dns_record` — Create a DNS record inside a Cloudflare zone. [write]
- `create_event_notification_rules` — Add event notification rules that send R2 bucket events to a Cloudflare Queue. [write]
- `create_kv_namespace` — Create a Workers KV namespace for application data. [write]
- `create_manual_build` — Start a Workers Builds job from a configured trigger and branch or commit. [write]
- `create_pages_domain` — Attach a custom domain to a Pages project. Inspect its validation status and configure the required DNS records separately. [write]
- `create_pages_project` — Create a Pages project. Omit source for Direct Upload; use official project configuration fields for Git integration and Functions bindings. [write]
- `create_routing_rule` — Create a Cloudflare Email Routing rule in a zone. Forward actions require verified destination addresses. [write]
- `create_temporary_access_credentials` — Create short-lived S3-compatible credentials scoped to one R2 bucket and optionally to prefixes or objects. [write]
- `create_worker` — Create a Cloudflare Worker using the Workers beta API. [write]
- `create_worker_route` — Attach a Worker to a zone route pattern, or create an exclusion route by omitting scriptName. [write]
- `create_zone` — Create a Cloudflare zone and return its assigned nameservers. Registrar nameserver changes are a separate step. [write]
- `delete_bucket` — Delete an R2 bucket by name. [destructive]
- `delete_bucket_cors_policy` — Delete the bucket-level CORS policy for an R2 bucket. [destructive]
- `delete_custom_domain` — Detach a custom domain from an R2 bucket. [destructive]
- `delete_dns_record` — Delete one DNS record from a Cloudflare zone. [destructive]
- `delete_event_notification_rules` — Delete event notification rules bound to one queue. Deletes every rule for the queue when ruleIds is omitted. [destructive]
- `delete_kv_namespace` — Delete a Workers KV namespace and all its keys. [destructive]
- `delete_kv_value` — Delete one key from a Workers KV namespace. [destructive]
- `delete_object` — Delete one R2 object by key. [destructive]
- `delete_objects` — Delete a list of R2 objects by key in one request. [destructive]
- `delete_objects_by_prefix` — Start a background job that deletes every object under a key prefix, or empties the whole bucket. [destructive]
- `delete_pages_deployment` — Delete a Pages deployment. [destructive]
- `delete_pages_domain` — Detach a Pages custom domain. [destructive]
- `delete_pages_project` — Delete a Pages project. [destructive]
- `delete_routing_rule` — Delete a Cloudflare Email Routing rule from a zone. [destructive]
- `delete_worker` — Delete a Cloudflare Worker and its associated resources using the Workers beta API. [destructive]
- `delete_worker_domain` — Detach a Worker custom domain. [destructive]
- `delete_worker_route` — Delete a Worker route from a zone. [destructive]
- `delete_worker_script` — Delete a Cloudflare Worker script. [destructive]
- `delete_worker_script_secret` — Delete a secret binding from a Cloudflare Worker script. [destructive]
- `deploy_pages_site` — Deploy a prebuilt Pages site from a public ZIP URL. The archive root is the site root. Uploads assets in batches and submits the deployment; use get_pages_deployment to wait for completion. Connector limits: 512 MiB compressed and expanded, 20,000 files, 25 MiB per file. Include compiled _worker.js or _worker.bundle for Pages Functions. [write]
- `disable_sippy` — Disable Sippy on an R2 bucket. [destructive]
- `download_object` — Download one R2 object and upload it to connector transit storage.
- `edit_worker` — Partially update a Cloudflare Worker using the Workers beta API while leaving omitted fields unchanged. [write]
- `enable_sippy` — Enable Sippy so that objects missing from the R2 bucket are copied on demand from a source bucket on AWS S3, Google Cloud Storage, an S3-compatible service, or Azure Blob Storage. [write]
- `generate_presigned_url` — Generate a pre-signed R2 URL for one GET, PUT, or HEAD request using a custom API token credential.
- `get_account_metrics` — Get object count and storage usage metrics across all R2 buckets in the account. Metrics may lag behind the latest data.
- `get_bucket` — Get one R2 bucket by name.
- `get_bucket_cors_policy` — Fetch the bucket-level CORS policy for an R2 bucket.
- `get_bucket_job` — Get the current status of one R2 bucket background job.
- `get_bucket_lifecycle` — Get the object lifecycle rules of an R2 bucket.
- `get_bucket_local_uploads` — Get whether local uploads are enabled, which writes objects to the nearest region before replicating to the primary region.
- `get_bucket_lock` — Get the object lock rules of an R2 bucket.
- `get_build` — Get the current status and outcome of one Workers Builds job.
- `get_build_logs` — Get one page of log lines for a Workers Builds job.
- `get_custom_domain` — Get the settings of one custom domain attached to an R2 bucket.
- `get_dns_record` — Get one DNS record from a Cloudflare zone.
- `get_event_notification_rules` — Get the event notification rules that send R2 bucket events to one queue.
- `get_html_content` — Render a URL or raw HTML with Cloudflare Browser Run and return the fully rendered HTML content.
- `get_json` — Render a URL or raw HTML with Cloudflare Browser Run and extract structured JSON from the page.
- `get_kv_value` — Read a Workers KV value as text or base64 for binary data.
- `get_links` — Render a URL or raw HTML with Cloudflare Browser Run and return links discovered on the page.
- `get_managed_domain` — Get the r2.dev managed domain and its public access state for an R2 bucket.
- `get_markdown` — Render a URL or raw HTML with Cloudflare Browser Run and return the page content as Markdown.
- `get_pages_deployment` — Get a Pages deployment and its current processing status.
- `get_pages_domain` — Read Pages custom domain validation and certificate status.
- `get_pages_project` — Read a Pages project and its deployment configuration.
- `get_sippy_config` — Get the Sippy incremental migration configuration of an R2 bucket.
- `get_worker` — Get one Worker by Worker ID using the Workers beta API.
- `get_worker_script_content` — Fetch the raw source content for a Cloudflare Worker script.
- `get_worker_script_secret` — Get one secret binding attached to a Cloudflare Worker script.
- `get_worker_script_settings` — Get Worker metadata and configuration for a Cloudflare Worker script.
- `get_zone` — Get one Cloudflare zone by zone ID.
- `get_zone_dns_settings` — Read the DNS settings of a Cloudflare zone.
- `get_zone_setting` — Read one Cloudflare zone setting, such as SSL mode or cache configuration.
- `list_accounts` — List Cloudflare accounts visible to the current credential.
- `list_bucket_jobs` — List background jobs for an R2 bucket, such as prefix delete jobs.
- `list_buckets` — List the R2 buckets in a Cloudflare account.
- `list_build_triggers` — List Workers Builds triggers configured for one Worker script tag.
- `list_builds` — List Workers Builds jobs for one Worker script tag.
- `list_custom_domains` — List the custom domains attached to an R2 bucket.
- `list_destination_addresses` — List Cloudflare Email Routing destination addresses and their verification status.
- `list_dns_records` — List DNS records inside one Cloudflare zone.
- `list_event_notification_rules` — List every event notification rule of an R2 bucket grouped by target queue.
- `list_kv_keys` — List keys and metadata in a Workers KV namespace.
- `list_kv_namespaces` — List Workers KV namespaces in an account.
- `list_objects` — List objects in an R2 bucket with optional prefix, delimiter grouping, and cursor pagination.
- `list_pages_deployments` — List deployments for a Pages project.
- `list_pages_domains` — List custom domains attached to a Pages project.
- `list_pages_projects` — List Cloudflare Pages projects.
- `list_routing_rules` — List Cloudflare Email Routing rules for a zone or account.
- `list_worker_domains` — List Worker custom domains in an account.
- `list_worker_routes` — List Worker routes for a zone.
- `list_worker_script_secrets` — List secret bindings attached to a Cloudflare Worker script.
- `list_worker_scripts` — List Worker scripts in a Cloudflare account.
- `list_workers` — List Workers in a Cloudflare account using the Workers beta API.
- `list_zones` — List the Cloudflare zones visible to the current API token.
- `patch_worker_script_settings` — Patch Worker metadata and configuration for a Cloudflare Worker script. [write]
- `put_kv_value` — Write a Workers KV value with optional expiration and metadata. [write]
- `put_object` — Upload one R2 object from a public URL, plain text, or base64-encoded content. [destructive]
- `put_worker_script_content` — Replace only the content of a Cloudflare Worker script without changing metadata. [write]
- `put_worker_script_secret` — Add or replace a secret_text binding on a Cloudflare Worker script. [write]
- `rename_kv_namespace` — Rename a Workers KV namespace. [write]
- `rollback_pages_deployment` — Roll back a Pages project to a previous production deployment. [write]
- `scrape_elements` — Render a URL or raw HTML with Cloudflare Browser Run and scrape selected HTML elements.
- `search_worker_scripts` — Search Worker scripts in a Cloudflare account by name or script tag.
- `update_bucket` — Update mutable R2 bucket properties such as default storage class or jurisdiction. [write]
- `update_bucket_cors_policy` — Replace the bucket-level CORS policy for an R2 bucket. [destructive]
- `update_bucket_lifecycle` — Replace the object lifecycle rules of an R2 bucket with the given rule set. [destructive]
- `update_bucket_local_uploads` — Enable or disable local uploads for an R2 bucket. [destructive]
- `update_bucket_lock` — Replace the object lock rules of an R2 bucket with the given rule set. [destructive]
- `update_custom_domain` — Update the public access, TLS version, or cipher settings of a custom domain. [write]
- `update_dns_record` — Patch one DNS record inside a Cloudflare zone. [write]
- `update_managed_domain` — Enable or disable public access to an R2 bucket through its r2.dev domain. [destructive]
- `update_pages_project` — Update Pages project configuration using official API fields, including deployment_configs for environment variables and bindings. [write]
- `update_routing_rule` — Replace a Cloudflare Email Routing rule in a zone. [destructive]
- `update_worker` — Replace a Cloudflare Worker using the Workers beta API, setting omitted fields to API defaults. [write]
- `update_worker_route` — Update the pattern and Worker for a zone route. [write]
- `upload_worker_script` — Create or replace a Cloudflare Worker script by uploading a module bundle as multipart/form-data. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cloudflare state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cloudflare is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key, OAuth2) at:

  ```text
  https://console.oomol.com/connections/cloudflare
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Cloudflare homepage: https://www.cloudflare.com
- API documentation: https://developers.cloudflare.com/api/
