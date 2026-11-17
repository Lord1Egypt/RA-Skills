---
name: oo-chattermill
description: "Chattermill (chattermill.com). Use this skill for ANY Chattermill request — reading, creating, updating, and deleting data. Whenever a task involves Chattermill, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Chattermill"
  author: "OOMOL"
  version: "1.0.4"
  services: ["chattermill"]
  icon: "https://static.oomol.com/logo/third-party/chattermill.svg"
---

# Chattermill

Operate **Chattermill** through your OOMOL-connected account. This skill calls the `chattermill` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Chattermill. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "chattermill" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "chattermill" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_response` — Create a response in a Chattermill project. [write]
- `delete_response` — Permanently delete a Chattermill response by ID. [destructive]
- `get_attribute` — Get a Chattermill attribute by ID.
- `get_category` — Get a Chattermill category by ID.
- `get_data_source` — Get a Chattermill data source by ID.
- `get_data_type` — Get a Chattermill data type by ID.
- `get_metric` — Get a Chattermill metric value for a project.
- `get_project` — Get a Chattermill project by project ID.
- `get_response` — Get a single Chattermill response by ID.
- `get_tag` — Get a Chattermill tag by ID.
- `get_theme` — Get a Chattermill theme by ID.
- `list_attributes` — List attributes for a Chattermill project.
- `list_categories` — List categories for a Chattermill project.
- `list_custom_segments` — List custom segments for a Chattermill project.
- `list_data_sources` — List data sources for a Chattermill project.
- `list_data_types` — List data types for a Chattermill project.
- `list_projects` — List Chattermill projects accessible to the API key.
- `list_responses` — List responses for a Chattermill project with optional filters.
- `list_tags` — List tags for a Chattermill project.
- `list_themes` — List themes for a Chattermill project.
- `search_responses` — Search for Chattermill responses by response ID, user metadata, or custom criteria.
- `update_response` — Update user metadata, segments, or other response fields in Chattermill. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Chattermill state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Chattermill is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/chattermill
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Chattermill homepage: https://chattermill.com
- API documentation: https://apidocs.chattermill.com/
