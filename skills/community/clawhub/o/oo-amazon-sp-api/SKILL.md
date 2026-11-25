---
name: oo-amazon-sp-api
description: "Amazon Selling Partner API (developer.amazonservices.com). Use this skill for ANY Amazon Selling Partner API request — reading, creating, updating, and deleting data. Whenever a task involves Amazon Selling Partner API, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Amazon Selling Partner API"
  author: "OOMOL"
  version: "1.0.0"
  services: ["amazon_sp_api"]
  icon: "https://static.oomol.com/logo/third-party/amazon_sp_api.svg"
---

# Amazon Selling Partner API

Operate **Amazon Selling Partner API** through your OOMOL-connected account. This skill calls the `amazon_sp_api` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Amazon Selling Partner API. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "amazon_sp_api" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "amazon_sp_api" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_listings_item` — Delete the seller's listing for one Amazon marketplace. The returned submission status indicates whether Amazon accepted the deletion for processing. [destructive]
- `get_catalog_item` — Retrieve an Amazon catalog item by ASIN with selected datasets for the requested marketplaces.
- `get_inventory_summaries` — Read FBA inventory summaries for one marketplace. For changed inventory, retain startDateTime when paging and reuse nextToken within 30 seconds. Inbound quantity changes are not detected by the incremental filter.
- `get_listings_item` — Retrieve a seller listing, including selected attributes, offers, live availability, and processing issues.
- `list_marketplace_participations` — List the connected seller's Amazon marketplaces and participation status in the connected region.
- `patch_listings_item` — Partially update listing attributes with add, replace, merge, or delete operations. Deleting attribute instances requires selector values. VALIDATION_PREVIEW checks without saving; ACCEPTED submissions may still develop processing issues. [write]
- `put_listings_item` — Create or fully update a seller listing. Omitted existing attributes may be removed; use patch_listings_item for partial edits. VALIDATION_PREVIEW checks the submission without saving it. [write]
- `search_catalog_items` — Search the Amazon catalog by product identifiers or keywords. Search pagination exposes at most 1,000 matching ASINs.
- `search_listings_items` — Search the seller's listings by identifiers, relationships, dates, status, or issue severity. Pagination exposes at most 1,000 matching SKUs.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Amazon Selling Partner API state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Amazon Selling Partner API is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/amazon_sp_api
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Amazon Selling Partner API homepage: https://developer.amazonservices.com/
- API documentation: https://developer-docs.amazon/sp-api/docs/overview
