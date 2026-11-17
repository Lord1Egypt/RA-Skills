---
name: oo-cloudflare-r2
description: "Cloudflare R2 (cloudflare.com). Use this skill for ANY Cloudflare R2 request — reading, creating, updating, and deleting data. Whenever a task involves Cloudflare R2, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cloudflare R2"
  author: "OOMOL"
  version: "1.0.12"
  services: ["cloudflare_r2"]
  icon: "https://static.oomol.com/logo/third-party/Cloudflare.svg"
---

# Cloudflare R2

Operate **Cloudflare R2** through your OOMOL-connected account. This skill calls the `cloudflare_r2` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cloudflare R2. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cloudflare_r2" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cloudflare_r2" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_custom_domain` — Attach a custom domain from a Cloudflare zone to an R2 bucket. [write]
- `create_bucket` — Create an R2 bucket in a Cloudflare account. [write]
- `create_event_notification_rules` — Add event notification rules that send R2 bucket events to a Cloudflare Queue. [write]
- `create_temporary_access_credentials` — Create short-lived S3-compatible credentials scoped to one R2 bucket and optionally to prefixes or objects. [write]
- `delete_bucket` — Delete an R2 bucket by name. [destructive]
- `delete_bucket_cors_policy` — Delete the bucket-level CORS policy for an R2 bucket. [destructive]
- `delete_custom_domain` — Detach a custom domain from an R2 bucket. [destructive]
- `delete_event_notification_rules` — Delete event notification rules bound to one queue. Deletes every rule for the queue when ruleIds is omitted. [destructive]
- `delete_object` — Delete one R2 object by key. [destructive]
- `delete_objects` — Delete a list of R2 objects by key in one request. [destructive]
- `delete_objects_by_prefix` — Start a background job that deletes every object under a key prefix, or empties the whole bucket. [destructive]
- `disable_sippy` — Disable Sippy on an R2 bucket. [destructive]
- `download_object` — Download one R2 object and upload it to connector transit storage.
- `enable_sippy` — Enable Sippy so that objects missing from the R2 bucket are copied on demand from a source bucket on AWS S3, Google Cloud Storage, an S3-compatible service, or Azure Blob Storage. [write]
- `generate_presigned_url` — Generate a pre-signed R2 URL for one GET, PUT, or HEAD request using a custom API token credential.
- `get_account_metrics` — Get object count and storage usage metrics across all R2 buckets in the account. Metrics may lag behind the latest data.
- `get_bucket` — Get one R2 bucket by name.
- `get_bucket_cors_policy` — Fetch the bucket-level CORS policy for an R2 bucket.
- `get_bucket_job` — Get the current status of one R2 bucket background job.
- `get_bucket_lifecycle` — Get the object lifecycle rules of an R2 bucket.
- `get_bucket_local_uploads` — Get whether local uploads are enabled, which writes objects to the nearest region before replicating to the primary region.
- `get_bucket_lock` — Get the object lock rules of an R2 bucket.
- `get_custom_domain` — Get the settings of one custom domain attached to an R2 bucket.
- `get_event_notification_rules` — Get the event notification rules that send R2 bucket events to one queue.
- `get_managed_domain` — Get the r2.dev managed domain and its public access state for an R2 bucket.
- `get_sippy_config` — Get the Sippy incremental migration configuration of an R2 bucket.
- `list_accounts` — List Cloudflare accounts visible to the current credential.
- `list_bucket_jobs` — List background jobs for an R2 bucket, such as prefix delete jobs.
- `list_buckets` — List the R2 buckets in a Cloudflare account.
- `list_custom_domains` — List the custom domains attached to an R2 bucket.
- `list_event_notification_rules` — List every event notification rule of an R2 bucket grouped by target queue.
- `list_objects` — List objects in an R2 bucket with optional prefix, delimiter grouping, and cursor pagination.
- `put_object` — Upload one R2 object from a public URL, plain text, or base64-encoded content. [destructive]
- `update_bucket` — Update mutable R2 bucket properties such as default storage class or jurisdiction. [write]
- `update_bucket_cors_policy` — Replace the bucket-level CORS policy for an R2 bucket. [destructive]
- `update_bucket_lifecycle` — Replace the object lifecycle rules of an R2 bucket with the given rule set. [destructive]
- `update_bucket_local_uploads` — Enable or disable local uploads for an R2 bucket. [destructive]
- `update_bucket_lock` — Replace the object lock rules of an R2 bucket with the given rule set. [destructive]
- `update_custom_domain` — Update the public access, TLS version, or cipher settings of a custom domain. [write]
- `update_managed_domain` — Enable or disable public access to an R2 bucket through its r2.dev domain. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cloudflare R2 state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cloudflare R2 is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential, OAuth2) at:

  ```text
  https://console.oomol.com/connections/cloudflare_r2
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Cloudflare R2 homepage: https://www.cloudflare.com
- API documentation: https://developers.cloudflare.com/r2/api/s3/api/
