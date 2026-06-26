---
name: oo-apaleo
description: "apaleo (apaleo.com). Use this skill for ANY apaleo request — reading, creating, updating, and deleting data. Whenever a task involves apaleo, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "apaleo"
  author: "OOMOL"
  version: "1.0.1"
  services: ["apaleo"]
  icon: "https://static.oomol.com/logo/third-party/Apaleo.svg"
---

# apaleo

Operate **apaleo** through your OOMOL-connected account. This skill calls the `apaleo` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected apaleo. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "apaleo" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "apaleo" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `archive_property` — Archive a live property by ID. [write]
- `check_property_exists` — Check whether a property exists by ID.
- `check_unit_attribute_exists` — Check whether a unit attribute definition exists by ID.
- `check_unit_exists` — Check whether a unit exists by ID.
- `check_unit_group_exists` — Check whether a unit group exists by ID.
- `clone_property` — Clone an existing property into a new property with inventory and rate plans.
- `count_properties` — Return the total number of properties accessible to the connected apaleo account.
- `count_unit_groups` — Return the total number of unit groups matching the provided filters.
- `count_units` — Return the total number of units matching the provided filters.
- `create_multiple_units` — Create multiple units in a single bulk request. [write]
- `create_property` — Create a new property in apaleo. [write]
- `create_unit` — Create a new unit. [write]
- `create_unit_attribute` — Create a new unit attribute definition. [write]
- `create_unit_group` — Create a new unit group. [write]
- `delete_unit` — Delete a unit by ID. [destructive]
- `delete_unit_attribute` — Delete a unit attribute definition by ID. [destructive]
- `delete_unit_group` — Delete a unit group by ID. [destructive]
- `get_property` — Get one property by ID, including optional localized fields and expanded actions.
- `get_unit` — Get one unit by ID, including optional localized fields and expansions.
- `get_unit_attribute` — Get one unit attribute definition by ID.
- `get_unit_group` — Get one unit group by ID, including optional localized fields and expansions.
- `list_properties` — List properties accessible to the connected apaleo account, with optional status, archive, country, and expansion filters.
- `list_supported_countries` — List ISO country codes supported by apaleo property creation.
- `list_unit_attributes` — List unit attribute definitions for the current account.
- `list_unit_groups` — List unit groups with filters for property, unit group type, pagination, and embedded resources.
- `list_units` — List units with filters for property, unit group, attributes, occupancy, maintenance state, archive state, and expansions.
- `move_property_to_live` — Move a test property to live status. [write]
- `replace_unit_group` — Completely replace the mutable fields of an existing unit group. [write]
- `reset_property_data` — Delete all transactional data for a test property. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change apaleo state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — apaleo is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=apaleo
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- apaleo homepage: https://apaleo.com
