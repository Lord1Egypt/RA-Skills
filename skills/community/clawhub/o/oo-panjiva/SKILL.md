---
name: oo-panjiva
description: "Panjiva (panjiva.com). Use this skill for ANY Panjiva request — reading, creating, and updating data. Whenever a task involves Panjiva, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Panjiva"
  author: "OOMOL"
  version: "1.0.2"
  services: ["panjiva"]
  icon: "https://static.oomol.com/logo/third-party/panjiva.svg"
---

# Panjiva

Operate **Panjiva** through your OOMOL-connected account. This skill calls the `panjiva` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Panjiva. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "panjiva" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "panjiva" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `batch_search_companies` — Submit multiple company searches as one downloadable batch. Poll get_batch_job_status with the returned job ID. [write]
- `bulk_rollup_shipments` — Submit a bulk shipment aggregation for JSONL or CSV download. Poll get_bulk_job_status with the returned job ID. [write]
- `bulk_search_shipments` — Submit a large shipment search for JSONL or CSV download. Poll get_bulk_job_status with the returned job ID. [write]
- `get_batch_job_status` — Check a batch company search job and retrieve its download URL when ready.
- `get_bulk_job_status` — Check a bulk shipment job and retrieve its download URL when ready.
- `get_company_network` — Retrieve a company's top buyers, suppliers and trade statistics from Panjiva.
- `get_data_source_metadata` — Discover searchable fields, filters, sort keys, metrics, dimensions and refinements for a Panjiva data source.
- `get_data_source_schema` — Retrieve native shipment record schemas for a Panjiva data source.
- `get_shipment_refinements` — List the most common values of selected shipment attributes for matching Panjiva records.
- `get_shipment_time_series` — Calculate shipment metrics aggregated by week, month, quarter or year.
- `list_data_sources` — List the Panjiva data sources available to the connected organization.
- `lookup_companies` — Retrieve Panjiva company entities by company IDs and identifier representation.
- `parse_hs_codes` — Identify HS codes from a product description using the Panjiva commodity coder. Optionally restrict the HS prefix and enable parser, manual rules or classifier methods; the first matching method supplies the results.
- `parse_many_hs_codes` — Call Panjiva's Parse Many commodity coder and return per-item HS codes and classifier metadata. The published request schema defines items as an object with description, optional marks and partial_hs; pass that documented object shape.
- `rollup_companies` — Aggregate trade records for selected companies into up to three grouping dimensions.
- `rollup_shipments` — Group matching shipments into up to three dimensions with metrics and optional time-series aggregation.
- `search_companies` — Find buyers and suppliers through matching Panjiva trade records, with company identity types and trade-role filtering.
- `search_hs_codes` — Search Harmonized System codes and US Harmonized Tariff Schedule descriptions.
- `search_shipments` — Search Panjiva import and export shipment records with filtering, sorting, pagination and optional metrics. Use bulk_search_shipments for larger result sets.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Panjiva state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Panjiva is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/panjiva
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Panjiva homepage: https://panjiva.com/
- API documentation: https://panjiva.com/api-guide/spec
