---
name: oo-google-bigquery
description: "Google BigQuery (cloud.google.com). Use this skill for ANY Google BigQuery request — reading, creating, updating, and deleting data. Whenever a task involves Google BigQuery, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google BigQuery"
  author: "OOMOL"
  version: "1.0.1"
  services: ["google_bigquery"]
  icon: "https://static.oomol.com/logo/third-party/google_bigquery.png"
---

# Google BigQuery

Operate **Google BigQuery** through your OOMOL-connected account. This skill calls the `google_bigquery` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google BigQuery. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "google_bigquery" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "google_bigquery" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_job` — Cancel a BigQuery job. [write]
- `create_dataset` — Create a BigQuery dataset. [write]
- `create_routine` — Create a BigQuery routine such as a user-defined function or stored procedure. [write]
- `create_table` — Create a BigQuery table. [write]
- `delete_dataset` — Delete a BigQuery dataset, optionally deleting contained tables when explicitly requested. [destructive]
- `delete_model` — Delete a BigQuery ML model from a dataset. [destructive]
- `delete_routine` — Delete a BigQuery routine from a dataset. [destructive]
- `delete_table` — Delete a BigQuery table from a dataset. [destructive]
- `get_dataset` — Retrieve BigQuery dataset metadata.
- `get_job` — Retrieve BigQuery job metadata.
- `get_model` — Retrieve BigQuery ML model metadata.
- `get_query_results` — Poll a BigQuery query job and return a page of results.
- `get_routine` — Retrieve BigQuery routine metadata.
- `get_table` — Retrieve BigQuery table metadata, including schema when available.
- `insert_all` — Insert a small batch of rows into a BigQuery table. [write]
- `list_datasets` — List BigQuery datasets in a Google Cloud project.
- `list_jobs` — List BigQuery jobs in a Google Cloud project.
- `list_models` — List BigQuery ML models in a dataset.
- `list_projects` — List Google Cloud projects accessible to BigQuery.
- `list_routines` — List BigQuery routines in a dataset.
- `list_table_data` — List rows from a BigQuery table.
- `list_tables` — List BigQuery tables in a dataset.
- `patch_dataset` — Patch BigQuery dataset metadata. [write]
- `patch_model` — Patch BigQuery ML model metadata such as friendly name, description, or labels. [write]
- `patch_table` — Patch BigQuery table metadata. [write]
- `query` — Run a BigQuery SQL query and return the first page of results.
- `start_extract_job_to_gcs` — Start an asynchronous BigQuery extract job to Cloud Storage objects. [write]
- `start_load_job_from_gcs` — Start an asynchronous BigQuery load job from Cloud Storage objects. [write]
- `start_query_job` — Start an asynchronous BigQuery query job. [write]
- `update_dataset` — Replace BigQuery dataset metadata with the supplied dataset resource fields. [write]
- `update_routine` — Replace BigQuery routine metadata and definition fields. [write]
- `update_table` — Replace BigQuery table metadata with the supplied table resource fields. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google BigQuery state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google BigQuery is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=google_bigquery
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Google BigQuery homepage: https://cloud.google.com/bigquery
