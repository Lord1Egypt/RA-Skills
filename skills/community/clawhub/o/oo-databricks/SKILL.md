---
name: oo-databricks
description: "Databricks (databricks.com). Use this skill for ANY Databricks request — reading, creating, updating, and deleting data. Whenever a task involves Databricks, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Databricks"
  author: "OOMOL"
  version: "1.0.1"
  services: ["databricks"]
  icon: "https://static.oomol.com/logo/third-party/Databricks.svg"
---

# Databricks

Operate **Databricks** through your OOMOL-connected account. This skill calls the `databricks` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Databricks. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "databricks" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "databricks" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_run` — Cancel a Databricks job run by run ID. [write]
- `create_cluster` — Create a Databricks cluster from a raw official clusters create payload and return the new cluster ID. [write]
- `create_job` — Create a Databricks job from a raw official Jobs API settings object and return the new job ID. [write]
- `create_repo` — Create a Databricks workspace repo that links a Git remote into the connected workspace. [write]
- `create_secret_scope` — Create a Databricks secret scope with an optional backend configuration and initial manager principal. [write]
- `delete_job` — Delete a Databricks job by ID. [destructive]
- `delete_repo` — Delete a Databricks workspace repo by repo ID. [destructive]
- `delete_secret` — Delete one Databricks secret value from a Databricks secret scope. [destructive]
- `delete_secret_scope` — Delete a Databricks secret scope by scope name. [destructive]
- `edit_cluster` — Edit an existing Databricks cluster by cluster ID using a raw official clusters edit payload. [write]
- `get_cluster` — Get one Databricks cluster by cluster ID.
- `get_current_user` — Get the current Databricks workspace principal profile for the connected personal access token.
- `get_job` — Get one Databricks job, including its current settings and optional continuation page token.
- `get_run_by_id` — Get one Databricks job run by run ID.
- `get_run_output` — Get the output payload for one Databricks run, including notebook output or error details when available.
- `list_cluster_node_types` — List Databricks cluster node types that are available in the connected workspace region.
- `list_cluster_spark_versions` — List Databricks Runtime and Spark versions that can be used when creating or editing clusters.
- `list_cluster_zones` — List Databricks cluster availability zones for the connected workspace when the API is supported.
- `list_clusters` — List Databricks clusters with optional paging, filtering, and sorting controls from the official clusters API.
- `list_jobs` — List Databricks jobs in the connected workspace with optional pagination, name filtering, and task expansion.
- `list_runs` — List Databricks job runs with optional job, state, time-range, and pagination filters.
- `list_secret_scopes` — List Databricks secret scopes in the connected workspace.
- `list_secrets` — List Databricks secret metadata rows in one secret scope.
- `permanent_delete_cluster` — Permanently delete a Databricks cluster by cluster ID. [destructive]
- `put_secret` — Create or overwrite a Databricks secret value inside one Databricks secret scope. [write]
- `run_now_job` — Trigger an immediate run for a Databricks job with optional parameter maps and idempotency token.
- `start_cluster` — Start a terminated Databricks cluster by cluster ID. [write]
- `submit_run` — Submit a one-time Databricks run from a raw official Jobs API submit payload and return the run ID. [write]
- `update_job_by_id` — Update an existing Databricks job by ID using the official partial-update payload fields. [write]
- `update_repo` — Update a Databricks workspace repo by switching branch or tag, or by changing sparse-checkout settings. [write]
- `workspace_delete` — Delete a Databricks workspace object or directory by absolute path. [destructive]
- `workspace_export` — Export one Databricks workspace object as base64 content or direct text content, depending on the export mode.
- `workspace_get_status` — Get metadata for one Databricks workspace object by absolute path.
- `workspace_import` — Import base64 content into the Databricks workspace at an absolute path. [write]
- `workspace_list` — List the direct Databricks workspace objects under a workspace path.
- `workspace_mkdirs` — Create a Databricks workspace directory, including any missing parent directories.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Databricks state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Databricks is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=databricks
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Databricks homepage: https://www.databricks.com
