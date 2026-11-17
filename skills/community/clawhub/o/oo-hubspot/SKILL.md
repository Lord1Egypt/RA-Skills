---
name: oo-hubspot
description: "HubSpot (hubspot.com). Use this skill for ANY HubSpot request — reading, creating, and updating data. Whenever a task involves HubSpot, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "HubSpot"
  author: "OOMOL"
  version: "1.0.6"
  services: ["hubspot"]
  icon: "https://static.oomol.com/logo/third-party/HubSpot.svg"
---

# HubSpot

Operate **HubSpot** through your OOMOL-connected account. This skill calls the `hubspot` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected HubSpot. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "hubspot" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "hubspot" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_company` — Create a HubSpot company with the provided properties and optional associations. [write]
- `create_contact` — Create a HubSpot contact with the provided properties and optional associations. [write]
- `create_deal` — Create a HubSpot deal with the provided properties and optional associations. [write]
- `get_campaign_analytics` — Get HubSpot campaign analytics for one or more campaigns.
- `get_campaign_asset_metrics` — Get metrics and properties for CRM objects associated with a HubSpot campaign.
- `get_campaign_asset_types` — List HubSpot asset type names available as campaign assets.
- `get_campaign_contacts_by_type` — Fetch paginated HubSpot contact IDs for a campaign filtered by attribution type.
- `get_company` — Get a HubSpot company by record ID or by a custom idProperty value.
- `get_contact` — Get a HubSpot contact by record ID or by a custom idProperty value.
- `get_crm_objects` — Fetch one or more HubSpot CRM objects by ID through the MCP server.
- `get_deal` — Get a HubSpot deal by record ID or by a custom idProperty value.
- `get_properties` — Get full HubSpot property definitions for an object type.
- `get_property` — Get a single HubSpot property definition for an MCP-supported object type.
- `get_user_details` — Get the authenticated HubSpot MCP user's account and access details.
- `list_properties` — List or search HubSpot property definitions for an MCP-supported object type.
- `manage_crm_objects` — Create or update HubSpot CRM records or activities through the MCP server. [write]
- `search_companies` — Search HubSpot companies with optional filters, sorting, and selected properties.
- `search_contacts` — Search HubSpot contacts with optional filters, sorting, and selected properties.
- `search_crm_objects` — Search and filter HubSpot CRM records for any object type supported by the MCP server.
- `search_deals` — Search HubSpot deals with optional filters, sorting, and selected properties.
- `search_owners` — Find HubSpot CRM record owners by name, email, or owner ID.
- `search_properties` — Find HubSpot property definitions for an object type using keyword search.
- `submit_feedback` — Send feedback about the HubSpot MCP server experience to HubSpot. [write]
- `update_company` — Update a HubSpot company by record ID or by a custom idProperty value. [write]
- `update_contact` — Update a HubSpot contact by record ID or by a custom idProperty value. [write]
- `update_deal` — Update a HubSpot deal by record ID or by a custom idProperty value. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change HubSpot state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — HubSpot is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/hubspot
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- HubSpot homepage: https://www.hubspot.com
- API documentation: https://developers.hubspot.com/docs/api/overview
